# 项目现状、实测结果诊断与接手路线图

本文档基于对全部数据文件、源码和三模型运行目录的实地检查，回答接手最关心的 4 个问题：**做到哪了、已有模型跑得怎么样、暴露出哪些数据/工程 Bug、接下来先做什么。**

---

## 一、项目推进现状盘点

### 1.1 数据与推理进度（50 题全景）

| 批次 | 题号范围 | 题数 | 基线指纹提取 | 变体与 Rubric 构建 | 模型实际推理 (`dsh-runs`) | 正式评分 (`scoring`) |
| --- | --- | --- | --- | --- | --- | --- |
| **Phase 1a** | `1`–`14` | 14 | 完成 (`baseline-17`) | **已完成**（84 变体，旧版 v4.3/v4.4） | **已完成 3 模型**（各 84 变体） | **尚未正式出分** |
| **Phase 1b** | `15`–`17` | 3 | 完成（早期原型） | **已完成**（16 变体，旧版 `exec`） | **已完成 3 模型**（各 16 变体） | **尚未正式出分** |
| **Phase 2** | `18`–`50` | 33 | 完成 (`baseline-33`) | **未生成**（仅抽好 [`benchmark_groups_33.json`](../baseline_fingerprint/benchmark_groups_33.json)） | 未运行 | 未运行 |
| **合计** | `1`–`50` | **50** | **50/50 完成** | **17/50 完成（100 变体）** | **仅前 17 题跑了 3 模型** | [`scoring/results/`](../scoring/results) **仅含 1 条 demo** |

### 1.2 两套代码库的离线测试状态

在 Python 3.11 下实测，生成器与评分器各自的离线单元测试全部通过：
- [`benchmark-group-generator/`](../benchmark-group-generator/)（v5.8）：**102 项测试全过**。
- [`scoring/`](../scoring/)：**21 项测试全过**。

> 但要注意：这两套代码是在 **2026-11-10** 刚重整上传的，**还没有和 `baseline_fingerprint/` 里的真实数据做过端到端联调**。

---

## 二、已评估模型实测分析（Phase 1：17 组 × 100 变体）

目前已完成推理的 3 个模型为 **`deepseek-v4-pro`**、**`glm-5.3`**、**`pangu92b_wandr`**（配置里的 `openPangu-v21-pro` 还未跑）。

由于 3 个运行目录都缺了根目录 `results.jsonl`，此前一直没跑过 `scoring/`。我们通过脚本在内存中补齐映射后直接调用 `score_benchmark.py` 的程序规则逻辑，得到了三模型的 **运行稳定性与 IF（指令遵循）初评数据**（TC 和 SE 尚待跑 LLM Judge）：

| 对比维度 | `deepseek-v4-pro`<br>(10-24 运行) | `glm-5.3`<br>(11-03 运行) | `pangu92b_wandr`<br>(10-25 运行) |
| --- | --- | --- | --- |
| **运行正常结束 (`succeeded`)** | **99 / 100** | **88 / 100** | **77 / 100** |
| **运行中断失败 (`run_failed`)** | **1 例**（1 次 `max-tokens`） | **12 例**（3 次 503 无渠道、3 次内容安全拦截、4 次账户欠费、2 次 `max-tokens`） | **23 例**（21 次 `max-tokens`、2 次上下文超限） |
| **全部 16 条 D 档冲突注入有效性** | **0 / 16 生效** | **0 / 16 生效** | **0 / 16 生效** |
| **Task 1–14 有效 A/B/C 变体 IF 通过率**<br>*(仅统计成功跑完的题)* | **61 / 69 (88.4%)**<br>*(单条规则：87 过 / 8 挂)* | **44 / 61 (72.1%)**<br>*(单条规则：71 过 / 18 挂)* | **40 / 51 (78.4%)**<br>*(单条规则：56 过 / 13 挂)* |
| **Task 1–14 A/B/C 端到端通过率**<br>*(以全量 70 题为分母)* | **61 / 70 (87.1%)** | **44 / 70 (62.9%)** | **40 / 70 (57.1%)** |
| **Task 15–17（原型 3 题）IF 状态** | 6 过, 0 挂, **8 无法自动判**, 2 不适用 | 5 过, 0 挂, **8 无法自动判**, 2 不适用 | 6 过, 0 挂, **8 无法自动判**, 2 不适用 |

### 结果解读：和预期有什么出入？

