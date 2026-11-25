#!/usr/bin/env python3
"""Extract v5.10-compatible baseline_fingerprint groups from a DSH queries batch run."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

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
}

NODE_EXTRACT_SCRIPT = r"""
const fs = require("node:fs");
const zlib = require("node:zlib");
const raw = fs.readFileSync(process.argv[1]);
const magic = Buffer.from([0x28, 0xb5, 0x2f, 0xfd]);
const frames = [];
for (let idx = raw.indexOf(magic, 0); idx !== -1; idx = raw.indexOf(magic, idx + 4)) {
  const next = raw.indexOf(magic, idx + 4);
  try {
    frames.push(zlib.zstdDecompressSync(next === -1 ? raw.subarray(idx) : raw.subarray(idx, next)).toString("utf8"));
  } catch {}
}
const events = frames.join("").trim().split("\n").filter(Boolean).map(l => JSON.parse(l));
const sysEvt = events.find(e => e.type === "system/message");
let systemPrompt = "";
if (sysEvt && sysEvt.data && sysEvt.data.message && Array.isArray(sysEvt.data.message.content)) {
  systemPrompt = sysEvt.data.message.content.map(c => c.text || "").join("\n").trim();
}
const reqEvt = events.find(e => e.type === "request/header");
let tools = [];
let provider = null;
let model = null;
if (reqEvt && reqEvt.data && reqEvt.data.header) {
  const h = reqEvt.data.header;
  if (Array.isArray(h.tools)) tools = h.tools.map(t => t.name).filter(Boolean);
  if (h.config) { provider = h.config.provider || null; model = h.config.model || null; }
}
process.stdout.write(JSON.stringify({ systemPrompt, tools, provider, model }));
"""


def find_node(explicit: str | None) -> str:
    if explicit and Path(explicit).is_file():
        return explicit
    for cand in (
        Path.home() / ".conda/envs/dsh/bin/node",
        Path.home() / "anaconda3/envs/dsh/bin/node",
    ):
        if cand.is_file():
            return str(cand)
    found = shutil.which("node")
    if found:
        return found
    raise RuntimeError("Node.js >= 22 is required to decompress session.v4.jsonl.zstd")


def norm_tool(name: str) -> str:
    return TOOL_NORM.get(name, name)


def extract_session_meta(zstd_path: Path, node_bin: str) -> dict[str, Any]:
    out = subprocess.check_output([node_bin, "-e", NODE_EXTRACT_SCRIPT, str(zstd_path)], text=True)
    return json.loads(out)


def extract_domains(text: str) -> list[str]:
    domains: list[str] = []
    seen: set[str] = set()
    for url in re.findall(r"https?://[^\s<>\"'\)\]]+", text):
        try:
            host = (urlsplit(url.rstrip(".,;:")).hostname or "").lower().rstrip(".")
        except ValueError:
            continue
        if host.startswith("www."):
            host = host[4:]
        if host and host not in seen:
            seen.add(host)
            domains.append(host)
    return domains


def detect_reply_format(text: str) -> list[str]:
    tags: list[str] = []
    if re.search(r"(?m)^#{1,3}\s+", text):
        tags.append("markdown_headings")
    if re.search(r"(?m)^\|.+\|\s*$\n^\|[-: |]+\|\s*$", text):
        tags.append("markdown_table")
    if re.search(r"(?m)^\s*([-*]|\d+\.)\s+", text):
        tags.append("markdown_lists")
    if "```" in text:
        tags.append("code_fences")
    if "http://" in text or "https://" in text:
        tags.append("urls")
    return tags or ["plain_text"]


def build_group(
    task_dir: Path,
    uq: dict[str, Any],
    gt: dict[str, Any] | None,
    node_bin: str,
    cached_session_meta: dict[str, Any] | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    result = json.loads((task_dir / "result.json").read_text(encoding="utf-8"))
    trace_doc = json.loads((task_dir / "trace.json").read_text(encoding="utf-8"))
    final_text = (task_dir / "final.txt").read_text(encoding="utf-8")
    artifacts_doc = json.loads((task_dir / "artifacts.json").read_text(encoding="utf-8"))

    zstd_path = task_dir / "session-records/session.v4.jsonl.zstd"
    session_meta = extract_session_meta(zstd_path, node_bin) if zstd_path.is_file() else (cached_session_meta or {})
    system_prompt = session_meta.get("systemPrompt") or (cached_session_meta or {}).get("systemPrompt", "")
    raw_declared_tools = session_meta.get("tools") or (cached_session_meta or {}).get("tools", [])

    msgs = trace_doc.get("trace", [])
    tool_seq: list[str] = []
    search_queries: list[str] = []
    fetched_sites: list[str] = []
    fetched_seen: set[str] = set()
    search_calls = 0
    fetch_calls = 0
    tool_errors = 0
    parallel_calls = 0
    rounds = 0
    reasoning_len = 0
    asked_question = False

    for m in msgs:
        role = m.get("role")
        if role == "assistant":
            rounds += 1
            rc = m.get("reasoning_content")
            if isinstance(rc, str):
                reasoning_len += len(rc)
            tcs = m.get("tool_calls", [])
            if len(tcs) > 1:
                parallel_calls += 1
            for tc in tcs:
                fn = tc.get("function", {}).get("name", "")
                if not fn:
                    continue
                n_fn = norm_tool(fn)
                tool_seq.append(n_fn)
                if fn == "ask_user_question":
                    asked_question = True
                raw_args = tc.get("function", {}).get("arguments", "")
                try:
                    parsed_args = json.loads(raw_args) if isinstance(raw_args, str) else raw_args
                except json.JSONDecodeError:
                    parsed_args = {}
                if n_fn == "web_search":
                    search_calls += 1
                    if isinstance(parsed_args, dict):
                        qs = parsed_args.get("queries")
                        if isinstance(qs, list):
                            search_queries.extend(str(q) for q in qs if str(q).strip())
                        elif isinstance(parsed_args.get("query"), str):
                            search_queries.append(parsed_args["query"])
                elif n_fn == "web_fetch":
                    fetch_calls += 1
                    if isinstance(parsed_args, dict) and isinstance(parsed_args.get("url"), str):
                        for d in extract_domains(parsed_args["url"]):
                            if d not in fetched_seen:
                                fetched_seen.add(d)
                                fetched_sites.append(d)
        elif role == "tool":
            content = str(m.get("content", ""))
            if (
                "HTTP 403" in content
                or "E2B execution failed" in content
                or content.startswith("Error:")
                or '"isError": true' in content
            ):
                tool_errors += 1

    # Count step_end events in trace.jsonl for accurate agent_steps
    agent_steps = rounds
    trace_jsonl = task_dir / "trace.jsonl"
    if trace_jsonl.is_file():
        step_ends = 0
        for line in trace_jsonl.read_text(encoding="utf-8", errors="replace").splitlines():
            if '"phase":"step_end"' in line or '"phase": "step_end"' in line:
                step_ends += 1
        if step_ends > 0:
            agent_steps = step_ends

    # Combine declared environment tools + any invoked tools (normalized, deduped, order-preserved)
    declared_norm: list[str] = []
    seen_tools: set[str] = set()
    for t in list(raw_declared_tools) + tool_seq:
        nt = norm_tool(t)
        if nt and nt not in seen_tools:
            seen_tools.add(nt)
            declared_norm.append(nt)

    # Extract actual output artifacts recorded by run.sh
    output_artifacts: list[str] = []
    for key in ("created", "modified"):
        entries = artifacts_doc.get(key, [])
        if isinstance(entries, list):
            for entry in entries:
                if isinstance(entry, dict) and isinstance(entry.get("path"), str):
                    output_artifacts.append(entry["path"])
                elif isinstance(entry, str):
                    output_artifacts.append(entry)

    cited_domains = extract_domains(final_text)
    tool_counts = dict(Counter(tool_seq))
    sp_sha256 = hashlib.sha256(system_prompt.encode("utf-8")).hexdigest() if system_prompt else ""

    fingerprint: dict[str, Any] = {
        "tool_seq": tool_seq,
        "tool_call_count": len(tool_seq),
        "unique_tools": sorted(set(tool_seq)),
        "tool_counts": tool_counts,
        "tool_error_count": tool_errors,
        "agent_steps": agent_steps,
        "rounds": rounds,
        "parallel_calls": parallel_calls,
        "asked_question": asked_question,
        "reply_len": len(final_text),
        "reply_format": detect_reply_format(final_text),
        "reasoning_len": reasoning_len,
        "search_call_count": search_calls,
        "search_queries": search_queries[:50],
        "search_query_count": len(search_queries),
        "fetch_call_count": fetch_calls,
        "fetched_sites": fetched_sites,
        "cited_source_domains": cited_domains,
        "output_artifacts": output_artifacts,
        "duration_seconds": result.get("duration_seconds"),
    }

    task_type_label = uq.get("task_type_zh") or uq.get("task_type") or "日常搜索与综合规划"
    if uq.get("sub_category"):
        task_type_label = f"{task_type_label}/{uq['sub_category']}"

    group: dict[str, Any] = {
        "task_id": int(uq["id"]),
        "group_id": uq["group_id"],
        "task_type": task_type_label,
        "user_query": uq["user_query"],
        "system_prompt": system_prompt,
        "system_prompt_sha256": sp_sha256,
        "execution_status": result.get("status", "unknown"),
        "model": session_meta.get("model") or "deepseek-v4-pro",
        "tools": declared_norm,
        "attached_files": uq.get("attached_files", []),
        "env": {
            "harness": "deepseek-harness",
            "profile": "headless",
            "baseline_model": session_meta.get("model") or "deepseek-v4-pro",
            "provider": session_meta.get("provider") or "company-deepseek",
            "search_provider": "serper (yibuapi.com)",
            "code_sandbox": "E2B cloud sandbox",
            "attached_files_root": "naq_50",
            "source_benchmark": uq.get("source_benchmark"),
            "source_uid": uq.get("source_uid"),
            "language": uq.get("language"),
            "batch_run_dir": str(task_dir.parent.name),
        },
        "baseline_fingerprint": fingerprint,
    }
    if gt:
        group["source_eval_type"] = gt.get("eval_type")
    return group, session_meta


def main() -> None:
    bench_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run-dir",
        type=Path,
        default=bench_root / "dsh-runs/naq_48_company-deepseek-20261119-132115",
    )
    parser.add_argument(
        "--queries",
        type=Path,
        default=bench_root / "naq_50/user_query_naq50.jsonl",
    )
    parser.add_argument(
        "--ground-truth",
        type=Path,
        default=bench_root / "naq_50/tc_ground_truth_50.jsonl",
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--exclude-ids",
        default="",
        help="Comma-separated task IDs to exclude (e.g., 82,85,87,88,92)",
    )
    parser.add_argument("--node", default=None, help="Path to Node.js >= 22 binary")
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate output directly through benchmark-group-generator/generator.py",
    )
    args = parser.parse_args()

    node_bin = find_node(args.node)
    exclude = {int(x.strip()) for x in args.exclude_ids.split(",") if x.strip()}

    uqs = {
        int(r["id"]): r
        for r in (json.loads(l) for l in args.queries.read_text(encoding="utf-8").splitlines() if l.strip())
    }
    gts = {
        int(r["id"]): r
        for r in (json.loads(l) for l in args.ground_truth.read_text(encoding="utf-8").splitlines() if l.strip())
    }

    groups: list[dict[str, Any]] = []
    cached_meta: dict[str, Any] | None = None
    for sub in sorted(p for p in args.run_dir.iterdir() if p.is_dir()):
        rp = sub / "result.json"
        if not rp.is_file():
            continue
        res = json.loads(rp.read_text(encoding="utf-8"))
        tid = int(res["id"])
        if tid in exclude or tid not in uqs:
            continue
        group, meta = build_group(sub, uqs[tid], gts.get(tid), node_bin, cached_meta)
        if meta.get("systemPrompt"):
            cached_meta = meta
        groups.append(group)

    groups.sort(key=lambda g: g["task_id"])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(groups, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(groups)} groups -> {args.output}")

    if args.validate:
        gen_dir = bench_root / "benchmark-group-generator"
        sys.path.insert(0, str(gen_dir))
        import generator

        loaded = generator.load_tasks(str(args.output))
        print(f"generator.load_tasks() PASSED: {len(loaded)} tasks normalized cleanly.")
        warnings = [w for row in loaded for w in row.get("import_metadata", {}).get("warnings", [])]
        print(f"Import warnings: {len(warnings)}")


if __name__ == "__main__":
    main()

