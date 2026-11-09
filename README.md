# HW-IF-Bench

## 📖 项目简介

本项目提供一个可复现的 Agent 评测环境，主要解决以下问题：

- **统一 Harness**：通过标准化的 Agent Harness 驱动模型完成多轮工具调用、任务规划与结果产出。
- **可复现基线**：内置以 `deepseek-v4-pro` 作为驱动模型生成的基线指纹（Baseline Fingerprint），包含完整 Benchmark 测试数据，便于对模型升级 / 配置变更后的能力变化进行回归比对。
- **配置隔离**：敏感凭证与运行配置分别通过 `.secrets` 与 `dsh-config` 管理，避免硬编码。

> ⚠️ 本项目产生的基线数据仅用于内部评测与回归对比，不代表任何官方发布结论。

---

## 📂 目录结构

```
.
├── .secrets                 # 敏感凭证配置（API Key 等，不纳入版本控制）
├── dsh-config               # Harness 运行配置（模型、超参、评测项等）
├── deepseek-harness/        # Agent Harness 实现（被测 Agent 的执行框架）
└── baseline_fingerprint/    # 基线指纹：deepseek-v4-pro 驱动的 Benchmark 测试数据
```

### 各目录 / 文件说明

| 路径 | 类型 | 说明 |
| --- | --- | --- |
| `.secrets` | 配置文件 | 存放 API Key、Endpoint 等敏感信息。**必须加入 `.gitignore`，严禁提交到仓库。** |
| `dsh-config` | 配置文件 | Harness 的运行配置，包括驱动模型、温度、最大轮次、启用的 Benchmark 用例集等。 |
| `deepseek-harness/` | 代码 | Agent Harness 的实现，负责驱动模型、执行工具调用、收集轨迹与评分。 |
| `baseline_fingerprint/` | 数据 | 以 `deepseek-v4-pro` 作为驱动模型产出的基线指纹，内含 Benchmark 测试数据与期望输出。 |

---

## 🚀 快速开始

### 1. 环境要求

- Python >= 3.11（如 Harness 为其他语言实现，请按实际依赖调整）
- 可访问 DeepSeek API 的网络环境
- 已获取有效的 API Key

### 2. 克隆项目

- 按照 deepseek-harness 配置即可

### 3. 配置凭证

在项目根目录创建 `.secrets` 文件（**不要提交**）：

```ini
# .secrets
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

> 注意：`.secrets` 已在 `.gitignore` 中忽略。首次使用请确认不要将其推送到远程仓库。

### 5. 运行评测

```bash
# 进入 Harness 目录
cd deepseek-harness

# 安装依赖（以 Python 为例）
pip install -r requirements.txt

# 启动评测
sbatch run.sh            # 生成 baseline_fingureprint
sbatch run_deepseek.sh   # 评测 deepseek-v4-pro
sbatch run_glm.sh        # 评测 glm-5.3
sbatch run_pangu92b.sh   # 评测 pangu92b
```

运行结束后，轨迹与评分结果将输出至与 deepseek-harness 同级的目录 `dsh-runs` 中。

---

## 🧪 基线指纹（Baseline Fingerprint）

`baseline_fingerprint/` 保存了以 `deepseek-v4-pro` 为驱动模型跑出的基准结果，主要用途：

- 根据基线指纹构建 Benchmark 中的指令变体(instruction)和评分标准(rubrics)

---
## 📬 联系方式

如有问题或建议，欢迎通过 Issue 反馈。