1. **Pangu92b 在长文件/复杂代码任务上容易陷入“死循环”，导致端到端可用率垫底**：
   - 表面上看 Pangu92b 在“成功跑完的题目”上 IF 通过率（78.4%）似乎高于 GLM（72.1%），但那是因为它把最难的 `G-coding-django-11417` 和 `G-legal-cb100-*`（97 份文件）几乎全部跑挂了（23/100 失败）。
   - 查看轨迹发现，Pangu92b 动辄连续调用 100–130 次工具且夹杂二三十次工具报错（如 `G-legal-cb100-031/S3` 连续 `read` 105 次、报错 27 次直到上下文爆炸）。
2. **GLM 的失败主要是外部平台/风控问题，而非模型能力本身**：
   - GLM 的 12 次失败里有 10 次属于网关 503 无可用渠道、账户欠费 `Arrearage`，以及历史类题目（`G-research-query-032`：1937–1949 抗战史学研究）触发平台内容安全过滤（`DataInspectionFailed`）。
3. **IF 违规高度集中在“字数超标”和“管不住手调禁用工具”**：
   - DeepSeek 仅挂了 8 条 IF 规则，其中 **7 条是字数略微超出上限**（如限制 1200 字实际写了 1215–1545 字），**1 条是工具惯性违禁**（`G-legal-cb100-031/S2` 要求禁用 `task_planning`，但 DeepSeek 第一步就习惯性调了 `todo_write`）。
   - GLM 挂掉的 18 条 IF 规则里也是 **12 条超字数**、**5 条误调禁用工具**，外加 1 条在沙箱代码里偷偷用 `urllib` 访问 `github.com` 触犯域名黑名单。
4. **实锤观察到“遵守约束却把原任务搞砸”的副作用现象**：
   - 最典型的是 `G-customer-airline-000/S1`（限制回复 `<= 180` 字）：DeepSeek（83 字）和 GLM（119 字）能在字数内把退款条件说清楚；而 `pangu92b` 为卡在 180 字内只回了一句 **46 个字的提问**，把所有 24 小时政策解释和例外条件全删光了——完美印证了为什么需要 **TC + SE** 评估。

---

## 三、实测暴露出的 7 大数据与工程问题

这些问题直接影响后续评估的可信度和 Phase 2 能否顺利推进：

1. **[严重] 全部 48 条 Tier D 冲突对抗测试实际上“根本没跑冲突”**
   - 检查三模型运行目录的 `task.json` 发现：第 1–14 题的 `user_query_append_applied`（是否已追加用户冲突指令）**全部为 `false`**，发给模型的 `effective_query` 里压根没有冲突话术；第 16–17 题的 `environment_override_applied` **也全部为 `false`**。
   - 同时评分器 `score_benchmark.py` 也只认 `environment_override`，不认 `user_query_append`。这意味着 **Phase 1 所有 Tier D 成绩目前都是无效的**。

2. **[严重] 50 道题的 `tools` 字段只填了“基线用过的工具”，不是“环境实际开放的工具”**
   - 核对全量 50 题发现，`group["tools"]` 100% 等于 `set(baseline_fingerprint["tool_seq"])`。导致第 37/39/43/45/47 题的 `tools` 里**只写了 `["file_read"]` 1 个工具**。
   - 这会直接卡死 v5.8 生成器：单工具任务无法生成禁用工具、限制工具总数、规定先后顺序或先查目录等策略；同时模型在真实运行中其实还能调用其他未列出的工具（例如 GLM 在 `t12` 仅声明了搜索工具的情况下，实际写出了 `output/` 文件）。

