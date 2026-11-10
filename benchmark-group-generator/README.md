# Benchmark Group Generator

根据**外部提供**的 `user_query`、基线运行环境和 `baseline_fingerprint`，生成 Agent 指令遵从评测的 `benchmark_groups`：每个任务默认 5 个独立指令变体（可配置为 4–6 个）、对应的系统提示词及评分规则。

本仓库只负责构造和检查变体。基线 fingerprint 由数据提供方生成；程序不会从执行轨迹中提取 fingerprint，也不会替 Agent 运行变体。生成结果还需要在实际评测环境回放，并根据回放产物与轨迹评分、人工复核。

## 工作流程

1. 按 `task_id` 匹配任务、query 与 fingerprint，检查系统提示词、工具列表、环境信息和输入字段。
2. 使用 DeepSeek 提议候选指令和任务完成标准。根据提供的基线观测核对候选依据，排除已由基线自然满足、无可执行规则或缺少证据字段的候选。
3. 从有效候选中选择 4–6 条不同策略；每个变体只有**一条独立指令**。单条流程指令可以包含连续步骤。C 档增加任务上下文，D 档在用户追加内容中施加冲突压力。
4. 运行本地规则、反例和独立语义审查，生成 `effective_system_prompt`、IF/TC/SE 评分规则及构建记录。审查只把**同一变体内**的候选视为组合；不同变体各自独立运行。
5. 将 benchmark 写入 `output/`，日志、检查点、报告和构建元数据写入 `generated/`。生成成功仍需真实回放和人工复核。

流程指令中，“先查目录”和“先规划”目前只能自动核验首次工具调用。要求可见进度、只读探查或用户确认的策略，需要评测平台提供有序运行事件适配器；详见 [WORKFLOW_CONTRACT.md](WORKFLOW_CONTRACT.md)。

## 环境与配置

- Python 3.10 或更新版本；运行代码只使用 Python 标准库。
- 一个可用的 DeepSeek API Key。生成和语义审查会调用 DeepSeek；输入检查与离线测试不需要 API Key。

在仓库根目录复制配置模板，并在本机填写密钥：

```powershell
Copy-Item config.example.yaml config.yaml
```

macOS/Linux 可用 `cp config.example.yaml config.yaml`。`config.yaml` 已被 `.gitignore` 排除，**不要提交密钥**。`profile` 默认 `balanced`；`count` 可设为 4、5 或 6。`workflow` 模式只适用于明确提供了运行事件适配器的任务。

## 输入文件

每批数据放在 `data/` 下独立子目录，例如 `data/my_batch/`。支持两种格式，文件名需符合以下前缀：

| 格式 | 文件 | 说明 |
| --- | --- | --- |
| 分离输入 | `user_query*.jsonl` + `baseline_fingerprint*.jsonl` | 每行一个 JSON 对象；按 `task_id` 匹配，不按行号匹配。 |
| 内嵌输入 | `benchmark_groups*.json`，可选 `user_query*.jsonl` | JSON 数组，每条含非空 `baseline_fingerprint`；如同时提供 query 文件，任务 ID、`user_query` 和 `attached_files` 必须一致。 |

每条任务至少需要非空 `user_query`、真实基线 `system_prompt`、实际可用工具名数组 `tools`、非空环境信息 `env` 和非空 `baseline_fingerprint`。`task_id`/`id` 必须唯一；建议提供唯一的 `group_id`、`task_type` 和 `attached_files`。分离输入时，系统提示词、工具和环境信息通常放在 fingerprint 行中。示例见 [provided_user_query.jsonl](examples/provided_user_query.jsonl) 与 [provided_fingerprint.jsonl](examples/provided_fingerprint.jsonl)。

`attached_files` 记录评测任务的附件引用；生成器只检查输入中的一致性，不负责准备或验证附件实体。fingerprint 字段应来自提供方的基线运行，例如工具序列、调用次数或回复特征；程序核对**所提供文件**内的值，无法独立证明其运行来源。不要把含真实任务、轨迹或个人路径的数据文件提交到公开仓库。

## 使用方法

```powershell
# 只检查输入，不调用 DeepSeek
python quick_run.py "data/my_batch" --check

# 生成或续跑；不写目录参数时会列出 data 下的数据目录供选择
python quick_run.py "data/my_batch"

# 同一数据集开启全新生成；旧结果保留
python quick_run.py "data/my_batch" --new-run

# 只生成指定任务
python quick_run.py "data/my_batch" --task-ids 22
```

普通运行会寻找同一输入、模型、配置和生成器版本的最新结果并续跑：已成功任务跳过，失败任务重试。`--new-run` 会创建新结果并重新生成所有选中任务。终端显示进度条、重试和错误摘要；结束时看 `Summary` 中的 `failed`。重试消息不等于任务最终失败。

输出示例：

```text
output/benchmark_my_batch_YYYYMMDD_HHMMSS.json
generated/benchmark_my_batch_YYYYMMDD_HHMMSS/run.log
generated/benchmark_my_batch_YYYYMMDD_HHMMSS/report.json
generated/benchmark_my_batch_YYYYMMDD_HHMMSS/metadata.json
generated/benchmark_my_batch_YYYYMMDD_HHMMSS/task_22_checkpoint.json
```

最终 benchmark 不包含 `construction_metadata`；构建记录单独保存在 `metadata.json`。失败任务可在相同输入与配置下直接重跑 `python quick_run.py "data/my_batch"`，无需 `--new-run`。评分入口是 `python generator.py score --groups ... --group-id ... --variant-id ... --evidence ... --judgments ... --output ...`；评分必须使用实际变体回放证据，人工判断项由 `judgments` 提供。

## 离线验证与发布边界

```powershell
python -m unittest discover -s tests -q
```

合成示例仅用于检查输入格式和规则，不代表真实任务已可执行。生成器的本地校验与模型审查不能替代真实回放、任务完成判定或人工复核。此仓库不包含真实基线数据、API Key、输出、检查点或日志。

## 上传到 GitHub

在本目录创建 Git 仓库后，连接你自己的 GitHub 空仓库：

```powershell
git init -b main
git add .
git commit -m "Initial benchmark group generator"
git remote add origin "https://github.com/USERNAME/REPO.git"
git push -u origin main
```

提交前可运行 `git status` 核对文件清单；`.gitignore` 会排除本机配置、数据集和生成结果。若通过 GitHub 网页上传，请解压发布包并上传其中的文件和目录，而不是把 ZIP 本身当成代码文件提交。
