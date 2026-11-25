#!/usr/bin/env python3
"""Audit TC correctness, contamination/reward-hacking, and runaway traces for a naq_50 baseline run."""

from __future__ import annotations

import argparse
import json
import os
import re
import time
from collections import Counter
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

LOCAL_CHEAT_KEYS = (
    "dsqa-full",
    "tc_ground_truth",
    "user_query_naq50",
    "openweb_246",
    "data/deepsearchqa",
)
WEB_CHEAT_KEYS = (
    "deepsearchqa",
    "dsqa-full",
    "rl-research/dsqa",
    "deepmind/deepsearchqa",
)


def batch_of(tid: int) -> str:
    if tid <= 59:
        return "B1_ChinaTravel"
    if tid <= 67:
        return "B2_BrowseComp+"
    if tid <= 75:
        return "B3_DSQA_self"
    return "B4_DSQA_collab"


def audit_task(sub: Path, uq: dict[str, Any], gt: dict[str, Any]) -> dict[str, Any]:
    res = json.loads((sub / "result.json").read_text(encoding="utf-8"))
    tid = int(res["id"])
    msgs = json.loads((sub / "trace.json").read_text(encoding="utf-8")).get("trace", [])
    final_txt = (sub / "final.txt").read_text(encoding="utf-8")

    tools: list[str] = []
    reason_ch = 0
    http_403 = 0
    local_cheat = 0
    web_cheat = 0
    cheat_samples: list[str] = []

    for m in msgs:
        role = m.get("role")
        if role == "assistant":
            rc = m.get("reasoning_content")
            if isinstance(rc, str):
                reason_ch += len(rc)
            for tc in m.get("tool_calls", []):
                fn = tc.get("function", {}).get("name", "")
                args = tc.get("function", {}).get("arguments", "")
                if fn:
                    tools.append(fn)
                low = str(args).lower()
                if fn in ("read", "grep", "glob") and any(k in low for k in LOCAL_CHEAT_KEYS):
                    local_cheat += 1
                    if len(cheat_samples) < 3:
                        cheat_samples.append(f"LOCAL {fn}: {str(args)[:120]}")
                if any(k in low for k in WEB_CHEAT_KEYS):
                    web_cheat += 1
                    if len(cheat_samples) < 3:
                        cheat_samples.append(f"WEB {fn}: {str(args)[:120]}")
        elif role == "tool":
            c = str(m.get("content", ""))
            if "HTTP 403" in c or "403 Forbidden" in c:
                http_403 += 1

    dur = float(res.get("duration_seconds", 0.0))
    runaway = dur > 1800 or len(tools) > 150
    contaminated = local_cheat > 0 or web_cheat >= 2

    gold = str(gt.get("gold_answer", "")).strip()
    ev = gt.get("eval_type", "")
    heuristic_tc = "manual_itinerary"
    if tid >= 60 and gold:
        low = final_txt.lower()
        if ev == "exact_answer":
            heuristic_tc = "HIT" if gold.lower() in low else "CHECK"
        elif ev == "set_answer":
            parts = [p.strip() for p in re.split(r"[\n,]+", gold) if p.strip() and len(p.strip()) >= 3]
            hits = sum(1 for p in parts if p.lower() in low)
            heuristic_tc = f"{hits}/{len(parts)}"

    return {
        "id": tid,
        "group_id": uq["group_id"],
        "batch": batch_of(tid),
        "status": res["status"],
        "duration_s": round(dur, 1),
        "tool_calls": len(tools),
        "unique_tools": len(set(tools)),
        "reasoning_chars": reason_ch,
        "final_chars": len(final_txt),
        "http_403": http_403,
        "local_cheat_calls": local_cheat,
        "web_cheat_calls": web_cheat,
        "contaminated": contaminated,
        "runaway": runaway,
        "eval_type": ev,
        "heuristic_tc": heuristic_tc,
        "cheat_samples": cheat_samples,
    }


def load_key_from_env_or_secret(bench_root: Path) -> tuple[str, str]:
    base_url = os.environ.get("COMPANY_DEEPSEEK_BASE_URL", "http://115.120.87.159:8082/v1").rstrip("/")
    api_key = os.environ.get("COMPANY_DEEPSEEK_API_KEY", "").strip()
    if not api_key:
        secret = bench_root / ".secrets/deepseek-api-key"
        if secret.is_file():
            api_key = secret.read_text(encoding="utf-8-sig").strip()
    if not api_key:
        raise RuntimeError("Missing COMPANY_DEEPSEEK_API_KEY or .secrets/deepseek-api-key for --llm-judge")
    return base_url + "/chat/completions", api_key


