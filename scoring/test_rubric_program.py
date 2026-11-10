import json
import tempfile
import unittest
from pathlib import Path
from rubric_program import evaluate_rule, recorded_calls


class RubricRuleTests(unittest.TestCase):
    def test_rule_uses_full_recorded_calls_and_aliases(self):
        with tempfile.TemporaryDirectory() as name:
            folder = Path(name)
            events = [
                {"type": "tool_call", "tool": "read", "input": {"file_path": "a.py"}},
                {"type": "tool_call", "tool": "web_fetch", "input": {"url": "https://example.com"}},
            ]
            (folder / "trace.jsonl").write_text("\n".join(json.dumps(x) for x in events), encoding="utf8")
            row = {"recording_status": "complete", "final_event_seen": True,
                   "parse_errors": [], "tool_calls": 2}
            calls = recorded_calls(folder, row)
            self.assertEqual([c["name"] for c in calls], ["file_read", "web_fetch"])
            rule = {"all": [{"path": "trace.calls.*.name", "op": "count_eq", "value": 0, "match": "web_fetch"},
                            {"path": "trace.calls.0.name", "op": "eq", "value": "file_read"}]}
            self.assertFalse(evaluate_rule(rule, "done", calls, []))
            self.assertIsNone(evaluate_rule(rule, "done", None, []))
            self.assertIsNone(recorded_calls(folder, {**row, "tool_calls": 3}))

    def test_rules_do_not_invent_artifact_or_source_evidence(self):
        rule = {"path": "artifacts.*.path", "op": "all_prefix", "value": "output/"}
        self.assertIsNone(evaluate_rule(rule, "done", [], []))
        self.assertTrue(evaluate_rule(rule, "done", [], ["output/chart.png"]))
        self.assertFalse(evaluate_rule(rule, "done", [], ["other/chart.png"]))
        source = {"path": "trace", "op": "sources_allowed",
                  "value": {"domains": ["github.com"], "keywords": ["GitHub"]}}
        self.assertFalse(evaluate_rule(source, "done", [{"name": "web_search", "args": {"q": "GitHub docs"}}], []))
        self.assertTrue(evaluate_rule(source, "done", [{"name": "web_search", "args": {"q": "-site:github.com docs"}}], []))
        self.assertIsNone(evaluate_rule(source, "done", None, []))

    def test_composite_unknown_stays_unknown(self):
        rule = {"any": [{"path": "final_answer", "op": "eq", "value": "yes"},
                        {"path": "final_answer", "op": "unsupported", "value": "no"}]}
        self.assertIsNone(evaluate_rule(rule, "yes", [], []))


if __name__ == "__main__":
    unittest.main()
