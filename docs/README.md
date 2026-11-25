# HW-IF-Bench 项目总览与使用指南（V2 整合版）

> **HW-IF-Bench** 用来评测大模型 Agent 在多轮工具调用过程中，**“听不听话（IF, Instruction Following）”** 与 **“听话之后还能不能把事办好（TC, Task Completion）”**。
>
> 当前仓库已完成 V1/V2 整合与历史归档：**[`benchmark/`](../benchmark/)** 是唯一主数据目录，**[`seed_pipeline/`](../seed_pipeline/)** 是唯一现行构建与打分主引擎，历史 v5.10 模板代码与拆分目录已完整留存至 [`archive/`](../archive/)。

---

## 1. 仓库目录结构（现行主线）

```text
HW-IF-Bench/
├── benchmark/                           # 【唯一主数据目录：合并老 50 + 新 48 = 98 题】
│   ├── queries_98.jsonl                 # 统一 98 道母题（id 1~98，含 source_split）
│   ├── tc_ground_truth_98.jsonl         # 统一 TC 客观真值
│   ├── attached_files/                  # 统一 task_1 ~ task_67 共 62 个任务附件包
│   ├── baseline_v4pro_98.json           # 统一 98 题 v4-pro 基线指纹与轨迹证据（自包含）
│   └── releases/hw_if_bench_v2_588/     # 正式冻结的 588 条评测集 + 审计报告 + 人工复核包
├── seed_pipeline/                       # 【唯一现行构建与自动打分引擎】
│   ├── workflow_seeds.yaml              # 44 条声明式种子库（4 大流程原语 L=2~5 + 思考 + 产物）
│   ├── profiler.py                      # 零手工标注任务能力画像器（支持 98 题及任意新 Query）
│   ├── scheduler.py                     # 4 阶段反默认回放 + MRV 全局配额调度 + V1/V2 分层配平 + 审计自愈
│   ├── verifiers.py                     # 纯 Python 确定性校验器（生成期反默认与评测期打分同源）
│   ├── llm_enhancer.py                  # 可插拔 LLM 语义增强层（哈希缓存 + Token 硬守卫 + 探活）
│   ├── run_seed_generator.py            # 约束数据集生成入口
│   ├── score_seed_runs.py               # 运行后自动 IF/TC 打分与研究报表生成
│   ├── export_human_review.py           # 导出人工审查包（高危切片 MD + 抽样 MD + 588 条 CSV）
│   └── tests/test_seed_pipeline.py      # 单元与 98 题全量集成测试
├── deepseek-harness/                    # Agent 批处理执行框架（已开启 personaSuffix & Tier D 注入 + 断点续跑）
├── dsh-config/                          # 模型配置补丁（deepseek / deepseek-v4.1-flash-1017 / glm / pangu）
├── docs/                                # 现行文档
│   ├── README.md                        # 本总览指南
│   └── seed_library_and_v2_data_report.md # V2 工作流种子库方法论与 588 条定稿数据汇报文档
├── scripts/                             # [.gitignore] 本地一键启动脚本（run_seed_generation.sh / run_seed_eval.sh）
├── dsh-runs/                            # [.gitignore] 本地基线与评测运行产物目录
└── archive/                             # 【历史归档留存区】旧版 v5.10 生成器、旧 scoring、旧拆分数据与 Phase 1/2 文档
```

---

## 2. 常用一键操作命令

```bash
# 1. 运行全套单元与 98 题集成测试
python3 -m unittest seed_pipeline/tests/test_seed_pipeline.py -v

# 2. 生产 / 重生成 98 题 588 条约束集（或对任意外部新 Query JSONL 生成）
bash scripts/run_seed_generation.sh --with-llm --llm-workers 4
bash scripts/run_seed_generation.sh --input-jsonl /path/to/queries.jsonl --with-llm

# 3. 启动评估（默认模型 deepseek-v4.1-flash-1017，可用 --model v4-pro 切换）
bash scripts/run_seed_eval.sh --mode smoke   # 1 题 × 6 变体（约 3~5 分钟验闭环）
bash scripts/run_seed_eval.sh --mode pilot   # 10 题分层 Pilot × 6 = 60 变体
bash scripts/run_seed_eval.sh --mode full    # 全量 98 题 × 6 = 588 变体（支持 --resume 续跑）

# 4. 对已完成评估目录单独重算 IF 或补跑 LLM TC Judge
python3 seed_pipeline/score_seed_runs.py --run-dir dsh-runs/<batch_id> --with-tc-judge
```

---

## 3. 文档导航

1. **[`seed_library_and_v2_data_report.md`](./seed_library_and_v2_data_report.md)** —— **现行核心方法论与 Mentor 汇报主文档**（6 阶段 DAG、44 条种子库、`S0–S6` 梯度、98 题 588 条定稿实测分布与典型案例）。
2. **[`../archive/README.md`](../archive/README.md)** —— 历史归档清单（如需回查 Phase 1/2 文档或旧版 v5.10 静态模板实现）。
