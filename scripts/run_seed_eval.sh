#!/usr/bin/env bash
# 一键在 deepseek-harness 上评测 588 条 Seed Pipeline 变体并支持断点续跑与自动打分
#
# 默认模型：deepseek-v4.1-flash-1017（可用 --model v4-pro 切换）
#
# 常用启动方式：
#   1. 1 题 6 变体快速验证注入闭环（约 3~5 分钟，强烈建议最先跑！）：
#      bash scripts/run_seed_eval.sh --mode smoke
#
#   2. 10 题分层 Pilot 实测（60 条变体，V1 5 题 + V2 5 题，约 2~3 小时）：
#      bash scripts/run_seed_eval.sh --mode pilot
#
#   3. 全量 98 题 588 条正式评估：
#      bash scripts/run_seed_eval.sh --mode full
#
#   4. 中断后断点续跑（传入上次的批次目录名）：
#      bash scripts/run_seed_eval.sh --mode full --resume eval_full_v41flash_20261125-193000
#
#   5. 切换模型为 deepseek-v4-pro：
#      bash scripts/run_seed_eval.sh --mode pilot --model v4-pro

set -Eeuo pipefail

BENCH_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
DSH_DIR="$BENCH_ROOT/deepseek-harness"

# 默认使用正式冻结的 98 题 588 变体评测集（也可用 --groups-file 覆盖）
DEFAULT_GROUPS="$BENCH_ROOT/benchmark/releases/hw_if_bench_v2_588/benchmark_groups_v2_588.json"

MODE="smoke"
MODEL="v4.1-flash"
GROUPS_FILE="$DEFAULT_GROUPS"
CUSTOM_GROUPS=""
CUSTOM_VARIANTS=""
RESUME_BATCH=""
CASE_TIMEOUT="900"
CHECK_ONLY="0"
AUTO_SCORE="1"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode)      MODE="$2"; shift 2 ;;
    --model)     MODEL="$2"; shift 2 ;;
    --groups-file) GROUPS_FILE="$2"; shift 2 ;;
    --groups)    CUSTOM_GROUPS="$2"; shift 2 ;;
    --variants)  CUSTOM_VARIANTS="$2"; shift 2 ;;
    --resume)    RESUME_BATCH="$2"; shift 2 ;;
    --timeout)   CASE_TIMEOUT="$2"; shift 2 ;;
    --check-only) CHECK_ONLY="1"; shift ;;
    --no-score)  AUTO_SCORE="0"; shift ;;
    *) echo "ERROR: 未知参数 $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$GROUPS_FILE" || ! -f "$GROUPS_FILE" ]]; then
  echo "ERROR: 找不到 benchmark_groups_seed_v1.json，请用 --groups-file 指定路径" >&2
  exit 1
fi
GROUPS_FILE="$(readlink -f -- "$GROUPS_FILE")"

# 加载本地环境变量（网关、Key、直连配置）
if [[ -f "$BENCH_ROOT/scripts/env.local.sh" ]]; then
  # shellcheck source=/dev/null
  source "$BENCH_ROOT/scripts/env.local.sh"
fi

# 1. 从统一主数据目录 benchmark/attached_files/ 同步 98 题全部附件（已加入 .gitignore，不污染 git）
echo "[eval] 同步 benchmark/attached_files/ 至 deepseek-harness/attached_files/ ..."
mkdir -p "$DSH_DIR/attached_files"
rsync -a "$BENCH_ROOT/benchmark/attached_files/" "$DSH_DIR/attached_files/"

# 2. 按模型选择 patch（均已统一收编在 dsh-config/）
export DSH_MODEL_PROVIDER="company-deepseek"
if [[ "$MODEL" == "v4.1-flash" || "$MODEL" == "deepseek-v4.1-flash-1017" ]]; then
  MODEL_TAG="v41flash"
  export DSH_PATCH_FILE="$BENCH_ROOT/dsh-config/deepseek-v4.1-flash-1017.patch.yml"
elif [[ "$MODEL" == "v4-pro" || "$MODEL" == "deepseek-v4-pro" ]]; then
  MODEL_TAG="v4pro"
  export DSH_PATCH_FILE="$BENCH_ROOT/dsh-config/deepseek.patch.yml"
else
  echo "ERROR: 不支持的 --model=$MODEL（可选：v4.1-flash | v4-pro）" >&2
  exit 1
fi

# 3. 选择评测范围（smoke=1题6条 | pilot=10题60条 | full=98题588条）
if [[ -n "$CUSTOM_GROUPS" ]]; then
  export DSH_BENCHMARK_GROUPS="$CUSTOM_GROUPS"
elif [[ "$MODE" == "smoke" ]]; then
  export DSH_BENCHMARK_GROUPS="G-travel-chinatravel-001"
