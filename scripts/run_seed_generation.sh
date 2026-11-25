#!/usr/bin/env bash
# 一键启动 HW-IF-Bench 工作流种子库全套约束生成流水线
#
# 用法示例：
#   1. 全量 98 题（老 50 + 新 48 = 588 变体）开启 LLM 增强生成（推荐）：
#      bash scripts/run_seed_generation.sh --with-llm
#
#   2. 先用 5 题做 30 秒 LLM 冒烟测试：
#      bash scripts/run_seed_generation.sh --with-llm --limit 5
#
#   3. 纯离线确定性秒级生成（不调 LLM API）：
#      bash scripts/run_seed_generation.sh --no-llm
#
#   4. 换用 deepseek-v4-pro 模型做 LLM 增强（默认 deepseek-v4.1-flash-1017 更快更省）：
#      SEED_LLM_MODEL="deepseek-v4-pro" bash scripts/run_seed_generation.sh --with-llm
#
#   5. 对任意外部新 Query JSONL 一键生成约束数据集：
#      bash scripts/run_seed_generation.sh --input-jsonl /path/to/queries.jsonl --with-llm

set -Eeuo pipefail

BENCH_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"

# 自动加载本地环境变量（网关、API Key、代理配置），与基线脚本保持完全一致
if [[ -f "$BENCH_ROOT/scripts/env.local.sh" ]]; then
  # shellcheck source=/dev/null
  source "$BENCH_ROOT/scripts/env.local.sh"
fi

export SEED_LLM_MODEL="${SEED_LLM_MODEL:-deepseek-v4.1-flash-1017}"

PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! "$PYTHON_BIN" -c "import yaml" >/dev/null 2>&1; then
  if [[ -x "$HOME/.conda/envs/dsh/bin/python" ]]; then
    PYTHON_BIN="$HOME/.conda/envs/dsh/bin/python"
  fi
fi

exec "$PYTHON_BIN" "$BENCH_ROOT/seed_pipeline/run_seed_generator.py" "$@"

