# 材料成分-性能机器学习的数据基础设施：数据库与基准评测（系统调研）

> 调研说明：本报告所有事实均附来源 URL（markdown 链接）。已按要求排除 `www.microsoft.com` 与 `news.northwestern.edu` 及其子域名。无法确认的具体数值标注"待核实"。

---

## 1. 主要计算数据库

### 1.1 Materials Project（MP）
- **机构**：美国劳伦斯伯克利国家实验室（LBNL）与 UC Berkeley（Kristin Persson 团队），由美国能源部资助。
- **数据规模**：精编数据库含 **15.4 万+** 已知与预测无机材料、**17.2 万+** 分子（[能源部介绍](https://www.energy.gov/science/articles/search-engine-materials-data-how-materials-project-advances-research)）。旧版站点口径：**144,595 无机化合物、76,240 能带结构、63,876 分子、530,243 纳米多孔材料、14,072 弹性张量、3,402 压电张量**（[legacy 统计页](https://legacy.materialsproject.org/)）。新版站点（next-gen）统计口径不同（含分子等，列出 "Materials 271,325"），具体精确值待核实（[next-gen.materialsproject.org](https://next-gen.materialsproject.org/)）。
- **主要性质**：形成能、相稳定性（凸包/energy above hull）、能带结构、带隙、弹性常数、压电、磁性、介电、离子扩散（电池电极）等数十类。
- **成分搜索/ML 支持**：支持成分与结构搜索；提供 `pymatgen`/`MPRester` REST API（新版需注册获取 API key）、OPTIMADE 接口；是绝大多数成分-性能 ML 模型的默认数据源。
- **开放程度**：开放（CC BY 授权），免费注册即可用 API。
- **优点**：规模大、质量高、标准化与文档好、生态最成熟（pymatgen/emmet/atomate）。
- **缺点**：以 GGA(+U) 计算为主，带隙被系统性低估；对无序、高熵、缺陷体系覆盖弱；成分搜索受凸包稳定相偏置。
- 来源：[Materials Project](https://materialsproject.org)、[next-gen 站点](https://next-gen.materialsproject.org/)、[文档](https://docs.materialsproject.org/)。

### 1.2 AFLOW（Automatic-FLOW）
- **机构**：杜克大学（Stefano Curtarolo 团队）。
- **数据规模**：**3,929,948 种化合物、817,429,184 条计算性质**（[aflowlib.org 首页](https://www.aflowlib.org/)）。
- **主要性质**：形成焓、能带结构、带隙、弹性、热力学（振动/热膨胀）、磁性、超导等，附带 AFLOW 原型（prototype）分类。
- **成分搜索/ML 支持**：AFLUX/AFLOW REST API；AFLOW-ML 提供面向 ML 的下载与特征（[AFLOW-ML 论文](https://arxiv.org/abs/1711.10744)）；支持成分与原型搜索。
- **开放程度**：开放，可 API 查询与批量下载。
- **优点**：规模最大之一，性质门类全，含热力学与振动数据。
- **缺点**：计算设置（VASP 默认参数）与 MP/OQMD 不完全一致，跨库对比时需注意；部分结构为原型衍生（decorated prototypes）而非 ICSD 原始结构。
- 来源：[AFLOW](https://www.aflowlib.org/)、[AFLOW API 文档](https://aflow.org/documentation/)。

### 1.3 OQMD（Open Quantum Materials Database）
- **机构**：西北大学 Chris Wolverton 课题组（注意：不使用 news.northwestern.edu 作为来源，改用官方站点与论文）。
- **数据规模**：**1,407,395 种材料的 DFT 热力学与结构性质**（[oqmd.org](https://oqmd.org/)）。
- **主要性质**：形成能、凸包稳定性、相图相关信息、结构、磁性。
- **成分搜索/ML 支持**：支持成分与结构搜索；提供 REST API（qmpy）与批量下载，可直接用于成分-性能 ML 训练。
- **开放程度**：开放，可网页查询、API 与 SQL 下载。
- **优点**：覆盖大量亚稳/不稳定相（远超 MP 的"热力学稳定"偏置），适合做稳定性/形成能回归。
- **缺点**：部分早期数据精度与收敛标准较松（[OQMD 形成能精度评估论文](https://www.researchgate.net/publication/286490327_The_Open_Quantum_Materials_Database_OQMD_assessing_the_accuracy_of_DFT_formation_energies)）；更新频率与文档弱于 MP。
- 来源：[OQMD](https://oqmd.org/)。

### 1.4 NOMAD（Novel Materials Discovery）
- **机构**：德国 Fritz-Haber-Institut（柏林）/ Max Planck，现为 FAIR-DI / NFDI-MatWerk 联盟核心（[NOMAD 官网](https://nomad-lab.eu/nomad-lab/nomad.html)）。
- **数据规模**：全球最大计算材料数据仓库，存储 **超过 1 亿条总能（total-energy）计算**（[NOMAD AI Toolkit 论文](https://www.nature.com/articles/s41524-022-00935-z)）；检索界面口径为 **1,900 万+ 条记录**（[FAIR-DI 教程](https://www.fair-di.eu/events/big-data-ai-in-materials-science/exercise-1)）。
- **主要性质**：以"原始上传 + 归一化 Archive"双轨存储各类第一性原理计算（VASP、Quantum ESPRESSO、FHI-aims、ABINIT、CP2K 等）的总能、能带、结构、力等；不做统一重算。
- **成分搜索/ML 支持**：提供 API 与 AI Toolkit（Jupyter 查询/建模），支持按材料/性质/方法过滤；是 FAIR 数据共享的标杆。
- **开放程度**：开放（可公开或 embargo 发布，带 DOI）。
- **优点**：数据来源广、FAIR 程度最高、含原始文件与归一化元数据。
- **缺点**：非单一计算协议，跨数据集一致性差；"大而杂"，直接用于成分-性能回归需要大量清洗。
- 来源：[NOMAD](https://nomad-lab.eu/nomad-lab/nomad.html)、[NOMAD AI Toolkit 论文](https://www.nature.com/articles/s41524-022-00935-z)。

### 1.5 JARVIS-DFT
- **机构**：美国国家标准与技术研究院 NIST（Kamal Choudhary 团队）。
- **数据规模**：网站口径 **80,000+ 材料、数百万条性质**（[jarvis.nist.gov](https://jarvis.nist.gov/)）；NIST 项目页早期口径为 **约 40,000 三维体材料 + 约 1,000 低维材料**（[NIST JARVIS-DFT 项目页](https://www.nist.gov/programs-projects/jarvis-dft)）。
- **主要性质**：形成能、带隙（OptB88vdW 与 TBmBJ 两种）、弹性、磁性、介电、能带等，含/不含自旋轨道耦合；另有 JARVIS-2D、分子、缺陷等子库。
- **成分搜索/ML 支持**：JARVIS-Tools Python 库、API、OPTIMADE；深度嵌入 JARVIS-Leaderboard（见 §4）。
- **开放程度**：开放（NIST 公共数据）。
- **优点**：性质门类全，提供 TBmBJ 高精度带隙，基准评测配套完善。
- **缺点**：体材料规模小于 MP/OQMD/AFLOW；TBmBJ 与 GGA 带隙并存需区分。
- 来源：[JARVIS](https://jarvis.nist.gov/)、[JARVIS-DFT 文档](https://jarvis-materials-design.github.io/dbdocs/jarvisdft/)、[NIST 项目页](https://www.nist.gov/programs-projects/jarvis-dft)。

### 1.6 Materials Cloud
- **机构**：瑞士 EPFL / MARVEL / NCCR MARVEL（Nicola Marzari 团队）。
- **数据规模**：以 AiiDA 工作流产出的精选数据库（MC3D 三维、MC2D 二维、MC1D、MC4D 及各类专题数据）为核心，规模量级百万级结构（具体当前总数待核实）。
- **主要性质**：结构、形成能、能带、拓扑、声子、输运等，以工作流可复现为特色（每条数据可追溯 provenance）。
- **成分搜索/ML 支持**：通过 AiiDA 与 **OPTIMADE** REST API 开放检索（[aiida-optimade](https://github.com/aiidateam/aiida-optimade)）；提供 AIIDA-LAB 与浏览器交互。
- **开放程度**：开放，强调 provenance 与可复现。
- **优点**：数据 provenance 最好，OPTIMADE 兼容，适合复现与跨库联邦查询。
- **缺点**：绝对规模与性质广度不如 MP/AFLOW；偏精选而非高通量全覆盖。
- 来源：[Materials Cloud](https://www.materialscloud.org/)。

### 1.7 关于 "Open Quantum Materials Database" 的说明
"OQMD" 即上文 1.3 的 Open Quantum Materials Database，无独立第二库，此处按任务列表重述避免遗漏。

---

## 2. 实验数据库与文献挖掘

### 2.1 Citrine Informatics
- **性质**：商业 SaaS 平台（非公开数据库），面向化工/材料企业，把实验与工艺数据接入 ML 建模（[citrine.io](https://citrine.io/)）。
- **数据**：以客户私有实验数据 + 平台能力为主，并开源 **GEMD（Graphical Expression of Materials Data）** 数据模型，用 Material/Process/Measurement/Ingredient 四类对象组织数据（[citrine.io](https://citrine.io/)；GEMD 文档链接待核实）。
- **开放程度**：平台商业闭源，GEMD 开源。
- **意义**：代表"实验数据 + 知识图谱 + ML 平台"的商业路线，与公开计算库互补。

### 2.2 MPDS / PAULING FILE（Materials Platform for Data Science）
- **机构**：ASM International 与 Springer（源自 Pauling File 项目）。
- **规模**：近 **200 万条数据条目**（物理性质、晶体结构、相图）（[MPDS 教程](https://tutorial.mpds.io/)、[re3data 登记](https://www.re3data.org/repository/r3d100012448)）。
- **性质**：经人工审校的无机材料实验数据（相图、结构、物理化学性质），机器可读，提供 REST API（[mpds.io](https://mpds.io/)）。
- **开放程度**：订阅制（商业），API 面向工业与科研。
- **优点**：实验数据质量高、审校严格，是成分-性能实验回归的重要来源。
- **缺点**：付费、覆盖偏经典无机体系，更新慢。

### 2.3 Springer Materials
- **机构**：Springer Nature。
- **规模**：**29 万+ 材料、3,000+ 物理/化学性质**（[SpringerNature 图书馆页](https://www.springernature.com/gp/librarians/products/databases-solutions/springermaterials)）。
- **性质**：整合 Landolt-Börnstein 等权威手册的经审校实验/理论数据，覆盖多类材料与性质（[springermaterials.com](https://materials.springer.com/)）。
- **开放程度**：订阅制。
- **优点**：权威、性质门类广；缺点：付费、机器可读/API 支持相对弱。

### 2.4 NIST（实验侧）
- **Interatomic Potentials Repository**：提供原子间势（力场）、相关文件与评估工具，支持 API（[potentials.nist.gov](https://potentials.nist.gov/)、[NIST 数据资源](https://www.nist.gov/mgi/materials-data-resources)）。
- NIST 还通过 JARVIS 系列（DFT/实验/基准）提供机器可读数据与评测（见 §1.5、§4）。

### 2.5 自动文献抽取（LLM/NLP）建库努力
- **MatSciBERT**：材料领域语言模型，基于大量材料文献语料训练，用于文本挖掘与信息抽取（[arXiv:2109.15290](https://arxiv.org/abs/2109.15290)）。
- **大规模 LLM 文献挖掘建库**：Pei 等（橡树岭 ORNL）用 LLM 从 **600 万篇论文**中自动抽取高熵合金成分与性能，构建数据库并用于超高温高熵合金筛选（[Nature Communications](https://www.nature.com/articles/s41467-022-35766-5)）。
- **ULTERA**（见 §3）本身也是文献抽取建库的典型：人工+工具从 810+ 篇论文解析 HEA 数据。
- 趋势：LLM/NLP 抽取 + 人工/程序校验（如 ULTERA 的 PyQAlloy 清洗）成为"把非结构化文献变成可训练数据"的主要路径，但抽取噪声与重复仍需治理。

---

## 3. 高熵合金 / 专用数据库

### 3.1 ULTERA（Ultrahigh TEmperature Refractory Alloys）
- **机构**：宾州州立大学 Phases Research Lab，DOE **ARPA-E ULTIMATE** 项目（[phaseslab.com/ultera](https://phaseslab.com/ultera)、[Zenodo 登记](https://zenodo.org/records/7566416)）。
- **规模**（截至 2025 年 4 月）：**12,500+ 条性质数据点、4,300 种高熵合金（HEA）、来自 810+ 篇文献**，95%+ 为实验数据，自称迄今最大的 HEA 数据库。
- **工具**：开源 Python 包 **PyQAlloy**（[pyqalloy.ultera.org](https://pyqalloy.ultera.org)）做数据清洗/聚合；团队称可剔除文献数据集中约 **5–10% 的错误数据**（重复点、成分解析错误等）。
- **开放程度**：当前**非完全公开**，通过 Zenodo 申请/合作使用（contribute.ultera.org）。
- **意义**：面向成分-性能实验回归的专用库，凸显实验 HEA 数据的稀缺与清洗难度。

### 3.2 其他合金/HEA 数据库
- **TCHEA**（Thermo-Calc High Entropy Alloy 热力学数据库，CALPHAD 框架，TCHEA9 等版本）：面向相平衡与热力学性质，非 ML 训练库但常作为特征/标签来源（[thermocalc.com](https://thermocalc.com/products/databases/high-entropy-alloys/)）。
- **公开 HEA 实验数据集**：如难熔高熵合金室温硬度/压缩数据集（82 种电弧熔炼合金）（[PMC 数据集](https://pmc.ncbi.nlm.nih.gov/articles/PMC9679436/)）。
- 总体：HEA 领域缺乏像 MP 那样的大规模公开"成分-性能"库，数据主要靠文献挖掘与 CALPHAD 补足（稀疏性问题见 §5）。

---

## 4. 机器学习基准评测

### 4.1 MatBench
- **主办**：Materials Project（[matbench.materialsproject.org](https://matbench.materialsproject.org/)）。
- **任务**：13 个监督任务，覆盖回归（MAE）与分类（ROC-AUC），如形成能、带隙、体/剪切模量、介电、声子、实验带隙、钢屈服强度、钙钛矿、玻璃、2D exfoliation 能等；部分任务仅需成分（composition-only），部分需结构。
- **指标**：MAE / ROC-AUC。
- **当前最佳（SOTA，matbench_v0.1 总榜，成分模型 coGN/coNGN 与 MODNet 占优）**：
  | 任务 | 样本数 | 最佳模型 | 数值 |
  |---|---|---|---|
  | matbench_mp_e_form | 132,752 | coGN | 0.0170 eV/atom |
  | matbench_mp_gap | 106,113 | coGN | 0.1559 eV |
  | matbench_mp_is_metal | 106,113 | CGCNN v2019 | 0.9520 (ROC-AUC) |
  | matbench_perovskites | 18,928 | coGN | 0.0269 eV/unit cell |
  | matbench_log_gvrh | 10,987 | coNGN | 0.0670 log10(GPa) |
  | matbench_log_kvrh | 10,987 | coNGN | 0.0491 log10(GPa) |
  | matbench_glass | 5,680 | MODNet v0.1.12 | 0.9603 |
  | matbench_expt_is_metal | 4,921 | AMMExpress v2020 | 0.9209 |
  | matbench_dielectric | 4,764 | MODNet v0.1.12 | 0.2711 |
  | matbench_expt_gap | 4,604 | MODNet v0.1.12 | 0.3327 eV |
  | matbench_phonons | 1,265 | MegNet | 28.7606 cm⁻¹ |
  | matbench_jdft2d | 636 | MODNet v0.1.12 | 33.1918 meV/atom |
  | matbench_steels | 312 | MODNet v0.1.12 | 87.7627 MPa |
  来源：[MatBench 总榜](https://matbench.materialsproject.org/)（注：站点自述分类 ROC-AUC 为 0.5 阈值下的平衡精度口径，非严格 ROC-AUC）。
- **相关**：**Matbench Discovery**（[站点](https://matbench-discovery.materialsproject.org/)、[arXiv:2308.14920](https://arxiv.org/abs/2308.14920)、[Nature Machine Intelligence 2025](https://www.nature.com/articles/s42256-025-01055-1)）评估 ML 能量模型作为高通量"晶体稳定性预筛"的能力，引入坐标无关的 **Wrenformer** 基线。

### 4.2 JARVIS-Leaderboard
- **主办**：NIST（Kamal Choudhary 等）。
- **规模**：**1,281 个提交、274 个基准、152 种方法、800 万+ 数据点**（[arXiv:2306.11688](https://arxiv.org/abs/2306.11688)、[Nature npj Comput Mater 2024](https://www.nature.com/articles/s41524-024-01259-w)）。
- **五大类**：AI（原子结构/图像/谱/文本输入）、电子结构 ES（DFT/QMC/多体微扰，比较不同软件/赝势/泛函并与实验对照）、力场 FF、量子计算 QC、实验 EXP（跨实验室比对）。
- **指标**：以 MAE 为主，另引入 **MAD/MAE 归一化**指标比较跨性质预测力（[alphaXiv 解读](https://www.alphaxiv.org/abs/2306.11688)）。
- **平台**：[pages.nist.gov/jarvis_leaderboard](https://pages.nist.gov/jarvis_leaderboard)。

### 4.3 Open Catalyst Project（OC20 / OC22）
- **主办**：Meta AI（FAIR）+ 卡内基梅隆大学。
- **数据规模**：OC20 + OC22 合计 **130 万个分子弛豫（relaxation）、来自 2.6 亿+ 次 DFT 计算**（[opencatalystproject.org](https://opencatalystproject.org/)、[数据集页](https://fair-chem.github.io/core/datasets/oc20.html)）。
- **任务类型**：
  - **S2EF**（结构→能量与力）：回归，指标为能量 MAE（meV/原子）与力 MAE（meV/Å）；
  - **IS2RE**（初始结构→弛豫能量）：能量 MAE（eV）；
  - **IS2RS**（初始结构→弛豫结构）：AFbT（阈值内平均距离）。
- **OC22** 聚焦氧化物电催化，含 S2EF-Total 与 OC22 特有评估（[OC22 论文](https://arxiv.org/abs/2206.08917)）。
- **SOTA**：**EquiformerV2**（[arXiv:2306.12059](https://arxiv.org/abs/2306.12059)、[ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/file/ab12e8f3443c1a789f595b18d8c597b4-Paper-Conference.pdf)）为当前主流最佳之一：相对上一代 eSCN 在 OC20 上**力 MAE 提升最高 9%、能量 MAE 提升最高 4%**；在吸附能计算上可减少约 **2 倍 DFT 计算量**；仅用 OC22 训练的 EquiformerV2 即**超过用 OC20+OC22 训练的 GemNet-OC**。参考量级：eSCN 在 S2EF 测试集力 MAE 约 **15.6 meV/Å**（[arXiv HTML](https://arxiv.org/html/2306.12059v3)）。OC20/OC22 具体 leaderboard 能量/力 MAE 精确小数以 [eval.ai](https://eval.ai/web/challenges/challenge-page/712/overview) 为准（待核实）。
- **代码/模型**：开源 FAIR-Chem / fairchem 与 equiformer_v2。

### 4.4 MatSciML benchmark
- **主办**：Intel Labs 等（[arXiv:2309.05934](https://arxiv.org/abs/2309.05934)、[代码](https://github.com/IntelLabs/matsciml)）。
- **定位**：面向固态材料（周期晶体）的**多任务、多数据集**统一基准，缓解"数据集碎片化导致模型不可比"问题。
- **数据来源**：Open Catalyst、OQMD、NOMAD、Carolina Materials Database、Materials Project。
- **任务**：能量、原子力（回归）、带隙（回归）、空间群晶体对称性分类；支持单任务/多任务/多数据集联合学习，评测 GNN 与等变点云网络。

### 4.5 成分-性能预测常用基准小结
- 纯**成分→性能**（composition-only）：MatBench 的 composition 任务（形成能、带隙、体模量等，coGN/coNGN/CrabNet/MODNet 为常用基线）。
- **结构→能量/力**：OC20/OC22、MatSciML、Matbench Discovery。
- **实验成分→性能**：MatBench 的 steels/expt_gap/glass 等小样本任务（如 312 条钢数据），体现实验稀疏性。

---

## 5. 数据规模、质量、不平衡、稀疏性与 FAIR

### 5.1 规模与不平衡/稀疏性
- **计算库规模大但偏置明显**：MP（~15 万材料）、OQMD（~140 万）、AFLOW（~393 万）集中在热力学稳定或易收敛的简单/有序化合物；**无序固溶体、高熵合金、缺陷、界面、亚稳相**覆盖不足。OQMD 相对保留了更多亚稳相，但其精度一致性弱于 MP。
- **实验库稀疏**：MatBench 的钢屈服强度仅 **312 条**、玻璃形成 **5,680 条**、实验带隙 **4,604 条**——与计算形成能的 13 万+ 条相差 2–3 个数量级；HEA 全领域公开可训数据仅数千到万余条（ULTERA 12,500+ 点）。
- **类别不平衡**：金属/非金属分类、稳定/亚稳分类、成分空间分布（常见元素过采样、稀土/贵金属欠采样）导致模型长尾失效。
- **标签噪声**：文献抽取数据含重复、成分解析错误（ULTERA 报告剔除 5–10% 错误数据）。

### 5.2 FAIR 原则与数据共享现状
- **计算数据 FAIR 化较好**：NOMAD 是 FAIR 数据共享标杆（原始文件 + 归一化 Archive + DOI + API），并推动 FAIR-DI / NFDI-MatWerk（[NOMAD](https://nomad-lab.eu/nomad-lab/nomad.html)）。
- **互操作标准**：**OPTIMADE** 联盟统一跨库检索 API，Materials Cloud、Materials Project、NOMAD、JARVIS、AFLOW、OQMD 等多库已接入（[optimade.org](https://www.optimade.org/)、[NIST 应用论文](https://www.nist.gov/publications/developments-and-applications-optimade-api-materials-discovery-design-and-data-exchange)）。
- **实验数据 FAIR 化滞后**：实验数据分散在论文/手册（Springer Materials、MPDS 订阅制），缺少统一开放注册，自动抽取（§2.5）与领域 LLM（MatSciBERT）是补课方向。

---

## 6. 数据库之间差异、误差与一致性；DFT 设置迁移性

### 6.1 主要差异来源
- **交换关联泛函**：MP/AFLOW/OQMD 多为 PBE-GGA（部分 +U）；JARVIS 用 OptB88vdW 并额外给 TBmBJ 带隙。PBE 带隙被系统性低估，跨库带隙可比性差。
- **赝势与平面波/截断**：VASP PAW（MP/AFLOW/OQMD）vs 其他代码（NOMAD 汇集多代码）造成形成能、总能差异。
- **+U 与磁性初始化**：过渡金属/稀土氧化物的 U 参数、磁序初始化不同 → 形成能与稳定性排序不一致。
- **结构来源与收敛标准**：ICSD 原始结构 vs AFLOW 原型衍生结构；k 点密度、离子弛豫/力收敛阈值不同。
- **量级参考**：文献报道跨库形成能差异可达 **数十~100 meV/atom**，带隙差异可达 **~0.5–1 eV** 量级（精确数值待核实；方向性结论可靠）。

### 6.2 对 ML 迁移性的影响
- **单一库训练 → 跨库/跨实验泛化差**：在 MP 上训练的模型直接用于 OQMD/JARVIS 标签会引入系统性偏差。
- **混合多库数据**需先做协议对齐/归一化（如统一泛函、U 校正、能量参考态），否则模型学到的是"协议差异"而非"材料规律"。
- **实验 vs 计算标签**：实验带隙（MatBench expt_gap MAE ~0.33 eV）与计算带隙（mp_gap MAE ~0.16 eV）精度差距，反映计算-实验系统误差无法被成分模型完全吸收。
- **建议**：成分-性能 ML 应显式记录/标注数据来源与计算设置（NOMAD/OPTIMADE provenance），或用多源数据增强 + 域适应缓解迁移性问题。

---

## 关键结论

1. **计算数据基础设施已成熟且规模巨大**：Materials Project（~15 万材料，成分-性能 ML 的默认源）、OQMD（~140 万，稳定性/亚稳相）、AFLOW（~393 万化合物、8.17 亿性质，规模最大）构成"三巨头"，NOMAD（1 亿+ 计算，FAIR 标杆）与 JARVIS-DFT（~4–8 万材料，含高精度 TBmBJ 带隙）与 Materials Cloud（provenance 最强）提供互补能力；OPTIMADE 正把各库打通为可联邦查询的网络。

2. **成分搜索/ML 支持普遍**：上述库均提供 API/OPTIMADE，MP 的 pymatgen/MPRester 生态最成熟；JARVIS 自带基准评测闭环。

3. **实验数据是短板**：公开成分-性能实验数据稀疏（钢 312 条、HEA 万余条），多锁在订阅库（Springer Materials 29 万材料、MPDS/Pauling File 200 万条目）或商业平台（Citrine）；LLM/NLP 文献挖掘（MatSciBERT、ORNL 六百万篇论文挖掘、ULTERA 810+ 文献）是当前主流补数据手段，但需清洗（ULTERA 剔除 5–10% 错误）。

4. **基准评测已体系化**：MatBench（13 任务，成分模型 coGN/coNGN/MODNet 领先，形成能 MAE 低至 0.017 eV/atom）适合成分-性能；OC20/OC22（130 万弛豫、2.6 亿 DFT，EquiformerV2 为 SOTA）与 MatSciML（多任务多数据集）覆盖结构→能量/力；JARVIS-Leaderboard（274 基准、800 万数据点）横向覆盖 AI/ES/FF/QC/EXP；Matbench Discovery 专注"稳定性预筛"这一真实发现流程。

5. **质量与一致性是核心瓶颈**：跨库 DFT 设置（泛函/赝势/U/收敛）差异带来形成能数十~100 meV/atom、带隙 ~0.5–1 eV 量级的系统偏差，导致单库训练的模型跨库迁移性差；数据不平衡（稳定相/常见元素过采样）与实验稀疏性进一步限制成分-性能模型的泛化。未来方向是"协议对齐 + provenance + 多源域适应"。

> 未决事项（待核实）：Materials Project next-gen 精确统计口径与 2024 具体版本数；NOMAD 条目数的精确口径（"1900 万条记录" vs "1 亿+ 计算"）；OC20/OC22 在 eval.ai 上的精确 SOTA 能量/力 MAE 小数；Materials Cloud 当前结构总数。以上均已标注来源，可在链接处二次核对。
