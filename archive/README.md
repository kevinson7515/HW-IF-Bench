# HW-IF-Bench 历史资产归档目录 (`archive/`)

本目录用于完整留存 **V1 / Phase 1–2 历史代码、旧版拆分数据集与早期过程文档**，不参与当前 V2 主线构建与评测；现行唯一主线请见根目录的 [`benchmark/`](../benchmark/) 与 [`seed_pipeline/`](../seed_pipeline/)。

| 归档子目录 | 原目录位置 | 留存内容说明 |
| :--- | :--- | :--- |
| `legacy_generator_v5_10/` | `benchmark-group-generator/` | V1 静态模板生成器（46 种策略、`generator.py`、`policies.py`、`workflow_policies.py`） |
| `legacy_scoring_v1/` | `scoring/` | V1 早期评分器（仅支持 7 种基础程序算子；现行评分器已统一整合进 `seed_pipeline/score_seed_runs.py`） |
| `legacy_datasets/` | `baseline_fingerprint/`、`baseline_task_50/`、`naq_50/` | 合并前拆分为三处的 V1 老 50 题、Phase 1 原始运行日志与 V2 新 48 题拆分目录（现已全部统一整合至 `benchmark/`） |
| `legacy_docs/` | `docs/01~04_*.md` | V1 / Phase 1–2 阶段接手与设计历史文档 |

