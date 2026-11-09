# 面向"成分–性能预测与成分优化"的机器学习/深度学习：数据库与模型精度基准调研

**调研范围**：2019–2025 年发表/维护的材料信息学数据库与模型精度基准（含 2026 年页面快照反映的最新状态）
**核验方式**：全部数值经 web 检索/页面抓取核验，每项附来源 URL；未能从一手来源确认的数值标注 **待核实**
**核验时间**：约 2026 年（多个来源页面为 2026 年快照，如 Materials Project 数据库版本 v2026.09.28、PoLyInfo 数据截至 2026-09-30；因此"当前值"按页面快照日期注明）

---

## 1. 数据库调研

### 1.1 DFT 计算数据库（总表）

| 数据库 | 条目规模（核验日期） | 数据类型 | 维护机构 | URL | 在成分/结构优化中的典型用途 |
|---|---|---|---|---|---|
| **Materials Project (MP)** | 历史版本 v2022.10.28 = **154,713**（≈155k）；当前（v2026.09.28 快照）**271,325** 材料，其中 GNoME 来源材料合计 **117k**（含一批 15,483 及后续 74,052 个 r2SCAN 计算材料）；另有分子 577,813 | DFT（PBE/PBE+U，新增 r2SCAN）+ 实验数据聚合 | 美国劳伦斯伯克利国家实验室（LBNL） | https://next-gen.materialsproject.org/ ；变更日志 https://docs.materialsproject.org/changes/database-versions ；155k 数值见 https://matbench-discovery.materialsproject.org/models/alignn | 成分筛选、凸包稳定性分析、模型训练主数据源 |
| **MP 弛豫轨迹库 MPtrj** | **1,580,395** 个构型（来自约 **146,000** 种材料） | DFT 弛豫中间构型（能量/力/应力） | LBNL | CHGNet 论文 https://arxiv.org/abs/2302.14231 ；https://matbench-discovery.materialsproject.org/models/mace-mp-0 | 通用机器学习原子间势（UIP）训练 |
| **OQMD** | 当前 **1,407,395** 材料（检索快照；2021 年中为 1,022,603） | DFT（VASP，PAW/PBE）+ 部分实验 | 美国西北大学（Wolverton 组） | https://www.oqmd.org/ （直接抓取返回 502，数值来自搜索快照）；历史值见 https://iopscience.iop.org/article/10.1088/2515-7639/ac7ba9 | 凸包构建、成分能量筛选、Roost/CrabNet 等成分模型训练 |
| **AFLOW** | **3,929,948** 个材料化合物；**817,429,184** 条计算性质 | DFT（VASP，多种泛函）+ 模型化/热力学数据 | 美国杜克大学（Curtarolo 组，AFLOW.org 联盟） | https://www.aflowlib.org/ （数值来自站内搜索快照） | 高通量筛选、形成能/凸包、AEL/APL 弹性与声子 |
| **JARVIS-DFT** | **77,096** 个 DFT 材料（OptB88vdW）；JARVIS-QETB **800,000+** PBEsol 材料；JARVIS-FF **2,538** 个材料 | DFT（OptB88vdW/TBmBJ/SENECA 等）+ 半经验 + 力场 | 美国国家标准与技术研究院（NIST） | https://jarvis.nist.gov/ | 二维材料筛选、带隙/形成能/弹性等基准任务 |
| **NOMAD** | 已上传条目 **19,425,275**；可表示材料 **4,346,100**；数据量 **129.3 TB** | DFT/电子结构原始输入输出（归档 + FAIR 元数据） | 德国马普学会/FHI（FAIRmat 与 NOMAD CoE） | https://nomad-lab.eu/nomad-lab/index.html | 数据复用、"查找-复用"FAIR 数据底座、AI 训练数据提取 |
| **GNoME** | **220 万（2.2M）** 个新晶体结构，其中 **38.1 万（381k）** 位于凸包上（较此前知识新增）；与 ICSD 中独立实验结构匹配 **736** 个 | DFT（PBE）标签的机器学习势生成结构 + DFT 验证 | Google DeepMind | 论文 https://www.nature.com/articles/s41586-023-06735-9 ；博客 https://deepmind.google/discover/blog/millions-of-new-materials-discovered-with-deep-learning/ | 超大规模候选结构库，成分/结构优化正样本扩充 |
| **Alexandria** | **5.8M** 结构、其中 **175k** 位于凸包（2025 论文口径）；OMat24 论文（2024-10）口径约 **4.5M**；sAlex25 离平衡子库 **14M** 结构 | DFT（PBE/PBEsol）平衡+离平衡结构 | 德国鲁尔大学波鸿分校（ICAMS） | https://alexandria.icams.rub.de/ ；论文 https://arxiv.org/abs/2512.09169 （2 页摘要口径）；OMat24 对照见 https://arxiv.org/abs/2410.12771 | UIP 训练、结构弛豫基准（PBEsol，修正 MPtrj 的构型采样偏置） |
| **OMat24** | **1.18 亿（118M）** DFT 结构（训练集 100,824,585） | DFT（PBE+U，含扰动/构型采样结构） | Meta FAIR | https://arxiv.org/abs/2410.12771 | 大规模 UIP 训练（eqV2） |
| **MatterSim 训练集** | 约 **1700 万（17M）** 个第一性原理标注结构 | DFT（0–5000 K、0–1000 GPa 温压采样） | 微软研究院（MSR AI4Science） | https://arxiv.org/abs/2405.04967 | 跨温压 UIP/性质预测 |

