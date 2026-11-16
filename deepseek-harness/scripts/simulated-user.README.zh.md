# 无界面批处理中的模拟用户

[English](simulated-user.README.md) | 中文

## 概要

设置 `DSH_SIM_USER=1` 后，独立的 Qwen 模型会在 JSONL 或基准批处理中回答显式的工具问题，无需终端或人工回复。这是合成对话，不是业务后端，也不是真人授权。不设置此标志或设为 `0` 时，不安装模拟回答处理方。

## 部署

同步 `run.sh`、`run_70.sh`、`scripts/run-benchmark.py`、`scripts/check-user-queries.py`、`scripts/dsh_e2b_environment.py`、`scripts/simulated-user.mjs`、`scripts/dsh_simulated_user.py` 和 `scripts/config/simulated-user.json`，以及 `user_query_70.jsonl` 和对应的 `attached_files/`。现有源码启动方式无需重新安装 Node 依赖或构建。将 Qwen 密钥保存为仅所有者可访问的 `$WORK/.secrets/qwen-api-key`，内容为一行非空密钥；`DSH_SIM_USER_KEY_FILE` 可覆盖路径，已导出的 `DSH_SIM_USER_API_KEY` 优先于文件。不要把密钥写入 JSON 配置或批处理输入。

```bash
chmod 600 "$WORK/.secrets/qwen-api-key"
sbatch --export=ALL,DSH_SIM_USER=1 run_deepseek.sh
```

其他主模型分别使用 `run_pangu.sh`、`run_pangu92b.sh` 或 `run_glm.sh`；`run.sh` 仍读取 JSONL 输入。现有基准组和变体筛选仍有效。集群模块、Singularity、代理和 Slurm 执行须在服务器验证，本地测试不会提交作业。取消此标志或设置 `DSH_SIM_USER=0` 即可返回原基准模式。不要把模拟对话结果与单轮基线分数混合。

`DSH_SIM_USER_CONFIG` 可指定公开 JSON 配置，替代 `scripts/config/simulated-user.json`。默认使用 `https://dashscope.aliyuncs.com/compatible-mode/v1` 上的 `qwen3.7-flash`，HTTP 期限 60 秒、输出上限 1,024 token、每任务最多送达八次回复和发起二十次请求，响应上限 1 MiB、输入上限 65,536 字符。只计入工具提问请求。以上限制均可在配置文件中调整。请求不自动重试。模拟器接受 HTTPS 站点，仅离线夹具可使用回环 HTTP。一次真实 Qwen 双问题冒烟测试已验证具体选项选择及前后一致的虚拟细节；完整真实模型批处理行为须在服务器验证。

### 执行 70 条 JSONL 样例

在服务器的仓库目录提交 `sbatch run_70.sh`。该入口选择 `user_query_70.jsonl`、启用模拟用户，并在启动模型任务前检查全部 70 条记录和附件路径。当前数据有 553 个附件引用，其中包括 70 个空 `.keep` 占位文件。缺失文件、重复 ID、不安全的附件路径或条数不符都会使预检终止。`python scripts/check-user-queries.py user_query_70.jsonl --expected-count 70` 可单独运行同一预检，不调用模型。

Slurm 日志为 `dsh_70_<jobid>.out`；记录位于 `$WORK/dsh-runs/user_query_70-<jobid>/`，包含 `results.jsonl`、逐任务轨迹、模拟器审计及产物副本。任务顺序运行，每条使用新 Session。失败任务会记录后继续下一条；取消或批处理致命错误可能中止整批。JSONL 模式只拷贝变动产物，不在任务间还原工作区或附件。70 条输入使用不同的附件路径，但生成的文件名仍可能冲突。运行期间不要修改仓库或在同一仓库中运行其他任务。`run_deepseek.sh` 仍是 JSON 基准入口，不是 JSONL 入口。

## 对话及限制

只回答显式的 `ask_user_question` 调用，使用严格 JSON Schema（`response_format.type=json_schema`、`strict=true`），本地仍校验字段类型及问题 ID。不改变主模型的工具定义、工具使用规则或系统提示词，不判断或回答普通文本问题。

每个启用此模式的任务会获得已有的阻塞式 `ask_user_question` 工具及合成回答处理方。回答以选中的选项标签和带标记的自由文本进入普通工具结果。本地校验会拒绝未提供的标签、重复选项和单选题的多选回答。不监听 `agent/turn-stopping`，也不注入 steering 消息或提供普通文本兜底。若主模型只在正文中提问，headless 轮次可能直接结束而得不到回答。此模式不强制模型调用工具。

Qwen 只接收原始 `user_query`、当前工具问题及选项，以及自身之前的对话。它不会收到附件字节、系统提示词变体、评分 rubric、业务工具输出、主模型推理或主模型提供方密钥。缺失偏好和无害的场景细节会得到合理的虚拟回答，例如受众、时长、预算或明确的选项选择。策略要求保留原始约束、保持前后设定一致，而不是默认回答不知道。新增虚构细节时设置 `synthetic=true`，并在回复标记中加入 `含虚构设定`。需要真实凭据、经验证的后台事实或真实操作才能回答时，仍可设置 `unknown=true`。Qwen 不得声称真实付款、操作设备、恢复业务、完成测速，或有权覆盖系统及安全规则。这是提示词约束，不是绝对保证；解释结果前请检查审计记录。

不会回答运行时子智能体。带意图标签的计划审阅会交给原回答通道，不自动批准；此模式不安装沙箱或权限批准提供方。回复明确标记为模拟内容，不是真人授权。电信等领域缺失的 API 仍然缺失：对话正常结束，不代表业务操作成功。

超时、HTTP 错误、错误答案 ID/JSON、截断输出或预算耗尽会产生错误。模拟器失败会阻止后续主模型步骤，取消会传递给 HTTP 请求。问题调用及回答保留在原生 Session 工具历史中；无需修改 Session 格式或 agent-loop。

## 记录及检查

每条 `request` 记录本次指令及响应 schema。每次 HTTP 成功且可解析的 JSON 输出都会在应用校验前记录为 `provider_response`，其中 API key 被脱敏。这些值仍是不可信的模型输出，不是已确认的用户事实。校验失败时，审计会保留返回字段及具体字段错误；HTTP 错误响应正文仍不记录。

每个任务的 `simulated-user.patch.json` 保存公开配置。`simulated-user.jsonl` 记录模拟器策略、模型、输入、回复、未知及虚构标记、用量及错误，不含 API key 或 HTTP 错误正文。模拟回答只出现在原生工具结果中，不产生合成 `user` 消息或 `simulated_user` 标准输出事件，已归档的旧轨迹仍可读取。基准的系统提示词处理见[基准指南](benchmark.README.zh.md#提示词与环境)，退出/最终事件判定及恢复逻辑不变。

```bash
python scripts/test-simulated-user.py
python scripts/test-user-queries.py
python scripts/test-benchmark.py
bash -n run.sh
bash -n run_70.sh
```

将 `DSH_BENCHMARK_TEST_NODE` 指向受支持的 Node 可执行文件，可启用真实 headless 源码组合测试。测试只模拟模型 HTTP 端点，验证原生工具回答、证明普通文本问题不会调用 Qwen、检查持久化工具结果，并拒绝提供方失败、错误 ID、截断输出及耗尽预算。无密钥测试不会调用付费提供方。
