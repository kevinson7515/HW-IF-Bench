"""Schedule independent DSH sessions for the three open-web conditions."""

import argparse
import json
import os
import random
import shutil
import signal
import subprocess
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from common import ROOT, load_tasks, read_events, write_json
from policies import POLICIES


def run_case(task, condition, output, dsh, profile, timeout):
    folder = output / condition / task["id"]
    workspace = folder / "workspace"
    workspace.mkdir(parents=True)
    env = os.environ.copy()
    env.pop("OPENWEB_JUDGE_API_KEY", None)
    env["DSH_TELEMETRY_DISABLED"] = "1"
    env["DSH_NESTED_CONSTRAINT"] = POLICIES[condition]
    env.setdefault("SERPER_AUTH_MODE", "bearer")
    patches = ["model.yml", "web.yml"]
    if condition != "S0":
        patches.append("constraint.yml")
    command = ["timeout", str(max(1, timeout - 5)), dsh, "--profile", profile]
    for patch in patches:
        command.extend(["--patch", str(ROOT / "patches" / patch)])
    command.extend(
        [
            "--json",
            "--permission-mode",
            "workspace-write",
            "--approval-policy",
            "never",
            "-",
        ]
    )
    events_path = folder / "events.jsonl"
    timed_out = False
    with (
        events_path.open("wb") as stdout,
        (folder / "diagnostics.log").open("wb") as stderr,
    ):
        process = subprocess.Popen(
            command,
            cwd=workspace,
            env=env,
            stdin=subprocess.PIPE,
            stdout=stdout,
            stderr=stderr,
            start_new_session=True,
        )
        try:
            process.communicate(
                (task["user_query"] + "\n").encode("utf-8"), timeout=timeout
            )
        except subprocess.TimeoutExpired:
            timed_out = True
            stop_process(process)

    events = read_events(events_path)
    final = next(
        (
            event.get("text")
            for event in reversed(events)
            if event.get("type") == "final"
        ),
        "",
    )
    final = final if isinstance(final, str) else ""
    (folder / "final.txt").write_text(final, encoding="utf-8")
    if timed_out or process.returncode in (124, 137):
        status = "timed_out"
    elif not final.strip():
        status = "empty_final"
    else:
        status = "succeeded"
    return {
        "status": status,
        "return_code": process.returncode,
        "final_chars": len(final),
        "tool_calls": sum(event.get("type") == "tool_call" for event in events),
    }


def stop_process(process):
    try:
        os.killpg(process.pid, signal.SIGTERM)
        process.wait(timeout=15)
    except ProcessLookupError:
        process.wait()
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--dsh", default=os.environ.get("DSH_BIN", "dsh"))
    parser.add_argument("--profile", default="headless")
    parser.add_argument("--workers", type=int, default=15)
    parser.add_argument("--timeout", type=int, default=390)
    parser.add_argument("--seed", type=int, default=246118)
    parser.add_argument(
        "--plan",
        action="store_true",
        help="write the schedule without starting sessions",
    )
    args = parser.parse_args()
    if args.workers < 1 or args.timeout < 1:
        parser.error("workers and timeout must be positive")

    dsh = shutil.which(args.dsh)
    if not args.plan:
        if not dsh or not shutil.which("timeout"):
            parser.error("DSH and GNU timeout must be installed")
        dsh = str(Path(dsh).absolute())
        required = (
            "COMPANY_DEEPSEEK_API_KEY",
            "COMPANY_DEEPSEEK_BASE_URL",
            "SERPER_API_KEY",
            "SERPER_BASE_URL",
        )
        missing = [variable for variable in required if not os.environ.get(variable)]
        if missing:
            parser.error("missing environment variables: " + ", ".join(missing))

    tasks = load_tasks()
    randomizer = random.Random(args.seed)
    randomizer.shuffle(tasks)
    jobs = []
    for task in tasks:
        block = list(POLICIES)
        randomizer.shuffle(block)
        jobs.extend((task, condition) for condition in block)

    output = args.output.resolve()
    output.mkdir(parents=True, mode=0o700)
    write_json(
        output / "schedule.json",
        {
            "seed": args.seed,
            "workers": args.workers,
            "timeout_seconds": args.timeout,
            "model": "deepseek-v4-pro",
            "evidence_mode": "web_only",
            "profile": args.profile,
            "jobs": [[task["id"], condition] for task, condition in jobs],
        },
    )
    write_json(output / "policies.json", POLICIES)
    if args.plan:
        print(f"Planned {len(jobs)} sessions")
        return

    counts = {condition: Counter() for condition in POLICIES}
    with (output / "attempt_index.jsonl").open("w", encoding="utf-8") as stream:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {
                pool.submit(
                    run_case, task, condition, output, dsh, args.profile, args.timeout
                ): (task, condition)
                for task, condition in jobs
            }
            for future in as_completed(futures):
                task, condition = futures[future]
                try:
                    result = future.result()
                except OSError as exc:
                    result = {
                        "status": "runner_error",
                        "failure_type": type(exc).__name__,
                    }
                row = {
                    "id": task["id"],
                    "category": task["task_type"],
                    "condition": condition,
                    "query_sha256": task["query_sha256"],
                    **result,
                }
                counts[condition][row["status"]] += 1
                print(json.dumps(row, ensure_ascii=False), file=stream, flush=True)
    write_json(
        output / "run_summary.json", {"attempts": len(jobs), "conditions": counts}
    )


if __name__ == "__main__":
    main()