**说明**
- MP 的"271,325"与"117k GNoME"均取自 next-gen 站点与官方变更日志快照；2024/2025 年的中间精确值未单独公布，**待核实**（可按变更日志逐版本累计）。
- OQMD 主站抓取返回 502（多次），1,407,395 来自其搜索快照；建议引用时以主站复核。
- AFLOW 的 817M"计算性质"为逐条计算条目数，非独立材料数。

### 1.2 基准数据集（用于精度评测）

| 基准 | 规模 | 用途 | 来源 |
|---|---|---|---|
| **Matbench v0.1** | 13 个任务，样本量 **312–132,752** | 成分/结构→性能回归与分类（5 折交叉验证，五重统计） | https://matbench.materialsproject.org/ ；论文 https://www.nature.com/articles/s41524-020-00406-3 |
| **Matbench Discovery** | 测试集 WBM **256,445**（232,291 + 24,154） | 前瞻式热力学稳定性预测（F1/DAF/MAE/CPS） | https://matbench-discovery.materialsproject.org/ ；论文 https://arxiv.org/abs/2308.14920 |
| **OC20** | **1.3M** 分子弛豫、>**260M** DFT 单点计算 | 催化剂吸附能/力预测（IS2RE/IS2RS/S2EF） | https://opencatalystproject.org/ ；论文 https://arxiv.org/abs/2010.09990 |
| **OC22** | **62,331** DFT 弛豫 | 贱金属催化剂吸附能（含 Cu/Ag/Au 表面 + 洁净表面基线） | https://arxiv.org/abs/2206.08917 |

**Matbench 13 任务样本量**（https://matbench.materialsproject.org/ ）：steels 312；jdft2d 636；phonons 1,265；expt_gap 4,604；dielectric 4,764；expt_is_metal 4,921；glass 5,680；log_gvrh 10,987；log_kvrh 10,987；perovskites 18,928；mp_gap 106,113；mp_is_metal 106,113；mp_e_form 132,752。

### 1.3 实验数据库

| 数据库 | 规模（核验日期） | 数据类型 | 维护机构 | URL | 用途 |
|---|---|---|---|---|---|
| **ICSD** | 当前 **347,985** 条晶体结构（2018 年 20 万；2024 年 5 月 30 万） | 实验晶体结构（X 射线/中子衍射） | 德国 FIZ Karlsruhe（与圣路易斯 NIST/STN 合作） | https://www.fiz-karlsruhe.de/de/produkte-und-dienstleistungen/inorganic-crystal-structure-database-icsd-news | 结构模板库、GNoME 等预测的实验对照 |
| **SpringerMaterials** | **290,000+** 材料、**3,000+** 种性质、500,000+ 在线文档 | 实验/DFT 混合参考数据（含 Landolt–Börnstein） | Springer Nature | https://www.springernature.com/gp/librarians/products/databases-solutions/springermaterials | 实验物性检索与对照 |
| **MatWeb** | **200,000+** 材料 | 实验物性（金属/陶瓷/聚合物/复合材料） | MatWeb（美国） | http://matweb.com/ （直接抓取 403，数值来自搜索快照） | 工程材料物性检索 |
| **PoLyInfo** | 截至 2026-09-30：均聚物 **16,064**、共聚物 **5,638**、共混物 **1,978**、复合材料 **2,153**；聚合物样品 **112,771**；数据点 **357,812**；文献 15,365 | 实验聚合物物性（约 100 种性质类型） | 日本国立材料研究所（NIMS） | https://polymer.nims.go.jp/ ；2024 年论文称数据点 >500,000（https://www.tandfonline.com/doi/full/10.1080/27660400.2024.2354649 ），与站点口径存在差异（统计口径不同，**待核实**） | 聚合物成分–物性建模 |
| **Citrine / Citrination** | 公开平台 **Open Citrination 已下线**（官方声明）；商业平台规模未公开（官网称 380 个项目、550 个 AI 模型部署等，完整口径 **待核实**） | 实验+计算聚合（GEMD 数据模型、含不确定度与溯源） | 美国 Citrine Informatics | https://citrination.com/ （下线声明）；https://citrine.io/ | 工业"实验-配方"数据管理与小数据建模（GEMD 格式） |

### 1.4 领域专用数据库

