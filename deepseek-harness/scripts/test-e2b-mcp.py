"""Offline checks for the E2B MCP adapter used by the cluster batch profile."""

from __future__ import annotations

import hashlib
import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch


def load_adapter() -> types.ModuleType:
    script = Path(__file__).with_name("dsh-e2b-mcp.py")
    spec = importlib.util.spec_from_file_location("dsh_e2b_test", script)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeFiles:
    def __init__(self) -> None:
        self.contents: dict[str, bytes] = {}
        self.fail_after_first_chunk = False
        self.calls: list[tuple[str, str]] = []

    def write(self, path: str, data: bytes) -> None:
        self.contents[path] = bytes(data)

    def read(self, path: str, *, format: str) -> object:
        self.calls.append((path, format))
        data = self.contents[path]

        def chunks() -> object:
            yield data[:2]
            if self.fail_after_first_chunk:
                raise RuntimeError("remote read interrupted")
            yield data[2:]

        return chunks()


class FakeSandbox:
    instances: list[FakeSandbox] = []

    def __init__(self, **kwargs: object) -> None:
        self.options = kwargs
        self.sandbox_id = "sandbox-test"
        self.calls: list[str] = []
        self.files = FakeFiles()
        self.closed = False
        self.install_calls: list[list[str]] = []
        self.install_failure = False
        self.upload_failure = False
        self.commands = types.SimpleNamespace(run=lambda *args, **kwargs: None)
        self.instances.append(self)

    @classmethod
    def create(cls, **kwargs: object) -> FakeSandbox:
        return cls(**kwargs)

    def __enter__(self) -> FakeSandbox:
        return self

    def __exit__(self, *_args: object) -> None:
        self.closed = True

    def run_code(self, code: str) -> object:
        self.calls.append(code)
        if code.startswith("import os as _dsh_os"):
            output = io.StringIO()
            def install(argv: list[str], **_kwargs: object) -> None:
                self.install_calls.append(argv)
                if self.install_failure:
                    raise RuntimeError("dependency install failed")
            try:
                with contextlib.redirect_stdout(output), patch.object(sys, "path", sys.path.copy()), patch("os.chdir"), patch("subprocess.run", side_effect=install), patch.object(Path, "read_bytes", autospec=True, side_effect=lambda path: self.files.contents[path.as_posix()]), patch.object(Path, "write_text", return_value=0), patch("importlib.metadata.distributions", return_value=[]), patch("importlib.metadata.version", return_value="test-version"):
                    exec(compile(code, "<remote-setup>", "exec"), {})
                error = None
            except Exception as failure:
                error = str(failure)
            return types.SimpleNamespace(logs=types.SimpleNamespace(stdout=[output.getvalue()], stderr=[]), error=error, results=[])
        error = "bad code" if code == "raise" else None
        return types.SimpleNamespace(
            logs=types.SimpleNamespace(stdout=["15\n"], stderr=[]),
            error=error,
            results=[types.SimpleNamespace(text="15", png=None, jpeg=None)],
        )


