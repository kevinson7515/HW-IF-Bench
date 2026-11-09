# 机器学习/深度学习驱动的材料成分配比优化：研究进展、模型应用与产业化前景评估报告

> 编制说明：本报告基于截至 2026 年底的公开文献、基准排行榜、机构官网与产业新闻信息整理；所有关键数据均附来源链接（本报告不引用 www.microsoft.com 与 news.northwestern.edu 及其子域名的内容）。报告聚焦"元素成分配比（composition）→ 材料性能"这一核心链条，同时覆盖其依赖的数据库、模型与验证闭环生态。

---

## 0. 执行摘要

1. **范式已成主流**：机器学习（ML）与深度学习（DL）辅助材料成分设计，已从 2011—2016 年的"描述符 + 浅层模型"阶段，演进到"通用机器学习原子间势（uMLIP）+ 生成式逆向设计 + 自主实验闭环"阶段。领域旗舰综述（[Machine learning for alloys, Nat. Rev. Mater. 2021](https://scholars.duke.edu/individual/pub1493174)）与近两年新综述（[ScienceDirect 2026 合金 ML 综述](https://www.sciencedirect.com/science/article/pii/S3117722026001478/pdf)、[逆向设计综述 2025](https://www.sciencedirect.com/org/science/article/pii/S1546221825001626)）确认该方向为材料信息学的中心议题。
2. **精度已达"计算级可用"**：在形成能预测上，当前最强通用势模型在 Matbench Discovery 排行榜上的 MAE 已降至 **17—18 meV/atom**、发现任务 F1 ≈ **0.93**、发现加速因子（DAF）≈ **6**（[排行榜](https://matbench-discovery.materialsproject.org/)），与 GGA-PBE 级 DFT 自身误差、以及凸包稳定性判定常用的 25 meV/atom 阈值同量级（[DFT 稳定性阈值讨论](https://arxiv.org/html/2607.18092)）。但在成分级实验性能（如实验带隙 MAE≈0.42 eV、钢屈服强度 MAE≈95 MPa，样本仅 312 条）上精度仍受限（[Matbench v0.1 榜单](https://hackingmaterials.lbl.gov/automatminer/datasets.html)）。
3. **数据库基础设施成熟但偏计算**：MP/OQMD/AFLOW/JARVIS/NOMAD/Alexandria/GNoME 构成数百万至数千万级条目的开放计算数据生态（如 [OQMD 140.7 万条](https://www.oqmd.org/)、[AFLOW 392.9 万化合物](https://www.aflowlib.org/)），训练用轨迹数据集已达亿级结构规模（OMat24 1.01 亿、COSMOS 2.43 亿，[数据集总表](https://matbench-discovery.materialsproject.org/data/sets)）；**实验数据与"失败实验"负样本仍是最大缺口**。
4. **成分优化闭环已有端到端示范但验证率有限**：生成式模型 MatterGen 无条件生成的"稳定+新颖+独特（S.U.N.）"率约 **38.6%**，并与实验方合作合成了目标体弹模量 200 GPa 的 TaCr₂O₆（实测 169 GPa）（[Nature 2025](https://www.nature.com/articles/s41586-025-08628-5)、[Foundry Labs 页面](https://labs.ai.azure.com/innovations/mattergen/)）；A-Lab 自主实验室 17 天合成 41/58 个新化合物，但其产物归属与相判定随后受到同行质疑（[Nature 2023](https://www.nature.com/articles/s41586-023-06734-w)、[Chemistry World 质疑报道](https://www.chemistryworld.com/news/new-analysis-raises-doubts-over-autonomous-labs-materials-discoveries/4018791.article)、[C&EN 2026 更正报道](https://cen.acs.org/research-integrity/Nature-robot-chemist-paper-corrected/104/web/2026/01)）。
5. **产业化已真实发生但集中于窄域**：NASA GRX-810 合金（强度 2 倍、蠕变寿命 1000 倍提升）已许可给 4 家美国企业商业化（[Nature 2023](https://www.nature.com/articles/s41586-023-05893-0)、[NASA 许可公告](https://www.nasa.gov/centers-and-facilities/glenn/nasa-licenses-3d-printable-superalloy-to-benefit-us-economy/)）；Matlantis 通用原子模拟平台被 **150+ 企业**使用（[Matlantis 2026 公告](https://matlantis.com/en/news/release-260917/)）；SCG Chemicals 借助 Uncountable 平台实现研发产出 +20%、实验设计工作量 −45%（[Uncountable 案例](https://www.linkedin.com/posts/uncountable-inc_if-your-clients-in-chemicals-materials-activity-7454522291561992192-6709)）。
6. **距"理想模型"的总体判断**：成分→热力学/结构性质的正向预测已接近工程可用；**端到端"性能目标→可合成成分配方"的全自动闭环仍处在 TRL 4—6 区间**。综合技术曲线、资本动向与各国路线图，本报告的判断是：窄垂直领域（合金微调、聚合物/橡胶配方、催化剂/电池材料筛选）3—5 年内成为研发标配（2028—2031）；跨成分—工艺—组织的通用设计大模型 5—10 年（2030—2036）才能在多个材料类同时达到 TRL 7+；而"输入服役性能、输出可量产配方与工艺窗口"的理想模型，属于 **2035 年以后** 的愿景，且更可能以"人机协同"而非全自动形态落地（详见第 8 节）。

---

## 1. 问题界定与研究范式

### 1.1 什么问题在被求解

"材料元素成分配比优化"在 ML 语境下通常拆解为三类任务：

| 任务 | 数学形式 | 典型方法 |
| --- | --- | --- |
| 正向代理（成分→性质） | 学习 f(成分) → 性质，替代昂贵计算/实验 | 成分描述符+树模型、成分 GNN（ElemNet/Roost/CrabNet） |
| 逆向设计（性质→成分） | 在成分空间中搜索/生成满足约束的候选 | 贝叶斯优化、主动学习、生成模型（CDVAE/MatterGen）、进化算法 |
| 闭环验证 | 候选→合成→表征→回灌数据 | 自主实验室（A-Lab、NIMS 自主 AI 网络）、贝叶斯主动学习 |

对多主元合金（高熵合金 HEA）、镍基高温合金、钛合金等体系，成分空间是连续高维的（例如 5 主元各 5—35 at.%），穷举不可行，ML 的价值在于以 10³—10⁶ 倍速度替代 DFT/实验进行筛选（[HEA 数据驱动综述 2024](https://www.nature.com/articles/s43246-024-00487-3)、[Machine learning for alloys 综述](https://scholars.duke.edu/individual/pub1493174)）。

### 1.2 四个发展阶段

1. **描述符+浅层模型（2011—2016）**：MGI（美国材料基因组计划，2011 年启动，[官网](https://www.mgi.gov/mgi-homepage)）推动高通量 DFT 数据开放；Ward 等 2016 年用 145 个 MAGPIE 成分描述符 + 梯度提升树预测无机材料性质，成为被引 2000+ 的奠基工作（[npj Comput. Mater. 2016](https://www.nature.com/articles/npjcompumats201628)）。
2. **深度成分模型（2017—2019）**：ElemNet 直接从元素比例端到端学习（[Sci. Rep. 2018](https://www.nature.com/articles/s41598-018-35934-y)）；Conduit 等用神经网络+全局优化设计出实验验证的新型镍基高温合金（[arXiv/Nat. Mater. 2017](https://arxiv.org/abs/1803.03039)）；文本挖掘开始提取文献中的"暗数据"（[Raccuglia, Nature 2016](https://www.nature.com/articles/nature17439)）。
3. **GNN 与通用势（2020—2023）**：CGCNN/MEGNet/ALIGNN 等图网络引入晶体结构；Roost/CrabNet 把"仅成分"预测推到接近结构模型的精度；M3GNet/CHGNet/PFP 等通用势覆盖几乎整张周期表（89 元素，[M3GNet](https://arxiv.org/abs/2202.02450)）。
4. **生成式 + 自主实验 + LLM（2023 至今）**：GNoME 发现 220 万晶体结构（38 万稳定，[Nature 2023](https://www.nature.com/articles/s41586-023-06735-9)、[DeepMind 博客](https://deepmind.google/blog/millions-of-new-materials-discovered-with-deep-learning/)）；MatterGen 实现按性质约束的扩散式生成（[Nature 2025](https://www.nature.com/articles/s41586-025-08628-5)）；A-Lab 与 NIMS 展示无人合成闭环（[Nature 2023](https://www.nature.com/articles/s41586-023-06734-w)、[NIMS 2025](https://www.nims.go.jp/eng/press/2025/12/202512100.html)）；LLM 智能体（ChemCrow、MatChat、CrystaLLM）进入工作流（[ChemCrow](https://pubmed.ncbi.nlm.nih.gov/38799228/)、[MatChat](https://matchat.cn/)、[CrystaLLM, Nat. Commun. 2024](https://www.nature.com/articles/s41467-024-54639-7)）。

---

## 2. 数据库分析

### 2.1 主要开放计算数据库（成分—性质数据的主体来源）

| 数据库 | 规模（以官方/排行榜为准） | 作用与特点 |
| --- | --- | --- |
| [Materials Project（MP）](https://next-gen.materialsproject.org/) | 2022.10 版 15.5 万条；持续增长（[数据集表](https://matbench-discovery.materialsproject.org/data/sets)） | 事实标准库；提供 API/APPs；2025 年 Nature Materials 论文系统总结其对数据驱动研究的支撑（被引 550+）（[Horton 2025](https://www.nature.com/articles/s41563-025-02272-0)） |
| [OQMD](https://www.oqmd.org/)（西北大学 Wolverton 组） | 140.7 万化合物 | 热力学凸包/相图导向；"百万化合物"历程回顾见 [IOP 2022](https://iopscience.iop.org/article/10.1088/2515-7639/ac7ba9/ampdf) |
| [AFLOW](https://www.aflowlib.org/)（Duke Curtarolo 组） | 392.9 万化合物、8.17 亿条性质 | 最大的高通量计算库；含原型、热力学、电子结构模块（[aflow.org 论文](https://www.sciencedirect.com/science/article/abs/pii/S0927025622005195)） |
| [JARVIS-DFT](https://jarvis-materials-design.github.io/dbdocs/jarvisdft/)（NIST Choudhary 组） | ~4 万 3D + 1000 2D 材料、~百万条性质 | 与 ALIGNN 等 NIST 工具链深度绑定 |
| [NOMAD](https://nomad-lab.eu/nomad-lab/faqs.html)（FHI/FAIRmat） | 数百万至千万级计算条目（聚合 AFLOW/OQMD/MP 等） | FAIR 数据归档与检索，欧洲材料数据基础设施核心 |
| [Alexandria](https://alexandria.icams.rub.de/)（ICAMS-RUB） | 约 310 万材料 / 3050 万结构（[数据集表](https://matbench-discovery.materialsproject.org/data/sets)）；2025 年末扩展版含 580 万结构、17.5 万凸包稳定化合物（[arXiv 2512.09169](https://arxiv.org/html/2512.09169v1)） | MatterGen 等生成模型的训练库之一 |
| GNoME 库 | 8900 万结构 / 600 万材料（部分开放，[数据集表](https://matbench-discovery.materialsproject.org/data/sets)） | 220 万新晶体、~38 万稳定候选（[Nature 2023](https://www.nature.com/articles/s41586-023-06735-9)） |

### 2.2 模型训练用"轨迹/基模型"数据集（决定当前精度上限）

| 数据集 | 规模 | 用途 |
| --- | --- | --- |
| [MPF.2021.2.8](https://matbench-discovery.materialsproject.org/data/sets) | 18.8 万结构 / 6.28 万材料 | M3GNet 等第一代通用势训练集 |
| [MPtrj](https://matbench-discovery.materialsproject.org/data/sets) | 158 万结构 / 14.6 万材料 | CHGNet、MACE-MP-0 等通用势主力训练集（[CHGNet 论文](https://www.nature.com/articles/s42256-023-00716-3)） |
| [OMat24](https://arxiv.org/html/2410.12771v1)（Meta） | 1.01 亿结构（>1 亿次单点 DFT） | 新一代基模型（Equiformer 系、Prophet 等）核心训练集 |
| [sAlex](https://matbench-discovery.materialsproject.org/data/sets) | 1040 万结构 | Alexandria 抽样子集 |
| COSMOS / ELEMENTA 等 | 2.43 亿 / 2.11 亿结构（[数据集表](https://matbench-discovery.materialsproject.org/data/sets)） | 2025 年后出现的"亿级结构"训练集，支撑基模型 scaling |
| MatterGen 训练集 | 60.8 万稳定材料（MP+Alexandria）（[Foundry Labs](https://labs.ai.azure.com/innovations/mattergen/)） | 生成式模型的"正样本"语料 |

**趋势判断**：训练数据从"十万级材料"（2016—2020）跃迁到"亿级结构"（2024—2026），这是 17—18 meV/atom 精度的主要来源；但结构多样性仍受 DFT 采样偏好限制，出现"系统性软化"等偏差（见 7.2）。

### 2.3 实验/文献数据（成分—实验性能的稀缺来源）

- **实验数据集小而贵**：Matbench v0.1 中钢屈服强度仅 312 条（来自 Citrine 公开集）、实验带隙 4604 条（[Matbench v0.1](https://matbench.materialsproject.org/Benchmark%20Info/matbench_v0.1/)）；性能 MAD 高达 229 MPa / 1.14 eV，凸显小样本+高噪声。
- **文献挖掘**：word embeddings 从 330 万篇摘要中无监督提取材料知识（[Tshitoyan, Nature 2019](https://www.nature.com/articles/s41586-019-1335-8)，被引 1600+）；松山湖材料实验室 MatChat 智能体整合数十万篇论文提供可溯源问答（官网称 80 万+，[matchat.cn](https://matchat.cn/)；[21 财经报道](https://www.21jingji.com/article/20250215/herald/b7cefbb68d951222f572a5da3e3eea35.html)）。
- **失败实验/负样本**：Raccuglia 等 2016 年用"失败的水热合成实验"训练模型，预测反应成功率，证明负样本对可合成性判断的决定性价值（[Nature 2016](https://www.nature.com/articles/nature17439)，被引 2200+）——但此类数据几乎全部锁在企业内部。

### 2.4 中国的数据基础设施

- **材料基因工程重点专项**：2016 年启动，设立 45 个项目，强调高通量计算、高通量实验与数据库融合（[宿彦京等，金属学报 2020](https://www.ams.org.cn/article/2020/0412-1961/0412-1961-56-10-1313.shtml)）。
- **北京材料基因工程高精尖创新中心（北科大）**：建有材料基因工程基础及专题数据库、材料信息学知识系统、数据标准规范团队（[官网](https://bjmge.ustb.edu.cn/yanjiuduiwu/yanjiutuandui/cljxgczysjk/cljygczysjk/)）。
- **深势科技/Bohrium 平台**：面向科研的算力+软件+AI 平台，承载 OpenLAM 大原子模型计划（[Bohrium](https://www.bohrium.com/intro)、[DPA-2 发布解读](https://www.alphaxiv.org/zh/abs/2312.15492)）。

### 2.5 数据缺口（数据库层面的问题清单）

1. 计算库以 PBE/PBE+U 为主，与实验热力学存在系统性偏差（GNoME 的 r2SCAN 复核显示 PBE(+U) 稳定性判定的化学依赖性分歧，[arXiv 2610.33101](https://arxiv.org/abs/2610.33101)）；
2. 数据库间存在大量重复结构（[C&EN 2025 报道](https://cen.acs.org/research-integrity/Duplicate-structures-haunt-crystallography-databases/103/web/2025/12)）；
3. 成分—工艺—组织—性能四类数据中，后两者几乎只在企业内部（[数据中心的材料 ML 方法论讨论](https://pmc.ncbi.nlm.nih.gov/articles/PMC8600243/)）。

---

## 3. 模型谱系与精度评估

### 3.1 仅成分输入模型（与"元素配比优化"最直接相关）

| 模型 | 机构 | 思路 | 精度/意义 |
| --- | --- | --- | --- |
| Ward/MAGPIE+GBRT（2016） | UChicago | 145 个人工成分描述符 + 树模型 | 奠基性工作，被引 2000+（[npj Comput. Mater.](https://www.nature.com/articles/npjcompumats201628)） |
| ElemNet（2018） | UChicago/ANL | 纯成分端到端 DNN | 证明可不依赖人工描述符（[Sci. Rep.](https://www.nature.com/articles/s41598-018-35934-y)，被引 750+） |
| Roost（2020） | Cambridge/Samsung AI | 把化学计量"重铸"为消息传递图 | 无结构预测的标杆，被引 540+（[Nat. Commun.](https://www.nature.com/articles/s41467-020-19964-7)） |
| CrabNet（2021） | USC Jianjun Hu 组 | 成分受限的自注意力/Transformer（EDM 表示） | 无结构预测 SOTA 之一，被引 360+（[npj Comput. Mater.](https://www.nature.com/articles/s41524-021-00545-1)）；同组 2024 年 MD-HIT 系统比较成分/结构模型（[npj Comput. Mater. 2024](https://www.nature.com/articles/s41524-024-01426-z)） |
| Finder、MODNet 等 | — | 成分/结构混合、小样本优化 | Matbench 常客（[Matbench 提交列表](https://matbench.materialsproject.org/Benchmark%20Info/matbench_v0.1/)） |

### 3.2 结构感知 GNN（成分优化的"下游放大器"）

- **CGCNN**（Xie & Grossman, PRL 2018，被引 2000+）：晶体图卷积，10⁴ 数据即达高精度（[arXiv:1710.10324](https://arxiv.org/abs/1710.10324)）。
- **MEGNet**（2019，Chem. Mater.）：在 Matbench v0.1 上拿下形成能 0.0327 eV/atom、钙钛矿形成能 0.0417 eV 等最佳成绩（[DOI](https://doi.org/10.1021/acs.chemmater.9b01294)、[Matbench 榜](https://hackingmaterials.lbl.gov/automatminer/datasets.html)）。
- **ALIGNN**（2021）：引入键角线图，较 CGCNN/MEGNet/SchNet 最高改善 43.6%，覆盖 52 个固态性质（[npj Comput. Mater.](https://www.nature.com/articles/s41524-021-00650-1)，被引 870+；[arXiv:2106.01829](https://arxiv.org/abs/2106.01829)）。

### 3.3 通用机器学习原子间势（uMLIP）——当前精度天花板

uMLIP 是"成分优化"基础设施中最关键的一层：给定任意成分/结构即可弛豫、算凸包、算声子，速度比 DFT 快 3—6 个数量级。

**Matbench Discovery 排行榜（截至 2026 年末，Discovery 任务、unique prototypes）前列模型**（[排行榜](https://matbench-discovery.materialsproject.org/)，指标定义见[论文 Nature Machine Intelligence 2025](https://nature.com/articles/s42256-025-01055-1)）：

| 排名 | 模型（机构） | F1 | DAF | MAE (eV/atom) | R² | 训练数据 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | DPA-4.1-Max-OAM-PFT（北京科学智能研究院 AISI + IAPCM） | 0.935 | 6.09 | 0.017 | 0.872 | 661 万结构（MPtrj+OMat24+sAlex+MDR-MP） |
| 2 | Prophet-OAME-MBD（Kairos Materials，初创公司） | 0.928 | 6.07 | 0.018 | 0.869 | 1640 万结构（含 ELEMENTA） |
| 3 | DPA-4.1-Max-OAM（AISI+IAPCM） | 0.933 | 6.16 | 0.017 | 0.872 | 660 万结构 |
| 4 | TECE-OAM-RRA-1.0（上海科技大学） | 0.929 | 6.07 | 0.018 | 0.871 | 660 万结构 |
| 5 | EquFlashV2（三星电子） | 0.929 | 6.07 | 0.018 | 0.873 | 660 万结构 |
| 6 | EquiformerV3+DeNS（MIT） | 0.931 | 6.07 | 0.018 | 0.868 | 660 万结构 |
| 7 | GRACE-3L-OAM-L（波鸿鲁尔大学 ICAMS） | 0.925 | 6.04 | 0.018 | 0.875 | 660 万结构 |

代表性早期通用势（精度低一档但奠基）：M3GNet（89 元素，[arXiv:2202.02450](https://arxiv.org/abs/2202.02450)）、CHGNet（含磁序信息，[Nat. Mach. Intell. 2023](https://www.nature.com/articles/s42256-023-00716-3)，被引 1600+）、PFP/Matlantis（45 元素，[Nat. Commun. 2022](https://www.nature.com/articles/s41467-022-30687-9)）、MatterSim（[arXiv:2405.04967](https://arxiv.org/abs/2405.04967)）、DPA-2（73 元素、18 个数据集多任务预训练，[arXiv:2312.15492](https://arxiv.org/abs/2312.15492)）。

### 3.4 生成式/逆向设计模型

| 模型 | 类型 | 关键结果 |
| --- | --- | --- |
| CDVAE（2022，ICML；被引 700+） | 扩散 VAE，以稳定性为归纳偏置生成晶体 | 生成式晶体设计的转折点（[arXiv:2110.06197](https://arxiv.org/abs/2110.06197)） |
| MatterGen（2023 预印本 / Nature 2025，被引 1250+） | 扩散生成元素+坐标+晶格，可按体弹模量/带隙/磁性/化学体系微调 | 生成物新颖+稳定概率是此前模型 2 倍以上；S.U.N. 率 38.57%（无条件）；实验合成 TaCr₂O₆（目标 200 GPa，实测 169 GPa）（[Nature](https://www.nature.com/articles/s41586-025-08628-5)、[arXiv](https://arxiv.org/abs/2312.03687)、[Foundry Labs](https://labs.ai.azure.com/innovations/mattergen/)） |
| GNoME（DeepMind，2023，被引 2500+） | 图网络+主动学习+蒸馏 | 22 天等效"800 年"知识增量：220 万结构、~38 万稳定候选（[Nature](https://www.nature.com/articles/s41586-023-06735-9)、[博客](https://deepmind.google/blog/millions-of-new-materials-discovered-with-deep-learning/)） |
| CrystaLLM（2023/2024） | 把 CIF 文件当"语言"自回归生成结构 | NLP 范式迁移的代表性尝试（[Nat. Commun. 2024](https://www.nature.com/articles/s41467-024-54639-7)） |

### 3.5 优化与闭环：贝叶斯优化、主动学习、自主实验

- **贝叶斯优化**在三元随机合金成分设计中早期示范（[Tran & Kalidindi 2020](https://arxiv.org/abs/2006.00139)）；近年用于 Nb 合金等最优成分搜索（[Ghorbani 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11004116/)）。
- **A-Lab**（Berkeley/LBNL，Nature 2023）：主动学习驱动，17 天 21 次/天实验合成 41/58 个目标化合物（[论文](https://www.nature.com/articles/s41586-023-06734-w)）；随后遭 Palgrave 等对相鉴定（Rietveld）的公开质疑（[Nature 新闻](https://www.nature.com/articles/d41586-023-03956-w)、[Chemistry World](https://www.chemistryworld.com/news/new-analysis-raises-doubts-over-autonomous-labs-materials-discoveries/4018791.article)），论文 2026 年被更正（[C&EN](https://cen.acs.org/research-integrity/Nature-robot-chemist-paper-corrected/104/web/2026/01)）。
- **NIMS**（日本物质材料研究机构）2025 年发布"多自主 AI 系统网络"技术（[新闻稿](https://www.nims.go.jp/eng/press/2025/12/202512100.html)）。
- **自驱实验室（SDL）系统综述**：ACS Chem. Rev. 2024（被引 1100+）与技术综述 2025（[Tom 2024](https://pubs.acs.org/chreay/article/124/16/9633/154652/Self-Driving-Laboratories-for-Chemistry-and)、[Tobias 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12368842/)、[C&EN 2026 现状报道](https://cen.acs.org/physical-chemistry/computational-chemistry/Self-driving-labs-changing-chemists/104/web/2026/06)）。

### 3.6 合金领域专用模型的精度（成分配比优化的直接战场）

| 对象 | 模型/研究 | 精度 |
| --- | --- | --- |
| 镍基高温合金设计 | Conduit 2017 神经网络+多目标优化 | 设计并实验验证了兼顾成本/密度/γ′含量/solvus 的新合金（[arXiv](https://arxiv.org/abs/1803.03039)，被引 200+；Nature Materials 2017 原文） |
| 双相钛合金 | Wen 2019（经验知识+ML 混合框架） | 实验验证强度—塑性更优的新双相 Ti 合金（[Acta Mater.](https://www.sciencedirect.com/science/article/abs/pii/S1359645419301430)，被引 1000+） |
| HEA 硬度 | Shen 2023，XGBoost | RMSE 52.66 HV / MAE 26.49 HV，原子半径差 δ 为最重要特征（[论文](https://www.sciencedirect.com/science/article/abs/pii/S0966979523002108)） |
| HEA 相形成（FCC/BCC/IM 等） | Jain 2024 | FCC 89.1%、FCC+IM 86.11% 分类准确率（[论文](https://www.sciencedirect.com/science/article/pii/S2949917824000579)）；Peivaste 2023 亦得 XGBoost 最优（[Sci. Rep.](https://www.nature.com/articles/s41598-023-50044-0)） |
| 钢屈服强度（仅成分） | Matbench v0.1（n=312） | 最佳 MAE 95.2 MPa（数据 MAD 229.4 MPa）（[榜](https://hackingmaterials.lbl.gov/automatminer/datasets.html)） |
| 实验带隙（仅成分，n=4604） | Matbench v0.1 | 最佳 MAE 0.416 eV（MAD 1.14 eV） |
| 聚酰亚胺介电常数 | He 2025 | 3 个新聚酰亚胺合成验证，预测与实测吻合（[Polymers](https://www.mdpi.com/2073-4360/17/12/1622)） |
| 聚合物电介质 | Mannodi-Kanakkithodi 2016（Ramprasad 组） | ML 预测+DFT 计算与实验测量三向吻合（[Sci. Rep.](https://www.nature.com/articles/srep20952)，被引 480+；[Polymer Genome 平台](https://pubs.acs.org/jpccck/article/122/31/17575/1470511/Polymer-Genome-A-Data-Powered-Polymer-Informatics)） |

### 3.7 精度评估的基准体系与解读

**基准 1：Matbench v0.1（13 个任务，2020）**——任务清单与官方"verified top score"（[自动榜单](https://hackingmaterials.lbl.gov/automatminer/datasets.html)、[任务详情](https://matbench.materialsproject.org/Benchmark%20Info/matbench_v0.1/)、[论文 DOI](https://doi.org/10.1038/s41524-020-00406-3)）：

| 任务（输入类型） | 样本 | 最佳成绩 | 意义 |
| --- | --- | --- | --- |
| mp_e_form（结构） | 132,752 | 0.0327 eV/atom（MEGNet） | MAD 1.006→降 31 倍 |
| mp_gap（结构） | 106,113 | 0.228 eV（CGCNN） | 带隙仍是最难任务之一 |
| perovskites（结构） | 18,928 | 0.0417 eV/cell（MEGNet） | — |
| expt_gap（成分） | 4,604 | 0.416 eV | 实验性质更难 |
| steels 屈服强度（成分） | 312 | 95.2 MPa | 小样本典型 |
| glass 形成能力（成分，分类） | 5,680 | ROCAUC 0.861 | 成分分类可用 |

**基准 2：Matbench Discovery（WBM 独立测试集，2023—2026）**：以"模型能否发现 WBM 中的稳定材料"为核心，报告 F1/DAF/MAE/κ_SRME/RMSD 等（[论文 Nature Machine Intelligence 2025](https://nature.com/articles/s42256-025-01055-1)、[arXiv:2308.14920](https://arxiv.org/html/2308.14920v3)）。当前榜首 F1≈0.93、DAF≈6、MAE≈17 meV/atom；论文基准发布时（2023）第一代 uMLIP 的 F1 明显低于此，三年内被scaling 推高约 15—20 个百分点。

**精度解读（工程视角）**：
- 热力学量（形成能、凸包）在插值域内已达 DFT 置信水平（17—18 vs ~25 meV/atom 阈值），**可用于驱动成分筛选流水线**；
- 发现级 F1 0.93 意味着模型判定"稳定"的材料中仍有约 7—15% 假阳性（unique prototype 口径），**必须保留 DFT/实验复核环节**；
- 成分→实验宏观性能（屈服强度、断裂韧性、腐蚀、疲劳）因样本量（10²—10³）和工艺耦合，误差普遍在工程容差边缘，**只能做排序/方向指导，不能直接定牌**；
- uMLIP 存在"系统性软化"（体积预测偏大）与外推失稳等已知病态（[npj Comput. Mater. 2025](https://www.nature.com/articles/s41524-024-01500-6)；系统评测见 [Wiley 2024](https://onlinelibrary.wiley.com/doi/full/10.1002/mgea.58)）。

---

## 4. 活跃研究课题组图谱

### 4.1 美洲

| 课题组/机构 | 成分配比优化方向 | 代表成果 |
| --- | --- | --- |
| UC Berkeley / LBNL（Gerbrand Ceder 组） | 高通量计算+自主合成闭环（A-Lab）；电池/电解质成分筛选 | [Materials Project](https://next-gen.materialsproject.org/)；[A-Lab, Nature 2023](https://www.nature.com/articles/s41586-023-06734-w)；[LBL 新闻：GNoME 数据并入 MP](https://newscenter.lbl.gov/2023/11/29/google-deepmind-new-compounds-materials-project/) |
| UCSD（Shyue Ping Ong 组，Materials Virtual Lab） | 通用势、电池材料成分—电压/稳定性筛选 | M3GNet（89 元素，[arXiv:2202.02450](https://arxiv.org/abs/2202.02450)） |
| MIT（Jeffrey Grossman、孔敬等；Tian Xie 出自该组） | CGCNN（成分+结构表示）；生成式 | [CGCNN PRL 2018](https://arxiv.org/abs/1710.10324)；CDVAE、MatterGen（Tian Xie 现 Microsoft Research，[arXiv:2312.03687](https://arxiv.org/abs/2312.03687)）；[EquiformerV3](https://arxiv.org/abs/2604.09130) 亦登顶 Matbench Discovery |
| UChicago（Rampi Ramprasad 组） | 聚合物基因组/成分—介电性能优化（Matmerize 创始来源） | [Polymer Genome](https://pubs.acs.org/jpccck/article/122/31/17575/1470511/Polymer-Genome-A-Data-Powered-Polymer-Informatics)；[Matmerize](https://www.matmerize.com/) |
| USC（Jianjun Hu 组） | 无结构成分预测、外推性能预测、主动学习 | [CrabNet](https://www.nature.com/articles/s41524-021-00545-1)；[MD-HIT](https://www.nature.com/articles/s41524-024-01426-z) |
| NIST（Kamal Choudhary 组） | JARVIS 数据库+ALIGNN 全家桶 | [ALIGNN](https://www.nature.com/articles/s41524-021-00650-1)、[JARVIS](https://jarvis-materials-design.github.io/dbdocs/jarvisdft/) |
| Duke（Curtarolo 组） | AFLOW 生态、合金 CALPHAD+ML、合金设计综述 | [aflowlib.org](https://www.aflowlib.org/)；[Machine learning for alloys 综述](https://scholars.duke.edu/individual/pub1493174) |
| BYU（Gus Hart 组） | 合金 ML 综述、相图 ML | [Nat. Rev. Mater. 2021](https://scholars.duke.edu/individual/pub1493174) |
| 西北大学（Chris Wolverton 组） | OQMD、高通量热力学、多主元合金 | [oqmd.org](https://www.oqmd.org/) |
| LANL（Lookman、Pilania 等） | 主动学习加速实验、外推性分析 | [多保真贝叶斯合金设计](https://arxiv.org/abs/2006.00139)；[外推量化研究](https://pubs.acs.org/jctcce/article/22/13/6917/5164109/) |
| 马里兰大学（Ichiro Takeuchi 组） | 组合薄膜+原位 ML 自主搜索 | 领域经典（见[合金 ML 综述](https://scholars.duke.edu/individual/pub1493174)） |
| CMU（Zachary Ulissi 组） | Open Catalyst（成分—催化剂表面） | OC20/OC22（OMat24 生态，[arXiv:2410.12771](https://arxiv.org/html/2410.12771v1)） |
| NASA Glenn | GRX-810、难熔合金 ML 回归+热力学设计 | [GRX-810, Nature 2023](https://www.nature.com/articles/s41586-023-05893-0)；[难熔合金资助项目](https://www.nasa.gov/directorates/stmd/space-tech-research-grants/design-of-refractory-alloys-for-processing-by-additive-manufacturing-and-service-at-extremely-high-temperatures/) |

### 4.2 欧洲

| 课题组/机构 | 方向 | 代表成果 |
| --- | --- | --- |
| 剑桥大学（Alpha Lee 组；Rhys Goodall 等） | 无结构成分表示（Roost）、Matbench Discovery 基准 | [Roost](https://www.nature.com/articles/s41467-020-19964-7)；[Matbench Discovery](https://nature.com/articles/s42256-025-01055-1) |
| 剑桥（Gareth Conduit；衍生公司 Alloyed） | 神经网络+全局优化设计超合金 | [Conduit 合金设计](https://arxiv.org/abs/1803.03039)；[ABD-900AM](https://www.metal-am.com/aubert-duval-and-alloyed-to-discuss-new-ni-based-superalloy-in-free-webinar/) |
| EPFL（Marzari、Ceriotti 组） | Materials Cloud、表示学习、数据 FAIR | NOMAD/Materials Cloud 生态（[NOMAD](https://nomad-lab.eu/nomad-lab/faqs.html)） |
| 波鸿鲁尔大学 ICAMS（ maintained Alexandria、GRACE） | 大规模数据库+势函数 | [Alexandria](https://alexandria.icams.rub.de/)；[GRACE-3L 登顶](https://matbench-discovery.materialsproject.org/) |
| FHI Berlin / FAIRmat（Scheffler 等） | NOMAD 数据基础设施 | [NOMAD](https://nomad-lab.eu/nomad-lab/faqs.html) |
| 三星 AI 剑桥 | 成分表示、生成模型 | EquFlashV2 登顶 [Matbench Discovery](https://matbench-discovery.materialsproject.org/) |

### 4.3 亚太

| 课题组/机构 | 方向 | 代表成果 |
| --- | --- | --- |
| 中科院金属所 材料人工智能研究部（主任陈星秋） | AI 驱动跨尺度模拟、多主元合金机器学习势、高通量相图 | [研究部主页](http://imr.cas.cn/jgsz/synl/202604/t20260410_8183678.html)；[陈星秋简介](https://imr.cas.cn/gkjj/xrsld/202309/t20230921_8063555.html) |
| 松山湖材料实验室 | 材料大模型智能体（MatChat）、铁基非晶/难熔高熵合金 ML 软磁/力学预测 | [MatChat](https://matchat.cn/)；[吕志超报告（非晶/HEA 数据驱动）](https://www.bmgforming.com/conference-activity/6477.html) |
| 北京科学智能研究院 AISI / 深势科技（张林峰、鄂维南生态） | DPA 系列大原子模型（DPA-2 覆盖 73 元素）、Bohrium 平台、OpenLAM 计划 | [DPA-2](https://arxiv.org/abs/2312.15492)；[DPA-4.1 登顶 Matbench Discovery](https://matbench-discovery.materialsproject.org/)；[Bohrium](https://www.bohrium.com/intro) |
| 上海科技大学 | TECE 通用势（Matbench Discovery 前列） | [TECE, arXiv 2607.10664](https://arxiv.org/abs/2607.10664) |
| 北京科技大学（北京材料基因工程高精尖中心；宿彦京等） | 材料基因工程数据库、数据标准 | [中心数据库团队](https://bjmge.ustb.edu.cn/yanjiuduiwu/yanjiutuandui/cljxgczysjk/cljygczysjk/)；[材料基因工程综述](https://www.ams.org.cn/article/2020/0412-1961/0412-1961-56-10-1313.shtml) |
| 东京大学（Koji Tsuda 组）等日本团队 | 材料 GNN、数据驱动相图 | 见[合金 ML 综述](https://scholars.duke.edu/individual/pub1493174) |
| NIMS（日本） | 数据驱动材料开发（DDM）部门、自主 AI 网络 | [NIMS 2025 新闻](https://www.nims.go.jp/eng/press/2025/12/202512100.html) |
| Preferred Networks（PFN，工业界） | PFP 通用势（45 元素）、Matlantis | [PFP, Nat. Commun. 2022](https://www.nature.com/articles/s41467-022-30687-9)；[Matlantis](https://matlantis.com/en/news/release-260917/) |

### 4.4 企业研究院

Google DeepMind（GNoME）、Microsoft Research（MatterGen/MatterSim；引用见 [Nature](https://www.nature.com/articles/s41586-025-08628-5) 与 [arXiv:2405.04967](https://arxiv.org/abs/2405.04967)）、Meta FAIR（[OMat24](https://arxiv.org/html/2410.12771v1)）、三星电子（[EquFlashV2](https://matbench-discovery.materialsproject.org/)）、丰田研究院 TRI（[Materials Discovery 项目](http://www.tri.global/materials-discovery)）、NVIDIA（[ALCHEMI 计划](https://developer.nvidia.com/blog/revolutionizing-ai-driven-material-discovery-using-nvidia-alchemi/)）、Kairos Materials（[Prophet 模型](https://www.kairosmaterials.com/papers/Prophet.pdf)）。

---

## 5. 代表性论文清单（按主题）

**综述与路线图**
- Machine learning for alloys, Nat. Rev. Mater. 2021（Hart/Mueller/Toher/Curtarolo）— [链接](https://scholars.duke.edu/individual/pub1493174)
- Machine learning for high-performance alloy design（2026 综述）— [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S3117722026001478/pdf)
- Machine Learning-Based Methods for Materials Inverse Design（2025 综述）— [链接](https://www.sciencedirect.com/org/science/article/pii/S1546221825001626)
- AI-driven inverse design of materials: past, present and future — [arXiv:2411.09429](https://arxiv.org/html/2411.09429v1)
- HEA 数据驱动高通量综述（2024）— [链接](https://www.nature.com/articles/s43246-024-00487-3)

**成分/结构性质预测模型**：Ward 2016（[npj Comput. Mater.](https://www.nature.com/articles/npjcompumats201628)）、ElemNet（[Sci. Rep.](https://www.nature.com/articles/s41598-018-35934-y)）、CGCNN（[PRL/arXiv](https://arxiv.org/abs/1710.10324)）、Roost（[Nat. Commun.](https://www.nature.com/articles/s41467-020-19964-7)）、CrabNet（[npj Comput. Mater.](https://www.nature.com/articles/s41524-021-00545-1)）、ALIGNN（[npj Comput. Mater.](https://www.nature.com/articles/s41524-021-00650-1)）、MEGNet（[Chem. Mater.](https://doi.org/10.1021/acs.chemmater.9b01294)）。

**通用势/基模型**：M3GNet（[arXiv](https://arxiv.org/abs/2202.02450)）、CHGNet（[Nat. Mach. Intell.](https://www.nature.com/articles/s42256-023-00716-3)）、PFP（[Nat. Commun.](https://www.nature.com/articles/s41467-022-30687-9)）、MatterSim（[arXiv](https://arxiv.org/abs/2405.04967)）、DPA-2（[arXiv](https://arxiv.org/abs/2312.15492)）。

**生成式与发现**：CDVAE（[arXiv:2110.06197](https://arxiv.org/abs/2110.06197)）、MatterGen（[Nature 2025](https://www.nature.com/articles/s41586-025-08628-5)）、GNoME（[Nature 2023](https://www.nature.com/articles/s41586-023-06735-9)）、CrystaLLM（[Nat. Commun.](https://www.nature.com/articles/s41467-024-54639-7)）。

**闭环与自主实验**：A-Lab（[Nature 2023](https://www.nature.com/articles/s41586-023-06734-w)）、自驱实验室综述（[ACS Chem. Rev. 2024](https://pubs.acs.org/chreay/article/124/16/9633/154652/Self-Driving-Laboratories-for-Chemistry-and)）、Bayesian 优化合金设计（[arXiv:2006.00139](https://arxiv.org/abs/2006.00139)）。

**成分设计落地案例**：Conduit 镍基超合金（[arXiv:1803.03039](https://arxiv.org/abs/1803.03039)）、Wen 双相钛合金（[Acta Mater. 2019](https://www.sciencedirect.com/science/article/abs/pii/S1359645419301430)）、GRX-810（[Nature 2023](https://www.nature.com/articles/s41586-023-05893-0)）、HEA 成分设计四步法（[Zhou 2024](https://www.mdpi.com/2075-4701/14/8/952)）。

**数据与文本挖掘**：Raccuglia 2016（[Nature](https://www.nature.com/articles/nature17439)）、Tshitoyan 2019（[Nature](https://www.nature.com/articles/s41586-019-1335-8)）、MatChat（[matchat.cn](https://matchat.cn/)）。

**可合成性与可信度**：SynthNN（[npj Comput. Mater. 2023](https://www.nature.com/articles/s41524-023-01114-4)）、Zhu 2023（[ACS Omega](https://pubs.acs.org/acsodf/article/8/9/8210/344172/)）、外推量化（[JCTC 2022](https://pubs.acs.org/jctcce/article/22/13/6917/5164109/)）、uMLIP 系统性软化（[npj Comput. Mater. 2025](https://www.nature.com/articles/s41524-024-01500-6)）、GNoME r2SCAN 审计（[arXiv:2610.33101](https://arxiv.org/abs/2610.33101)）。

---

## 6. 典型应用案例剖析

### 6.1 学术验证（模型确实"设计出了更好成分"的硬证据）

| 案例 | 成分优化对象 | 结果 |
| --- | --- | --- |
| 镍基高温合金（2017） | 成本/密度/γ′/solvus 多目标下的 Ni 基成分 | 神经网络设计→实验验证合格，开创"ML 直接给出工业合金成分"先例（[论文](https://arxiv.org/abs/1803.03039)） |
| GRX-810（NASA，2023） | NiCoCr 基 + 氧化物弥散（ODS）增材制造成分 | 强度 2 倍、蠕变寿命 1000 倍；计算热力学模型驱动的代表（[Nature](https://www.nature.com/articles/s41586-023-05893-0)） |
| 双相钛合金（2019） | 强度—塑性兼顾的 Ti 合金成分 | ML+经验知识混合框架设计并实验验证（[论文](https://www.sciencedirect.com/science/article/abs/pii/S1359645419301430)，被引 1000+） |
| 高熵合金（2023—2024） | 硬度/相组成多主元成分 | XGB 硬度 MAE≈26.5 HV；相分类 86—89%；"数据准备→建模→设计→实验验证"四步法成为标准范式（[Shen 2023](https://www.sciencedirect.com/science/article/abs/pii/S0966979523002108)、[Jain 2024](https://www.sciencedirect.com/science/article/pii/S2949917824000579)、[Zhou 2024](https://www.mdpi.com/2075-4701/14/8/952)） |
| 聚合物电介质/聚酰亚胺 | 链段成分/官能团配比 | 预测-合成-表征闭环（[Ramprasad 系](https://www.nature.com/articles/srep20952)、[He 2025](https://www.mdpi.com/2073-4360/17/12/1622)） |
| MatterGen→TaCr₂O₆ | 目标体弹模量 200 GPa 的氧化物成分 | 实测 169 GPa，生成式模型首个"性质条件+实验合成"闭环案例之一（[Foundry Labs](https://labs.ai.azure.com/innovations/mattergen/)、[Nature](https://www.nature.com/articles/s41586-025-08628-5)） |

### 6.2 产业部署（真金白银的证据）

| 企业/平台 | 定位 | 关键事实 |
| --- | --- | --- |
| [Matlantis（PFN+ENEOS）](https://matlantis.com/en/news/release-260917/) | SaaS 通用原子模拟 | 2026 年公告：150+ 企业使用；ENEOS 用其筛选催化剂；已在美设 PFCC 运营（[美区发布](https://matlantis.com/en/news/matlantis-us-launch/)、[2022 大更新](https://www.preferred.jp/en/news/pr20220916)） |
| [Uncountable](https://www.uncountable.com/) | R&D 数据+AI 平台（配方起家） | 客户含 Clariant、SCG Chemicals（研发产出 +20%、DOE 工作量 −45%）（[客户页](https://www.uncountable.com/resources-old/customers)、[SCG 案例](https://www.linkedin.com/posts/uncountable-inc_if-your-clients-in-chemicals-materials-activity-7454522291561992192-6709)、[MIT News 2021](https://news.mit.edu/2021/uncountable-rd-0713)） |
| [Citrine Informatics](https://citrine.io/) | 材料/化学品企业 SaaS | 2025 年入选 CleanAI 60、获 30 万美元联邦资助支持聚变材料技术（[新闻室](https://citrine.io/media-type/press-releases/)）；早期 A 轮 760 万美元（[公告](https://citrine.io/media-post/citrine-informatics-raises-7-6m-to-revolutionize-materials-driven-product-development-with-ai/)） |
| [QuesTek Innovations](https://questek.com/forged-to-win-how-a-navy-alloy-ended-up-on-a-fighting-robot/) | ICME 商业化鼻祖（Ferrium 钢） | Ferrium M54 服务美海军起落架；ICMD SaaS 平台输出"成分+工艺"设计 |
| Alloyed → [ABD-900AM](https://www.metal-am.com/aubert-duval-and-alloyed-to-discuss-new-ni-based-superalloy-in-free-webinar/)（与 Aubert & Duval） | 增材制造镍基超合金 | 对比 IN718：>800 ℃ 屈服提升 ≥30%；[产品页](https://www.aubertduval.com/en/products/stellar-abd-900am-powder-for-additive-manufacturing/) |
| NASA GRX-810 商业化 | 高温增材合金 | 已许可 4 家美国企业（Carpenter、Elementum 3D、Linde 等）量产（[NASA 公告](https://www.nasa.gov/centers-and-facilities/glenn/nasa-licenses-3d-printable-superalloy-to-benefit-us-economy/)、[Elementum 3D 首批交付](https://www.elementum3d.com/elementum-3d-first-to-commercialize-nasas-breakthrough-high-temp-am-superalloy-grx-810/)、[许可方名单](https://www.voxelmatters.com/nasa-licenses-3d-printable-grx-810-superalloy/)） |
| [Orbital Industries](https://fortune.com/2026/05/28/exclusive-orbital-industries-raises-50-million-series-b-funding-round-ai-to-discover-exotic-new-materials/) | AI 材料初创 | 2026 年 5 月完成 5000 万美元 B 轮（Plural 领投）；方向含数据中心冷却/电池材料（[C&EN 介绍](https://cen.acs.org/physical-chemistry/computational-chemistry/Orbital-Materials-applies-AI-to-the-search-for-cleantech-materials/102/i35)） |
| [Entalpic](https://entalpic.ai/)（法国） | 生成式 AI 材料/化学 | 850 万欧元种子轮（Breega/Cathay 等）（[公告](https://welcometoparissaclay.com/en/event-gen-ai-startup-entalpic-announces-funding/)） |
| [Kairos Materials](https://www.kairosmaterials.com/papers/Prophet.pdf) | 通用势基模型初创 | Prophet 模型位居 Matbench Discovery 第 2（[排行榜](https://matbench-discovery.materialsproject.org/)） |
| [Intellegens（Alchemite）](https://intellegens.com/intellegens-and-ansys-to-empower-additive-manufacturing/) | 稀疏数据深度学习 | 与 Ansys Granta MI 集成，服务增材制造航空航天合金 |
| [TRI 丰田研究院](http://www.tri.global/materials-discovery) | 材料+AI+机器人闭环 | AMDD 计划聚焦电池/催化等材料加速 |

---

## 7. 挑战与模型可行性分析

### 7.1 挑战一：数据——小、偏、缺负样本

- **已合成偏差**：公开库只包含"自然界/文献已出现"的成分，模型在已知区域插值优异、越界即失效（外推量化研究表明成分外推误差随化学距离快速增长，[JCTC 2022](https://pubs.acs.org/jctcce/article/22/13/6917/5164109/)）。
- **负样本缺失**：失败实验几乎不发表，可合成性模型先天营养不良（[Raccuglia 2016](https://www.nature.com/articles/nature17439) 的价值正在于此）。
- **实验-计算鸿沟与重复污染**：以数据中心方法可显著改善（[Bartel 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8600243/)）；数据库间重复结构需要专门清洗（[C&EN 2025](https://cen.acs.org/research-integrity/Duplicate-structures-haunt-crystallography-databases/103/web/2025/12)）。

### 7.2 挑战二：泛化与外推

- uMLIP 的"系统性软化"（体积偏大、近邻分布偏软）已被系统测量（[npj Comput. Mater. 2025](https://www.nature.com/articles/s41524-024-01500-6)）；
- 对 M3GNet-DIRECT/CHGNet/MACE-MP-0/ALIGNN 的横评表明：排行榜精度 ≠ 真实模拟可靠性，需按体系验证（[Wiley 2024](https://onlinelibrary.wiley.com/doi/full/10.1002/mgea.58)）；
- 成分空间中"新主元体系"（如全新难熔组合）的预测仍是外推，模型给出的凸包稳定性不可尽信。

### 7.3 挑战三：可合成性与验证闭环

- 热力学稳定 ≠ 可合成：SynthNN 等专门模型学习"合成可行性"（[npj Comput. Mater. 2023](https://www.nature.com/articles/s41524-023-01114-4)、[ACS Omega 2023](https://pubs.acs.org/acsodf/article/8/9/8210/344172/)）。
- GNoME 的 PBE(+U) 稳定性标签在 r2SCAN 复核下呈"化学依赖的分歧"：二元/三元总体 84% 保持稳定，但按化学体系分解后稳定保持率跨度高达 26.7 个百分点，含 U 修正元素体系分歧概率显著升高（OR≈3.45）（[arXiv:2610.33101](https://arxiv.org/abs/2610.33101)）。
- A-Lab 的教训：自动合成+自动 XRD+Rietveld 的相判定可靠性被同行质疑，论文更正后仍存争议（[Nature 新闻](https://www.nature.com/articles/d41586-023-03956-w)、[Chemistry World](https://www.chemistryworld.com/news/new-analysis-raises-doubts-over-autonomous-labs-materials-discoveries/4018791.article)、[C&EN 2026](https://cen.acs.org/research-integrity/Nature-robot-chemist-paper-corrected/104/web/2026/01)）。**结论：闭环的价值已被证明，但"无人判定"的置信度尚不足以替代专家表征。**

### 7.4 挑战四：成分—工艺—组织—性能链条断裂

- 成分只解释了性能的一部分方差；工艺（热处理、增材参数）与微观组织数据几乎全在企业内部（[Machine learning for alloys 综述](https://scholars.duke.edu/individual/pub1493174)、[Dierk Raabe：冶金中的 ML](https://www.dierk-raabe.com/machine-learning-ai-in-metallurgy/)）。
- 服役性能（疲劳、蠕变、腐蚀）是长周期数据，ML 模型多止步于"加速初筛"。
- 多目标（强度/韧性/成本/可持续性）权重设定需要工程决策逻辑介入，纯模型不可代办。

### 7.5 挑战五：不确定性与可信度

- UQ 方法综述指出材料 ML 的 UQ 实践远落后于预测精度竞赛（[Renew. Sustain. Energy Rev. 2025 系统综述](https://www.sciencedirect.com/science/article/abs/pii/S1364032125004903)）。
- 可复现性问题：从基准泄漏到"纸面 SOTA"（[材料信息学可复现性研究](https://pubs.rsc.org/dd/article/3/2/281/804967/Reproducibility-in-materials-informatics-lessons)）。

### 7.6 模型可行性矩阵（按应用场景）

| 场景 | 数据可得性 | 现有精度 | **可行性结论** |
| --- | --- | --- | --- |
| 已知体系内成分微调（超合金/钛合金/钢成分-热力学量） | 高（CALPHAD+DFT+企业数据） | 热力学量 MAE≈17—33 meV/atom | ✅ **已可行**，正成为设计工具标配 |
| 富实验数据的配方优化（橡胶/涂料/聚合物/混凝土） | 中-高（企业内部） | 排序与方向预测可靠（SCG 案例 +20% 产出） | ✅ **已可行**（前提：企业先治理好自身数据） |
| 新成分空间筛选（电池/催化剂/热电候选） | 高（uMLIP 虚拟筛选） | 发现 F1≈0.93，仍需 DFT/实验复核 | ⚠️ **部分可行**：作为"漏斗第一层"极有效，作为"终审"不可靠 |
| 性质条件生成新化合物（MatterGen 类） | 中（稳定相正样本 60 万级） | S.U.N.≈38.6% | ⚠️ **部分可行**：候选质量已超随机采样一个量级，但命中率仍低 |
| 成分→服役性能端到端（疲劳/腐蚀/蠕变寿命） | 低（工艺耦合+长周期） | 误差常超工程容差 | ❌ **尚不可行**，仅作排序参考 |
| 全自动闭环无人研发 | 中（自主实验室初代） | A-Lab 41/58（有争议）；NIMS 多智能体网络初期 | ❌ **尚不可行**：验证与表征环节不可全自动化 |

---

## 8. 距离理想模型的大规模应用与产业化还有多远

### 8.1 先定义"理想模型"

一个可产业化的理想系统应同时满足：
1. 输入：多目标服役性能（含成本/可持续性约束）；
2. 输出：可直接投产的成分配方 + 工艺窗口（含合成路线建议）；
3. 全程带不确定性量化（UQ），并给出可追溯依据；
4. 由自主实验闭环持续自我改进，人工只在关键节点复核。

### 8.2 当前各模块技术成熟度（TRL 估计）

| 模块 | TRL（本报告评估） | 依据 |
| --- | --- | --- |
| 成分→形成能/凸包（uMLIP 筛选） | 7—8（窄域商用） | Matlantis 150+ 企业、DPA-4.1 商用化（[排行榜](https://matbench-discovery.materialsproject.org/)） |
| 企业配方优化平台（实验数据驱动） | 7—8 | Uncountable/Citrine/Intellegens 多家商用部署 |
| ICME+ML 合金设计（超合金等） | 6—7 | GRX-810 已许可量产；ABD-900AM 商用 |
| 性质条件生成模型 | 4—5 | MatterGen S.U.N.≈38.6%，单点实验验证 |
| 自主合成/表征闭环 | 4—5 | A-Lab 争议、NIMS 起步 |
| 服役性能端到端预测 | 3—4 | 公开证据不足 |

### 8.3 产业渗透的现状证据

- **资本**：Orbital 5000 万美元 B 轮（2026）、Entalpic 850 万欧元种子轮、Matlantis 独立运营、Kairos 等基模型初创入场——说明"AI+材料"已被视为可规模化赛道，但单轮金额仍属中早期量级（对照 AI 药物发现单轮数亿美元级）。
- **政策**：美国 MGI 2021 战略计划把"数据基础设施+AI"列为核心行动（[MGI 计划](https://www.mgi.gov/sites/mgi/files/MGI-2021-Strategic-Plan.pdf)）；欧盟 Materials 2030 宣言/倡议推动 2030 前建立先进材料数字基础设施（[宣言](https://www.iam-i.eu/wp-content/uploads/2025/07/advanced-materials-2030-manifesto.pdf)、[倡议](https://manufuture.org/the-advanced-materials-2030-initiative-is-now-up-and-running-join-us/)）；中国材料基因工程重点专项持续投入（[金属学报综述](https://www.ams.org.cn/article/2020/0412-1961/0412-1961-56-10-1313.shtml)）。
- **效果**：已披露的最强企业口径为"研发产出 +20%、DOE 工作量 −45%"（SCG）与"计算加速 3—6 个数量级"（Matlantis/CHGNet 类），尚未见"研发周期缩短 50%+"的大规模公开审计数据。McKinsey 判断 AI 能显著"弯曲研发生产率曲线"，但同时强调组织与数据瓶颈（[McKinsey 报告](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-next-innovation-revolution-powered-by-ai)）。

### 8.4 分阶段预测（判断 + 依据）

**阶段一（现在—2030）：窄垂直领域标配化（置信度：高）**
- 合金微调（超合金/钛/高熵）、聚合物与配方、催化剂/电池材料筛选中的 ML 工作流渗透率从"领先企业"扩展到"主流企业"；uMLIP+LLM 助手成为研发标配工具链。
- 依据：精度竞赛已越过"计算级可用"阈值（17 meV/atom）、平台商业化已验证付费意愿、自主实验室在电池/催化窄场景进入常态运行（[C&EN 2026](https://cen.acs.org/physical-chemistry/computational-chemistry/Self-driving-labs-changing-chemists/104/web/2026/06)）。

**阶段二（2030—2035）：跨体系通用设计模型 TRL 6—7（置信度：中高）**
- 生成式模型+uMLIP+自主实验三者耦合，在 3—5 个材料大类实现"目标性能→实验验证命中率>50%"的稳定闭环；行业级数据联盟与 FAIR 标准成熟（呼应欧盟 2030 目标与 MGI 数据基础设施行动）。
- 依据：训练数据 3 年增长两个数量级（MPtrj 158 万→COSMOS 2.43 亿）；发现 F1 三年内提升约 15—20 个百分点的既有斜率；但**验证环节（合成+表征）的通量与可靠性不会同速增长，是主要限速项**。

**阶段三（2035—2040）：理想模型在部分材料类落地（置信度：中）**
- "输入服役性能、输出可量产配方+工艺窗口"的全链条系统在数据基础最好的少数类别（如增材制造合金、聚合物配方）率先达到 TRL 8；但跨材料类别的"万能设计模型"大概率不会出现——材料研发更可能长期保持"模型提案+人类专家审定+自动化验证"的人机协同形态。
- 依据：成分-工艺-组织-性能链中工艺数据几乎全部专有；UQ 与可复现性短板需要标准与文化建设（欧、美、中路线图均指向 2030 年数据基础设施，落地滞后 3—5 年属常态；参考 CALPHAD 从 1970s 学术工具到 2000s 工业标配的 30 年周期，AI 周期会缩短但不会为零）。

### 8.5 主要瓶颈与建议（给打算入场的团队/企业）

1. **数据先于模型**：先建设带失败样本与工艺参数的内部数据资产（Raccuglia 教训），再谈模型精度；
2. **分层验证**：uMLIP 粗筛 → DFT 精筛 → 高通量实验 → 常规表征，不要跳层；
3. **引入 UQ**：任何进入决策链的预测都应带置信区间与适用域声明；
4. **可合成性前置**：在生成/搜索目标函数中显式加入可合成性惩罚（SynthNN 类）；
5. **对标基准**：新模型必须在 Matbench Discovery 等独立测试集上验证，避免"自家划分上的 SOTA"。

### 8.6 结论

- **成分配比优化的 ML 不是"是否可行"的问题，而是"在哪一层可行"的问题**：热力学量预测层已达到 DFT 置信水平（MAE≈17 meV/atom、发现 F1≈0.93），窄域工业部署已发生（GRX-810 量产、Matlantis 150+ 企业、SCG +20% 研发产出）。
- **离"理想模型"的三道鸿沟**：可合成性与表征闭环（当前生成命中率约 40%、自主判定仍被质疑）、工艺—组织数据（企业专有、几乎未流通）、不确定性与标准（UQ 实践远落后于精度竞赛）。
- **距离的量化表述**：窄垂直领域的大规模应用（>30% 相关研发项目采用 AI 工作流）预计还需 **3—5 年（约 2029—2031）**；跨材料类的通用设计闭环达到工业验证级（TRL 7+）预计还需 **5—10 年（约 2031—2036）**；完整意义的"理想模型"（全自动、可信、跨体系）是 **2035 年以后**的目标，且更可能以人机协同形态部分实现。
- **给研究与产业界的窗口判断**：2026—2028 年是"数据资产+领域模型"卡位期——谁能把自己的实验/工艺数据变成可训练资产并接入通用势与生成模型生态，谁就在下一阶段的成分设计竞争中占据复利位置。

---

## 附：主要参考来源索引

**综述/路线图**：[Machine learning for alloys (NRM 2021)](https://scholars.duke.edu/individual/pub1493174) ｜ [HEA 综述 2024](https://www.nature.com/articles/s43246-024-00487-3) ｜ [合金 ML 综述 2026](https://www.sciencedirect.com/science/article/pii/S3117722026001478/pdf) ｜ [逆向设计综述 2025](https://www.sciencedirect.com/org/science/article/pii/S1546221825001626) ｜ [MGI](https://www.mgi.gov/mgi-homepage) ｜ [Materials 2030 宣言](https://www.iam-i.eu/wp-content/uploads/2025/07/advanced-materials-2030-manifesto.pdf) ｜ [McKinsey](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-next-innovation-revolution-powered-by-ai)

**数据库/基准**：[Matbench Discovery 排行榜](https://matbench-discovery.materialsproject.org/) ｜ [Matbench Discovery 论文](https://nature.com/articles/s42256-025-01055-1) ｜ [Matbench v0.1 榜](https://hackingmaterials.lbl.gov/automatminer/datasets.html) ｜ [数据集总表](https://matbench-discovery.materialsproject.org/data/sets) ｜ [Materials Project](https://next-gen.materialsproject.org/) ｜ [MP Nature Materials 2025](https://www.nature.com/articles/s41563-025-02272-0) ｜ [OQMD](https://www.oqmd.org/) ｜ [AFLOW](https://www.aflowlib.org/) ｜ [JARVIS](https://jarvis-materials-design.github.io/dbdocs/jarvisdft/) ｜ [NOMAD](https://nomad-lab.eu/nomad-lab/faqs.html) ｜ [Alexandria](https://alexandria.icams.rub.de/) ｜ [OMat24](https://arxiv.org/html/2410.12771v1)

**关键论文**：[CGCNN](https://arxiv.org/abs/1710.10324) ｜ [ALIGNN](https://arxiv.org/abs/2106.01829) ｜ [Roost](https://www.nature.com/articles/s41467-020-19964-7) ｜ [CrabNet](https://www.nature.com/articles/s41524-021-00545-1) ｜ [ElemNet](https://www.nature.com/articles/s41598-018-35934-y) ｜ [Ward 2016](https://www.nature.com/articles/npjcompumats201628) ｜ [CHGNet](https://www.nature.com/articles/s42256-023-00716-3) ｜ [PFP](https://www.nature.com/articles/s41467-022-30687-9) ｜ [MatterSim](https://arxiv.org/abs/2405.04967) ｜ [DPA-2](https://arxiv.org/abs/2312.15492) ｜ [CDVAE](https://arxiv.org/abs/2110.06197) ｜ [MatterGen](https://www.nature.com/articles/s41586-025-08628-5) ｜ [GNoME](https://www.nature.com/articles/s41586-023-06735-9) ｜ [CrystaLLM](https://www.nature.com/articles/s41467-024-54639-7) ｜ [Raccuglia 2016](https://www.nature.com/articles/nature17439) ｜ [Tshitoyan 2019](https://www.nature.com/articles/s41586-019-1335-8) ｜ [A-Lab](https://www.nature.com/articles/s41586-023-06734-w) ｜ [GRX-810](https://www.nature.com/articles/s41586-023-05893-0) ｜ [Conduit 超合金](https://arxiv.org/abs/1803.03039) ｜ [Wen 2019](https://www.sciencedirect.com/science/article/abs/pii/S1359645419301430) ｜ [SynthNN](https://www.nature.com/articles/s41524-023-01114-4) ｜ [uMLIP 软化](https://www.nature.com/articles/s41524-024-01500-6) ｜ [GNoME 审计](https://arxiv.org/abs/2610.33101) ｜ [SDL 综述](https://pubs.acs.org/chreay/article/124/16/9633/154652/Self-Driving-Laboratories-for-Chemistry-and)

**产业/机构**：[Matlantis](https://matlantis.com/en/news/release-260917/) ｜ [Uncountable](https://www.uncountable.com/) ｜ [Citrine](https://citrine.io/) ｜ [QuesTek](https://questek.com/forged-to-win-how-a-navy-alloy-ended-up-on-a-fighting-robot/) ｜ [Aubert&Duval × Alloyed](https://www.metal-am.com/aubert-duval-and-alloyed-to-discuss-new-ni-based-superalloy-in-free-webinar/) ｜ [NASA GRX-810 许可](https://www.nasa.gov/centers-and-facilities/glenn/nasa-licenses-3d-printable-superalloy-to-benefit-us-economy/) ｜ [Orbital（Fortune）](https://fortune.com/2026/05/28/exclusive-orbital-industries-raises-50-million-series-b-funding-round-ai-to-discover-exotic-new-materials/) ｜ [Entalpic](https://entalpic.ai/) ｜ [Intellegens](https://intellegens.com/intellegens-and-ansys-to-empower-additive-manufacturing/) ｜ [Matmerize](https://www.matmerize.com/) ｜ [TRI](http://www.tri.global/materials-discovery) ｜ [NIMS](https://www.nims.go.jp/eng/press/2025/12/202512100.html) ｜ [中科院金属所材料 AI 研究部](http://imr.cas.cn/jgsz/synl/202604/t20260410_8183678.html) ｜ [MatChat](https://matchat.cn/) ｜ [北科大材料基因工程中心](https://bjmge.ustb.edu.cn/yanjiuduiwu/yanjiutuandui/cljxgczysjk/cljygczysjk/) ｜ [Bohrium](https://www.bohrium.com/intro)