def run_llm_judge(url: str, key: str, query: str, gt: dict[str, Any], answer: str) -> dict[str, str]:
    gold = gt.get("gold_answer") or gt.get("hard_logic_nl") or gt.get("hard_logic_py")
    payload = {
        "model": "deepseek-v4-pro",
        "temperature": 0,
        "max_tokens": 500,
        "response_format": {"type": "json_object"},
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a strict benchmark evaluator. Compare candidate_response against reference for original_question. "
                    "Return JSON with keys verdict (FULL, PARTIAL, or INCORRECT) and reason (brief Chinese summary). "
                    "For Set Answer, FULL requires complete match without extra wrong items; missing or extra items => PARTIAL."
                ),
            },
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "original_question": query,
                        "eval_type": gt.get("eval_type"),
                        "reference": gold,
                        "candidate_response": answer[:12000],
                    },
                    ensure_ascii=False,
                ),
            },
        ],
    }
    req = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    for attempt in range(2):
        try:
            with urlopen(req, timeout=60) as resp:
                txt = json.load(resp)["choices"][0]["message"]["content"]
            out = json.loads(txt)
            return {"verdict": str(out.get("verdict", "ERROR")), "reason": str(out.get("reason", ""))[:400]}
        except (HTTPError, URLError, TimeoutError, ValueError, KeyError) as exc:
            if attempt == 0:
                time.sleep(2)
            else:
                return {"verdict": "ERROR", "reason": str(exc)[:200]}
    return {"verdict": "ERROR", "reason": "unknown"}


def main() -> None:
    bench_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run-dir",
        type=Path,
        default=bench_root / "dsh-runs/naq_48_company-deepseek-20261119-132115",
    )
    parser.add_argument("--llm-judge", action="store_true", help="Also call DeepSeek V4 Pro to grade TC")
    args = parser.parse_args()

    uqs = {
        int(r["id"]): r
        for r in (
            json.loads(l)
            for l in (bench_root / "naq_50/user_query_naq50.jsonl").read_text(encoding="utf-8").splitlines()
            if l.strip()
        )
    }
    gts = {
        int(r["id"]): r
        for r in (
            json.loads(l)
            for l in (bench_root / "naq_50/tc_ground_truth_50.jsonl").read_text(encoding="utf-8").splitlines()
            if l.strip()
        )
    }

    judge_cfg = load_key_from_env_or_secret(bench_root) if args.llm_judge else None
    rows: list[dict[str, Any]] = []
    for sub in sorted(p for p in args.run_dir.iterdir() if p.is_dir()):
        if not (sub / "result.json").is_file():
            continue
        tid = int(json.loads((sub / "result.json").read_text(encoding="utf-8"))["id"])
        row = audit_task(sub, uqs[tid], gts[tid])
        if judge_cfg:
            final_txt = (sub / "final.txt").read_text(encoding="utf-8")
            row["llm_judge"] = run_llm_judge(*judge_cfg, uqs[tid]["user_query"], gts[tid], final_txt)
        rows.append(row)

    rows.sort(key=lambda r: r["id"])
    out_json = args.run_dir / "tc_audit_report.json"
    out_md = args.run_dir / "tc_audit_report.md"
    out_json.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# NAQ_48 Baseline Audit Report",
        "",
        f"- Total tasks: `{len(rows)}` | Succeeded: `{sum(r['status'] == 'succeeded' for r in rows)}`",
        f"- Contaminated (`local_cheat > 0` or `web_cheat >= 2`): `{[r['id'] for r in rows if r['contaminated']]}`",
        f"- Runaway (`dur > 1800s` or `tools > 150`): `{[r['id'] for r in rows if r['runaway']]}`",
        "",
        "| ID | Batch | Tools (Uniq) | Dur (s) | 403 | Local/Web Cheat | Heuristic TC | Flags |",
        "| :---: | :--- | :---: | ---: | ---: | :---: | :---: | :--- |",
    ]
    for r in rows:
        flags = []
        if r["contaminated"]:
            flags.append("CONTAMINATED")
        if r["runaway"]:
            flags.append("RUNAWAY")
        if r["unique_tools"] == 1:
            flags.append("SINGLE_TOOL")
        tc_col = r["llm_judge"]["verdict"] if "llm_judge" in r else r["heuristic_tc"]
        lines.append(
            f"| {r['id']} | {r['batch']} | {r['tool_calls']} ({r['unique_tools']}) | {r['duration_s']:.0f} | "
            f"{r['http_403']} | {r['local_cheat_calls']}/{r['web_cheat_calls']} | {tc_col} | {', '.join(flags) or '-'} |"
        )
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Audit written -> {out_md} & {out_json}")
    print("Contaminated IDs:", [r["id"] for r in rows if r["contaminated"]])
    print("Runaway IDs:", [r["id"] for r in rows if r["runaway"]])


if __name__ == "__main__":
    main()

