"""Deterministic verifier & trace-evidence builder for the Workflow Seed Library.

Every rule emitted by the Seed Pipeline is evaluated by the exact same
`evaluate_seed_rule(rule, evidence)` function during:
  1. Stage 2 Anti-Default Baseline Replay (proving baseline_pass == False);
  2. Post-run IF Evaluation in scoring/.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

TOOL_NORM: dict[str, str] = {
    "read": "file_read",
    "edit": "file_edit",
    "write": "file_write",
    "grep": "file_search",
    "glob": "file_glob",
    "working_directory": "cwd_inspect",
    "todo_write": "task_planning",
    "list_mcp_resources": "mcp_resource_list",
    "list_mcp_resource_templates": "mcp_template_list",
    "mcp__e2b__execute_python": "python_exec",
    "mcp__e2b__prepare_environment": "sandbox_prepare",
    "mcp__e2b__export_file": "file_export",
    "mcp__serper__google_search": "web_search",
    "bash": "shell_exec",
}

ALL_DSH_TOOLS: list[str] = [
    "file_read",
    "file_edit",
    "file_write",
    "file_search",
    "file_glob",
    "cwd_inspect",
    "task_planning",
    "mcp_resource_list",
    "mcp_template_list",
    "read_mcp_resource",
    "python_exec",
    "sandbox_prepare",
    "file_export",
    "web_search",
    "web_fetch",
    "image_search",
    "read_image",
    "create_goal",
    "get_goal",
    "update_goal",
    "subagent",
    "subagent_fork",
    "list_agents",
    "send_message",
    "interrupt_agent",
    "skill",
    "workflow",
    "exit_plan_mode",
]

READONLY_TOOLS = {
    "file_read",
    "file_glob",
    "file_search",
    "cwd_inspect",
    "web_search",
    "web_fetch",
    "mcp_resource_list",
    "mcp_template_list",
    "read_mcp_resource",
    "image_search",
    "read_image",
    "task_planning",
}

WRITE_TOOLS = {"file_write", "file_edit", "file_export"}

URL_RE = re.compile(r"https?://[^\s<>\"'\)\]\},`]+")

EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001F9FF"
    "\U0001FA00-\U0001FAFF"
    "\U00002600-\U000027BF"
    "]",
    flags=re.UNICODE,
)

PREAMBLE_PATTERNS = [
    re.compile(r"^\s*(i\s+now\s+have|based\s+on\s+(my|the)\s+(research|analysis|search|data)|here\s+is\s+(the|a|your)|sure[!,.]|certainly[!,.]|let\s+me\s+(summarize|present))", re.I),
    re.compile(r"^\s*(我已经|已为您|根据(您提供的|以上|查询|读取|搜索)|好的[，,！!。]|下面为您|以下是|经过(核查|检索|分析))"),
]

ERROR_RE = re.compile(
    r"(http\s*(error\s*)?403|status[_\s]*code[\"']?\s*[:=]\s*(403|404|429|500|502|503)|forbidden|traceback\s*\(most recent|econnrefused|timed?\s*out|error:\s*)",
    re.I,
)


def norm_tool(name: str) -> str:
    return TOOL_NORM.get(name, name)


def _parse_args(raw: Any) -> Any:
    if isinstance(raw, (dict, list)):
        return raw
    if isinstance(raw, str):
        s = raw.strip()
        if s.startswith("{") or s.startswith("["):
            try:
                return json.loads(s)
            except Exception:
                return {"raw": raw}
        return {"raw": raw}
    return {}


def _iter_strings(obj: Any):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, list):
        for item in obj:
            yield from _iter_strings(item)
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _iter_strings(v)


def normalize_url(url: str) -> str:
    url = url.strip().rstrip(".,;:!?)\"]'")
    try:
        parts = urlsplit(unquote(url))
        host = (parts.hostname or "").lower().rstrip(".")
        if host.startswith("www."):
            host = host[4:]
        path = parts.path.rstrip("/")
        query = f"?{parts.query}" if parts.query else ""
        return f"{host}{path}{query}".lower()
    except Exception:
        return url.lower()


def extract_urls(text: str) -> list[str]:
    return [m.group(0).rstrip(".,;:!?)\"]'") for m in URL_RE.finditer(text or "")]


def extract_host(url: str) -> str:
    try:
        host = (urlsplit(url).hostname or "").lower().rstrip(".")
        return host[4:] if host.startswith("www.") else host
    except Exception:
        return ""


def strip_code_fences(text: str) -> list[str]:
    lines: list[str] = []
    fence = None
    for line in (text or "").splitlines():
        m = re.match(r"^\s*(`{3,}|~{3,})", line)
        if m:
            ch = m.group(1)[0]
            fence = None if fence == ch else ch
            lines.append("")
        else:
            lines.append(line if fence is None else "")
    return lines


def detect_text_language_ratio(text: str) -> dict[str, float]:
    zh = len(re.findall(r"[\u4e00-\u9fff]", text or ""))
    en = len(re.findall(r"[A-Za-z]", text or ""))
    total = zh + en
    if total == 0:
        return {"zh_ratio": 0.0, "en_ratio": 0.0, "zh_chars": 0, "en_chars": 0}
    return {
        "zh_ratio": zh / total,
        "en_ratio": en / total,
        "zh_chars": zh,
        "en_chars": en,
    }


def has_markdown_table(text: str) -> bool:
    lines = strip_code_fences(text)
    for i in range(len(lines) - 1):
        if "|" in lines[i] and re.match(r"^\s*\|?[\s:-]+\|[\s|:-]*$", lines[i + 1]):
            return True
    return False


def has_markdown_lists(text: str) -> bool:
    for line in strip_code_fences(text):
        if re.match(r"^\s*([-*+]\s+|\d+\.\s+)", line):
            return True
    return False


def has_preamble(text: str) -> bool:
    for line in (text or "").splitlines():
        s = line.strip()
        if not s:
            continue
        return any(p.search(s) for p in PREAMBLE_PATTERNS)
    return False


def has_emoji(text: str) -> bool:
    return bool(EMOJI_RE.search(text or ""))


def build_evidence_from_trace(
    trace_json_path: Path | None,
    final_txt_path: Path | None = None,
    artifacts_dir: Path | None = None,
    user_query: str = "",
    fallback_fingerprint: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build normalized evidence dict from real DSH trace.json + final.txt + artifacts."""
    calls: list[dict[str, Any]] = []
    turns: list[dict[str, Any]] = []
    thinking_blocks: list[dict[str, Any]] = []
    tool_outputs_by_id: dict[str, str] = {}
    has_trace = False

    if trace_json_path and trace_json_path.is_file():
        has_trace = True
        raw = json.loads(trace_json_path.read_text(encoding="utf-8"))
        events = raw.get("trace", raw) if isinstance(raw, dict) else raw
        # First pass: index tool responses by tool_call_id
        for ev in events:
            if not isinstance(ev, dict):
                continue
            if ev.get("role") == "tool":
                tcid = ev.get("tool_call_id") or ev.get("id")
                content = ev.get("content", "")
                if isinstance(content, list):
                    content = "\n".join(str(x.get("text", x) if isinstance(x, dict) else x) for x in content)
                if tcid:
                    tool_outputs_by_id[str(tcid)] = str(content)

        # Second pass: build turns, calls, thinking
        turn_idx = 0
        for ev in events:
            if not isinstance(ev, dict) or ev.get("role") != "assistant":
                continue
            rc = str(ev.get("reasoning_content") or "")
            content = ev.get("content") or ""
            if isinstance(content, list):
                content = "\n".join(str(x.get("text", x) if isinstance(x, dict) else x) for x in content)
            tcs = ev.get("tool_calls") or []
            turn_calls: list[dict[str, Any]] = []
            for tc in tcs:
                fn_obj = tc.get("function") or {}
                raw_name = fn_obj.get("name") or tc.get("name") or ""
                name = norm_tool(str(raw_name))
                args = _parse_args(fn_obj.get("arguments") if "arguments" in fn_obj else tc.get("arguments"))
                tcid = str(tc.get("id") or "")
                output_text = tool_outputs_by_id.get(tcid, "")
                is_error = bool(ERROR_RE.search(output_text[:4000]))
                # Retain only compact evidence needed by verifiers to keep memory tiny across 98+ traces
                if name == "web_search":
                    compact_out = "\n".join(dict.fromkeys(extract_urls(output_text)))
                elif name in {"file_glob", "file_search", "cwd_inspect"}:
                    compact_out = output_text[:16384]
                else:
                    compact_out = ""
                call_rec = {
                    "index": len(calls),
                    "turn_index": turn_idx,
                    "name": name,
                    "raw_name": str(raw_name),
                    "args": args,
                    "output": compact_out,
                    "is_error": is_error,
                }
                calls.append(call_rec)
                turn_calls.append(call_rec)
            thinking_blocks.append(
                {
                    "turn_index": turn_idx,
                    "text": rc,
                    "length": len(rc.strip()),
                    "has_tool_calls": bool(turn_calls),
                    "is_final": not bool(turn_calls) and bool(str(content).strip()),
                }
            )
            turns.append(
                {
                    "turn_index": turn_idx,
                    "thinking": rc,
                    "thinking_len": len(rc.strip()),
                    "tool_calls": turn_calls,
                    "parallel_count": len(turn_calls),
                    "content": str(content),
                }
            )
            turn_idx += 1

    final_answer = ""
    if final_txt_path and final_txt_path.is_file():
        final_answer = final_txt_path.read_text(encoding="utf-8", errors="replace")
    elif turns:
        for t in reversed(turns):
            if t["content"].strip():
                final_answer = t["content"]
                break

    artifacts: list[dict[str, Any]] = []
    if artifacts_dir and artifacts_dir.is_dir():
        for p in sorted(artifacts_dir.rglob("*")):
            if p.is_file():
                rel = p.relative_to(artifacts_dir).as_posix()
                text_content = None
                if p.suffix.lower() in {".json", ".csv", ".txt", ".md", ".yaml", ".yml"} and p.stat().st_size <= 512_000:
                    try:
                        text_content = p.read_text(encoding="utf-8", errors="replace")
                    except OSError:
                        text_content = None
                artifacts.append({"path": rel, "ext": p.suffix.lower(), "content": text_content})

    # Synthetic fallback when Old 50 task has no trace.json (3 tasks)
    if not has_trace and fallback_fingerprint:
        fp_seq = fallback_fingerprint.get("tool_seq") or fallback_fingerprint.get("tool_sequence") or []
        fp_tools = fallback_fingerprint.get("tools_used") or []
        fp_counts = fallback_fingerprint.get("tool_counts") or {}
        if isinstance(fp_seq, list) and fp_seq:
            for idx, tname in enumerate(fp_seq):
                nm = norm_tool(str(tname))
                calls.append({"index": idx, "turn_index": idx, "name": nm, "raw_name": nm, "args": {}, "output": "", "is_error": False})
                turns.append({"turn_index": idx, "thinking": "x" * 200, "thinking_len": 200, "tool_calls": [calls[-1]], "parallel_count": 1, "content": ""})
        elif isinstance(fp_counts, dict) and fp_counts:
            first = norm_tool(str(fallback_fingerprint.get("first_tool") or ""))
            seq_names: list[str] = []
            if first:
                seq_names.append(first)
            for tname, cnt in fp_counts.items():
                nt = norm_tool(str(tname))
                rem = int(cnt) - (1 if nt == first and seq_names.count(nt) == 1 else 0)
                seq_names.extend([nt] * max(0, rem))
            for idx, nm in enumerate(seq_names):
                calls.append({"index": idx, "turn_index": idx, "name": nm, "raw_name": nm, "args": {}, "output": "", "is_error": False})
                turns.append({"turn_index": idx, "thinking": "x" * 200, "thinking_len": 200, "tool_calls": [calls[-1]], "parallel_count": 1, "content": ""})
        elif fp_tools:
            for idx, tname in enumerate(fp_tools):
                nm = norm_tool(str(tname))
                calls.append({"index": idx, "turn_index": idx, "name": nm, "raw_name": nm, "args": {}, "output": "", "is_error": False})
                turns.append({"turn_index": idx, "thinking": "x" * 200, "thinking_len": 200, "tool_calls": [calls[-1]], "parallel_count": 1, "content": ""})
        if not final_answer:
            # Synthesize structural markers from fingerprint tags
            rlen = int(fallback_fingerprint.get("reply_len") or 1200)
            tags = set(fallback_fingerprint.get("reply_format") or [])
            parts = []
            if "markdown_headings" in tags:
                parts.append("## Overview\n")
            if "markdown_table" in tags:
                parts.append("| A | B |\n|---|---|\n| 1 | 2 |\n")
            if "markdown_lists" in tags:
                parts.append("- item 1\n- item 2\n")
            body = "\n".join(parts)
            if len(body) < rlen:
                body += "a" * (rlen - len(body))
            final_answer = body
        for af in fallback_fingerprint.get("artifact_files") or []:
            artifacts.append({"path": str(af), "ext": Path(str(af)).suffix.lower(), "content": None})

    return {
        "has_real_trace": has_trace,
        "user_query": user_query,
        "final_answer": final_answer,
        "artifacts": artifacts,
        "trace": {
            "calls": calls,
            "turns": turns,
            "thinking": thinking_blocks,
        },
    }


