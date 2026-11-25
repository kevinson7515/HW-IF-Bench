"""Unit & integration tests for the Workflow Seed Library pipeline."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from seed_pipeline.llm_enhancer import LLMEnhancer
from seed_pipeline.profiler import build_task_profile, load_arbitrary_jsonl_tasks, load_unified_benchmark_tasks
from seed_pipeline.scheduler import load_seed_library, run_seed_pipeline
from seed_pipeline.verifiers import evaluate_seed_rule


def _mk_evidence(calls, turns=None, thinking=None, final_answer="", artifacts=None, user_query=""):
    if turns is None:
        turns = [
            {
                "turn_index": i,
                "thinking": "Reasoning step " + "x" * 60,
                "thinking_len": 75,
                "tool_calls": [c],
                "parallel_count": 1,
                "content": "",
            }
            for i, c in enumerate(calls)
        ]
    if thinking is None:
        thinking = [{"turn_index": t["turn_index"], "text": t["thinking"], "length": t["thinking_len"]} for t in turns]
    return {
        "has_real_trace": True,
        "user_query": user_query,
        "final_answer": final_answer,
        "artifacts": artifacts or [],
        "trace": {"calls": calls, "turns": turns, "thinking": thinking},
    }


class TestSeedVerifiers(unittest.TestCase):
    def test_stage_chain_first_occurrence_allows_backtracking(self):
        rule = {
            "path": "trace.calls",
            "op": "workflow_stage_chain",
            "value": {
                "stages": [["task_planning"], ["file_glob", "file_search"], ["file_read"], ["python_exec"]],
                "require_first_call_in_stage0": True,
            },
        }
        # Trace with normal error backtracking (python_exec -> file_read -> python_exec) MUST PASS
        ev_pass = _mk_evidence(
            [
                {"name": "task_planning", "args": {}, "output": ""},
                {"name": "file_glob", "args": {}, "output": ""},
                {"name": "file_read", "args": {}, "output": ""},
                {"name": "python_exec", "args": {}, "output": "Error", "is_error": True},
                {"name": "file_read", "args": {}, "output": ""},
                {"name": "python_exec", "args": {}, "output": "OK"},
            ]
        )
        self.assertTrue(evaluate_seed_rule(rule, ev_pass))

        # Out of order at start MUST FAIL
        ev_fail = _mk_evidence(
            [
                {"name": "file_read", "args": {}, "output": ""},
                {"name": "task_planning", "args": {}, "output": ""},
                {"name": "file_glob", "args": {}, "output": ""},
                {"name": "python_exec", "args": {}, "output": ""},
            ]
        )
        self.assertFalse(evaluate_seed_rule(rule, ev_fail))

    def test_source_before_fetch(self):
        rule = {"path": "trace.events", "op": "source_before_fetch", "value": True}
        ev_ok = _mk_evidence(
            [
                {"name": "web_search", "args": {"q": "nhl"}, "output": "Result: https://api-web.nhle.com/v1/standings"},
                {"name": "web_fetch", "args": {"url": "https://api-web.nhle.com/v1/standings"}, "output": "ok"},
            ]
        )
        self.assertTrue(evaluate_seed_rule(rule, ev_ok))

        ev_guessed = _mk_evidence(
            [
                {"name": "web_search", "args": {"q": "nhl"}, "output": "Result: https://example.com/a"},
                {"name": "web_fetch", "args": {"url": "https://hockey-reference.com/guessed"}, "output": "403"},
            ]
        )
        self.assertFalse(evaluate_seed_rule(rule, ev_guessed))

    def test_max_parallel_calls_blocks_subagent_bypass(self):
        rule = {
            "path": "trace.turns",
            "op": "max_parallel_calls",
            "value": {"max_parallel": 1, "forbid_subagent_bypass": True},
        }
        ev_ok = _mk_evidence([{"name": "web_search", "args": {}}, {"name": "web_fetch", "args": {}}])
        self.assertTrue(evaluate_seed_rule(rule, ev_ok))

        ev_subagent = _mk_evidence([{"name": "subagent", "args": {}}, {"name": "web_fetch", "args": {}}])
        self.assertFalse(evaluate_seed_rule(rule, ev_subagent))

        ev_par = _mk_evidence(
            [{"name": "file_read", "args": {}}, {"name": "file_read", "args": {}}],
            turns=[{"turn_index": 0, "thinking": "abc" * 30, "thinking_len": 90, "tool_calls": [{}, {}], "parallel_count": 2, "content": ""}],
        )
        self.assertFalse(evaluate_seed_rule(rule, ev_par))

    def test_thinking_controls(self):
        # step_thinking_required
        rule_step = {"path": "trace.turns", "op": "step_thinking_required", "value": {"min_chars": 50}}
        ev_zero = _mk_evidence(
            [{"name": "file_read", "args": {}}],
            turns=[{"turn_index": 0, "thinking": "", "thinking_len": 0, "tool_calls": [{}], "parallel_count": 1, "content": ""}],
        )
        self.assertFalse(evaluate_seed_rule(rule_step, ev_zero))

        # thinking_language
        rule_zh = {"path": "trace.thinking", "op": "thinking_language", "value": {"language": "zh", "min_ratio": 0.7}}
        ev_en = _mk_evidence([], turns=[], thinking=[{"turn_index": 0, "text": "The user wants a travel plan for Guangzhou.", "length": 43}])
        ev_zh = _mk_evidence([], turns=[], thinking=[{"turn_index": 0, "text": "用户需要一份武汉到广州的三天火车旅游规划，我要先读取车次和酒店表格。", "length": 34}])
        self.assertFalse(evaluate_seed_rule(rule_zh, ev_en))
        self.assertTrue(evaluate_seed_rule(rule_zh, ev_zh))

        # thinking_pre_final_verify
        rule_sc = {"path": "trace.thinking", "op": "thinking_pre_final_verify", "value": {"marker": "[SELF_CHECK]"}}
        ev_sc = _mk_evidence([], turns=[], thinking=[{"turn_index": 0, "text": "[SELF_CHECK] Checked budget <= 5000.", "length": 36}])
        self.assertTrue(evaluate_seed_rule(rule_sc, ev_sc))

    def test_error_branch_protocol(self):
        rule = {
            "path": "trace",
            "op": "error_branch_protocol",
            "value": {
                "error_heading": "## 异常与替代路径",
                "normal_heading": "## 正常核验记录",
                "error_thinking_marker": "[ERROR_ANALYSIS]",
            },
        }
        ev_err_ok = _mk_evidence(
            [{"name": "web_fetch", "args": {}, "output": "HTTP 403", "is_error": True}],
            thinking=[{"turn_index": 0, "text": "[ERROR_ANALYSIS] Hit 403, switching source.", "length": 44}],
            final_answer="## 异常与替代路径\n切换了官网接口。",
        )
        self.assertTrue(evaluate_seed_rule(rule, ev_err_ok))
        ev_ok_branch = _mk_evidence(
            [{"name": "web_fetch", "args": {}, "output": "200 OK", "is_error": False}],
            final_answer="## 正常核验记录\n全部拉取成功。",
        )
        self.assertTrue(evaluate_seed_rule(rule, ev_ok_branch))

    def test_arbitrary_unseen_query_cold_start(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "unseen.jsonl"
            p.write_text(
                json.dumps(
                    {
                        "id": 999,
                        "user_query": "帮我调研 2026 年主流开源向量数据库 Milvus、Qdrant、Weaviate 的最新性能基准和内存占用，按 1000 万条 768 维向量场景给一个选型建议。",
                    },
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )
            tasks = load_arbitrary_jsonl_tasks(p)
            llm = LLMEnhancer(enabled=False)
            profiles = [build_task_profile(t, t["baseline_evidence"], llm) for t in tasks]
            self.assertTrue(profiles[0]["semantic_flags"]["needs_web_info"])
            self.assertTrue(profiles[0]["semantic_flags"]["needs_computation"])
            self.assertFalse(profiles[0]["semantic_flags"]["needs_local_files"])
            groups, stats = run_seed_pipeline(tasks, profiles, load_seed_library(), llm)
            self.assertEqual(len(groups), 1)
            self.assertEqual(len(groups[0]["variants"]), 6)
            self.assertEqual(stats["total_variants"], 6)


class TestFull98OfflinePipeline(unittest.TestCase):
    def test_full_98_tasks_anti_default_and_diversity(self):
        tasks = load_unified_benchmark_tasks(REPO_ROOT, split="all98")
        self.assertEqual(len(tasks), 98)
        llm = LLMEnhancer(enabled=False)
        profiles = [build_task_profile(t, t["baseline_evidence"], llm) for t in tasks]
        groups, stats = run_seed_pipeline(tasks, profiles, load_seed_library(), llm)

        self.assertEqual(stats["tasks_count"], 98)
        self.assertEqual(stats["total_variants"], 588)
        # Every single variant must be verified anti-default on real/fallback baseline!
        self.assertEqual(stats["anti_default_verified_variants"], 588)
        # All 4 chain lengths L=2,3,4,5 must be present!
        for L in ("2", "3", "4", "5"):
            self.assertGreater(stats["tier_a_chain_length_counts"].get(L, 0), 0, f"Missing chain length L={L}")
        # All 4 process primitives must be present!
        for pt in ("chain", "invariant", "cadence", "conditional"):
            self.assertGreater(stats["tier_a_primitive_counts"].get(pt, 0), 0, f"Missing primitive {pt}")
        # Process/workflow variants must be the clear majority (>55%)!
        self.assertGreaterEqual(stats["process_workflow_variant_share"], 0.55)
        # V1_old50 and V2_naq48 must BOTH have balanced thinking & cadence/conditional slices!
        sb = stats["split_tier_a_primitive_counts"]
        self.assertGreaterEqual(sb["V1_old50"].get("thinking", 0), 15)
        self.assertGreaterEqual(sb["V2_naq48"].get("thinking", 0), 15)
        self.assertGreaterEqual(sb["V1_old50"].get("cadence", 0), 10)
        self.assertGreaterEqual(sb["V2_naq48"].get("cadence", 0), 10)


if __name__ == "__main__":
    unittest.main()

