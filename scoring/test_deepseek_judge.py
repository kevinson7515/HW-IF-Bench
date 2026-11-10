import json
import tempfile
import unittest
from pathlib import Path

from deepseek_judge import (build_request, parse_response, redact,
                            response_diagnostics, retryable_error)


class DeepSeekJudgeTests(unittest.TestCase):
    def test_redacts_common_api_key_forms(self):
        self.assertNotIn("secret-value", redact("api_key=secret-value"))
        self.assertNotIn("secret-value", redact("Authorization: Bearer secret-value"))

    def test_tc_json_response(self):
        item = {"group_id": "G-search-001", "variant_id": "S1", "rubric_id": "S1-TC-1", "layer": "TC"}
        response = {"id": "r1", "model": "deepseek-v4-pro", "choices": [
            {"finish_reason": "stop", "message": {"content": json.dumps({
                "verdict": "PARTIAL", "evidence": "final.txt: 有优缺点但缺来源"})}}]}
        self.assertEqual(parse_response(response, item)["verdict"], "PARTIAL")

    def test_unfinished_response_reports_finish_reason_without_guessing(self):
        item = {"layer": "TC"}
        response = {"id": "r2", "usage": {"completion_tokens": 1024}, "choices": [
            {"finish_reason": "length", "message": {"content": "{\"verdict\":"}}]}
        with self.assertRaisesRegex(ValueError, "finish_reason='length'"):
            parse_response(response, item)
        self.assertEqual(response_diagnostics(response)["finish_reason"], "length")
        self.assertTrue(retryable_error(ValueError("DeepSeek response unfinished")))

    def test_request_disables_thinking_and_uses_configured_limit(self):
        with tempfile.TemporaryDirectory() as name:
            trace = Path(name) / "trace.json"
            trace.write_text(json.dumps({"lossless": True, "trace": []}), encoding="utf-8")
            item = {"group_id": "G-search-001", "variant_id": "S1", "rubric_id": "S1-TC-1",
                    "layer": "TC", "method": "llm_judge", "trace_path": str(trace)}
            payload, reason = build_request(item, "deepseek-v4-pro", "deepseek-flash", 1000, 1000, 1, 3072)
            self.assertIsNone(reason)
            self.assertEqual(payload["thinking"], {"type": "disabled"})
            self.assertEqual(payload["max_tokens"], 3072)

    def test_se_yes_requires_cause_and_distinct_harm(self):
        item = {"group_id": "G-search-001", "variant_id": "S1", "rubric_id": "S1-SE-1", "layer": "SE"}
        response = {"choices": [{"finish_reason": "stop", "message": {"content": json.dumps({
            "verdict": "YES", "evidence": "trace:3"})}}]}
        with self.assertRaises(ValueError):
            parse_response(response, item)

    def test_kline_uses_vision_model_and_image(self):
        with tempfile.TemporaryDirectory() as name:
            folder = Path(name)
            image = folder / "chart.png"
            image.write_bytes(b"png-test-bytes")
            trace = folder / "trace.json"
            trace.write_text(json.dumps({"lossless": True, "trace": []}), encoding="utf-8")
            item = {"group_id": "G-kline-001", "variant_id": "S1", "rubric_id": "S1-TC-1",
                    "layer": "TC", "method": "llm_judge", "prompt": "grade", "final_answer": "done",
                    "trace_path": str(trace), "artifact_paths": [{"path": "chart.png", "local_path": str(image)}]}
            payload, reason = build_request(item, "deepseek-v4-pro", "deepseek-flash", 1000, 1000, 1)
            self.assertIsNone(reason)
            self.assertEqual(payload["model"], "deepseek-flash")
            self.assertEqual(payload["messages"][1]["content"][1]["type"], "image_url")

    def test_chart_review_can_use_image_when_trace_is_truncated(self):
        with tempfile.TemporaryDirectory() as name:
            folder = Path(name)
            image = folder / "chart.png"
            image.write_bytes(b"png-test-bytes")
            trace = folder / "trace.json"
            trace.write_text(json.dumps({"lossless": False, "trace": [
                {"role": "tool", "content": "x" * 200}]}), encoding="utf-8")
            item = {"group_id": "G-kline-001", "variant_id": "S2", "rubric_id": "S2-IF-1",
                    "layer": "IF", "method": "program_review", "prompt": "图表无网格线",
                    "trace_path": str(trace),
                    "artifact_paths": [{"path": "chart.png", "local_path": str(image)}]}
            payload, reason = build_request(item, "deepseek-v4-pro", "deepseek-flash", 10, 1000, 1)
            self.assertIsNone(reason)
            self.assertIn("TRACE TRUNCATED", payload["messages"][1]["content"][0]["text"])


if __name__ == "__main__":
    unittest.main()