| 领域 | 数据库 | 规模（核验日期） | 数据类型 | 维护机构 | URL |
|---|---|---|---|---|---|
| 高熵合金 | **ULTERA** | **4,300** 个 HEA、**12,500+** 条物性数据、来自 **810+** 篇文献（2025-04）；自称最大 HEA 实验数据库，95%+ 实验数据 | 实验为主（力学性能等） | 美国宾州州立大学 Phases Research Lab（DOE ARPA-E ULTIMATE 计划） | https://phaseslab.com/ultera |
| 高熵合金 | Thermo-Calc TCHEA 系列（如 TCHEA9） | 商业 CALPHAD 数据库（条目数未公开，**待核实**） | 热力学/物性评估 | 瑞典 Thermo-Calc Software | https://thermocalc.com/products/databases/high-entropy-alloys/ |
| 电池 | **MP Battery Explorer** | **6,847** 个插层电极（含 Li/Mg/Ca 体系，预测电压曲线与析氧数据） | DFT 计算电极数据 | LBNL（Materials Project） | https://next-gen.materialsproject.org/batteries |
| 电池 | **文本挖掘电池材料库**（Huang 2020） | **292,313** 条数据记录、**214,617** 条唯一"化学式–性质"对 | 文献实验数据（ChemDataExtractor 自动抽取） | 美国加州大学圣地亚哥分校（Shyue Ping Ong 组） | https://pmc.ncbi.nlm.nih.gov/articles/PMC7411033/ |
| 电池 | **DRX（阳离子无序岩盐相）数据集** | DRX-CE 数据集：岩盐格架不同阳/阴离子有序构型 + DFT 弛豫（含 MD 轨迹采样 200 结构/条并入训练集）；总条目数 **待核实** | DFT（Ceder 组高通量） | 美国加州大学伯克利分校/LBL（Ceder 组） | https://ceder.berkeley.edu/publications/2025_Peichen_modeling-deltaDRX.pdf ；https://batterygroup.lbl.gov/disordered-rock-salts |
| 催化 | **OC20** | **1.3M** 弛豫、>**260M** DFT 计算（含吸附能/力） | DFT | Meta FAIR + CMU | https://opencatalystproject.org/ |
| 催化 | **OC22** | **62,331** 弛豫 | DFT | Meta FAIR + CMU | https://arxiv.org/abs/2206.08917 |

### 1.5 文本挖掘数据/工具

| 工具/语料 | 规模 | 说明 | 来源 |
|---|---|---|---|
| **MatBERT**（LBNL） | 训练语料 **200 万篇论文**、**61,253,938** 段落 | 材料领域预训练 BERT；下游 NER/关系抽取（含 12 种材料 NER 数据集，F1 最高约 0.86–0.91，**逐任务数值待核实**） | https://github.com/lbnlp/MatBERT |
| **MatSciBERT / 其他领域模型** | — | 二次预训练与领域自适应（引用见 Walker 2021） | https://www.nature.com/articles/s41524-022-00784-w |
| **ChemDataExtractor 2.0** | 自动构建本体 + 多性质并发抽取 | 化学文献表格/文本结构化抽取（电池库 292k 记录即其应用） | https://pubs.acs.org/doi/10.1021/acs.jcim.1c00607 （原文 403，转引 DOI/页） |
| **电池材料自动库**（ChemDataExtractor 应用） | **292,313** 记录 / **214,617** 唯一化学–性质对 | 抽取自 20 万+篇文献（实验电压/容量等） | https://pmc.ncbi.nlm.nih.gov/articles/PMC7411033/ |

---

## 2. 模型精度基准

### 2.1 形成能预测（DFT 数据集；单位 eV/atom，除非注明）

