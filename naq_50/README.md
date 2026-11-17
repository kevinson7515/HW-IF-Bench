# NAQ_50：新增 50 条真实搜索型 Task Query 构建区

本目录用于收集并标准组织 `HW-IF-Bench` V2 拟新增的 **50 条日常/真实搜索型 Task Query**（编号顺延为 `id: 51 ~ 100`），以便直接对接现有跑基线与生成器流程。

## 目录结构

```text
naq_50/
├── README.md                  # 本说明文档
├── user_query_naq50.jsonl     # 主题目清单（对接 baseline 与 benchmark-group-generator）
├── tc_ground_truth_50.jsonl   # 多源统一 TC 标准答案 / DSL 检验代码（按 id 对齐）
└── attached_files/            # 本地附件与城市沙箱数据目录（task_51 ~ task_100，按需挂载）
```

### 统一类别元数据规范（已覆盖全量已入库条目）
`user_query_naq50.jsonl` 与 `tc_ground_truth_50.jsonl` 的每一行均对齐写入了 4 个显式类别字段：
- `task_type`：顶层英文大类（如 `travel_transportation`、`education_career`、`entertainment_sports_culture`）
- `task_type_zh`：顶层中文大类（如 `出行与交通规划`、`教育求学与职场发展`、`文娱体育与文化生活`）
- `sub_category`：细分子类（如 `education`、`jobs`、`sports`、`media_entertainment`、`arts` 等）
- `source_category`：源数据集原始类别（如 `ChinaTravel/medium`、`BrowseComp-Plus/education`、`deepsearchqa/Sports`）

## 当前已写入批次 1：出行与交通规划（`id: 51 ~ 59`，共 9 条，来自 ChinaTravel）

配比：**中文 5 条 + 英文 4 条**，覆盖 9 个互不重复的目的地城市：

| `id` | `group_id` | 来源分片 | 行程与人数 | 语言 | 复杂度特征 |
| :---: | :--- | :--- | :--- | :---: | :--- |
| 51 | `G-travel-chinatravel-001` | `medium` | 武汉 → 广州（3天，2人） | zh | 12 条硬约束（预算/智能大床房/打车/餐标） |
| 52 | `G-travel-chinatravel-002` | `medium` | 重庆 → 苏州（3天，2人） | zh | 12 条硬约束（亲子/儿童乐园酒店/打车/餐标） |
| 53 | `G-travel-chinatravel-003` | `human` | 南京 → 北京（4天，2人） | zh | 8 条硬约束（高铁G往返/5个必去景点/烤鸭豆汁/住宿上限） |
| 54 | `G-travel-chinatravel-004` | `human` | 南京 → 重庆（4天，2人） | zh | 6 条硬约束（高铁G往返/4大景点/本地饮食体验） |
| 55 | `G-travel-chinatravel-005` | `preference4_base50` | 广州 → 杭州（3天，2人） | zh | 6 条硬约束 + 双重软偏好（省住宿费且多逛景点） |
| 56 | `G-travel-chinatravel-006` | `TPC2026_phase2` | Shanghai → Shenzhen（4天，3人） | en | 17 条约束（含 OR 分支 / 步行距离预算 / 时间窗） |
| 57 | `G-travel-chinatravel-007` | `TPC2026_phase2` | Nanjing → Wuhan（3天，4人） | en | 17 条约束（含 OR 分支 / 跨类先后序 / 返程时间底线） |
| 58 | `G-travel-chinatravel-008` | `TPC2026_phase2` | Shenzhen → Shanghai（3天，4人） | en | 17 条约束（含精确时刻 / 每日预算 / 禁乘返程方式） |
| 59 | `G-travel-chinatravel-009` | `TPC2026_phase2` | Chongqing → Chengdu（5天，5人） | en | 17 条约束（含 5 天长程 / 跨类先后序 / 12 次地铁限制） |

> ✅ 已基于 `LAMDA-NeSy/ChinaTravel-Sandbox`（`2026.08.2`）完成按城市/航线精准切片挂载：
> - 中文 5 题（`task_51 ~ task_55`）挂载自中文沙箱 `ChinaTravel_sandbox_zh.zip`，英文 4 题（`task_56 ~ task_59`）挂载自规范英文沙箱 `ChinaTravel_sandbox_en.zip`；
> - 每个 `attached_files/task_XX/` 目录仅包含该题目的目的城市表（`accommodations.csv`、`attractions.csv`、`restaurants.csv`、`poi.json`、`subways.json`）与对应往返交通（`trains_outbound.json`、`trains_return.json`、以及有航线时的 `flights.jsonl`），单题总体积约 310~460 KB，并已回填至 `user_query_naq50.jsonl`。


---

## 当前已写入批次 2：教育求学与职场发展（`id: 60 ~ 67`，共 8 条，来自 BrowseComp-Plus）

采用 **“本地混淆快照池 + 开放联网自由选择（A+B 混合）”** 模式：每题保留全量去重后的正例与证据网页（3–7 篇），混入 25 篇硬负例网页后彻底打乱重命名为 `attached_files/task_XX/corpus/doc_01.md ~ doc_NN.md`（去除正负标签），同时开放 `web_search` / `web_fetch` 让 Agent 自由选择检索路径。

