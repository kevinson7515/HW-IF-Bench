#!/usr/bin/env python3
"""Run benchmark variants through headless dsh, archive changes, and restore the workspace."""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import re
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from collections.abc import Iterator
from dsh_simulated_user import simulated_user_patch


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def sync_directory(path: Path) -> None:
    if os.name == "posix":
        descriptor = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    descriptor, temporary = tempfile.mkstemp(prefix=".benchmark-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        sync_directory(path.parent)
    finally:
        Path(temporary).unlink(missing_ok=True)


def write_text(path: Path, value: str) -> None:
    with path.open("x", encoding="utf-8", newline="") as stream:
        stream.write(value)
        stream.flush()
        os.fsync(stream.fileno())
    sync_directory(path.parent)


def positive_env(name: str, default: int) -> int:
    raw = os.environ.get(name, str(default))
    if not raw.isdecimal() or int(raw) < 1:
        raise ValueError(f"{name} must be a positive integer")
    return int(raw)


def process_start_ticks(pid: int) -> str | None:
    try:
        fields = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()
        return fields[19]
    except FileNotFoundError:
        return None


def identifier(value: object, name: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,99}", value):
        raise ValueError(f"{name} must contain 1 to 100 filename-safe characters")
    return value


def load_cases(source: Path, root: Path) -> list[dict[str, Any]]:
    groups = json.loads(source.read_text(encoding="utf-8-sig"))
    if not isinstance(groups, list) or not groups:
        raise ValueError("benchmark_groups.json must contain a nonempty array")
    cases: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    group_ids: set[str] = set()
    for group in groups:
        if not isinstance(group, dict):
            raise ValueError("each group must be an object")
        group_id = identifier(group.get("group_id"), "group_id")
        if group_id in group_ids:
            raise ValueError(f"duplicate group_id: {group_id}")
        group_ids.add(group_id)
        query = group.get("user_query")
        variants = group.get("variants")
        if not isinstance(query, str) or not query.strip() or not isinstance(variants, list) or not variants:
            raise ValueError(f"{group_id}: user_query and variants must be nonempty")
        attachments = group.get("attached_files", [])
        if not isinstance(attachments, list):
            raise ValueError(f"{group_id}: attached_files must be an array")
        resolved: list[str] = []
        for item in attachments:
            if not isinstance(item, str) or not item.strip():
                raise ValueError(f"{group_id}: attachment must be a nonempty path")
            candidate = Path(item)
            if not candidate.is_absolute():
                candidate = source.parent / candidate
            attachment = candidate.resolve(strict=True)
            if not attachment.is_file() or not attachment.is_relative_to(root):
                raise ValueError(f"{group_id}: attachment must be a regular file inside the repository: {item}")
            if protected(attachment.relative_to(root)):
                raise ValueError(f"{group_id}: attachment is in an excluded runtime directory: {item}")
            resolved.append(str(attachment))
        for variant in variants:
            if not isinstance(variant, dict):
                raise ValueError(f"{group_id}: variant must be an object")
            variant_id = identifier(variant.get("variant_id"), "variant_id")
            key = (group_id, variant_id)
            if key in seen:
                raise ValueError(f"duplicate variant: {group_id}/{variant_id}")
            seen.add(key)
            prompt = variant.get("effective_system_prompt")
            if not isinstance(prompt, str) or not prompt.strip():
                raise ValueError(f"{group_id}/{variant_id}: effective_system_prompt must be nonempty")
            prompt_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
            if variant.get("system_prompt_sha256", prompt_hash) != prompt_hash:
                raise ValueError(f"{group_id}/{variant_id}: system_prompt_sha256 does not match the prompt")
            cases.append({
                "group_id": group_id, "variant_id": variant_id,
                "task_id": group.get("task_id"), "user_query": query,
                "effective_system_prompt": prompt, "system_prompt_sha256": prompt_hash,
                "attached_files": attachments, "resolved_attached_files": resolved,
                "group_metadata": {key: value for key, value in group.items() if key != "variants"},
                "variant_metadata": variant,
                "environment_override_applied": False,
                "user_query_append_applied": False,
            })
    return cases


def protected(relative: Path) -> bool:
    return any(part in {".git", "node_modules"} for part in relative.parts) or (
        len(relative.parts) == 1 and re.fullmatch(r"dsh_.*\.(out|err)", relative.name) is not None
    )


def same(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return {key: value for key, value in left.items() if key != "mtime_ns"} == {
        key: value for key, value in right.items() if key != "mtime_ns"
    }


def relative_parts(relative: str) -> list[str]:
    parts = relative.split("/")
    if any(part in {"", ".", ".."} for part in parts) or "\\" in relative or ":" in parts[0]:
        raise ValueError(f"invalid workspace path: {relative}")
    return parts


def copy_verified(source: Path, destination: Path, expected: dict[str, Any]) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    descriptor = os.open(source, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    value = hashlib.sha256()
    size = 0
    try:
        with os.fdopen(descriptor, "rb") as incoming, destination.open("xb") as outgoing:
            if not stat.S_ISREG(os.fstat(incoming.fileno()).st_mode):
                raise ValueError(f"source is no longer a regular file: {source}")
            for chunk in iter(lambda: incoming.read(1024 * 1024), b""):
                outgoing.write(chunk)
                value.update(chunk)
                size += len(chunk)
            outgoing.flush()
            os.fsync(outgoing.fileno())
        os.chmod(destination, 0o600)
        if size != expected["size"] or value.hexdigest() != expected["sha256"]:
            raise ValueError(f"file changed during recording: {source}")
        sync_directory(destination.parent)
    except BaseException:
        destination.unlink(missing_ok=True)
        raise


class Workspace:
    """Own one durable baseline of regular files, directories, and symbolic links."""

    def __init__(self, root: Path, store: Path) -> None:
        self.root = root.resolve(strict=True)
        self.store = store.resolve()
        if self.root == Path(self.root.anchor) or self.store.is_relative_to(self.root):
            raise ValueError("baseline storage must be outside a non-root repository directory")
        self.entries: dict[str, dict[str, Any]] = {}

    def path(self, relative: str) -> Path:
        parts = relative_parts(relative)
        target = self.root.joinpath(*parts)
        if not target.is_relative_to(self.root):
            raise ValueError(f"workspace path escapes repository: {relative}")
        for parent in target.parents:
            if parent == self.root:
                break
            if parent.is_symlink():
                raise ValueError(f"workspace path traverses a symbolic link: {relative}")
        return target

    def scan(self) -> dict[str, dict[str, Any]]:
        entries: dict[str, dict[str, Any]] = {}

        def visit(directory: Path) -> None:
            with os.scandir(directory) as children:
                for child in sorted(children, key=lambda item: item.name):
                    path = Path(child.path)
                    relative = path.relative_to(self.root)
                    if protected(relative):
                        continue
                    metadata = child.stat(follow_symlinks=False)
                    if getattr(metadata, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0) and not stat.S_ISLNK(metadata.st_mode):
                        raise ValueError(f"unsupported filesystem reparse point: {relative}")
                    item: dict[str, Any] = {"mode": stat.S_IMODE(metadata.st_mode), "mtime_ns": metadata.st_mtime_ns}
                    if stat.S_ISLNK(metadata.st_mode):
                        item.update(type="symlink", target=os.readlink(path))
                    elif stat.S_ISDIR(metadata.st_mode):
                        item["type"] = "directory"
                    elif stat.S_ISREG(metadata.st_mode):
                        item.update(type="file", size=metadata.st_size, sha256=digest(path))
                    else:
                        raise ValueError(f"unsupported workspace entry: {relative}")
                    entries[relative.as_posix()] = item
                    if item["type"] == "directory":
                        visit(path)

        visit(self.root)
        return entries

    def snapshot(self) -> None:
        self.store.mkdir(mode=0o700, parents=True, exist_ok=False)
        self.entries = self.scan()
        total = sum(item.get("size", 0) for item in self.entries.values())
        if total > positive_env("DSH_BENCHMARK_BASELINE_MAX_BYTES", 10 * 1024 ** 3):
            raise ValueError(f"workspace baseline is too large ({total} bytes)")
        for relative, item in self.entries.items():
            if item["type"] == "file":
                copy_verified(self.path(relative), self.store / "files" / relative, item)
        if not self.matches(self.scan()):
            raise ValueError("workspace changed while its baseline was being saved")
        write_json(self.store / "manifest.json", {"root": str(self.root), "entries": self.entries})

    def load(self) -> None:
        manifest = json.loads((self.store / "manifest.json").read_text(encoding="utf-8"))
        if manifest["root"] != str(self.root):
            raise ValueError("baseline belongs to a different workspace")
        self.entries = manifest["entries"]
        if not isinstance(self.entries, dict):
            raise ValueError("baseline entries must be an object")
        for relative, item in self.entries.items():
            relative_parts(relative)
            if not isinstance(item, dict) or item.get("type") not in {"file", "directory", "symlink"}:
                raise ValueError(f"invalid baseline entry: {relative}")
            if not isinstance(item.get("mode"), int) or not 0 <= item["mode"] <= 0o7777 or not isinstance(item.get("mtime_ns"), int):
                raise ValueError(f"invalid baseline metadata: {relative}")
            if protected(Path(relative)):
                raise ValueError(f"baseline includes protected runtime entry: {relative}")
            if item["type"] == "file":
                backup = self.store / "files" / relative
                if not isinstance(item.get("size"), int) or item["size"] < 0 or not isinstance(item.get("sha256"), str):
                    raise ValueError(f"invalid baseline file metadata: {relative}")
                if not backup.resolve(strict=True).is_relative_to(self.store) or backup.is_symlink() or not backup.is_file() or digest(backup) != item["sha256"]:
                    raise ValueError(f"baseline file is missing or corrupt: {relative}")
            elif item["type"] == "symlink" and not isinstance(item.get("target"), str):
                raise ValueError(f"invalid baseline symbolic link: {relative}")

    def matches(self, entries: dict[str, dict[str, Any]]) -> bool:
        return entries.keys() == self.entries.keys() and all(same(self.entries[key], entries[key]) for key in entries)

    def archive(self, task_dir: Path, after: dict[str, dict[str, Any]]) -> dict[str, Any]:
        created = sorted(after.keys() - self.entries.keys())
        deleted = sorted(self.entries.keys() - after.keys())
        modified = sorted(key for key in after.keys() & self.entries.keys() if not same(after[key], self.entries[key]))
        files = [key for key in created + modified if after[key]["type"] == "file"]
        max_file = positive_env("DSH_ARTIFACT_MAX_FILE_BYTES", 100 * 1024 ** 2)
        max_total = positive_env("DSH_ARTIFACT_MAX_TOTAL_BYTES", 1024 ** 3)
        if any(after[key]["size"] > max_file for key in files) or sum(after[key]["size"] for key in files) > max_total:
            raise ValueError("artifact size limit exceeded; workspace retained, raise DSH_ARTIFACT_MAX_* before recovery")
        copied = []
        for relative in files:
            destination = task_dir / "artifacts" / relative
            copy_verified(self.path(relative), destination, after[relative])
            copied.append({"path": relative, "copy": str(destination), "change": "created" if relative in created else "modified", **after[relative]})
        manifest = {
            "status": "complete", "scope": str(self.root), "detection": "file bytes, permissions, entry types, and symbolic-link targets",
            "created": created, "modified": modified, "deleted": deleted, "copied": copied,
            "entries": {key: after[key] for key in created + modified},
            "deleted_entries": {key: self.entries[key] for key in deleted},
        }
        if not equivalent(after, self.scan()):
            raise ValueError("workspace changed during artifact recording; cleanup stopped")
        write_json(task_dir / "artifacts.json", manifest)
        return manifest

    def restore(self, expected: dict[str, dict[str, Any]]) -> None:
        if not equivalent(expected, self.scan()):
            raise ValueError("workspace changed after recording; cleanup stopped")
        affected = {relative for relative in self.entries.keys() | expected.keys()
                    if relative not in self.entries or relative not in expected
                    or not same(self.entries[relative], expected[relative])
                    or self.entries[relative]["mtime_ns"] != expected[relative]["mtime_ns"]}
        for relative in list(affected):
            while "/" in relative:
                relative = relative.rsplit("/", 1)[0]
                affected.add(relative)
        # Verify originals needed by this restore before removing task-created entries.
        for relative, item in self.entries.items():
            if relative in affected and item["type"] == "file" and digest(self.store / "files" / relative) != item["sha256"]:
                raise ValueError(f"corrupt baseline: {relative}")
        for relative in sorted(expected, key=lambda key: (key.count("/"), key), reverse=True):
            current = expected[relative]
            original = self.entries.get(relative)
            if original is not None and current["type"] == original["type"]:
                continue
            target = self.path(relative)
            if current["type"] == "directory":
                target.rmdir()
            else:
                target.unlink()
        for relative in sorted(self.entries, key=lambda key: (key.count("/"), key)):
            if relative not in affected:
                continue
            original = self.entries[relative]
            target = self.path(relative)
            current = expected.get(relative)
            if original["type"] == "directory":
                target.mkdir(mode=0o700, exist_ok=True)
                os.chmod(target, original["mode"] | 0o700)
            elif current is None or not same(current, original):
                if original["type"] == "symlink":
                    target.unlink(missing_ok=True)
                    os.symlink(original["target"], target)
                else:
                    descriptor, temporary = tempfile.mkstemp(prefix=".benchmark-restore-", dir=target.parent)
                    os.close(descriptor)
                    Path(temporary).unlink()
                    try:
                        copy_verified(self.store / "files" / relative, Path(temporary), original)
                        os.replace(temporary, target)
                    finally:
                        Path(temporary).unlink(missing_ok=True)
            if original["type"] == "file":
                os.chmod(target, original["mode"])
                os.utime(target, ns=(original["mtime_ns"], original["mtime_ns"]))
        for relative in sorted(self.entries, key=lambda key: (key.count("/"), key), reverse=True):
            original = self.entries[relative]
            if relative in affected and original["type"] == "directory":
                target = self.path(relative)
                os.chmod(target, original["mode"])
                os.utime(target, ns=(original["mtime_ns"], original["mtime_ns"]))
        if not self.matches(self.scan()):
            raise ValueError("workspace restore verification failed; baseline retained")
        sync_directory(self.root)


def equivalent(left: dict[str, dict[str, Any]], right: dict[str, dict[str, Any]]) -> bool:
    return left.keys() == right.keys() and all(same(left[key], right[key]) for key in left)


def read_trace(path: Path, prompt: str | None, query: str) -> tuple[dict[str, Any], dict[str, Any]]:
    info: dict[str, Any] = {"session_id": None, "final_event_seen": False, "final_text": "", "parse_errors": [], "tool_calls": 0, "tool_errors": 0, "steps": 0}
    messages: list[dict[str, Any]] = ([] if prompt is None else [{"role": "system", "content": prompt}]) + [{"role": "user", "content": query}]
    text: list[str] = []
    thinking: list[str] = []
    calls: list[dict[str, Any]] = []

    def flush() -> None:
        if text or thinking or calls:
            messages.append({"role": "assistant", "content": "".join(text), "weight": 1,
                             **({"reasoning_content": "".join(thinking)} if thinking else {}),
                             **({"tool_calls": list(calls)} if calls else {})})
            text.clear()
            thinking.clear()
            calls.clear()

    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError as error:
                info["parse_errors"].append(f"line {line_number}: {error}")
                continue
            kind = event.get("type")
            if kind == "session":
                info["session_id"] = event.get("sessionId")
            elif kind in {"text", "thinking"}:
                (text if kind == "text" else thinking).append(event.get("text", ""))
            elif kind == "tool_call":
                info["tool_calls"] += 1
                arguments = event.get("input", {})
                calls.append({"id": event.get("callId"), "type": "function", "function": {
                    "name": event.get("tool"), "arguments": arguments if isinstance(arguments, str) else json.dumps(arguments, ensure_ascii=False)}})
            elif kind == "tool_result":
                flush()
                info["tool_errors"] += event.get("status") == "error"
                result = event.get("result", "")
                messages.append({"role": "tool", "tool_call_id": event.get("callId"),
                                 "content": result if isinstance(result, str) else json.dumps(result, ensure_ascii=False)})
            elif kind == "simulated_user":
                flush()
                messages.append({"role": "user", "content": event["text"], "simulated": True,
                                 "model": event["model"], "message_id": event["messageId"]})
            elif kind == "status" and event.get("phase") == "step_end":
                flush()
                info["steps"] += 1
            elif kind == "status" and event.get("phase") == "turn_end":
                info["turn_end_reason"] = event.get("reason")
            elif kind == "final":
                info["final_event_seen"] = True
                info["final_text"] = event.get("text", "")
    flush()
    if info["final_text"] and not any(message.get("role") == "assistant" and info["final_text"] in message.get("content", "") for message in messages):
        messages.append({"role": "assistant", "content": info["final_text"], "weight": 1})
    return info, {"format": "openai-chat-like-projection", "lossless": False, "source": str(path),
                  "system_source": "persisted Session system/message (not projected)" if prompt is None else "benchmark effective_system_prompt",
                  "variant_system_prompt_applied": prompt is not None, "trace": messages}


def archive_session(home: Path, task_dir: Path, session_id: str | None) -> dict[str, Any]:
    if session_id is None:
        result = {"status": "not_created", "session_id": None, "copied": []}
    else:
        matches = []
        for directory, children, _files in os.walk(home / "sessions", followlinks=False):
            children[:] = [name for name in children if not (Path(directory) / name).is_symlink()]
            if Path(directory).name == session_id:
                matches.append(Path(directory))
                children[:] = []
        if len(matches) != 1:
            raise ValueError(f"expected one Session directory for {session_id}, found {len(matches)}")
        copied = []
        for directory, children, files in os.walk(matches[0], followlinks=False):
            children[:] = [name for name in children if not (Path(directory) / name).is_symlink()]
            for name in files:
                source = Path(directory) / name
                if not stat.S_ISREG(source.lstat().st_mode):
                    continue
                relative = source.relative_to(matches[0])
                destination = task_dir / "session-records" / relative
                expected = {"size": source.stat().st_size, "sha256": digest(source)}
                copy_verified(source, destination, expected)
                copied.append({"path": relative.as_posix(), "copy": str(destination), **expected})
        result = {"status": "complete", "session_id": session_id, "source": str(matches[0]), "copied": copied}
    write_json(task_dir / "session-records.json", result)
    return result


class Runner:
    """Serialize fresh headless sessions and own cancellation through artifact cleanup."""

    def __init__(self, root: Path, records: Path, home: Path, journal: Path, patches: list[Path], launcher: list[str] | None = None) -> None:
        self.root, self.records, self.home, self.journal = root, records, home, journal
        self.patches = patches
        self.launcher = launcher or ["pnpm", "--silent", "dsh"]
        self.workspace = Workspace(root, records / "workspace-baseline")
        self.process: subprocess.Popen[bytes] | None = None
        self.interrupted: int | None = None

    def stop(self, signum: int, _frame: object) -> None:
        self.interrupted = signum
        self.terminate(signal.SIGTERM)

    def terminate(self, signum: int) -> None:
        if self.process is not None and self.process.poll() is None:
            try:
                if os.name == "posix":
                    os.killpg(self.process.pid, signum)
                elif signum == signal.SIGTERM:
                    self.process.terminate()
                else:
                    self.process.kill()
            except ProcessLookupError:
                pass

    def execute(self, command: list[str], query: str, trace: Path, errors: Path) -> int:
        grace = positive_env("DSH_BENCHMARK_STOP_GRACE_SECONDS", 20)
        environment = {**os.environ, "DSH_E2B_TASK_FILE": str(trace.parent / "task.json")}
        with trace.open("wb") as stdout, errors.open("wb") as stderr:
            self.process = subprocess.Popen(command, cwd=self.root, env=environment, stdin=subprocess.PIPE,
                                            stdout=stdout, stderr=stderr, start_new_session=True)
            deadline: float | None = None
            try:
                if os.name == "posix" and self.journal.exists():
                    pending = json.loads(self.journal.read_text(encoding="utf-8"))
                    pending.update(child_pid=self.process.pid, child_start_ticks=process_start_ticks(self.process.pid))
                    write_json(self.journal, pending)
                if self.interrupted is not None:
                    self.terminate(signal.SIGTERM)
                incoming: bytes | None = query.encode("utf-8")
                while True:
                    try:
                        self.process.communicate(incoming, timeout=1)
                        break
                    except subprocess.TimeoutExpired:
                        incoming = None
                        if self.interrupted is not None:
                            deadline = deadline or time.monotonic() + grace
                            if time.monotonic() >= deadline:
                                self.terminate(getattr(signal, "SIGKILL", signal.SIGTERM))
                return self.process.returncode
            finally:
                if self.process.poll() is None:
                    self.terminate(getattr(signal, "SIGKILL", signal.SIGTERM))
                    self.process.wait()
                self.process = None
                for stream in (stdout, stderr):
                    stream.flush()
                    os.fsync(stream.fileno())

    def run_case(self, case: dict[str, Any]) -> dict[str, Any]:
        task_dir = self.records / case["group_id"] / case["variant_id"]
        task_dir.mkdir(mode=0o700, parents=True, exist_ok=False)
        if not self.workspace.matches(self.workspace.scan()):
            raise ValueError("workspace differs from the saved baseline before the next variant")
        query = case["user_query"]
        if case["resolved_attached_files"]:
            query += "\n\nAttached files are available at the following paths. Read them as needed:\n" + "\n".join(
                f"- {path}" for path in case["resolved_attached_files"])
        inputs = []
        for source_text in case["resolved_attached_files"]:
            source = Path(source_text)
            relative = source.relative_to(self.root)
            expected = self.workspace.entries[relative.as_posix()]
            destination = task_dir / "inputs" / relative
            copy_verified(source, destination, expected)
            inputs.append({"source": source_text, "copy": str(destination), **expected})
        write_json(task_dir / "inputs" / "manifest.json", inputs)
        write_json(task_dir / "task.json", {**case, "variant_system_prompt_applied": False,
                                          "effective_query": query, "provider": os.environ.get("DSH_MODEL_PROVIDER"), "started_at": now()})
        prompt_file = task_dir / "variant_system_prompt.txt"
        write_text(prompt_file, case["effective_system_prompt"])
        command = self.launcher + ["--profile", "headless"]
        for patch in self.patches + simulated_user_patch(self.root, task_dir):
            command.extend(("--patch", str(patch)))
        command.extend(("--json", "-"))
        started_at, started = now(), time.monotonic()
        write_json(self.journal, {"root": str(self.root), "records": str(self.records), "active_case": str(task_dir),
                                  "lock_file": os.environ.get("DSH_BENCHMARK_LOCK_FILE")})
        trace, diagnostics = task_dir / "trace.jsonl", task_dir / "diagnostics.log"
        print(f"[benchmark] {case['group_id']}/{case['variant_id']}: starting", flush=True)
        code = self.execute(command, query, trace, diagnostics)
        executed = time.monotonic()
        info, projection = read_trace(trace, None, query)
        write_json(task_dir / "trace.json", projection)
        write_text(task_dir / "final.txt", info["final_text"])
        archive_session(self.home, task_dir, info["session_id"])
        after = self.workspace.scan()
        self.workspace.archive(task_dir, after)
        recorded = time.monotonic()
        result = {
            "group_id": case["group_id"], "variant_id": case["variant_id"], "task_id": case["task_id"],
            "provider": os.environ.get("DSH_MODEL_PROVIDER"),
            "simulated_user_enabled": os.environ.get("DSH_SIM_USER", "0") == "1",
            "variant_system_prompt_applied": False,
            "status": "interrupted" if self.interrupted is not None else ("succeeded" if code == 0 and info["final_event_seen"] and not info["parse_errors"] else "failed"),
            "exit_code": code, "started_at": started_at, "finished_at": now(),
            "duration_seconds": round(time.monotonic() - started, 3),
            "execution_duration_seconds": round(executed - started, 3),
            "recording_duration_seconds": round(recorded - executed, 3),
            "variant_system_prompt_sha256": case["system_prompt_sha256"], "task_dir": str(task_dir),
            "recording_status": "complete", "workspace_restore_status": "pending",
            "signal": self.interrupted,
            **{key: value for key, value in info.items() if key != "final_text"},
        }
        write_json(task_dir / "result.json", result)
        self.workspace.restore(after)
        result["workspace_restore_status"] = "complete"
        result["restore_duration_seconds"] = round(time.monotonic() - recorded, 3)
        result["duration_seconds"] = round(time.monotonic() - started, 3)
        result["finished_at"] = now()
        write_json(task_dir / "result.json", result)
        self.journal.unlink()
        sync_directory(self.journal.parent)
        print(f"[benchmark] {case['group_id']}/{case['variant_id']}: {result['status']} (exit={code}, recorded, workspace restored)", flush=True)
        return result


@contextlib.contextmanager
def recovery_lock(path: Path) -> Iterator[None]:
    if not sys.platform.startswith("linux"):
        raise ValueError("cluster recovery requires Linux and its repository flock")
    import fcntl
    with path.open("a") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield


def recover(records: Path) -> None:
    plan = json.loads((records / "plan.json").read_text(encoding="utf-8"))
    root = Path(plan["root"]).resolve(strict=True)
    if root != Path.cwd().resolve():
        raise ValueError(f"run recovery from the original repository: {root}")
    with recovery_lock(Path(plan["lock_file"])):
        workspace = Workspace(root, records / "workspace-baseline")
        workspace.load()
        journal = Path(plan["journal"])
        pending = json.loads(journal.read_text(encoding="utf-8"))
        if Path(pending["records"]).resolve() != records.resolve() or Path(pending["root"]).resolve() != root:
            raise ValueError("pending journal belongs to a different benchmark")
        if isinstance(pending.get("child_pid"), int):
            current_start = process_start_ticks(pending["child_pid"])
            if current_start is not None and current_start == pending.get("child_start_ticks"):
                raise ValueError("benchmark child is still running; cancel the Slurm job and wait for it to exit before recovery")
        after = workspace.scan()
        destination = records / ("recovery-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f"))
        destination.mkdir(mode=0o700)
        active_case = Path(pending["active_case"]).resolve(strict=True)
        if not active_case.is_relative_to(records.resolve()):
            raise ValueError("active task recording directory leaves this benchmark")
        active_trace = active_case / "trace.jsonl"
        if active_trace.is_file():
            task = json.loads((active_case / "task.json").read_text(encoding="utf-8"))
            info, projection = read_trace(active_trace, task["effective_system_prompt"] if task.get("variant_system_prompt_applied", True) else None, task["effective_query"])
            copy_verified(active_trace, destination / "trace.jsonl", {"size": active_trace.stat().st_size, "sha256": digest(active_trace)})
            write_json(destination / "trace.json", projection)
            archive_session(Path(plan["home"]), destination, info["session_id"])
        workspace.archive(destination, after)
        workspace.restore(after)
        write_json(destination / "restore.json", {"status": "complete", "finished_at": now()})
        journal.unlink()
        sync_directory(journal.parent)
        print(f"workspace restored; interrupted-task files archived in {destination}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, help="validate dataset and attachments without credentials or task execution")
    parser.add_argument("--restore", type=Path, help="archive residual changes and restore a stopped benchmark's saved baseline")
    args = parser.parse_args()
    if args.restore:
        recover(args.restore.resolve(strict=True))
        return 0
    root = Path(os.environ.get("DSH_BATCH_REPO_ROOT", Path.cwd())).resolve(strict=True)
    source = (args.check or Path(os.environ["DSH_BATCH_INPUT_JSONL"])).resolve(strict=True)
    cases = load_cases(source, root)
    if args.check:
        print(json.dumps({"groups": len({case['group_id'] for case in cases}), "variants": len(cases),
                          "cases": [f"{case['group_id']}/{case['variant_id']}" for case in cases],
                          "environment_overrides_not_applied": [f"{case['group_id']}/{case['variant_id']}" for case in cases if case['variant_metadata'].get('environment_override')]}, ensure_ascii=False, indent=2))
        return 0
    for field, variable in (("group_id", "DSH_BENCHMARK_GROUPS"), ("variant_id", "DSH_BENCHMARK_VARIANTS")):
        if os.environ.get(variable):
            wanted = set(os.environ[variable].split(","))
            missing = wanted - {case[field] for case in cases}
            if missing:
                raise ValueError(f"{variable} contains unknown identifiers: {sorted(missing)}")
            cases = [case for case in cases if case[field] in wanted]
    if not cases:
        raise ValueError("benchmark selection is empty")
    records = Path(os.environ["DSH_BATCH_OUTPUT_DIR"]).resolve(strict=True)
    home = Path(os.environ["DSH_HOME"]).resolve()
    journal = Path(os.environ["DSH_BENCHMARK_JOURNAL"]).resolve()
    if any(path.is_relative_to(root) for path in (records, home, journal)):
        raise ValueError("benchmark records, DSH_HOME, and recovery journal must be outside the repository")
    if journal.exists():
        raise ValueError(f"pending workspace recovery: {journal}")
    if (records / "plan.json").exists():
        raise ValueError("benchmark output already exists; use a new DSH_BATCH_ID")
    patches = [Path(os.environ[name]).resolve(strict=True) for name in ("DSH_BATCH_PATCH_FILE", "DSH_BATCH_TOOLS_PATCH_FILE")]
    runner = Runner(root, records, home, journal, patches)
    signal.signal(signal.SIGTERM, runner.stop)
    signal.signal(signal.SIGINT, runner.stop)
    write_json(records / "plan.json", {"root": str(root), "home": str(home), "provider": os.environ["DSH_MODEL_PROVIDER"], "input": str(source),
                                       "simulated_user_enabled": os.environ.get("DSH_SIM_USER", "0") == "1",
                                       "variant_system_prompt_applied": False,
                                       "input_sha256": digest(source), "journal": str(journal),
                                       "lock_file": os.environ["DSH_BENCHMARK_LOCK_FILE"],
                                       "selected": [f"{case['group_id']}/{case['variant_id']}" for case in cases],
                                       "patches": [{"path": str(path), "sha256": digest(path)} for path in patches]})
    copy_verified(source, records / "benchmark_groups.json", {"size": source.stat().st_size, "sha256": digest(source)})
    print(f"[benchmark] saving workspace baseline for {len(cases)} variants", flush=True)
    runner.workspace.snapshot()
    print(f"[benchmark] baseline saved ({len(runner.workspace.entries)} entries)", flush=True)
    results = []
    attempted = 0
    fatal: str | None = None
    try:
        with (records / "results.jsonl").open("x", encoding="utf-8", newline="\n") as stream:
            for case in cases:
                if runner.interrupted is not None:
                    break
                attempted += 1
                try:
                    result = runner.run_case(case)
                except Exception as error:
                    fatal = str(error)
                    task_dir = records / case["group_id"] / case["variant_id"]
                    result_path = task_dir / "result.json"
                    previous = json.loads(result_path.read_text(encoding="utf-8")) if result_path.exists() else {}
                    failure = {**previous, "group_id": case["group_id"], "variant_id": case["variant_id"],
                               "provider": os.environ.get("DSH_MODEL_PROVIDER"),
                               "task_id": case["task_id"], "status": "failed", "error": fatal,
                               "recording_status": previous.get("recording_status", "failed"),
                               "workspace_restore_status": "failed" if previous else "not_attempted", "finished_at": now(), "task_dir": str(task_dir)}
                    write_json(result_path, failure)
                    results.append(failure)
                    stream.write(json.dumps(failure, ensure_ascii=False) + "\n")
                    stream.flush()
                    os.fsync(stream.fileno())
                    write_json(records / "fatal.json", {"error": fatal, "group_id": case["group_id"], "variant_id": case["variant_id"],
                                                         "workspace_retained": True, "journal": str(journal), "time": now()})
                    print(f"[benchmark] stopped: {fatal}; workspace and baseline retained for recovery", file=sys.stderr, flush=True)
                    break
                results.append(result)
                stream.write(json.dumps(result, ensure_ascii=False) + "\n")
                stream.flush()
                os.fsync(stream.fileno())
    finally:
        failed = sum(result["status"] != "succeeded" for result in results)
        summary = {"status": "interrupted" if runner.interrupted else ("failed" if failed or fatal else "succeeded"),
                   "total": len(cases), "executed": attempted,
                   "recorded_and_restored": sum(result["workspace_restore_status"] == "complete" for result in results),
                   "succeeded": len(results) - failed, "failed": failed,
                   "not_run": len(cases) - attempted, "fatal": fatal, "signal": runner.interrupted, "finished_at": now()}
        write_json(records / "summary.json", summary)
        print(f"[benchmark] summary: {json.dumps(summary, ensure_ascii=False)}", flush=True)
    return 128 + runner.interrupted if runner.interrupted else (1 if failed or fatal else 0)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError) as error:
        print(f"[benchmark] ERROR: {error}", file=sys.stderr)
        raise SystemExit(1) from error