| 模型 | 模型类型 | 数据集 | 精度 | 来源 |
|---|---|---|---|---|
| Magpie 特征 + 随机森林（Ward 2016） | 成分描述符+树模型 | OQMD 256,620 子集 | MAE **0.067** | Roost 论文表格 https://pmc.ncbi.nlm.nih.gov/articles/PMC7722901/ （原始 Ward 2016 数值 **待核实**） |
| **ElemNet**（Jha 2018） | 纯成分 DNN | OQMD 测试集 | MAE **0.055** | 论文 https://pmc.ncbi.nlm.nih.gov/articles/PMC6279928/ ；Roost 论文复测同值 0.055 |
| **CGCNN**（Xie & Grossman 2018） | 晶体图 CNN（需结构） | MP 数据集 | MAE ≈ **0.03** | MEGNet 论文转引 https://arxiv.org/abs/1812.05055 ；对照综述称 0.03–0.04 https://www.cell.com/patterns/fulltext/S2666-3899(21)00223-3 |
| **MEGNet**（Chen 2019） | 材料图网络（需结构） | MP ~60,000 晶体 | MAE **0.032** | 论文 https://arxiv.org/abs/1812.05055 |
| **Roost**（Goodall 2020，成分模型） | 成分消息传递+注意力池化 | OQMD 256,620 子集 | 单模型 MAE **0.0297**；集成 MAE **0.0241**（RMSE 0.0871） | 论文 https://pmc.ncbi.nlm.nih.gov/articles/PMC7722901/ |
| **ALIGNN**（Choudhary 2021） | 原子+键线图网络（需结构） | Matbench matbench_mp_e_form（132,752 样本） | MAE **0.0215** | https://matbench.materialsproject.org/ |
| **CrabNet**（Wang 2021，成分模型） | 成分受限 Transformer | Matbench matbench_mp_e_form | MAE **0.0862**；OQMD 形成能 MAE ≈ **0.0861**（转引） | Matbench https://matbench.materialsproject.org/ ；OQMD 数值转引自 https://pubs.acs.org/doi/10.1021/acs.jctc.4c00187 （原文表格数值建议复核） |
| **coGN**（Parker 2023/2024） | 晶体图网络 | Matbench matbench_mp_e_form | MAE **0.0170**（截至核验时榜首） | https://matbench.materialsproject.org/ |
| **M3GNet**（Chen & Ong 2022，UIP） | 三体图网络通用势 | WBM 测试集 | MAE **0.072**；训练数据为 MP 的 187k 能量/16M 力/1.6M 应力 | https://raw.githubusercontent.com/janosh/matbench-discovery/main/models/m3gnet/m3gnet.yml ；论文 https://arxiv.org/abs/2202.02450 |
| **CHGNet**（Deng 2023，UIP） | 电荷感知图网络 | MPtrj 测试集 | 能量 MAE **30 meV/atom**；力 77 meV/Å；应力 0.348 GPa；磁矩 0.032 μB | 论文 https://arxiv.org/abs/2302.14231 ；WBM F1 0.613 https://matbench-discovery.materialsproject.org/models/chgnet-0.3.0 |
| **MACE-MP-0**（Batatia 2023/2025，UIP） | 等变消息传递（MACE） | MPtrj 训练；JCP 报告 | 能量 MAE **18 meV/atom**、力 MAE **39 meV/Å**（medium 模型） | J Chem Phys 2025 https://pubs.aip.org/aip/jcp/article/163/18/184110/3372267 ；WBM 上 F1 0.668 / MAE 0.055 eV/atom / R² 0.698 https://raw.githubusercontent.com/janosh/matbench-discovery/main/models/mace-mp-0.yml |
| **MatterSim**（Microsoft 2024，UIP） | 图 Transformer + 三体 | 自建 17M 结构（0–5000 K，0–1000 GPa） | MPF-TP 能量 MAE **36 meV/atom**；Gibbs 自由能（≤1000 K 对实验）MAE **15 meV/atom**；Matbench Discovery **F1 0.83** | 论文 https://arxiv.org/abs/2405.04967 ；F1 摘要口径 https://www.alphaxiv.org/abs/2405.04967 |
| **OMat24 eqV2**（Meta 2024，UIP） | 等变 Transformer（31M/86M/153M 参数） | OMat24（118M 结构） | 仅 OMat24 训练：验证集能量 MAE **9.6–11 meV/atom**；WBM 测试 **14.57–15.96 meV/atom**；仅 MPtrj"合规"训练：F1 **0.823**、能量 MAE 35–36 meV/atom；OMat24 预训练+微调：**F1 0.916**、能量 MAE **20 meV/atom** | 论文 https://arxiv.org/abs/2410.12771 |
| **GNoME 模型**（DeepMind 2023，图网络势） | 图网络势迭代主动学习 | 自建+DFT 验证 | 能量 **11 meV/atom**；稳定预测命中率/精度 **>80%** | 论文 https://www.nature.com/articles/s41586-023-06735-9 |

### 2.2 带隙预测（注意：PBE 系统性低估）

**重要口径警示**：PBE 泛函对带隙存在系统性低估（对 sp 键半导体典型低估 **30%–50%**，见 https://chemrxiv.org/engage/chemrxiv/public-assets/v1/doi/10.26434/chemrxiv.15003709 ；MP 官方口径亦注明"DFT 计算通常系统性低估带隙"，见 https://matsci.org/t/band-gap-calculation/1031 ）。下表数值须区分 PBE 计算值与实验值。

| 模型 | 数据集 | 精度 | 来源 |
|---|---|---|---|
| **MEGNet** | MP（PBE 带隙，~60k） | MAE **0.35 eV** | https://arxiv.org/abs/1812.05055 |
| **CGCNN v2019** | Matbench matbench_mp_gap（106,113 PBE） | MAE **0.2972 eV** | https://matbench.materialsproject.org/Leaderboards%20Per-Task/matbench_v0.1_matbench_mp_gap/ |
| **coGN**（榜首） | Matbench matbench_mp_gap | MAE **0.1559 eV** | 同上 |
| **MODNet**（榜首） | Matbench matbench_expt_gap（4,604 实验） | MAE **0.3327 eV** | https://matbench.materialsproject.org/ |
| **Roost**（成分模型） | 实验带隙（3,895 非金属）；MP→实验迁移 | 基线 0.277；Roost 直接训练 **0.243**；MP 预训练迁移 **0.219** | https://pmc.ncbi.nlm.nih.gov/articles/PMC7722901/ |
| ALIGNN（JARVIS-DFT OptB88vdW 带隙） | JARVIS-DFT | **待核实**（原论文表格数值未能从可抓取来源确认） | https://github.com/usnistgov/alignn |