| `id` | `group_id` | 原 `qid` | 子类 | 考察点 | 标准答案 | 语料包规模 |
| :---: | :--- | :---: | :---: | :--- | :--- | :---: |
| 60 | `G-edu-browsecomp-001` | `769` | education | 大学活动/毕业典礼/学院新闻多跳寻证 | `Queen Arwa University` | 31 篇 (6正+25负, 754.8 KB) |
| 61 | `G-edu-browsecomp-002` | `1097` | education | 高校学生分会/奖学金/讲师论文合著者 | `Shoummo Ahsan Khandoker` | 31 篇 (6正+25负, 486.8 KB) |
| 62 | `G-edu-browsecomp-003` | `591` | education | 建校时间/科学家创始人/必修外语/海外校区 | `German University in Cairo` | 31 篇 (6正+25负, 378.4 KB) |
| 63 | `G-edu-browsecomp-004` | `263` | education | 教授同日退休/空军转学界/合著论文轨迹 | `Simerly` | 32 篇 (7正+25负, 713.4 KB) |
| 64 | `G-job-browsecomp-001` | `821` | jobs | 撤回Offer诉讼/入职奖金/员工推荐率查询 | `94%` | 28 篇 (3正+25负, 307.7 KB) |
| 65 | `G-job-browsecomp-002` | `651` | jobs | 前员工集体诉讼和解/大客户占比/CEO更替 | `FormFactor` | 30 篇 (5正+25负, 1215.1 KB) |
| 66 | `G-job-browsecomp-003` | `674` | jobs | 金融从业经历/个人博客招聘帖/人物履历 | `Jeremy Eder` | 29 篇 (4正+25负, 252.1 KB) |
| 67 | `G-job-browsecomp-004` | `563` | jobs | 美国MBA/芬兰创业CEO/收购后访谈轨迹 | `Mikko Uusitalo` | 29 篇 (4正+25负, 419.7 KB) |


---

## 当前已写入批次 3：文娱体育与文化生活（`id: 68 ~ 75`，共 8 条，来自 DeepSearchQA）

全部选自 `data/deepsearchqa/DSQA-full.csv`（位于本地未入库的 `data/` 目录）中**时间已锚定/历史固定不变**的多步链式检索题（3 条 `Sports` + 3 条 `Media & Entertainment` + 2 条 `Arts`），走纯开放联网真实搜索模式（`attached_files: []`），兼具 `Set Answer`（穷举集合）与 `Single Answer`：

| `id` | `group_id` | 原行号 | 子类 (`problem_category`) | 题型 | 考察点 | 标准答案摘要 |
| :---: | :--- | :---: | :--- | :---: | :--- | :--- |
| 68 | `G-culture-deepsearchqa-001` | `row_765` | `Sports` | `Set Answer` | 2010–11 至 2014–15 连续 5 个 NHL 赛季对阵温哥华加人队进球最多球队（无格式锁死） | `Calgary Flames/Minnesota Wild` 等 5 季明细 |
| 69 | `G-culture-deepsearchqa-002` | `row_493` | `Sports` | `Set Answer` | 2015–2024 NBA 选秀八月第一周出生且单季场均>15分球员 | `Kristaps Porziņģis, Anthony Edwards, Scottie Barnes` |
| 70 | `G-culture-deepsearchqa-003` | `row_778` | `Sports` | `Set Answer` | 2023 MLB 国联 OPS>.900、Brls/PA%>10 且对右投≥500 PA | `Ronald Acuña Jr., Matt Olson` |
| 71 | `G-culture-deepsearchqa-004` | `row_182` | `Media & Entertainment` | `Set Answer` | Them There 团体第二年长成员与 91 届奥斯卡最佳女主共同参演电影交集 | `Paddington in Peru, Wonka` |
| 72 | `G-culture-deepsearchqa-005` | `row_267` | `Media & Entertainment` | `Single Answer` | 2022 情景喜剧客串→片尾曲艺人→Ivor Novello 同年→英榜 Top40 合作→原音乐剧（5 跳） | `Scraps` |
| 73 | `G-culture-deepsearchqa-006` | `row_2` | `Media & Entertainment` | `Set Answer` | 2006 Phoenix New Times 最佳乐队→2016–2021 鼓手→TikTok 爆火两首单曲 | `I Can't Handle Change (2010), Christmas Kids (2010)` |
| 74 | `G-culture-deepsearchqa-007` | `row_700` | `Arts` | `Single Answer` | 荷兰 Zeitgeist 音乐节 2022 + 厂牌 Speedy Wunderground 7 寸黑胶 − Wide Awake 2023 差集 | `Squid` |
| 75 | `G-culture-deepsearchqa-008` | `row_519` | `Arts` | `Set Answer` | 战乱受审东欧艺术家+波兰截肢战士丈夫→纪念奖项 2021 年前全部得主（无指定站点） | Katarzyna Kobro 奖 19 位得主列表 |


---

## 合作者续写对接说明（预留 `id: 76 ~ 100`，共 25 条）

为避免协作合并冲突，`id: 51 ~ 75`（共 25 条）已定稿并占用了 `attached_files/task_51 ~ task_67`。另外 25 条请按以下约定顺延追加：

1. **ID 与附件目录分配**：
   - `id` 请从整型 **`76` 编至 `100`**；
   - 如任务需挂载本地附件/语料包，统一放入 `naq_50/attached_files/task_76/` ~ `task_100/`，并在 `user_query_naq50.jsonl` 写相对路径 `"attached_files/task_XX/..."`；纯联网题写 `[]`。
2. **建议补齐的剩余 3 个应用场景（共 25 条）**：
   - **消费购物与产品对比**（`shopping_consumer`，建议 9 条）
   - **医疗健康与日常养生**（`health_wellness`，建议 8 条）
   - **社会民生与本地生活服务**（`social_news_local_life`，建议 8 条）
3. **文件与字段对齐**：
   - 同 `id` 分别向 `user_query_naq50.jsonl` 和 `tc_ground_truth_50.jsonl` 末尾各追加 1 行 JSON；
   - 请务必填全 4 个统一类别字段：`task_type`、`task_type_zh`、`sub_category`、`source_category`，并在 `tc_ground_truth_50.jsonl` 写明 `eval_type` 与 `gold_answer`（或校验程序）。
