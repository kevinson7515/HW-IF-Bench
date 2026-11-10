# Rubric Benchmark Scoring

基于 rubric 对 benchmark 运行记录评分的 Python 工具。支持结构化程序规则、旧版断言兼容检查、DeepSeek 模型评审和分层加权汇总。

**标准来自输入 rubric；代码决定如何验证标准。不会直接执行 rubric 中的 `exec` 字符串，也不会把证据缺失默认判为通过或零分。** 本项目是运行完成后的评分器，不负责执行 benchmark 任务。

## 环境与快速开始

需要 Python 3.10 或以上版本，仅使用标准库，无需安装第三方 Python 包。

在仓库根目录运行：

```bash
python run_scoring.py --no-judge
```

默认配置使用 `examples/dataset` 中的合成示例，不调用外部 API。示例包含一条程序项、两条模型评审项，因此初评应为 `needs_review`，而不是完整得分。

使用附带的**人工示例判断**完成离线汇总：

```bash
python score_benchmark.py --groups examples/dataset/benchmark_groups.json --run examples/dataset/dsh-runs/benchmark-demo --judgments examples/manual_judgments.jsonl --out results/demo_scores.json
```

预期结果：`IF=0.6`、`TC=0.4`、`SE=0`、`weighted_score=1.0`、`joint_success=true`。这些示例判断不是模型实测结果。

Windows 也可使用 `score.cmd`，它调用 PATH 中的 `python`。

## 评分标准与执行逻辑

### 1. rubric 是标准，规则实现是验证方式

每个 group 包含多个 variant；每个 variant 的 `rubric` 列表定义评分项：

| 字段          | 含义                             |
| ----------- | ------------------------------ |
| `id`        | 评分项标识，与 group、variant 一起定位判断结果 |
| `layer`     | `IF` 指令遵循、`TC` 任务完成、`SE` 副作用   |
| `method`    | `program` 或 `llm_judge`        |
| `weight`    | 通过项得分或副作用惩罚；SE 应使用负权重          |
| `must_pass` | IF 的必过条件，默认 false              |
| `assert`    | 人类可读的断言描述；程序项无法判断时用于复核队列       |
| `rule`      | 程序项实际使用的结构化规则，优先于 `exec`       |
| `exec`      | 旧版程序断言文本，或模型项的评分提示词            |

实际分流如下：

1. `program` 有 `rule`：调用 `rubric_program.evaluate_rule()`，在最终回复、完整工具记录和产物路径上解释规则。
2. `program` 没有 `rule`：仅对 IF 项尝试旧版兼容。`exec` 的 SHA-256 必须与 `PROGRAM_EXEC_HASHES` 中登记的 group/variant 一致，然后执行 `check_program()` 中预先实现的检查。原断言字符串不会执行。
3. `llm_judge`：读取已提供的 judgments；没有有效判断时，生成队列。启用模型评审后，将该项 `exec` 作为评分提示，连同可用证据发给 DeepSeek，再导入结果汇总。
4. 未支持的程序断言或缺失证据：保留为无法判断，进入复核队列。

所以，**只改 `assert` 不一定改变实际评分**。程序项应同步修改 `rule`；旧版 `exec` 一旦改变，哈希不匹配便不能继续使用原来的兼容实现。新增任务建议提供结构化规则；超出支持范围的操作需要扩展解释器，而不是添加任意 Python 字符串。

旧版兼容逻辑针对 K 线、检索和 parser 代码任务，包含输出目录、图表样式、来源域名、字数与内容、抓取次数、代码修改范围及验证行为等检查；它不是面向所有任务的通用断言执行器。

### 2. 程序规则如何判断

例如，“最终回复长度不超过 100 个字符”：

```json
{
  "path": "final_answer",
  "op": "length_le",
  "value": 100
}
```

可访问路径包括 `final_answer`、`trace.calls.*.name`、`trace.calls.0.name`、`trace.calls.*.args` 和 `artifacts.*.path`。支持数字下标和 `*` 投影。

