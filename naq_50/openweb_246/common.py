"""Read the published query manifest and verify its upstream provenance."""

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "user_query_openweb_246.jsonl"
REVISION = "b2623f8653065c2672de6d941fc5434cd652376c"
CSV_SHA256 = "25d48dcf7efa872e5467032e8b8eedf38d301f59a252d0da95cda584baa78396"
CONDITIONS = ("S0", "S1", "S2")


def sha256(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_jsonl(path):
    with path.open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def read_events(path):
    if not path.is_file():
        return []
    events = []
    with path.open(encoding="utf-8", errors="replace") as stream:
        for line in stream:
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(event, dict):
                events.append(event)
    return events


def write_json(path, value):
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def load_tasks(path=MANIFEST):
    tasks = read_jsonl(path)
    if len(tasks) != 23 or len({task["id"] for task in tasks}) != 23:
        raise ValueError("Expected 23 distinct DeepSearchQA tasks")
    if Counter(task["task_type_id"] for task in tasks) != {2: 7, 4: 8, 6: 8}:
        raise ValueError("Unexpected task type counts")
    for task in tasks:
        row = task["source_row_0"]
        if (
            type(row) is not int
            or not 0 <= row < 900
            or task["id"] != f"DSQA-{row:03d}"
            or task["source_uid"] != f"row_{row}"
            or task["source_revision"] != REVISION
            or task["attached_files"] != []
            or task["query_sha256"] != sha256(task["user_query"])
        ):
            raise ValueError(f"Invalid task provenance for {task['id']}")
    return tasks


def load_references(path, tasks):
    if hashlib.sha256(path.read_bytes()).hexdigest() != CSV_SHA256:
        raise ValueError("DeepSearchQA CSV SHA-256 does not match the pinned snapshot")
    with path.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    references = {}
    for task in tasks:
        row = rows[task["source_row_0"]]
        if (
            row["problem"] != task["user_query"]
            or row["problem_category"] != task["source_category"]
        ):
            raise ValueError(f"Source mismatch for {task['id']}")
        references[task["id"]] = row
    return references
