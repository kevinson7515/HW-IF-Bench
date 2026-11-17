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
| **Harness（执行框架）** | 负责把题目发给大模型、替模型执行读写文件/网页搜索/E2B 沙箱/视觉桥接等工具调用、保护工作区快照并录下轨迹的运行环境 | [`deepseek-harness/`](../deepseek-harness/)（已合入完整自定义源码、[`dsh-config/`](../dsh-config/) 及 [`scripts/run-benchmark.py`](../deepseek-harness/scripts/run-benchmark.py)） |
| **Baseline Fingerprint（基线指纹）** | 先让基准模型（`deepseek-v4-pro`）**不加任何额外约束**跑一遍原始任务，记录它“默认习惯怎么做”（用了哪些工具、查了哪些网站、回复多长等） | [`baseline-17/`](../baseline_fingerprint/dsh-runs/baseline-17/)、[`baseline-33/`](../baseline_fingerprint/dsh-runs/baseline-33/) 及抽取出的 `baseline_fingerprint` 字段 |
| **Variant（变体 / S1~S6）** | 围绕同一道原始任务，基于基线指纹故意加上**反着它默认习惯来的约束**，派生出的不同考题版本 | 旧版 [`benchmark_groups_17.json`](../baseline_fingerprint/benchmark_groups_17.json)（100 变体）、新版全量 [`benchmark_baseline_all_20261111_155505.json`](../baseline_fingerprint/benchmark_baseline_all_20261111_155505.json)（250 变体）及 [`baseline_task_50/`](../baseline_task_50/) 下 `20261110` 版 |
| **Rubric（评分细则）** | 挂在每个变体下面的“阅卷标准列表”，写明哪些项用代码自动判（IF）、哪些项用裁判模型判（TC / SE），以及每项占多少分 | 每个变体里的 `rubric` 数组 |
| **Generator & Scoring** | 两套核心工具：**生成器**负责把“原始任务 + 基线指纹”变成“带变体和 Rubric 的评测集”；**评分器**负责读取模型跑完的轨迹打分 | [`benchmark-group-generator/`](../benchmark-group-generator/) 和 [`scoring/`](../scoring/) |

---

## 2. 仓库目录与文件定位

```text
HW-IF-Bench/
├── README.md                        # 原始项目简介与集群运行命令说明
├── dsh-config/                      # 4 个待测模型的接口配置（DeepSeek / GLM / Pangu92b / openPangu-v21-pro）
├── deepseek-harness/                # [已同步完整源码] Agent 批处理执行框架
│   ├── run.sh & run_*.sh            # Slurm 集群入口（含 deepseek/glm/pangu/pangu92b/run_70）
│   ├── batch-tools.patch.yml        # Serper 联网检索、E2B 沙箱 MCP、Pangu 视觉桥接补丁
│   ├── scripts/run-benchmark.py     # Benchmark 批跑器（含 SHA-256 工作区保护与自动恢复）
│   └── user_query_70.jsonl          # Harness 端自带的 70 题独立冒烟/指令测试集（非本项目 50 题）
├── baseline_fingerprint/            # 第 1–50 题基线产物、三模型跑测日志与最新版 250 变体
│   ├── user_query_50.jsonl          # 全量 50 道原始任务清单（id 1~50）
│   ├── attached_files/              # task_1 ~ task_50 各自附带的源码仓库、PDF 财报、法律卷宗、客服环境包
│   ├── benchmark_groups_17.json     # Phase 1 旧版：第 1~17 题（已生成 100 个变体并跑过 3 模型）
│   ├── benchmark_groups_33.json     # Phase 2 中间态：第 18~50 题（只有基线指纹，无变体）
│   ├── benchmark_baseline_all_20261111_155505.json  # 最新全量 50 题重生成版（250 条单约束变体，暂未实测）
│   └── dsh-runs/                    # Phase 1 三模型与基线运行产物目录
├── baseline_task_50/                # [新增] 50 题标准打包输入与官方评测真值
│   ├── prepare_task.py              # 校验与展开工作区脚本（注：目录名 attached_file 缺 s 暂会报错）
│   ├── source_manifest_50.json      # 50 题附件 SHA-256 校验清单
│   ├── evaluation_only/             # 第 18–25 题 SWE-bench、第 26–31 题 τ²-bench 官方评分依据
│   └── benchmark_baseline_all_20261110_215942.json  # 11-10 版全量 250 变体生成结果
├── naq_50/                          # [新增] V2 扩库区：拟新增 50 条日常/真实搜索题（id 51~100）
│   ├── user_query_naq50.jsonl       # 已构建前 25 条（id 51~75：ChinaTravel 9 + BrowseComp-Plus 8 + DeepSearchQA 8）
│   ├── tc_ground_truth_50.jsonl     # 对应 TC 客观答案 / DSL 程序校验真值（预留 76~100 给合作者）
│   └── attached_files/              # task_51~59 城市沙箱切片 + task_60~67 混淆网页语料包（共 312 个文件）
├── data/                            # [.gitignore 忽略] 本地原始外部数据集下载源（ChinaTravel/Sandbox/AssistantBench/deepsearchqa）
├── benchmark-group-generator/       # [已同步至 v5.10] 评测变体生成器（107 项单元测试全过）
│   ├── quick_run.py                 # 一键批处理入口（支持 --check 校验、断点续跑）
│   ├── generator.py                 # 生成、审查、组装的核心流程代码
│   ├── base_policies.py             # 20 种基础约束模板
│   ├── policies.py                  # 14 种高阶约束 + 变体组合规划器
│   ├── workflow_policies.py         # 12 种流程/工作流控制约束（含新增 6 种多阶段工具流）
│   ├── policy_catalog.json          # 全部 46 种约束策略与 25 个指令族清单
│   └── 指令种类说明.md              # v5.10 全量 46 种策略说明
├── scoring/                         # [独立评分工具] 运行后打分器（21 项单元测试通过，暂仅支持 7 种基础算子）
│   ├── run_scoring.py               # 批量入口：扫描运行目录 → 程序评分 → 调用 LLM Judge → 输出 summary.csv
│   ├── score_benchmark.py           # 单次运行评分主逻辑（算分、状态判定、导出待人工/模型复核队列）
│   ├── rubric_program.py            # 程序规则解释器（当前只支持 7 种基础算子）
│   ├── deepseek_judge.py            # 调用大模型裁判评判 TC 和 SE
│   └── results/                     # 评分结果输出目录（目前只有 1 条合成示例 demo 的输出）
└── docs/                            # 接手文档（含个人草稿 my_thinking.md）
```

