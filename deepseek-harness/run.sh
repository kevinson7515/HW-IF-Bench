#!/usr/bin/env bash

# Cluster prerequisites and tool configuration: scripts/batch-tools.README.md.

#SBATCH --job-name=deepseek-harness
#SBATCH --output=/home/export/base/ycsc_chenkh/hitici_07/online1/deepseek-harness/dsh_%j.out
#SBATCH --error=/home/export/base/ycsc_chenkh/hitici_07/online1/deepseek-harness/dsh_%j.out
#SBATCH --partition=q_amd_gpu_nvidia_A100_chenkh
#SBATCH --gres=gpu:1
#SBATCH --nodes=1
#SBATCH --ntasks=1

set -Eeuo pipefail
umask 077

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >&2
}

die() {
  log "ERROR: $*"
  exit 1
}

trap 'status=$?; log "batch runner stopped at line ${LINENO} with status ${status}"; exit "${status}"' ERR

WORK="${WORK:-/home/export/base/ycsc_chenkh/hitici_07/online1}"
BATCH_MODE="${DSH_BATCH_MODE:-queries}"
[[ "$BATCH_MODE" == queries || "$BATCH_MODE" == benchmark ]] || die "DSH_BATCH_MODE must be queries or benchmark"
CONTAINER_IMAGE="${DSH_CONTAINER_IMAGE:-/online1/hpc_containers/base_hpc_glibc_235.sif}"
CONDA_ROOT="${DSH_CONDA_ROOT:-$WORK/anaconda3}"
CONDA_ENV="${DSH_CONDA_ENV:-$CONDA_ROOT/envs/dsh}"

if [[ "${DSH_INSIDE_CONTAINER:-0}" == 1 ]]; then
  [[ -n "${DSH_REPO_ROOT:-}" ]] || die "DSH_REPO_ROOT was not passed into the container"
  [[ -n "${DSH_SCRIPT_PATH:-}" ]] || die "DSH_SCRIPT_PATH was not passed into the container"
  REPO_ROOT="$DSH_REPO_ROOT"
  SCRIPT_PATH="$DSH_SCRIPT_PATH"
elif [[ -n "${SLURM_JOB_ID:-}" ]]; then
  # sbatch runs a private spool copy such as
  # /var/log/slurm/job123/slurm_script. That path is not visible inside the
  # container, so re-enter through the submitted repository copy instead.
  [[ -n "${SLURM_SUBMIT_DIR:-}" ]] || die "SLURM_SUBMIT_DIR is missing"
  REPO_ROOT="$(readlink -f -- "${DSH_REPO_ROOT:-$SLURM_SUBMIT_DIR}")"
  SCRIPT_PATH="$(readlink -f -- "${DSH_SCRIPT_PATH:-$REPO_ROOT/run.sh}")"
else
  SCRIPT_PATH="$(readlink -f -- "${BASH_SOURCE[0]}")"
  REPO_ROOT="$(cd -- "$(dirname -- "$SCRIPT_PATH")" && pwd -P)"
fi

[[ -r "$SCRIPT_PATH" ]] || die "repository script is not readable: $SCRIPT_PATH"

# Re-enter this same script non-interactively inside Singularity. Slurm ignores
# the #SBATCH lines on this second invocation.
if [[ "${DSH_INSIDE_CONTAINER:-0}" != 1 ]]; then
  if ! type module >/dev/null 2>&1; then
    [[ -r /etc/profile.d/modules.sh ]] || die "the environment-modules initialization script was not found"
    # shellcheck source=/dev/null
    source /etc/profile.d/modules.sh
  fi

  module load amd/gcc_compiler/13.2.0
  module load amd/singularity/3.10.4
  command -v singularity >/dev/null 2>&1 || die "singularity was not added to PATH"
  [[ -r "$CONTAINER_IMAGE" ]] || die "container image is not readable: $CONTAINER_IMAGE"

  export SINGULARITYENV_DSH_INSIDE_CONTAINER=1
  export SINGULARITYENV_DSH_REPO_ROOT="$REPO_ROOT"
  export SINGULARITYENV_DSH_SCRIPT_PATH="$SCRIPT_PATH"
  export SINGULARITYENV_DSH_MODEL_PROVIDER="${DSH_MODEL_PROVIDER:-company-deepseek}"
  export SINGULARITYENV_DSH_BATCH_MODE="$BATCH_MODE"
  log "entering Singularity through repository script: $SCRIPT_PATH"
  exec singularity exec --nv \
    -B /online1/hpc_containers/conda/ \
    -B /online1/ycsc_chenkh/hitici_07 \
    -B "$WORK:$WORK" \
    --pwd "$REPO_ROOT" \
    "$CONTAINER_IMAGE" \
    /bin/bash "$SCRIPT_PATH" "$@"
fi

[[ -r "$CONDA_ROOT/etc/profile.d/conda.sh" ]] || die "conda initialization script is not readable under $CONDA_ROOT"
set +u
# shellcheck source=/dev/null
source "$CONDA_ROOT/etc/profile.d/conda.sh"
conda activate "$CONDA_ENV"
set -u
hash -r

command -v node >/dev/null 2>&1 || die "node is not available after activating $CONDA_ENV"
command -v pnpm >/dev/null 2>&1 || die "pnpm is not available after activating $CONDA_ENV"
command -v python >/dev/null 2>&1 || die "python is not available after activating $CONDA_ENV"
command -v flock >/dev/null 2>&1 || die "flock is required to isolate workspace artifact recording"
command -v sha256sum >/dev/null 2>&1 || die "sha256sum is required to identify the repository lock"

export DSH_HOME="${DSH_HOME:-$WORK/.dsh}"
export DSH_TELEMETRY_DISABLED="${DSH_TELEMETRY_DISABLED:-1}"
export NPM_CONFIG_CACHE="${NPM_CONFIG_CACHE:-$WORK/.cache/npm}"
export PNPM_STORE_DIR="${PNPM_STORE_DIR:-$WORK/.cache/pnpm/store}"
[[ "${DSH_TOOLS_MODE:-native}" == native ]] || die "E2B batches require DSH_TOOLS_MODE=native"
export DSH_TOOLS_MODE=native