| 操作                      | 行为                                                             |
| ----------------------- | -------------------------------------------------------------- |
| `eq`                    | 类型和值均相等                                                        |
| `length_le`             | 字符串、列表或字典的长度不超过阈值；字符串按 Python 字符数计算                            |
| `count_eq` / `count_le` | 列表中等于 `match` 的元素数量等于／不超过阈值                                    |
| `section_content`       | 指定二级 Markdown 标题下有非空内容                                         |
| `all_prefix`            | 非空产物路径列表均位于指定前缀下，且无 `..` 路径段                                   |
| `sources_allowed`       | 检查回复和工具参数未使用给定的禁用域名／检索关键词；名称虽为 allowed，`value.domains` 实际是排除列表 |
| `all` / `any`           | 组合子规则，例如 `{"all": [规则1, 规则2]}`                                 |

返回值为 `True`、`False` 或 `None`。缺失字段、未知操作或不合适的类型会得到 `None`。组合规则采用保守策略：任一子项未知，整个组合即未知，即使其他子项已经足以决定普通布尔表达式。空产物列表通常不足以验证 `all_prefix`；明确完整且无产物的 manifest 在评分入口会被判为失败。

### 3. 模型如何判断

模型逐项查看 rubric 评分提示、variant 指令、最终回复、可用轨迹和产物。文本产物和轨迹有长度上限；部分图表任务需要图片证据及配置的视觉模型。证据不足时应返回 `ABSTAIN`。

| 层级  | 判断值                         | 得分含义                                 |
| --- | --------------------------- | ------------------------------------ |
| TC  | `FULL` / `PARTIAL` / `NONE` | 全额／半额／零分                             |
| SE  | `YES` / `NO`                | 触发惩罚／无惩罚                             |
| IF  | `YES` / `NO`                | 评审协议支持这两个值，但当前汇总对模型 IF 的状态映射存在限制，见下文 |

SE=YES 需要同时提供非空 `evidence`、`caused_by_constraint=true`、`distinct_from_tc=true`，用于避免无证据扣分和与 TC 重复扣分。

### 4. 分数如何汇总

设每项权重为 w：

```text
IF = 所有通过的 IF 项权重之和
     但任一 must_pass 项失败时，整个 IF = 0
TC = Σ(w × 完成系数)，FULL=1、PARTIAL=0.5、NONE=0
SE = max(-0.5, Σ已触发 SE 项的权重)
总分 = max(0, IF + TC + SE)
```

权重来自 rubric，代码没有自动归一化，也没有把总分封顶为 1。因此只有合理配置权重时，才可把分数理解为 0–1 范围。

例：IF 权重 0.6 且通过，TC 权重 0.4 且部分完成，SE 权重 −0.2 且触发，总分为 `0.6 + 0.2 - 0.2 = 0.6`。必过项失败只将 IF 归零，不会自动将整条案例总分归零。

`joint_success` 单独表示 IF 必过项与所有 TC 项是否全部通过。它不检查普通 IF 项，也不考虑 SE，不能等同于满分或“没有副作用”。

### 5. 何时没有完整总分

运行失败时为 `run_failed`。D 类注入变体需有送达证据，否则为 `not_applicable`。存在且不匹配的系统提示词哈希会标为 `invalid_prompt_hash`。证据或判断未齐备时通常为 `needs_review`，相关分项及总分保留 `null`。

`eligible_for_comparison` 要求运行成功、状态为 `scored`，且提示词哈希没有已知冲突；哈希缺失并不会单独导致排除。基线指纹对齐只作为诊断，不会修改 rubric，也不会独立排除已评分案例。

## 使用自己的数据

建议数据目录如下（原始数据不随本仓库发布）：

```text
dataset/
  benchmark_groups.json
  baseline_fingerprint_*.jsonl          # 可选
  attached_files/task_3/parser.py       # 代码任务可能需要
  dsh-runs/
    benchmark-example/
      results.jsonl
      G-example/
        S1/
          final.txt
          trace.json
          trace.jsonl
          artifacts.json
          ...                          # 实际产物及记录器导出文件
```

`results.jsonl` 每行至少包含 `group_id`、`variant_id`、`status`，评分入口会检查这些 ID 是否属于所选 rubric。

结构化工具规则读取 `trace.jsonl`，每个工具事件应含 `type: "tool_call"`、`tool` 和 `input`；行记录还需声明 `recording_status: "complete"`、`final_event_seen: true`、无解析错误及准确的整数 `tool_calls` 数量。缺失这些完整性信息时，工具记录不被当作完整证据。模型评审使用的 `trace.json` 与这里的 JSONL 不能互相替代。

