"""Validate an entire JSONL batch and its attachments without starting models."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from dsh_e2b_environment import Environment


def validate(path: Path, expected: int | None = None) -> dict[str, int]:
    """Validate records, unique IDs and in-tree regular attachments before paid requests."""
    path = path.resolve(strict=True)
    ids = set()
    count = attachments = placeholders = 0
    for number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip():
            continue
        item = json.loads(line)
        if not isinstance(item, dict) or not isinstance(item.get("user_query"), str) or not item["user_query"].strip():
            raise ValueError(f"line {number}: user_query must be nonempty")
        identifier = item.get("id", number)
        if not isinstance(identifier, (str, int)) or isinstance(identifier, bool) or str(identifier) in ids:
            raise ValueError(f"line {number}: id must be a unique string or integer")
        ids.add(str(identifier))
        files = item.get("attached_files", [])
        if not isinstance(files, list):
            raise ValueError(f"line {number}: attached_files must be an array")
        for name in files:
            if not isinstance(name, str) or not name.strip():
                raise ValueError(f"line {number}: invalid attachment path")
            candidate = path.parent / name
            try:
                resolved = Environment.safe_file(path.parent, candidate)
            except (ValueError, OSError) as error:
                raise ValueError(f"line {number}: invalid attachment {name}: {error}") from error
            if resolved.name == ".keep":
                placeholders += 1
            attachments += 1
        count += 1
    if not count or (expected is not None and count != expected):
        raise ValueError(f"expected {expected or 'a nonempty batch'} tasks, found {count}")
    return {"tasks": count, "attachment_references": attachments, "empty_keep_files": placeholders}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--expected-count", type=int)
    arguments = parser.parse_args()
    print(json.dumps(validate(arguments.input, arguments.expected_count)))