---

## 3. 项目推进时间线与现状速览

整个项目目前已经集齐 **“生成器 v5.10 + 执行器 Harness 源码 + 50 题完整打包资料 + 250 条新版全量变体 + V2 日常搜索扩库前 25 题”**，当前核心卡点在于 **执行侧（`run-benchmark.py`）和评分侧（`scoring/`）的闭环对齐**：

| 阶段 | 时间 | 做了什么 | 现在卡在哪 / 需要注意什么 |
| --- | --- | --- | --- |
| **Phase 0（早期原型）** | 10 月中旬前 | 手工构建了 3 道原型题（`G-kline-001`、`G-search-001`、`G-code-001`） | 并入 `benchmark_groups_17.json` 的第 15~17 题；依赖旧版专属判分逻辑 |
| **Phase 1（17 题测试）** | 10-18 ~ 11-03 | 跑了 3 个模型（100 变体），产出在 `baseline_fingerprint/dsh-runs/` | **正式评分（TC/SE）从未跑过**；三模型 **D 档冲突注入均未生效** |
| **Phase 2（50 题与工具链）** | 11-06 ~ 11-14 | 扩充至 50 题（`baseline_task_50/` 含官方 `evaluation_only/` 真值），并合入全量 250 变体数据集 | `benchmark_baseline_all_20261111_155505.json`（及 `1110` 版）**尚未实测**；`scoring/` 仍停留在 7 种旧算子 |
| **代码同步完成** | 11-17 合入 | 仓库同步了 **生成器 v5.10**（46 种策略，**全量 250 条 IF 校验 0 报错**）和完整 **`deepseek-harness/` 源码** | **关键发现**：新同步的 `run-benchmark.py` **刻意关闭了系统提示词注入（`variant_system_prompt_applied: false`）与冲突注入**，开跑前必须改回启用！ |
| **V2 扩库（`naq_50/`）** | 11-17 | 新增前 **25 条**日常/真实搜索题（`id 51~75`：ChinaTravel 9 + BrowseComp-Plus 8 + DeepSearchQA 8） | 剩余 `id 76~100` 由合作者补齐；后续需补充“思考过程约束”能力 |

---

## 4. 文档阅读顺序建议

1. **[`01_tasks_and_constraints.md`](./01_tasks_and_constraints.md)** —— 先搞清楚 **“考什么题”** 和 **“加什么约束”**（50 题的 5 大领域来源、反默认约束怎么来、40 种约束和 A–D 四档压力是什么）。
2. **[`02_data_construction_pipeline.md`](./02_data_construction_pipeline.md)** —— 搞清楚 **“数据是怎么造出来的”**（先解释输入/输出 JSON 每个字段的含义，再用 4 个步骤讲透生成器 v5.8 的工作流程）。
3. **[`03_evaluation_and_scoring.md`](./03_evaluation_and_scoring.md)** —— 搞清楚 **“模型怎么跑、分数怎么算”**（运行产物里每个文件的作用、IF/TC/SE 怎么打分和汇总、当前评分器的限制）。
4. **[`04_progress_results_and_roadmap.md`](./04_progress_results_and_roadmap.md)** —— 直接看 **“现有结果怎么样、踩了哪些坑、接手先干啥”**（含 3 模型 100 变体的实测通过率统计、暴露的 7 个具体问题及 P0/P1/P2 行动清单）。
