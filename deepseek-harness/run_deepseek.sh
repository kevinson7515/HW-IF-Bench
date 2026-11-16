#!/usr/bin/env bash
#SBATCH --job-name=deepseek-benchmark
#SBATCH --output=dsh_deepseek_%j.out
#SBATCH --error=dsh_deepseek_%j.out
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
export DSH_MODEL_PROVIDER=company-deepseek
export DSH_PATCH_FILE="${DSH_PATCH_FILE:-$WORK/dsh-config/deepseek.patch.yml}"
export DSH_API_KEY_FILE="${DSH_API_KEY_FILE:-$WORK/.secrets/deepseek-api-key}"
export DSH_BATCH_MODE=benchmark
export DSH_BATCH_ID="${DSH_BATCH_ID:-benchmark-deepseek-${SLURM_JOB_ID:-$(date '+%Y%m%d-%H%M%S')}}"
exec /bin/bash "$DSH_SCRIPT_PATH" "${1:-$repo_root/benchmark_groups.json}"
