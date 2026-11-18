# 类型 2、4、6 的开放网页检索实验

共 23 道 DeepSearchQA 原题，消费购物 7 道，医疗健康 8 道，社会民生 8 道。每道题在三种条件下各启动一次独立的 DSH 会话，共 69 次。题面采用上游原文，实验约束通过系统提示加载。

| 条件 | 新增约束 |
| --- | --- |
| S0 | 无 |
| S1 | 作答前用 `write` 写入 `evidence_check.json`，为至少两个已成功抓取的不同网页分别记录 `url`、`role`、`scope` |
| S2 | S1 的全部要求，加上每次 `web_fetch` 的 URL 须先出现在原题或已完成的 `web_search` 结果中 |

## 数据来源

[user_query_openweb_246.jsonl](user_query_openweb_246.jsonl) 沿用 `naq_50` 的题面与类别字段。实验 ID 形如 `DSQA-386`，其中数字对应上游 CSV 从 0 起算的数据行。每条记录包含来源版本、原始行号、原类别及题面 UTF-8 SHA-256。附件列表为空。

题面取自 Google DeepMind 的 DeepSearchQA，仅筛选条目并添加本地分类和来源元数据。固定版本为 `b2623f8653065c2672de6d941fc5434cd652376c`，CSV SHA-256 为 `25d48dcf7efa872e5467032e8b8eedf38d301f59a252d0da95cda584baa78396`。授权见 [Apache-2.0](LICENSE-DeepSearchQA)。[上游数据卡](https://huggingface.co/datasets/google/deepsearchqa/blob/b2623f8653065c2672de6d941fc5434cd652376c/README.md)

## 运行

在 Linux 上使用 Python 3.9+、GNU `timeout` 和已安装的 DSH。从本目录执行以下命令即可离线生成调度和核对原文。

```bash
python3 run.py --output /tmp/openweb-246-plan --plan
curl -fsSL https://huggingface.co/datasets/google/deepsearchqa/resolve/b2623f8653065c2672de6d941fc5434cd652376c/DSQA-full.csv -o /tmp/DSQA-full.csv
python3 assess.py --reference /tmp/DSQA-full.csv
```

正式运行使用 Node.js 24 和 DSH `0.2.2-rc.1`。选择一个加载 `@deepseek-ai/dsh-base`、`@deepseek-ai/dsh-headless` 的 headless profile，确保该 profile 能解析 `@deepseek-ai/dsh-web-search-serper`。历史运行的搜索插件版本为 `0.2.2-local`，复现需要从现有 DSH 部署取得该版本或兼容实现。可通过 `DSH_HOME` 指向已配置的运行目录，并通过 `--profile` 指定 profile 名称。

| 环境变量 | 用途 |
| --- | --- |
| `DSH_BIN` | DSH 可执行文件，可用 `--dsh` 指定 |
| `COMPANY_DEEPSEEK_BASE_URL` | 华为模型网关的 OpenAI 兼容基址，通常以 `/v1` 结尾 |
| `COMPANY_DEEPSEEK_API_KEY` | 模型网关凭证 |
| `SERPER_BASE_URL` | Serper 兼容搜索网关基址 |
| `SERPER_API_KEY` | 搜索网关凭证 |
| `SERPER_AUTH_MODE` | 搜索认证方式，默认 `bearer` |

```bash
python3 run.py --output /tmp/openweb-246-run --workers 15 --timeout 390 --seed 246118
python3 assess.py /tmp/openweb-246-run
```

运行器按固定随机种子排列题目及每题三种条件的提交顺序。各条件使用同一 DeepSeek V4 Pro、相同的 DSH 工具配置和超时预算。每次会话有独立工作目录，DSH 标准输入只接收原题，标准答案仅由评分程序读取。输出根目录必须是新目录。调度、约束、尝试索引和执行汇总写入根目录，各会话的事件、最终回答和证据文件位于 `<条件>/<题目 ID>/`。

## 评分

`assess.py` 校验 69 个调度和尝试记录后，对照 DSH 事件和实际证据文件检查约束遵循。检查包括证据条目格式、不同 URL 数量、抓取成功与写入的先后关系，以及 S2 的搜索结果与抓取请求时序。证据的 `role` 和 `scope` 检查非空，语义需另行复核。缺少正常最终回答时，S1 和 S2 的约束遵循记为不可判定。

如需同时评估任务正确性，设置 `OPENWEB_JUDGE_URL`（完整的 `/v1/chat/completions` 地址）和 `OPENWEB_JUDGE_API_KEY`，再运行以下命令。评分会把原题、上游参考答案、答案类型和最终回答发送给独立的 DeepSeek V4 Pro 调用。

```bash
python3 assess.py /tmp/openweb-246-run --reference /tmp/DSQA-full.csv --judge
```

每次评分生成逐次 `assessment.jsonl` 和按条件、类别汇总的 `assessment_summary.json`。仅运行轨迹评分时，任务正确性标记为不可判定。启用任务正确性评分后，联合成功要求正常完成、答案正确，且附加约束通过或不适用。汇总分母包含全部尝试。网页内容、搜索排序和网关响应会随运行时间变化。
