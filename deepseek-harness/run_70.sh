#!/usr/bin/env bash
#SBATCH --job-name=deepseek-70
#SBATCH --output=dsh_70_%j.out
#SBATCH --error=dsh_70_%j.out
#SBATCH --partition=q_amd_gpu_nvidia_A100_chenkh
#SBATCH --gres=gpu:1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --signal=B:TERM@120

set -Eeuo pipefail
export WORK="${WORK:-/home/export/base/ycsc_chenkh/hitici_07/online1}"
repo_root="${DSH_REPO_ROOT:-${SLURM_SUBMIT_DIR:-$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)}}"
export DSH_REPO_ROOT="$repo_root"
export DSH_SCRIPT_PATH="$repo_root/run.sh"
export DSH_MODEL_PROVIDER="${DSH_MODEL_PROVIDER:-company-deepseek}"
export DSH_BATCH_MODE=queries
export DSH_SIM_USER=1
export DSH_QUERY_CHECK=1
export DSH_EXPECTED_TASKS="${DSH_EXPECTED_TASKS:-70}"
export DSH_BATCH_ID="${DSH_BATCH_ID:-user_query_70-${SLURM_JOB_ID:-$(date '+%Y%m%d-%H%M%S')}}"
exec /bin/bash "$DSH_SCRIPT_PATH" "${1:-$repo_root/user_query_70.jsonl}"