LOCK_ROOT="${DSH_LOCK_ROOT:-$WORK/.locks}"
mkdir -p "$LOCK_ROOT"
chmod 700 "$LOCK_ROOT"
repo_lock_id="$(printf '%s' "$REPO_ROOT" | sha256sum)"
repo_lock_id="${repo_lock_id%% *}"
exec 9>"$LOCK_ROOT/deepseek-harness-$repo_lock_id.lock"
if [[ "$BATCH_MODE" == benchmark ]]; then
  log "waiting for exclusive benchmark access to repository $REPO_ROOT"
  flock 9
else
  flock -n 9 || die "another batch job is already using repository $REPO_ROOT"
fi
export DSH_BENCHMARK_JOURNAL="$LOCK_ROOT/deepseek-harness-$repo_lock_id.benchmark-pending.json"
export DSH_BENCHMARK_LOCK_FILE="$LOCK_ROOT/deepseek-harness-$repo_lock_id.lock"
[[ ! -e "$DSH_BENCHMARK_JOURNAL" ]] || die "a benchmark workspace needs recovery; see $DSH_BENCHMARK_JOURNAL before starting another job"

proxy_url="${DSH_HTTP_PROXY-http://174.0.250.13:3128}"
if [[ -n "$proxy_url" ]]; then
  export http_proxy="$proxy_url"
  export https_proxy="$proxy_url"
  export HTTP_PROXY="$proxy_url"
  export HTTPS_PROXY="$proxy_url"
  export NODE_USE_ENV_PROXY="${NODE_USE_ENV_PROXY:-1}"
else
  unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY E2B_PROXY || true
  export NODE_USE_ENV_PROXY=0
fi

