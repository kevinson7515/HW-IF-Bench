# DSH 开放网页评测 Pipeline

本流程评测华为 DeepSeek V4 Pro 在不同网页检索约束下的表现。输入是 23 道 DeepSearchQA 原题，覆盖消费购物（类型 2，7 道）、医疗健康（类型 4，8 道）和社会民生（类型 6，8 道）。每道题在三种条件下各启动一次独立的 DSH 会话，共 69 次。三组共用模型、工具和超时预算，题面保持原文，实验约束通过系统提示加载。

| 条件 | 系统提示增加的要求 |
| --- | --- |
| S0 | 基线，无附加要求 |
| S1 | 先成功抓取至少两个不同网页，再用 `write` 将各网页的 `url`、`role`、`scope` 写入 `evidence_check.json`，然后给出最终回答 |
| S2 | 执行 S1。每次调用 `web_fetch` 前，URL 还须出现在原题或已完成的 `web_search` 结果中 |

## 1. 核对输入并生成调度

从仓库根目录进入实验目录。先用 `--plan` 验证输入清单并生成 69 条调度。此步无需安装 DSH 或配置网关。再下载固定版本的上游 CSV，校验整文件哈希和 23 条题面。该 CSV 含参考答案，保存在运行目录之外。

```bash
cd naq_50/openweb_246
experiment_dir="$(mktemp -d "${TMPDIR:-/tmp}/hwif-openweb.XXXXXXXX")"
python3 run.py --output "$experiment_dir/plan" --plan
curl -fsSL https://huggingface.co/datasets/google/deepsearchqa/resolve/b2623f8653065c2672de6d941fc5434cd652376c/DSQA-full.csv -o "$experiment_dir/DSQA-full.csv"
python3 assess.py --reference "$experiment_dir/DSQA-full.csv"
```

预期输出为 `Planned 69 sessions` 和 `Verified 23 original questions against the pinned CSV`。调度按种子分别打乱题目顺序和每题内部三种条件的提交顺序。并发执行时，完成顺序随响应时间变化。

## 2. 配置 DSH 与网关

运行环境为 Linux、Python 3.9+、GNU `timeout`。历史实验使用 Node.js 24、DSH `0.2.2-rc.1` 和 Serper 搜索插件 `0.2.2-local`。准备一个加载 `@deepseek-ai/dsh-base`、`@deepseek-ai/dsh-headless` 的 profile，并让该 profile 能解析 `@deepseek-ai/dsh-web-search-serper`。搜索插件由 DSH 部署提供，可使用历史版本或兼容实现。模型、网页工具和附加约束分别由 [patches](patches/) 中的配置加载。

在当前 shell 中通过环境变量提供配置。

| 环境变量 | 用途 |
| --- | --- |
| `DSH_HOME` | 已配置 profile 的 DSH 运行目录 |
| `DSH_BIN` | DSH 可执行文件。默认从 `PATH` 查找 `dsh`，也可用 `--dsh` 指定 |
| `COMPANY_DEEPSEEK_BASE_URL` | 华为模型网关的 OpenAI 兼容基址，通常以 `/v1` 结尾 |
| `COMPANY_DEEPSEEK_API_KEY` | 模型网关凭证 |
| `SERPER_BASE_URL` | Serper 兼容搜索网关基址 |
| `SERPER_API_KEY` | 搜索网关凭证 |
| `SERPER_AUTH_MODE` | 搜索认证方式，默认 `bearer` |

## 3. 执行 69 次会话

```bash
python3 run.py --output "$experiment_dir/run" \
  --profile headless --workers 15 --timeout 390 --seed 246118
```

`--output` 指向尚未创建的目录。`--workers` 控制最大并发数，`--timeout` 指定每次会话的秒数。若 profile 名称不同，修改 `--profile`。每次会话在各自工作目录中启动，DSH 标准输入只接收原题。执行结束后，`run_summary.json` 应显示 69 次尝试。超时和无最终回答均保留在尝试索引中。

