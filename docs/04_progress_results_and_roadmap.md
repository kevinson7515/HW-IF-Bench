# 项目现状、实测结果诊断与接手路线图

本文档基于对全部数据文件、源码和三模型运行目录的实地检查，回答接手最关心的 4 个问题：**做到哪了、已有模型跑得怎么样、暴露出哪些数据/工程 Bug、接下来先做什么。**

---

## 一、项目推进现状盘点

### 1.1 数据与推理进度（50 题全景）

| 批次 / 资产 | 题号范围 | 题数 | 基线指纹提取 | 变体与 Rubric 构建 | 模型实际推理 (`dsh-runs`) | 正式评分 (`scoring`) |
| --- | --- | --- | --- | --- | --- | --- |
| **Phase 1a（旧版）** | `1`–`14` | 14 | 完成 (`baseline-17`) | **已完成**（84 变体，旧版 v4.3/v4.4） | **已完成 3 模型**（各 84 变体） | **尚未正式出分** |
| **Phase 1b（原型）** | `15`–`17` | 3 | 完成（早期原型） | **已完成**（16 变体，旧版 `exec`） | **已完成 3 模型**（各 16 变体） | **尚未正式出分** |
| **Phase 2（纯指纹态）** | `18`–`50` | 33 | 完成 (`baseline-33`) | 纯指纹中间态（[`benchmark_groups_33.json`](../baseline_fingerprint/benchmark_groups_33.json)） | 未运行 | 未运行 |
| **全量重生成版（两版 250 变体）** | `1`–`50` | **50** | **50/50 完成** | **已完成单约束版**（`1111` 版 [`benchmark_baseline_all_20261111_155505.json`](../baseline_fingerprint/benchmark_baseline_all_20261111_155505.json) 与 `1110` 版 [`baseline_task_50/`](../baseline_task_50/)，各 **250 变体**） | **尚未运行** | 未运行 |
| **V2 扩库（`naq_50/`）** | `51`–`100` | 已构建 **25/50** | 待跑基线 | `id 51–75`（ChinaTravel 9 + BrowseComp-Plus 8 + DeepSearchQA 8）已就绪；`76–100` 留待合作者补齐 | 未运行 | 已配真值表 `tc_ground_truth_50.jsonl` |

### 1.2 三套核心代码库的最新状态

在 Python 3.11 下实测，生成器与评分器各自的离线单元测试全部通过：
- [`benchmark-group-generator/`](../benchmark-group-generator/)（**已同步至修订版 v5.10**，46 种策略）：**107 项测试全过**；且对 [`benchmark_baseline_all_20261111_155505.json`](../baseline_fingerprint/benchmark_baseline_all_20261111_155505.json) 与 `20261110` 版各 **250 条 IF 规则校验均为 0 报错**。
- [`scoring/`](../scoring/)：**21 项测试全过**，[`scoring/results/`](../scoring/results) 目前仅含 1 条合成 demo。
- [`deepseek-harness/`](../deepseek-harness/)：**已上传完整定制源码**（包含 `run.sh`、四模型入口、工具补丁、`scripts/run-benchmark.py` 及 `evaluation_only/` 外围配合体系）。

> **重要提醒**：虽然生成器 `v5.10` 与 250 变体数据已经对齐，但 **`deepseek-harness/scripts/run-benchmark.py` 当前默认禁用了系统提示词覆盖与冲突注入**，且 `scoring/` 仍只实现了 7 种旧算子——两端代码修通前仍不能直接跑通新版端到端评测。

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