产物需要通过 manifest 定位到真实可读文件；仅在最终回复中声称“已生成”不等于存在产物证据。不同任务的旧版指标提取还可能依赖记录器导出的其他文件，应保留完整运行目录。

```bash
# 仅本地初评
python run_scoring.py --data /path/to/dataset --no-judge

# 明确指定 rubric 与某一次运行
python run_scoring.py --data /path/to/dataset --groups /path/to/dataset/benchmark_groups.json --run /path/to/dataset/dsh-runs/benchmark-example --no-judge

# 只列出将评测的运行
python run_scoring.py --data /path/to/dataset --list
```

支持多个 `--run`；它们必须使用同一份 rubric。自动发现运行时只扫描数据根目录及 `dsh-runs` 下名称以 `benchmark-` 开头、含 `results.jsonl` 的目录；其他名称可用 `--run` 指定。

其他参数：`--config`、`--baseline-file`、`--results-dir`。配置中的相对目录以配置文件位置为基准；`--data` 路径以当前工作目录为基准。

## 启用 DeepSeek 评审

复制 `config.json` 为 `config.local.json`，将 `deepseek_judge.enabled` 改为 true，填写自己的可用文本模型名称；需要图像评审时填写支持图像输入的 `vision_model`。仓库不预设模型名称，实际可用名称由所用接口决定。

优先使用环境变量提供密钥，避免写入发布文件。PowerShell 示例：

```powershell
$env:DEEPSEEK_API_KEY = "你的密钥"
python run_scoring.py --config config.local.json --data "D:\datasets\my-dataset"
```

启用后会提示发送待评证据和 API 费用，确认后先本地评分，再评审队列中的 `llm_judge` 项，最后重新汇总。若未设置环境变量，程序可交互式隐藏输入密钥。文本脱敏只是尽力处理，图片和文件仍可能包含私密信息，上传前应确认数据可以交给该接口。

本地模式 `--no-judge` 不会调用接口，但会复用当前结果目录里已有的对应 judgments。

## 输出与复核

默认写入 `results/`，不纳入版本控制：

| 文件                            | 内容                       |
| ----------------------------- | ------------------------ |
| `*_scores.json`               | 每条案例分项、rubric 状态、总分及可比较性 |
| `*_scores_review_queue.jsonl` | 未完成判断的评分项与可用证据           |
| `*_judgments.jsonl`           | 模型判断及证据，调用模型后产生          |
| `*_judgments_errors.jsonl`    | 模型调用或响应解析问题，出错时产生        |
| `summary.csv`                 | 最近一次批量调用的运行概览            |

输出名指纹由运行路径、`results.jsonl`、rubric 文件和可选外部基线文件计算；**没有覆盖全部轨迹和产物内容**。更改证据或评审配置后，建议使用新的 `--results-dir`，避免复用过时判断。

人工 judgments 的格式见 `examples/manual_judgments.jsonl`，可用 `score_benchmark.py --judgments 文件路径` 导入。程序项始终依其规则与证据重算，不会被同名的人工或模型 verdict 覆盖。

## 当前实现边界

- 本项目包含面向特定 benchmark 的旧版适配，不是任意 `exec` 代码的执行框架。
- `program_review` 只作为复核记录：当前模型循环仅处理 `llm_judge`，汇总也不导入程序项的替代 verdict。应补齐证据或修正规则后重跑。
- `deepseek_judge.py` 虽声明 `--include-program-review` 参数，当前筛选逻辑并不会因此处理程序复核项；发布配置已移除此无效选项。
- 当前模型 IF 判断被映射为 `triggered/clear`，而 IF 汇总要求 `pass/fail`，因此不能正常完成这一组合的汇总。当前应将 IF 写成可支持的 `program` 项；此发布整理保留原评分行为，未改动该逻辑。
- 没有统一的 rubric schema 校验；请使用一致且唯一的 ID、正确层级、合理的数值权重和受支持操作。格式错误可能导致报错，而非友好的校验提示。
- 模型判断不是事实真值。轨迹截断、产物缺失、模型能力和提示词都会影响结果；图表、来源真实性及代码行为仍可能需要人工核验。
