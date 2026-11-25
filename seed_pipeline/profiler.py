"""Unified Task Loader & Zero-Manual-Labeling Task Capability Profiler.

Supports:
  - Old 50 tasks (baseline_fingerprint/benchmark_baseline_all_*.json + real traces)
  - New 48 NAQ tasks (dsh-runs/naq_48_company-deepseek-*/baseline_groups_naq48.json + real traces)
  - Any arbitrary raw query JSONL (with or without baseline traces)
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from .llm_enhancer import LLMEnhancer
from .verifiers import (
    ALL_DSH_TOOLS,
    build_evidence_from_trace,
    detect_text_language_ratio,
    extract_host,
    extract_urls,
    has_emoji,
    has_markdown_lists,
    has_markdown_table,
    has_preamble,
    norm_tool,
)

CODE_EXTS = {".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".cpp", ".c", ".h", ".go", ".rs", ".rb"}

PEEKING_REPO_DOMAINS = {
    "github.com",
    "raw.githubusercontent.com",
    "api.github.com",
    "patch-diff.githubusercontent.com",
    "gist.github.com",
    "huggingface.co",
    "datasets-server.huggingface.co",
}

COMPUTE_HINT_RE = re.compile(
    r"(预算|费用|总价|人均|计算|统计|比例|百分比|增长率|净利润|现金流|财报|方差|均值|排序|排名前|前\s*\d+|"
    r"内存|估算|基准|万条|维度|性能对比|吞吐|延迟|"
    r"budget|total\s+cost|calculate|compute|ratio|percentage|revenue|net\s+income|capex|cfo|median|average|"
    r"million|billion|memory|benchmark|estimate|fix\s+the\s+bug|unit\s+test|pytest|patch|astropy|django|sympy|scikit)",
    re.I,
)

CODE_MOD_HINT_RE = re.compile(
    r"(修复|修改代码|补丁|单元测试|提交\s*patch|fix\s+(the\s+)?(bug|issue|error)|implement\s+|refactor|pull\s+request|pytest|git\s+diff|swebench)",
    re.I,
)

FORMAT_LOCK_HINT_RE = re.compile(
    r"(严格只输出\s*json|only\s+output\s+valid\s+json|output\s+must\s+be\s+a\s+single\s+number|"
    r"return\s+only\s+the\s+(exact\s+)?(json|csv|xml))",
    re.I,
)

WEB_HINT_RE = re.compile(
    r"(最新|官网|调研|检索|搜一下|新闻|报告|排名|202\d|according\s+to|which\s+team|regular\s+season|"
    r"wikipedia|official\s+website|latest|benchmark|resale\s+report|index\s+of|who\s+won|what\s+year)",
    re.I,
)

DEFAULT_SYSTEM_PROMPT = (
    "You are an AI agent equipped with file, search, planning, and code execution tools. "
    "Solve the user's request accurately and thoroughly."
)


def _compute_rich_fingerprint(evidence: dict[str, Any], fallback_fp: dict[str, Any] | None = None) -> dict[str, Any]:
    trace = evidence.get("trace") or {}
    calls: list[dict[str, Any]] = trace.get("calls") or []
    turns: list[dict[str, Any]] = trace.get("turns") or []
    thinking: list[dict[str, Any]] = trace.get("thinking") or []
    final_answer: str = evidence.get("final_answer") or ""
    artifacts: list[dict[str, Any]] = evidence.get("artifacts") or []

    tool_counts = Counter(c["name"] for c in calls)
    max_par = max((t.get("parallel_count", 0) for t in turns), default=0)
    tool_turns = [t for t in turns if t.get("parallel_count", 0) > 0]
    zero_think_turns = sum(1 for t in tool_turns if t.get("thinking_len", 0) < 50)
    think_lens = [int(b.get("length", 0)) for b in thinking if int(b.get("length", 0)) > 0]
    all_think_text = "\n".join(b.get("text", "") for b in thinking if b.get("text", "").strip())
    think_lang_ratio = detect_text_language_ratio(all_think_text)
    if think_lang_ratio["zh_chars"] + think_lang_ratio["en_chars"] < 20:
        thinking_lang = "unknown"
    elif think_lang_ratio["zh_ratio"] >= 0.55:
        thinking_lang = "zh"
    elif think_lang_ratio["en_ratio"] >= 0.55:
        thinking_lang = "en"
    else:
        thinking_lang = "mixed"

    # Max consecutive tool repeat
    max_repeat_any = 0
    max_repeat_by_tool: dict[str, int] = {}
    prev_t, run = None, 0
    for c in calls:
        nm = c["name"]
        run = run + 1 if nm == prev_t else 1
        prev_t = nm
        if run > max_repeat_any:
            max_repeat_any = run
        if run > max_repeat_by_tool.get(nm, 0):
            max_repeat_by_tool[nm] = run

    # Consecutive errors
    max_consec_err = 0
    cur_err = 0
    any_error = False
    for c in calls:
        if c.get("is_error"):
            any_error = True
            cur_err += 1
            max_consec_err = max(max_consec_err, cur_err)
        else:
            cur_err = 0

    # Domains used in web_fetch / final_answer
    domain_counter: Counter[str] = Counter()
    for u in extract_urls(final_answer):
        h = extract_host(u)
        if h:
            domain_counter[h] += 1
    for c in calls:
        if c["name"] in {"web_fetch", "web_search"}:
            for u in extract_urls(json.dumps(c.get("args", ""), ensure_ascii=False)):
                h = extract_host(u)
                if h:
                    domain_counter[h] += 1
    if not domain_counter and fallback_fp:
        for d in fallback_fp.get("cited_source_domains") or fallback_fp.get("domains_used") or []:
            if isinstance(d, str) and d.strip():
                domain_counter[d.strip().lower()] += 1

    top_domains = [d for d, _ in domain_counter.most_common(10)]
    final_urls = {extract_host(u) + u for u in extract_urls(final_answer)}

    return {
        "has_real_trace": bool(evidence.get("has_real_trace")),
        "total_tool_calls": len(calls),
        "first_tool": calls[0]["name"] if calls else None,
        "tool_counts": dict(tool_counts),
        "tools_used": sorted(tool_counts.keys()),
        "max_parallel_calls": max_par,
        "tool_turn_count": len(tool_turns),
        "zero_think_turns": zero_think_turns,
        "total_think_chars": sum(think_lens),
        "max_step_think_chars": max(think_lens, default=0),
        "thinking_lang": thinking_lang,
        "thinking_zh_ratio": round(think_lang_ratio["zh_ratio"], 3),
        "max_repeat_any": max_repeat_any,
        "max_repeat_by_tool": max_repeat_by_tool,
        "any_tool_error": any_error,
        "max_consec_errors": max_consec_err,
        "domains_used": top_domains,
        "reply_len": len(final_answer.strip()),
        "has_table": has_markdown_table(final_answer),
        "has_lists": has_markdown_lists(final_answer),
        "has_preamble": has_preamble(final_answer),
        "has_emoji": has_emoji(final_answer),
        "artifact_count": len(artifacts),
        "citation_count": len(final_urls),
    }


def _default_deliverable_spec(query: str, query_lang: str, flags: dict[str, bool], task_type: str = "") -> tuple[str, list[str], list[str]]:
    lbl = (task_type + " " + query[:250]).lower()
    if any(k in lbl for k in ("travel", "出行", "旅行", "行程", "火车", "酒店", "景点")):
        fname = "output/itinerary_summary.json"
        keys = ["trip_overview", "budget_breakdown", "verification_notes"]
        headings = ["行程总览", "预算与交通核算", "核验说明"] if query_lang == "zh" else ["Trip Overview", "Budget Breakdown", "Verification Notes"]
    elif flags.get("needs_code_modification") or any(k in lbl for k in ("coding", "code", "bug", "swebench", "代码")):
        fname = "output/fix_summary.json"
        keys = ["root_cause", "modified_files", "verification_result"]
        headings = ["根因分析", "修改方案", "测试验证结果"] if query_lang == "zh" else ["Root Cause", "Code Changes", "Verification Results"]
    elif any(k in lbl for k in ("finance", "financial", "财务", "金融", "财报", "stock")):
        fname = "output/financial_metrics.json"
        keys = ["key_metrics", "calculation_basis", "final_conclusion"]
        headings = ["核心财务指标", "数据来源与计算依据", "最终结论"] if query_lang == "zh" else ["Key Metrics", "Calculation Basis", "Final Conclusion"]
    elif any(k in lbl for k in ("legal", "法律", "诉讼", "合同", "privacy")):
        fname = "output/legal_review.json"
        keys = ["legal_issues", "evidence_citations", "conclusion"]
        headings = ["核心争议点", "条款与证据引用", "审查结论"] if query_lang == "zh" else ["Key Issues", "Clause Citations", "Conclusion"]
    elif flags.get("needs_web_info"):
        fname = "output/evidence_summary.json"
        keys = ["answer_summary", "verified_sources", "verification_status"]
        headings = ["核心结论", "关键证据来源", "核验说明"] if query_lang == "zh" else ["Core Answer", "Verified Sources", "Verification Summary"]
    else:
        fname = "output/task_summary.json"
        keys = ["answer_summary", "key_evidence", "verification_status"]
        headings = ["核心结论", "关键依据", "核验说明"] if query_lang == "zh" else ["Core Answer", "Key Evidence", "Verification Notes"]
    return fname, keys, headings


def build_task_profile(
    task: dict[str, Any],
    evidence: dict[str, Any],
    llm: LLMEnhancer | None = None,
) -> dict[str, Any]:
    """Build zero-manual-labeling TaskCapabilityProfile for any task."""
    query = str(task.get("user_query") or "")
    attached_files = [str(x) for x in (task.get("attached_files") or [])]
    tools = sorted({norm_tool(str(t)) for t in (task.get("tools") or ALL_DSH_TOOLS)})
    tool_set = set(tools)
    fp = _compute_rich_fingerprint(evidence, task.get("baseline_fingerprint"))

    lang_r = detect_text_language_ratio(query)
    query_lang = "zh" if lang_r["zh_ratio"] >= 0.25 else "en"
    has_code_repo = any(Path(f).suffix.lower() in CODE_EXTS for f in attached_files)

    # Heuristic baseline for 5 binary semantic flags
    used = set(fp["tools_used"])
    tcounts = fp.get("tool_counts") or {}
    domains_used = [d.lower() for d in (fp.get("domains_used") or [])]
    non_peeking_domains = [
        d for d in domains_used if not any(d == pd or d.endswith("." + pd) for pd in PEEKING_REPO_DOMAINS)
    ]
    used_web_genuinely = bool({"web_search", "web_fetch"} & used) and (
        not attached_files or bool(non_peeking_domains)
    )
    needs_web = used_web_genuinely or (not attached_files and bool(WEB_HINT_RE.search(query)))
    needs_local = bool(attached_files) or bool({"file_read", "file_glob", "file_search"} & used)
    # Require >=2 python_exec calls or explicit compute/code signals so single exploratory sandbox call doesn't mislabel pure policy QA
    needs_compute = (
        int(tcounts.get("python_exec", 0)) >= 2
        or bool(COMPUTE_HINT_RE.search(query))
        or has_code_repo
    )
    needs_code_mod = bool("file_edit" in used) or (has_code_repo and bool(CODE_MOD_HINT_RE.search(query)))
    locks_format = bool(FORMAT_LOCK_HINT_RE.search(query))

    # Optional LLM semantic inference (for unseen queries or nuanced computation/format detection)
    llm_prof = None
    if llm and llm.enabled:
        llm_prof = llm.infer_semantic_profile(query, attached_files, str(task.get("task_type") or ""))
    if isinstance(llm_prof, dict):
        # Baseline-observed genuine physical tool usage takes precedence over LLM guesses
        if not used_web_genuinely:
            needs_web = bool(llm_prof.get("needs_web_info", needs_web))
        if not attached_files and not ({"file_read", "file_glob", "file_search"} & used):
            needs_local = bool(llm_prof.get("needs_local_files", needs_local))
        if int(tcounts.get("python_exec", 0)) < 2 and not has_code_repo:
            needs_compute = bool(llm_prof.get("needs_computation", needs_compute))
        if "file_edit" not in used:
            needs_code_mod = bool(llm_prof.get("needs_code_modification", needs_code_mod))
        locks_format = bool(llm_prof.get("locks_output_format", locks_format))

    # Guard 1: open-web task without attached files should NOT treat local files as primary source
    if not attached_files and needs_web and not ({"file_read", "file_glob", "file_search"} & used):
        needs_local = False
    # Guard 2: local SWE code-fix or local attached-file policy task with only GitHub peeking is NOT an open-web task
    if attached_files and not non_peeking_domains and (needs_code_mod or not WEB_HINT_RE.search(query)):
        needs_web = False

    flags = {
        "needs_web_info": needs_web,
        "needs_local_files": needs_local,
        "needs_computation": needs_compute,
        "needs_code_modification": needs_code_mod,
        "locks_output_format": locks_format,
    }

    fname, dkeys, headings = _default_deliverable_spec(query, query_lang, flags, str(task.get("task_type") or ""))
    if isinstance(llm_prof, dict):
        cand_fn = llm_prof.get("deliverable_filename")
        if isinstance(cand_fn, str) and re.match(r"^output/[a-zA-Z0-9_-]{3,40}\.json$", cand_fn.strip()):
            fname = cand_fn.strip()
        cand_keys = llm_prof.get("deliverable_keys")
        if isinstance(cand_keys, list) and len(cand_keys) == 3 and all(isinstance(k, str) and re.match(r"^[a-z][a-z0-9_]{1,28}$", k) for k in cand_keys):
            dkeys = cand_keys
        cand_h = llm_prof.get("suggested_headings")
        if isinstance(cand_h, list) and len(cand_h) == 3 and all(isinstance(h, str) and 2 <= len(h.strip()) <= 30 for h in cand_h):
            headings = [h.strip() for h in cand_h]

    # Primary domain family for slot binding
    if needs_code_mod:
        primary_domain = "code"
    elif needs_web and not needs_local:
        primary_domain = "web"
    elif needs_local and needs_compute:
        primary_domain = "local_compute"
    elif needs_local:
        primary_domain = "local"
    else:
        primary_domain = "web" if "web_search" in tool_set else "local"

    env_caps = {
        "has_plan": "task_planning" in tool_set,
        "has_env": bool({"cwd_inspect", "sandbox_prepare", "mcp_resource_list"} & tool_set),
        "has_discover_web": "web_search" in tool_set,
        "has_discover_local": bool({"file_glob", "file_search"} & tool_set),
        "has_consume_web": "web_fetch" in tool_set,
        "has_consume_local": "file_read" in tool_set,
        "has_compute": "python_exec" in tool_set,
        "has_deliver": bool({"file_write", "file_export"} & tool_set),
    }

    return {
        "query_lang": query_lang,
        "primary_domain": primary_domain,
        "tools": tools,
        "env_capabilities": env_caps,
        "input_signals": {
            "has_local_files": bool(attached_files),
            "file_count": len(attached_files),
            "has_code_repo": has_code_repo,
            "has_urls_in_query": bool(extract_urls(query)),
        },
        "semantic_flags": flags,
        "deliverable_filename": fname,
        "deliverable_keys": dkeys,
        "suggested_headings": headings,
        "fingerprint": fp,
    }


def load_unified_benchmark_tasks(repo_root: Path, split: str = "all98", baseline_json: Path | None = None) -> list[dict[str, Any]]:
    """Load unified 98-task dataset from benchmark/baseline_v4pro_98.json (single source of truth)."""
    src = baseline_json or (repo_root / "benchmark" / "baseline_v4pro_98.json")
    if not src.is_file():
        raise FileNotFoundError(f"Unified baseline file not found: {src}")
    raw_list = json.loads(src.read_text(encoding="utf-8"))
    if split == "old50":
        return [t for t in raw_list if t.get("source_split") == "V1_old50"]
    if split == "naq48":
        return [t for t in raw_list if t.get("source_split") == "V2_naq48"]
    return raw_list


def _find_old50_trace_dirs(repo_root: Path) -> dict[str, Path]:
    mapping: dict[str, Path] = {}
    for cand_root in (
        repo_root / "archive" / "legacy_datasets" / "baseline_fingerprint" / "dsh-runs",
        repo_root / "baseline_fingerprint" / "dsh-runs",
    ):
        if cand_root.is_dir():
            for p in sorted(cand_root.glob("baseline-*/G-*/trace.json")):
                mapping[p.parent.name] = p.parent
            if mapping:
                break
    return mapping


def load_old50_tasks(repo_root: Path) -> list[dict[str, Any]]:
    if (repo_root / "benchmark" / "baseline_v4pro_98.json").is_file():
        return load_unified_benchmark_tasks(repo_root, split="old50")
    src = repo_root / "archive" / "legacy_datasets" / "baseline_fingerprint" / "benchmark_baseline_all_20261111_155505.json"
    raw_list = json.loads(src.read_text(encoding="utf-8"))
    trace_dirs = _find_old50_trace_dirs(repo_root)
    tasks: list[dict[str, Any]] = []
    for item in raw_list:
        gid = str(item.get("group_id") or f"G-{item.get('task_id')}")
        tdir = trace_dirs.get(gid)
        # Upgrade tools from baseline-only subset to full real DSH toolset while keeping extra domain tools
        orig_tools = [norm_tool(str(t)) for t in (item.get("tools") or [])]
        merged_tools = sorted(set(ALL_DSH_TOOLS) | set(orig_tools))
        evidence = build_evidence_from_trace(
            trace_json_path=(tdir / "trace.json") if tdir else None,
            final_txt_path=(tdir / "final.txt") if tdir else None,
            artifacts_dir=(tdir / "artifacts") if tdir else None,
            user_query=str(item.get("user_query") or ""),
            fallback_fingerprint=item.get("baseline_fingerprint"),
        )
        tasks.append(
            {
                "source_split": "V1_old50",
                "task_id": item.get("task_id"),
                "group_id": gid,
                "task_type": item.get("task_type") or "general",
                "system_prompt": item.get("system_prompt") or DEFAULT_SYSTEM_PROMPT,
                "user_query": item.get("user_query") or "",
                "tools": merged_tools,
                "env": item.get("env") or {},
                "attached_files": item.get("attached_files") or [],
                "baseline_fingerprint": item.get("baseline_fingerprint") or {},
                "baseline_fingerprint_ref": f"old50#{gid}",
                "baseline_evidence": evidence,
                "tc_ground_truth": None,
            }
        )
    return tasks


def load_naq48_tasks(repo_root: Path, run_dir: Path | None = None) -> list[dict[str, Any]]:
    if run_dir is None and (repo_root / "benchmark" / "baseline_v4pro_98.json").is_file():
        return load_unified_benchmark_tasks(repo_root, split="naq48")
    if run_dir is None:
        run_dir = repo_root / "dsh-runs" / "naq_48_company-deepseek-20261119-132115"
    groups_path = run_dir / "baseline_groups_naq48.json"
    raw_list = json.loads(groups_path.read_text(encoding="utf-8"))

    # Load optional TC ground truth
    tc_map: dict[str, dict[str, Any]] = {}
    for tc_path in (
        repo_root / "benchmark" / "tc_ground_truth_98.jsonl",
        repo_root / "archive" / "legacy_datasets" / "naq_50" / "tc_ground_truth_50.jsonl",
    ):
        if tc_path.is_file():
            for line in tc_path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    r = json.loads(line)
                    tc_map[str(r.get("id"))] = r.get("tc_ground_truth", r)
            break

    # Map task_id -> folder under run_dir
    dir_by_id: dict[str, Path] = {}
    for p in sorted(run_dir.glob("0*/trace.json")):
        folder_name = p.parent.name
        parts = folder_name.split("-")
        if len(parts) >= 2:
            dir_by_id[parts[1]] = p.parent

    tasks: list[dict[str, Any]] = []
    for item in raw_list:
        tid = str(item.get("task_id"))
        gid = str(item.get("group_id") or f"G-naq-{tid}")
        tdir = dir_by_id.get(tid)
        merged_tools = sorted(set(ALL_DSH_TOOLS) | {norm_tool(str(t)) for t in (item.get("tools") or [])})
        evidence = build_evidence_from_trace(
            trace_json_path=(tdir / "trace.json") if tdir else None,
            final_txt_path=(tdir / "final.txt") if tdir else None,
            artifacts_dir=(tdir / "artifacts") if tdir else None,
            user_query=str(item.get("user_query") or ""),
            fallback_fingerprint=item.get("baseline_fingerprint"),
        )
        tasks.append(
            {
                "source_split": "V2_naq48",
                "task_id": item.get("task_id"),
                "group_id": gid,
                "task_type": item.get("task_type") or "daily_search",
                "system_prompt": item.get("system_prompt") or DEFAULT_SYSTEM_PROMPT,
                "user_query": item.get("user_query") or "",
                "tools": merged_tools,
                "env": item.get("env") or {},
                "attached_files": item.get("attached_files") or [],
                "baseline_fingerprint": item.get("baseline_fingerprint") or {},
                "baseline_fingerprint_ref": f"naq48_v4pro#{gid}",
                "baseline_evidence": evidence,
                "tc_ground_truth": tc_map.get(tid),
            }
        )
    return tasks


def load_arbitrary_jsonl_tasks(jsonl_path: Path) -> list[dict[str, Any]]:
    """Load arbitrary raw query JSONL (zero manual labels required, with or without baseline traces)."""
    tasks: list[dict[str, Any]] = []
    for idx, line in enumerate(jsonl_path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        r = json.loads(line)
        tid = r.get("task_id", r.get("id", idx))
        gid = str(r.get("group_id") or f"G-custom-{tid}")
        query = str(r.get("user_query") or r.get("query") or r.get("prompt") or "")
        tools = sorted({norm_tool(str(t)) for t in (r.get("tools") or ALL_DSH_TOOLS)})
        trace_dir = Path(r["trace_dir"]) if r.get("trace_dir") else None
        evidence = build_evidence_from_trace(
            trace_json_path=(trace_dir / "trace.json") if trace_dir and (trace_dir / "trace.json").is_file() else None,
            final_txt_path=(trace_dir / "final.txt") if trace_dir and (trace_dir / "final.txt").is_file() else None,
            artifacts_dir=(trace_dir / "artifacts") if trace_dir and (trace_dir / "artifacts").is_dir() else None,
            user_query=query,
            fallback_fingerprint=r.get("baseline_fingerprint"),
        )
        tasks.append(
            {
                "source_split": "custom_jsonl",
                "task_id": tid,
                "group_id": gid,
                "task_type": str(r.get("task_type") or r.get("domain") or "general"),
                "system_prompt": str(r.get("system_prompt") or DEFAULT_SYSTEM_PROMPT),
                "user_query": query,
                "tools": tools,
                "env": r.get("env") or {},
                "attached_files": r.get("attached_files") or [],
                "baseline_fingerprint": r.get("baseline_fingerprint") or {},
                "baseline_fingerprint_ref": f"custom#{gid}" if evidence["has_real_trace"] else "cold_start_no_trace",
                "baseline_evidence": evidence,
                "tc_ground_truth": r.get("tc_ground_truth"),
            }
        )
    return tasks
