"""Synchronize task-owned inputs and prepare explicitly configured E2B dependencies."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shlex
import stat
from pathlib import Path, PurePosixPath
from typing import Any


class Environment:
    """One MCP process owns its dependency preparation and partial-failure state."""

    def __init__(self) -> None:
        self.initialized = False
        self.dependencies: dict[str, Any] | None = None
        self.failure: str | None = None
        self.dependency_signature: str | None = None

    def prepare(self, sandbox: Any) -> dict[str, Any]:
        task_file = os.environ.get("DSH_E2B_TASK_FILE", "")
        if not task_file:
            return {"status": "not_configured", "files": [], "dependencies": None}
        if self.failure is not None:
            raise RuntimeError(self.failure)
        try:
            return self._prepare(sandbox, Path(task_file))
        except Exception as error:
            self.failure = f"E2B input/dependency preparation failed; task code was not run: {error}"
            raise RuntimeError(self.failure) from error

    def _prepare(self, sandbox: Any, task_file: Path) -> dict[str, Any]:
        root = Path(os.environ["DSH_E2B_EXPORT_ROOT"]).resolve(strict=True)
        task = json.loads(task_file.read_text(encoding="utf-8"))
        attachments = task.get("resolved_attached_files", [])
        if not isinstance(attachments, list) or not all(isinstance(path, str) for path in attachments):
            raise ValueError("task resolved_attached_files must be an array of file paths")
        paths = {self.safe_file(root, Path(path)) for path in attachments}
        profiles_file = os.environ.get("DSH_E2B_PROJECTS_FILE", "")
        profiles = []
        if profiles_file:
            profiles = json.loads(Path(profiles_file).read_text(encoding="utf-8")).get("projects")
            if not isinstance(profiles, list):
                raise ValueError("E2B project configuration must contain a projects array")
        selected = []
        for profile in profiles:
            if not isinstance(profile, dict):
                raise ValueError("E2B project entries must be objects")
            prefix = profile.get("attachment_prefix")
            if not isinstance(prefix, str) or not prefix or PurePosixPath(prefix).is_absolute() or ".." in PurePosixPath(prefix).parts or "\\" in prefix:
                raise ValueError("attachment_prefix must be a nonempty repository-relative path")
            prefix = prefix.rstrip("/") + "/"
            if any(path.relative_to(root).as_posix().startswith(prefix) for path in paths):
                selected.append(profile)
        packages: list[str] = []
        imports: list[str] = []
        requirements: list[Path] = []
        projects: list[Path] = []
        project_roots: list[Path] = []
        for profile in selected:
            specs = profile.get("packages", [])
            if not isinstance(specs, list) or not all(isinstance(spec, str) and spec and not spec.startswith("-") and not any(char in spec for char in "\r\n\x00") for spec in specs):
                raise ValueError("project packages must contain pip requirements, not options")
            packages.extend(specs)
            module_names = profile.get("imports", [])
            if not isinstance(module_names, list) or not all(isinstance(name, str) and re.fullmatch(r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*", name) for name in module_names):
                raise ValueError("project imports must contain dotted Python module names")
            imports.extend(module_names)
            names = profile.get("requirements_files", [])
            if not isinstance(names, list) or not all(isinstance(name, str) for name in names):
                raise ValueError("requirements_files must contain repository-relative file paths")
            for name in names:
                if Path(name).is_absolute():
                    raise ValueError("requirements_files must be repository-relative")
                source = self.safe_file(root, root / name)
                requirements.append(source)
                paths.add(source)
            directory = profile.get("project_dir")
            if not isinstance(profile.get("install_project", False), bool):
                raise ValueError("install_project must be a boolean")
            if profile.get("install_project", False) and directory is None:
                raise ValueError("install_project requires project_dir")
            if directory is not None:
                if not isinstance(directory, str) or Path(directory).is_absolute():
                    raise ValueError("project_dir must be a repository-relative directory")
                project = self.safe_path(root, root / directory)
                if not project.is_dir():
                    raise ValueError(f"project_dir is not a directory: {directory}")
                project_roots.append(project)
                # Full source synchronization is opt-in through operator-owned configuration.
                for parent, directories, files in os.walk(project, followlinks=False):
                    directories[:] = [name for name in directories if not self.excluded(name)]
                    if any((Path(parent) / name).is_symlink() for name in directories):
                        raise ValueError("project_dir may not contain symbolic-link directories")
                    for name in files:
                        if not self.excluded(name):
                            paths.add(self.safe_file(root, Path(parent) / name))
                if profile.get("install_project", False):
                    if not any((project / name).is_file() for name in ("pyproject.toml", "setup.py")):
                        raise ValueError("install_project requires pyproject.toml or setup.py; sparse attachments are not a full project")
                    projects.append(project)
        per_file = self.limit("DSH_E2B_MAX_INPUT_FILE_BYTES", 104857600)
        total_limit = self.limit("DSH_E2B_MAX_INPUT_TOTAL_BYTES", 268435456)
        total = 0
        contents = []
        for path in sorted(paths):
            descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
            with os.fdopen(descriptor, "rb") as incoming:
                if not stat.S_ISREG(os.fstat(incoming.fileno()).st_mode):
                    raise ValueError("E2B inputs must remain regular files")
                data = incoming.read(per_file + 1)
            total += len(data)
            if len(data) > per_file or total > total_limit:
                raise ValueError("E2B input size limit exceeded")
            contents.append((path, data, hashlib.sha256(data).hexdigest()))
        dependency_inputs = {str(path): sha for path, _data, sha in contents if path in requirements}
        signature = hashlib.sha256(json.dumps([packages, imports, dependency_inputs, [str(path) for path in projects], [str(path) for path in project_roots]], sort_keys=True).encode()).hexdigest()
        if self.dependency_signature is not None and signature != self.dependency_signature:
            raise ValueError("dependency configuration changed after preparation; restart this task to prepare a consistent environment")
        remote_root = root.as_posix() if os.name == "posix" else "/home/user/dsh-workspace"
        if contents and not self.initialized:
            if len(PurePosixPath(remote_root).parts) < 3 or remote_root.startswith(("/etc/", "/usr/", "/proc/", "/sys/")):
                raise ValueError("repository path cannot be mirrored into a reserved sandbox directory")
            command = shlex.join(["mkdir", "-p", remote_root]) + " && " + shlex.join(["chown", "user:user", remote_root])
            sandbox.commands.run(command, user="root")
            self.initialized = True
        files = []
        for path, data, sha in contents:
            remote = str(PurePosixPath(remote_root) / path.relative_to(root).as_posix())
            # The host attachments are authoritative; remote edits are not written back implicitly.
            sandbox.files.write(remote, data)
            files.append({"local_path": str(path), "remote_path": remote, "bytes": len(data), "sha256": sha})
        verify = {item["remote_path"]: item["sha256"] for item in files}
        argv = ["--disable-pip-version-check", *dict.fromkeys(packages)]
        for path in requirements:
            argv.extend(("-r", str(PurePosixPath(remote_root) / path.relative_to(root).as_posix())))
        for path in projects:
            argv.extend(("-e", str(PurePosixPath(remote_root) / path.relative_to(root).as_posix())))
        install = self.dependencies is None and bool(packages or requirements or projects)
        package_names = list(dict.fromkeys(re.split(r"[\[<>=!~ ;@]", spec, maxsplit=1)[0] for spec in packages))
        if contents or selected:
            setup_code = (
                "import os as _dsh_os, sys as _dsh_sys, json as _dsh_json, hashlib as _dsh_hashlib, subprocess as _dsh_subprocess\n"
                "from pathlib import Path as _dsh_Path\n"
                f"_dsh_inputs = {verify!r}\n"
                "for _dsh_path, _dsh_sha in _dsh_inputs.items():\n"
                "    if _dsh_hashlib.sha256(_dsh_Path(_dsh_path).read_bytes()).hexdigest() != _dsh_sha:\n"
                "        raise RuntimeError('E2B input digest mismatch: ' + _dsh_path)\n"
            )
            if self.dependencies is None:
                setup_code += f"_dsh_os.chdir({remote_root!r})\n"
                setup_code += f"_dsh_sys.path.insert(0, {remote_root!r})\n"
                for project in project_roots:
                    remote_project = str(PurePosixPath(remote_root) / project.relative_to(root).as_posix())
                    setup_code += f"_dsh_sys.path.insert(0, {remote_project!r})\n"
            if install:
                setup_code += f"_dsh_subprocess.run([_dsh_sys.executable, '-m', 'pip', 'install', *{argv!r}], check=True)\n"
            if self.dependencies is None:
                setup_code += (
                    "import importlib.metadata as _dsh_metadata, importlib as _dsh_importlib\n"
                    "_dsh_importlib.invalidate_caches()\n"
                    f"_dsh_names = {package_names!r}\n"
                    f"_dsh_modules = {{n: _dsh_importlib.import_module(n) for n in {list(dict.fromkeys(imports))!r}}}\n"
                    "_dsh_versions = {d.metadata['Name']: d.version for d in _dsh_metadata.distributions() if d.metadata['Name']}\n"
                    "_dsh_Path('.dsh-e2b-installed.json').write_text(_dsh_json.dumps(_dsh_versions, sort_keys=True))\n"
                    "for _dsh_path, _dsh_sha in _dsh_inputs.items():\n"
                    "    if _dsh_hashlib.sha256(_dsh_Path(_dsh_path).read_bytes()).hexdigest() != _dsh_sha:\n"
                    "        raise RuntimeError('E2B input changed during dependency preparation: ' + _dsh_path)\n"
                    "print('DSH_E2B_ENVIRONMENT=' + _dsh_json.dumps({'python': _dsh_sys.version, 'packages': {n: _dsh_metadata.version(n) for n in _dsh_names}, 'imports': {n: {'file': getattr(m, '__file__', None), 'version': getattr(m, '__version__', None)} for n,m in _dsh_modules.items()}, 'all_versions_file': str(_dsh_Path('.dsh-e2b-installed.json').resolve())}))\n"
                )
            result = sandbox.run_code(setup_code)
            if result.error is not None:
                raise RuntimeError(str(result.error))
            if self.dependencies is None:
                stdout = "".join(result.logs.stdout) if isinstance(result.logs.stdout, list) else result.logs.stdout
                marker = next((line for line in reversed(stdout.splitlines()) if line.startswith("DSH_E2B_ENVIRONMENT=")), None)
                if marker is None:
                    raise RuntimeError("dependency preparation returned no environment report")
                self.dependencies = json.loads(marker.split("=", 1)[1])
                self.dependency_signature = signature
        return {
            "status": "ready", "remote_root": remote_root, "files": files,
            "dependencies": self.dependencies, "profiles": [profile["attachment_prefix"] for profile in selected],
            "validation_scope": "Dependency availability only. Sparse attachments are not a full original project; importing an installed package does not validate edited attachments.",
        }

    @staticmethod
    def excluded(name: str) -> bool:
        return name.startswith(".") or name in {"node_modules", "__pycache__"} or name.endswith(("-api-key", "-api-kay", ".pem", ".key"))

    @classmethod
    def safe_path(cls, root: Path, path: Path) -> Path:
        absolute = Path(os.path.abspath(path))
        if not absolute.is_relative_to(root) or absolute == root:
            raise ValueError("E2B input must be inside the repository")
        if any(cls.excluded(part) for part in absolute.relative_to(root).parts):
            raise ValueError("E2B inputs may not include hidden, dependency, or credential paths")
        for parent in [absolute, *absolute.parents]:
            if parent == root:
                break
            if parent.is_symlink():
                raise ValueError("E2B inputs may not traverse symbolic links")
        resolved = absolute.resolve(strict=True)
        if resolved != absolute or not resolved.is_relative_to(root):
            raise ValueError("E2B inputs may not traverse filesystem links or leave the repository")
        return resolved

    @classmethod
    def safe_file(cls, root: Path, path: Path) -> Path:
        absolute = Path(os.path.abspath(path))
        if absolute.name == ".keep":
            cls.safe_path(root, absolute.parent)
            if absolute.is_symlink() or not absolute.is_file() or absolute.stat().st_size != 0:
                raise ValueError("E2B .keep placeholders must be empty regular files, not links")
            return absolute
        path = cls.safe_path(root, path)
        if not path.is_file():
            raise ValueError("E2B attachments must be regular files")
        return path

    @staticmethod
    def limit(name: str, default: int) -> int:
        value = os.environ.get(name, str(default))
        if not value.isdecimal() or int(value) < 1:
            raise ValueError(f"{name} must be a positive integer")
        return int(value)
