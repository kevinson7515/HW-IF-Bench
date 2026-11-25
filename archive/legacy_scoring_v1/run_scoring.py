"""Score one or more benchmark runs against their rubric without editing code."""

from __future__ import annotations

import argparse
import csv
import getpass
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCORE_SCRIPT = ROOT / "score_benchmark.py"
JUDGE_SCRIPT = ROOT / "deepseek_judge.py"


def resolve_config_path(value: str, base: Path) -> Path:
    path = Path(value)
    return (path if path.is_absolute() else base / path).resolve()


def data_root(path: Path) -> Path:
    """Accept a dataset folder or a parent containing exactly one dataset."""
    if not path.is_dir():
        raise ValueError(f"数据目录不存在：{path}")
    if list(path.glob("benchmark_groups*.json")):
        return path
    children = [child for child in path.iterdir()
                if child.is_dir() and list(child.glob("benchmark_groups*.json"))]
    if len(children) == 1:
        return children[0]
    return path


def find_groups(data: Path, configured: str | None, explicit: Path | None) -> Path:
    if explicit:
        if not explicit.is_file():
            raise ValueError(f"rubric 文件不存在：{explicit}")
        return explicit.resolve()
    if configured and (data / configured).is_file():
        return (data / configured).resolve()
    candidates = sorted(data.glob("benchmark_groups*.json"))
    if len(candidates) != 1:
        raise ValueError(f"在 {data} 找到 {len(candidates)} 个 rubric 文件；请用 --groups 指定其中一个")
    return candidates[0].resolve()


def discover_runs(data: Path) -> list[Path]:
    candidates = []
    for parent in (data / "dsh-runs", data):
        if parent.is_dir():
            candidates.extend(p for p in parent.iterdir()
                              if p.is_dir() and p.name.startswith("benchmark-")
                              and (p / "results.jsonl").is_file())
    return sorted(set(candidates))


def normalize_run(path: Path) -> Path:
    path = path.resolve()
    if path.is_file() and path.name == "results.jsonl":
        path = path.parent
    if not (path / "results.jsonl").is_file():
        raise ValueError(f"找不到运行结果：{path / 'results.jsonl'}")
    return path


def find_baseline(run: Path, data: Path, config: dict, explicit: Path | None) -> Path | None:
    if explicit:
        if not explicit.is_file():
            raise ValueError(f"基线文件不存在：{explicit}")
        return explicit.resolve()
    for fragment, name in config.get("baseline_files", {}).items():
        if fragment.lower() in run.name.lower() and (data / name).is_file():
            return (data / name).resolve()
    candidates = sorted(data.glob("baseline_fingerprint*.jsonl"))
    return candidates[0].resolve() if len(candidates) == 1 else None