### 2.3 Matbench v0.1 各任务当前最优（截至核验时）

| 任务 | 样本数 | 性质 | 最优模型 | 分数 | 备注 |
|---|---|---|---|---|---|
| matbench_steels | 312 | 屈服强度（MPa，MAE） | MODNet | **87.7627** | 成分+热处理 |
| matbench_jdft2d | 636 | 剥离能 | **待核实**（页面截断） | — | |
| matbench_phonons | 1,265 | 声子峰频率 | **待核实** | — | |
| matbench_expt_gap | 4,604 | 实验带隙（MAE, eV） | MODNet | **0.3327** | 实验数据 |
| matbench_dielectric | 4,764 | 折射率 | **待核实** | — | |
| matbench_expt_is_metal | 4,921 | 金属/非金属 | AMMExpress | **0.9209** | 见下方 ROC-AUC 口径警示 |
| matbench_glass | 5,680 | 金属玻璃形成（分类） | MODNet | **0.9603** | 同上 |
| matbench_log_gvrh | 10,987 | 体积剪切模量（log, MAE） | coNGN | **0.0670** | |
| matbench_log_kvrh | 10,987 | 体积模量（log, MAE） | coNGN | **0.0491** | |
| matbench_perovskites | 18,928 | 钙钛矿形成能（MAE, eV/晶胞） | coGN | **0.0269** | |
| matbench_mp_gap | 106,113 | PBE 带隙（MAE, eV） | coGN | **0.1559** | PBE 低估警示 |
| matbench_mp_is_metal | 106,113 | 金属/非金属 | CGCNN v2019 | **0.9520** | 分类任务（见下注） |
| matbench_mp_e_form | 132,752 | 形成能（MAE, eV/atom） | coGN | **0.0170** | |

**分类任务口径警示**：Matbench 官方声明"matbench_v0.1 分类排行榜上的 ROC-AUC 分数是在 0.5 阈值化预测上计算的，因此等于平衡准确率而非真正 ROC-AUC"（https://matbench.materialsproject.org/ ；https://github.com/materialsproject/matbench ）。上表 expt_is_metal / glass / mp_is_metal 分数应按**平衡准确率**理解。

**matbench_mp_e_form 完整榜单参考**（成分模型 vs 结构模型差距）：coGN 0.0170 → coNGN 0.0178 → ALIGNN 0.0215 → SchNet 0.0218 → DimeNet++ 0.0235 → GN-OA 0.0248 → MEGNet 0.0252 → CGCNN 0.0337 → DeeperGATGNN 0.0340 → MODNet 0.0448 → **Finder（仅成分）0.0839 → CrabNet（仅成分）0.0862 → RF-SCM/Magpie 0.1165** → AMMExpress 0.1726 → Dummy 1.0059（https://matbench.materialsproject.org/ ）。

### 2.4 Matbench Discovery（WBM 前瞻稳定性预测，256,445 个新结构）

- **2019–2025 经典模型排名**（论文 v3）：EquiformerV2+DeNS > Orb > SevenNet > MACE > CHGNet > M3GNet > ALIGNN > MEGNet > CGCNN（+CGCNN+P）> Wrenformer > BOWSR > Voronoi RF（https://arxiv.org/abs/2308.14920 ）。
- **UIP 模型 F1 范围 0.57–0.82，发现加速因子（DAF）最高约 6×**（同上）。
- 代表模型：M3GNet F1 **0.576**/MAE 0.072；CHGNet F1 **0.613**；MACE-MP-0 F1 **0.668**/MAE 0.055；ALIGNN F1 **0.567**；MatterSim F1 **0.83**；OMat24 eqV2（微调）F1 **0.916**（各来源见 2.1 表）。
- 截至 2026 年快照，排行榜头部的最新模型 MAE 已达 **0.017–0.018 eV/atom**、DAF 约 6（https://matbench-discovery.materialsproject.org/ ；属 2025/2026 新模型，超出本调研 2019–2025 主焦点，仅作趋势参照）。

### 2.5 实验性能预测（非 DFT 数据集）

