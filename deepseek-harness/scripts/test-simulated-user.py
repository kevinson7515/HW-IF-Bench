"""Real source headless dialogue checks with loopback model endpoints only."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import tempfile
import threading
import unittest
import importlib.util
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import patch

from dsh_simulated_user import simulated_user_patch

ROOT = Path(__file__).resolve().parents[1]


class SimulatedUserTests(unittest.TestCase):
    def test_disabled_and_invalid_configuration(self) -> None:
        with tempfile.TemporaryDirectory() as temporary, patch.dict(os.environ, {"DSH_SIM_USER": "0"}):
            self.assertEqual(simulated_user_patch(ROOT, Path(temporary)), [])
            with patch.dict(os.environ, {"DSH_SIM_USER": "bad"}):
                with self.assertRaisesRegex(ValueError, "0 or 1"):
                    simulated_user_patch(ROOT, Path(temporary))
            with patch.dict(os.environ, {"DSH_SIM_USER": "1", "DSH_SIM_USER_API_KEY": ""}):
                with self.assertRaisesRegex(ValueError, "API_KEY"):
                    simulated_user_patch(ROOT, Path(temporary))
            invalid_config = Path(temporary) / "invalid.json"
            invalid_config.write_text('{"apiKey": "must-not-be-in-config"}', encoding="utf-8")
            with patch.dict(os.environ, {"DSH_SIM_USER": "1", "DSH_SIM_USER_API_KEY": "fixture", "DSH_SIM_USER_CONFIG": str(invalid_config)}):
                with self.assertRaisesRegex(ValueError, "configuration fields"):
                    simulated_user_patch(ROOT, Path(temporary))

    @unittest.skipUnless(os.environ.get("DSH_BENCHMARK_TEST_NODE"), "set DSH_BENCHMARK_TEST_NODE for the source deployment test")
    def test_tool_answer_then_plain_question_ends_without_continuation(self) -> None:
        self.exercise()

    @unittest.skipUnless(os.environ.get("DSH_BENCHMARK_TEST_NODE"), "set DSH_BENCHMARK_TEST_NODE for the source deployment test")
    def test_plain_question_never_calls_simulator(self) -> None:
        self.exercise(plain_only=True)

    @unittest.skipUnless(os.environ.get("DSH_BENCHMARK_TEST_NODE"), "set DSH_BENCHMARK_TEST_NODE for the source deployment test")
    def test_budget_exhaustion_is_not_a_completed_turn(self) -> None:
        self.exercise(max_replies=1)

    @unittest.skipUnless(os.environ.get("DSH_BENCHMARK_TEST_NODE"), "set DSH_BENCHMARK_TEST_NODE for the source deployment test")
    def test_provider_failure_stops_before_another_agent_request(self) -> None:
        self.exercise(fail="http")

    @unittest.skipUnless(os.environ.get("DSH_BENCHMARK_TEST_NODE"), "set DSH_BENCHMARK_TEST_NODE for the source deployment test")
    def test_invalid_answer_ids_stop_the_turn(self) -> None:
        self.exercise(fail="ids")

    @unittest.skipUnless(os.environ.get("DSH_BENCHMARK_TEST_NODE"), "set DSH_BENCHMARK_TEST_NODE for the source deployment test")
    def test_truncated_provider_output_stops_the_turn(self) -> None:
        self.exercise(fail="length")

    @unittest.skipUnless(os.environ.get("DSH_BENCHMARK_TEST_NODE"), "set DSH_BENCHMARK_TEST_NODE for the source deployment test")
    def test_invalid_question_text_is_audited_without_coercion(self) -> None:
        self.exercise(fail="question-fields")

    @unittest.skipUnless(os.environ.get("DSH_BENCHMARK_TEST_NODE"), "set DSH_BENCHMARK_TEST_NODE for the source deployment test")
    def test_offered_choice_is_preserved_in_native_tool_result(self) -> None:
        self.exercise(choices=True)

    @unittest.skipUnless(os.environ.get("DSH_BENCHMARK_TEST_NODE"), "set DSH_BENCHMARK_TEST_NODE for the source deployment test")
    def test_unoffered_choice_stops_the_turn(self) -> None:
        self.exercise(fail="choice", choices=True)

    def exercise(self, max_replies: int = 4, fail: str | None = None, plain_only: bool = False, choices: bool = False) -> None:
        agent_requests = []
        sim_requests = []

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_args: object) -> None:
                pass

            def do_POST(self) -> None:
                request = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                if self.path == "/sim/chat/completions":
                    sim_requests.append(request)
                    payload = json.loads(request["messages"][1]["content"])
                    mode = payload["mode"]
                    value = {"answers": [{"id": "status", "custom": "虚拟设定：使用 120 分钟培训。", "selected": []}], "unknown": False, "synthetic": True}
                    if choices:
                        value["answers"][0]["selected"] = ["90 分钟" if fail == "choice" else "120 分钟"]
                    if fail == "ids" and mode == "questions":
                        value["answers"][0]["id"] = "unexpected-id"
                    if fail == "question-fields":
                        value = {"answers": [{"id": "status", "custom": None, "selected": []}], "unknown": False, "synthetic": True, "debug": "sim-secret-not-for-agent"}
                    completion = {"choices": [{"finish_reason": "length" if fail == "length" else "stop", "message": {"content": json.dumps(value, ensure_ascii=False)}}], "usage": {"total_tokens": 30}}
                    body = json.dumps(completion).encode()
                    self.send_response(401 if fail == "http" else 200)
                    self.send_header("Content-Type", "application/json")
                else:
                    agent_requests.append(request)
                    if not plain_only and (len(agent_requests) == 1 or max_replies == 1):
                        question = {"id": "status", "question": "请选择培训时长。"}
                        if choices:
                            question["options"] = [{"label": "60 分钟"}, {"label": "120 分钟"}]
                        delta = {"role": "assistant", "tool_calls": [{"index": 0, "id": "ask-" + str(len(agent_requests)), "type": "function", "function": {
                            "name": "ask_user_question", "arguments": json.dumps({"questions": [question]})}}]}
                        finish = "tool_calls"
                    else:
                        delta = {"role": "assistant", "content": "数据漫游开启了吗？" if len(agent_requests) == 2 else "无法确认设备状态；本次无法验证网络恢复。"}
                        finish = "stop"
                    chunks = [{"choices": [{"index": 0, "delta": delta, "finish_reason": None}]},
                              {"choices": [{"index": 0, "delta": {}, "finish_reason": finish}]}]
                    body = ("".join("data: " + json.dumps(chunk) + "\n\n" for chunk in chunks) + "data: [DONE]\n\n").encode()
                    self.send_response(200)
                    self.send_header("Content-Type", "text/event-stream")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        try:
            with tempfile.TemporaryDirectory() as temporary:
                folder = Path(temporary)
                task = folder / "task.json"
                task.write_text(json.dumps({"user_query": "我在法国，手机无服务。不更换套餐。", "rubric": "HIDDEN_DO_NOT_SEND", "effective_system_prompt": "HIDDEN_DO_NOT_SEND"}), encoding="utf-8")
                config = folder / "sim.json"
                config.write_text(json.dumps({"baseURL": f"http://127.0.0.1:{server.server_port}/sim", "maxReplies": max_replies}), encoding="utf-8")
                provider = folder / "provider.json"
                provider.write_text(json.dumps([
                    {"id": "llm-deepseek", "disabled": True}, {"id": "session-title-llm", "disabled": True},
                    {"id": "llm-pi-ai", "config": {"providers": {"fixture": {"api": "openai-completions", "baseURL": f"http://127.0.0.1:{server.server_port}/v1", "apiKeyEnv": "DSH_FIXTURE_KEY", "models": [{"id": "fixture", "contextWindow": 32768, "maxTokens": 1024}]}}}},
                    {"id": "agent-default-model", "config": {"provider": "fixture", "model": "fixture"}},
                    {"id": "session-persistence-jsonl", "config": {"root": str(folder / "home/sessions"), "compression": "none"}},
                ]), encoding="utf-8")
                environment = {**os.environ, "DSH_SIM_USER": "1", "DSH_SIM_USER_API_KEY": "sim-secret-not-for-agent", "DSH_SIM_USER_CONFIG": str(config),
                               "DSH_E2B_TASK_FILE": str(task), "DSH_FIXTURE_KEY": "agent-key", "DSH_HOME": str(folder / "home"),
                               "DSH_TELEMETRY_DISABLED": "1", "DSH_TOOLS_MODE": "native", "NO_PROXY": "localhost,127.0.0.1",
                               "TSX_TSCONFIG_PATH": str(ROOT / "tsconfig.base.json")}
                with patch.dict(os.environ, environment):
                    overlays = simulated_user_patch(ROOT, folder)
                command = [os.environ["DSH_BENCHMARK_TEST_NODE"], "--import", (ROOT / "node_modules/tsx/dist/esm/index.mjs").as_uri(),
                           str(ROOT / "apps/cli/src/bin.ts"), "--profile", "headless", "--patch", str(provider), "--patch", str(overlays[0]), "--json", "请排查我的手机。"]
                # Source launch exercises the out-of-tree deployment plugin's TS imports.
                process = subprocess.Popen(command, cwd=folder, env=environment, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                try:
                    stdout, stderr = process.communicate(timeout=90)
                finally:
                    if process.poll() is None:
                        process.kill()
                        process.wait()
                events = [json.loads(line) for line in stdout.decode().splitlines() if line.startswith("{")]
                reasons = [event["reason"]["kind"] for event in events if event.get("phase") == "turn_end"]
                audit_file = folder / "simulated-user.jsonl"
                self.assertTrue(audit_file.exists(), stderr.decode(errors="replace"))
                audit = audit_file.read_text(encoding="utf-8")
                self.assertNotIn("sim-secret-not-for-agent", audit)
                self.assertNotIn("HIDDEN_DO_NOT_SEND", json.dumps(sim_requests))
                self.assertNotIn("sim-secret-not-for-agent", json.dumps(agent_requests))
                for simulated in sim_requests:
                    response_format = simulated["response_format"]
                    self.assertEqual(response_format["type"], "json_schema")
                    self.assertTrue(response_format["json_schema"]["strict"])
                    schema = response_format["json_schema"]["schema"]
                    mode = json.loads(simulated["messages"][1]["content"])["mode"]
                    self.assertEqual(mode, "questions")
                    self.assertEqual(set(schema["required"]), {"answers", "unknown", "synthetic"})
                    self.assertFalse(schema["additionalProperties"])
                    self.assertNotIn("For mode=", simulated["messages"][0]["content"])
                if fail or max_replies == 1:
                    self.assertNotEqual(process.returncode, 0, stdout.decode() + stderr.decode())
                    self.assertIn("error", reasons)
                    self.assertLessEqual(len(agent_requests), 2)
                    self.assertIn('"type":"error"', audit.replace(" ", ""))
                    if fail == "question-fields":
                        records = [json.loads(line) for line in audit.splitlines()]
                        invalid = [record for record in records if record.get("type") == "provider_response"][-1]
                        self.assertIsNone(invalid["value"]["answers"][0]["custom"])
                        self.assertEqual(invalid["value"]["debug"], "[REDACTED]")
                        self.assertIn("answer ids or text are invalid", records[-1]["reason"])
                else:
                    self.assertEqual(process.returncode, 0, stderr.decode(errors="replace"))
                    self.assertEqual(reasons, ["completed"])
                    self.assertEqual(len(agent_requests), 1 if plain_only else 2)
                    self.assertEqual(len(sim_requests), 0 if plain_only else 1)
                    self.assertTrue(any(tool["function"]["name"] == "ask_user_question" for tool in agent_requests[0]["tools"]))
                    tool = next(tool["function"] for tool in agent_requests[0]["tools"] if tool["function"]["name"] == "ask_user_question")
                    self.assertEqual(tool["description"], "Ask the user a concise question when you need confirmation, a choice, or missing information before proceeding.")
                    self.assertNotIn("You simulate the user", json.dumps(agent_requests))
                    if not plain_only:
                        self.assertTrue(any(message["role"] == "tool" and "虚拟设定" in json.dumps(message, ensure_ascii=False) for message in agent_requests[1]["messages"]))
                        records = [json.loads(line) for line in audit.splitlines()]
                        answer = next(record for record in records if record["type"] == "response")
                        self.assertTrue(answer["synthetic"])
                        self.assertIn("含虚构设定", answer["reply"]["answers"][0]["custom"])
                        self.assertEqual(answer["reply"]["answers"][0]["selected"], ["120 分钟"] if choices else [])
                    self.assertFalse(any(event["type"] == "simulated_user" for event in events))
                    sessions = list((folder / "home/sessions").rglob("session.v4.jsonl"))
                    self.assertEqual(len(sessions), 1)
                    saved = sessions[0].read_text(encoding="utf-8")
                    self.assertNotIn('"kind":"simulated-user"', saved.replace(" ", ""))
                    if not plain_only:
                        self.assertIn("非真人授权", saved)
                    self.assertNotIn("sim-secret-not-for-agent", saved)
                    trace_file = folder / "trace.jsonl"
                    trace_file.write_bytes(stdout)
                    spec = importlib.util.spec_from_file_location("sim_benchmark", ROOT / "scripts/run-benchmark.py")
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    info, projected = module.read_trace(trace_file, "unchanged system", "original user")
                    self.assertEqual(info["tool_calls"], 0 if plain_only else 1)
                    self.assertEqual(info["steps"], 1 if plain_only else 2)
                    simulated = [message for message in projected["trace"] if message.get("simulated")]
                    self.assertEqual(len(simulated), 0)
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


if __name__ == "__main__":
    unittest.main()
