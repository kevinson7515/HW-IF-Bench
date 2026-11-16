#!/usr/bin/env python3
"""Keep one official E2B code-interpreter sandbox alive per MCP process."""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

from dsh_e2b_environment import Environment

import certifi

os.environ["SSL_CERT_FILE"] = certifi.where()

from e2b_code_interpreter import Sandbox  # noqa: E402


SERVER_INFO = {"name": "dsh-e2b", "version": "1.0.0"}
EXECUTE_TOOL = {
    "name": "execute_python",
    "description": (
        "Execute Python in a persistent E2B cloud sandbox. Imports and variables persist "
        "between calls in this task. Files created there are not local until export_file copies them."
        " Declared attachments, including local edits, are mirrored before each call and configured dependencies are prepared first."
        " Use prepare_environment to inspect remote paths and actual installed versions."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {"code": {"type": "string", "description": "Python source to execute."}},
        "required": ["code"],
        "additionalProperties": False,
    },
}
EXPORT_TOOL = {
    "name": "export_file",
    "description": (
        "Copy a file created in this task's E2B sandbox into a new, repository-relative "
        "local path. Use this for charts or other deliverables after execute_python saves "
        "them in E2B; do not copy file bytes through the model or upload them to a public host. "
        "Existing local files cannot be overwritten. Returns only the local path, byte count, "
        "and SHA-256 digest."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "remote_path": {
                "type": "string",
                "description": "Absolute path of the existing file in the E2B sandbox.",
            },
            "local_path": {
                "type": "string",
                "description": "New path relative to the repository, such as stock-analysis/chart.png.",
            },
        },
        "required": ["remote_path", "local_path"],
        "additionalProperties": False,
    },
}
stack = contextlib.ExitStack()
sandbox: Sandbox | None = None
environment = Environment()
PREPARE_TOOL = {
    "name": "prepare_environment",
    "description": "Synchronize this task's declared attachments and prepare configured E2B dependencies. Returns remote paths, input hashes, Python and installed versions. Sparse attachments are not a full original project; this tool does not run project tests.",
    "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
}


def send(message: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(message, ensure_ascii=False, separators=(",", ":")) + "\n")
    sys.stdout.flush()


def error_response(request_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def get_sandbox() -> Sandbox:
    global sandbox
    if sandbox is None:
        if not os.environ.get("E2B_API_KEY"):
            raise RuntimeError("E2B_API_KEY is not configured")
        proxy = os.environ.get("E2B_PROXY", "")
        options: dict[str, Any] = {}
        if proxy:
            options = {"proxy": proxy, "timeout": 3600}
        if os.environ.get("DSH_E2B_TEMPLATE"):
            options["template"] = os.environ["DSH_E2B_TEMPLATE"]
        sandbox = stack.enter_context(Sandbox.create(**options))
    return sandbox


def execution_result(execution: Any, sandbox_id: str) -> dict[str, Any]:
    logs = execution.logs
    stdout = logs.stdout
    stderr = logs.stderr
    if isinstance(stdout, list):
        stdout = "".join(stdout)
    if isinstance(stderr, list):
        stderr = "".join(stderr)
    error = execution.error
    results: list[dict[str, str]] = []
    content: list[dict[str, str]] = []
    for result in execution.results:
        item: dict[str, str] = {}
        for field in ("text", "html", "svg", "markdown", "latex"):
            value = getattr(result, field, None)
            if isinstance(value, str) and value:
                item[field] = value
        for field, mime in (("png", "image/png"), ("jpeg", "image/jpeg")):
            value = getattr(result, field, None)
            if isinstance(value, str) and value:
                content.append({"type": "image", "data": value, "mimeType": mime})
                item[field] = f"{mime} returned as an MCP image block"
        results.append(item or {"text": str(result)})
    output = {
        "sandbox_id": sandbox_id,
        "stdout": stdout,
        "stderr": stderr,
        "error": str(error) if error is not None else None,
        "results": results,
    }
    content.insert(0, {"type": "text", "text": json.dumps(output, ensure_ascii=False)})
    return {"content": content, "structuredContent": output, "isError": error is not None}


def export_file(active_sandbox: Sandbox, remote_path: str, local_path: str) -> dict[str, Any]:
    root_value = os.environ.get("DSH_E2B_EXPORT_ROOT")
    if not root_value:
        raise ValueError("DSH_E2B_EXPORT_ROOT is not configured")
    root = Path(root_value).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("DSH_E2B_EXPORT_ROOT is not a directory")
    limit_value = os.environ.get("DSH_E2B_MAX_EXPORT_BYTES")
    if not limit_value or not limit_value.isdecimal() or int(limit_value) < 1:
        raise ValueError("DSH_E2B_MAX_EXPORT_BYTES must be a positive integer")
    limit = int(limit_value)
    parts = local_path.split("/")
    if (
        not local_path
        or local_path.startswith("/")
        or "\\" in local_path
        or "\x00" in local_path
        or any(part in ("", ".", "..") for part in parts)
        or any(part.startswith(".") or part == "node_modules" for part in parts)
        or ":" in parts[0]
    ):
        raise ValueError("local_path must be a repository-relative deliverable path without hidden, dependency, empty, or parent segments")

    parent = root
    for part in parts[:-1]:
        parent = parent / part
        if parent.is_symlink():
            raise ValueError("local_path may not traverse a symbolic link")
        parent.mkdir(mode=0o700, exist_ok=True)
        if not parent.is_dir() or not parent.resolve().is_relative_to(root):
            raise ValueError("local_path must remain inside the repository")
    destination = parent / parts[-1]
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f"local file already exists: {local_path}")

    temporary_path: Path | None = None
    digest = hashlib.sha256()
    size = 0
    try:
        descriptor, temporary_name = tempfile.mkstemp(prefix=".dsh-e2b-", dir=parent)
        temporary_path = Path(temporary_name)
        with os.fdopen(descriptor, "wb") as output:
            for chunk in active_sandbox.files.read(remote_path, format="stream"):
                if not isinstance(chunk, bytes):
                    raise TypeError("E2B file stream returned a non-byte chunk")
                size += len(chunk)
                if size > limit:
                    raise ValueError(f"E2B file exceeds export limit of {limit} bytes")
                output.write(chunk)
                digest.update(chunk)
        os.link(temporary_path, destination)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)

    metadata = {
        "remote_path": remote_path,
        "local_path": str(destination),
        "bytes": size,
        "sha256": digest.hexdigest(),
    }
    return {
        "content": [{"type": "text", "text": json.dumps(metadata, ensure_ascii=False)}],
        "structuredContent": metadata,
        "isError": False,
    }