load_secret() {
  local variable_name="$1"
  local secret_file="$2"
  local key_owner key_mode secret_value

  if [[ -n "${!variable_name:-}" ]]; then
    return
  fi
  [[ -f "$secret_file" && -r "$secret_file" ]] || die "set $variable_name or create the protected key file $secret_file"
  key_owner="$(stat -c '%u' "$secret_file")"
  key_mode="$(stat -c '%a' "$secret_file")"
  [[ "$key_owner" == "$(id -u)" ]] || die "secret file is not owned by the current user: $secret_file"
  (( (8#$key_mode & 077) == 0 )) || die "secret file must not grant group or other permissions: chmod 600 $secret_file"
  secret_value="$(<"$secret_file")"
  # Accept a single key line saved by Windows editors without forwarding CR/BOM bytes.
  secret_value="${secret_value#$'\xef\xbb\xbf'}"
  secret_value="${secret_value%$'\r'}"
  [[ -n "$secret_value" ]] || die "secret file is empty: $secret_file"
  [[ "$secret_value" != *$'\r'* && "$secret_value" != *$'\n'* ]] || die "secret file must contain exactly one key line: $secret_file"
  printf -v "$variable_name" '%s' "$secret_value"
  export "$variable_name"
}

load_pangu92b_credentials() {
  if [[ -n "${PANGU92B_API_KEY:-}" && -n "${PANGU92B_HW_ID:-}" && -n "${PANGU92B_APP_KEY:-}" ]]; then
    export PANGU92B_API_KEY PANGU92B_HW_ID PANGU92B_APP_KEY
    return
  fi
  local secret_file="${DSH_API_KEY_FILE:-$WORK/.secrets/pangu92b-api-key.yml}"
  local key_owner key_mode credentials
  local -a fields
  [[ -f "$secret_file" && -r "$secret_file" ]] || die "export all PANGU92B credentials or create the protected credential file $secret_file"
  key_owner="$(stat -c '%u' "$secret_file")"
  key_mode="$(stat -c '%a' "$secret_file")"
  [[ "$key_owner" == "$(id -u)" ]] || die "secret file is not owned by the current user: $secret_file"
  (( (8#$key_mode & 077) == 0 )) || die "secret file must not grant group or other permissions: chmod 600 $secret_file"
  # JSON is a YAML subset and needs no additional parser in the Conda environment.
  credentials="$(python - "$secret_file" <<'PY'
import json
import os
import sys

try:
    with open(sys.argv[1], encoding="utf-8-sig") as source:
        bundle = json.load(source)
    if not isinstance(bundle, dict):
        raise ValueError("expected an object")
    values = [os.environ.get(variable) or bundle.get(field) for variable, field in (
        ("PANGU92B_API_KEY", "api_key"), ("PANGU92B_HW_ID", "hw_id"), ("PANGU92B_APP_KEY", "hw_app_key"),
    )]
    if any(not isinstance(value, str) or not value.strip() or any(ord(c) < 32 or ord(c) > 126 for c in value) for value in values):
        raise ValueError("expected nonempty single-line ASCII credentials")
except (OSError, ValueError):
    print("Pangu92B credentials must be a JSON-compatible YAML object with api_key, hw_id, and hw_app_key; credential values are not logged", file=sys.stderr)
    sys.exit(1)
print("\n".join(values))
PY
  )" || die "invalid Pangu92B credential file: $secret_file"
  credentials="${credentials//$'\r'/}"
  mapfile -t fields <<<"$credentials"
  export PANGU92B_API_KEY="${fields[0]}"
  export PANGU92B_HW_ID="${fields[1]}"
  export PANGU92B_APP_KEY="${fields[2]}"
}

# Slurm jobs have no interactive terminal. Read credentials from owner-only
# files unless the submitter explicitly exported them with --export.
MODEL_PROVIDER="${DSH_MODEL_PROVIDER:-company-deepseek}"
export DSH_MODEL_PROVIDER="$MODEL_PROVIDER"
no_proxy_additions="localhost,127.0.0.1"
case "$MODEL_PROVIDER" in
  company-deepseek)
    export COMPANY_DEEPSEEK_BASE_URL="${COMPANY_DEEPSEEK_BASE_URL:-https://api.deepseek.com/v1}"
    company_host="${COMPANY_DEEPSEEK_BASE_URL#*://}"
    company_host="${company_host%%/*}"
    company_host="${company_host%%:*}"
    if [[ "${DSH_COMPANY_API_NO_PROXY:-0}" == 1 ]]; then
      no_proxy_additions="$no_proxy_additions,$company_host"
    fi
    if [[ "$COMPANY_DEEPSEEK_BASE_URL" == http://* ]]; then
      log "WARNING: the company API uses unencrypted HTTP; the bearer token is not protected in transit"
    fi
    load_secret COMPANY_DEEPSEEK_API_KEY "${DSH_API_KEY_FILE:-$WORK/.secrets/deepseek-api-key}"
    PATCH_FILE="${DSH_PATCH_FILE:-$WORK/dsh-config/deepseek.patch.yml}"
    ;;
  company-glm)
    export COMPANY_GLM_BASE_URL="${COMPANY_GLM_BASE_URL:-http://115.120.87.159:8082/v1}"
    company_host="${COMPANY_GLM_BASE_URL#*://}"
    company_host="${company_host%%/*}"
    company_host="${company_host%%:*}"
    if [[ "${DSH_COMPANY_API_NO_PROXY:-0}" == 1 ]]; then
      no_proxy_additions="$no_proxy_additions,$company_host"
    fi
    if [[ "$COMPANY_GLM_BASE_URL" == http://* ]]; then
      log "WARNING: the company API uses unencrypted HTTP; the bearer token is not protected in transit"
    fi
    load_secret COMPANY_GLM_API_KEY "${DSH_API_KEY_FILE:-$WORK/.secrets/glm-api-key}"
    PATCH_FILE="${DSH_PATCH_FILE:-$WORK/dsh-config/glm.patch.yml}"
    ;;
  pangu)
    export PANGU_BASE_URL="${PANGU_BASE_URL:-http://101.245.71.190:9080/v1}"
    export PANGU_CONTEXT_WINDOW="${PANGU_CONTEXT_WINDOW:-524288}"
    export PANGU_MAX_TOKENS="${PANGU_MAX_TOKENS:-32768}"
    export PANGU_COMPACTION_HEADROOM_TOKENS="${PANGU_COMPACTION_HEADROOM_TOKENS:-4096}"
    export PANGU_COMPACTION_MAX_TOKENS="${PANGU_COMPACTION_MAX_TOKENS:-2048}"
    [[ "$PANGU_CONTEXT_WINDOW" =~ ^[1-9][0-9]*$ ]] || die "PANGU_CONTEXT_WINDOW must be a positive integer"
    [[ "$PANGU_MAX_TOKENS" =~ ^[1-9][0-9]*$ ]] || die "PANGU_MAX_TOKENS must be a positive integer"
    [[ "$PANGU_COMPACTION_HEADROOM_TOKENS" =~ ^(0|[1-9][0-9]*)$ ]] || die "PANGU_COMPACTION_HEADROOM_TOKENS must be a non-negative integer"
    [[ "$PANGU_COMPACTION_MAX_TOKENS" =~ ^[1-9][0-9]*$ ]] || die "PANGU_COMPACTION_MAX_TOKENS must be a positive integer"
    (( PANGU_MAX_TOKENS < PANGU_CONTEXT_WINDOW )) || die "PANGU_MAX_TOKENS must be smaller than PANGU_CONTEXT_WINDOW"
    (( PANGU_MAX_TOKENS + PANGU_COMPACTION_HEADROOM_TOKENS < PANGU_CONTEXT_WINDOW )) || die "PANGU_MAX_TOKENS plus PANGU_COMPACTION_HEADROOM_TOKENS must be smaller than PANGU_CONTEXT_WINDOW"
    if [[ "$PANGU_BASE_URL" == http://* ]]; then
      log "WARNING: the Pangu API uses unencrypted HTTP; credentials are not protected in transit"
    fi
    load_secret PANGU_API_KEY "${DSH_API_KEY_FILE:-${DSH_PANGU_API_KEY_FILE:-$WORK/.secrets/pangu-api-key}}"
    if [[ "${DSH_COMPANY_API_NO_PROXY:-0}" == 1 ]]; then
      pangu_host="${PANGU_BASE_URL#*://}"
      pangu_host="${pangu_host%%/*}"
      pangu_host="${pangu_host%%:*}"
      no_proxy_additions="$no_proxy_additions,$pangu_host"
    fi
    PATCH_FILE="${DSH_PATCH_FILE:-$WORK/dsh-config/pangu.patch.yml}"
    ;;
  pangu92b)
    export PANGU92B_BASE_URL="${PANGU92B_BASE_URL:-https://apigw-dgg-b0.huawei.com/api/pangu/v1}"
    export PANGU92B_CONTEXT_WINDOW="${PANGU92B_CONTEXT_WINDOW:-262144}"
    export PANGU92B_MAX_TOKENS="${PANGU92B_MAX_TOKENS:-32768}"
    export PANGU92B_COMPACTION_HEADROOM_TOKENS="${PANGU92B_COMPACTION_HEADROOM_TOKENS:-4096}"
    export PANGU92B_COMPACTION_MAX_TOKENS="${PANGU92B_COMPACTION_MAX_TOKENS:-2048}"
    [[ "$PANGU92B_CONTEXT_WINDOW" =~ ^[1-9][0-9]*$ ]] || die "PANGU92B_CONTEXT_WINDOW must be a positive integer"
    [[ "$PANGU92B_MAX_TOKENS" =~ ^[1-9][0-9]*$ ]] || die "PANGU92B_MAX_TOKENS must be a positive integer"
    [[ "$PANGU92B_COMPACTION_HEADROOM_TOKENS" =~ ^(0|[1-9][0-9]*)$ ]] || die "PANGU92B_COMPACTION_HEADROOM_TOKENS must be a non-negative integer"
    [[ "$PANGU92B_COMPACTION_MAX_TOKENS" =~ ^[1-9][0-9]*$ ]] || die "PANGU92B_COMPACTION_MAX_TOKENS must be a positive integer"
    (( PANGU92B_MAX_TOKENS + PANGU92B_COMPACTION_HEADROOM_TOKENS < PANGU92B_CONTEXT_WINDOW )) || die "PANGU92B_MAX_TOKENS plus PANGU92B_COMPACTION_HEADROOM_TOKENS must be smaller than PANGU92B_CONTEXT_WINDOW"
    load_pangu92b_credentials
    if [[ "${DSH_COMPANY_API_NO_PROXY:-0}" == 1 ]]; then
      pangu_host="${PANGU92B_BASE_URL#*://}"
      pangu_host="${pangu_host%%/*}"
      pangu_host="${pangu_host%%:*}"
      no_proxy_additions="$no_proxy_additions,$pangu_host"
    fi
    if [[ "$PANGU92B_BASE_URL" == http://* ]]; then
      log "WARNING: the Pangu92B API uses unencrypted HTTP; credentials are not protected in transit"
    fi
    PATCH_FILE="${DSH_PATCH_FILE:-$WORK/dsh-config/pangu92b.patch.yml}"
    ;;
  *) die "DSH_MODEL_PROVIDER must be company-deepseek, company-glm, pangu, or pangu92b: $MODEL_PROVIDER" ;;
esac
if [[ "$MODEL_PROVIDER" == pangu || "$MODEL_PROVIDER" == pangu92b ]]; then
    export COMPANY_DEEPSEEK_BASE_URL="${COMPANY_DEEPSEEK_BASE_URL:-https://api.deepseek.com/v1}"
    company_host="${COMPANY_DEEPSEEK_BASE_URL#*://}"
    company_host="${company_host%%/*}"
    company_host="${company_host%%:*}"
    if [[ "${DSH_COMPANY_API_NO_PROXY:-0}" == 1 ]]; then
      no_proxy_additions="$no_proxy_additions,$company_host"
    fi
    if [[ "$COMPANY_DEEPSEEK_BASE_URL" == http://* ]]; then
      log "WARNING: the company vision API uses unencrypted HTTP; the bearer token and image bytes are not protected in transit"
    fi
    load_secret COMPANY_DEEPSEEK_API_KEY "${DSH_VISION_API_KEY_FILE:-$WORK/.secrets/deepseek-api-key}"
    if [[ -z "${SSL_CERT_FILE:-}" || ! -f "$SSL_CERT_FILE" || ! -r "$SSL_CERT_FILE" ]]; then
      if [[ -n "${SSL_CERT_FILE:-}" ]]; then
        log "WARNING: inherited SSL_CERT_FILE is not readable inside Singularity; using Conda certifi"
      fi
      SSL_CERT_FILE="$(python -c 'import certifi; print(certifi.where())')" || die "could not locate the Conda certifi CA bundle"
    fi
    [[ -f "$SSL_CERT_FILE" && -r "$SSL_CERT_FILE" ]] || die "Pangu CA bundle is not readable: $SSL_CERT_FILE"
    export SSL_CERT_FILE
fi
export no_proxy="${no_proxy:+$no_proxy,}$no_proxy_additions"
export NO_PROXY="${NO_PROXY:+$NO_PROXY,}$no_proxy_additions"

load_secret SERPER_API_KEY "${DSH_SERPER_API_KEY_FILE:-$WORK/.secrets/serper-api-key}"
load_secret E2B_API_KEY "${DSH_E2B_API_KEY_FILE:-$WORK/.secrets/e2b-api-key}"
[[ "${DSH_SIM_USER:-0}" == 0 || "${DSH_SIM_USER:-0}" == 1 ]] || die "DSH_SIM_USER must be 0 or 1"
if [[ "${DSH_SIM_USER:-0}" == 1 ]]; then
  load_secret DSH_SIM_USER_API_KEY "${DSH_SIM_USER_KEY_FILE:-$WORK/.secrets/qwen-api-key}"
  log "simulated user enabled: synthetic dialogue only; no real user authorization or business simulation"
fi

export SERPER_BASE_URL="${SERPER_BASE_URL:-https://yibuapi.com}"
export SERPER_AUTH_MODE="${SERPER_AUTH_MODE:-auto}"
e2b_proxy="${E2B_PROXY-$proxy_url}"
export E2B_PROXY="${e2b_proxy}"
export DSH_E2B_PROJECTS_FILE="${DSH_E2B_PROJECTS_FILE:-$REPO_ROOT/scripts/config/e2b-projects.json}"
[[ -r "$DSH_E2B_PROJECTS_FILE" ]] || die "E2B project configuration is not readable: $DSH_E2B_PROJECTS_FILE"

python -c 'import certifi, e2b_code_interpreter' || die \
  "E2B Python dependencies are missing; install e2b-code-interpreter and certifi in $CONDA_ENV"

TOOLS_PATCH_FILE="${DSH_TOOLS_PATCH_FILE:-$REPO_ROOT/batch-tools.patch.yml}"
INPUT_JSONL="${1:-${DSH_INPUT_JSONL:-$REPO_ROOT/user_query.jsonl}}"
RUN_ROOT="${DSH_RUN_ROOT:-$WORK/dsh-runs}"
BATCH_ID="${DSH_BATCH_ID:-user_query-${SLURM_JOB_ID:-$(date '+%Y%m%d-%H%M%S')}}"

[[ "$BATCH_ID" =~ ^[A-Za-z0-9._-]+$ && "$BATCH_ID" != . && "$BATCH_ID" != .. ]] || die "DSH_BATCH_ID must be a filename-safe batch name other than . or .."
[[ -r "$PATCH_FILE" ]] || die "provider patch is not readable: $PATCH_FILE"
[[ -r "$TOOLS_PATCH_FILE" ]] || die "batch tools patch is not readable: $TOOLS_PATCH_FILE"
[[ -r "$INPUT_JSONL" ]] || die "input JSONL is not readable: $INPUT_JSONL"
[[ -f "$REPO_ROOT/package.json" ]] || die "repository root does not contain package.json: $REPO_ROOT"
if [[ "$BATCH_MODE" == queries && "${DSH_QUERY_CHECK:-0}" == 1 ]]; then
  python "$REPO_ROOT/scripts/check-user-queries.py" "$INPUT_JSONL" --expected-count "${DSH_EXPECTED_TASKS:-70}"
fi

mkdir -p "$DSH_HOME" "$NPM_CONFIG_CACHE" "$PNPM_STORE_DIR" "$RUN_ROOT/$BATCH_ID"
chmod 700 "$RUN_ROOT/$BATCH_ID"
cd "$REPO_ROOT"

log "repository: $REPO_ROOT"
log "provider:   $MODEL_PROVIDER"
log "patch:      $PATCH_FILE"
if [[ "$MODEL_PROVIDER" == pangu ]]; then
  log "pangu:      openPangu-v21-pro at $PANGU_BASE_URL; context=$PANGU_CONTEXT_WINDOW output=$PANGU_MAX_TOKENS compaction-headroom=$PANGU_COMPACTION_HEADROOM_TOKENS"
elif [[ "$MODEL_PROVIDER" == pangu92b ]]; then
  log "pangu92b:   pangu92b_wandr at $PANGU92B_BASE_URL; context=$PANGU92B_CONTEXT_WINDOW output=$PANGU92B_MAX_TOKENS compaction-headroom=$PANGU92B_COMPACTION_HEADROOM_TOKENS"
fi
if [[ "$MODEL_PROVIDER" == pangu || "$MODEL_PROVIDER" == pangu92b ]]; then
  log "vision:     ${DSH_VISION_MODEL:-deepseek-v4-pro} via company API"
fi
log "input:      $INPUT_JSONL"
log "records:    $RUN_ROOT/$BATCH_ID"
log "node:       $(node --version)"
log "pnpm:       $(pnpm --version)"
log "serper:     $SERPER_BASE_URL/serper/{search,images}"
log "e2b:        official service"
log "validating composed headless configuration"

export DSH_BATCH_REPO_ROOT="$REPO_ROOT"
export DSH_BATCH_INPUT_JSONL="$INPUT_JSONL"
export DSH_BATCH_PATCH_FILE="$PATCH_FILE"
export DSH_BATCH_TOOLS_PATCH_FILE="$TOOLS_PATCH_FILE"
export DSH_BATCH_OUTPUT_DIR="$RUN_ROOT/$BATCH_ID"
export DSH_BATCH_PYTHON="$(command -v python)"
pnpm dsh --profile headless --patch "$PATCH_FILE" --patch "$TOOLS_PATCH_FILE" --dump-config >/dev/null
if [[ "$BATCH_MODE" == benchmark ]]; then
  log "benchmark:  preserve harness system prompt; archive then restore each variant"
  exec python "$REPO_ROOT/scripts/run-benchmark.py"
fi

python - <<'PY'
from __future__ import annotations

import json
import hashlib
import os
import re
import signal
import shutil
import stat
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, TextIO


repo_root = Path(os.environ["DSH_BATCH_REPO_ROOT"])
sys.path.insert(0, str(repo_root / "scripts"))
from dsh_simulated_user import simulated_user_patch
input_path = Path(os.environ["DSH_BATCH_INPUT_JSONL"])
patch_path = Path(os.environ["DSH_BATCH_PATCH_FILE"])
tools_patch_path = Path(os.environ["DSH_BATCH_TOOLS_PATCH_FILE"])
batch_dir = Path(os.environ["DSH_BATCH_OUTPUT_DIR"])
summary_path = batch_dir / "results.jsonl"
attachment_root = input_path.resolve().parent
repo_root_resolved = repo_root.resolve()
session_root = Path(os.environ["DSH_HOME"]) / "sessions"


def positive_limit(name: str, default: int) -> int:
    raw_value = os.environ.get(name, str(default))
    try:
        value = int(raw_value)
    except ValueError as error:
        raise SystemExit(f"{name} must be an integer") from error
    if value <= 0:
        raise SystemExit(f"{name} must be greater than zero")
    return value


artifact_max_file_bytes = positive_limit("DSH_ARTIFACT_MAX_FILE_BYTES", 100 * 1024 * 1024)
artifact_max_total_bytes = positive_limit("DSH_ARTIFACT_MAX_TOTAL_BYTES", 1024 * 1024 * 1024)
allow_external_attachments = os.environ.get("DSH_ALLOW_EXTERNAL_ATTACHMENTS", "0") == "1"

try:
    batch_relative = batch_dir.resolve().relative_to(repo_root_resolved)
except ValueError:
    batch_relative = None

current_process: subprocess.Popen[bytes] | None = None
interrupted_signal: int | None = None


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(path: Path, value: object) -> None:
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    with temporary.open("w", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.chmod(temporary, 0o600)
    os.replace(temporary, path)


def append_result(stream: TextIO, value: object) -> None:
    json.dump(value, stream, ensure_ascii=False, separators=(",", ":"))
    stream.write("\n")
    stream.flush()
    os.fsync(stream.fileno())


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def excluded_workspace_path(relative: Path) -> bool:
    if any(part in {".git", "node_modules"} for part in relative.parts):
        return True
    if batch_relative is not None:
        batch_parts = batch_relative.parts
        if relative.parts[: len(batch_parts)] == batch_parts:
            return True
    return False


def snapshot_workspace() -> dict[str, tuple[int, int]]:
    snapshot: dict[str, tuple[int, int]] = {}
    for directory, child_directories, file_names in os.walk(repo_root_resolved, followlinks=False):
        directory_path = Path(directory)
        kept_directories: list[str] = []
        for name in child_directories:
            relative = (directory_path / name).relative_to(repo_root_resolved)
            if excluded_workspace_path(relative) or (directory_path / name).is_symlink():
                continue
            kept_directories.append(name)
        child_directories[:] = kept_directories

        for name in file_names:
            path = directory_path / name
            relative = path.relative_to(repo_root_resolved)
            if excluded_workspace_path(relative):
                continue
            try:
                metadata = path.lstat()
            except FileNotFoundError:
                continue
            if stat.S_ISREG(metadata.st_mode):
                snapshot[relative.as_posix()] = (metadata.st_size, metadata.st_mtime_ns)
    return snapshot


def archive_attachments(task_dir: Path, attachments: list[Path]) -> list[dict[str, object]]:
    archived: list[dict[str, object]] = []
    input_dir = task_dir / "inputs"
    for index, source in enumerate(attachments, start=1):
        try:
            relative = source.relative_to(attachment_root)
        except ValueError:
            relative = Path(f"external-{index}") / source.name
        destination = input_dir / relative
        destination.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        shutil.copy2(source, destination, follow_symlinks=False)
        os.chmod(destination, 0o600)
        archived.append(
            {
                "source": str(source),
                "copy": str(destination),
                "size": destination.stat().st_size,
                "sha256": sha256_file(destination),
            }
        )
    if archived:
        write_json(input_dir / "manifest.json", archived)
    return archived


def archive_workspace_changes(
    task_dir: Path,
    before: dict[str, tuple[int, int]],
    after: dict[str, tuple[int, int]],
) -> dict[str, object]:
    created = sorted(after.keys() - before.keys())
    deleted = sorted(before.keys() - after.keys())
    modified = sorted(path for path in before.keys() & after.keys() if before[path] != after[path])
    artifact_dir = task_dir / "artifacts"
    copied: list[dict[str, object]] = []
    skipped_files: list[dict[str, object]] = []
    errors: list[dict[str, str]] = []
    copied_bytes = 0

    for relative_text in created + modified:
        source = repo_root_resolved / Path(relative_text)
        expected_size = after[relative_text][0]
        if expected_size > artifact_max_file_bytes:
            skipped_files.append(
                {"path": relative_text, "reason": "file_limit", "size": expected_size}
            )
            continue
        if copied_bytes + expected_size > artifact_max_total_bytes:
            skipped_files.append(
                {"path": relative_text, "reason": "task_total_limit", "size": expected_size}
            )
            continue

        destination = artifact_dir / Path(relative_text)
        try:
            destination.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            shutil.copy2(source, destination, follow_symlinks=False)
            os.chmod(destination, 0o600)
            copied_size = destination.stat().st_size
            copied_bytes += copied_size
            copied.append(
                {
                    "path": relative_text,
                    "copy": str(destination),
                    "change": "created" if relative_text in created else "modified",
                    "size": copied_size,
                    "sha256": sha256_file(destination),
                }
            )
        except OSError as error:
            errors.append({"path": relative_text, "error": str(error)})

    status = "complete" if not skipped_files and not errors else "partial"
    manifest: dict[str, object] = {
        "status": status,
        "scope": str(repo_root_resolved),
        "detection": "regular-file size and nanosecond mtime before and after the task",
        "created": created,
        "modified": modified,
        "deleted": deleted,
        "copied": copied,
        "skipped": skipped_files,
        "errors": errors,
        "limits": {
            "max_file_bytes": artifact_max_file_bytes,
            "max_total_bytes": artifact_max_total_bytes,
        },
    }
    write_json(task_dir / "artifacts.json", manifest)
    return manifest


def archive_session_record(task_dir: Path, session_id: str | None) -> dict[str, object]:
    copied: list[dict[str, object]] = []
    errors: list[dict[str, str]] = []
    matches: list[Path] = []
    if session_id is not None and session_root.exists():
        for directory, child_directories, _file_names in os.walk(session_root, followlinks=False):
            directory_path = Path(directory)
            child_directories[:] = [
                name for name in child_directories if not (directory_path / name).is_symlink()
            ]
            if directory_path.name == session_id:
                matches.append(directory_path)
                child_directories[:] = []

    if session_id is None:
        errors.append({"path": str(session_root), "error": "the run reported no session id"})
    elif len(matches) != 1:
        errors.append(
            {
                "path": str(session_root),
                "error": f"expected one directory for session {session_id!r}, found {len(matches)}",
            }
        )
    else:
        source_root = matches[0]
        destination_root = task_dir / "session-records"
        for directory, child_directories, file_names in os.walk(source_root, followlinks=False):
            directory_path = Path(directory)
            child_directories[:] = [
                name for name in child_directories if not (directory_path / name).is_symlink()
            ]
            for name in file_names:
                source = directory_path / name
                try:
                    metadata = source.lstat()
                    if not stat.S_ISREG(metadata.st_mode):
                        continue
                    relative = source.relative_to(source_root)
                    destination = destination_root / relative
                    destination.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
                    shutil.copy2(source, destination, follow_symlinks=False)
                    os.chmod(destination, 0o600)
                    copied.append(
                        {
                            "path": relative.as_posix(),
                            "copy": str(destination),
                            "size": destination.stat().st_size,
                            "sha256": sha256_file(destination),
                        }
                    )
                except OSError as error:
                    errors.append({"path": str(source), "error": str(error)})

    manifest: dict[str, object] = {
        "status": "complete" if not errors else "partial",
        "session_id": session_id,
        "source": str(matches[0]) if len(matches) == 1 else None,
        "copied": copied,
        "errors": errors,
    }
    write_json(task_dir / "session-records.json", manifest)
    return manifest


def safe_id(value: object) -> str:
    if isinstance(value, (str, int, float)) and not isinstance(value, bool):
        text = str(value)
    else:
        text = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    sanitized = re.sub(r"[^A-Za-z0-9._-]+", "_", text).strip("._-")
    return (sanitized or "no-id")[:80]


def read_projection(path: Path) -> tuple[bool, str, str | None, str | None]:
    final_seen = False
    final_text = ""
    session_id: str | None = None
    parse_error: str | None = None
    try:
        with path.open("r", encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, start=1):
                if not line.strip():
                    continue
                try:
                    event = json.loads(line)
                except json.JSONDecodeError as error:
                    parse_error = f"invalid trace JSON on line {line_number}: {error}"
                    continue
                if event.get("type") == "session" and isinstance(event.get("sessionId"), str):
                    session_id = event["sessionId"]
                if event.get("type") == "final" and isinstance(event.get("text"), str):
                    final_seen = True
                    final_text = event["text"]
    except OSError as error:
        parse_error = f"could not read trace: {error}"
    return final_seen, final_text, session_id, parse_error


def write_chat_trace(path: Path, destination: Path, user_content: str) -> None:
    messages: list[dict[str, object]] = [
        {"role": "system", "content": ""},
        {"role": "user", "content": user_content},
    ]
    pending_content: list[str] = []
    pending_reasoning: list[str] = []
    pending_tool_calls: list[dict[str, object]] = []
    final_text: str | None = None

    def flush_assistant() -> None:
        if not pending_content and not pending_reasoning and not pending_tool_calls:
            return
        message: dict[str, object] = {
            "role": "assistant",
            "content": "".join(pending_content),
            "weight": 1,
        }
        if pending_reasoning:
            message["reasoning_content"] = "".join(pending_reasoning)
        if pending_tool_calls:
            message["tool_calls"] = list(pending_tool_calls)
        messages.append(message)
        pending_content.clear()
        pending_reasoning.clear()
        pending_tool_calls.clear()

    with path.open("r", encoding="utf-8") as stream:
        for line in stream:
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            event_type = event.get("type")
            if event_type == "thinking" and isinstance(event.get("text"), str):
                pending_reasoning.append(event["text"])
            elif event_type == "text" and isinstance(event.get("text"), str):
                pending_content.append(event["text"])
            elif event_type == "tool_call":
                call_id = event.get("callId")
                tool_name = event.get("tool")
                if isinstance(call_id, str) and isinstance(tool_name, str):
                    arguments = event.get("input", {})
                    arguments_text = (
                        arguments
                        if isinstance(arguments, str)
                        else json.dumps(arguments, ensure_ascii=False, separators=(",", ":"))
                    )
                    pending_tool_calls.append(
                        {
                            "id": call_id,
                            "type": "function",
                            "function": {
                                "name": tool_name,
                                "arguments": arguments_text,
                            },
                        }
                    )
            elif event_type == "tool_result":
                flush_assistant()
                call_id = event.get("callId")
                result = event.get("result", "")
                if isinstance(call_id, str):
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": call_id,
                            "content": result if isinstance(result, str) else json.dumps(result, ensure_ascii=False),
                        }
                    )
            elif event_type == "simulated_user":
                flush_assistant()
                messages.append({"role": "user", "content": event["text"], "simulated": True,
                                 "model": event["model"], "message_id": event["messageId"]})
            elif event_type == "status" and event.get("phase") == "step_end":
                flush_assistant()
            elif event_type == "final" and isinstance(event.get("text"), str):
                final_text = event["text"]
    flush_assistant()
    if final_text:
        for message in reversed(messages):
            if message.get("role") == "assistant" and "tool_calls" not in message:
                message["content"] = final_text
                break
    write_json(
        destination,
        {
            "format": "openai-chat-like-projection",
            "source": str(path),
            "lossless": False,
            "trace": messages,
        },
    )


def stop_current_process(signum: int, _frame: Any) -> None:
    global interrupted_signal
    interrupted_signal = signum
    process = current_process
    if process is None or process.poll() is not None:
        return
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass


signal.signal(signal.SIGTERM, stop_current_process)
signal.signal(signal.SIGINT, stop_current_process)

total = 0
succeeded = 0
failed = 0
skipped = 0
recording_issues = 0

with input_path.open("r", encoding="utf-8-sig") as input_stream, summary_path.open(
    "a", encoding="utf-8", newline="\n"
) as summary_stream:
    os.chmod(summary_path, 0o600)
    for line_number, raw_line in enumerate(input_stream, start=1):
        if interrupted_signal is not None:
            break
        if not raw_line.strip():
            continue

        total += 1
        try:
            record = json.loads(raw_line)
            if not isinstance(record, dict):
                raise ValueError("record must be a JSON object")
            task_id = record.get("id", line_number)
            user_query = record.get("user_query")
            if not isinstance(user_query, str) or not user_query.strip():
                raise ValueError("user_query must be a non-empty string")
            attached_files = record.get("attached_files", [])
            if not isinstance(attached_files, list):
                raise ValueError("attached_files must be an array of paths")
            attachment_paths: list[Path] = []
            for attached_file in attached_files:
                if not isinstance(attached_file, str) or not attached_file.strip():
                    raise ValueError("each attached_files entry must be a non-empty string")
                candidate = Path(attached_file)
                if not candidate.is_absolute():
                    candidate = attachment_root / candidate
                resolved_attachment = candidate.resolve(strict=True)
                if not resolved_attachment.is_file():
                    raise ValueError(f"attachment is not a regular file: {attached_file}")
                if not allow_external_attachments and not resolved_attachment.is_relative_to(attachment_root):
                    raise ValueError(
                        f"attachment leaves the input directory: {attached_file}; "
                        "set DSH_ALLOW_EXTERNAL_ATTACHMENTS=1 to allow it"
                    )
                attachment_paths.append(resolved_attachment)
        except (json.JSONDecodeError, OSError, ValueError) as error:
            failed += 1
            append_result(
                summary_stream,
                {
                    "line": line_number,
                    "status": "invalid_input",
                    "error": str(error),
                    "finished_at": utc_now(),
                },
            )
            print(f"[batch] line {line_number}: invalid input: {error}", file=sys.stderr, flush=True)
            continue

        task_dir = batch_dir / f"{line_number:06d}-{safe_id(task_id)}"
        task_dir.mkdir(mode=0o700, parents=False, exist_ok=True)
        os.chmod(task_dir, 0o700)
        result_path = task_dir / "result.json"

        if result_path.exists():
            try:
                previous = json.loads(result_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                previous = None
            if isinstance(previous, dict) and previous.get("status") == "succeeded":
                skipped += 1
                previous_recording_status = previous.get("recording_status")
                if previous_recording_status != "complete":
                    recording_issues += 1
                append_result(
                    summary_stream,
                    {
                        "line": line_number,
                        "id": task_id,
                        "status": "skipped_succeeded",
                        "recording_status": previous_recording_status,
                        "task_dir": str(task_dir),
                        "finished_at": utc_now(),
                    },
                )
                print(f"[batch] line {line_number}, id={task_id!r}: already succeeded; skipped", flush=True)
                continue

        archived_attachments = archive_attachments(task_dir, attachment_paths)
        effective_query = user_query
        if attachment_paths:
            attachment_lines = "\n".join(f"- {path}" for path in attachment_paths)
            effective_query += (
                "\n\nAttached files are available at the following paths. Read them as needed:\n"
                f"{attachment_lines}"
            )
        trace_path = task_dir / "trace.jsonl"
        diagnostics_path = task_dir / "diagnostics.log"
        final_path = task_dir / "final.txt"
        started_at = utc_now()
        started_monotonic = time.monotonic()

        write_json(
            task_dir / "task.json",
            {
                "line": line_number,
                "id": task_id,
                "user_query": user_query,
                "effective_query": effective_query,
                "attached_files": attached_files,
                "resolved_attached_files": [str(path) for path in attachment_paths],
                "archived_attachments": archived_attachments,
                "started_at": started_at,
            },
        )

        print(f"[batch] line {line_number}, id={task_id!r}: starting", flush=True)
        before_snapshot = snapshot_workspace()
        command = [
            "pnpm",
            "--silent",
            "dsh",
            "--profile",
            "headless",
            "--patch",
            str(patch_path),
            "--patch",
            str(tools_patch_path),
        ]
        for simulated_patch in simulated_user_patch(repo_root, task_dir):
            command.extend(("--patch", str(simulated_patch)))
        command.extend(("--json", "-"))

        return_code: int
        launch_error: str | None = None
        try:
            with trace_path.open("wb") as trace_stream, diagnostics_path.open("wb") as diagnostics_stream:
                current_process = subprocess.Popen(
                    command,
                    cwd=repo_root,
                    env={**os.environ, "DSH_E2B_TASK_FILE": str(task_dir / "task.json")},
                    stdin=subprocess.PIPE,
                    stdout=trace_stream,
                    stderr=diagnostics_stream,
                    start_new_session=True,
                )
                current_process.communicate(effective_query.encode("utf-8"))
                return_code = current_process.returncode
        except OSError as error:
            return_code = 127
            launch_error = f"could not launch dsh: {error}"
            diagnostics_path.write_text(launch_error + "\n", encoding="utf-8")
        finally:
            current_process = None

        try:
            after_snapshot = snapshot_workspace()
            artifact_manifest = archive_workspace_changes(task_dir, before_snapshot, after_snapshot)
        except OSError as error:
            artifact_manifest = {
                "status": "failed",
                "scope": str(repo_root_resolved),
                "errors": [{"error": str(error)}],
            }
            write_json(task_dir / "artifacts.json", artifact_manifest)

        final_seen, final_text, session_id, trace_error = read_projection(trace_path)
        session_manifest = archive_session_record(task_dir, session_id)
        write_chat_trace(trace_path, task_dir / "trace.json", effective_query)
        final_path.write_text(final_text, encoding="utf-8", newline="\n")
        os.chmod(final_path, 0o600)

        finished_at = utc_now()
        status = "succeeded" if return_code == 0 and final_seen and trace_error is None else "failed"
        recording_status = (
            "complete"
            if artifact_manifest["status"] == "complete" and session_manifest["status"] == "complete"
            else "partial"
        )
        result = {
            "line": line_number,
            "id": task_id,
            "status": status,
            "exit_code": return_code,
            "session_id": session_id,
            "final_event_seen": final_seen,
            "started_at": started_at,
            "finished_at": finished_at,
            "duration_seconds": round(time.monotonic() - started_monotonic, 3),
            "task_dir": str(task_dir),
            "trace_events": str(trace_path),
            "trace": str(task_dir / "trace.json"),
            "diagnostics": str(diagnostics_path),
            "final": str(final_path),
            "artifacts": str(task_dir / "artifacts.json"),
            "session_records": str(task_dir / "session-records.json"),
            "recording_status": recording_status,
            **({"error": launch_error} if launch_error is not None else {}),
            **({"trace_error": trace_error} if trace_error is not None else {}),
        }
        write_json(result_path, result)
        append_result(summary_stream, result)

        if status == "succeeded":
            succeeded += 1
        else:
            failed += 1
        if recording_status != "complete":
            recording_issues += 1
        print(
            f"[batch] line {line_number}, id={task_id!r}: {status} "
            f"(exit={return_code}, recording={recording_status}, dir={task_dir})",
            flush=True,
        )

summary = {
    "status": "interrupted" if interrupted_signal is not None else ("failed" if failed or recording_issues else "succeeded"),
    "total": total,
    "succeeded": succeeded,
    "failed": failed,
    "skipped": skipped,
    "recording_issues": recording_issues,
    "signal": interrupted_signal,
    "finished_at": utc_now(),
    "results": str(summary_path),
}
write_json(batch_dir / "summary.json", summary)
print(f"[batch] summary: {json.dumps(summary, ensure_ascii=False)}", flush=True)

if interrupted_signal is not None:
    raise SystemExit(128 + interrupted_signal)
raise SystemExit(1 if failed or recording_issues else 0)
PY

log "batch completed successfully"