3. **[高] 评分器与生成器版本脱节（生成器已对齐数据，评分器仍滞后）**
   - 随着 **v5.10** 同步完成，[`benchmark-group-generator/`](../benchmark-group-generator/)（46 种策略）现已 **100% 兼容** 两份 250 变体数据（250/250 条校验通过）；但 [`scoring/rubric_program.py`](../scoring/rubric_program.py#L138-L188) 仍然只实现了 Phase 1 用到的 **7 个旧算子**，其余 39 种新策略送进来会变成 `unjudgeable`。
   - 工具名映射表 `TOOL_ALIASES` 滞后：缺了 `sandbox_prepare`、`file_export`、`shell_exec`、`list_mcp_resources` 等映射。

4. **[高] Phase 1 旧版约束偏科，且部分规则“过严”导致失真**
   - Phase 1（1–14 题）近三成 IF 规则都在卡字符长度，把长篇综述（`t14` 限 1200 字）、97 份法律尽调（`t6` 限 1200 字）和纯数值问答（`t9` 强迫写文件到 `output/`）硬套限制，容易出现“所有模型一起轻微超字数”或逼出无效压缩。

5. **[高] Phase 1 运行目录缺 `results.jsonl`，且存在编号错位**
   - `benchmark-deepseek-17`、`glm-17`、`pangu92b-17` 根目录都缺 `results.jsonl`，`run_scoring.py` 无法直接扫描运行。
   - 这批运行发生在编号合并前，因此 `G-code-001/S1/result.json` 里仍记录着旧名字 `G-coding-parser-000` 和旧编号 `task_23`；`t3` 的 TC 文本里还写着旧路径 `task_4/policy.md`（现已改为 `task_3/`）。
   - 另外，`baseline-33/G-research-candidate-002/trace.jsonl` 第 87 行存在未转义换行符，解析该行会报 JSON 错误。

6. **[中] 早期原型 3 题（`t15–t17`）一半以上指标无法自动判分**
   - `G-kline-001`（K 线网格/红绿颜色/走势时段）和 `G-code-001`（空输入是否实际执行通过、是否只跑了内联副本）有 **8/14 项非 D 档 IF** 在 `score_benchmark.py` 中硬编码返回 `unavailable`，只能进人工/复核队列。

7. **[严重] `deepseek-harness` 新版源码主动禁用了变体提示词与冲突注入（且 `baseline_task_50/` 存在附件目录名拼写错位）**
   - 审阅最新同步的 [`deepseek-harness/scripts/run-benchmark.py`](../deepseek-harness/scripts/run-benchmark.py#L546-L553) 与 [`benchmark.README.zh.md`](../deepseek-harness/scripts/benchmark.README.zh.md#L42-L44) 发现：**当前版本的批跑器不创建也不加载 `prompt.patch.json`（强制写死 `variant_system_prompt_applied: false`），同时把 `user_query_append_applied` 和 `environment_override_applied` 硬编码为 `False`**。虽然它补齐了工作区 SHA-256 还原与 `results.jsonl` 生成，但直接拿它跑任何变体集只会重复执行无约束基线！
   - 此外，实测执行 `python3 baseline_task_50/prepare_task.py --verify` 会直接报错 `FileNotFoundError`：因为该目录下实际存放附件的目录名为单数 [`attached_file/`](../baseline_task_50/attached_file/)，而 `user_query_50.jsonl` 与 `prepare_task.py` 校验的均是复数 `attached_files/`。

8. **[高] 新版 250 条全量数据（`benchmark_baseline_all_20261111_155505.json`）存在 4 项结构局限**
   - **无 Tier B 且 C/D 控制变量失效**：全部 50 组统一走 `('A', 'A', 'A', 'C', 'D')` 单约束模式，且 `C/D` 均选用与 `A` 不同的新约束（复用率为 `0`），无法按旧版思路直接对比同一约束在长上下文/冲突下的性能衰减。
   - **SE 覆盖偏少且版本不一**：`20261111` 版仅 9 题（45/250 条）带 `SE` 项，而较早一天的 `20261110` 版则是 50 题均带 `SE`（50/250 条）。
   - **部分编程题 TC 证据面偏窄**：`20261111` 版有 195/250 条变体的 `TC` 仅要求 `["final_answer"]` 作为 `evidence_paths`，部分代码修改题未纳入 `workspace_diff`（后续应结合 [`baseline_task_50/evaluation_only/`](../baseline_task_50/evaluation_only/) 里的 SWE-bench / τ²-bench 真实单测补齐）。
   - **缺乏“思考过程约束”与日常搜索任务**：老 50 题均偏高门槛专业场景，且 IF 仅检验产出或外部工具顺序（`trace.json` 已记录 `reasoning_content`，尚未被消费）。

---

## 四、接手后的核心任务优先级（P0 → P2）

### P0（本周立即阻塞项）：打通评分器与 Harness 注入开关
1. **修复并跑通 Phase 1 三模型完整评分**：补全旧版 `benchmark-{deepseek,glm,pangu92b}-17` 缺失的 `results.jsonl`，在 `score_benchmark.py` 补上 `user_query_append_applied` 判定，跑通 `run_scoring.py` 输出旧版 100 变体的 **IF + TC + SE** 全量三维评分。
2. **修复 `deepseek-harness/scripts/run-benchmark.py` 的提示词与冲突注入**：恢复对 `effective_system_prompt`（生成并加载 `prompt.patch.json`，置 `variant_system_prompt_applied: true`）以及 `user_query_append` / `environment_override` 的真实下发（并在 `task.json` 如实记录 `*_applied: true`）。
3. **打通 `scoring/` 对 v5.10 的 46 种策略支持**：让 [`scoring/rubric_program.py`](../scoring/rubric_program.py) 直接桥接或同步 [`benchmark-group-generator/`](../benchmark-group-generator/) v5.10 的 `evaluate_rule()` 实现，并补全 `TOOL_ALIASES`；顺手修复 [`baseline_task_50/`](../baseline_task_50/) 下 `attached_file` → `attached_files` 目录命名以跑通 `prepare_task.py --verify`。

### P1（中期核心）：Pilot 验证新版 250 条，并合齐 V2 `naq_50/` 50 题
4. **小规模 Pilot 试跑新版 250 条（5–10 题）**：在修复注入开关后的 Harness 上抽样试测 `benchmark_baseline_all_20261111_155505.json`，并引入 `baseline_task_50/evaluation_only/` 验证第 18–31 题 SWE-bench / τ²-bench 的真实 `TC` 完成度。
5. **完成 V2 `naq_50/` 剩余 25 题并上线“思考过程约束”**：配合合作者补齐 `naq_50/` 的 `id 76–100`（消费对比、医疗健康、社会民生）并跑通这 50 条的基线；同步在 `scoring/` 与生成器中新增从 `trace.json`（`reasoning_content`）提取“首轮工具前思考片段”的适配器与思考类约束模板。

### P2（补全闭环）：全量多模型横向评测
6. **全量模型跑测与对比**：使用修复后的 Harness 跑通修复版 Tier D、补齐未测的 `openPangu-v21-pro`（[`pangu.patch.yml`](../dsh-config/pangu.patch.yml)），以及最终 **“老 50 专业题 + 新 50 日常搜索题”** 完整榜单评测。
