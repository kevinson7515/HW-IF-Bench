"""Offline checks for the company-vision MCP adapter used by Pangu batches."""

from __future__ import annotations

import base64
import importlib.util
import json
import os
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError


def load_adapter() -> types.ModuleType:
    script = Path(__file__).with_name("dsh-vision-mcp.py")
    spec = importlib.util.spec_from_file_location("dsh_vision_test", script)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeResponse:
    def __init__(self, body: object) -> None:
        self.body = json.dumps(body).encode()

    def __enter__(self) -> FakeResponse:
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def read(self, _limit: int) -> bytes:
        return self.body


class VisionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name)
        self.image = self.root / "chart.png"
        self.image.write_bytes(b"\x89PNG\r\n\x1a\nchart")
        env_patch = patch.dict(os.environ, {
            "DSH_BATCH_REPO_ROOT": str(self.root),
            "COMPANY_DEEPSEEK_API_KEY": "test-secret",
            "COMPANY_DEEPSEEK_BASE_URL": "http://gateway.test/v1",
            "DSH_VISION_MODEL": "deepseek-v4-pro",
            "DSH_VISION_TIMEOUT_SECONDS": "12",
            "DSH_VISION_MAX_TOKENS": "256",
            "DSH_VISION_MAX_IMAGE_BYTES": "1024",
        })
        env_patch.start()
        self.addCleanup(env_patch.stop)
        self.adapter = load_adapter()

    def call(self, image_path: str, question: str = "Are labels clipped?") -> dict[str, object]:
        response = self.adapter.handle({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": "inspect_image", "arguments": {"image_path": image_path, "question": question}},
        })
        assert response is not None
        return response["result"]

    def test_send_image_to_company_route_and_return_only_observation(self) -> None:
        sent: list[object] = []

        def respond(request: object, *, timeout: int) -> FakeResponse:
            sent.append((request, timeout))
            return FakeResponse({"choices": [{"message": {"content": "The x-axis labels are visible."}}]})

        with patch.object(self.adapter, "urlopen", side_effect=respond):
            result = self.call("chart.png")
        self.assertFalse(result["isError"])
        self.assertEqual(result["structuredContent"]["observation"], "The x-axis labels are visible.")
        request, timeout = sent[0]
        self.assertEqual(timeout, 12)
        self.assertEqual(request.full_url, "http://gateway.test/v1/chat/completions")
        self.assertEqual(request.get_header("Authorization"), "Bearer test-secret")
        payload = json.loads(request.data)
        self.assertEqual(payload["model"], "deepseek-v4-pro")
        self.assertEqual(payload["max_tokens"], 256)
        self.assertEqual(payload["messages"][1]["content"][0]["text"], "Are labels clipped?")
        image_url = payload["messages"][1]["content"][1]["image_url"]["url"]
        self.assertEqual(base64.b64decode(image_url.split(",", 1)[1]), self.image.read_bytes())
        self.assertNotIn("test-secret", json.dumps(result))

    def test_absolute_export_path_is_accepted(self) -> None:
        with patch.object(self.adapter, "urlopen", return_value=FakeResponse({
            "choices": [{"message": {"content": "Chart visible."}}],
        })):
            self.assertFalse(self.call(str(self.image))["isError"])

    def test_reject_outside_hidden_invalid_and_oversized_images_before_request(self) -> None:
        outside = self.root.parent / "outside.png"
        hidden = self.root / ".secret.png"
        hidden.write_bytes(self.image.read_bytes())
        invalid = self.root / "invalid.png"
        invalid.write_bytes(b"not an image")
        oversized = self.root / "large.png"
        oversized.write_bytes(b"\x89PNG\r\n\x1a\n" + b"x" * 1024)
        with patch.object(self.adapter, "urlopen") as send:
            for path in (str(outside), ".secret.png", "invalid.png", "large.png"):
                with self.subTest(path=path):
                    self.assertTrue(self.call(path)["isError"])
            send.assert_not_called()

    def test_http_rejection_is_not_reported_as_a_visual_observation(self) -> None:
        body = b'{"error":{"message":"model does not accept image; token test-secret"}}'
        failure = HTTPError("http://gateway.test/v1/chat/completions", 400, "Bad Request", {}, None)
        failure.fp = __import__("io").BytesIO(body)
        with patch.object(self.adapter, "urlopen", side_effect=failure):
            result = self.call("chart.png")
        self.assertTrue(result["isError"])
        self.assertIn("HTTP 400", result["content"][0]["text"])
        self.assertNotIn("test-secret", json.dumps(result))

    def test_empty_model_content_and_invalid_arguments_fail(self) -> None:
        with patch.object(self.adapter, "urlopen", return_value=FakeResponse({
            "choices": [{"message": {"content": ""}}],
        })):
            self.assertTrue(self.call("chart.png")["isError"])
        rejected = self.adapter.handle({
            "jsonrpc": "2.0", "id": 1, "method": "tools/call",
            "params": {"name": "inspect_image", "arguments": {"image_path": "chart.png"}},
        })
        self.assertEqual(rejected["error"]["code"], -32602)


if __name__ == "__main__":
    unittest.main()
