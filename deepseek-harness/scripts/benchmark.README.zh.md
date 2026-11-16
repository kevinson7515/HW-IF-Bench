# 模型基准批处理

[English](benchmark.README.md) | 中文

## 概要

提交 `run_deepseek.sh`、`run_pangu.sh`、`run_glm.sh` 或 `run_pangu92b.sh`，可把 `benchmark_groups.json` 中选定的每个变体作为新的无界面 Session 执行。每个变体使用同组的 `user_query`，保留 harness/提供方原有系统提示词。`effective_system_prompt` 只作为元数据保存，不会应用。运行器将产物和 Session 记录复制到 `dsh-runs`，随后在下一个变体开始前恢复仓库到批处理启动时的文件状态。

## 目录

- [提交](#提交)
- [提示词与环境](#提示词与环境)
- [记录](#记录)
- [工作区恢复](#工作区恢复)
- [验证](#验证)

## 提交

DeepSeek、Pangu 和 GLM 入口复用 `run.sh` 的 Slurm、Singularity、Conda、受保护密钥、代理以及 Serper/E2B 配置。提供方补丁仍位于 `$WORK/dsh-config/` 下，分别为 `deepseek.patch.yml`、`pangu.patch.yml` 和 `glm.patch.yml`；对应部署模板位于 `scripts/config/`。各入口选择对应补丁及仅所有者可访问的 `$WORK/.secrets/<model>-api-key` 文件，其中 `<model>` 为 `deepseek`、`pangu` 或 `glm`。请一起上传入口、更新后的 `run.sh`、`scripts/run-benchmark.py`、`scripts/dsh_simulated_user.py` 及仓库外的配置目录。无需更改 Node 依赖或重新构建。从仓库目录提交即可；默认分区和 GPU 请求与 `run.sh` 一致，也可使用常规 `sbatch` 参数覆盖资源。实际集群运行依赖服务器现有模块和密钥，须在服务器验证。

```bash
sbatch run_deepseek.sh
sbatch run_pangu.sh
sbatch run_glm.sh
sbatch run_pangu92b.sh
```

补丁通过 OpenAI Chat Completions 和 Bearer 认证选择 `deepseek-v4-pro`、`glm-5.3` 和 `openPangu-v21-pro`；站点、密钥覆盖变量及 Pangu 的有界退避重试统一见[批处理工具](batch-tools.README.zh.md#模型提供方)。Pangu 不再要求华为硬件或应用凭据，现有视觉桥接单独使用 DeepSeek 密钥。GLM 容量沿用 harness 的通用默认值：上下文 262,144 token、输出 32,768 token，可通过 `COMPANY_GLM_CONTEXT_WINDOW` 和 `COMPANY_GLM_MAX_TOKENS` 覆盖，并非已验证的网关限制。Pangu 保留已有容量配置及流等待超时。GLM 补丁不声明图像输入能力，也不启用 Pangu 专用视觉桥接。YAML 模板中不应包含密钥。

输入默认为仓库中的 `benchmark_groups.json`；入口的第一个参数可指定其他 JSON 文件。运行器按组和变体的文件顺序执行所有选定变体。各入口会固定各自的提供方，不受继承的 `DSH_MODEL_PROVIDER` 影响；显式的 `DSH_PATCH_FILE` 仍会覆盖补丁，切换模型前请取消旧提供方的覆盖值。可用 `DSH_BENCHMARK_GROUPS` 和 `DSH_BENCHMARK_VARIANTS` 按逗号分隔的标识符筛选；不设置时执行全部变体。未知标识符会在任何任务开始前报错。同一仓库的作业会等待同一把锁。批处理期间不要编辑仓库文件或运行不遵守此锁的其他智能体，因为这些写入无法与基准测试的写入区分。

```bash
sbatch --export=ALL,DSH_BENCHMARK_GROUPS=G-code-001 run_pangu.sh
```

`pangu92b` 提供方通过 `$WORK/dsh-config/pangu92b.patch.yml` 选择 `pangu92b_wandr`，并读取仅所有者可访问的 `$WORK/.secrets/pangu92b-api-key.yml` 凭据包；其华为认证及容量覆盖变量见[批处理工具](batch-tools.README.zh.md#模型提供方)。请同步 `run_pangu92b.sh`、更新后的 `run.sh`、`batch-tools.patch.yml` 和这两个仓库外的文件；无需 Node 构建。记录保存到 `$WORK/dsh-runs/benchmark-pangu92b-<job-id>/`。它沿用现有 Serper、E2B、DeepSeek 视觉密钥、变体筛选、记录及恢复行为。本地模拟检查覆盖请求头和文件工具；完整评测前，须在集群验证实际接口的流式输出及 Function Calling 支持。

## 提示词与环境

在无界面服务器上显式启用 Qwen 回答 `ask_user_question`，见[模拟用户](simulated-user.README.zh.md)。此模式改变对话及工具 schema，不改变 harness 系统提示词，须与单轮基线分开报告。

运行器不加载 `benchmark-prompt`，也不创建 `prompt.patch.json`，不会用 benchmark 的 `effective_system_prompt` 覆盖或追加系统提示词。原有 profile/提供方系统提示词、工具指引、工作区指令及技能目录保持有效。任务、结果和计划记录中的 `variant_system_prompt_applied: false` 明确标记此行为。仅系统提示词不同的变体现在会重复同一任务条件，不能再用其运行结果测量原提示词差异。

运行器不会把 `tools`、`env`、`rubric.exec`、`environment_override`、`env_snapshot` 或 `user_query_append` 解释为可执行配置。它保存这些字段作为元数据，只应用组查询。特别是，两处包含自然语言注入描述的 S5 变体不会注入网页或源码注释夹具；`task.json` 会记录 `environment_override_applied: false`。搜索、抓取及 E2B 仍调用实际服务，不回放数据集中的抽象基线。Rubric 评分是独立步骤。

附件路径相对于输入 JSON 文件解析。每个附件须为仓库内、且不在排除的运行目录中的普通文件。运行器在用户消息中列出原始绝对路径，并在执行前把起始字节复制到 `inputs/`。它不会移动工作目录或重定向模型选定的产物路径。

## 记录

默认记录目录为 `$WORK/dsh-runs/benchmark-deepseek-<job-id>/`、`$WORK/dsh-runs/benchmark-pangu-<job-id>/` 和 `$WORK/dsh-runs/benchmark-glm-<job-id>/`。`DSH_RUN_ROOT` 和 `DSH_BATCH_ID` 仍可覆盖现有默认值。记录目录与 `DSH_HOME` 必须位于仓库外。已有 `plan.json` 的基准输出目录不会复用；重跑时请选择新的批次 ID。

```text
benchmark-pangu-<job-id>/
  plan.json
  benchmark_groups.json
  workspace-baseline/manifest.json
  workspace-baseline/files/...
  G-code-001/S1/
    task.json
    variant_system_prompt.txt
    trace.jsonl
    trace.json
    final.txt
    diagnostics.log
    inputs/...
    artifacts/...
    artifacts.json
    session-records/...
    session-records.json
    result.json
  results.jsonl
  summary.json
```

`trace.jsonl` 是 headless 事件流。`trace.json` 因投影中没有真实系统提示词而省略 system 角色；请读取已归档 Session 的 `system/message` 事件了解实际请求。`variant_system_prompt.txt` 和 `variant_system_prompt_sha256` 描述未应用的输入变体，不是运行时提示词。`result.json` 记录退出/最终事件检查、工具统计以及记录和恢复结果。执行成功不代表 rubric 成功。失败任务可先记录、恢复，再开始下一个变体。

## 工作区恢复

运行器保存一次实际工作文件的私有基线，包含已有未提交修改和产物。每个任务结束后，它按文件字节、权限、条目类型及符号链接目标检测变化，对新增或修改的普通文件归档并校验 SHA-256，记录删除路径与链接变化，复制 Session，随后才恢复原件并移除新增条目。批处理开始前已存在的产物仍属于基线。`.git`、所有 `node_modules` 目录以及根目录的 `dsh_*.out`/`dsh_*.err` 日志被排除；harness 主目录、Session、仓库外缓存及远程 E2B 内容不会回退。清理不会沿符号链接进入仓库外，也不使用 Git reset 或 clean。

若记录或恢复验证失败，运行器会停止后续变体，保留基线，并在 `$WORK/.locks` 下留下按仓库区分的恢复日志。其他遵守锁的批处理会拒绝启动，直到恢复完成。入口会请求 Slurm 在时间限制前发送 TERM 提醒；正常取消会停止子进程、记录已有输出并恢复工作区。SIGKILL、节点故障或清理时间不足可能阻止自动恢复。先取消原作业并等待其退出，再检查日志所示恢复文件与记录，在原始仓库目录、同一 Linux/Conda 环境中执行恢复：

```bash
python scripts/run-benchmark.py --restore "$WORK/dsh-runs/benchmark-pangu-<job-id>"
```

恢复会取得仓库锁，将残留变化复制到新的 `recovery-*` 目录，验证保存的基线，恢复工作区并清除恢复日志。它不会把中断任务报告为成功。产物记录沿用单文件 100 MiB、总计 1 GiB 的上限（`DSH_ARTIFACT_MAX_FILE_BYTES`、`DSH_ARTIFACT_MAX_TOTAL_BYTES`）；超过上限会停止清理并保留工作区等待恢复。基线存储默认最多 10 GiB（`DSH_BENCHMARK_BASELINE_MAX_BYTES`）。取消时经过 `DSH_BENCHMARK_STOP_GRACE_SECONDS`（默认 20 秒）仍未退出的子进程会被强制终止。

## 验证

数据集验证仅需 Python，不读取密钥或执行任务：

```bash
python scripts/run-benchmark.py --check benchmark_groups.json
python scripts/test-benchmark.py
bash -n run.sh
bash -n run_deepseek.sh
bash -n run_pangu.sh
bash -n run_glm.sh
bash -n run_pangu92b.sh
```

文件系统测试验证记录与恢复、失败任务、中断、不安全路径、损坏备份和延迟修改。源码 profile 冒烟测试可通过 `DSH_BENCHMARK_TEST_NODE` 指向受支持的 Node 可执行文件来启用；它们用实际 headless 启动器和文件工具配合本地模拟模型，检查实际 HTTP 系统提示词被保留，而非替换成输入变体，以及归档和恢复后的附件字节。四个提供方用例都加载部署模板，验证模型名、Bearer 密钥和 Chat Completions 地址；仅 Pangu92B 发送华为硬件及应用认证头。可用 `DSH_BENCHMARK_TEST_CONFIG_DIR` 指定部署补丁目录，替代 `scripts/config/`。`DSH_BENCHMARK_TEST_BASH` 启用入口及新密钥文件名的初始化检查，集群依赖以模拟方式替代。这些测试不会调用公司、盘古、Serper 或 E2B 服务。在解读基准分数前，应先检查首次实际集群批次。
