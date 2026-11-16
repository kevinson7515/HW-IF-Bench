"""Offline workspace checks and an opt-in real headless composition with a local model fixture."""

from __future__ import annotations

import hashlib
import contextlib
import importlib.util
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch


REPOSITORY = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("benchmark_batch", Path(__file__).with_name("run-benchmark.py"))
assert spec is not None and spec.loader is not None
batch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(batch)


class BenchmarkTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.root = self.base / "workspace"
        self.root.mkdir()
        (self.root / "parser.py").write_bytes(b"original broken parser\n")
        (self.root / "preexisting.svg").write_bytes(b"user-owned old chart\n")
        self.workspace = batch.Workspace(self.root, self.base / "baseline")

    def dataset(self) -> Path:
        prompt = "Only use this system prompt. {{literal}}\n"
        source = self.root / "benchmark.json"
        source.write_text(json.dumps([{
            "group_id": "G-code", "task_id": 3, "user_query": "Fix parser.py",
            "attached_files": ["parser.py"], "variants": [{
                "variant_id": "S1", "effective_system_prompt": prompt,
                "system_prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                "environment_override": "not executable metadata", "rubric": [{"exec": "raise Exception('must not execute')"}],
            }, {"variant_id": "S2", "effective_system_prompt": "Second system prompt"}],
        }]), encoding="utf-8")
        return source

    def test_groups_flatten_and_prompt_hash_and_metadata(self) -> None:
        cases = batch.load_cases(self.dataset(), self.root)
        self.assertEqual([case["variant_id"] for case in cases], ["S1", "S2"])
        self.assertEqual(cases[0]["resolved_attached_files"], [str(self.root / "parser.py")])
        self.assertIn("{{literal}}", cases[0]["effective_system_prompt"])
        self.assertFalse(cases[0]["environment_override_applied"])

    def test_bad_hash_and_external_attachment_are_rejected(self) -> None:
        source = self.dataset()
        data = json.loads(source.read_text(encoding="utf-8"))
        data[0]["variants"][0]["system_prompt_sha256"] = "bad"
        source.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "sha256"):
            batch.load_cases(source, self.root)
        data[0]["variants"][0].pop("system_prompt_sha256")
        (self.base / "outside.py").write_text("outside", encoding="utf-8")
        data[0]["attached_files"] = ["../outside.py"]
        source.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "inside the repository"):
            batch.load_cases(source, self.root)

    def test_check_command_rejects_bad_input_without_workspace_writes(self) -> None:
        source = self.dataset()
        data = json.loads(source.read_text(encoding="utf-8"))
        data[0]["variants"][0]["system_prompt_sha256"] = "bad"
        source.write_text(json.dumps(data), encoding="utf-8")
        before = self.workspace.scan()
        environment = {**os.environ, "DSH_BATCH_REPO_ROOT": str(self.root)}
        result = subprocess.run([sys.executable, str(REPOSITORY / "scripts/run-benchmark.py"), "--check", str(source)], cwd=self.root, env=environment, capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 1)
        self.assertIn("sha256", result.stderr)
        self.assertTrue(batch.equivalent(before, self.workspace.scan()))

    def test_restore_modified_deleted_created_files_and_preserve_dirty_baseline(self) -> None:
        (self.root / "nested").mkdir()
        (self.root / "nested" / "original.txt").write_bytes(b"dirty user contents")
        self.workspace.snapshot()
        (self.root / "parser.py").write_bytes(b"model fixed parser")
        (self.root / "nested" / "original.txt").unlink()
        (self.root / "output").mkdir()
        (self.root / "output" / "chart.svg").write_bytes(b"new chart")
        after = self.workspace.scan()
        record = self.base / "task"
        manifest = self.workspace.archive(record, after)
        self.assertIn("nested/original.txt", manifest["deleted"])
        self.assertEqual((record / "artifacts" / "parser.py").read_bytes(), b"model fixed parser")
        reopened = batch.Workspace(self.root, self.workspace.store)
        reopened.load()
        reopened.restore(after)
        self.assertEqual((self.root / "parser.py").read_bytes(), b"original broken parser\n")
        self.assertEqual((self.root / "nested" / "original.txt").read_bytes(), b"dirty user contents")
        self.assertEqual((self.root / "preexisting.svg").read_bytes(), b"user-owned old chart\n")
        self.assertFalse((self.root / "output").exists())

    def test_restore_file_directory_type_changes(self) -> None:
        (self.root / "folder").mkdir()
        (self.root / "folder" / "item").write_bytes(b"keep")
        self.workspace.snapshot()
        (self.root / "folder" / "item").unlink()
        (self.root / "folder").rmdir()
        (self.root / "folder").write_bytes(b"replacement file")
        (self.root / "parser.py").unlink()
        (self.root / "parser.py").mkdir()
        (self.root / "parser.py" / "new").write_bytes(b"replacement directory")
        after = self.workspace.scan()
        self.workspace.archive(self.base / "task", after)
        self.workspace.restore(after)
        self.assertEqual((self.root / "folder" / "item").read_bytes(), b"keep")
        self.assertTrue((self.root / "parser.py").is_file())

    def test_symlink_replacement_does_not_touch_external_directory(self) -> None:
        outside = self.base / "outside"
        outside.mkdir()
        (outside / "keep").write_bytes(b"external")
        (self.root / "folder").mkdir()
        (self.root / "folder" / "item").write_bytes(b"original")
        self.workspace.snapshot()
        (self.root / "folder" / "item").unlink()
        (self.root / "folder").rmdir()
        try:
            (self.root / "folder").symlink_to(outside, target_is_directory=True)
        except OSError as error:
            self.skipTest(f"symlink privilege unavailable: {error}")
        after = self.workspace.scan()
        self.workspace.archive(self.base / "task", after)
        reopened = batch.Workspace(self.root, self.workspace.store)
        reopened.load()
        reopened.restore(after)
        self.assertEqual((outside / "keep").read_bytes(), b"external")
        self.assertEqual((self.root / "folder" / "item").read_bytes(), b"original")

    def test_late_change_and_corrupt_backup_stop_cleanup(self) -> None:
        self.workspace.snapshot()
        (self.root / "new").write_bytes(b"artifact")
        after = self.workspace.scan()
        self.workspace.archive(self.base / "task", after)
        (self.root / "parser.py").write_bytes(b"external edit after recording")
        with self.assertRaisesRegex(ValueError, "after recording"):
            self.workspace.restore(after)
        self.assertTrue((self.root / "new").exists())
        after = self.workspace.scan()
        (self.workspace.store / "files" / "parser.py").write_bytes(b"corrupt")
        with self.assertRaisesRegex(ValueError, "corrupt baseline"):
            self.workspace.restore(after)
        self.assertTrue((self.root / "new").exists())

    def test_archive_limit_failure_preserves_workspace(self) -> None:
        self.workspace.snapshot()
        (self.root / "big").write_bytes(b"12345")
        with patch.dict(os.environ, {"DSH_ARTIFACT_MAX_FILE_BYTES": "4"}):
            with self.assertRaisesRegex(ValueError, "size limit"):
                self.workspace.archive(self.base / "task", self.workspace.scan())
        self.assertEqual((self.root / "big").read_bytes(), b"12345")

    def runner(self) -> tuple[Any, list[dict[str, object]]]:
        cases = batch.load_cases(self.dataset(), self.root)
        records = self.base / "records"
        records.mkdir()
        runner = batch.Runner(self.root, records, self.base / "home", self.base / "pending.json", [])
        runner.workspace.snapshot()
        return runner, cases

    def simulated_execution(self, runner: Any, *, code: int = 0) -> Any:
        def execute(command: list[str], query: str, trace: Path, diagnostics: Path) -> int:
            self.assertEqual((self.root / "parser.py").read_bytes(), b"original broken parser\n")
            self.assertIn(str(self.root / "parser.py"), query)
            (self.root / "parser.py").write_bytes(b"fixed by model\n")
            (self.root / "new-chart.svg").write_bytes(b"new chart\n")
            trace.write_text(json.dumps({"type": "final", "text": "done"}) + "\n", encoding="utf-8")
            diagnostics.write_text("", encoding="utf-8")
            return code
        return execute

    def test_variants_start_with_identical_attachments_and_record_exact_prompts(self) -> None:
        runner, cases = self.runner()
        with patch.object(runner, "execute", side_effect=self.simulated_execution(runner)):
            for case in cases:
                result = runner.run_case(case)
                self.assertEqual(result["workspace_restore_status"], "complete")
                folder = runner.records / case["group_id"] / case["variant_id"]
                self.assertEqual((folder / "artifacts" / "parser.py").read_bytes(), b"fixed by model\n")
                projection = json.loads((folder / "trace.json").read_text(encoding="utf-8"))
                self.assertFalse(projection["variant_system_prompt_applied"])
                self.assertFalse(any(message["role"] == "system" for message in projection["trace"]))
                self.assertFalse((folder / "prompt.patch.json").exists())
                self.assertEqual((folder / "variant_system_prompt.txt").read_text(encoding="utf-8"), case["effective_system_prompt"])
        self.assertFalse(runner.journal.exists())
        self.assertFalse((self.root / "new-chart.svg").exists())

    def test_failed_task_is_recorded_restored_and_next_variant_can_run(self) -> None:
        runner, cases = self.runner()
        with patch.object(runner, "execute", side_effect=self.simulated_execution(runner, code=1)):
            first = runner.run_case(cases[0])
        self.assertEqual(first["status"], "failed")
        with patch.object(runner, "execute", side_effect=self.simulated_execution(runner)):
            self.assertEqual(runner.run_case(cases[1])["status"], "succeeded")

    def test_child_receives_only_the_current_task_manifest_path(self) -> None:
        runner, _cases = self.runner()
        task_dir = self.base / "child-task"
        task_dir.mkdir()
        manifest = task_dir / "task.json"
        manifest.write_text("{}\n", encoding="utf-8")
        code = "import os,json; print(json.dumps({'type':'final','text':os.environ['DSH_E2B_TASK_FILE']}))"
        trace, errors = task_dir / "trace.jsonl", task_dir / "diagnostics.log"
        with patch.dict(os.environ, {"DSH_E2B_TASK_FILE": "stale-previous-task.json"}):
            status = runner.execute([sys.executable, "-c", code], "query", trace, errors)
            self.assertEqual(os.environ["DSH_E2B_TASK_FILE"], "stale-previous-task.json")
        self.assertEqual(status, 0, errors.read_text(encoding="utf-8"))
        self.assertEqual(json.loads(trace.read_text(encoding="utf-8"))["text"], str(manifest))

    def test_recording_failure_leaves_outputs_and_recovery_journal(self) -> None:
        runner, cases = self.runner()
        with patch.object(runner, "execute", side_effect=self.simulated_execution(runner)), patch.object(runner.workspace, "archive", side_effect=OSError("archive unavailable")):
            with self.assertRaisesRegex(OSError, "archive unavailable"):
                runner.run_case(cases[0])
        self.assertTrue(runner.journal.exists())
        self.assertEqual((self.root / "parser.py").read_bytes(), b"fixed by model\n")
        with self.assertRaisesRegex(ValueError, "differs from the saved baseline"):
            runner.run_case(cases[1])

    def test_recovery_archives_interrupted_output_before_restoring(self) -> None:
        runner, cases = self.runner()
        batch.write_json(runner.records / "plan.json", {"root": str(self.root), "home": str(runner.home),
                                                       "lock_file": str(self.base / "lock"), "journal": str(runner.journal)})
        with patch.object(runner, "execute", side_effect=self.simulated_execution(runner)), patch.object(runner.workspace, "archive", side_effect=OSError("archive unavailable")):
            with self.assertRaises(OSError):
                runner.run_case(cases[0])
        # Only the platform lock is simulated; recording and restore use the real saved files.
        with patch.object(batch, "recovery_lock", return_value=contextlib.nullcontext()), patch.object(batch.Path, "cwd", return_value=self.root):
            batch.recover(runner.records)
        self.assertFalse(runner.journal.exists())
        self.assertEqual((self.root / "parser.py").read_bytes(), b"original broken parser\n")
        recovery = list(runner.records.glob("recovery-*"))
        self.assertEqual(len(recovery), 1)
        self.assertEqual((recovery[0] / "artifacts" / "parser.py").read_bytes(), b"fixed by model\n")
        self.assertTrue((recovery[0] / "trace.jsonl").exists())

    def test_linux_process_start_token_distinguishes_pid_reuse(self) -> None:
        fields = ["S", "1", "100"] + ["0"] * 16 + ["123456", "0"]
        with patch.object(batch.Path, "read_text", return_value="100 (name with spaces) " + " ".join(fields)):
            self.assertEqual(batch.process_start_ticks(100), "123456")
        with patch.object(batch.Path, "read_text", side_effect=FileNotFoundError):
            self.assertIsNone(batch.process_start_ticks(100))

    def test_interruption_records_available_output_and_restores(self) -> None:
        runner, cases = self.runner()
        runner.interrupted = signal.SIGTERM
        with patch.object(runner, "execute", side_effect=self.simulated_execution(runner, code=-15)):
            result = runner.run_case(cases[0])
        self.assertEqual(result["status"], "interrupted")
        self.assertEqual(result["workspace_restore_status"], "complete")

    def main_environment(self) -> tuple[dict[str, str], Path]:
        source = self.dataset()
        records = self.base / "records"
        records.mkdir()
        home = self.base / "home"
        home.mkdir()
        provider = self.base / "provider.json"
        tools = self.base / "tools.json"
        batch.write_json(provider, [])
        batch.write_json(tools, [])
        environment = {
            "DSH_BATCH_REPO_ROOT": str(self.root), "DSH_BATCH_INPUT_JSONL": str(source),
            "DSH_BATCH_OUTPUT_DIR": str(records), "DSH_HOME": str(home),
            "DSH_BENCHMARK_JOURNAL": str(self.base / "pending.json"), "DSH_BENCHMARK_LOCK_FILE": str(self.base / "lock"),
            "DSH_BATCH_PATCH_FILE": str(provider), "DSH_BATCH_TOOLS_PATCH_FILE": str(tools), "DSH_MODEL_PROVIDER": "pangu",
            "DSH_BENCHMARK_GROUPS": "G-code", "DSH_BENCHMARK_VARIANTS": "S1,S2",
        }
        return environment, records

    def test_main_runs_all_variants_and_writes_batch_summary(self) -> None:
        environment, records = self.main_environment()
        def execute(instance: object, *arguments: object) -> int:
            return self.simulated_execution(instance)(*arguments)
        with patch.dict(os.environ, environment), patch.object(sys, "argv", ["run-benchmark.py"]), patch.object(batch.signal, "signal"), patch.object(batch.Runner, "execute", new=execute):
            self.assertEqual(batch.main(), 0)
        summary = json.loads((records / "summary.json").read_text(encoding="utf-8"))
        self.assertEqual((summary["total"], summary["executed"], summary["succeeded"], summary["not_run"]), (2, 2, 2, 0))
        self.assertEqual(len((records / "results.jsonl").read_text(encoding="utf-8").splitlines()), 2)
        self.assertEqual((self.root / "parser.py").read_bytes(), b"original broken parser\n")
        self.assertFalse((self.root / "new-chart.svg").exists())

    def test_main_stops_after_failed_recording(self) -> None:
        environment, records = self.main_environment()
        def execute(instance: object, *arguments: object) -> int:
            return self.simulated_execution(instance)(*arguments)
        with patch.dict(os.environ, environment), patch.object(sys, "argv", ["run-benchmark.py"]), patch.object(batch.signal, "signal"), patch.object(batch.Runner, "execute", new=execute), patch.object(batch.Workspace, "archive", side_effect=OSError("recording failed")):
            self.assertEqual(batch.main(), 1)
        summary = json.loads((records / "summary.json").read_text(encoding="utf-8"))
        self.assertEqual((summary["executed"], summary["failed"], summary["not_run"], summary["recorded_and_restored"]), (1, 1, 1, 0))
        result = json.loads((records / "G-code/S1/result.json").read_text(encoding="utf-8"))
        self.assertEqual(result["recording_status"], "failed")
        self.assertEqual(result["workspace_restore_status"], "not_attempted")
        self.assertFalse((records / "G-code/S2").exists())
        self.assertTrue(Path(environment["DSH_BENCHMARK_JOURNAL"]).exists())
        self.assertEqual((self.root / "parser.py").read_bytes(), b"fixed by model\n")

    def test_cancellation_waits_for_child_exit(self) -> None:
        runner, _cases = self.runner()
        ready = self.base / "ready"
        outcome: list[int] = []
        errors: list[BaseException] = []
        command = [sys.executable, "-c", "import pathlib,sys,time; pathlib.Path(sys.argv[1]).write_text('ready'); time.sleep(120)", str(ready)]
        def execute() -> None:
            try:
                outcome.append(runner.execute(command, "", self.base / "trace", self.base / "errors"))
            except BaseException as error:
                errors.append(error)
        worker = threading.Thread(target=execute)
        def stop_worker() -> None:
            runner.stop(signal.SIGTERM, None)
            worker.join(timeout=30)
        self.addCleanup(stop_worker)
        worker.start()
        deadline = time.monotonic() + 30
        tick = threading.Event()
        while not ready.exists() and worker.is_alive() and time.monotonic() < deadline:
            tick.wait(0.02)
        self.assertTrue(ready.exists(), f"child did not signal readiness: {errors}")
        runner.stop(signal.SIGTERM, None)
        worker.join(timeout=30)
        self.assertFalse(worker.is_alive(), "child cancellation did not finish")
        self.assertEqual(errors, [])
        self.assertEqual(len(outcome), 1)
        self.assertIsNone(runner.process)

    @unittest.skipUnless(os.environ.get("DSH_BENCHMARK_TEST_BASH"), "set DSH_BENCHMARK_TEST_BASH for protected-file setup checks")
    def test_batch_setup_loads_renamed_files_and_separates_pangu_vision_credentials(self) -> None:
        work = self.base / "work"
        secrets = work / ".secrets"
        secrets.mkdir(parents=True)
        configs = work / "dsh-config"
        configs.mkdir()
        for model in ("deepseek", "glm", "pangu"):
            secret = secrets / f"{model}-api-key"
            secret.write_bytes(f"{model}-test-key\r\n".encode("utf-8"))
            secret.chmod(0o600)
            (configs / f"{model}.patch.yml").write_text("[]\n", encoding="utf-8")
        credentials = secrets / "pangu92b-api-key.yml"
        credentials.write_text(json.dumps({"api_key": "pangu92b-test-key", "hw_id": "test-hw-id", "hw_app_key": "test-app-key"}), encoding="utf-8-sig")
        credentials.chmod(0o600)
        (configs / "pangu92b.patch.yml").write_text("[]\n", encoding="utf-8")
        for filename in ("serper-api-key", "e2b-api-key"):
            secret = secrets / filename
            secret.write_bytes(f"{filename}-test-value\r\n".encode("utf-8"))
            secret.chmod(0o600)
        (self.root / "package.json").write_text("{}\n", encoding="utf-8")
        (self.root / "batch-tools.patch.yml").write_text("[]\n", encoding="utf-8")
        (self.root / "scripts/config").mkdir(parents=True)
        (self.root / "scripts/config/e2b-projects.json").write_text('{"projects": []}\n', encoding="utf-8")
        self.dataset()
        conda = self.base / "conda"
        profile = conda / "etc/profile.d"
        profile.mkdir(parents=True)
        # NTFS cannot represent the Linux key-file permission check; only that stat result is simulated.
        permission_stat = 'stat() { if [[ "$1" == -c && "$2" == %a ]]; then printf "600\\n"; else /usr/bin/stat "$@"; fi; }\n' if os.name == "nt" else ""
        (profile / "conda.sh").write_text("conda() { return 0; }\n" + permission_stat, encoding="utf-8")
        ca_file = self.base / "ca.pem"
        ca_file.write_text("test certificate placeholder\n", encoding="utf-8")
        binaries = self.base / "bin"
        binaries.mkdir()
        programs = {
            "node": 'printf "v24.21.0\\n"\n',
            "pnpm": 'if [[ "${1:-}" == --version ]]; then printf "11.28.5\\n"; fi\n',
            "flock": "exit 0\n",
            "python": 'if [[ "${1:-}" == - ]]; then exec "$DSH_TEST_PYTHON" "$@"; fi\n'
            'if [[ "${1:-}" == -c ]]; then if [[ "$2" == *certifi.where* ]]; then printf "%s\\n" "$DSH_TEST_CA_FILE"; fi; exit 0; fi\n'
            'for name in PANGU_API_KEY PANGU92B_API_KEY PANGU92B_HW_ID PANGU92B_APP_KEY COMPANY_GLM_API_KEY COMPANY_DEEPSEEK_API_KEY SERPER_API_KEY E2B_API_KEY; do '
            'if [[ "${!name:-}" == *$\'\\r\'* || "${!name:-}" == *$\'\\n\'* ]]; then printf "invalid credential newline\\n" >&2; exit 43; fi; done\n'
            'printf "%s\\n" "$DSH_MODEL_PROVIDER" "$DSH_BATCH_PATCH_FILE" '
            '"${PANGU92B_API_KEY:-${PANGU_API_KEY:-${COMPANY_GLM_API_KEY:-${COMPANY_DEEPSEEK_API_KEY:-}}}}" '
            '"${COMPANY_DEEPSEEK_API_KEY:-}" "$SERPER_API_KEY" "$E2B_API_KEY" '
            '"${PANGU92B_BASE_URL:-${PANGU_BASE_URL:-${COMPANY_GLM_BASE_URL:-${COMPANY_DEEPSEEK_BASE_URL:-}}}}" "$NO_PROXY" '
            '"${PANGU92B_HW_ID:-}" "${PANGU92B_APP_KEY:-}"\n',
        }
        for name, code in programs.items():
            executable = binaries / name
            executable.write_text("#!/bin/bash\n" + code, encoding="utf-8")
            executable.chmod(0o700)
        environment = {name: value for name, value in os.environ.items() if not name.upper().startswith(("DSH_", "COMPANY_", "PANGU_", "PANGU92B_", "SERPER_", "E2B_", "SLURM_"))}
        for name in ("SSL_CERT_FILE", "NO_PROXY", "no_proxy"):
            environment.pop(name, None)
        environment.update(
            PATH=binaries.as_posix() + ":/usr/bin:/bin", WORK=work.as_posix(),
            DSH_INSIDE_CONTAINER="1", DSH_REPO_ROOT=self.root.as_posix(), DSH_SCRIPT_PATH=(REPOSITORY / "run.sh").as_posix(),
            DSH_CONDA_ROOT=conda.as_posix(), DSH_BATCH_MODE="benchmark", DSH_TEST_CA_FILE=ca_file.as_posix(),
            DSH_COMPANY_API_NO_PROXY="1",
            COMPANY_DEEPSEEK_BASE_URL="http://115.120.87.159:8082/v1",
            DSH_TEST_PYTHON=sys.executable,
        )
        for model, provider, base_url in (
            ("deepseek", "company-deepseek", "http://115.120.87.159:8082/v1"),
            ("glm", "company-glm", "http://115.120.87.159:8082/v1"),
            ("pangu", "pangu", "http://101.245.71.190:9080/v1"),
            ("pangu92b", "pangu92b", "https://apigw-dgg-b0.huawei.com/api/pangu/v1"),
        ):
            with self.subTest(provider=provider):
                selected = {**environment, "DSH_MODEL_PROVIDER": provider, "DSH_BATCH_ID": f"setup-{model}"}
                result = subprocess.run([os.environ["DSH_BENCHMARK_TEST_BASH"], (REPOSITORY / "run.sh").as_posix(), (self.root / "benchmark.json").as_posix()], env=selected, capture_output=True, text=True, timeout=30)
                self.assertEqual(result.returncode, 0, result.stderr)
                values = result.stdout.splitlines()
                self.assertEqual(values[:3], [provider, configs.as_posix() + f"/{model}.patch.yml", f"{model}-test-key"])
                self.assertEqual(values[3], "deepseek-test-key" if model != "glm" else "")
                self.assertEqual(values[4:7], ["serper-api-key-test-value", "e2b-api-key-test-value", base_url])
                self.assertIn(base_url.split("/")[2].split(":")[0], values[7].split(","))
                if model in ("pangu", "pangu92b"):
                    self.assertIn("115.120.87.159", values[7].split(","))
                self.assertEqual(values[8:], ["test-hw-id", "test-app-key"] if model == "pangu92b" else ["", ""])
                self.assertNotIn(f"{model}-test-key", result.stderr)
                self.assertNotIn("test-app-key", result.stderr)
        for bundle in ({"api_key": "must-not-leak"}, {"api_key": "must-not-leak\nsecond", "hw_id": "id", "hw_app_key": "app"}, "must-not-leak"):
            credentials.write_text(json.dumps(bundle), encoding="utf-8")
            selected = {**environment, "DSH_MODEL_PROVIDER": "pangu92b", "DSH_BATCH_ID": "setup-invalid-bundle"}
            rejected = subprocess.run([os.environ["DSH_BENCHMARK_TEST_BASH"], (REPOSITORY / "run.sh").as_posix(), (self.root / "benchmark.json").as_posix()], env=selected, capture_output=True, text=True, timeout=30)
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("invalid Pangu92B credential file", rejected.stderr)
            self.assertNotIn("must-not-leak", rejected.stderr)
            self.assertEqual(rejected.stdout, "")
        selected = {**environment, "DSH_MODEL_PROVIDER": "pangu", "DSH_BATCH_ID": "setup-missing", "DSH_API_KEY_FILE": (secrets / "missing-key").as_posix()}
        failed = subprocess.run([os.environ["DSH_BENCHMARK_TEST_BASH"], (REPOSITORY / "run.sh").as_posix(), (self.root / "benchmark.json").as_posix()], env=selected, capture_output=True, text=True, timeout=30)
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("protected key file", failed.stderr)
        self.assertEqual(failed.stdout, "")
        invalid = secrets / "multiline-key"
        invalid.write_bytes(b"first-line\nsecond-line\n")
        invalid.chmod(0o600)
        selected["DSH_API_KEY_FILE"] = invalid.as_posix()
        rejected = subprocess.run([os.environ["DSH_BENCHMARK_TEST_BASH"], (REPOSITORY / "run.sh").as_posix(), (self.root / "benchmark.json").as_posix()], env=selected, capture_output=True, text=True, timeout=30)
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn("exactly one key line", rejected.stderr)
        self.assertEqual(rejected.stdout, "")

    @unittest.skipUnless(os.environ.get("DSH_BENCHMARK_TEST_BASH"), "set DSH_BENCHMARK_TEST_BASH for Slurm wrapper checks")
    def test_wrappers_select_provider_and_resolve_repository_not_spool_path(self) -> None:
        (self.root / "run.sh").write_text("printf '%s\\n' \"$DSH_MODEL_PROVIDER\" \"$DSH_BATCH_MODE\" \"$DSH_BATCH_ID\" \"$1\" \"$DSH_PATCH_FILE\" \"$DSH_API_KEY_FILE\"\n", encoding="utf-8")
        environment = os.environ.copy()
        for name in ("DSH_REPO_ROOT", "DSH_SCRIPT_PATH", "DSH_BATCH_ID", "DSH_PATCH_FILE", "DSH_API_KEY_FILE"):
            environment.pop(name, None)
        environment.update(SLURM_SUBMIT_DIR=self.root.as_posix(), SLURM_JOB_ID="123", DSH_MODEL_PROVIDER="wrong-provider", WORK=self.base.as_posix())
        for filename, provider, model, batch_id in (
            ("run_deepseek.sh", "company-deepseek", "deepseek", "benchmark-deepseek-123"),
            ("run_pangu.sh", "pangu", "pangu", "benchmark-pangu-123"),
            ("run_glm.sh", "company-glm", "glm", "benchmark-glm-123"),
            ("run_pangu92b.sh", "pangu92b", "pangu92b", "benchmark-pangu92b-123"),
        ):
            result = subprocess.run([os.environ["DSH_BENCHMARK_TEST_BASH"], (REPOSITORY / filename).as_posix()], cwd=self.base, env=environment, capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.splitlines(), [
                provider, "benchmark", batch_id, self.root.as_posix() + "/benchmark_groups.json",
                self.base.as_posix() + f"/dsh-config/{model}.patch.yml", self.base.as_posix() + f"/.secrets/{model}-api-key" + (".yml" if model == "pangu92b" else ""),
            ])

    @unittest.skipUnless(os.environ.get("DSH_BENCHMARK_TEST_NODE"), "set DSH_BENCHMARK_TEST_NODE to a supported Node executable for the source-profile smoke")
    def test_actual_headless_profile_preserves_prompt_and_restores_tool_write(self) -> None:
        self.exercise_headless_profile(deployment=None)

    @unittest.skipUnless(os.environ.get("DSH_BENCHMARK_TEST_NODE"), "set DSH_BENCHMARK_TEST_NODE to a supported Node executable for the GLM source-profile smoke")
    def test_company_glm_patch_sends_model_and_credential_and_restores_tool_write(self) -> None:
        self.exercise_headless_profile(deployment="glm")

    @unittest.skipUnless(os.environ.get("DSH_BENCHMARK_TEST_NODE"), "set DSH_BENCHMARK_TEST_NODE for the DeepSeek deployment smoke")
    def test_deepseek_patch_sends_model_and_credential_and_restores_tool_write(self) -> None:
        self.exercise_headless_profile(deployment="deepseek")

    @unittest.skipUnless(os.environ.get("DSH_BENCHMARK_TEST_NODE"), "set DSH_BENCHMARK_TEST_NODE for the Pangu deployment smoke")
    def test_pangu_patch_uses_bearer_without_huawei_headers_and_restores_tool_write(self) -> None:
        self.exercise_headless_profile(deployment="pangu")

    @unittest.skipUnless(os.environ.get("DSH_BENCHMARK_TEST_NODE"), "set DSH_BENCHMARK_TEST_NODE for the Pangu92B deployment smoke")
    def test_pangu92b_patch_sends_bearer_and_huawei_headers_and_restores_tool_write(self) -> None:
        self.exercise_headless_profile(deployment="pangu92b")

    @unittest.skipUnless(os.environ.get("DSH_BENCHMARK_TEST_NODE"), "set DSH_BENCHMARK_TEST_NODE for the Pangu rate-limit recovery smoke")
    def test_pangu_patch_retries_rate_limit_with_deployment_backoff_and_records_recovery(self) -> None:
        self.exercise_headless_profile(deployment="pangu", rate_limit_once=True)

    @unittest.skipUnless(os.environ.get("DSH_BENCHMARK_TEST_NODE"), "set DSH_BENCHMARK_TEST_NODE for the E2B attachment composition smoke")
    def test_headless_session_logs_e2b_sync_of_the_actual_modified_attachment(self) -> None:
        self.exercise_headless_profile(deployment=None, with_e2b=True)

    def exercise_headless_profile(self, *, deployment: str | None, rate_limit_once: bool = False, with_e2b: bool = False) -> None:
        requests: list[dict[str, object]] = []
        request_headers: list[tuple[str, str | None, str | None, str | None]] = []
        root = self.root

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_arguments: object) -> None:
                pass

            def do_POST(self) -> None:
                payload = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                requests.append(payload)
                request_headers.append((self.path, self.headers.get("Authorization"), self.headers.get("X-HW-ID"), self.headers.get("X-HW-AppKey")))
                if rate_limit_once and len(requests) == 1:
                    body = json.dumps({"error_msg": "rate limit exceeded"}).encode()
                    self.send_response(429)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                    return
                response_number = len(requests) - int(rate_limit_once)
                if response_number == 1:
                    delta = {"role": "assistant", "tool_calls": [{"index": 0, "id": "call-read", "type": "function", "function": {
                        "name": "read", "arguments": json.dumps({"file_path": str(root / "parser.py")})}}]}
                    finish = "tool_calls"
                elif response_number == 2:
                    delta = {"role": "assistant", "tool_calls": [{"index": 0, "id": "call-write", "type": "function", "function": {
                        "name": "write", "arguments": json.dumps({"file_path": str(root / "parser.py"), "content": "fixed via real harness\n"})}}]}
                    finish = "tool_calls"
                elif with_e2b and response_number == 3:
                    delta = {"role": "assistant", "tool_calls": [{"index": 0, "id": "call-e2b", "type": "function", "function": {
                        "name": "mcp__e2b__execute_python", "arguments": json.dumps({"code": "print(15)"})}}]}
                    finish = "tool_calls"
                else:
                    delta, finish = {"role": "assistant", "content": "done"}, "stop"
                chunks = [
                    {"id": "response-test", "object": "chat.completion.chunk", "model": payload["model"], "choices": [{"index": 0, "delta": delta, "finish_reason": None}]},
                    {"id": "response-test", "object": "chat.completion.chunk", "model": payload["model"], "choices": [{"index": 0, "delta": {}, "finish_reason": finish}], "usage": {"prompt_tokens": 20, "completion_tokens": 10, "total_tokens": 30}},
                ]
                body = "".join("data: " + json.dumps(chunk) + "\n\n" for chunk in chunks) + "data: [DONE]\n\n"
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Content-Length", str(len(body.encode())))
                self.end_headers()
                self.wfile.write(body.encode())

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        def close_server() -> None:
            server.shutdown()
            server.server_close()
            thread.join()
        self.addCleanup(close_server)
        scripts = self.root / "scripts"
        scripts.mkdir()
        if with_e2b:
            for name in ("dsh-e2b-mcp.py", "dsh_e2b_environment.py"):
                shutil.copy2(REPOSITORY / "scripts" / name, scripts / name)
        home = self.base / "home"
        fixture = self.base / "provider.patch.json"
        batch.write_json(fixture, [
            {"id": "llm-deepseek", "disabled": True},
            {"id": "session-title-llm", "disabled": True},
            {"id": "llm-pi-ai", "config": {"providers": {"fixture-provider": {
                "api": "openai-completions", "baseURL": f"http://127.0.0.1:{server.server_port}/v1",
                "apiKeyEnv": "DSH_BENCHMARK_TEST_KEY", "models": [{"id": "fixture", "contextWindow": 32768, "maxTokens": 1024}],
            }}}},
            {"id": "agent-default-model", "config": {"provider": "fixture-provider", "model": "fixture"}},
            {"id": "session-persistence-jsonl", "config": {"root": str(home / "sessions"), "compression": "none"}},
        ])
        runner, cases = self.runner()
        runner.home = home
        runner.patches = [fixture]
        if with_e2b:
            fixture_sdk = REPOSITORY / "scripts/test-e2b-mcp.py"
            bootstrap = (
                "import importlib.util,runpy,sys,types; "
                f"sys.path.insert(0,{str(scripts)!r}); "
                f"spec=importlib.util.spec_from_file_location('e2b_fixture',{str(fixture_sdk)!r}); "
                "fixture=importlib.util.module_from_spec(spec);spec.loader.exec_module(fixture); "
                "sdk=types.ModuleType('e2b_code_interpreter');sdk.Sandbox=fixture.FakeSandbox;sys.modules['e2b_code_interpreter']=sdk; "
                f"runpy.run_path({str(scripts / 'dsh-e2b-mcp.py')!r},run_name='__main__')"
            )
            configuration = self.base / "e2b-projects.json"
            batch.write_json(configuration, {"projects": [{"attachment_prefix": "parser.py/", "packages": []}]})
            overlay = self.base / "e2b.patch.json"
            batch.write_json(overlay, [{"insert": [{"id": "mcp-e2b", "name": "@deepseek-ai/dsh-mcp-client", "config": {
                "transport": "stdio", "serverName": "e2b", "command": sys.executable, "args": ["-c", bootstrap],
                "env": {"E2B_API_KEY": "test-key", "E2B_PROXY": "", "DSH_E2B_TASK_FILE": str(runner.records / "G-code/S1/task.json"),
                        "DSH_E2B_EXPORT_ROOT": str(self.root), "DSH_E2B_PROJECTS_FILE": str(configuration)},
                "cwd": str(self.root), "failOnStartupError": True, "reconnect": {"enabled": False},
            }}]}])
            runner.patches.append(overlay)
        if deployment is not None:
            config_root = Path(os.environ.get("DSH_BENCHMARK_TEST_CONFIG_DIR", REPOSITORY / "scripts/config"))
            runner.patches.append(config_root / f"{deployment}.patch.yml")
        # This source launch exercises an out-of-tree deployment prompt plugin through the dsh CLI.
        runner.launcher = [os.environ["DSH_BENCHMARK_TEST_NODE"], "--import", (REPOSITORY / "node_modules/tsx/dist/esm/index.mjs").as_uri(), str(REPOSITORY / "apps/cli/src/bin.ts")]
        with patch.dict(os.environ, {
            "DSH_HOME": str(home), "DSH_TELEMETRY_DISABLED": "1", "DSH_TOOLS_MODE": "native",
            "DSH_BENCHMARK_TEST_KEY": "test-key", "NO_PROXY": "127.0.0.1,localhost",
            "TSX_TSCONFIG_PATH": str(REPOSITORY / "tsconfig.base.json"),
            "COMPANY_GLM_API_KEY": "glm-test-key", "COMPANY_GLM_BASE_URL": f"http://127.0.0.1:{server.server_port}/v1",
            "COMPANY_GLM_CONTEXT_WINDOW": "32768", "COMPANY_GLM_MAX_TOKENS": "1024",
            "COMPANY_DEEPSEEK_API_KEY": "deepseek-test-key", "COMPANY_DEEPSEEK_BASE_URL": f"http://127.0.0.1:{server.server_port}/v1",
            "PANGU_API_KEY": "pangu-test-key", "PANGU_BASE_URL": f"http://127.0.0.1:{server.server_port}/v1",
            "PANGU_CONTEXT_WINDOW": "32768", "PANGU_MAX_TOKENS": "1024",
            "PANGU_HW_ID": "obsolete-test-id", "PANGU_APP_KEY": "obsolete-test-app-key",
            "PANGU92B_API_KEY": "pangu92b-test-key", "PANGU92B_BASE_URL": f"http://127.0.0.1:{server.server_port}/v1",
            "PANGU92B_HW_ID": "test-hw-id", "PANGU92B_APP_KEY": "test-app-key",
            "PANGU92B_CONTEXT_WINDOW": "32768", "PANGU92B_MAX_TOKENS": "1024",
        }):
            result = runner.run_case(cases[0])
        folder = runner.records / "G-code" / "S1"
        self.assertEqual(result["status"], "succeeded", (folder / "diagnostics.log").read_text(encoding="utf-8"))
        request_count = 3 + int(rate_limit_once) + int(with_e2b)
        self.assertEqual(len(requests), request_count)
        if deployment is not None:
            model = {"deepseek": "deepseek-v4-pro", "glm": "glm-5.3", "pangu": "openPangu-v21-pro", "pangu92b": "pangu92b_wandr"}[deployment]
            hw_id, hw_app_key = ("test-hw-id", "test-app-key") if deployment == "pangu92b" else (None, None)
            self.assertEqual(request_headers, [("/v1/chat/completions", f"Bearer {deployment}-test-key", hw_id, hw_app_key)] * request_count)
            self.assertTrue(all(request["model"] == model for request in requests))
            if deployment != "deepseek":
                self.assertTrue(all(0 < request["max_tokens"] <= 1024 for request in requests))
        for request in requests:
            systems = [message["content"] for message in request["messages"] if message["role"] == "system"]
            self.assertTrue(systems)
            self.assertNotIn(cases[0]["effective_system_prompt"], systems)
            self.assertTrue(any("You are" in system for system in systems))
        self.assertFalse((folder / "prompt.patch.json").exists())
        self.assertTrue(any(message["role"] == "tool" for message in requests[1 + int(rate_limit_once)]["messages"]))
        self.assertTrue((folder / "artifacts" / "parser.py").exists(), json.dumps(requests[-1]["messages"], ensure_ascii=False)[-3500:])
        self.assertEqual((folder / "artifacts" / "parser.py").read_bytes(), b"fixed via real harness\n")
        self.assertEqual((self.root / "parser.py").read_bytes(), b"original broken parser\n")
        self.assertEqual(json.loads((folder / "session-records.json").read_text(encoding="utf-8"))["status"], "complete")
        if with_e2b:
            messages = [message for message in requests[-1]["messages"] if message["role"] == "tool"]
            self.assertTrue(any(hashlib.sha256(b"fixed via real harness\n").hexdigest() in json.dumps(message) for message in messages))
            events = [json.loads(line) for line in (folder / "session-records/session.v4.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertTrue(any(event.get("type") == "tool/result" and "validation_scope" in json.dumps(event) for event in events))
        if rate_limit_once:
            events = [json.loads(line) for line in (folder / "session-records/session.v4.jsonl").read_text(encoding="utf-8").splitlines()]
            retries = [event["data"] for event in events if event["type"] == "llm/retry"]
            self.assertEqual(len(retries), 1)
            retry = retries[0]
            self.assertEqual((retry["provider"], retry["failure"]["code"], retry["mode"], retry["retry"], retry["maxRetries"]), ("pangu", "RATE_LIMIT", "normal", 1, 8))
            self.assertGreaterEqual(retry["delayMs"], 9000)
            self.assertLessEqual(retry["delayMs"], 11000)
            self.assertEqual(json.loads(retry["policyKey"])[3:], [10000, 120000, 0.1])


if __name__ == "__main__":
    unittest.main()