class E2BTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name)
        FakeSandbox.instances = []
        fake_sdk = types.ModuleType("e2b_code_interpreter")
        fake_sdk.Sandbox = FakeSandbox
        module_patch = patch.dict(sys.modules, {"e2b_code_interpreter": fake_sdk})
        module_patch.start()
        self.addCleanup(module_patch.stop)
        env_patch = patch.dict(os.environ, {
            "E2B_API_KEY": "test-key",
            "E2B_PROXY": "http://proxy.test:3128",
            "DSH_E2B_EXPORT_ROOT": str(self.root),
            "DSH_E2B_MAX_EXPORT_BYTES": "8",
            "DSH_E2B_TASK_FILE": "", "DSH_E2B_PROJECTS_FILE": "", "DSH_E2B_TEMPLATE": "",
        })
        env_patch.start()
        self.addCleanup(env_patch.stop)
        self.adapter = load_adapter()
        self.addCleanup(self.adapter.stack.close)

    def call(self, name: str, **arguments: str) -> dict[str, object]:
        response = self.adapter.handle({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments},
        })
        assert response is not None
        return response["result"]

    def test_persistent_sandbox_proxy_and_error(self) -> None:
        listed = self.adapter.handle({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
        self.assertEqual([tool["name"] for tool in listed["result"]["tools"]], ["execute_python", "export_file", "prepare_environment"])
        for code in ("x = 10", "x += 5; print(x)"):
            self.assertFalse(self.call("execute_python", code=code)["isError"])
        self.assertTrue(self.call("execute_python", code="raise")["isError"])
        self.assertEqual(len(FakeSandbox.instances), 1)
        self.assertEqual(FakeSandbox.instances[0].options, {"proxy": "http://proxy.test:3128", "timeout": 3600})
        self.assertEqual(FakeSandbox.instances[0].calls[1], "x += 5; print(x)")
        self.adapter.stack.close()
        self.assertTrue(FakeSandbox.instances[0].closed)

    def test_export_from_same_sandbox_returns_metadata_not_bytes(self) -> None:
        self.call("execute_python", code="x = 10")
        sandbox = FakeSandbox.instances[0]
        sandbox.files.contents["/home/user/chart.png"] = b"PNG\x00data"
        result = self.call("export_file", remote_path="/home/user/chart.png", local_path="charts/chart.png")
        self.assertFalse(result["isError"])
        self.assertEqual(len(FakeSandbox.instances), 1)
        self.assertEqual(sandbox.files.calls, [("/home/user/chart.png", "stream")])
        self.assertEqual((self.root / "charts/chart.png").read_bytes(), b"PNG\x00data")
        self.assertEqual(result["structuredContent"]["bytes"], 8)
        self.assertEqual(result["structuredContent"]["sha256"], hashlib.sha256(b"PNG\x00data").hexdigest())
        self.assertNotIn("PNG", result["content"][0]["text"])

    def test_export_rejects_existing_file_and_unsafe_paths(self) -> None:
        self.call("execute_python", code="x = 10")
        FakeSandbox.instances[0].files.contents["/chart.png"] = b"new"
        existing = self.root / "chart.png"
        existing.write_bytes(b"old")
        for local_path in ("chart.png", "../escape.png", "/tmp/escape.png", "a//b.png", "a/./b.png", "a/../b.png", "a\\b.png", ".git/hooks/chart.png", "node_modules/chart.png"):
            with self.subTest(local_path=local_path):
                result = self.call("export_file", remote_path="/chart.png", local_path=local_path)
                self.assertTrue(result["isError"])
        self.assertEqual(existing.read_bytes(), b"old")
        self.assertFalse((self.root.parent / "escape.png").exists())

    def test_export_rejects_symlink_parent(self) -> None:
        outside = self.root / "outside"
        outside.mkdir()
        try:
            (self.root / "linked").symlink_to(outside, target_is_directory=True)
        except OSError as error:
            self.skipTest(f"directory symlinks unavailable: {error}")
        self.call("execute_python", code="x = 10")
        FakeSandbox.instances[0].files.contents["/chart.png"] = b"new"
        result = self.call("export_file", remote_path="/chart.png", local_path="linked/chart.png")
        self.assertTrue(result["isError"])
        self.assertFalse((outside / "chart.png").exists())

    def test_export_limit_and_remote_failure_leave_no_partial_file(self) -> None:
        self.call("execute_python", code="x = 10")
        files = FakeSandbox.instances[0].files
        files.contents["/large.png"] = b"123456789"
        self.assertTrue(self.call("export_file", remote_path="/large.png", local_path="charts/large.png")["isError"])
        self.assertFalse((self.root / "charts/large.png").exists())
        files.contents["/broken.png"] = b"good"
        files.fail_after_first_chunk = True
        self.assertTrue(self.call("export_file", remote_path="/broken.png", local_path="charts/broken.png")["isError"])
        self.assertFalse((self.root / "charts/broken.png").exists())
        self.assertEqual(list((self.root / "charts").iterdir()), [])

    def task_inputs(self, *, packages: list[str] | None = None) -> Path:
        folder = self.root / "attached_files/task_2"
        folder.mkdir(parents=True)
        source = folder / "model.py"
        source.write_bytes(b"x = 10\n")
        task_file = self.root / "task.json"
        task_file.write_text(json.dumps({"resolved_attached_files": [str(source)]}), encoding="utf-8")
        configuration = self.root / "projects.json"
        configuration.write_text(json.dumps({"projects": [{"attachment_prefix": "attached_files/task_2/", "packages": packages or []}]}), encoding="utf-8")
        os.environ.update(DSH_E2B_TASK_FILE=str(task_file), DSH_E2B_PROJECTS_FILE=str(configuration))
        return source

    def test_sync_and_dependency_install_precede_code_and_repeat_local_edits(self) -> None:
        source = self.task_inputs(packages=["example-project==1.0", "pytest"])
        first = self.call("execute_python", code="x = 10")
        self.assertFalse(first["isError"], first)
        active = FakeSandbox.instances[0]
        report = first["structuredContent"]["environment"]
        remote = report["files"][0]["remote_path"]
        self.assertEqual(active.files.contents[remote], source.read_bytes())
        self.assertEqual(report["files"][0]["sha256"], hashlib.sha256(source.read_bytes()).hexdigest())
        self.assertEqual(active.install_calls[0][-2:], ["example-project==1.0", "pytest"])
        self.assertEqual(active.calls[-1], "x = 10")
        source.write_bytes(b"x = 20\n")
        again = self.call("execute_python", code="print(x)")
        self.assertFalse(again["isError"], again)
        self.assertEqual(active.files.contents[remote], b"x = 20\n")
        self.assertEqual(len(active.install_calls), 1)
        self.assertEqual(len(FakeSandbox.instances), 1)
        self.assertIn("not a full original project", report["validation_scope"])

    def test_prepare_reports_paths_without_running_task_code_and_template_is_explicit(self) -> None:
        self.task_inputs()
        os.environ["DSH_E2B_TEMPLATE"] = "project-template"
        result = self.call("prepare_environment")
        self.assertFalse(result["isError"], result)
        self.assertEqual(result["structuredContent"]["status"], "ready")
        self.assertEqual(FakeSandbox.instances[0].options["template"], "project-template")
        self.assertTrue(all(code.startswith("import os as _dsh_os") for code in FakeSandbox.instances[0].calls))

    def test_failed_install_blocks_task_code_and_does_not_claim_ready(self) -> None:
        self.task_inputs(packages=["example-project==1.0"])
        self.adapter.get_sandbox().install_failure = True
        result = self.call("execute_python", code="must_not_run")
        self.assertTrue(result["isError"])
        self.assertIn("dependency install failed", result["content"][0]["text"])
        self.assertNotIn("must_not_run", FakeSandbox.instances[0].calls)
        previous = len(FakeSandbox.instances[0].calls)
        self.assertTrue(self.call("execute_python", code="still_must_not_run")["isError"])
        self.assertEqual(len(FakeSandbox.instances[0].calls), previous)

    def test_reject_external_hidden_symlink_and_oversize_inputs_before_upload(self) -> None:
        source = self.task_inputs()
        task_file = Path(os.environ["DSH_E2B_TASK_FILE"])
        outside = self.root.parent / (self.root.name + "-outside.py")
        # The invalid external name need not exist: it must fail before opening it.
        for path in (outside, self.root / ".secrets/key", self.root / "node_modules/key"):
            with self.subTest(path=path):
                self.adapter.environment = self.adapter.Environment()
                task_file.write_text(json.dumps({"resolved_attached_files": [str(path)]}), encoding="utf-8")
                self.assertTrue(self.call("execute_python", code="must_not_run")["isError"])
                self.assertEqual(FakeSandbox.instances[0].files.contents, {})
        task_file.write_text(json.dumps({"resolved_attached_files": [str(source)]}), encoding="utf-8")
        self.adapter.environment = self.adapter.Environment()
        os.environ["DSH_E2B_MAX_INPUT_FILE_BYTES"] = "2"
        self.assertTrue(self.call("execute_python", code="must_not_run")["isError"])
        self.assertEqual(FakeSandbox.instances[0].files.contents, {})

    def test_opt_in_project_tree_and_requirements_are_prepared_but_secrets_are_excluded(self) -> None:
        source = self.task_inputs()
        project = source.parent
        (project / "requirements.txt").write_text("example-project==1.0\n", encoding="utf-8")
        (project / "pyproject.toml").write_text('[project]\nname="example-project"\nversion="1.0"\n', encoding="utf-8")
        (project / ".env").write_text("SECRET=must_not_upload\n", encoding="utf-8")
        (project / "service-api-key").write_text("must_not_upload\n", encoding="utf-8")
        profile = {
            "attachment_prefix": "attached_files/task_2/", "project_dir": "attached_files/task_2",
            "install_project": True, "requirements_files": ["attached_files/task_2/requirements.txt"],
        }
        Path(os.environ["DSH_E2B_PROJECTS_FILE"]).write_text(json.dumps({"projects": [profile]}), encoding="utf-8")
        result = self.call("prepare_environment")
        self.assertFalse(result["isError"], result)
        uploaded = FakeSandbox.instances[0].files.contents
        self.assertEqual(len(uploaded), 3)
        self.assertTrue(all(".env" not in path and "api-key" not in path for path in uploaded))
        arguments = FakeSandbox.instances[0].install_calls[0]
        self.assertIn("-r", arguments)
        self.assertIn("-e", arguments)

    def test_incomplete_project_and_bad_dependency_options_fail_before_execution(self) -> None:
        self.task_inputs()
        config = Path(os.environ["DSH_E2B_PROJECTS_FILE"])
        for values in ({"project_dir": "attached_files/task_2", "install_project": True}, {"install_project": True}, {"packages": ["--extra-index-url"]}):
            self.adapter.environment = self.adapter.Environment()
            config.write_text(json.dumps({"projects": [{"attachment_prefix": "attached_files/task_2/", **values}]}), encoding="utf-8")
            result = self.call("execute_python", code="must_not_run")
            self.assertTrue(result["isError"])
            self.assertNotIn("must_not_run", FakeSandbox.instances[0].calls)

    def test_real_stdio_mcp_process_returns_logged_sync_and_dependency_metadata(self) -> None:
        source = self.task_inputs(packages=["example-project==1.0"])
        scripts = Path(__file__).resolve().parent
        bootstrap = (
            "import importlib.util,runpy,sys,types; "
            f"sys.path.insert(0,{str(scripts)!r}); "
            f"spec=importlib.util.spec_from_file_location('e2b_fixture',{str(Path(__file__).resolve())!r}); "
            "fixture=importlib.util.module_from_spec(spec);spec.loader.exec_module(fixture); "
            "sdk=types.ModuleType('e2b_code_interpreter');sdk.Sandbox=fixture.FakeSandbox;sys.modules['e2b_code_interpreter']=sdk; "
            f"runpy.run_path({str(scripts / 'dsh-e2b-mcp.py')!r},run_name='__main__')"
        )
        requests = [
            {"jsonrpc": "2.0", "id": 1, "method": "tools/list"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "prepare_environment", "arguments": {}}},
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "execute_python", "arguments": {"code": "print(15)"}}},
        ]
        result = subprocess.run([sys.executable, "-c", bootstrap], input="".join(json.dumps(request) + "\n" for request in requests), env=os.environ.copy(), capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        responses = [json.loads(line) for line in result.stdout.splitlines()]
        self.assertEqual([response["id"] for response in responses], [1, 2, 3])
        for response in responses[1:]:
            self.assertFalse(response["result"]["isError"], response)
            logged = json.loads(response["result"]["content"][0]["text"])
            report = logged.get("environment", logged)
            self.assertEqual(report["files"][0]["sha256"], hashlib.sha256(source.read_bytes()).hexdigest())
            self.assertEqual(report["dependencies"]["packages"], {"example-project": "test-version"})

    def test_symlink_attachment_is_rejected(self) -> None:
        source = self.task_inputs()
        linked = source.parent / "linked.py"
        try:
            linked.symlink_to(source)
        except OSError as error:
            self.skipTest(f"file symlinks unavailable: {error}")
        Path(os.environ["DSH_E2B_TASK_FILE"]).write_text(json.dumps({"resolved_attached_files": [str(linked)]}), encoding="utf-8")
        self.assertTrue(self.call("execute_python", code="must_not_run")["isError"])
        self.assertEqual(FakeSandbox.instances[0].files.contents, {})

    def test_empty_keep_placeholder_uploads_but_nonempty_keep_is_rejected(self) -> None:
        source = self.task_inputs()
        placeholder = source.parent / ".keep"
        placeholder.write_bytes(b"")
        task_file = Path(os.environ["DSH_E2B_TASK_FILE"])
        task_file.write_text(json.dumps({"resolved_attached_files": [str(placeholder)]}), encoding="utf-8")
        result = self.call("prepare_environment")
        self.assertFalse(result["isError"], result)
        remote = result["structuredContent"]["files"][0]["remote_path"]
        self.assertEqual(FakeSandbox.instances[0].files.contents[remote], b"")
        placeholder.write_bytes(b"must_not_upload")
        self.adapter.environment = self.adapter.Environment()
        result = self.call("execute_python", code="must_not_run")
        self.assertTrue(result["isError"])
        self.assertNotIn("must_not_run", FakeSandbox.instances[0].calls)

    def test_keep_with_hidden_parent_is_rejected(self) -> None:
        hidden = self.root / ".hidden/.keep"
        hidden.parent.mkdir()
        hidden.write_bytes(b"")
        with self.assertRaisesRegex(ValueError, "hidden"):
            self.adapter.Environment.safe_file(self.root, hidden)

    def test_keep_symlink_is_rejected(self) -> None:
        source = self.task_inputs()
        placeholder = source.parent / ".keep"
        source.write_bytes(b"")
        try:
            placeholder.symlink_to(source)
        except OSError as error:
            self.skipTest(f"file symlinks unavailable: {error}")
        with self.assertRaisesRegex(ValueError, "empty regular files"):
            self.adapter.Environment.safe_file(self.root, placeholder)

    def test_changed_dependency_configuration_requires_a_fresh_task(self) -> None:
        self.task_inputs(packages=["example-project==1.0"])
        self.assertFalse(self.call("prepare_environment")["isError"])
        config = Path(os.environ["DSH_E2B_PROJECTS_FILE"])
        data = json.loads(config.read_text(encoding="utf-8"))
        data["projects"][0]["packages"] = ["example-project==2.0"]
        config.write_text(json.dumps(data), encoding="utf-8")
        result = self.call("execute_python", code="must_not_run")
        self.assertTrue(result["isError"])
        self.assertIn("restart this task", result["content"][0]["text"])
        self.assertNotIn("must_not_run", FakeSandbox.instances[0].calls)

    def test_declared_import_failure_blocks_task_code(self) -> None:
        self.task_inputs()
        config = Path(os.environ["DSH_E2B_PROJECTS_FILE"])
        data = json.loads(config.read_text(encoding="utf-8"))
        data["projects"][0]["imports"] = ["nonexistent_dsh_e2b_fixture_module"]
        config.write_text(json.dumps(data), encoding="utf-8")
        result = self.call("execute_python", code="must_not_run")
        self.assertTrue(result["isError"])
        self.assertIn("nonexistent_dsh_e2b_fixture_module", result["content"][0]["text"])
        self.assertNotIn("must_not_run", FakeSandbox.instances[0].calls)

    def test_shipped_astropy_profile_and_unpinned_django_profile_are_explicit(self) -> None:
        configuration = json.loads((Path(__file__).parent / "config/e2b-projects.json").read_text(encoding="utf-8"))
        profiles = {profile["attachment_prefix"]: profile for profile in configuration["projects"]}
        self.assertEqual(profiles["attached_files/task_2/"]["packages"], ["astropy==8.0.2", "numpy==2.3.5", "pytest"])
        self.assertEqual(profiles["attached_files/task_3/"]["packages"], ["Django", "pytest"])

    def test_total_input_limit_and_failed_upload_never_run_task_code(self) -> None:
        source = self.task_inputs()
        second = source.parent / "second.py"
        second.write_bytes(b"x = 20\n")
        Path(os.environ["DSH_E2B_TASK_FILE"]).write_text(json.dumps({"resolved_attached_files": [str(source), str(second)]}), encoding="utf-8")
        os.environ["DSH_E2B_MAX_INPUT_TOTAL_BYTES"] = "10"
        self.assertTrue(self.call("execute_python", code="must_not_run")["isError"])
        self.assertEqual(FakeSandbox.instances[0].files.contents, {})
        os.environ["DSH_E2B_MAX_INPUT_TOTAL_BYTES"] = "100"
        self.adapter.environment = self.adapter.Environment()
        with patch.object(FakeSandbox.instances[0].files, "write", side_effect=RuntimeError("upload failed")):
            result = self.call("execute_python", code="must_not_run")
        self.assertTrue(result["isError"])
        self.assertIn("upload failed", result["content"][0]["text"])
        self.assertNotIn("must_not_run", FakeSandbox.instances[0].calls)


if __name__ == "__main__":
    unittest.main()