def _extract_file_path_from_args(args: Any) -> str:
    if isinstance(args, dict):
        for k in ("path", "file_path", "filename", "file", "target_file"):
            v = args.get(k)
            if isinstance(v, str) and v.strip():
                return v.strip()
    return ""


def _extract_url_from_args(args: Any) -> str:
    if isinstance(args, dict):
        for k in ("url", "uri", "link", "href"):
            v = args.get(k)
            if isinstance(v, str) and v.strip():
                return v.strip()
    for s in _iter_strings(args):
        urls = extract_urls(s)
        if urls:
            return urls[0]
    return ""


def evaluate_seed_rule(rule: dict[str, Any], evidence: dict[str, Any]) -> bool:
    """Deterministically evaluate a single seed rule against evidence.

    Returns True iff the evidence satisfies the constraint.
    """
    if "all_of" in rule:
        return all(evaluate_seed_rule(sub, evidence) for sub in rule["all_of"])
    if "any_of" in rule:
        return any(evaluate_seed_rule(sub, evidence) for sub in rule["any_of"])

    op = rule.get("op")
    val = rule.get("value")
    trace = evidence.get("trace") or {}
    calls: list[dict[str, Any]] = trace.get("calls") or []
    turns: list[dict[str, Any]] = trace.get("turns") or []
    thinking_blocks: list[dict[str, Any]] = trace.get("thinking") or []
    final_answer: str = evidence.get("final_answer") or ""
    artifacts: list[dict[str, Any]] = evidence.get("artifacts") or []
    user_query: str = evidence.get("user_query") or ""

    # ------------------------------------------------------------------
    # 1. Stage Chains (first_occurrence_order)
    # ------------------------------------------------------------------
    if op == "workflow_stage_chain":
        # value: {"stages": [[tool1, tool2], [tool3], ...], "require_first_call_in_stage0": True}
        stages_tools: list[list[str]] = val["stages"]
        require_first = val.get("require_first_call_in_stage0", True)
        if not calls:
            return False
        if require_first and calls[0]["name"] not in set(stages_tools[0]):
            return False
        first_indices: list[int] = []
        for stage_set in stages_tools:
            allowed = set(stage_set)
            idx = next((i for i, c in enumerate(calls) if c["name"] in allowed), None)
            if idx is None:
                return False
            first_indices.append(idx)
        return all(first_indices[i] < first_indices[i + 1] for i in range(len(first_indices) - 1))

    # ------------------------------------------------------------------
    # 2. Universal Precondition Invariants
    # ------------------------------------------------------------------
    if op == "source_before_fetch":
        seen_urls = {normalize_url(u) for u in extract_urls(user_query)}
        seen_hosts = {extract_host(u) for u in extract_urls(user_query) if extract_host(u)}
        fetch_count = 0
        for c in calls:
            if c["name"] == "web_search":
                for u in extract_urls(c.get("output", "")):
                    seen_urls.add(normalize_url(u))
                    h = extract_host(u)
                    if h:
                        seen_hosts.add(h)
            elif c["name"] == "web_fetch":
                fetch_count += 1
                u = _extract_url_from_args(c.get("args"))
                if not u:
                    return False
                nu = normalize_url(u)
                # Strict match against prior search results or user_query URLs
                if nu not in seen_urls:
                    # Allow prefix match if search returned URL without query string or vice versa
                    if not any(nu.startswith(su) or su.startswith(nu) for su in seen_urls if len(su) >= 12):
                        return False
        return fetch_count > 0

    if op == "locate_before_read":
        discovered_tokens: set[str] = set()
        # Any filename explicitly mentioned in user_query is allowed directly
        prompt_lower = user_query.lower()
        read_count = 0
        for c in calls:
            if c["name"] in {"file_glob", "file_search", "cwd_inspect"}:
                out = c.get("output", "")
                for tok in re.findall(r"[\w./-]+\.[A-Za-z0-9]{1,8}", out):
                    discovered_tokens.add(tok.lower())
                    discovered_tokens.add(Path(tok).name.lower())
            elif c["name"] == "file_read":
                read_count += 1
                fp = _extract_file_path_from_args(c.get("args"))
                if not fp:
                    continue
                fp_low = fp.lower()
                base_low = Path(fp).name.lower()
                if base_low in prompt_lower or fp_low in prompt_lower:
                    continue
                if fp_low not in discovered_tokens and base_low not in discovered_tokens:
                    return False
        return read_count > 0

    if op == "readonly_before_write":
        min_ro = int((val or {}).get("min_readonly_calls", 2))
        if not calls:
            return False
        first_write_idx = next((i for i, c in enumerate(calls) if c["name"] in WRITE_TOOLS), None)
        if first_write_idx is None:
            return False
        # Turn 0 must not perform any write
        if calls[first_write_idx].get("turn_index", 0) == 0:
            return False
        ro_before = sum(1 for c in calls[:first_write_idx] if c["name"] in READONLY_TOOLS)
        return ro_before >= min_ro

    if op == "step_thinking_required":
        min_chars = int((val or {}).get("min_chars", 50))
        tool_turns = [t for t in turns if t.get("parallel_count", 0) > 0]
        if not tool_turns:
            return False
        return all(t.get("thinking_len", 0) >= min_chars for t in tool_turns)

    # ------------------------------------------------------------------
    # 3. Cadence, Parallelism & Resource Gates
    # ------------------------------------------------------------------
    if op == "max_parallel_calls":
        max_par = int((val or {}).get("max_parallel", 1))
        forbid_sub = bool((val or {}).get("forbid_subagent_bypass", True))
        if not turns:
            return False
        if any(t.get("parallel_count", 0) > max_par for t in turns):
            return False
        if forbid_sub and any(c["name"] in {"subagent", "subagent_fork"} for c in calls):
            return False
        return True

    if op == "periodic_plan_update":
        interval = int((val or {}).get("interval", 5))
        if not calls or calls[0]["name"] != "task_planning":
            return False
        since_plan = 0
        for c in calls[1:]:
            if c["name"] == "task_planning":
                since_plan = 0
            else:
                since_plan += 1
                if since_plan > interval:
                    return False
        return True

    if op == "tool_repeat_limit":
        target_tool = (val or {}).get("tool")  # None => applies to every tool
        max_run = int((val or {}).get("max_consecutive", 2))
        if not calls:
            return True
        run = 0
        prev = None
        for c in calls:
            nm = c["name"]
            if nm == prev:
                run += 1
            else:
                prev = nm
                run = 1
            if (target_tool is None or nm == target_tool) and run > max_run:
                return False
        return True

    if op == "error_retry_cap":
        max_retries = int((val or {}).get("max_consecutive_errors", 2))
        consec = 0
        last_sig = None
        for c in calls:
            if c.get("is_error"):
                url = _extract_url_from_args(c.get("args"))
                sig = (c["name"], extract_host(url) if url else "")
                consec = consec + 1 if sig == last_sig else 1
                last_sig = sig
                if consec > max_retries:
                    return False
            else:
                consec = 0
                last_sig = None
        return True

    if op == "tool_budget":
        target_tool = val["tool"]
        limit = int(val["max_calls"])
        cnt = sum(1 for c in calls if c["name"] == target_tool)
        return cnt <= limit

    if op == "tool_total_budget":
        limit = int(val["max_calls"])
        return len(calls) <= limit

    if op == "tool_forbidden":
        forbidden = set(val["tools"] if isinstance(val, dict) else val)
        return all(c["name"] not in forbidden for c in calls)

    if op == "tool_required_usage":
        req_tool = val["tool"]
        min_calls = int(val.get("min_calls", 1))
        require_no_err = bool(val.get("require_success", False))
        matched = [c for c in calls if c["name"] == req_tool and (not require_no_err or not c.get("is_error"))]
        return len(matched) >= min_calls

    if op == "sources_allowed":
        domains = [d.lower() for d in (val.get("domains") or [])]
        keywords = [k.lower() for k in (val.get("keywords") or [])]

        def _hits(text: str, is_search: bool = False) -> bool:
            low = unquote(text or "").lower()
            if is_search:
                low = re.sub(r"-site:[\w.-]+", "", low)
            for u in extract_urls(low):
                h = extract_host(u)
                if any(h == d or h.endswith("." + d) for d in domains):
                    return True
            if is_search:
                if any(k in low for k in keywords):
                    return True
                if any(d in low for d in domains):
                    return True
            return False

        if _hits(final_answer, is_search=False):
            return False
        for c in calls:
            is_s = "search" in c["name"]
            for s in _iter_strings(c.get("args")):
                if _hits(s, is_search=is_s):
                    return False
        return True

    # ------------------------------------------------------------------
    # 4. Conditional Branches & Milestones
    # ------------------------------------------------------------------
    if op == "min_sources_before_deliver":
        min_k = int((val or {}).get("min_sources", 2))
        deliver_tools = set((val or {}).get("deliver_tools", ["file_write", "file_export"]))
        first_del = next((i for i, c in enumerate(calls) if c["name"] in deliver_tools), None)
        if first_del is None:
            return False
        unique_sources: set[str] = set()
        for c in calls[:first_del]:
            if c.get("is_error"):
                continue
            if c["name"] == "web_fetch":
                u = _extract_url_from_args(c.get("args"))
                if u:
                    unique_sources.add("url:" + normalize_url(u))
            elif c["name"] == "file_read":
                fp = _extract_file_path_from_args(c.get("args"))
                if fp:
                    unique_sources.add("file:" + fp.lower())
        return len(unique_sources) >= min_k

    if op == "error_branch_protocol":
        err_heading = val.get("error_heading", "## 异常与替代路径")
        ok_heading = val.get("normal_heading", "## 正常核验记录")
        err_marker = val.get("error_thinking_marker", "[ERROR_ANALYSIS]")
        any_err = any(c.get("is_error") for c in calls)
        if any_err:
            has_h = err_heading in final_answer
            has_m = any(err_marker in (b.get("text") or "") for b in thinking_blocks)
            return has_h and has_m
        return ok_heading in final_answer and err_heading not in final_answer

    # ------------------------------------------------------------------
    # 5. Cognitive / Thinking Control
    # ------------------------------------------------------------------
    if op == "thinking_language":
        target_lang = val.get("language", "zh")
        min_ratio = float(val.get("min_ratio", 0.70))
        all_think = "\n".join(b.get("text", "") for b in thinking_blocks if b.get("text", "").strip())
        if len(all_think.strip()) < 20:
            return False
        ratios = detect_text_language_ratio(all_think)
        if target_lang == "zh":
            return ratios["zh_ratio"] >= min_ratio
        if target_lang == "en":
            return ratios["en_ratio"] >= min_ratio
        return False

    if op == "thinking_budget_total":
        max_chars = int(val["max_chars"])
        total = sum(int(b.get("length", 0)) for b in thinking_blocks)
        return 0 < total <= max_chars

    if op == "thinking_budget_per_step":
        max_chars = int(val["max_chars"])
        non_empty = [int(b.get("length", 0)) for b in thinking_blocks if int(b.get("length", 0)) > 0]
        if not non_empty:
            return False
        return all(n <= max_chars for n in non_empty)

    if op == "thinking_plan_before_act":
        marker = val.get("marker", "[PLAN]")
        first_tool_turn = next((t for t in turns if t.get("parallel_count", 0) > 0), None)
        if not first_tool_turn:
            return False
        txt = first_tool_turn.get("thinking", "")
        has_numbered = bool(re.search(r"(?m)(^|\s)1[\.\)、]", txt)) and bool(re.search(r"(?m)(^|\s)2[\.\)、]", txt))
        return marker in txt and has_numbered

    if op == "thinking_pre_final_verify":
        marker = val.get("marker", "[SELF_CHECK]")
        if not thinking_blocks:
            return False
        last_non_empty = next((b for b in reversed(thinking_blocks) if b.get("length", 0) > 0), None)
        if not last_non_empty:
            return False
        return marker in last_non_empty.get("text", "")

    # ------------------------------------------------------------------
    # 6. Artifact & Output Contracts
    # ------------------------------------------------------------------
    if op == "no_markdown_table":
        return bool(final_answer.strip()) and not has_markdown_table(final_answer)

    if op == "no_lists":
        return bool(final_answer.strip()) and not has_markdown_lists(final_answer)

    if op == "no_preamble":
        return bool(final_answer.strip()) and not has_preamble(final_answer)

    if op == "no_emoji":
        return bool(final_answer.strip()) and not has_emoji(final_answer)

    if op == "answer_length_lte":
        max_chars = int(val["max_chars"])
        return 0 < len(final_answer.strip()) <= max_chars

    if op == "headings_exact":
        expected: list[str] = val["headings"]
        found = [
            m.group(1).strip()
            for line in strip_code_fences(final_answer)
            for m in [re.match(r"^\s*##\s+(.+?)\s*$", line)]
            if m
        ]
        return found == expected

    if op == "json_valid_schema":
        required_keys: list[str] = val.get("required_keys", [])
        s = final_answer.strip()
        if s.startswith("```"):
            return False
        try:
            obj = json.loads(s)
        except Exception:
            return False
        if not isinstance(obj, dict):
            return False
        return all(k in obj and obj[k] not in (None, "", []) for k in required_keys)

    if op == "artifact_structured_file":
        target_path = val["path"]
        required_keys: list[str] = val.get("required_keys", [])
        # Check artifacts dir first; also check file_write tool calls as backup evidence
        for art in artifacts:
            if art["path"].rstrip("/") == target_path or art["path"].endswith("/" + target_path):
                if not required_keys:
                    return True
                try:
                    obj = json.loads(art.get("content") or "")
                    if isinstance(obj, dict) and all(k in obj for k in required_keys):
                        return True
                except Exception:
                    return False
        # Fallback: inspect file_write call payload if artifacts folder not captured
        for c in reversed(calls):
            if c["name"] == "file_write":
                fp = _extract_file_path_from_args(c.get("args"))
                if fp.endswith(target_path):
                    content = (c.get("args") or {}).get("content", "") if isinstance(c.get("args"), dict) else ""
                    if not required_keys:
                        return True
                    try:
                        obj = json.loads(content)
                        if isinstance(obj, dict) and all(k in obj for k in required_keys):
                            return True
                    except Exception:
                        return False
        return False

    if op == "citation_range":
        min_c = int(val["min"])
        max_c = int(val["max"])
        uniq = {normalize_url(u) for u in extract_urls(final_answer)}
        return min_c <= len(uniq) <= max_c

    raise ValueError(f"Unknown seed verifier op: {op}")
