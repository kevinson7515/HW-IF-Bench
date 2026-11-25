#!/usr/bin/env bash
# 本地 / 登录节点运行 DSH 的环境变量模板
# 使用方式：复制为 scripts/env.local.sh（不要提交到 git）并填入你的网关与密钥覆盖项，
# 或直接通过 .secrets/ 目录下的单行密钥文件自动加载。

# 1. 模型提供方选择：company-deepseek（默认）| company-glm | pangu | pangu92b
export DSH_MODEL_PROVIDER="${DSH_MODEL_PROVIDER:-company-deepseek}"

# 2. 各模型 API_KEY 与 BASE_URL（导出环境变量的优先级高于 .secrets/ 文件）
# 注意：run.sh 默认将 COMPANY_DEEPSEEK_BASE_URL 设为 https://api.deepseek.com/v1，
# 若你使用的是公司内网/中转网关（如 http://115.120.87.159:8082/v1），请务必显式导出 BASE_URL！
# export COMPANY_DEEPSEEK_BASE_URL="https://api.deepseek.com/v1"
# export COMPANY_DEEPSEEK_API_KEY="sk-..."

# export COMPANY_GLM_BASE_URL="http://115.120.87.159:8082/v1"
# export COMPANY_GLM_API_KEY="..."

# export PANGU_BASE_URL="http://101.245.71.190:9080/v1"
# export PANGU_API_KEY="..."

# 3. 联网检索（Serper）与代码沙箱（E2B）
# 默认读取 .secrets/serper-api-key 与 .secrets/e2b-api-key；也可在此直接导出覆盖：
export SERPER_BASE_URL="${SERPER_BASE_URL:-https://yibuapi.com}"
export SERPER_AUTH_MODE="${SERPER_AUTH_MODE:-auto}" # 可选: auto | bearer | x-api-key
# export SERPER_API_KEY="..."
# export E2B_API_KEY="..."

# 4. 代理与内网直连设置
# run_naq_baseline_local.sh 默认将 DSH_HTTP_PROXY 设为空字符串（直连，不用原集群 174.0.250.13:3128）。
# 若当前节点需要临时走本地替代代理端口，改为填入你的代理地址即可：
export DSH_HTTP_PROXY=""
# export DSH_HTTP_PROXY="http://127.0.0.1:7890"
# 若走代理且公司模型网关是内网地址不走代理，设成 1：
# export DSH_COMPANY_API_NO_PROXY=1

# 5. 基线运行行为开关
export DSH_SIM_USER="${DSH_SIM_USER:-0}"           # 0=纯单轮基线（不调 Qwen 模拟用户）；1=启用模拟用户
export DSH_QUERY_CHECK="${DSH_QUERY_CHECK:-1}"     # 启动前先校对题目数和附件
export DSH_EXPECTED_TASKS="${DSH_EXPECTED_TASKS:-48}"

