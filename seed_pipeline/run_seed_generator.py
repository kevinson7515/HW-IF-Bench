#!/usr/bin/env python3
"""CLI entrypoint for the HW-IF-Bench Workflow Seed Library Constraint Generator.

Examples:
  # 1. Generate full 98 tasks (Old 50 + New 48 = 588 variants) with LLM semantic enhancement
  python3 benchmark-group-generator/seed_pipeline/run_seed_generator.py --source all98 --with-llm

  # 2. Fast offline deterministic run (zero API calls, instant verification)
  python3 benchmark-group-generator/seed_pipeline/run_seed_generator.py --source all98 --no-llm

  # 3. Smoke test 5 tasks with LLM
  python3 benchmark-group-generator/seed_pipeline/run_seed_generator.py --source all98 --limit 5 --with-llm

  # 4. Run on ANY arbitrary raw query JSONL (with or without baseline traces)
  python3 benchmark-group-generator/seed_pipeline/run_seed_generator.py --input-jsonl my_queries.jsonl --with-llm
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Any

# Ensure package import works whether called as script or module
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from seed_pipeline.llm_enhancer import LLMEnhancer
from seed_pipeline.profiler import (
    build_task_profile,
    load_arbitrary_jsonl_tasks,
    load_naq48_tasks,
    load_old50_tasks,
    load_unified_benchmark_tasks,
)
from seed_pipeline.scheduler import load_seed_library, run_seed_pipeline


def _render_markdown_report(stats: dict[str, Any], groups: list[dict[str, Any]], out_dir: Path) -> str:
    lines: list[str] = [
        "# HW-IF-Bench 工作流种子库约束生成审计报告",
        "",
        f"- **生成时间**：`{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`",
        f"- **输出目录**：`{out_dir}`",
        f"- **母题总数**：`{stats['tasks_count']}` 题 → **总变体数**：`{stats['total_variants']}` 条",
        f"- **反默认实测通过率（基线回放均违背）**：`{stats['anti_default_verified_variants']} / {stats['total_variants']}` (`{stats['anti_default_verified_rate']*100:.1f}%`)",
        f"- **基线回放拦截送分候选数**：`{stats['freebies_filtered_by_baseline_replay']}` 条（触发自动升档加权 `{stats['escalation_boosted_candidates']}` 次）",
        f"- **含执行流程约束的变体占比**：`{stats['process_workflow_variant_share']*100:.1f}%`（含广义过程+思考：`{stats['broad_process_plus_thinking_share']*100:.1f}%`）",
        f"- **LLM 增强统计**：`{json.dumps(stats['llm_stats'], ensure_ascii=False)}`（语义审计剩余告警：`{stats['llm_audit_warnings']}` 条，自动替换自愈：`{len(stats.get('audit_auto_replacements') or [])}` 条）",
        "",
        "## 一、 Tier 档位与 V1/V2 分层均衡分布",
        "",
        "| Tier | 变体数 |",
        "| :---: | :---: |",
    ]
    for tier in ("A", "B", "C", "D"):
        lines.append(f"| Tier {tier} | {stats['tier_counts'].get(tier, 0)} |")

    if stats.get("split_tier_a_primitive_counts"):
        lines += [
            "",
            "| 数据来源 (`source_split`) | `chain` | `invariant` | `cadence` | `conditional` | `thinking` | `artifact` |",
            "| :--- | :---: | :---: | :---: | :---: | :---: | :---: |",
        ]
        for sp, counts in sorted(stats["split_tier_a_primitive_counts"].items()):
            lines.append(
                f"| `{sp}` | {counts.get('chain', 0)} | {counts.get('invariant', 0)} | "
                f"{counts.get('cadence', 0)} | {counts.get('conditional', 0)} | "
                f"{counts.get('thinking', 0)} | {counts.get('artifact', 0)} |"
            )

    lines += [
        "",
        "## 二、 Tier A 控制原语分布",
        "",
        "| 原语类型 (`primitive_type`) | 数量 | 占比 (占 Tier A) |",
        "| :--- | :---: | :---: |",
    ]
    tier_a_total = max(1, stats["tier_counts"].get("A", 1))
    for k, v in sorted(stats["tier_a_primitive_counts"].items(), key=lambda kv: -kv[1]):
        lines.append(f"| `{k}` | {v} | {v / tier_a_total * 100:.1f}% |")

    lines += [
        "",
        "## 三、 Tier A 阶段链长度阶梯分布（$L=2 \\to 5$）",
        "",
        "| 阶段链长度 $L$ | 数量 | 占阶段链比例 |",
        "| :---: | :---: | :---: |",
    ]
    chain_tot = max(1, sum(stats["tier_a_chain_length_counts"].values()))
    for L in ("2", "3", "4", "5"):
        cnt = stats["tier_a_chain_length_counts"].get(L, 0)
        lines.append(f"| `L={L}` | {cnt} | {cnt / chain_tot * 100:.1f}% |")

    lines += [
        "",
        "## 四、 Tier A 流程约束绑定工具生态分布",
        "",
        "| 工具生态 (`tool_family`) | 数量 | 占比 |",
        "| :--- | :---: | :---: |",
    ]
    tf_tot = max(1, sum(stats["tier_a_process_tool_family_counts"].values()))
    for k, v in sorted(stats["tier_a_process_tool_family_counts"].items(), key=lambda kv: -kv[1]):
        lines.append(f"| `{k}` | {v} | {v / tf_tot * 100:.1f}% |")

    lines += [
        "",
        "## 五、 Tier A 具体种子频次分布（防坍缩检验）",
        "",
        f"- **最高单一种子出现次数**：`{stats['max_single_seed_count_tier_a']}`",
        "",
        "| Seed ID | 数量 |",
        "| :--- | :---: |",
    ]
    for sid, cnt in stats["tier_a_seed_counts"].items():
        lines.append(f"| `{sid}` | {cnt} |")

    lines += [
        "",
        "## 六、 抽样变体预览（前 3 道母题的 S1~S6）",
        "",
    ]
    for g in groups[:3]:
        lines.append(f"### `{g['group_id']}` (`{g['source_split']}` · `{g['task_type']}`)")
        lines.append(f"- Query: `{g['user_query'][:120].replace(chr(10), ' ')}`")
        for v in g["variants"]:
            uqa_snip = f" | Conflict: `{v['user_query_append'][:80]}`" if v.get("user_query_append") else ""
            lines.append(
                f"  - **{v['variant_id']}** (Tier {v['tier']}, seeds=`{v['seed_ids']}`, L=`{v['chain_length_L']}`, "
                f"anti_default=`{v['anti_default_verified']}`): {v['instruction'][:140].replace(chr(10), ' ')}{uqa_snip}"
            )
        lines.append("")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="HW-IF-Bench Workflow Seed Library Generator")
    parser.add_argument(
        "--source",
        choices=["all98", "old50", "naq48", "custom"],
        default="all98",
        help="Task source split (default: all98 = Old 50 + New 48)",
    )
    parser.add_argument("--input-jsonl", type=Path, default=None, help="Path to arbitrary query JSONL (implies --source custom)")
    parser.add_argument("--naq-run-dir", type=Path, default=None, help="Override NAQ v4-pro baseline run dir")
    parser.add_argument("--seed-yaml", type=Path, default=None, help="Override workflow_seeds.yaml path")
    parser.add_argument("--out-dir", type=Path, default=None, help="Output directory")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of tasks (for quick smoke test)")

    llm_group = parser.add_mutually_exclusive_group()
    llm_group.add_argument("--with-llm", dest="with_llm", action="store_true", help="Enable LLM semantic profiling, controlled paraphrasing & Tier D conflict synthesis")
    llm_group.add_argument("--no-llm", dest="with_llm", action="store_false", help="Run purely deterministic offline generation (zero API calls)")
    parser.set_defaults(with_llm=False)

    parser.add_argument("--llm-model", type=str, default=None, help="Override LLM model ID (default: deepseek-v4.1-flash-1017)")
    parser.add_argument("--llm-base-url", type=str, default=None, help="Override OpenAI-compatible base URL")
    parser.add_argument("--llm-workers", type=int, default=4, help="Concurrent LLM worker threads (default: 4)")
    parser.add_argument("--llm-timeout", type=int, default=180, help="Per-call HTTP timeout seconds (default: 180)")
    parser.add_argument("--skip-health-check", action="store_true", help="Skip startup gateway ping check")
    parser.add_argument("--skip-audit", action="store_true", help="Skip LLM post-generation Task-Preserving audit to save calls")
    parser.add_argument("--cache-path", type=Path, default=None, help="Persistent JSON cache for LLM calls")

    args = parser.parse_args()
    repo_root = REPO_ROOT
    t0 = time.time()

    # Load tasks (unified benchmark/baseline_v4pro_98.json by default)
    if args.input_jsonl is not None:
        source_name = "custom"
        tasks = load_arbitrary_jsonl_tasks(args.input_jsonl.resolve())
    elif args.naq_run_dir is not None and args.source == "naq48":
        source_name = "naq48"
        tasks = load_naq48_tasks(repo_root, run_dir=args.naq_run_dir)
    else:
        source_name = args.source
        tasks = load_unified_benchmark_tasks(repo_root, split=args.source)

    if args.limit and args.limit > 0:
        tasks = tasks[: args.limit]

    if not tasks:
        print("ERROR: No tasks loaded.", file=sys.stderr)
        return 1

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    mode_tag = "llm" if args.with_llm else "det"
    out_dir = args.out_dir or (repo_root / "dsh-runs" / f"seed_bench_{source_name}_{mode_tag}_{ts}")
    out_dir.mkdir(parents=True, exist_ok=True)
    cache_path = args.cache_path or (repo_root / "dsh-runs" / "seed_llm_cache.json")

    print(f"[seed-gen] Loaded {len(tasks)} tasks (source={source_name}, mode={'with-llm' if args.with_llm else 'no-llm'})")
    llm = LLMEnhancer(
        enabled=args.with_llm,
        base_url=args.llm_base_url,
        model=args.llm_model,
        cache_path=cache_path,
        timeout=args.llm_timeout,
    )
    if llm.enabled:
        print(f"[seed-gen] LLM enabled: model={llm.model}, base_url={llm.base_url}, workers={args.llm_workers}, timeout={llm.timeout}s, cache={cache_path}")
        if not args.skip_health_check:
            ok, msg = llm.health_check()
            print(f"[seed-gen] Gateway health check: {msg}")
            if not ok:
                print(
                    "[seed-gen][ERROR] LLM gateway is currently unreachable or timing out. "
                    "Aborting early so we do not silently fall back to templates.\n"
                    "  Check COMPANY_DEEPSEEK_BASE_URL / SEED_LLM_MODEL / gateway load, or retry later.",
                    file=sys.stderr,
                )
                return 2

    # Step 1: Build Task Capability Profiles (parallelized when LLM is enabled)
    profiles: list[dict[str, Any] | None] = [None] * len(tasks)
    if llm.enabled:
        with ThreadPoolExecutor(max_workers=max(1, args.llm_workers)) as pool:
            futs = {
                pool.submit(build_task_profile, task, task["baseline_evidence"], llm): idx
                for idx, task in enumerate(tasks)
            }
            done = 0
            for fut in as_completed(futs):
                idx = futs[fut]
                profiles[idx] = fut.result()
                done += 1
                if done % 15 == 0 or done == len(tasks):
                    print(f"[seed-gen] Profiled {done}/{len(tasks)} tasks...")
        llm.save_cache()
    else:
        for idx, task in enumerate(tasks):
            profiles[idx] = build_task_profile(task, task["baseline_evidence"], None)

    seed_lib = load_seed_library(args.seed_yaml)
    print(f"[seed-gen] Loaded {len(seed_lib['seeds'])} declarative seeds from workflow_seeds.yaml")

    # Step 2–4: Instantiate, Anti-Default Replay, Quota Schedule, LLM Paraphrase/Conflict, Assemble
    groups, stats = run_seed_pipeline(
        tasks=tasks,
        profiles=profiles,  # type: ignore[arg-type]
        seed_lib=seed_lib,
        llm=llm,
        llm_workers=args.llm_workers,
        run_audit=not args.skip_audit,
    )

    # Write outputs
    groups_file = out_dir / "benchmark_groups_seed_v1.json"
    flat_file = out_dir / "variants_flat_seed_v1.jsonl"
    stats_file = out_dir / "generation_stats.json"
    report_file = out_dir / "generation_report.md"

    groups_file.write_text(json.dumps(groups, ensure_ascii=False, indent=2), encoding="utf-8")
    with flat_file.open("w", encoding="utf-8") as fh:
        for g in groups:
            for v in g["variants"]:
                row = {
                    "task_id": g["task_id"],
                    "group_id": g["group_id"],
                    "source_split": g["source_split"],
                    "task_type": g["task_type"],
                    "user_query": g["user_query"],
                    **v,
                }
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    stats_file.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
    report_file.write_text(_render_markdown_report(stats, groups, out_dir), encoding="utf-8")

    elapsed = time.time() - t0
    print(f"\n[seed-gen] DONE in {elapsed:.1f}s!")
    print(f"  Tasks:      {stats['tasks_count']} -> Variants: {stats['total_variants']}")
    print(f"  Anti-Def:   {stats['anti_default_verified_variants']}/{stats['total_variants']} ({stats['anti_default_verified_rate']*100:.1f}%)")
    print(f"  Freebies:   {stats['freebies_filtered_by_baseline_replay']} filtered, {stats['escalation_boosted_candidates']} escalated")
    print(f"  Tier A Prims:   {stats['tier_a_primitive_counts']}")
    print(f"  Chain Lengths:  {stats['tier_a_chain_length_counts']}")
    print(f"  Tool Families:  {stats['tier_a_process_tool_family_counts']}")
    print(f"  Max SingleSeed: {stats['max_single_seed_count_tier_a']}")
    print(f"  Outputs:")
    print(f"    - {groups_file}")
    print(f"    - {flat_file}")
    print(f"    - {report_file}")
    print(f"    - {stats_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