def handle(request: object) -> dict[str, Any] | None:
    if not isinstance(request, dict):
        return error_response(None, -32600, "request must be an object")
    request_id = request.get("id")
    if request_id is None:
        return None
    method = request.get("method")
    if method == "initialize":
        params = request.get("params")
        protocol_version = "2024-11-05"
        if isinstance(params, dict) and isinstance(params.get("protocolVersion"), str):
            protocol_version = params["protocolVersion"]
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": protocol_version,
                "capabilities": {"tools": {}},
                "serverInfo": SERVER_INFO,
            },
        }
    if method == "ping":
        return {"jsonrpc": "2.0", "id": request_id, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": request_id, "result": {"tools": [EXECUTE_TOOL, EXPORT_TOOL, PREPARE_TOOL]}}
    if method == "tools/call":
        params = request.get("params")
        if not isinstance(params, dict) or params.get("name") not in (EXECUTE_TOOL["name"], EXPORT_TOOL["name"], PREPARE_TOOL["name"]):
            return error_response(request_id, -32602, "unknown tool")
        arguments = params.get("arguments", {})
        if not isinstance(arguments, dict):
            return error_response(request_id, -32602, "arguments must be an object")
        name = params["name"]
        if name == EXECUTE_TOOL["name"]:
            code = arguments.get("code")
            if not isinstance(code, str) or not code.strip():
                return error_response(request_id, -32602, "code must be a non-empty string")
        elif name == EXPORT_TOOL["name"]:
            remote_path = arguments.get("remote_path")
            local_path = arguments.get("local_path")
            if not isinstance(remote_path, str) or not remote_path.startswith("/") or not remote_path.strip():
                return error_response(request_id, -32602, "remote_path must be an absolute E2B path")
            if not isinstance(local_path, str):
                return error_response(request_id, -32602, "local_path must be a string")
        try:
            active_sandbox = get_sandbox()
            prepared = environment.prepare(active_sandbox) if name != EXPORT_TOOL["name"] else None
            if name == EXECUTE_TOOL["name"]:
                execution = active_sandbox.run_code(code)
                result = execution_result(execution, active_sandbox.sandbox_id)
                result["structuredContent"]["environment"] = prepared
                result["content"][0]["text"] = json.dumps(result["structuredContent"], ensure_ascii=False)
            elif name == EXPORT_TOOL["name"]:
                result = export_file(active_sandbox, remote_path, local_path)
            else:
                result = {"content": [{"type": "text", "text": json.dumps(prepared, ensure_ascii=False)}], "structuredContent": prepared, "isError": False}
        except Exception as error:
            operation = {EXECUTE_TOOL["name"]: "execution", EXPORT_TOOL["name"]: "file export", PREPARE_TOOL["name"]: "environment preparation"}[name]
            result = {"content": [{"type": "text", "text": f"E2B {operation} failed: {error}"}], "isError": True}
        return {"jsonrpc": "2.0", "id": request_id, "result": result}
    return error_response(request_id, -32601, f"method not found: {method}")


def main() -> None:
    try:
        for raw_line in sys.stdin.buffer:
            if not raw_line.strip():
                continue
            try:
                request = json.loads(raw_line)
                response = handle(request)
            except json.JSONDecodeError:
                response = error_response(None, -32700, "invalid JSON")
            except Exception as error:
                response = error_response(None, -32603, f"internal error: {error}")
            if response is not None:
                send(response)
    finally:
        stack.close()


if __name__ == "__main__":
    main()