def validate_run(run: Path, groups: Path) -> int:
    rubric = json.loads(groups.read_text(encoding="utf-8"))
    if isinstance(rubric, dict):
        rubric = rubric.get("groups", [rubric])
    allowed = {(group["group_id"], variant["variant_id"])
               for group in rubric for variant in group["variants"]}
    rows = [json.loads(line) for line in (run / "results.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()]
    if not rows:
        raise ValueError(f"运行结果为空：{run}")
    missing = sorted({(row["group_id"], row["variant_id"]) for row in rows} - allowed)
    if missing:
        sample = ", ".join(f"{group}/{variant}" for group, variant in missing[:5])
        raise ValueError(f"{run.name} 有 {len(missing)} 个题目不在 rubric 中：{sample}；请检查 --groups")
    return len(rows)


def output_stem(run: Path, groups: Path, baseline: Path | None) -> str:
    digest = hashlib.sha256()
    digest.update(str(run).encode("utf-8"))
    for path in (run / "results.jsonl", groups, baseline):
        if path:
            digest.update(path.read_bytes())
    return f"{run.name}_{digest.hexdigest()[:10]}"


def run_command(args: list[str], env: dict[str, str] | None = None) -> None:
    subprocess.run([sys.executable, *args], check=True, cwd=ROOT, env=env)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "config.json")
    parser.add_argument("--data", type=Path, help="数据集目录；省略时使用配置中的 data_dir")
    parser.add_argument("--run", type=Path, action="append", help="指定运行目录或 results.jsonl；可重复使用")
    parser.add_argument("--groups", type=Path, help="本次使用的 benchmark_groups*.json")
    parser.add_argument("--baseline-file", type=Path, help="本次使用的外部基线指纹文件")
    parser.add_argument("--results-dir", type=Path, help="结果输出目录")
    parser.add_argument("--no-judge", action="store_true", help="只做本地初评")
    parser.add_argument("--list", action="store_true", help="只列出将评测的运行")
    args = parser.parse_args()

    if not args.config.is_file():
        parser.error(f"配置文件不存在：{args.config}")
    config = json.loads(args.config.read_text(encoding="utf-8"))
    base = args.config.resolve().parent
    configured_data = args.data or resolve_config_path(config.get("data_dir", "data"), base)
    try:
        if args.groups and not args.data:
            configured_data = args.groups.resolve().parent
        elif args.run and not args.data:
            first_run = normalize_run(args.run[0])
            for ancestor in (first_run, *first_run.parents):
                if list(ancestor.glob("benchmark_groups*.json")):
                    configured_data = ancestor
                    break
        data = data_root(configured_data.resolve())
        groups = find_groups(data, config.get("groups_file") if not args.data else None, args.groups)
        runs = [normalize_run(path) for path in args.run] if args.run else discover_runs(data)
        runs = sorted(set(runs))
        if not runs:
            raise ValueError(f"在 {data} 没有找到 benchmark-* 运行；可用 --run 指定目录")
        for run in runs:
            validate_run(run, groups)
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as exc:
        parser.error(str(exc))

    if args.list:
        print(f"rubric: {groups}")
        for run in runs:
            print(run)
        return

    out_dir = (args.results_dir or resolve_config_path(config.get("results_dir", "results"), base)).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    source_parser = data / config.get("source_parser", "attached_files/task_3/parser.py")
    judge = config.get("deepseek_judge", {})
    judge_enabled = bool(judge.get("enabled", True)) and not args.no_judge
    key = None
    if judge_enabled:
        key = judge.get("api_key") or os.getenv(judge.get("api_key_env", "DEEPSEEK_API_KEY"))
        if not key:
            key = getpass.getpass("DeepSeek API Key（输入时不显示）：")
        if not key:
            parser.error("缺少 DeepSeek API Key；可先用 --no-judge")
        base_url = judge.get("base_url", "https://api.deepseek.com")
        if judge.get("confirm_before_send", True):
            print(f"将向 {base_url} 发送待评证据并产生 API 费用。", flush=True)
            if input("确认继续？输入 yes：").strip().lower() != "yes":
                print("已取消；未调用 DeepSeek。")
                return

    summary = []
    for run in runs:
        try:
            baseline = find_baseline(run, data, config, args.baseline_file)
            stem = output_stem(run, groups, baseline)
            scores = out_dir / f"{stem}_scores.json"
            judgments = out_dir / f"{stem}_judgments.jsonl"
            score_args = [str(SCORE_SCRIPT), "--groups", str(groups), "--run", str(run), "--out", str(scores)]
            if source_parser.is_file():
                score_args += ["--source-parser", str(source_parser)]
            if baseline:
                score_args += ["--baseline-file", str(baseline)]
            print(f"评测 {run.name}", flush=True)
            current_score_args = score_args + (["--judgments", str(judgments)] if judgments.is_file() else [])
            run_command(current_score_args)
            queue = scores.with_name(scores.stem + "_review_queue.jsonl")
            if judge_enabled and queue.is_file() and queue.stat().st_size:
                judge_args = [str(JUDGE_SCRIPT), "--queue", str(queue), "--out", str(judgments),
                              "--base-url", base_url, "--model", judge.get("model", "deepseek-v4-pro"),
                              "--vision-model", judge.get("vision_model", "deepseek-flash"),
                              "--max-tokens", str(judge.get("max_tokens", 4096)),
                              "--max-attempts", str(judge.get("max_attempts", 3)), "--send"]
                if judge.get("max_new_judgments_per_run", 0):
                    judge_args += ["--limit", str(judge["max_new_judgments_per_run"])]
                env = os.environ.copy()
                env["DEEPSEEK_API_KEY"] = key
                run_command(judge_args, env=env)
                if judgments.is_file():
                    run_command(score_args + ["--judgments", str(judgments)])
            result = json.loads(scores.read_text(encoding="utf-8"))
            counts = {}
            for item in result["results"]:
                status = item["scoring_status"]
                counts[status] = counts.get(status, 0) + 1
            summary.append({"run": run.name, "cases": len(result["results"]),
                            "scored": counts.get("scored", 0),
                            "eligible_for_comparison": sum(bool(x["eligible_for_comparison"])
                                                           for x in result["results"]),
                            "status_counts": counts, "score_file": str(scores),
                            "review_queue": str(queue),
                            "judgments_file": str(judgments) if judgments.is_file() else ""})
        except (ValueError, OSError, subprocess.CalledProcessError) as exc:
            parser.exit(1, f"评测 {run.name} 失败：{exc}\n")

    summary_path = out_dir / "summary.csv"
    with summary_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary[0].keys())
        writer.writeheader()
        writer.writerows(summary)
    print(f"完成。汇总：{summary_path}")
    for row in summary:
        print(f"{row['run']}: {row['scored']}/{row['cases']} 已评分，"
              f"{row['eligible_for_comparison']} 条可正式比较；明细：{row['score_file']}")


if __name__ == "__main__":
    main()
