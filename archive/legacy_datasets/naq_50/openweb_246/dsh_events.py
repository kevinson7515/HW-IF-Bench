"""Read DSH JSON events and identify usable web fetches."""

import hashlib
import json
import re
from urllib.parse import urlsplit, urlunsplit

from common import read_events


def normalize(url):
    if not isinstance(url, str):
        return ""
    try:
        data = urlsplit(url.strip())
        if (
            data.scheme not in ("http", "https")
            or not data.hostname
            or data.username
            or data.password
        ):
            return ""
        return urlunsplit(
            (
                data.scheme.lower(),
                data.netloc.lower(),
                data.path.rstrip("/") or "/",
                data.query,
                "",
            )
        )
    except ValueError:
        return ""


def observed(path):
    events = read_events(path)
    pairs = {}
    trace = []
    last_final = max(
        (i for i, r in enumerate(events) if r.get("type") == "final"), default=-1
    )
    for i, row in enumerate(events):
        phase = row.get("type")
        key = row.get("callId")
        if phase == "tool_call":
            entry = {
                "event_index": i,
                "tool": row.get("tool"),
                "input": row.get("input"),
            }
            trace.append(entry)
            pairs[key] = entry
        if phase == "tool_result" and key in pairs:
            entry = pairs[key]
            entry["result_index"] = i
            entry["status"] = row.get("status")
            payload = row.get("result", "")
            if not isinstance(payload, str):
                payload = json.dumps(payload, ensure_ascii=False)
            entry["body"] = payload
            entry["result_sha256"] = hashlib.sha256(payload.encode()).hexdigest()
    return trace, last_final


def verified_fetch(entry):
    if entry["tool"] != "web_fetch" or entry.get("status") != "completed":
        return ""
    data = entry.get("input") or {}
    if not isinstance(data, dict):
        return ""
    link = normalize(data.get("url"))
    payload = entry.get("body", "")
    if not re.match(r"^Fetched https?://.+ \(HTTP 2[0-9]{2}\)", payload):
        return ""
    content = payload.split("External web content follows.", 1)[-1]
    blocked = r"checking your browser|sorry, you have been blocked|attention required!|verify you are human|enable javascript and cookies to continue"
    if len(content.strip()) < 350 or re.search(blocked, content[:850], re.I):
        return ""
    return link