3. **[高] 生成器 v5.8 与评分器 `scoring/` 之间存在严重版本脱节**
   - `benchmark-group-generator` v5.8 已经支持 **40 种策略**，但 [`scoring/rubric_program.py`](../scoring/rubric_program.py#L138-L188) 只写了 Phase 1 用到的 **7 个算子**。如果直接用 v5.8 生成 Phase 2（33 题），大部分新规则在评分器里都会变成 `unjudgeable`（无法自动评分）。
   - 工具名映射表 `TOOL_ALIASES` 也未同步：Phase 2 `benchmark_groups_33.json` 里新出现了 `sandbox_prepare`、`file_export`、`shell_exec`、`list_mcp_resources`，但代码里的映射表缺了 `mcp__e2b__prepare_environment -> sandbox_prepare`、`mcp__e2b__export_file -> file_export` 和 `bash/shell -> shell_exec`。

4. **[高] Phase 1 旧版约束偏科，且部分规则“过严”导致失真**
   - Phase 1（1–14 题）近三成 IF 规则都在卡字符长度，把长篇综述（`t14` 限 1200 字）、97 份法律尽调（`t6` 限 1200 字）和纯数值问答（`t9` 强迫写文件到 `output/`）硬套限制，容易出现“所有模型一起轻微超字数”或逼出无效压缩。

5. **[高] Phase 1 运行目录缺 `results.jsonl`，且存在编号错位**
   - `benchmark-deepseek-17`、`glm-17`、`pangu92b-17` 根目录都缺 `results.jsonl`，`run_scoring.py` 无法直接扫描运行。
   - 这批运行发生在编号合并前，因此 `G-code-001/S1/result.json` 里仍记录着旧名字 `G-coding-parser-000` 和旧编号 `task_23`；`t3` 的 TC 文本里还写着旧路径 `task_4/policy.md`（现已改为 `task_3/`）。
   - 另外，`baseline-33/G-research-candidate-002/trace.jsonl` 第 87 行存在未转义换行符，解析该行会报 JSON 错误。

6. **[中] 早期原型 3 题（`t15–t17`）一半以上指标无法自动判分**
   - `G-kline-001`（K 线网格/红绿颜色/走势时段）和 `G-code-001`（空输入是否实际执行通过、是否只跑了内联副本）有 **8/14 项非 D 档 IF** 在 `score_benchmark.py` 中硬编码返回 `unavailable`，只能进人工/复核队列。

7. **[中] `deepseek-harness` 源码不在当前仓库**
   - [`deepseek-harness/`](../deepseek-harness/) 目前是个空目录，涉及修改 D 档注入逻辑或给 Pangu92b 加工具死循环熔断时，需要向团队拉取真实的 Harness 代码库。

---

## 四、接手后的核心任务优先级（P0 → P2）

### P0（本周可立即做）：先把 Phase 1 三模型的完整三维分数跑出来
1. **生成缺失的 `results.jsonl`**：写个小脚本汇总 `benchmark-{deepseek,glm,pangu92b}-17/*/*/result.json`，把 `G-coding-parser-000` 等旧 ID 映射回 `benchmark_groups_17.json` 的标准 `group_id`。
2. **修复 `score_benchmark.py` 的 D 档送达判定**：增加对 `user_query_append` 类型的核验（检查 `task.json` 的 `user_query_append_applied` 是否为 `true`），确保目前未送达的 D 档如实标为 `not_applicable`，不混入正式对比。
3. **跑通 LLM Judge，产出第一份完整排行榜**：复制配置 `scoring/config.local.json`，运行 `run_scoring.py` 完成三模型在 A/B/C 档上的 **TC 与 SE 评分**（含 K 线图视觉核验），首次把 `IF + TC + SE` 三维分算齐。

### P1（中期核心）：修通工具链并生成 Phase 2（33 题）高质量数据
4. **补全 `benchmark_groups_33.json` 的真实 `tools` 清单**，并修复 `G-research-candidate-002/trace.jsonl` 第 87 行格式异常。
5. **对齐算子与工具别名**：在 `base_policies.py` 和 `rubric_program.py` 补全 `sandbox_prepare`、`file_export`、`shell_exec` 映射；让 `scoring/rubric_program.py` 同步或直接复用生成器 v5.8 的全部 40 种策略评估逻辑。
6. **用 v5.8 生成 Phase 2（第 18–50 题）并做小规模人工 Pilot**：先按 `--task-ids` 每类抽 1 题试跑 [`quick_run.py`](../benchmark-group-generator/quick_run.py)，确认约束自然、不破坏任务可解性后，再全量生成并合并成 50 题完整评测集。

### P2（补全闭环）：修复执行侧 Harness 并扩展测试
7. **拉取并修复 `deepseek-harness` 仓库**：排查为何 `user_query_append_applied` / `environment_override_applied` 均为 `false`，修好 D 档注入与回执日志 `injection_events.jsonl`，同时为高错误循环增加步数熔断。
8. **重跑与扩容**：补跑修复后的 Tier D、跑通尚未测试的 `openPangu-v21-pro`（[`pangu.patch.yml`](../dsh-config/pangu.patch.yml)），以及最终 50 题全量 Benchmark 评测。
