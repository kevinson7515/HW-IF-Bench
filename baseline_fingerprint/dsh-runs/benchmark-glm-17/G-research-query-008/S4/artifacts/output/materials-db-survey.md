# 材料信息学事实核查调研（2024–2025）

## 1 主流材料数据库现状
- **Materials Project**：基准训练集快照 v2022.10.28 含 154,719 个晶体（arXiv:2308.14920v3）；2024–2025 报道已扩至 **>20 万个材料 + 57.7 万个分子**，数据类型为高通量 DFT（形成能、带隙、弹性、介电等）及弛豫轨迹。来源：[next-gen.materialsproject.org](https://next-gen.materialsproject.org/)、[docs 数据库版本](https://docs.materialsproject.org/changes/database-versions)、[Lab Manager 报道](https://www.labmanager.com/materials-project-database-expansion-accelerates-ai-driven-materials-discovery-34872)
- **OQMD**：DFT 热力学/结构数据库，**1,407,395 个材料**（Northwestern Wolverton 组）。[oqmd.org](https://www.oqmd.org/)
- **AFLOW**：**3,929,948 个化合物、817,429,184 条计算性质**。[aflowlib.org](https://www.aflowlib.org/)
- **JARVIS-DFT**：**80,000+ 材料**（NIST）。[jarvis.nist.gov](https://jarvis.nist.gov/)（2025 综述称 JARVIS 全系可达约 600 万材料/千万条性质，[arXiv:2503.04133](https://arxiv.org/html/2503.04133v1)）
- **NOMAD**：**上传条目 19,425,275、涉及材料 4,346,100、文件 129.3 TB**。[nomad-lab.eu](https://nomad-lab.eu/nomad-lab/)
- **Citrine/Citrination**：平台型；官网称 **380 个项目、550 个 AI 模型上线**；Citrination 公共数据集仍可访问。[citrine.io](https://citrine.io/)、[citrination.com](https://citrination.com/)；数据总量未核实
- **MatWeb**：**>200,000 份材料数据表**（实验数据）。[matweb.com](https://www.matweb.com/)
- **Polymer Genome**：预测平台（非数据库），原始论文覆盖 7 种聚合物性质。[polymergenome.org](https://www.polymergenome.org/)；具体精度数值未核实
- **GNoME**（“约 220 万稳定晶体”出处）：Merchant et al., *Scaling deep learning for materials discovery*, Nature (2023)：**220 万个相对 MP 稳定的晶体结构，其中 381,000 个位于凸包上**。[nature.com/articles/s41586-023-06735-9](https://www.nature.com/articles/s41586-023-06735-9)；官方博客称其中 38 万稳定、外部实验室已独立合成 736 个（[DeepMind 博客](https://deepmind.google/blog/millions-of-new-materials-discovered-with-deep-learning/)）
- **MD/结构数据集**：MPtrj **1,580,395 构型 / 145,923 材料**；OMat24 **100,824,585 构型 / 3,227,606 材料**；子采样 Alexandria 10,447,765 构型（Matbench Discovery 数据页）；Alexandria **>500 万 DFT 计算**（[Schmidt 2024](https://www.sciencedirect.com/science/article/pii/S2542529324002360)），扩展版 **580 万结构、凸包上 17.5 万化合物**（[arXiv:2512.09169](https://arxiv.org/html/2512.09169v1)）；WBM 测试集 257,487 结构。

## 2 Matbench 与 Matbench Discovery
- **Matbench v0.1**：13 个任务、样本量 312–132,752（[arXiv:2005.00707](https://arxiv.org/abs/2005.00707)）。“13/16”中的 16 任务说法未核实。官方每任务最优（[排行榜](https://matbench.materialsproject.org/)）：steels **87.76 MPa**(MODNet)、expt_gap **0.3327 eV**(MODNet)、dielectric 0.2711(MODNet)、glass ROCAUC 0.9603(MODNet)、log_kvrh **0.0491 log10(GPa)**(coNGN)、log_gvrh 0.0670(coNGN)、perovskites 0.0269 eV/cell(coGN)、mp_gap **0.1559 eV**(coGN)、mp_e_form **0.0170 eV/atom**(coGN)、phonons 28.76 cm⁻¹(MegNet)、mp_is_metal 0.9520(CGCNN)。
- **Matbench Discovery**（[官方排行榜](https://matbench-discovery.materialsproject.org/)，论文 [arXiv:2308.14920v3](https://arxiv.org/html/2308.14920v3)，2024-12）：WBM 测试集去重后 **215,488 唯一原型、32,942 个稳定**；指标含 F1/DAF/MAE/R²/κSRME/RMSD/CMDS/CDS 与综合 CPS。论文结论：UIP 排名 EquiformerV2+DeNS > Orb > SevenNet > MACE > CHGNet > M3GNet > ALIGNN > MEGNet > CGCNN…，**UIP F1 = 0.57–0.82，DAF 最高 ~6x**。本次抓取的现行排行榜第 1 名 **DPA-4.1-Max-OAM-PFT**（CPS 0.913、F1 0.935、MAE 0.017 eV/atom、R² 0.872、κSRME 0.081、RMSD 0.058 Å）；2025 年代表 eSEN-30M-OAM（F1 0.925）。**MACE-MPA-0**（2024-12）：F1 **0.852**、κSRME 0.412、RMSD 0.0731、CPS 0.795；MACE-MP-0 官方 API 示例 F1 0.665、DAF 3.457。排行榜未见名为 "pznxt" 的模型（未核实）。

## 3 成分→性能模型典型精度
- **形成能（仅成分输入）**，OQMD 256,620 子集（[Roost 论文表1，arXiv:1910.00617](https://arxiv.org/html/1910.00617v4)）：RF+Magpie **67 meV/atom**；ElemNet **55 meV/atom**（与 [Jha 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6279928/) 0.055 eV/atom 一致）；Roost 单模型 **29.7**、集成 **24.1 meV/atom**。
- **结构输入**（Matbench mp_e_form，132,752 样本）：ALIGNN 21.5、CGCNN 33.7、coGN 17.0、CrabNet 86.2、Magpie-RF 116.5 meV/atom。
- **通用势（MPtrj 测试）**（[CHGNet 论文，arXiv:2302.14231](https://arxiv.org/html/2302.14231v2)）：CHGNet 能量 MAE **30 meV/atom**、力 77 meV/Å、应力 0.348 GPa、磁矩 0.032 μB；M3GNet（Chen & Ong 2022，[PubMed 38177366](https://pubmed.ncbi.nlm.nih.gov/38177366/)）具体 MAE 未核实。
- **带隙**：实验带隙 0.3327 eV（MODNet）、DFT 带隙 0.1559 eV（coGN）（Matbench）。
- **弹性模量**：log10(KVRH) 0.0491、log10(GVRH) 0.0670（coNGN，Matbench）。
- **高熵合金硬度**：RF **R²=0.91、RMSE=0.064**（[Guo 2023](https://www.sciencedirect.com/science/article/abs/pii/S0263436823000161)）。
- **钢**：Matbench steels（312 样本）最优 MAE **87.76 MPa**（MODNet）；成分-工艺-屈服强度 ANN 的 R²（Park 2024, [MDPI 14(10):4224](https://www.mdpi.com/2076-3417/14/10/4224)）具体值未核实（原文访问受限）。

## 4 产业化与自主实验室
- **Matlantis/PFN**：PFP 覆盖 **96 个元素**、较 DFT **约 7000 万倍提速**（3000 原子体系）、最大 44,000 原子；PFP v9 训练数据 **>6300 万结构**；原始论文 45 元素（[Nat. Commun. 2022](https://www.nature.com/articles/s41467-022-30687-9)）。[matlantis.com](https://matlantis.com/en/product/about-pfp/)
- **Citrine**：380 项目/550 模型（官网）；Panasonic 案例见 [citrine.io](https://citrine.io/)。
- **Atinary**：SDLabs 2.0，与 Takeda、MIT 合作（[官网](https://atinary.com/technology/self-driving-labs/)、[AWS 博客](https://aws.amazon.com/blogs/physical-ai/atinarys-ai-self-driving-labs-on-aws-accelerate-rd-for-takeda-and-mit/)）。
- **Alloyed**：ABD 合金设计；ABD-AM 增材制造高温合金（[Tang 2021](https://www.sciencedirect.com/science/article/pii/S1359645420307175)）。
- **Kebotix**：公司在线，曾获 NSF 1500 万美元合作（[kebotix.com](https://www.kebotix.com/)）。
- **A-Lab**（nature.com 原文 [s41586-023-06734-w](https://www.nature.com/articles/s41586-023-06734-w)）：原文（2023-12）称 17 天内从 58 个目标合成 **41 个新化合物**（[PubMed 38030721](https://pubmed.ncbi.nlm.nih.gov/38030721/)）；**2026-01-19 作者更正**改为 **36/57（成功率 63%）**——引用时务必用更正后数字。
- **多伦多 Acceleration Consortium**：**30+ 自驱动实验室**（[acceleration.utoronto.ca](https://acceleration.utoronto.ca/)）。
- **Emerald Cloud Lab**：远程自动化生命科学实验室（Austin）（[官网](https://www.emeraldcloudlab.com/)）。
- **RoboChem**（阿姆斯特丹 UvA）：Science 2024（[10.1126/science.adj1817](https://www.science.org/doi/10.1126/science.adj1817)），9 次实验内产率 **>90%**。
- **GNoME/MatterGen 实验验证**：GNoME——外部实验室独立合成 736 个结构（DeepMind 博客）；MatterGen——注意正确 arXiv 号为 **2312.03687**（用户所给 2312.03617 有误）；生成结构新颖且稳定概率比此前模型高 **2 倍以上**、距局部能量极小 **近 15 倍**（[arXiv:2312.03687](https://arxiv.org/abs/2312.03687)）；Nature 2025 发表并实验合成一个生成样品（[nature.com/articles/s41586-025-08628-5](https://www.nature.com/articles/s41586-025-08628-5)）。MatterSim 数值未核实。

**未核实项汇总**：Polymer Genome 具体精度、钢铁 ANN R²、"pznxt" 模型、Matbench "16 任务"、Citrination 公共数据总量。
