"""Offline preflight tests for JSONL batches and task attachments."""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("check_user_queries", Path(__file__).with_name("check-user-queries.py"))
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class UserQueryTests(unittest.TestCase):
    @unittest.skipUnless(os.environ.get("DSH_TEST_BASH"), "set DSH_TEST_BASH for the batch wrapper check")
    def test_wrapper_forwards_jsonl_and_enables_simulation_without_starting_models(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "run.sh").write_text('printf "%s\\n" "$1" "$DSH_BATCH_MODE" "$DSH_SIM_USER" "$DSH_QUERY_CHECK" "$DSH_EXPECTED_TASKS" "$DSH_BATCH_ID"\n', encoding="utf-8", newline="\n")
            environment = {**os.environ, "DSH_REPO_ROOT": root.as_posix(), "SLURM_JOB_ID": "fixture123", "DSH_EXPECTED_TASKS": "70", "DSH_BATCH_ID": "user_query_70-fixture123"}
            wrapper = Path(__file__).resolve().parents[1] / "run_70.sh"
            result = subprocess.run([os.environ["DSH_TEST_BASH"], str(wrapper)], env=environment, capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.splitlines(), [root.as_posix() + "/user_query_70.jsonl", "queries", "1", "1", "70", "user_query_70-fixture123"])

    def test_valid_batch_counts_regular_and_empty_placeholder_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "inputs").mkdir()
            (root / "inputs/.keep").write_bytes(b"")
            (root / "inputs/a.txt").write_text("data", encoding="utf-8")
            path = root / "queries.jsonl"
            path.write_text(json.dumps({"id": 1, "user_query": "help", "attached_files": ["inputs/.keep", "inputs/a.txt"]}), encoding="utf-8")
            self.assertEqual(checker.validate(path, 1), {"tasks": 1, "attachment_references": 2, "empty_keep_files": 1})
            with self.assertRaisesRegex(ValueError, "expected 70"):
                checker.validate(path, 70)

    def test_invalid_batch_is_rejected_before_any_model_runs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "queries.jsonl"
            valid = {"id": 1, "user_query": "help"}
            for records in ([valid, valid], [{"user_query": ""}], [{**valid, "attached_files": ["missing.txt"]}], [{**valid, "attached_files": "bad"}], [None], []):
                with self.subTest(records=records):
                    path.write_text("\n".join(json.dumps(record) for record in records), encoding="utf-8")
                    with self.assertRaises(ValueError):
                        checker.validate(path)


if __name__ == "__main__":
    unittest.main()