| 领域/性质 | 模型/研究 | 数据集 | 精度 | 来源 |
|---|---|---|---|---|
| **HEA 硬度** | 可解释 ML+固溶强化模型（Ren 2023） | 多主元合金硬度数据 | R² **0.9716**，RMSE **39.25**（HV） | https://lanlexperts.elsevierpure.com/en/publications/prediction-and-design-of-high-hardness-high-entropy-alloy-through/ |
| HEA 硬度 | XGBoost（Zhou 2026） | 612 组多元合金硬度 | R² **0.94** | https://www.sciencedirect.com/science/article/pii/S0264127526003059 |
| HEA 硬度 | Bakr 2022 | HEA 相+硬度 | R² **0.9** | https://www.sciencedirect.com/science/article/abs/pii/S2352492822002768 |
| **HEA 屈服强度** | ML 屈服强度+断裂应变模型（He 2024，难熔 HEA 设计） | 难熔 HEA 实验数据 | 屈服强度 R² **0.942**（RMSE 0.35）；断裂应变 R² **0.892**（RMSE 0.41） | https://pure.bit.edu.cn/en/publications/machine-learning-assisted-design-of-refractory-high-entropy-alloy/ |
| HEA 力学性能（早期代表） | Wen 2019（Acta Mater） | HEA 力学实验数据 | 力学性能 R² **0.80–0.90**；设计并制备出硬度超出训练集最优 10% 的新合金 | https://www.researchgate.net/publication/331693971_Machine_learning_assisted_design_of_high_entropy_alloys_with_desired_property |
| **金属玻璃 GFA** | ML vs 人类专家对照（Liu 2023, Acta Mater） | 块体金属玻璃（BMG）与非条带数据 | 四种模型准确率均 **>91%** | https://www.sciencedirect.com/science/article/pii/S1359645422008746 |
| 金属玻璃 GFA | 集成 ML（Liu 2023, Processes） | 合金 GFA 数据 | 分类准确率 **98%** | https://www.mdpi.com/2227-9717/11/9/2806 |
| **磁热材料** | ML 指导发现 HoB₂（Castro 2020） | 磁热候选库 | 发现巨磁热效应 HoB₂（近氢液化温度 ~20 K）；其 ML 为随机森林按成分预测 Curie 温度 | https://www.nature.com/articles/s41427-020-0214-y ；方法描述见 https://arxiv.org/abs/2307.06879 |
| 磁性（Curie 温度） | 梯度提升+贝叶斯优化特征筛选（Jung & Cole 2024） | 铁磁材料数据库 | Tc 回归 R² **0.91**；分类准确率 **87%** | https://pmc.ncbi.nlm.nih.gov/articles/PMC11350867/ （R²/准确率口径见 https://europepmc.org/articles/pmc11350867 ） |
| **热电 zT** | 可解释 ML（Barua 2025, ACS AMI） | 约 **160,000** 条实验数据 | 三个测试集 RMSE **0.15–0.20**；R² **0.67–0.80** | https://pubmed.ncbi.nlm.nih.gov/39686715/ |
| **催化吸附能（OC20）** | 2022 OC 挑战赛冠军 | OC20 IS2RE test-like | 能量 MAE **0.396 eV** | https://opencatalystproject.org/challenge.html |
| OC20 | GemNet-OC | OC20 IS2RE | 平均 MAE **471 meV** | https://openreview.net/forum?id=u8tvSxm4Bs |
| OC20 | EquiformerV2 + DeNS（160M，All+MD，2024/06 提交，榜首） | OC20 排行榜 | 能量 MAE **0.2933 eV**（同页力相关分数 18.78） | https://opencatalystproject.org/leaderboard.html （JS 渲染页，数值来自该页搜索快照，**建议二次复核**） |
| OC20/OC22 挑战赛 | 2023 冠军 CausalAI | 吸附能 0.1 eV 阈值内成功率 | **46%** | https://opencatalystproject.org/challenge.html |

### 2.6 主动学习/贝叶斯优化的实验效率

| 研究 | 任务 | 初始数据 | 迭代次数 | 合成/验证结果 | 来源 |
|---|---|---|---|---|---|
| Xue 2019（Science，经 Rao 2024 转引） | Ni-Ti 形状记忆合金 | **22** 条原始数据 | **9** 轮 | 预测出 **36** 个候选成分（提升形状记忆表现） | https://pmc.ncbi.nlm.nih.gov/articles/PMC11531902/ |
| **Rao 2022（Science）** | 高熵 Invar 合金（低热膨胀） | 百万级成分空间 | 仅 **6** 轮 | 制备表征 **17** 个新合金，发现 **2** 个新型高熵 Invar 合金 | https://pubmed.ncbi.nlm.nih.gov/36201584/ ；https://www.mpi-halle.mpg.de/3800867/2022-10-14-invar （报道页） |
| Sulley 2024（Scripta Mater.） | 2,198 合金实验数据集主动学习 | 全量数据的约 **27%** | — | 达到 **95%** 预测准确率（大幅降低实验需求） | https://www.sciencedirect.com/science/article/abs/pii/S135964622400215X （原文 403，数值来自搜索快照） |
| M3GNet 筛选+DFT 验证（Chen & Ong 2022） | 3100 万假想结构稳定性 | M3GNet 势 | 一轮筛选 | 1.8M 潜在稳定；top-2000 中 **1,578**（78.9%）经 DFT 确认稳定 | https://arxiv.org/abs/2202.02450 |

