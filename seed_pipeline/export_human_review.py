#!/usr/bin/env python3
"""Export human-friendly review views (CSV + Stratified Sample MD + High-Risk Focus MD)
from a generated seed_bench output directory.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


def _summarize_baseline(fp: dict[str, Any]) -> str:
    tc = fp.get("total_tool_calls", 0)
    par = fp.get("max_parallel_calls", 0)
    zt = fp.get("zero_think_turns", 0)
    tlang = fp.get("thinking_lang", "?")
    tchars = fp.get("total_think_chars", 0)
    rlen = fp.get("reply_len", 0)
    top_tools = sorted((fp.get("tool_counts") or {}).items(), key=lambda kv: -kv[1])[:4]
    tstr = ", ".join(f"{k}:{v}" for k, v in top_tools)
    return f"calls={tc}({tstr}) | max_par={par} | zero_think={zt} | think={tlang}/{tchars}c | reply={rlen}c"


def _summarize_rules(rubric: list[dict[str, Any]]) -> str:
    parts = []
    for item in rubric:
        if item.get("layer") != "IF":
            continue
        r = item.get("rule") or {}
        parts.append(f"{r.get('op')}({json.dumps(r.get('value'), ensure_ascii=False)})")
    return " ; ".join(parts)


def export_review_pack(run_dir: Path) -> Path:
    groups_path = next(
        (p for p in (run_dir / "benchmark_groups_v2_588.json", run_dir / "benchmark_groups_seed_v1.json") if p.is_file()),
        None,
    )
    if groups_path is None:
        raise FileNotFoundError(f"No benchmark_groups*.json found in {run_dir}")
    groups = json.loads(groups_path.read_text(encoding="utf-8"))
    stats = json.loads((run_dir / "generation_stats.json").read_text(encoding="utf-8"))
    out_dir = run_dir / "human_review"
    out_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # 1. Full 588-row Excel-ready CSV (UTF-8 with BOM)
    # ------------------------------------------------------------------
    csv_path = out_dir / "review_all_588.csv"
    fieldnames = [
        "group_id",
        "source_split",
        "task_type",
        "primary_domain",
        "variant_id",
        "tier",
        "seed_ids",
        "chain_length_L",
        "tool_families",
        "source_variant_ids",
        "conflict_style",
        "anti_default_verified",
        "user_query_preview",
        "baseline_summary",
        "instruction",
        "user_query_append",
        "if_rule_summary",
        "human_verdict",
        "human_notes",
    ]
    with csv_path.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        for g in groups:
            bsum = _summarize_baseline(g.get("baseline_fingerprint") or {})
            uq_short = g["user_query"].replace("\n", " ")[:220]
            pdom = (g.get("task_capability_profile") or {}).get("primary_domain", "")
            for v in g["variants"]:
                w.writerow(
                    {
                        "group_id": g["group_id"],
                        "source_split": g["source_split"],
                        "task_type": g["task_type"],
                        "primary_domain": pdom,
                        "variant_id": v["variant_id"],
                        "tier": v["tier"],
                        "seed_ids": "+".join(v["seed_ids"]),
                        "chain_length_L": v["chain_length_L"] or "",
                        "tool_families": "+".join(v["tool_families"]),
                        "source_variant_ids": "+".join(v["source_variant_ids"]),
                        "conflict_style": v.get("conflict_style") or "",
                        "anti_default_verified": v["anti_default_verified"],
                        "user_query_preview": uq_short,
                        "baseline_summary": bsum,
                        "instruction": v["instruction"],
                        "user_query_append": v.get("user_query_append") or "",
                        "if_rule_summary": _summarize_rules(v["rubric"]),
                        "human_verdict": "",
                        "human_notes": "",
                    }
                )

    # ------------------------------------------------------------------
    # 2. Stratified 15-Task Sample Markdown (90 variants across all domains)
    # ------------------------------------------------------------------
    picked: list[dict[str, Any]] = []
    picked_ids: set[str] = set()

    def _pick_where(pred, limit=1):
        cnt = 0
        for g in groups:
            if g["group_id"] in picked_ids:
                continue
            if pred(g):
                picked.append(g)
                picked_ids.add(g["group_id"])
                cnt += 1
                if cnt >= limit:
                    break

    # Pick diverse V1 Old 50 (7 tasks) + V2 New 48 (8 tasks, including healed task)
    _pick_where(lambda g: "astropy" in g["group_id"], 1)
    _pick_where(lambda g: "django" in g["group_id"], 1)
    _pick_where(lambda g: "legal" in g["group_id"], 2)
    _pick_where(lambda g: "finance" in g["group_id"], 2)
    _pick_where(lambda g: "customer" in g["group_id"], 1)
    _pick_where(lambda g: g["group_id"] == "G-culture-deepsearchqa-003", 1)  # auto-healed task
    _pick_where(lambda g: g["source_split"] == "V2_naq48" and "chinatravel" in g["group_id"].lower(), 2)
    _pick_where(lambda g: g["source_split"] == "V2_naq48" and "browsecomp" in g["group_id"].lower(), 2)
    _pick_where(lambda g: g["source_split"] == "V2_naq48" and "deepsearchqa" in g["group_id"].lower(), 3)

    sample_md = out_dir / "review_stratified_sample_15tasks.md"
    lines = [
        "# 人工分层抽检手册（15 道典型母题 × 6 变体 = 90 条）",
        "",
        "> 审查建议：逐题对照「原题 Query」「基线实际行为」与「S1–S6 约束」，重点核查：**① 是否合理不毁题（Task-Preserving）② 是否真的反默认 ③ 规则与文案是否一致 ④ Tier D 冲突是否逼真且不篡改原题核心目标**。",
        "",
    ]
    for idx, g in enumerate(picked, 1):
        fp = g.get("baseline_fingerprint") or {}
        prof = g.get("task_capability_profile") or {}
        lines += [
            f"---",
            f"## {idx}. `{g['group_id']}`（`{g['source_split']}` · `{g['task_type']}` · `domain={prof.get('primary_domain')}`）",
            "",
            f"- **原题 Query**：{g['user_query'][:500].replace(chr(10), ' ')}",
            f"- **附件数**：`{len(g.get('attached_files') or [])}` | **语义开关**：`{prof.get('semantic_flags')}`",
            f"- **基线实测行为**：`{_summarize_baseline(fp)}`",
            "",
        ]
        for v in g["variants"]:
            lines.append(
                f"### `- [ ]` **{v['variant_id']}**（Tier {v['tier']} · seeds=`{v['seed_ids']}` · L=`{v['chain_length_L']}` · family=`{v['tool_families']}` · src=`{v['source_variant_ids']}`）"
            )
            lines.append(f"- **注入约束**：{v['instruction']}")
            if v.get("user_query_append"):
                lines.append(f"- **Tier D 对抗追问**（`{v['conflict_style']}`）：{v['user_query_append']}")
            if v.get("long_context"):
                lines.append(f"- **Tier C 压力**：`position={v['position']}`, `context_records={v['context_records']}`")
            lines.append(f"- **确定性判分规则**：`{_summarize_rules(v['rubric'])}`")
            lines.append("")

    sample_md.write_text("\n".join(lines), encoding="utf-8")

    # ------------------------------------------------------------------
    # 3. High-Risk Focus Review Markdown (targeted checks where errors hide)
    # ------------------------------------------------------------------
    focus_md = out_dir / "review_high_risk_focus.md"
    flines = [
        "# 人工高危切片定向审查清单",
        "",
        "与其逐行盲翻 588 条，不如优先把最容易出现“过严伤 TC / 语义冲突 / 不可解”的 **4 类高危切片** 全部集中审完：",
        "",
    ]

    # Slice 1: All L=5 long chains (10 items)
    flines += ["## 切片 1：全部 `L=5` 超长阶段链（重点看 5 个阶段是否都合理必要）", ""]
    for g in groups:
        for v in g["variants"]:
            if v["tier"] == "A" and v.get("chain_length_L") == 5:
                flines.append(f"- [ ] **`{g['group_id']}` {v['variant_id']}** (`{v['seed_ids'][0]}` · `{g['task_type']}`)")
                flines.append(f"  - Query: {g['user_query'][:160].replace(chr(10), ' ')}")
                flines.append(f"  - 约束: {v['instruction']}")
                flines.append(f"  - 规则: `{_summarize_rules(v['rubric'])}`")
    flines.append("")

    # Slice 2: All tight budgets & answer lengths (risk of hurting TC)
    flines += ["## 切片 2：全部预算收紧 & 回答字数上限（重点看阈值是否卡得太死伤 TC）", ""]
    for g in groups:
        fp = g.get("baseline_fingerprint") or {}
        for v in g["variants"]:
            if v["tier"] == "A" and v["seed_ids"][0] in {"CAD_TOOL_BUDGET_TIGHT", "ART_ANSWER_LENGTH"}:
                flines.append(f"- [ ] **`{g['group_id']}` {v['variant_id']}** (`{v['seed_ids'][0]}`)")
                flines.append(f"  - Query: {g['user_query'][:140].replace(chr(10), ' ')}")
                flines.append(f"  - 基线: `{_summarize_baseline(fp)}`")
                flines.append(f"  - 约束: {v['instruction']}")
                flines.append(f"  - 规则: `{_summarize_rules(v['rubric'])}`")
    flines.append("")

    # Slice 3: All source blacklists & strict URL provenance & error branch
    flines += ["## 切片 3：全部域名黑名单 / 严格 URL 溯源 / 异常分支协议（重点看是否可解）", ""]
    for g in groups:
        for v in g["variants"]:
            if v["tier"] == "A" and v["seed_ids"][0] in {"INH_SOURCE_BLACKLIST", "INV_SOURCE_BEFORE_FETCH", "COND_ERROR_BRANCH_PROTOCOL"}:
                flines.append(f"- [ ] **`{g['group_id']}` {v['variant_id']}** (`{v['seed_ids'][0]}`)")
                flines.append(f"  - Query: {g['user_query'][:140].replace(chr(10), ' ')}")
                flines.append(f"  - 约束: {v['instruction']}")
                flines.append(f"  - 规则: `{_summarize_rules(v['rubric'])}`")
    flines.append("")

    # Slice 4: Auto-healed + 12 diverse Tier D conflicts
    flines += ["## 切片 4：审计自愈记录 & 抽样 12 条 Tier D 对抗冲突（重点看是否逼真且不篡改原题事实）", ""]
    for rep in stats.get("audit_auto_replacements") or []:
        flines.append(f"- **自动自愈**：`{rep['group_id']}` {rep['variant_id']}：`{rep['replaced_seed']}` → `{rep['new_seed']}`（原因：{rep['reason']}）")
    flines.append("")
    step = max(1, len(groups) // 12)
    for g in groups[::step][:12]:
        v6 = g["variants"][5]
        flines.append(f"- [ ] **`{g['group_id']}` S6** (`{v6['conflict_style']}` · 针对 `{v6['seed_ids'][0]}`)")
        flines.append(f"  - 原约束: {v6['instruction'][:150]}")
        flines.append(f"  - 对抗追问: {v6['user_query_append']}")
    flines.append("")

    focus_md.write_text("\n".join(flines), encoding="utf-8")
    return out_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Export human review pack from a seed_bench run dir")
    parser.add_argument("run_dir", type=Path, help="Path to seed_bench_* directory")
    args = parser.parse_args()
    out_dir = export_review_pack(args.run_dir.resolve())
    for p in sorted(out_dir.iterdir()):
        print(f"Created: {p} ({p.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

