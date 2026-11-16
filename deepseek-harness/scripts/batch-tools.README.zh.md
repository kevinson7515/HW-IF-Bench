# 集群批处理工具

[English](batch-tools.README.md) | 中文

## 概要

`run.sh` 可用公司 DeepSeek、GLM 或私有盘古接口执行无界面 JSONL 批处理任务。它通过 `batch-tools.patch.yml` 为 `web_search` 选择 Serper，并提供 E2B Python 执行和文件导出。盘古批处理还会获得 `mcp__vision__inspect_image`：它把已导出到仓库的图片交给公司 DeepSeek 接口，并将文字观察结果返回盘古。E2B 桥接器运行在 MCP 进程中；同一任务的多次调用共用一个 E2B 沙箱，任务结束时关闭。

## 模型提供方

默认的 `sbatch run.sh` 使用公司 DeepSeek 执行 `user_query.jsonl`。[基准测试指南](benchmark.README.zh.md#提交) 说明各模型专用评测入口。部署模板位于 `scripts/config/`，应放到 `$WORK/dsh-config/`，不要嵌入密钥。

| 提供方 | 模型 | `$WORK/dsh-config/` 下的补丁 | `$WORK/.secrets/` 下的密钥 |
|---|---|---|---|
| `company-deepseek`（默认） | `deepseek-v4-pro` | `deepseek.patch.yml` | `deepseek-api-key` |
| `company-glm` | `glm-5.3` | `glm.patch.yml` | `glm-api-key` |
| `pangu` | `openPangu-v21-pro` | `pangu.patch.yml` | `pangu-api-key` |
| `pangu92b` | `pangu92b_wandr` | `pangu92b.patch.yml` | `pangu92b-api-key.yml` |

DeepSeek 和 GLM 站点默认为 `http://115.120.87.159:8082/v1`，分别由 `COMPANY_DEEPSEEK_BASE_URL` 和 `COMPANY_GLM_BASE_URL` 覆盖。Pangu 默认为 `http://101.245.71.190:9080/v1`，由 `PANGU_BASE_URL` 覆盖。三个模型均使用 Chat Completions 和 Bearer 认证。密钥分别加载到 `COMPANY_DEEPSEEK_API_KEY`、`COMPANY_GLM_API_KEY` 或 `PANGU_API_KEY`，显式导出的值优先于文件。`DSH_API_KEY_FILE` 覆盖当前模型的密钥路径，`DSH_PATCH_FILE` 覆盖补丁。Pangu 不再读取硬件或应用凭据。视觉密钥独立读取 `deepseek-api-key` 或 `DSH_VISION_API_KEY_FILE`，不会误用 Pangu 的主密钥覆盖值。`DSH_COMPANY_API_NO_PROXY=1` 使当前 API 绕过 HTTP 代理；Pangu 模式也会让公司视觉 API 绕过代理。HTTP 站点不会加密密钥或任务内容。

Pangu 部署保留上下文 524,288 token、输出容量 32,768 token；这些数值尚未在新网关验证。如有需要，用 `PANGU_CONTEXT_WINDOW` 和 `PANGU_MAX_TOKENS` 覆盖为其支持的值。压缩保留 4,096 token 余量和 2,048 token 摘要上限，分别由 `PANGU_COMPACTION_HEADROOM_TOKENS` 和 `PANGU_COMPACTION_MAX_TOKENS` 控制。流等待超时不变。若 `SSL_CERT_FILE` 未设置或在 Singularity 内不可读，脚本为 Pangu 的 HTTPS 工具请求选择 Conda 环境中的 `certifi` CA 包；可读的自定义 CA 包会保留。

Pangu 在 `llm-pi-ai.config.providers.pangu` 下的 `retryPolicy` 使用有界的 `normal` 模式，首次请求后最多重试八次。本地退避从 10 秒开始倍增，每次最多等待 120 秒，并加入 10% 抖动：名义等待依次为 10、20、40、80、120、120、120、120 秒，不含请求耗时时合计约 10 分半。服务端重试等待提示可能按现有重试规则改变实际时间。耗尽次数后仍判定任务失败，取消作业仍可中断等待。默认的瞬时错误码集合（含 `RATE_LIMIT`）不变，鉴权及无效请求错误不会因此变成可重试错误。DeepSeek 和 GLM 保留原有策略。这不会提高网关额度，也不保证恢复。请将更新后的 `scripts/config/pangu.patch.yml` 复制到 `$WORK/dsh-config/pangu.patch.yml`；只修改仓库模板不会改变部署补丁。无需构建或修改启动脚本。

Pangu92B 使用独立的华为接口 `https://apigw-dgg-b0.huawei.com/api/pangu/v1`，可用 `PANGU92B_BASE_URL` 覆盖。其 `.yml` 凭据文件须使用 JSON 对象语法（YAML 的子集），包含非空、单行 ASCII 字符串 `api_key`、`hw_id` 和 `hw_app_key`。用 `chmod 600` 限制为仅所有者可访问；它不同于其他模型的原始单行密钥文件。加载器设置 `PANGU92B_API_KEY`、`PANGU92B_HW_ID` 和 `PANGU92B_APP_KEY`；导出变量优先于相应文件字段，三项均已导出时不读取文件。提供方发送 Bearer 认证及 `X-HW-ID`、`X-HW-AppKey`。不要公开解析后的配置，自定义请求头可能含凭据。默认设置上下文 262,144 token、输出 32,768 token、压缩余量 4,096 token、摘要 2,048 token；这些部署配置值并非已确认的私有模型上限；分别用 `PANGU92B_CONTEXT_WINDOW`、`PANGU92B_MAX_TOKENS`、`PANGU92B_COMPACTION_HEADROOM_TOKENS` 和 `PANGU92B_COMPACTION_MAX_TOKENS` 覆盖。请求超时及 harness 默认重试策略不变。它与 Pangu 一样使用 DeepSeek 视觉凭据及 certifi 回退；现有 `pangu` 提供方保持独立，不会新增华为认证头。

## 配置

在 `run.sh` 激活的 Conda 环境中安装 `e2b-code-interpreter` 和 `certifi`。Serper 与 E2B 默认分别使用仅所有者可访问的 `$WORK/.secrets/serper-api-key` 和 `$WORK/.secrets/e2b-api-key`。可用 `DSH_SERPER_API_KEY_FILE` 和 `DSH_E2B_API_KEY_FILE` 覆盖路径，或在提交前导出相应变量。密钥文件须包含一行非空内容；读取时会去除 Windows CRLF 和 UTF-8 BOM，内嵌换行会在调用 API 前被拒绝。脚本不会把密钥写入配置文件。

Serper 网关源地址默认为 `https://yibuapi.com`，文本搜索使用 `/serper/search`，图像搜索使用 `/serper/images`。`SERPER_BASE_URL` 可更换网关源地址；`SERPER_AUTH_MODE` 可设为 `bearer`、`x-api-key` 或默认的 `auto`。补丁会启用 `image_search`，同时保留现有搜索结果上限与超时设置；图像以链接形式返回，不下载字节。

E2B 使用官方服务和 `E2B_API_KEY`。`E2B_PROXY` 默认取批处理 HTTP 代理。适配器使用 `certifi` 设置 `SSL_CERT_FILE`，并沿用 SDK 的请求超时默认值；MCP 客户端保留自身配置的调用超时。它不会关闭证书校验，也不会把 Serper 网关用作 E2B 地址。

### E2B 附件与依赖

显式声明的空普通 `.keep` 文件是隐藏文件名的唯一例外。其父目录仍须通过普通输入检查；非空占位文件和符号链接会被拒绝。项目源码树发现仍跳过隐藏文件。

两个批处理运行器都通过 `DSH_E2B_TASK_FILE` 把当前任务已记录的 `task.json` 传给 E2B 桥接器。调用 `execute_python` 前，桥接器通过 E2B 的[文件接口](https://docs.e2b.dev/filesystem/read-write)上传清单中声明的附件及显式配置的项目源码，并在沙箱内校验 SHA-256。Linux 仓库路径映射为相同绝对路径；首次准备时，内核工作目录和导入路径设为镜像仓库。Windows 开发检查使用 `/home/user/dsh-workspace`，工具元数据会报告映射。本地附件为准，每次执行前重新复制，所以通过本地文件工具编辑后，下一次 E2B 调用能读到改动；仅在远端附件副本上的修改不会自动写回，下次同步会覆盖。现有导出工具仍不覆盖本地文件。隐藏路径、密钥、依赖目录、符号链接和仓库外路径均被拒绝。输入上限默认为单文件 100 MiB、合计 256 MiB（`DSH_E2B_MAX_INPUT_FILE_BYTES`、`DSH_E2B_MAX_INPUT_TOTAL_BYTES`）。

`DSH_E2B_PROJECTS_FILE` 默认为 `scripts/config/e2b-projects.json`。配置通过仓库相对的 `attachment_prefix` 匹配任务附件；`packages` 提供 pip 安装项，`imports` 提供必须能导入的模块。准备使用内核的 `sys.executable`，只在 E2B 内进行，每个任务一次。Astropy 配置使用记录中已知的兼容版本 `astropy==8.0.2`、`numpy==2.3.5` 及 pytest。Django 因原始版本不可得，安装未锁版本的 Django 和 pytest。两者均不重建历史项目基线。报告包含实际 Python、发行包版本、导入位置，以及远端记录全部发行包版本的 `.dsh-e2b-installed.json`。可调用 `mcp__e2b__prepare_environment` 在不执行任务代码的情况下检查报告；`execute_python` 的已记录结果也包含该信息。

若提供完整项目，可在配置中用仓库相对的 `project_dir` 同步非隐藏源码树，用 `requirements_files` 上传并安装显式依赖文件，用 `install_project: true` 以 editable 模式安装同步后的项目。项目安装要求存在 `pyproject.toml` 或 `setup.py`，不会把零散源码当成可安装项目。准备后若依赖配置或依赖文件变化，须启动新任务。若旧包需要其他 Python 版本，可用 `DSH_E2B_TEMPLATE` 选择预先准备的沙箱运行环境。上传、完整性校验、安装或声明模块导入失败时，任务代码不会运行，并明确报告错误；修复后请重启该任务。沙箱生命周期、SDK/MCP 超时、模型重试及评分均不变。

零散附件加上可导入的依赖，不构成可运行的原项目测试套件。导入安装版 Astropy 或 Django 不代表测试了修改后的附件，应通过报告中的路径和哈希确认实际执行的代码。这两个任务未提供完整原始源码或锁文件，因此仍无法进行完整历史回归验证。请一起同步更新后的 `run.sh`、`batch-tools.patch.yml`、`scripts/run-benchmark.py`、`scripts/dsh-e2b-mcp.py`、`scripts/dsh_e2b_environment.py` 和 `scripts/config/e2b-projects.json`；无需 Node 构建。离线检查为 `python scripts/test-e2b-mcp.py`、`python scripts/test-benchmark.py`。通过 `DSH_BENCHMARK_TEST_NODE` 启用的源码 profile 组合冒烟测试，会检查真实 headless Session 中关于本地已编辑附件的 E2B 元数据；仅模型和 E2B 网络端点被模拟。这些检查不证明实际 pip 或 E2B 服务可用。

仅盘古模式启用的视觉工具接受 E2B 导出后仓库内已存在的 PNG、JPEG 或 WebP 文件。它把图片字节和具体问题通过 Chat Completions 发送给 `COMPANY_DEEPSEEK_BASE_URL`（默认 `http://115.120.87.159:8082/v1`）上的 `DSH_VISION_MODEL`（默认 `deepseek-v4-pro`），只返回另一个模型的文字观察。`DSH_VISION_TIMEOUT_SECONDS` 默认 180 秒，`DSH_VISION_MAX_TOKENS` 默认 4096，`DSH_VISION_MAX_IMAGE_BYTES` 默认 8 MiB；MCP 调用比 HTTP 超时多预留 10 秒。该工具不把公司密钥暴露给盘古提示词或 E2B 沙箱。公司地址默认使用未加密的 HTTP，密钥和图片字节在传输途中没有保护；如果有 HTTPS 地址，应优先使用。DeepSeek 纯文本请求成功不代表网关支持图片：如果网关拒绝图片输入，工具会明确报错，不会声称已经看图。

## 运行与验证

从仓库根目录用 `sbatch run.sh` 提交公司 DeepSeek JSONL 任务，或使用模型专用评测入口。提交前可运行 `python scripts/test-e2b-mcp.py` 和 `python scripts/test-vision-mcp.py` 离线检查适配器，并在 Linux 上运行 `bash -n run.sh` 检查 Shell 语法。离线测试不验证实际服务；完整评测前，应先用小批次验证新 Pangu 网关的 token 限制与公司 DeepSeek 网关的图片支持。Pangu 要求 `$WORK/.secrets/` 下的 `pangu-api-key`、`deepseek-api-key`、`serper-api-key` 和 `e2b-api-key` 可读且仅所有者可访问。先检查日志中的提供方与补丁路径，再查看记录目录下 `results.jsonl` 中的结果。切换部署前请取消旧站点、密钥和补丁覆盖变量；脚本会保留显式覆盖。

`mcp__e2b__execute_python` 工具返回日志、错误和展示结果。在调用 `mcp__e2b__export_file` 之前，E2B 生成的文件不在本地；导出时指定沙箱绝对路径和新的仓库相对路径，例如 `remote_path=/home/user/chart.png`、`local_path=stock-analysis/chart.png`。该工具从同一任务的沙箱直接流式复制字节，只返回路径、大小和 SHA-256 校验值，不覆盖已有本地文件，并拒绝父目录跳转和符号链接目录。`DSH_ARTIFACT_MAX_FILE_BYTES` 也限制单个 E2B 导出文件大小（默认 100 MiB）；导出文件保留在任务选择的仓库位置，并纳入批处理产物副本。批处理脚本要求原生工具模式，禁用本地 Bash 执行，但保留本地文件系统工具。

盘古任务应把已导出的本地路径和具体视觉问题传给 `mcp__vision__inspect_image`，例如询问 K 线图标签是否被裁切。工具会拒绝仓库外路径、隐藏或依赖文件、不支持的图片字节以及超限文件。它的回答只是另一个模型给出的观察证据，不能代替数据计算检查，也不是给盘古的新指令。纯文本盘古路线不要调用 `read_image`；`image_search` 返回的是链接，不能检查本地图片。