### 2.7 生成式/逆向设计模型

| 模型 | 关键结果 | 来源 |
|---|---|---|
| **GNoME**（DeepMind 2023） | 新增 **220 万**晶体，**38.1 万**在凸包上；模型能量 MAE **11 meV/atom**；稳定预测精度/命中率 **>80%**；**736** 个结构与 ICSD 中独立获得的实验结构匹配 | https://www.nature.com/articles/s41586-023-06735-9 ；https://deepmind.google/discover/blog/millions-of-new-materials-discovered-with-deep-learning/ |
| **MatterGen**（Microsoft 2025, Nature） | 相比 CDVAE/DiffCSP 基线：生成"新颖且稳定"结构的概率 **>2×**，距局部能量极小 **>10×** 更近；1,024 个生成结构中 **78%** 距 MP 凸包 ≤0.1 eV/atom、**75%** 距 Alex-MP-ICSD 凸包 ≤0.1 eV/atom；**95%** 结构 RMSD < 0.076 Å；训练集 Alex-MP-20（**607,683** 稳定结构）；微调目标：磁性密度 0.20 Å⁻³、带隙 3.0 eV、体模量 400 GPa；实验验证合成 **TaCr₂O₆**，体模量与目标偏差 **<20%** | https://pmc.ncbi.nlm.nih.gov/articles/PMC11922738/ （Nature 原文 https://www.nature.com/articles/s41586-025-08628-5 ） |

---

## 3. 主要结论（面向成分–性能预测与成分优化）

1. **数据规模量级（2024–2026 快照）**：实验结构库 ICSD ≈ 35 万；DFT 平衡结构库 MP≈27 万（含 11.7 万 GNoME）、OQMD≈141 万、AFLOW≈393 万、Alexandria≈450–580 万；DFT 弛豫/离平衡轨迹库 MPtrj 158 万、OMat24 1.18 亿、MatterSim 训练集 1700 万；机器生成结构库 GNoME 220 万。成分优化可用的"稳定/近稳定正样本"规模已从 10⁵ 级跃升至 10⁶–10⁷ 级。
2. **成分输入 vs 结构输入**：在形成能上，结构 GNN（coGN 0.017、ALIGNN 0.0215 eV/atom）明显优于纯成分模型（Finder 0.0839、CrabNet 0.0862、Magpie+RF 0.1165，均在 matbench_mp_e_form）；成分模型中 Roost 集成（OQMD 0.0241）是精度/数据需求平衡最好的代表。**无结构场景（如高熵合金配方设计）仍以成分模型为主**。
3. **通用原子间势（UIP）成为成分筛选新引擎**：MACE-MP-0（18 meV/atom）、CHGNet（30 meV/atom）、MatterSim（36 meV/atom）、OMat24 eqV2（10–20 meV/atom）把"形成能/稳定性"预测误差推进到 10–40 meV/atom 区间，配合 WBM 前瞻基准（F1 0.57→0.92）验证了在"训练集外"的泛化能力。
4. **实验性能预测天花板**：HEA 硬度/屈服强度 R² 0.89–0.97；金属玻璃 GFA 分类 91–98%；Curie 温度 R²≈0.91；热电 zT R² 0.67–0.80（数据噪声大）。带隙预测须区分 PBE 与实验口径（PBE 系统性低估 30–50%），实验带隙最优 MAE ≈ 0.33 eV（MODNet）。
5. **闭环效率**：主动学习/BO 通常以 ≤20 条初始数据、6–9 轮迭代找到目标材料（Xue 2019、Rao 2022）；Sulley 2024 显示约 27% 数据即可达 95% 精度。生成式模型（GNoME、MatterGen）已实现"预测—合成—验证"闭环（736 个 ICSD 匹配；TaCr₂O₆ 实测体模量偏差 <20%）。

---

## 4. 待核实清单（未能从一手可抓取来源确认）

| 项 | 说明 | 建议核实途径 |
|---|---|---|
| MP 2024/2025 中间版本精确条目数 | 现有口径为 v2022.10.28=155k 与 2026 快照 271,325 | https://docs.materialsproject.org/changes/database-versions 逐版本累计 |
| OQMD 当前精确值 | 主站 502，1,407,395 来自搜索快照 | https://www.oqmd.org/ 复核 |
| Ward 2016（Magpie+RF）原始论文 MAE | 本报告采用 Roost 论文的复测值 0.067 | npj Comput. Mater. 2, 16028 (2016) 原文表格 |
| ALIGNN 在 JARVIS-DFT 的形成能/带隙 MAE | 原论文表格未能抓取 | npj Comput. Mater. 7, 185 (2021) 表格 |
| CrabNet 论文 OQMD 表格精确值 | 0.0861 为二手转引 | npj Comput. Mater. 7, 105 (2021) Table 2 |
| MatBERT 各 NER 任务 F1 | 语料规模已核实，逐任务 F1 未列 | Walker et al., Patterns 2 (2021) 表格 |
| OC20/OC22 排行榜精确名次 | 页面为 JS 渲染，快照数值建议复核 | https://opencatalystproject.org/leaderboard.html |
| DRX 数据集总条目数 | DRX-CE 等存在但规模未公布 | Ceder 组论文/数据仓库 |
| Citrine 平台数据规模 | 公开平台已下线，商业规模未公开 | citrine.io 官方口径 |
| jdft2d/phonons/dielectric 任务榜首 | 页面截断 | https://matbench.materialsproject.org/ 分任务页 |
| PoLyInfo 数据点口径（357,812 vs >500k） | 站点与论文统计口径差异 | NIMS 官方说明 |

