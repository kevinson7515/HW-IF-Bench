# HW-IF-Bench 项目总览与接手指南

> 本文档面向初次接手 **HW-IF-Bench** 的同学，用最直观的方式说明：**这个项目要测什么、代码和数据分别放在哪、目前推进到哪一步，以及应该按什么顺序阅读其余文档。**

---

## 1. 一句话理解项目目标

**HW-IF-Bench** 用来评测大模型 Agent（写代码、深度检索、财报/法律分析、客服业务流）在多轮工具调用过程中，**“听不听话（遵循约束）”** 以及 **“听话之后还能不能把事办好”**。

评测同时看三件事：
1. **指令遵循（IF, Instruction Following）**：你额外加给模型的限制（例如“不能用 `web_fetch`”“字数不能超过 800”“结果必须保存在 `output/` 目录”），模型有没有严格做到？
2. **任务完成度（TC, Task Completion）**：在遵守这些限制的前提下，用户原本交代的任务（如修复 Bug、算出财务指标）到底有没有真正做对？
3. **副作用（SE, Side Effect）**：模型有没有**因为死板遵守限制**而把任务搞砸，或引入额外的破坏（比如为了凑 180 字上限把关键规则全删了、或者因为不让用某个工具就开始胡编结果）？

### 核心术语小词典（先看这 6 个词，后面就不迷糊）

| 术语 | 通俗解释 | 在项目里对应的东西 |
| --- | --- | --- |
| **Task（原始任务）** | 一道最原始的用户考题，不包含任何额外约束 | [`user_query_50.jsonl`](../baseline_fingerprint/user_query_50.jsonl) 中的每一行（共 50 题） |
| **Harness（执行框架）** | 负责把题目发给大模型、替模型执行读写文件/网页搜索/Python沙箱等工具调用、并把过程录下来的运行环境 | [`deepseek-harness/`](../deepseek-harness/)（本仓库中为空引用，运行时配置在 [`dsh-config/`](../dsh-config/)） |
| **Baseline Fingerprint（基线指纹）** | 先让基准模型（`deepseek-v4-pro`）**不加任何额外约束**跑一遍原始任务，记录它“默认习惯怎么做”（用了哪些工具、查了哪些网站、回复多长等） | [`baseline-17/`](../baseline_fingerprint/dsh-runs/baseline-17/)、[`baseline-33/`](../baseline_fingerprint/dsh-runs/baseline-33/) 及抽取出的 `baseline_fingerprint` 字段 |
| **Variant（变体 / S1~S6）** | 围绕同一道原始任务，基于基线指纹故意加上**反着它默认习惯来的约束**，派生出的不同考题版本（分 A/B/C/D 四档压力） | [`benchmark_groups_17.json`](../baseline_fingerprint/benchmark_groups_17.json) 中每组下的 `variants` 列表 |
| **Rubric（评分细则）** | 挂在每个变体下面的“阅卷标准列表”，写明哪些项用代码自动判（IF）、哪些项用裁判模型判（TC / SE），以及每项占多少分 | 每个变体里的 `rubric` 数组 |
| **Generator & Scoring** | 两套核心工具：**生成器**负责把“原始任务 + 基线指纹”变成“带变体和 Rubric 的评测集”；**评分器**负责读取模型跑完的轨迹打分 | [`benchmark-group-generator/`](../benchmark-group-generator/) 和 [`scoring/`](../scoring/) |

---

## 2. 仓库目录与文件定位

