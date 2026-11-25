"""Evaluate rubric.rule with recorded evidence; never execute rubric.exec."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

TOOL_ALIASES = {
    "read": "file_read", "edit": "file_edit", "write": "file_write",
    "grep": "file_search", "glob": "file_glob",
    "working_directory": "cwd_inspect", "todo_write": "task_planning",
    "list_mcp_resources": "mcp_resource_list",
    "list_mcp_resource_templates": "mcp_template_list",
    "mcp__e2b__execute_python": "python_exec",
    "mcp__serper__google_search": "web_search",
}
MISSING = object()


def recorded_calls(folder: Path, row: dict):
    """Return the complete, ordered tool-call list only when recording verifies it."""
    path = folder / "trace.jsonl"
    if not path.is_file():
        return None
    try:
        events = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
                  if line.strip()]
    except (OSError, json.JSONDecodeError):
        return None
    calls = []
    for event in events:
        if event.get("type") != "tool_call":
            continue
        if not isinstance(event.get("tool"), str) or "input" not in event:
            return None
        calls.append({"name": TOOL_ALIASES.get(event["tool"], event["tool"]),
                      "args": event["input"]})
    complete = (row.get("recording_status") == "complete"
                and row.get("final_event_seen") is True
                and not row.get("parse_errors")
                and type(row.get("tool_calls")) is int
                and len(calls) == row["tool_calls"])
    return calls if complete else None


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)


def domain_used(text: str, domains: list[str], keywords=(), *, search=False):
    text = unquote(text).lower()
    if search:
        text = re.sub(r"-site:[\w.-]+", "", text)
    for url in re.findall(r"https?://[^\s<>\"\]\)]+", text):
        try:
            host = (urlsplit(url).hostname or "").rstrip(".").lower()
        except ValueError:
            continue
        if any(host == d.lower() or host.endswith("." + d.lower()) for d in domains):
            return True
    if search:
        return any(word.lower() in text for word in keywords) or any(
            re.search(r"(?<![\w.-])(?:[\w-]+\.)*" + re.escape(d.lower()) + r"(?![\w.-])", text)
            for d in domains)
    return False


def markdown_lines(text: str):
    lines, fence = [], None
    for line in text.splitlines():
        match = re.match(r"^\s*(\x60{3,}|~{3,})", line)
        if match:
            marker = match.group(1)[0]
            fence = None if fence == marker else marker
            lines.append("")
        else:
            lines.append(line if fence is None else "")
    return lines


def resolve(value, path: str):
    for part in re.sub(r"\[(\d+|\*)\]", r".\1", path).split("."):
        if part == "*":
            if not isinstance(value, list):
                return MISSING
            return value
        if isinstance(value, dict):
            value = value.get(part, MISSING)
        elif isinstance(value, list) and part.isdigit():
            index = int(part)
            value = value[index] if index < len(value) else MISSING
        else:
            return MISSING
        if value is MISSING:
            return MISSING
    return value


def resolve_projection(context: dict, path: str):
    if ".*." not in path:
        return resolve(context, path)
    prefix, suffix = path.split(".*.", 1)
    array = resolve(context, prefix)
    if not isinstance(array, list):
        return MISSING
    values = [resolve(item, suffix) for item in array]
    return MISSING if any(value is MISSING for value in values) else values


def all_leaf_paths(rule: dict):
    if "all" in rule or "any" in rule:
        children = rule.get("all", rule.get("any"))
        if not isinstance(children, list) or not children:
            return None
        paths = []
        for child in children:
            nested = all_leaf_paths(child)
            if nested is None:
                return None
            paths.extend(nested)
        return paths
    if not isinstance(rule, dict) or not isinstance(rule.get("path"), str):
        return None
    if rule.get("op") == "sources_allowed":
        return ["final_answer", "trace.calls"]
    return [rule["path"]]


def _evaluate(rule: dict, context: dict):
    if "all" in rule or "any" in rule:
        children = rule.get("all", rule.get("any"))
        results = [_evaluate(child, context) for child in children]
        if any(result is None for result in results):
            return None
        return all(results) if "all" in rule else any(results)
    op, expected = rule.get("op"), rule.get("value")
    value = resolve_projection(context, rule["path"])
    if value is MISSING:
        return None
    if op == "sources_allowed":
        if not isinstance(expected, dict) or not isinstance(value, dict):
            return None
        domains = expected.get("domains")
        keywords = expected.get("keywords", [])
        final = context["final_answer"]
        calls = context["trace"]["calls"]
        if not isinstance(domains, list) or not isinstance(final, str) or not isinstance(calls, list):
            return None
        for call in calls:
            for text in strings(call["args"]):
                if domain_used(text, domains, keywords, search="search" in call["name"].lower()):
                    return False
        return not domain_used(final, domains)
    if op == "length_le":
        return len(value) <= expected if isinstance(value, (str, list, dict)) and type(expected) is int else None
    if op in {"count_eq", "count_le"}:
        match = rule.get("match", MISSING)
        if not isinstance(value, list) or match is MISSING:
            return None
        count = sum(type(item) is type(match) and item == match for item in value)
        return (count == expected) if op == "count_eq" else (count <= expected)
    if op == "section_content":
        if not isinstance(value, str) or not isinstance(expected, str):
            return None
        active = False
        for line in markdown_lines(value):
            if re.match(r"^#{1,6} ", line):
                active = line.rstrip() == "## " + expected
            elif active and line.strip():
                return True
        return False
    if op == "all_prefix":
        if not isinstance(value, list) or not value or not all(isinstance(item, str) for item in value) or not isinstance(expected, str):
            return None
        return all(isinstance(item, str) and item.replace("\\", "/").startswith(expected)
                   and ".." not in item.replace("\\", "/").split("/") for item in value)
    if op == "eq":
        return type(value) is type(expected) and value == expected
    return None


def evaluate_rule(rule: dict, final: str | None, calls: list[dict] | None,
                  artifact_paths: list[str] | None):
    """Return True, False or None. Missing evidence and unsupported rules stay unknown."""
    if not isinstance(rule, dict):
        return None
    context = {
        "final_answer": final if final is not None else MISSING,
        "trace": {"calls": calls} if calls is not None else MISSING,
        "artifacts": [{"path": path} for path in artifact_paths]
                     if artifact_paths is not None else MISSING,
    }
    paths = all_leaf_paths(rule)
    if paths is None or any(resolve_projection(context, path) is MISSING for path in paths):
        return None
    try:
        return _evaluate(rule, context)
    except (KeyError, TypeError, ValueError):
        return None
