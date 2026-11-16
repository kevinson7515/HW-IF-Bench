"""Compose the opt-in simulated-user overlay without changing provider or benchmark prompts."""

from __future__ import annotations

import json
import os
from pathlib import Path


def simulated_user_patch(root: Path, task_dir: Path) -> list[Path]:
    """Return a per-task overlay, or no overlays when simulation is disabled."""
    enabled = os.environ.get("DSH_SIM_USER", "0")
    if enabled not in ("0", "1"):
        raise ValueError("DSH_SIM_USER must be 0 or 1")
    if enabled == "0":
        return []
    if not os.environ.get("DSH_SIM_USER_API_KEY"):
        raise ValueError("DSH_SIM_USER=1 requires DSH_SIM_USER_API_KEY")
    config_file = Path(os.environ.get("DSH_SIM_USER_CONFIG", root / "scripts/config/simulated-user.json"))
    configuration = json.loads(config_file.read_text(encoding="utf-8-sig"))
    if not isinstance(configuration, dict) or set(configuration) - {
        "baseURL", "model", "timeoutMs", "maxTokens", "maxReplies", "maxRequests", "maxResponseBytes", "maxInputChars",
    }:
        raise ValueError("invalid simulated-user configuration fields; credentials belong in the environment")
    entries = [{"id": "batch-tool-ask-user", "name": (root / "packages/interaction/tool-ask-user/src/index.ts").as_uri()},
               {"id": "batch-simulated-user", "name": (root / "scripts/simulated-user.mjs").as_uri(), "config": configuration}]
    path = task_dir / "simulated-user.patch.json"
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump([{"insert": entries}], stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    path.chmod(0o600)
    return [path]
