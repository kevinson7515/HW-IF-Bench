# DSH 开放网页评测 Pipeline

## 目标

用同一道原题比较不同检索约束下的**任务正确性**和**指令遵循**。Pipeline 面向购物、医疗健康和社会民生三类开放网页任务。各条件使用相同的题面、模型、网页工具和会话预算，逐次记录工具轨迹，便于定位约束是否执行以及在哪一步失效。

## 流程

1. **读取任务清单。** 从 [user_query_openweb_246.jsonl](user_query_openweb_246.jsonl) 加载题面和来源元数据，校验题目 ID、类别和题面哈希。
2. **生成调度。** 每题生成 S0、S1、S2 三个独立会话，用固定种子排列提交顺序。S0 是基线。S1 要求先抓取至少两个不同网页，再写入证据文件。S2 还要求抓取前能在原题或此前完成的搜索结果中找到该 URL。
3. **运行 DSH。** 每次调用在独立工作目录启动，原题通过标准输入传入，附加约束通过系统提示加载。运行器保存事件、最终回答和尝试索引。
4. **评分。** 根据事件顺序与工作目录内的证据文件检查指令遵循。启用答案评分时，评分器另行读取固定版本的上游参考答案，通过独立的模型调用判断任务正确性。逐次评分和按条件、类别汇总写回运行目录。

## 调用接口

在本目录执行。每个 `--output` 需要一个尚未创建的目录。

```bash
# 生成调度，无需 DSH 或网关
python3 run.py --output ./runs/plan --plan

# 配置网关后运行，参数值可按部署调整
python3 run.py --output ./runs/openweb --profile headless \
  --workers 15 --timeout 390 --seed 246118

# 根据工具轨迹和证据文件评分
python3 assess.py ./runs/openweb

# 如需同时评估答案正确性，设置评分网关后执行
python3 assess.py ./runs/openweb --reference /path/to/DSQA-full.csv --judge
```

| 入口 | 参数与产物 |
| --- | --- |
| `run.py` | `--profile` 选 DSH profile，`--dsh` 选可执行文件，`--workers` 控制并发，`--timeout` 以秒计，`--seed` 固定调度。生成 `schedule.json` 和 `policies.json`。实际运行还生成 `attempt_index.jsonl`、`run_summary.json` 及各会话工作目录。 |
| `assess.py` | 接收已完成的运行目录。默认执行轨迹评分，`--judge` 打开答案评分并要求 `--reference`，`--workers` 控制评分并发。生成或更新 `assessment.jsonl` 和 `assessment_summary.json`。只传 `--reference` 可校验参考快照及题面。 |

运行环境为 Linux、Python 3.9+、GNU `timeout` 和 DSH。DSH profile 需加载 headless 工具并能解析 `@deepseek-ai/dsh-web-search-serper`。参考 CSV 取自 `common.py` 指定的 DeepSearchQA 版本。 [固定版本 CSV](https://huggingface.co/datasets/google/deepsearchqa/resolve/b2623f8653065c2672de6d941fc5434cd652376c/DSQA-full.csv)

| 配置 | 环境变量 |
| --- | --- |
| DSH | `DSH_HOME` 可指向已配置 profile 的目录，`DSH_BIN` 可指定可执行文件 |
| 答题模型 | `COMPANY_DEEPSEEK_BASE_URL`（OpenAI 兼容基址，通常以 `/v1` 结尾）、`COMPANY_DEEPSEEK_API_KEY` |
| 网页搜索 | `SERPER_BASE_URL`、`SERPER_API_KEY`、`SERPER_AUTH_MODE`（默认 `bearer`） |
| 答案评分 | `OPENWEB_JUDGE_URL`（完整的 `/v1/chat/completions` 地址）、`OPENWEB_JUDGE_API_KEY`，启用 `--judge` 时使用 |

## 维护方式

| 变更 | 修改位置和检查 |
| --- | --- |
| 增删题目或更新来源 | 更新题目清单及 [common.py](common.py) 中的版本、哈希和数量校验。保留已有题目的来源 ID，更新行号和题面哈希后用 `--reference` 核对原文，再用 `--plan` 检查每题的条件覆盖。 |
| 修改条件或新增约束 | 同步更新 [policies.py](policies.py) 的提示文本和 [assess.py](assess.py) 的评分规则。条件集合有变化时同步调整 `common.py`，用通过、违规和缺少最终回答的轨迹检查判定。 |
| 更换模型、搜索服务或 DSH 版本 | 更新 [patches](patches/) 中的模型和网页配置。模型 ID 变化时同步核对运行元数据与评分模型配置。DSH 事件格式有变化时更新 [dsh_events.py](dsh_events.py)，用典型轨迹检查搜索、抓取、写入和最终回答的解析。 |
| 归档一次运行 | 使用独立目录保存调度、条件文本、尝试索引和评分产物。模型与搜索凭证通过环境变量提供，参考答案和原始会话轨迹保存在运行环境。 |

题目源自 Google DeepMind 的 DeepSearchQA。仓库记录了筛选后的原题与本地分类、来源元数据。 [上游数据卡](https://huggingface.co/datasets/google/deepsearchqa) · [Apache-2.0 许可](LICENSE-DeepSearchQA)
