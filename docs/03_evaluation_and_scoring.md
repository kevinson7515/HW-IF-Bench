# 评测执行与三维评分体系

本文档说明三件事：
1. **模型是怎么跑的**：[`dsh-config/`](../dsh-config) 的模型配置，以及运行完后目录里生成了哪些文件、各自记录什么内容。
2. **分数是怎么算的**：[`scoring/`](../scoring) 如何把 **IF（指令遵循）**、**TC（任务完成度）** 和 **SE（副作用）** 合成最终得分。
3. **当前评分器的能力边界**：接手后直接跑分时有哪些已知的限制。

---

## 一、模型运行配置与输出目录解析

### 1.1 四套模型配置（[`dsh-config/`](../dsh-config)）

| 配置文件 | 对应模型 (`model`) | 上下文与输出上限 | 当前在 `dsh-runs/` 中的状态 |
| --- | --- | --- | --- |
| [`deepseek.patch.yml`](../dsh-config/deepseek.patch.yml) | `deepseek-v4-pro` | 默认配置 | 已跑基线（`baseline-17`/`33`）及待测 run（`benchmark-deepseek-17`） |
| [`glm.patch.yml`](../dsh-config/glm.patch.yml) | `glm-5.3` | 262K / 32K | 已跑 `benchmark-glm-17`（100 变体） |
| [`pangu92b.patch.yml`](../dsh-config/pangu92b.patch.yml) | `pangu92b_wandr` | 262K / 32K（含压缩配置） | 已跑 `benchmark-pangu92b-17`（100 变体） |
| [`pangu.patch.yml`](../dsh-config/pangu.patch.yml) | `openPangu-v21-pro` | 524K / 32K（声明纯文本+视觉工具引导） | **仅配置了文件，尚未开跑** |

> **注意**：本仓库里的 [`deepseek-harness/`](../deepseek-harness/) 目前是一个空的 Git submodule 指针（`d743267`），实际执行脚本不在此目录中。

### 1.2 每次跑完一个变体，磁盘上会留下什么文件？

以 `dsh-runs/benchmark-deepseek-17/G-coding-astropy-12891/S1/` 为例，每个变体目录下包含这些关键文件：

| 文件名 | 里面存什么（通俗解释） | 谁会用到它 |
| --- | --- | --- |
| `task.json` | 下发给模型时的任务快照，包含实际输入的 `effective_query`、系统提示词哈希，以及 **`user_query_append_applied` / `environment_override_applied`**（D 档冲突到底有没有真正注入） | 核对 D 档送达、排查运行输入 |
| `result.json` | 这次运行的状态摘要：`status`（`succeeded`/`failed`）、总步数 `steps`、工具调用数 `tool_calls`、报错数 `tool_errors`、结束原因 `turn_end_reason`（如 `completed` 或 `max-tokens`）、录屏状态 `recording_status` | 判断有没有跑挂、供程序规则校验轨迹完整性 |
| `final.txt` | Agent 最终给用户的完整文本回复 | IF 字数/结构规则、TC/SE 裁判模型 |
| `trace.jsonl` | 按行记录的事件流（含每次 `tool_call` 的工具名和入参） | [`rubric_program.py`](../scoring/rubric_program.py) 解析调用次数、顺序和域名 |
| `trace.json` | 对话历史投影 JSON（含工具返回内容，标有 `lossless` 是否无损） | [`deepseek_judge.py`](../scoring/deepseek_judge.py) 发送给裁判模型做语义评审 |
| `artifacts.json` 与 `artifacts/` | 工作区变动清单（新增/修改/删除了哪些文件及 SHA-256）以及实际保存出来的产物文件 | 检查 `output/` 交付目录、提取 `parser.py` 做 AST 对比、传给视觉模型看 K 线图 |
| *(缺失)* 根目录 `results.jsonl` | 正常每次批量运行根目录应有一份汇总各变体 `result.json` 的总表 | [`run_scoring.py`](../scoring/run_scoring.py) 靠它扫描运行目录，**但当前 3 个 17 题模型目录都缺了这个文件** |

---