elif [[ "$MODE" == "pilot" ]]; then
  # 10 道分层代表题：V1 5 题（SWE×2 / Legal / Finance / Customer）+ V2 5 题（ChinaTravel×2 / BrowseComp+ / DSQA×2）
  export DSH_BENCHMARK_GROUPS="G-coding-astropy-12891,G-swebench-verified-astropy__astropy-14182,G-legal-cb100-001,G-finance-3m-2019-2021-cfo-net-income,G-customer-airline-000,G-travel-chinatravel-001,G-travel-chinatravel-002,G-edu-browsecomp-001,G-culture-deepsearchqa-001,G-openweb-dsqa-386"
elif [[ "$MODE" == "full" ]]; then
  unset DSH_BENCHMARK_GROUPS || true
else
  echo "ERROR: 不支持的 --mode=$MODE（可选：smoke | pilot | full）" >&2
  exit 1
fi

if [[ -n "$CUSTOM_VARIANTS" ]]; then
  export DSH_BENCHMARK_VARIANTS="$CUSTOM_VARIANTS"
fi

# 4. 配置 DSH 运行参数（显式开启 System Prompt 与 Tier D 冲突注入 + 超时保护 + IPv4 优先）
export DSH_HTTP_PROXY="${DSH_HTTP_PROXY-}"
export NODE_OPTIONS="--dns-result-order=ipv4first ${NODE_OPTIONS:-}"
export DSH_INSIDE_CONTAINER=1
export DSH_REPO_ROOT="$DSH_DIR"
export DSH_SCRIPT_PATH="$DSH_DIR/run.sh"
export WORK="${WORK:-$HOME}"
export DSH_HOME="${DSH_HOME:-$HOME/.dsh}"
export DSH_RUN_ROOT="${DSH_RUN_ROOT:-$BENCH_ROOT/dsh-runs}"
export DSH_LOCK_ROOT="${DSH_LOCK_ROOT:-$HOME/.dsh-locks}"

if [[ -z "${DSH_CONDA_ENV:-}" ]]; then
  if [[ -d "$HOME/.conda/envs/dsh" ]]; then
    DSH_CONDA_ENV="$HOME/.conda/envs/dsh"
  else
    DSH_CONDA_ENV="$HOME/anaconda3/envs/dsh"
  fi
fi
export DSH_CONDA_ENV

export DSH_BATCH_MODE="benchmark"
export DSH_SIM_USER="${DSH_SIM_USER:-0}"
export DSH_APPLY_VARIANT_PROMPT="1"
export DSH_APPLY_USER_QUERY_APPEND="1"
export DSH_BENCHMARK_CASE_TIMEOUT_SECONDS="$CASE_TIMEOUT"
export DSH_API_KEY_FILE="${DSH_API_KEY_FILE:-$BENCH_ROOT/.secrets/deepseek-api-key}"
export DSH_SERPER_API_KEY_FILE="${DSH_SERPER_API_KEY_FILE:-$BENCH_ROOT/.secrets/serper-api-key}"
export DSH_E2B_API_KEY_FILE="${DSH_E2B_API_KEY_FILE:-$BENCH_ROOT/.secrets/e2b-api-key}"

if [[ -n "$RESUME_BATCH" ]]; then
  export DSH_BATCH_ID="$RESUME_BATCH"
  export DSH_BENCHMARK_RESUME="1"
else
  export DSH_BATCH_ID="eval_${MODE}_${MODEL_TAG}_$(date '+%Y%m%d-%H%M%S')"
  export DSH_BENCHMARK_RESUME="0"
fi

# 5. 启动前先做零成本静态预检（验证所有 98 题附件与 JSON schema 完整）
echo "[eval] 静态校验数据集与附件路径..."
(cd "$DSH_DIR" && "$DSH_CONDA_ENV/bin/python" "$DSH_DIR/scripts/run-benchmark.py" --check "$GROUPS_FILE" >/dev/null)
echo "[eval] 静态校验 PASS！"
if [[ "$CHECK_ONLY" == "1" ]]; then
  echo "[eval] --check-only 模式完成，未启动真实推理。"
  exit 0
fi

echo "[eval] 启动评估：mode=$MODE | model=$MODEL | batch_id=$DSH_BATCH_ID | timeout=${CASE_TIMEOUT}s"
echo "[eval] 输入数据集：$GROUPS_FILE"
echo "[eval] 产物目录：$DSH_RUN_ROOT/$DSH_BATCH_ID"

set +e
(cd "$DSH_DIR" && bash "$DSH_DIR/run.sh" "$GROUPS_FILE")
EVAL_RC=$?
set -e

RUN_OUT="$DSH_RUN_ROOT/$DSH_BATCH_ID"
if [[ "$AUTO_SCORE" == "1" && -f "$RUN_OUT/results.jsonl" ]]; then
  echo "[eval] 评估结束（exit=$EVAL_RC），自动运行确定性 IF 评分与报表生成..."
  python3 "$BENCH_ROOT/seed_pipeline/score_seed_runs.py" \
    --run-dir "$RUN_OUT" --groups "$GROUPS_FILE" || true
fi

exit "$EVAL_RC"