## 4. 评估约束遵循

```bash
python3 assess.py "$experiment_dir/run"
```

评分器先核对调度、尝试索引与题面哈希，再按 DSH 工具请求和结果的事件顺序检查约束。正常最终回答要求会话退出码为 0，有最终回答事件，且回答文本非空。

- **S0** 的约束评分为 `not_applicable`。
- **S1** 检查实际保存的文件是否与最终回答前成功执行的 `write` 内容一致。文件需包含至少两个不同 URL，每条恰有三个非空字符串字段。各 URL 的抓取必须在写入请求前完成。抓取以 HTTP 2xx、返回正文至少 350 字符且无常见拦截页特征为准。`role` 和 `scope` 的语义由人工复核。
- **S2** 同时检查每个抓取请求与此前可见的 URL。URL 片段和末尾斜杠的差异允许通过，搜索请求后的结果必须先于抓取请求返回。
- **缺少正常最终回答**时，S1 和 S2 的约束评分为 `unassessable`。

## 5. 评估答案正确性（可选）

在当前 shell 中设置 `OPENWEB_JUDGE_URL`（完整的 `/v1/chat/completions` 地址）和 `OPENWEB_JUDGE_API_KEY`，然后执行以下命令。

```bash
python3 assess.py "$experiment_dir/run" \
  --reference "$experiment_dir/DSQA-full.csv" --judge
```

独立的 DeepSeek V4 Pro 评分调用读取原题、上游参考答案、答案类型及最终回答，给出 `FULL`、`PARTIAL`、`INCORRECT` 或 `UNASSESSABLE`。联合成功要求正常完成、答案为 `FULL`，且约束通过或不适用。仅运行第 4 步时，答案正确性标记为 `UNASSESSABLE`。重复评分会更新逐次评分和汇总文件。

## 6. 查阅产物

| 路径（相对于运行目录） | 内容 |
| --- | --- |
| `schedule.json`、`policies.json` | 随机种子、运行参数、提交顺序及三种条件的提示文本 |
| `attempt_index.jsonl`、`run_summary.json` | 逐次执行状态及按条件汇总的尝试结果 |
| `<条件>/<题目 ID>/events.jsonl` | DSH 工具请求、结果及最终回答事件 |
| `<条件>/<题目 ID>/final.txt`、`diagnostics.log` | 最终回答及进程诊断 |
| `<条件>/<题目 ID>/workspace/evidence_check.json` | 会话写入的证据文件（存在时） |
| `assessment.jsonl` | 逐次约束评分、答案评分、联合结果和事件文件哈希 |
| `assessment_summary.json` | 按条件和任务类别汇总，分母保留全部尝试 |

若评分提示缺少尝试，先确认运行已结束，再核对调度与索引是否各有 69 条。若应答为空或运行失败，用该次尝试的 `diagnostics.log` 和 `events.jsonl` 定位。网页内容、搜索排序及网关响应随运行时间变化。

## 数据来源

[user_query_openweb_246.jsonl](user_query_openweb_246.jsonl) 沿用 `naq_50` 的题面和类别字段。实验 ID 形如 `DSQA-386`，其中数字对应上游 CSV 从 0 起算的数据行。每条记录含来源版本、原始行号、原类别及题面 UTF-8 SHA-256，附件列表为空。

题面取自 Google DeepMind 的 DeepSearchQA。发布时筛选了条目并补充本地分类和来源元数据。固定版本为 `b2623f8653065c2672de6d941fc5434cd652376c`，CSV SHA-256 为 `25d48dcf7efa872e5467032e8b8eedf38d301f59a252d0da95cda584baa78396`。 [上游数据卡](https://huggingface.co/datasets/google/deepsearchqa/blob/b2623f8653065c2672de6d941fc5434cd652376c/README.md) · [Apache-2.0 许可](LICENSE-DeepSearchQA)