## 二、三维评分体系：IF / TC / SE 怎么打分？

评分核心实现在 [`scoring/score_benchmark.py`](../scoring/score_benchmark.py)、[`scoring/rubric_program.py`](../scoring/rubric_program.py) 和 [`scoring/deepseek_judge.py`](../scoring/deepseek_judge.py)，批量入口为 [`scoring/run_scoring.py`](../scoring/run_scoring.py)。

### 2.1 第一维：IF（指令遵循，权重 0.6，一票否决 `must_pass`）

- **怎么判**：
  1. **新版规则（`rubric` 里有 `rule` 字段）**：由 [`rubric_program.py`](../scoring/rubric_program.py) 直接解释 JSON 规则（**绝不执行 `exec` 字符串**）。
     - 如果规则涉及工具调用（如禁调某工具、禁用某域名），[`recorded_calls()`](../scoring/rubric_program.py#L22-L45) 会严查 `trace.jsonl` 是否完整（要求 `recording_status == "complete"`、`final_event_seen == True`、无解析报错且调用数与 `result.json` 一致），再用 `TOOL_ALIASES` 把原始工具名（如 `read`、`todo_write`）映射为规范名（`file_read`、`task_planning`）。
     - 如果规则检查产物目录（`all_prefix`）而 `artifacts.json` 明确声明无任何新建或修改文件，直接判不通过（`complete_empty_artifact_manifest`）。
  2. **旧版原型题兼容（Task 15–17 无 `rule` 字段）**：先核对 `exec` 字符串的 SHA-256 哈希是否在 [`PROGRAM_EXEC_HASHES`](../scoring/score_benchmark.py#L30-L47) 白名单内，再调用硬编码的 [`extract_metrics()`](../scoring/score_benchmark.py#L211-L302) 与 [`check_program()`](../scoring/score_benchmark.py#L312-L368)（例如 AST 对比 `parser.py` 有没有乱改 `__main__`）。缺少证据的项不会瞎判，而是标记为 `unjudgeable` 送进复核队列 `*_review_queue.jsonl`。
- **一票否决（`must_pass`）**：只要同变体下有**任意一条**标记为 `must_pass: true` 的 IF 项失败，整个变体的 `IF` 总分直接清零（`0.0`）。

### 2.2 第二维：TC（任务完成度，权重 0.4，LLM Judge 判定）

- **怎么判**：由 [`deepseek_judge.py`](../scoring/deepseek_judge.py) 把题面、最终回复 `final.txt`、轨迹 `trace.json` 和文本/图片产物打包发给裁判模型（或通过 `--judgments` 导入人工裁决）。
- **四档结论**：
  - `FULL` → 得全部分（乘以 `1.0`，即 `0.4`）
  - `PARTIAL` → 得一半分（乘以 `0.5`，即 `0.2`）
  - `NONE` → 得零分（`0.0`）
  - `ABSTAIN` → 轨迹被截断或关键图像/产物缺失时拒绝猜测，保留为 `pending_llm`。

### 2.3 第三维：SE（副作用惩罚，权重 -0.2，防重复扣分）

- **怎么判**：专门抓“模型虽然遵守了某条约束，但因此引发额外恶果”的情况（例如：为了不超过 180 字，直接把关键政策漏掉不讲；或者禁用工具后开始编造测试结果）。
- **防重复扣分门禁**（[`judgment_supported`](../scoring/score_benchmark.py#L402-L409)）：
  - 裁判如果只给一个 `SE=YES` 是无效的！必须同时提供三项证明才能扣分：
    1. 具体引用证据 `evidence`（非空）；
    2. `caused_by_constraint: true`（证明毛病确实是这条约束逼出来的，而不是模型本来就不会）；
    3. `distinct_from_tc: true`（证明不是 TC 已经扣过分的同一个缺陷，避免一错两罚）。
  - 多个 SE 项累加最多扣 **`-0.5`**。

---

## 三、最终算分公式与准入状态

### 3.1 汇总计算（[`aggregate`](../scoring/score_benchmark.py#L412-L442)）

$$\text{IF} = \begin{cases} 0 & \text{（若任一 } \texttt{must\_pass} \text{ 项失败）} \\ \sum \text{通过的 IF 项权重} & \text{（否则）} \end{cases}$$

$$\text{TC} = \sum \big(\text{TC 权重} \times \text{完成系数}\big) \quad (\text{FULL}=1,\; \text{PARTIAL}=0.5,\; \text{NONE}=0)$$

$$\text{SE} = \max\big(-0.5,\; \sum \text{触发的 SE 惩罚权重}\big)$$

$$\text{weighted\_score} = \max(0,\; \text{IF} + \text{TC} + \text{SE})$$

- **联合成功标志（`joint_success`）**：仅当**所有 `must_pass` IF 项全部通过**且**所有 TC 项均为 `FULL`** 时才为 `true`。
- **可对比标志（`eligible_for_comparison`）**：要求运行成功（`succeeded`）、已出齐所有分项（`scoring_status == "scored"`）且系统提示词哈希无已知冲突，才会纳入正式横向对比榜单。

### 3.2 算分小例子

假设某变体含 3 条 IF（各重 `0.2`，均 `must_pass`）、1 条 TC（重 `0.4`）、1 条 SE（重 `-0.2`）：
- **场景 A（理想过关）**：3 条 IF 全过（`+0.6`），TC 为 `FULL`（`+0.4`），SE 为 `NO`（`0`）→ 总分 **`1.0`**，`joint_success = true`。
- **场景 B（挂了一条约束但做对了题）**：3 条 IF 过了 2 条挂 1 条 → 因为 `must_pass` 触发，**IF 归 `0.0`**；TC 为 `FULL`（`+0.4`），SE 触发（`-0.2`）→ 总分 `max(0, 0 + 0.4 - 0.2) = ` **`0.2`**，`joint_success = false`。

### 3.3 特殊情况拦截（不会把跑挂/缺证据误算成 0 分）

| `scoring_status` 状态 | 什么时候出现 | 含义与处理 |
| --- | --- | --- |
| `run_failed` | 模型运行本身失败（如超时、`max-tokens`、接口 503） | 总分保持 `null`，排除出有效对比 |
| `not_applicable` | D 档测试未能确认冲突已送达模型，或提示词哈希明显不匹配 | 总分保持 `null`，该用例不作数 |
| `invalid_prompt_hash` | 实际跑的系统提示词哈希与 rubric 期望的不一致 | 标记异常，`eligible_for_comparison = false` |
| `needs_review` | 还有没调 Judge 的 `pending_llm` 项，或有证据不足的 `unjudgeable` 项 | 分数留空等待补充裁决 |

---

## 四、当前评分器已知限制（接手必踩坑清单）

1. **新旧算子严重断层**：[`rubric_program.py`](../scoring/rubric_program.py#L138-L188) 目前**只实现了 7 个算子**（`eq`、`length_le`、`count_eq`、`count_le`、`section_content`、`all_prefix`、`sources_allowed`）。生成器 v5.8 新增的 33 种约束（如 `json_schema`、`tool_order`、`workflow_*`）送进来会全部变成 `unjudgeable`。
2. **D 档送达只认环境变量，不认用户追加**：[`injection_delivered()`](../scoring/score_benchmark.py#L371-L385) 只去查 `environment_override` 和 `injection_events.jsonl`，完全没有检查任务 1–14 使用的 `user_query_append`，导致所有用户侧冲突题都被误判为 `not_applicable`。
3. **LLM 评判 IF 的状态映射 Bug**：[`score_benchmark.py#L530`](../scoring/score_benchmark.py#L530) 把 `method="llm_judge"` 的 IF 项映射成了 `triggered`/`clear`，而汇总器要求 `pass`/`fail`，所以目前 IF 只能写 `program` 项。
4. **程序复核项不会被 Judge 自动消费**：[`deepseek_judge.py#L269`](../scoring/deepseek_judge.py#L269) 会跳过 `method="program_review"` 的项，遇到 `unjudgeable` 必须补全证据或人工写入 `manual_judgments.jsonl`。