```text
HW-IF-Bench/
├── README.md                        # 原始项目简介与集群运行命令说明
├── dsh-config/                      # 4 个待测模型的接口配置（DeepSeek / GLM / Pangu92b / openPangu-v21-pro）
├── deepseek-harness/                # [空目录] 实际 Agent 执行框架的 Git submodule 指针，代码尚未检出
├── baseline_fingerprint/            # 全部数据资产与模型运行结果
│   ├── user_query_50.jsonl          # 全量 50 道原始任务清单（id 1~50）
│   ├── attached_files/              # task_1 ~ task_50 各自附带的源码仓库、PDF 财报、法律卷宗、客服环境包
│   ├── benchmark_groups_17.json     # Phase 1：第 1~17 题（已生成 100 个变体和 Rubric）
│   ├── benchmark_groups_33.json     # Phase 2：第 18~50 题（只有基线指纹，尚未生成变体）
│   └── dsh-runs/                    # 运行产物总目录
│       ├── baseline-17/             # 第 1 批无约束基线运行记录
│       ├── baseline-33/             # 第 2 批无约束基线运行记录
│       ├── benchmark-deepseek-17/   # deepseek-v4-pro 跑前 17 题（100 变体）的结果
│       ├── benchmark-glm-17/        # glm-5.3 跑前 17 题（100 变体）的结果
│       └── benchmark-pangu92b-17/   # pangu92b_wandr 跑前 17 题（100 变体）的结果
├── benchmark-group-generator/       # [最新版 v5.8] 评测变体生成器（102 项单元测试通过）
│   ├── quick_run.py                 # 一键批处理入口（支持 --check 校验、断点续跑）
│   ├── generator.py                 # 生成、审查、组装的核心流程代码
│   ├── base_policies.py             # 20 种基础约束模板
│   ├── policies.py                  # v5 新增 14 种常规约束 + 变体组合规划器
│   ├── workflow_policies.py         # v5.4 新增 6 种过程/流程类约束
│   └── policy_catalog.json          # 全部 40 种约束策略与 25 个指令族清单
├── scoring/                         # [独立评分工具] 运行后打分器（21 项单元测试通过，暂仅跑过 1 条 demo）
│   ├── run_scoring.py               # 批量入口：扫描运行目录 → 程序评分 → 调用 LLM Judge → 输出 summary.csv
│   ├── score_benchmark.py           # 单次运行评分主逻辑（算分、状态判定、导出待人工/模型复核队列）
│   ├── rubric_program.py            # 程序规则解释器（当前只支持 7 种基础算子）
│   ├── deepseek_judge.py            # 调用大模型裁判评判 TC 和 SE
│   └── results/                     # 评分结果输出目录（目前只有 1 条合成示例 demo 的输出）
└── docs/                            # 你正在看的接手文档
```

---

## 3. 项目推进时间线与现状速览

整个项目由前任同学分批搭建，目前正处于 **“Phase 1 跑完推理 + 工具链刚完成大升级 + 两端尚未接上、Phase 2 待生成”** 的交接节点：

| 阶段 | 时间 | 做了什么 | 现在卡在哪 / 需要注意什么 |
| --- | --- | --- | --- |
| **Phase 0（早期原型）** | 10 月中旬前 | 手工构建了 3 道原型题（`G-kline-001`、`G-search-001`、`G-code-001`） | 后来被并入 `benchmark_groups_17.json` 的第 15~17 题；它们的评分规则是旧版专属代码，很多指标目前无法自动打分 |
| **Phase 1（17 题构建与测试）** | 10-18 ~ 11-03 | 跑通第 1 批基线 → 用旧版生成器（v4.3/v4.4）生成第 1~14 题，合并成 **17 组共 100 个变体** → 跑了 DeepSeek、Pangu92b、GLM 三个模型 | **推理文件都在，但正式评分（TC/SE）从未跑过**；而且排查发现三模型的 **D 档冲突测试全部没有生效** |
| **Phase 2（扩充到 50 题）** | 11-06 | 扩充至 50 题，跑完了第 18~50 题的基线运行（`baseline-33`），并抽取出 [`benchmark_groups_33.json`](../baseline_fingerprint/benchmark_groups_33.json) | **只有基线指纹，还没有生成变体和 Rubric** |
| **工具链重构升级** | 11-10 | 上传了重写升级后的 **v5.8 生成器**（40 种约束）和独立 **评分器 `scoring/`** | **新工具链还没在真实数据上联调**：`scoring/` 只实现了 7 种旧算子，接不住 v5.8 生成的新约束；且历史数据缺汇总清单 `results.jsonl` |

---

## 4. 文档阅读顺序建议

1. **[`01_tasks_and_constraints.md`](./01_tasks_and_constraints.md)** —— 先搞清楚 **“考什么题”** 和 **“加什么约束”**（50 题的 5 大领域来源、反默认约束怎么来、40 种约束和 A–D 四档压力是什么）。
2. **[`02_data_construction_pipeline.md`](./02_data_construction_pipeline.md)** —— 搞清楚 **“数据是怎么造出来的”**（先解释输入/输出 JSON 每个字段的含义，再用 4 个步骤讲透生成器 v5.8 的工作流程）。
3. **[`03_evaluation_and_scoring.md`](./03_evaluation_and_scoring.md)** —— 搞清楚 **“模型怎么跑、分数怎么算”**（运行产物里每个文件的作用、IF/TC/SE 怎么打分和汇总、当前评分器的限制）。
4. **[`04_progress_results_and_roadmap.md`](./04_progress_results_and_roadmap.md)** —— 直接看 **“现有结果怎么样、踩了哪些坑、接手先干啥”**（含 3 模型 100 变体的实测通过率统计、暴露的 7 个具体问题及 P0/P1/P2 行动清单）。
