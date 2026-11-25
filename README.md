# HW-IF-Bench

## 📖 项目简介

本项目提供一个可复现的 Agent 指令遵循（IF）与任务完成度（TC）评测环境，主要解决以下问题：

- **统一 Harness**：通过标准化的 Agent Harness（`deepseek-harness`）驱动模型完成多轮工具调用、任务规划与结果产出，并支持系统提示词约束注入、Tier D 对抗追问、断点续跑与工作区自动恢复。
- **可复现基线与种子库构建**：内置以 `deepseek-v4-pro` 驱动的 98 题统一基线指纹（`benchmark/`），并基于工作流种子库流水线（`seed_pipeline/`）自动生成反默认约束变体与确定性评分规则（现行 V2 冻结集共 588 条）。
- **配置隔离**：敏感凭证与本地覆盖项分别通过 `.secrets/` 与 `scripts/env.local.sh` 管理，避免硬编码。

> ⚠️ 本项目产生的基线与评测数据仅用于内部评测与回归对比，不代表任何官方发布结论。

---

## 📂 目录结构

```
.
├── .secrets/                # 敏感凭证配置（API Key 等，不纳入版本控制）
├── benchmark/               # 统一主数据目录：98 题母题、附件、基线指纹与冻结 V2 评测集
├── seed_pipeline/           # 工作流种子库约束生产、人工审查导出与确定性自动打分引擎
├── deepseek-harness/        # Agent Harness 实现（被测 Agent 的执行框架）
├── dsh-config/              # Harness 模型运行配置（deepseek / v4.1-flash / glm / pangu）
├── scripts/                 # 一键启动脚本（生成、评估、本地基线；env.local.sh 已忽略）
├── docs/                    # 项目总览与 V2 种子库方法论及数据报告
└── archive/                 # 历史归档（旧版 v5.10 生成器、旧版 scoring、旧拆分数据与早期文档）
```

### 各目录 / 文件说明

| 路径 | 类型 | 说明 |
| --- | --- | --- |
| `.secrets/` | 配置 | 存放 API Key 等敏感信息。**已加入 `.gitignore`，严禁提交到仓库。** |
| `benchmark/` | 数据 | 合并 V1（老 50 题）与 V2（新 48 题）共 98 题的母题、统一附件（`attached_files/`）、`deepseek-v4-pro` 基线指纹（`baseline_v4pro_98.json`）及冻结 588 条评测集（`releases/hw_if_bench_v2_588/`）。 |
| `seed_pipeline/` | 代码 | 基于 6 阶段生命周期 DAG 与 44 条声明式种子的约束生产、反默认回放、全局配额调度与运行后自动打分引擎。 |
| `deepseek-harness/` | 代码 | Agent Harness 的实现，负责驱动模型、执行工具调用、收集轨迹与工作区快照恢复。 |
| `dsh-config/` | 配置 | Harness 模型配置补丁（含 `deepseek.patch.yml`、`deepseek-v4.1-flash-1017.patch.yml`、`glm.patch.yml`、`pangu*.patch.yml`）。 |
| `scripts/` | 脚本 | 一键启动脚本（`run_seed_generation.sh`、`run_seed_eval.sh` 等）；本地密钥覆盖文件 `scripts/env.local.sh` 已被忽略。 |
| `docs/` | 文档 | 现行总览（`docs/README.md`）与 V2 种子库及数据报告（`docs/seed_library_and_v2_data_report.md`）。 |
| `archive/` | 归档 | 留存历史 v5.10 生成器、旧版评分器、早期拆分数据与 Phase 1/2 历史文档。 |

---

## 🚀 快速开始

### 1. 环境要求

- Python >= 3.11（含 `pyyaml`），运行 Harness 需 Node.js >= 22.19 与 `pnpm`（详见 `deepseek-harness/`）
- 可访问模型网关与工具服务（Serper / E2B）的网络环境
- 已获取有效的 API Key

### 2. 配置凭证

在项目根目录的 `.secrets/` 下放置密钥文件，或复制 `scripts/env.example.sh` 为 `scripts/env.local.sh`（**两者均已加入 `.gitignore`，切勿提交**）：

```bash
cp scripts/env.example.sh scripts/env.local.sh
# 按实际网关与密钥填写 scripts/env.local.sh
```

### 3. 约束生产（`seed_pipeline/`）

```bash
# 运行单元与全量 98 题集成测试
python3 -m unittest seed_pipeline/tests/test_seed_pipeline.py -v

# 基于 benchmark/baseline_v4pro_98.json 生成 98 题 588 条约束集（开启 LLM 语义增强）
bash scripts/run_seed_generation.sh --with-llm --llm-workers 4

# 支持对任意外部新 Query JSONL 生成约束数据集
bash scripts/run_seed_generation.sh --input-jsonl /path/to/queries.jsonl --with-llm
```

### 4. 运行评测与自动打分

```bash
# 本地一键评估（默认模型 deepseek-v4.1-flash-1017，传 --model v4-pro 可切换）
bash scripts/run_seed_eval.sh --mode smoke   # 1 题 6 变体快速验证
bash scripts/run_seed_eval.sh --mode pilot   # 10 题分层 Pilot（60 变体）
bash scripts/run_seed_eval.sh --mode full    # 全量 98 题 588 变体（支持 --resume 续跑）

# 评估结束后会自动输出确定性 IF 报表；如需补跑 LLM TC 裁判：
python3 seed_pipeline/score_seed_runs.py --run-dir dsh-runs/<batch_id> --with-tc-judge
```

如需在 Slurm 集群运行，仍可进入 `deepseek-harness/` 使用 `sbatch run.sh` / `run_deepseek.sh` / `run_glm.sh` / `run_pangu92b.sh`。运行轨迹与评分报表默认输出至 `dsh-runs/` 目录。

---

## 🧪 基线指纹与约束体系

`benchmark/baseline_v4pro_98.json` 保存了 98 道母题在 `deepseek-v4-pro` 下的无约束基线指纹与轨迹证据，主要用途：

- 通过确定性基线回放过滤送分候选，结合 `seed_pipeline/workflow_seeds.yaml` 构建 100% 反默认的流程、思考与产物约束变体（`S1–S6`，覆盖 Tier A/B/C/D）；
- 评测期直接复用同一套确定性校验器（`seed_pipeline/verifiers.py`）计算 IF 通过率及各维度衰减曲线。

详细方法论与 588 条定稿数据统计见 [`docs/seed_library_and_v2_data_report.md`](./docs/seed_library_and_v2_data_report.md)。

---

## 📬 联系方式

如有问题或建议，欢迎通过 Issue 反馈。
