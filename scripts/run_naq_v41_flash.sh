#!/usr/bin/env bash
# 使用模型 deepseek-v4.1-flash-1017 重新运行 naq_50 无约束基线（独立输出目录，不覆盖 v4-pro 结果）
# 用法：
#   全量 48 题：bash scripts/run_naq_v41_flash.sh
#   断点续跑：  DSH_BATCH_ID=naq_48_deepseek-v4.1-flash-1017-YYYYMMDD-HHMMSS bash scripts/run_naq_v41_flash.sh
#   单题试跑：  DSH_EXPECTED_TASKS=1 bash scripts/run_naq_v41_flash.sh naq_50/test1.jsonl

set -Eeuo pipefail

BENCH_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
export DSH_MODEL_PROVIDER="company-deepseek"
export DSH_PATCH_FILE="${DSH_PATCH_FILE:-$BENCH_ROOT/scripts/deepseek-v4.1-flash-1017.patch.yml}"
export DSH_BATCH_ID="${DSH_BATCH_ID:-naq_48_deepseek-v4.1-flash-1017-$(date '+%Y%m%d-%H%M%S')}"

# 默认优先 IPv4，避免部分站点 DNS 解析出 IPv6 触发 EAFNOSUPPORT 崩溃
export NODE_OPTIONS="${NODE_OPTIONS:+$NODE_OPTIONS }--dns-result-order=ipv4first"

exec /bin/bash "$BENCH_ROOT/scripts/run_naq_baseline_local.sh" "$@"

