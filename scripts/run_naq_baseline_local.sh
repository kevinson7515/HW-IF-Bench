#!/usr/bin/env bash
# 直接在登录节点 / 无 GPU 无 Slurm 环境下跑 naq_50 无约束基线轨迹的启动脚本
# 用法：
#   bash scripts/run_naq_baseline_local.sh [输入JSONL路径]
# 示例：
#   DSH_HTTP_PROXY="http://127.0.0.1:你的端口" bash scripts/run_naq_baseline_local.sh

set -Eeuo pipefail

BENCH_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
DSH_DIR="$BENCH_ROOT/deepseek-harness"
INPUT_JSONL="${1:-$BENCH_ROOT/naq_50/user_query_naq50.jsonl}"
if [[ "$INPUT_JSONL" != /* ]]; then
  INPUT_JSONL="$(readlink -f -- "$INPUT_JSONL")"
fi

# 如果存在本地覆盖配置 scripts/env.local.sh，自动加载
if [[ -f "$BENCH_ROOT/scripts/env.local.sh" ]]; then
  # shellcheck source=/dev/null
  source "$BENCH_ROOT/scripts/env.local.sh"
fi

# 当前节点默认直连外网，不强制走集群旧代理 174.0.250.13:3128（如需临时端口可在 env.local.sh 中覆盖）
export DSH_HTTP_PROXY="${DSH_HTTP_PROXY-}"

# 绕过 run.sh 里的 module load + Singularity 容器重入逻辑，直接在当前节点运行
export DSH_INSIDE_CONTAINER=1
export DSH_REPO_ROOT="$DSH_DIR"
export DSH_SCRIPT_PATH="$DSH_DIR/run.sh"

# 目录隔离：运行产物放在项目根目录下已忽略的 dsh-runs/（且位于 deepseek-harness 工作区外），锁与状态目录放 $HOME
export WORK="${WORK:-$HOME}"
export DSH_HOME="${DSH_HOME:-$HOME/.dsh}"
export DSH_RUN_ROOT="${DSH_RUN_ROOT:-$BENCH_ROOT/dsh-runs}"
export DSH_LOCK_ROOT="${DSH_LOCK_ROOT:-$HOME/.dsh-locks}"
export DSH_CONDA_ROOT="${DSH_CONDA_ROOT:-$HOME/anaconda3}"
if [[ -z "${DSH_CONDA_ENV:-}" ]]; then
  if [[ -n "${CONDA_PREFIX:-}" && "$(basename -- "$CONDA_PREFIX")" == "dsh" && -d "$CONDA_PREFIX" ]]; then
    DSH_CONDA_ENV="$CONDA_PREFIX"
  elif [[ -d "$HOME/.conda/envs/dsh" ]]; then
    DSH_CONDA_ENV="$HOME/.conda/envs/dsh"
  else
    DSH_CONDA_ENV="$DSH_CONDA_ROOT/envs/dsh"
  fi
fi
export DSH_CONDA_ENV

# 绑定仓库内的配置补丁与密钥文件路径
export DSH_MODEL_PROVIDER="${DSH_MODEL_PROVIDER:-company-deepseek}"
case "$DSH_MODEL_PROVIDER" in
  company-deepseek) default_patch="$BENCH_ROOT/dsh-config/deepseek.patch.yml"; default_key="$BENCH_ROOT/.secrets/deepseek-api-key" ;;
  company-glm)      default_patch="$BENCH_ROOT/dsh-config/glm.patch.yml";      default_key="$BENCH_ROOT/.secrets/glm-api-key" ;;
  pangu)            default_patch="$BENCH_ROOT/dsh-config/pangu.patch.yml";    default_key="$BENCH_ROOT/.secrets/pangu-api-key" ;;
  pangu92b)         default_patch="$BENCH_ROOT/dsh-config/pangu92b.patch.yml"; default_key="$BENCH_ROOT/.secrets/pangu92b-api-key.yml" ;;
  *) echo "ERROR: 不支持的 DSH_MODEL_PROVIDER=$DSH_MODEL_PROVIDER" >&2; exit 1 ;;
esac

export DSH_PATCH_FILE="${DSH_PATCH_FILE:-$default_patch}"
export DSH_API_KEY_FILE="${DSH_API_KEY_FILE:-$default_key}"
export DSH_SERPER_API_KEY_FILE="${DSH_SERPER_API_KEY_FILE:-$BENCH_ROOT/.secrets/serper-api-key}"
export DSH_E2B_API_KEY_FILE="${DSH_E2B_API_KEY_FILE:-$BENCH_ROOT/.secrets/e2b-api-key}"
export DSH_SIM_USER_KEY_FILE="${DSH_SIM_USER_KEY_FILE:-$BENCH_ROOT/.secrets/qwen-api-key}"

export DSH_BATCH_MODE=queries
export DSH_SIM_USER="${DSH_SIM_USER:-0}"
export DSH_QUERY_CHECK="${DSH_QUERY_CHECK:-1}"
export DSH_EXPECTED_TASKS="${DSH_EXPECTED_TASKS:-48}"
export DSH_BATCH_ID="${DSH_BATCH_ID:-naq_48_${DSH_MODEL_PROVIDER}-$(date '+%Y%m%d-%H%M%S')}"

# ---- 启动前本地环境预检（先报错、不烧 API 额度） ----
missing=0
if [[ ! -d "$DSH_CONDA_ENV" ]]; then
  echo "[MISSING] Conda 环境不存在: $DSH_CONDA_ENV" >&2
  echo "          需要创建一个带 python>=3.10、nodejs>=22.19、pnpm、e2b-code-interpreter、certifi 的 dsh 环境。" >&2
  missing=1
fi
if [[ ! -d "$DSH_DIR/node_modules" ]]; then
  echo "[MISSING] 尚未安装 Node 依赖: $DSH_DIR/node_modules" >&2
  echo "          需先在 deepseek-harness/ 目录执行 pnpm install 并构建。" >&2
  missing=1
fi
for sf in "$DSH_API_KEY_FILE" "$DSH_SERPER_API_KEY_FILE" "$DSH_E2B_API_KEY_FILE"; do
  if [[ -f "$sf" ]]; then
    perm="$(stat -c '%a' "$sf")"
    if [[ "$perm" != "600" && "$perm" != "400" ]]; then
      echo "[WARN] 密钥文件权限过于宽松 ($perm): $sf -> run.sh 要求 chmod 600" >&2
      missing=1
    fi
  fi
done
if [[ "$missing" -ne 0 ]]; then
  echo "预检未通过，请先按提示补齐环境/权限后重试。" >&2
  exit 1
fi

echo "[INFO] 使用输入文件: $INPUT_JSONL (期望 $DSH_EXPECTED_TASKS 题)"
echo "[INFO] 输出目录:     $DSH_RUN_ROOT/$DSH_BATCH_ID"
exec /bin/bash "$DSH_SCRIPT_PATH" "$INPUT_JSONL"