## 5. 参考来源汇总（主要）

- Materials Project：https://next-gen.materialsproject.org/ ；https://docs.materialsproject.org/changes/database-versions
- OQMD：https://www.oqmd.org/ ；AFLOW：https://www.aflowlib.org/ ；JARVIS：https://jarvis.nist.gov/ ；NOMAD：https://nomad-lab.eu/nomad-lab/index.html
- GNoME：https://www.nature.com/articles/s41586-023-06735-9 ；https://deepmind.google/discover/blog/millions-of-new-materials-discovered-with-deep-learning/
- Alexandria：https://alexandria.icams.rub.de/ ；https://arxiv.org/abs/2512.09169
- Matbench：https://matbench.materialsproject.org/ ；Matbench Discovery：https://matbench-discovery.materialsproject.org/ （模型 yml：https://raw.githubusercontent.com/janosh/matbench-discovery/main/models/mace-mp-0.yml 、https://raw.githubusercontent.com/janosh/matbench-discovery/main/models/m3gnet/m3gnet.yml ）
- 论文：CGCNN https://arxiv.org/abs/1710.10324 ；MEGNet https://arxiv.org/abs/1812.05055 ；ElemNet https://pmc.ncbi.nlm.nih.gov/articles/PMC6279928/ ；Roost https://pmc.ncbi.nlm.nih.gov/articles/PMC7722901/ ；M3GNet https://arxiv.org/abs/2202.02450 ；CHGNet https://arxiv.org/abs/2302.14231 ；MACE-MP-0 https://pubs.aip.org/aip/jcp/article/163/18/184110/3372267/ ；MatterSim https://arxiv.org/abs/2405.04967 ；OMat24 https://arxiv.org/abs/2410.12771 ；Matbench Discovery https://arxiv.org/abs/2308.14920 ；MatterGen https://pmc.ncbi.nlm.nih.gov/articles/PMC11922738/ ；Rao 2022 https://pubmed.ncbi.nlm.nih.gov/36201584/ ；Rao 2024 综述（Xue 转引） https://pmc.ncbi.nlm.nih.gov/articles/PMC11531902/ ；Sulley 2024 https://www.sciencedirect.com/science/article/abs/pii/S135964622400215X
- 实验库：ICSD https://www.fiz-karlsruhe.de/de/produkte-und-dienstleistungen/inorganic-crystal-structure-database-icsd-news ；SpringerMaterials https://www.springernature.com/gp/librarians/products/databases-solutions/springermaterials ；MatWeb http://matweb.com/ ；PoLyInfo https://polymer.nims.go.jp/
- 领域库：ULTERA https://phaseslab.com/ultera ；Battery Explorer https://next-gen.materialsproject.org/batteries ；电池文本库 https://pmc.ncbi.nlm.nih.gov/articles/PMC7411033/ ；DRX https://ceder.berkeley.edu/publications/2025_Peichen_modeling-deltaDRX.pdf ；OC20/OC22 https://opencatalystproject.org/ 、https://arxiv.org/abs/2206.08917
- 文本挖掘：MatBERT https://github.com/lbnlp/MatBERT ；ChemDataExtractor 2.0 https://pubs.acs.org/doi/10.1021/acs.jcim.1c00607
- 实验性能预测：Ren 2023 https://lanlexperts.elsevierpure.com/en/publications/prediction-and-design-of-high-hardness-high-entropy-alloy-through/ ；Zhou 2026 https://www.sciencedirect.com/science/article/pii/S0264127526003059 ；He 2024 https://pure.bit.edu.cn/en/publications/machine-learning-assisted-design-of-refractory-high-entropy-alloy/ ；Wen 2019 https://www.researchgate.net/publication/331693971_Machine_learning_assisted_design_of_high_entropy_alloys_with_desired_property ；Liu 2023（GFA） https://www.sciencedirect.com/science/article/pii/S1359645422008746 、https://www.mdpi.com/2227-9717/11/9/2806 ；Castro 2020 https://www.nature.com/articles/s41427-020-0214-y ；Jung & Cole 2024 https://pmc.ncbi.nlm.nih.gov/articles/PMC11350867/ ；Barua 2025 https://pubmed.ncbi.nlm.nih.gov/39686715/
