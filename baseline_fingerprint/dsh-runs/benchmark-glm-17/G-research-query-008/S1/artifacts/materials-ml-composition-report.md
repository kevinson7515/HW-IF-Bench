# 机器学习/深度学习优化材料元素组合配比：研究进展与产业化前景评估报告

> **报告范围**：聚焦"成分（元素种类与配比）→ 性能"的机器学习建模，以及"目标性能 → 成分"的逆向设计/优化，涵盖金属合金（含高熵合金）、氧化物/钙钛矿、聚合物、玻璃、电池材料、催化剂等体系。
> **信息时效**：基于截至 2026 年可公开检索的文献、数据库与产业资料；所有关键事实均附可点击来源链接。
> **方法说明**：本报告由多路并行调研汇总而成，关键论文与数字均经过检索核实；个别未能完全核实之处已明确标注"未核实"。

---

## 摘要

机器学习/深度学习用于**优化材料元素组合与配比**，已从 2014 年前后"扫描百万候选成分"的概念验证，发展为 2026 年覆盖"代理模型—贝叶斯优化—生成式逆设计—自主实验闭环"的完整技术栈。本报告的核心判断：

1. **技术能力**：成分级代理模型的形成能预测误差（MAE 0.024–0.117 eV/atom）已低于 DFT 方法本身相对实验的系统误差（约 0.1 eV/atom）；通用原子间势基础模型在稳定相发现基准（Matbench Discovery）上 F1 达 0.93+、发现加速因子 ≈6.1（理论上限约 6.5）；实验性质任务（高熵合金相分类 86–94%、硬度 R² 0.93–0.97、超导分类 ≈92%）在内插域可用。
2. **应用现状**：主动学习闭环在工业案例中证明可削减 2–9 倍实验量；生成式模型（MatterGen 等）已实现按目标性质生成新材料并完成实验验证；自主实验室（A-Lab 等）速度突破但可信度建设仍在进行（Nature 2026 更正事件）；材料信息学市场约 2.5 亿美元（2026）并按 ~9% 年复合增速扩张。
3. **核心挑战**：分布外外推（留元素场景 MAE 恶化 3–14 倍）、可合成性建模、实验/工艺数据生态薄弱、闭环验证成本——限制因素已从算法精度转移到数据与验证基础设施。
4. **产业化距离**：专用成分优化系统已进入工业日常（2–5 年内普及）；通用材料基础模型处于商品化拐点（约 5–10 年）；"理想模型"（通用、全变量、校准不确定性、可合成性感知、全闭环）预计还需 **10–15 年**，且等待的是数据生态与验证基础设施，而非算法突破。

---

## 目录

1. [研究背景与问题定义](#1-研究背景与问题定义)
2. [技术路线全景](#2-技术路线全景)
3. [活跃研究课题组、研究方向与代表论文](#3-活跃研究课题组研究方向与代表论文)
4. [常用数据库与基准测试分析](#4-常用数据库与基准测试分析)
5. [模型准确度评估](#5-模型准确度评估)
6. [挑战与可行性分析](#6-挑战与可行性分析)
7. [产业化距离评估](#7-产业化距离评估距离理想模型的大规模应用还有多远)
8. [结论](#8-结论)
9. [主要参考文献与数据来源](#9-主要参考文献与数据来源)

---

## 1. 研究背景与问题定义

### 1.1 问题的本质：在近乎无限的成分空间中搜索最优配比

材料成分设计的核心问题是：**给定一组候选元素，确定其种类与配比（原子分数），使目标性能（强度、硬度、热膨胀、导电/导热、磁、电化学、催化活性等）达到最优，同时满足稳定性、可合成性与成本约束。**

这一问题的组合复杂度是天文数字级别的。Matbench Discovery 基准论文给出了一组常被引用的量级估计：迄今实验上研究过的无机材料组合约 10⁵ 量级，DFT 等模拟覆盖约 10⁷ 量级，而仅由电负性与电荷平衡规则允许的四元无机组合就有约 10¹⁰ 量级，五元以上体系更是远超于此（[Riebesell et al., arXiv:2308.14920](https://arxiv.org/abs/2308.14920)）。高熵合金等"多元主元素"材料进一步把问题推向连续、高维的成分空间：例如 Rao 等人在 Science 上明确指出，热力学合金设计规则在如此高维的成分空间中经常失效，发现有价值的高熵合金"过于依赖偶然"（[Rao et al., Science 378, 78 (2022)](https://www.science.org/doi/10.1126/science.abo4940)）。

### 1.2 传统范式与机器学习范式的对比

| 维度 | 传统"试错法"+经验规则 | CALPHAD/热力学计算 | 机器学习/深度学习 |
|---|---|---|---|
| 成分空间探索 | 局部、串行、依赖直觉 | 依赖已知热力学数据库外推 | 数据驱动全局搜索，可处理高维空间 |
| 单次评估成本 | 高（合成+表征，单个新材料表征可达数万美元，[Citrine 平台论文, arXiv:2607.25039](https://arxiv.org/abs/2607.25039)） | 中（热力学计算） | 极低（毫秒级代理预测） |
| 适用范围 | 稀固溶体、经验丰富体系 | 相平衡、已知体系 | 可外推但可靠性依赖数据覆盖 |
| 失效场景 | 高熵、多主元素、非平衡体系 | 缺乏评估的多元体系、动力学效应 | 分布外外推、数据偏差、负样本缺失 |

国家层面的布局印证了范式转移的判断：美国 2011 年启动"材料基因组计划"（Materials Genome Initiative, MGI），建设了 45 个材料基因组创新平台（每个政府投资 0.7–1.2 亿美元）；RTI International 的经济性分析估计 MGI 类基础设施可将新材料研发风险降低 1/2 以上、从发现到工程化应用的时间缩短 1/3 以上、研发成本降低 1/3 以上（转引自[宿彦京等, 金属学报 56, 1313 (2020)](https://www.ams.org.cn/article/2020/0412-1961/0412-1961-56-10-1313.shtml)）。中国 2015 年启动"材料基因工程关键技术与支撑平台"重点专项，共设立 45 个项目，科技部、地方政府与企业累计投入超过 30 亿元人民币，参与单位超过 400 家（同上来源）。

### 1.3 机器学习介入成分优化的两种基本模式

1. **正向模式（代理模型 + 全局搜索）**：训练"成分（+工艺/结构特征）→ 性能"的代理模型，在其上执行贝叶斯优化（Bayesian optimization, BO）、主动学习（active learning）、遗传算法/NSGA-II 多目标优化等搜索策略，用少量实验/计算迭代逼近最优配比。代表案例：高熵 Invar 合金的闭环主动学习发现（[Rao et al., Science 2022](https://www.science.org/doi/10.1126/science.abo4940)）。
2. **逆向模式（生成式设计）**：直接以目标性能为条件生成候选成分或晶体结构，如条件扩散/变分自编码器类模型 CDVAE、DiffCSP、MatterGen 等（详见第 2.3 节）。

两条路线在 2022–2026 年间加速融合，形成"生成/筛选 → 高保真校验 → 主动实验闭环"的完整发现流水线。

---

## 2. 技术路线全景

### 2.1 输入表示：成分如何被"编码"

成分优化问题的特殊性在于输入天然是**元素集合与配比**，因此"仅成分输入"（composition-only）的模型族在本领域地位突出：

- **元素属性统计特征（Magpie 特征）**：对 87 种元素属性（原子半径、电负性、熔点、价电子数等）在目标成分上取均值/方差/众数等统计量。Ward 等人以此构建了第一个通用性质预测框架（[Ward et al., npj Comput. Mater. 2, 16028 (2016)](https://www.nature.com/articles/npjcompumats201628)），至今仍是小数据集上最稳健的基线之一。Meredig 等人更早证明了该路线的威力：用随机森林扫描约 160 万个候选成分，预测出约 4500 个新的稳定三元化合物（[Meredig et al., Phys. Rev. B 89, 094104 (2014)](https://ui.adsabs.harvard.edu/abs/2014PhRvB..89i4104M/abstract)，被引 950+）——这是"无约束成分空间机器学习筛选"的开山之作。
- **元素嵌入（elemental embeddings）**：ElemNet 等深度网络直接以元素配比为输入，端到端学习元素表示，OQMD 形成能 MAE 0.055 eV/atom（[Jha et al., Sci. Rep. 8, 17593 (2018)](https://www.nature.com/articles/s41598-018-35934-y)，被引 750+）。
- **深度集合（Deep Sets）/图同构网络**：Roost 将成分表示为元素"图"上的消息传递，在不含晶体结构信息的情况下预测性质，形成能预测精度接近结构模型（[Goodall & Lee, Nat. Commun. 11, 6280 (2020)](https://www.nature.com/articles/s41467-020-19964-7)）。
- **注意力机制**：CrabNet（Compositionally Restricted Attention-Based Network）把注意力机制约束在成分输入上，在多种性质上取得一致的高精度（[Wang et al., npj Comput. Mater. 7 (2021)](https://www.nature.com/articles/s41524-021-00545-1)，被引 367+）。
- **晶体图网络**（需要结构信息，多用于 DFT 数据）：CGCNN（[Xie & Grossman, Phys. Rev. Lett. 120, 145301 (2018)](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.120.145301)）、MEGNet（[Chen et al., Chem. Mater. 31, 3564 (2019), arXiv:1812.05055](https://arxiv.org/abs/1812.05055)，被引 2150+）、ALIGNN（[Choudhary & DeCost, npj Comput. Mater. 7, 185 (2021)](https://www.nature.com/articles/s41524-021-00650-1)）。
- **通用机器学习原子间势（Universal Interatomic Potentials, UIP/基础模型）**：M3GNet、CHGNet、MACE-MP、EquiformerV2、MatterSim 等在 Materials Project 松弛轨迹（MPtrj）等大数据上预训练，可对任意成分"从非弛豫结构直接预测弛豫能量与稳定性"，是 2022 年以来精度提升最快的路线，也是"材料基础模型"的雏形（详见第 5 节）。

### 2.2 代理模型谱系：哪类模型在什么数据规模上占优

- **树模型（随机森林、GBDT/XGBoost/LightGBM）**：数百~数千条实验数据（如高熵合金硬度、相形成）上的事实标准；Matbench 系统评测显示其在小数据任务上经常名列前茅。
- **高斯过程回归（GPR）**：为贝叶斯优化提供解析不确定性，是小批量主动学习的经典选择。
- **GNN/深度网络**：10⁴~10⁶ 条 DFT 数据上占优，能利用力与应力标签训练原子间势。
- **成分专用网络（Roost/CrabNet/ElemNet 等）**：不依赖结构，天然适配"成分配比优化"的搜索场景，速度快、可枚举全空间。

### 2.3 搜索与优化策略

- **贝叶斯优化/主动学习**：Citrine 的 FUELS 序贯学习框架（Ling 等 2017 年提出）是工业界广泛使用的实现（见 [Citrine 平台论文](https://arxiv.org/abs/2607.25039)及其引文）；公开发表的工业案例显示其相对随机搜索可减少 **2–9 倍**实验量（[Citrine 平台论文, arXiv:2607.25039 (2026)](https://arxiv.org/abs/2607.25039)）。综述见 [Tian et al., "Materials design with target-oriented Bayesian optimization", npj Comput. Mater. 11, 209 (2025)](https://www.nature.com/articles/s41524-025-01704-4) 与 [Arróyave et al. (2022)](https://www.osti.gov/pages/biblio/2202745)。
- **多目标优化**：NSGA-II 遗传算法、约束贝叶斯优化（处理强度–延性、强度–导电率等 Pareto 前沿，如高强高导铜合金的 MLDS 设计系统，见[宿彦京等 2020](https://www.ams.org.cn/article/2020/0412-1961/0412-1961-56-10-1313.shtml)）。
- **混合变量优化**：元素"选与不选"（类别变量）与连续配比的联合优化，代表性方法为混合变量高斯过程 + BO（[Zhang, Apley & Chen, J. Mech. Des. 142 (2020)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7080833/)，被引 440+）。
- **生成式逆设计**：CDVAE（[Xie et al., NeurIPS 2022, arXiv:2110.06197](https://arxiv.org/abs/2110.06197)，被引 700+）、DiffCSP/DiffCSP++（[Jiao et al., NeurIPS 2023, arXiv:2309.04475](https://arxiv.org/abs/2309.04475)，被引 340+）生成晶体结构；MatterGen（[Zeni et al., Nature 639, 624 (2025)](https://www.nature.com/articles/s41586-025-08628-5)，被引 1250+）在 60.8 万稳定结构上训练，微调后可按目标化学计量、对称性与磁/电/力学性质生成**全新稳定材料**（78% 生成结构距 MP 凸包 ≤0.1 eV/atom），并与实验方合作合成了新化合物 TaCr₂O₆（实测体模量 169 GPa，目标 200 GPa，偏差 <20%）。**纯成分空间（仅元素配比）的生成模型**同样成熟：MatGAN 用 GAN 直接生成成分向量（200 万样本新颖率 92.5%、化学有效 84.5%，[Dan et al., npj Comput. Mater. 6, 84 (2020)](https://www.nature.com/articles/s41524-020-00352-0)）；微调 LLaMA-2 70B 把成分当文本生成，约 90% 样本满足电荷/电负性约束、亚稳比例约为 CDVAE 的 2 倍（[Gruver et al., ICLR 2024, arXiv:2402.04379](https://arxiv.org/abs/2402.04379)）；Crystal-GFN 以 GFlowNet 按"空间群→成分→晶格"顺序采样，天然适配约束与多样性（[Nguyen et al., NeurIPS 2023, arXiv:2310.04925](https://arxiv.org/abs/2310.04925)）。但 Park 等人的批判性综述指出：生成式逆设计尚未真正实现"给定性质→材料"的闭环，实验验证率与严格基准仍不足（[Park et al., Matter (2024)](https://www.cell.com/matter/fulltext/S2590-2385(24)00242-X)）。
- **闭环自主实验（self-driving lab）**：A-Lab（Nature 2023）17 天自动合成 41/58 → 修正后 36/57 个目标化合物；利物浦"移动机器人化学家"（Nature 2020）；此类系统的可信度争议也是本领域重要一课（详见第 6、7 节）。

### 2.4 与物理/热力学知识的融合

纯数据模型在成分外推上不可靠（第 6 节详述），因此主流做法是"物理 + 数据"混合：

- **物理引导特征**：热力学参量（混合熵、混合焓）、电子结构描述符（d 电子浓度、价电子浓度 VEC）与 ML 特征并用；高熵 Invar 合金设计中即采用了物理性质引导的主动学习（[Rao et al., Science 2022](https://www.science.org/doi/10.1126/science.abo4940)）。
- **CALPHAD + ML 混合工作流**：以 CALPHAD 计算相分数/相稳定度作为特征或约束，再由 ML 代理优化性能；这是工业合金设计（QuesTek 等公司 ICME 体系）的典型路线。
- **物理增强模型**：物理约束的损失函数、等变神经网络（MACE/Equiformer 系列）、以 DFT 势能面为监督的原子间势，本质上是把物理先验"烧入"模型权重。
- **多保真度与级联验证**：ML 粗筛 → DFT 精算 → 主动实验，Matbench Discovery 评测显示该策略可将"发现加速因子"提升至接近理论上限 6.5 倍（[Riebesell et al. 2024](https://arxiv.org/abs/2308.14920)）。

## 3. 活跃研究课题组、研究方向与代表论文

本章按材料体系与方法路线分组介绍 34 个活跃团队（学术课题组 + 国家实验室 + 企业研究院）。每个条目给出：机构、研究方向（具体到体系与方法）、代表性论文（均已核实存在，附链接）。

### 3.1 金属与合金：成分配比优化的主战场

**（1）Dierk Raabe / Fritz Körmann 团队** — 马普钢铁研究所（Max-Planck-Institut für Eisenforschung, MPIE，德国）
- **方向**：钢铁与高熵合金的"计算热力学 + 机器学习 + 原位实验"一体化成分设计；高熵 Invar 合金（超低热膨胀，面向液氢/液化天然气储运）。
- **代表论文**：Rao, Tung, Xie, …, Körmann, Raabe, "[Machine learning-enabled high-entropy alloy discovery](https://www.science.org/doi/10.1126/science.abo4940)", *Science* 378, 78 (2022)（被引 873+）——在高维成分空间以主动学习闭环发现高熵 Invar 合金的标志性工作。

**（2）Wen Chen 团队** — 马萨诸塞大学阿默斯特分校（UMass Amherst，美国）
- **方向**：机器学习 + 贝叶斯优化的合金/软材料设计；可解释性与不确定性量化驱动的成分优化。
- **代表论文**：Wen et al., "[Machine learning assisted design of high-entropy alloys with desired property](https://www.sciencedirect.com/science/article/abs/pii/S1359645419301430)", *Acta Mater.* 170, 109 (2019)（被引 1079+）；Zhang, Apley & Chen, "[Bayesian optimization for materials design with mixed qualitative and quantitative variables](https://pmc.ncbi.nlm.nih.gov/articles/PMC7080833/)", *J. Mech. Des.* 142, 111410 (2020)（被引 440+，处理"元素选择（类别变量）+ 配比（连续变量）"联合优化的经典方法）；Wen et al., "[Modeling solid solution strengthening in high-entropy alloys using machine learning](https://www.sciencedirect.com/science/article/abs/pii/S1359645421002974)", *Acta Mater.* 212, 116917 (2021)——成分→摩擦应力的可解释模型。

**（3）Turab Lookman** — 洛斯阿拉莫斯国家实验室（LANL，美国；现已加入佛罗里达大学）
- **方向**：主动学习/自适应实验加速功能材料发现（压电、形状记忆合金、磁致伸缩材料）；"ML 筛选 + 定向实验"范式的奠基者之一。
- **代表论文**：Xue et al., "[Accelerated search for BaTiO₃-based piezoelectrics with larger piezoelectric constants and Curie temperatures](https://pubmed.ncbi.nlm.nih.gov/27821777/)", *PNAS* 113, 13301 (2016)（被引 165+）；Yuan et al., "[Accelerated discovery of large electrostrains in BaTiO₃-based piezoelectrics using active learning](https://advanced.onlinelibrary.wiley.com/doi/abs/10.1002/adma.201702884)", *Adv. Mater.* 30, 1702884 (2018)；Lookman et al., "[Active learning in materials science with emphasis on adaptive sampling using uncertainties for targeted design](https://www.nature.com/articles/s41524-019-0153-8)", *npj Comput. Mater.* 5, 21 (2019)——不确定度驱动定向设计的系统综述。

**（4）Raymundo Arróyave 团队** — 德克萨斯农工大学（Texas A&M，美国）
- **方向**：物理信息贝叶斯优化与热力学-ML 耦合的合金成分设计（NiTi 形状记忆合金、稀土化合物）。
- **代表论文**：Arróyave et al., "[A perspective on Bayesian methods applied to materials discovery and design](https://www.osti.gov/pages/biblio/2202745)" (2022)（被引 65+）；Khatamsaz et al., "[A physics informed Bayesian optimization approach for material design: application to NiTi shape memory alloys](https://www.nature.com/articles/s41524-023-01173-7)", *npj Comput. Mater.* 9 (2023)——多目标 BO 优化 NiTi 相变温度/滞后并实验验证；Singh et al., "[Machine-learning enabled thermodynamic model for the design of new rare-earth compounds](https://www.sciencedirect.com/science/article/abs/pii/S135964542200146X)", *Acta Mater.* (2022)。

**（5）Zi-Kui Liu 团队** — 宾夕法尼亚州立大学（Penn State，美国）
- **方向**：CALPHAD + zentropy 熵理论 + 机器学习的成分-相结构设计（难熔合金、高熵陶瓷）；"基因组式"材料设计框架。
- **代表论文**：Li et al., "[Design and validation of refractory alloys using machine learning, CALPHAD, and experiments](https://doi.org/10.1016/j.ijrmhm.2024.106673)", *Int. J. Refract. Met. Hard Mater.* 121, 106673 (2024)；Debnath et al., "[Generative deep learning as a tool for inverse design of high-entropy refractory alloys](https://doi.org/10.20517/jmi.2021.05)", *J. Mater. Inform.* 1, 3 (2021)——生成式网络逆向生成满足目标的难熔高熵合金成分。

**（6）Ichiro Takeuchi** — 马里兰大学（UMD，美国）
- **方向**：组合薄膜实验 + 在线（on-the-fly）机器学习的相图构建与合金发现。
- **代表论文**：Ueno, Rhone, Hou, Mizoguchi, Tsuda, "[COMBO: An efficient Bayesian optimization library for materials science](https://www.semanticscholar.org/paper/COMBO%3A-An-efficient-Bayesian-optimization-library-Ueno-Rhone/aff41db86488fee0bf1fa302586690d0e621efca)" (2016)（材料领域被引用最多的 BO 工具库之一）；Stanev et al., "[Machine learning modeling of superconducting critical temperature](https://www.nature.com/articles/s41524-018-0085-8)", *npj Comput. Mater.* 4, 29 (2018)（UMD 参与的超导 ML 筛选，SuperCon 数据库建模）。此外，Kusne et al., "[On-the-fly machine-learning for high-throughput experiments: search for rare-earth-free permanent magnets](https://www.nature.com/articles/srep06367)", *Sci. Rep.* 4, 6367 (2014) 开创了高通量实验中"边采集边学习"的闭环范式；Al Hasan et al., "[Combinatorial exploration and mapping of phase transformation in a Ni–Ti–Co thin film library](https://pubs.acs.org/acsccc/article/22/11/641/605953/Combinatorial-Exploration-and-Mapping-of-Phase)", *ACS Comb. Sci.* 22, 641 (2020)。

**（7）Tejs Vegge 团队** — 丹麦技术大学（DTU，丹麦）
- **方向**：贝叶斯优化驱动的高熵合金电催化剂成分设计。
- **代表论文**：Pedersen et al., "[Bayesian optimization of high-entropy alloy compositions for electrocatalytic oxygen reduction](https://onlinelibrary.wiley.com/doi/abs/10.1002/anie.202108116)", *Angew. Chem. Int. Ed.* 60, 24144 (2021)——从庞大 HEA 成分空间搜索高活性 ORR 催化剂成分。

**（8）A. Lindsay Greer 团队** — 剑桥大学（英国）
- **方向**：金属玻璃成分的机器学习预测 + 演化算法设计。
- **代表论文**：Forrest & Greer, "[Evolutionary design of machine-learning-predicted bulk metallic glasses](https://doi.org/10.1039/D2DD00078D)", *Digital Discovery* 2, 202 (2023)——ML 预测玻璃形成能力 + 演化搜索新块体金属玻璃成分。

**（9）谢建新 / 宿彦京 / 付华栋 / 姜雪 团队** — 北京科技大学（USTB，中国；"北京材料基因工程高精尖创新中心"）
- **方向**：材料基因工程专用数据库与高通量技术；面向工程性能的合金成分 ML 双向设计（MLDS 系统：C²P 成分→性能 / P²C 性能→成分）；大语言模型驱动的钢材设计。
- **代表成果**：高强高导铜合金成分设计（强度 800 MPa 级 + 导电率 50% IACS，见[宿彦京等综述](https://www.ams.org.cn/article/2020/0412-1961/0412-1961-56-10-1313.shtml)）；"[Steel design based on a large language model](https://bjmge.ustb.edu.cn/kexueyanjiu/keyanchengguo1/keyanchengguo/2025-04-27/396.html)", *Acta Mater.* (2025)——从材料文本到钢材性能的 LLM 端到端预测；Zhang et al., "[Empowering the sustainable development of high-end alloys via interpretive machine learning](https://advanced.onlinelibrary.wiley.com/doi/10.1002/adma.202404478)", *Adv. Mater.* 36, 2404478 (2024)；Feng, Fu, …, Dong, "[A general and transferable deep learning framework for predicting phase formation in materials](https://www.nature.com/articles/s41524-020-00488-z)", *npj Comput. Mater.* 7, 24 (2021)——从成分直接预测相形成；中国"材料基因工程"重点专项的数据库与高通量计算牵头团队。

**（10）吕昭平团队（北京科技大学新金属材料全国重点实验室）与刘兴军团队**（香港城市大学，现北科大）
- **方向**：高熵合金强韧化（间隙原子有序化）、高通量实验。
- **代表论文**：Lei et al., "[Enhanced strength and ductility in a high-entropy alloy via ordered oxygen complexes](https://pubmed.ncbi.nlm.nih.gov/30429610/)", *Nature* 563, 546 (2018)（被引 1974+）。

**（11）Bryce Meredig / James Saal** — Citrine Informatics（美国，公司背景）
- **方向**：无约束成分空间的机器学习筛选；"已确认预测"（confirmed predictions）的系统性追踪。
- **代表论文**：Meredig et al., "[Combinatorial screening for new materials in unconstrained composition space with machine learning](https://ui.adsabs.harvard.edu/abs/2014PhRvB..89i4104M/abstract)", *Phys. Rev. B* 89, 094104 (2014)（被引 950+，扫描 160 万候选成分、预测 4500 个新稳定三元化合物）；Saal, Oliynyk, Meredig, "[Machine learning in materials discovery: confirmed predictions and their underlying approaches](https://par.nsf.gov/servlets/purl/10292820)", *Annu. Rev. Mater. Res.* 50, 49 (2020)。

**（12）Wei Xu（许伟）团队** — 东北大学轧制技术及连轧自动化国家重点实验室（RAL，中国）
- **方向**：物理冶金知识引导的机器学习超高强不锈钢成分设计。
- **代表论文**：Shen et al., "[Physical metallurgy-guided machine learning and artificial intelligent design of ultrahigh-strength stainless steel](https://www.sciencedirect.com/science/article/abs/pii/S1359645419305452)", *Acta Mater.* 179, 201 (2019)——以位错强化等冶金机理为特征工程的钢成分 ML 设计。

**（13）Jinshan Li（李金山）团队** — 西北工业大学凝固技术国家重点实验室（中国）
- **方向**：数据挖掘 + 深度学习的钛合金/高熵合金强塑性协同成分设计（AI for Materials）。
- **代表论文**：Zou et al., "[Integrating data mining and machine learning to discover high-strength ductile titanium alloys](https://doi.org/10.1016/j.actamat.2020.10.056)", *Acta Mater.* 202, 211 (2021)。

**（14）Shijun Zhao 与 Yang Yang 团队** — 香港城市大学（中国香港）
- **方向**：机器学习设计高熵陶瓷（碳化物）、可解释图注意力设计高熵电催化剂、生成式设计共晶成分复杂合金。
- **代表论文**：Zhang et al., "[Design high-entropy carbide ceramics from machine learning](https://doi.org/10.1038/s41524-021-00678-3)", *npj Comput. Mater.* 8, 5 (2022)；Chen et al., "[Design high-entropy electrocatalyst via interpretable deep graph attention learning](https://doi.org/10.1016/j.joule.2023.06.003)", *Joule* 7, 1832 (2023)；Chen, Shang, Liu & Yang, "[Accelerated discovery of eutectic compositionally complex alloys by generative machine learning](https://doi.org/10.1038/s41524-024-01385-5)", *npj Comput. Mater.* 10, 204 (2024)——CVAE 生成模型直接生成四元至六元共晶合金新成分。

**（15）Jun Ni（倪军）团队** — 清华大学物理系（中国）
- **方向**：小样本生成对抗网络 + 元素特征迁移预测高熵合金性质并探索成分空间。
- **代表论文**：Sun, …, Ni, "[EFTGAN: elemental features and transferring corrected data augmentation for the study of high-entropy alloys](https://doi.org/10.1038/s41524-025-01548-y)", *npj Comput. Mater.* 11 (2025)——小样本数据增强，免结构计算即在广阔成分空间预测形成能与磁矩。

**（16）Lijun Zhang（张利军）团队** — 中南大学粉末冶金国家重点实验室（中国）
- **方向**：CALPHAD + 机器学习耦合的铸造铝合金成分/元素配比设计。
- **代表论文**：Yi et al., "[Boosting for concept design of casting aluminum alloys driven by combining computational thermodynamics and machine learning techniques](https://www.oaepublish.com/articles/jmi.2021.10)", *J. Mater. Inform.* 1, 10 (2021)。

### 3.2 计算数据、通用模型与基础模型（成分优化的基础设施层）

**（17）Shyue Ping Ong 团队** — 加州大学圣地亚哥分校（UCSD，"Materials Virtual Lab"）
- **方向**：材料图网络（MEGNet）、特征工程库（matminer）、通用原子间势（CHGNet）。
- **代表论文**：Chen et al., "[Graph networks as a universal machine learning framework for molecules and crystals](https://arxiv.org/abs/1812.05055)" (2019)（被引 2100+）；Deng et al., "[CHGNet as a pretrained universal neural network potential for charge-informed atomistic modelling](https://www.nature.com/articles/s42256-023-00716-3)", *Nat. Mach. Intell.* 5, 1031 (2023)（被引 1624+）。

**（18）Kristin Persson** — 劳伦斯伯克利国家实验室（LBNL）/ UC Berkeley
- **方向**：Materials Project 数据库建设；性质预测基准（Matbench / Matbench Discovery）。
- **代表论文**：Jain et al., "[Commentary: The Materials Project: A materials genome approach to accelerating materials innovation](https://doi.org/10.1063/1.4812323)", *APL Mater.* 1, 011002 (2013)（被引 16,900+）；Horton et al., "[Accelerated data-driven materials science with the Materials Project](https://doi.org/10.1038/s41563-025-02272-0)", *Nat. Mater.* 24, 1522 (2025)；Riebesell et al., "[Matbench Discovery](https://www.nature.com/articles/s42256-025-01055-1)", *Nat. Mach. Intell.* 7, 836 (2025)。

**（19）Anubhav Jain** — 劳伦斯伯克利国家实验室（LBNL，美国）
- **方向**：高通量计算工作流（Atomate/FireWorks）与自然语言处理/LLM 的材料合成规划——把文献中的合成配方结构化，反哺"可合成性"建模。
- **代表论文**：Dagdelen et al., "[Structured information extraction from scientific text with large language models](https://www.nature.com/articles/s41467-024-45563-x)", *Nat. Commun.* 15, 1418 (2024)；Wang et al., "[Dataset of solution-based inorganic materials synthesis routes](https://www.nature.com/articles/s41597-022-01317-2)", *Sci. Data* 9, 205 (2022)。

**（20）Gerbrand Ceder 团队** — 麻省理工学院 / LBL（材料项目创始团队）
- **方向**：高通量 DFT + 机器学习的电池材料与无机新材料发现；成分级热力学描述符；自主合成实验室（A-Lab）。
- **代表论文**：Bartel et al., "[Physical descriptor for the Gibbs energy of inorganic crystalline solids and temperature-dependent materials chemistry](https://www.nature.com/articles/s41467-018-06682-4)", *Nat. Commun.* 9, 4168 (2018)——成分描述符预测吉布斯自由能；Bartel et al., "[New tolerance factor to predict the stability of perovskite oxides and halides](https://doi.org/10.1126/sciadv.aav0693)", *Sci. Adv.* 5, eaav0693 (2019)——从成分判断钙钛矿稳定性；Szymanski et al., "[An autonomous laboratory for the accelerated synthesis of inorganic materials](https://www.nature.com/articles/s41586-023-06734-w)", *Nature* 624, 86 (2023)（被引 1746+；2026 年作者更正见[此处](https://www.nature.com/articles/s41586-025-09992-y)）。

**（21）Chris Wolverton 团队** — 西北大学（Northwestern，美国）
- **方向**：OQMD 大型 DFT 数据库；MAGPIE 特征体系与早期的成分基机器学习（与 Logan Ward、Bryce Meredig 等合作）。
- **代表论文**：Kirklin et al., "[The Open Quantum Materials Database (OQMD) and the formation energy of compounds](https://www.nature.com/articles/npjcompumats201510)", *npj Comput. Mater.* 1, 15010 (2015)；Shen et al., "[Reflections on one million compounds in the Open Quantum Materials Database](https://iopscience.iop.org/article/10.1088/2515-7639/ac7ba9)" (2022)。

**（22）Stefano Curtarolo 团队** — 杜克大学（Duke，美国）
- **方向**：AFLOW 高通量计算框架与数据库（390 万+化合物）；"regret minimization"式的材料发现推荐。
- **代表论文**：Curtarolo et al., "[AFLOW: An automatic framework for high-throughput materials discovery](https://doi.org/10.1016/j.commatsci.2012.02.005)", *Comput. Mater. Sci.* 58, 218 (2012)（经典框架论文）；Esters & Curtarolo, "[Optimization of high-throughput searches: The AFLOW Fleet](https://www.sciencedirect.com/science/article/abs/pii/S0927025622005195)" (2023)；[aflow.org](https://www.aflowlib.org/)。

**（23）Logan Ward** — 芝加哥大学（UChicago/ChiMaD，美国）
- **方向**：MAGPIE/Matbench 特征与基准体系、自动化材料科学（Automatminer）。
- **代表论文**：Ward et al., "[A general-purpose machine learning framework for predicting properties of inorganic materials](https://www.nature.com/articles/npjcompumats201628)", *npj Comput. Mater.* 2, 16028 (2016)（被引 1000+，MAGPIE 特征体系奠基之作，与 Wolverton/Meredig 合作）；Ward et al., "[Matminer: An open source toolkit for materials data mining](https://www.osti.gov/pages/biblio/1532339)", *Comput. Mater. Sci.* 152, 60 (2018)。

**（24）Kamal Choudhary** — 美国国家标准技术研究院（NIST）
- **方向**：JARVIS 数据库与原子级线性图网络（ALIGNN）。
- **代表论文**：Choudhary et al., "[The joint automated repository for various integrated simulations (JARVIS) for data-driven materials design](https://www.nature.com/articles/s41524-020-00440-1)", *npj Comput. Mater.* 6, 64 (2020)（被引 690+）；Choudhary & DeCost, "[Atomistic line graph neural network for improved materials property predictions](https://www.nature.com/articles/s41524-021-00650-1)", *npj Comput. Mater.* 7, 185 (2021)。

**（25）Yousung Jung 团队** — 首尔国立大学（SNU，韩国）
- **方向**：AI + 电子结构方法；LLM 预测新材料可合成性——把"生成出来的成分能否做出来"变成可学习的对象。
- **代表论文**：Kim et al., "[Large language models for inorganic synthesis predictions](https://doi.org/10.1021/jacs.4c05840)", *J. Am. Chem. Soc.* 146, 10124 (2024)——LLM 从数万篇论文学习并预测无机合成路线；Kim et al., "[Explainable synthesizability prediction of inorganic crystal polymorphs using large language models](https://doi.org/10.1002/anie.202423950)", *Angew. Chem. Int. Ed.* (2025)。

**（26）Atsuto Seko 团队** — 京都大学（日本）
- **方向**：成分描述符与推荐系统；机器学习势。
- **代表论文**：Seko et al., "[Compositional descriptor-based recommender system for the materials discovery](https://pubs.aip.org/aip/jcp/article/148/24/241719/961129/Compositional-descriptor-based-recommender-system)", *J. Chem. Phys.* 148, 241719 (2018)；Seko et al., "[Representation of compounds for machine-learning prediction of materials properties](https://link.aps.org/doi/10.1103/PhysRevB.95.144110)", *Phys. Rev. B* 95, 144110 (2017)。

**（27）Koji Tsuda / Ryo Tamura** — 东京大学 + NIMS/RIKEN（日本）
- **方向**：贝叶斯优化（COMBO/PHYSBO 工具库）与 AI-机器人闭环自主实验（NIMS-OS）。
- **代表论文**：Ueno et al., "[COMBO: An efficient Bayesian optimization library for materials science](https://www.semanticscholar.org/paper/COMBO%3A-An-efficient-Bayesian-optimization-library-Ueno-Rhone/aff41db86488fee0bf1fa302586690d0e621efca)" (2016)；Tamura et al., "[NIMS-OS: an automation software to implement a closed loop between artificial intelligence and robotic experiments in materials science](https://doi.org/10.1080/27660400.2023.2232297)", *STAM Methods* 3, 2232297 (2023)；Motoyama et al., "[Bayesian optimization package: PHYSBO](https://www.sciencedirect.com/science/article/pii/S0010465522001242)", *Comput. Phys. Commun.* 278 (2022)；Yoshikawa et al., "[Self-driving laboratories in Japan](https://doi.org/10.1039/D4DD00387J)", *Digital Discovery* 4, 1384 (2025)。

**（28）Google DeepMind（Merchant 等）**
- **方向**：大规模图网络 + 主动学习替代 DFT 的材料探索（GNoME）。
- **代表论文**：Merchant et al., "[Scaling deep learning for materials discovery](https://www.nature.com/articles/s41586-023-06735-9)", *Nature* 624, 80 (2023)（被引 2581+）——220 万新晶体、38.1 万稳定相、736 种被外部实验室合成。

**（29）Microsoft Research AI for Science（Zeni、Xie 等）**
- **方向**：条件扩散生成式材料设计（MatterGen）、通用机器学习势（MatterSim）。
- **代表论文**：Zeni et al., "[A generative model for inorganic materials design](https://www.nature.com/articles/s41586-025-08628-5)", *Nature* 639, 624 (2025)（被引 1250+）。（注：本报告不引用该公司域名资源，引文为 Nature 论文与 arXiv 预印本。）

### 3.3 聚合物、催化与其他功能材料

**（30）Rampi Ramprasad 团队** — 佐治亚理工学院（Georgia Tech，美国）
- **方向**：聚合物信息学（Polymer Genome）——聚合物重复单元/组成→介电常数、带隙、Tg 等性质的 ML 预测与设计，已延伸至工业合作。
- **代表论文**：Kim et al., "[Polymer Genome: A data-powered polymer informatics platform for property predictions](https://pubs.acs.org/jpccck/article/122/31/17575/1470511/Polymer-Genome-A-Data-Powered-Polymer-Informatics)", *J. Phys. Chem. C* 122, 17575 (2018)（被引 674+）；Doan Tran et al., "[Machine-learning predictions of polymer properties with Polymer Genome](https://pubs.aip.org/aip/jap/article/128/17/171104/1062836/Machine-learning-predictions-of-polymer-properties)", *J. Appl. Phys.* 128, 171104 (2020)；Gurnani et al., "[Polymer informatics at scale with multitask graph neural networks](https://pmc.ncbi.nlm.nih.gov/articles/PMC9979603/)", *Chem. Mater.* (2023)。

**（31）Zachary Ulissi 团队** — 卡内基梅隆大学（CMU，美国）
- **方向**：电催化剂高通量 DFT + 主动学习的成分筛选。
- **代表论文**：Tran & Ulissi, "[Active learning across intermetallics to guide discovery of electrocatalysts for CO₂ reduction and H₂ evolution](https://www.osti.gov/biblio/1543784)", *Nat. Catal.* 1, 696 (2018)——主动学习跨金属间化合物筛选催化剂成分。

### 3.4 生成式模型与自主实验闭环

**（32）Tian Xie**（MIT 博士，CDVAE 一作；Orbital Materials/Orbital Industries 联合创始人，英国）
- **方向**：晶体扩散生成模型（CDVAE）；面向清洁技术材料的生成式基础模型（碳捕集吸附剂、数据中心冷却材料）。
- **代表论文**：Xie et al., "[Crystal Diffusion Variational Autoencoder for periodic material discovery](https://arxiv.org/abs/2110.06197)", NeurIPS 2022（被引 700+）。

**（33）Andrew Cooper 团队** — 利物浦大学（英国）
- **方向**：移动机器人化学家（robot chemist）与自主合成；序贯闭环贝叶斯优化的配方发现。
- **代表论文**：Burger et al., "[A mobile robotic chemist](https://www.nature.com/articles/s41586-020-2442-2)", *Nature* 583, 237 (2020)（被引 2197+）；Dai et al., "[Autonomous mobile robots for exploratory synthetic chemistry](https://www.nature.com/articles/s41586-024-08173-7)", *Nature* 635 (2024)；Li et al., "[Sequential closed-loop Bayesian optimization as a guide for organic molecular metallophotocatalyst formulation discovery](https://pmc.ncbi.nlm.nih.gov/articles/PMC11321994/)", *Nat. Chem.* (2024)。

**（34）Alán Aspuru-Guzik** — 多伦多大学（加拿大，Acceleration Consortium 主任）
- **方向**：自驱实验室（self-driving labs）与材料/化学闭环实验基础设施；"化学与材料科学的自主实验"权威综述。
- **代表论文**：Tom et al., "[Self-driving laboratories for chemistry and materials science](https://pubs.acs.org/chreay/article/124/16/9633/154652)", *Chem. Rev.* 124, 9633 (2024)（被引 1127+）。

### 3.5 中国的体系化布局（补充）

除 3.1 所列北科大、东北大学、西北工业大学、中南大学、香港城市大学、清华大学等团队外，中国在该领域的布局以国家专项为牵引：科技部"十三五""材料基因工程关键技术与支撑平台"重点专项（2015 年启动，45 个项目、投入 >30 亿元、参与单位 >400 家，见[宿彦京等 2020 综述](https://www.ams.org.cn/article/2020/0412-1961/0412-1961-56-10-1313.shtml)）；地方平台包括上海材料基因组工程研究院（2015，上海大学牵头）、中科院物理所怀柔材料基因工程平台、深圳材料基因组大科学装置平台等；2025 年《科技导报》以"[材料基因工程与智能科学：AI+时代无尽前沿](https://castjournals.cast.org.cn/joweb/kjdb/CN/10.3981/j.issn.1000-7857.2025.05.00039)"为题进行了阶段性总结。学术侧的高熵合金 ML 设计综述（如[李俊炎等 2025，材料导报](https://www.mater-rep.com/CN/abstract/abstract7790.shtml)）和难熔高熵合金 ML 设计工作（如北京理工大学 He et al. 2024，"Machine learning-assisted design of refractory high-entropy alloys with targeted yield strength and fracture strain"，被引 64+）代表了该方向的活跃度。

### 3.6 课题组汇总表

| 团队/PI | 机构（国家） | 研究方向 | 代表论文（年份，被引） |
|---|---|---|---|
| D. Raabe / F. Körmann | MPIE（德） | 高熵合金/Invar 主动学习闭环设计 | Science 2022（873+） |
| Wen Chen | UMass Amherst（美） | ML+BO 合金设计、可解释性 | Acta Mater. 2019（1079+）; JMD 2020（440+） |
| Turab Lookman | LANL→佛罗里达大学（美） | 主动学习功能材料发现 | PNAS 2016; Adv. Mater. 2018; npj 2019 |
| R. Arróyave | Texas A&M（美） | 物理信息 BO + CALPHAD | npj 2023（NiTi BO）; Acta Mater. 2022 |
| Zi-Kui Liu | Penn State（美） | CALPHAD+zentropy+ML 难熔合金 | IJRMHM 2024; JMI 2021 |
| I. Takeuchi | 马里兰大学（美） | 组合实验 + 在线 ML | Sci. Rep. 2014（on-the-fly） |
| T. Vegge | DTU（丹麦） | BO 设计高熵合金催化剂 | Angew. 2021 |
| A. L. Greer | 剑桥大学（英） | 金属玻璃 ML+演化设计 | Digital Discovery 2023 |
| B. Meredig | Citrine（美） | 无约束成分空间 ML 筛选 | PRB 2014（950+）; Annu. Rev. 2020 |
| 谢建新/宿彦京/付华栋等 | 北科大（中） | 材料基因工程数据库、MLDS、LLM 钢设计 | 金属学报 2020; npj 2021; Adv. Mater. 2024; Acta Mater. 2025 |
| 吕昭平 / 刘兴军 | 北科大 / 港城大（中） | 高熵合金强韧化、高通量实验 | Nature 2018（1974+） |
| Wei Xu 许伟 | 东北大学（中） | 冶金引导 ML 不锈钢设计 | Acta Mater. 2019 |
| Jinshan Li 李金山 | 西北工业大学（中） | 数据挖掘+ML 钛合金设计 | Acta Mater. 2021 |
| Shijun Zhao / Yang Yang | 香港城市大学（中） | 高熵陶瓷/催化剂、生成式共晶合金 | npj 2022; Joule 2023; npj 2024 |
| Jun Ni 倪军 | 清华大学（中） | 小样本 GAN 探索 HEA 成分空间 | npj 2025（EFTGAN） |
| Lijun Zhang 张利军 | 中南大学（中） | CALPHAD+ML 铸造铝合金 | J. Mater. Inform. 2021 |
| S. P. Ong | UCSD（美） | 图网络、通用势（CHGNet） | 2019（2100+）; Nat. Mach. Intell. 2023（1624+） |
| K. Persson | LBNL/UCB（美） | Materials Project、数据平台 | APL Mater. 2013（16,900+）; Nat. Mater. 2025 |
| A. Jain | LBNL（美） | 高通量工作流、LLM 合成规划 | Nat. Commun. 2024; Sci. Data 2022 |
| G. Ceder | MIT/LBL（美） | 热力学描述符、电池材料、A-Lab | Nat. Commun. 2018; Sci. Adv. 2019; Nature 2023（1746+） |
| C. Wolverton | Northwestern（美） | OQMD、MAGPIE | npj 2015; PRB 2014（950+） |
| S. Curtarolo | Duke（美） | AFLOW 数据库与发现推荐 | Comput. Mater. Sci. 2012; 2023 |
| Logan Ward | 芝加哥大学（美） | MAGPIE/Matminer 工具链 | npj 2016（1000+）; CMS 2018 |
| K. Choudhary | NIST（美） | JARVIS、ALIGNN | npj 2020（690+）; npj 2021 |
| Yousung Jung | 首尔国立大学（韩） | LLM 可合成性预测 | JACS 2024; Angew 2025 |
| A. Seko | 京都大学（日） | 成分描述符推荐系统 | PRB 2017; JCP 2018 |
| K. Tsuda / R. Tamura | 东京大学/NIMS（日） | COMBO/PHYSBO、NIMS-OS 闭环 | 2016; CPC 2022; STAM Methods 2023 |
| Google DeepMind | —（英/美） | 大规模 ML 材料探索（GNoME） | Nature 2023（2581+） |
| MSR AI for Science | —（英/美） | 生成式设计（MatterGen） | Nature 2025（1250+） |
| R. Ramprasad | Georgia Tech（美） | 聚合物信息学 | JPCC 2018（674+）; Chem. Mater. 2023 |
| Z. Ulissi | CMU（美） | 主动学习电催化剂筛选 | Nat. Catal. 2018 |
| Tian Xie / Orbital | MIT→企业（英/美） | 晶体生成模型、商业化 | NeurIPS 2022（700+） |
| A. Cooper | 利物浦大学（英） | 机器人化学家、闭环 BO | Nature 2020（2197+）; Nature 2024; Nat. Chem. 2024 |
| A. Aspuru-Guzik | 多伦多大学（加） | 自驱实验室 | Chem. Rev. 2024（1127+） |

**补充说明**：①企业主体（Citrine Informatics、QuesTek、Alloyed、Uncountable、Atinary、Albert Invent、Orbital Materials/Orbital Industries、Entalpic 等）及其融资与落地案例详见第 7.2 节（5）；②更细粒度的课题组调研底稿（含每篇论文的完整链接与核实状态）见同目录附档 `materials-ml-composition-groups.md`；③本节个别中文名（如 Wen Chen、Zi-Kui Liu、Yousung Jung 等的汉字写法）未逐一核实，以英文/拼音为准。

---


## 4. 常用数据库与基准测试分析

### 4.1 DFT 高通量计算数据库（成分优化的"训练数据主粮"）

| 数据库 | 维护方 | 规模（截至 2026） | 覆盖性质 | 代表论文/入口 |
|---|---|---|---|---|
| Materials Project (MP) | 伯克利 LBNL | >154,000 材料 + 172,000 分子 | 形成能、凸包距离、带隙、弹性、介电、电池电极性质 | [Jain et al., APL Mater. 1, 011002 (2013)](https://ceder.berkeley.edu/publications/2013_Jain_Materials_Project.pdf)；[materialsproject.org](https://materialsproject.org/) |
| OQMD | Northwestern 大学 Wolverton 组 | **1,407,395 材料**（官网快照） | DFT 形成能、基态相、结构 | [Kirklin et al., npj Comput. Mater. 1, 15010 (2015)](https://www.nature.com/articles/npjcompumats201510)；[Shen et al. 2022](https://iopscience.iop.org/article/10.1088/2515-7639/ac7ba9)；[oqmd.org](https://www.oqmd.org/) |
| AFLOW | Duke 大学 Curtarolo 组 | **>350 万材料条目** | 形成能、带隙、弹性、热力学、原型库 | [Esters & Curtarolo 2023](https://www.sciencedirect.com/science/article/abs/pii/S0927025622005195)；[aflow.org](https://www.aflowlib.org/)（官网现值约 393 万化合物） |
| JARVIS | 美国 NIST（Choudhary） | 80,000+ 材料、150 万+ 数据 | 形成能/带隙、2D 材料、力场、拓扑 | [Choudhary et al., npj Comput. Mater. 6, 64 (2020)](https://www.nature.com/articles/s41524-020-00440-1)；[jarvis.nist.gov](https://jarvis.nist.gov/) |
| NOMAD | 柏林 FHI/洪堡（Draxl & Scheffler） | 1,940 万上传条目、435 万材料 | 全谱 DFT 原始输入/输出（FAIR 共享） | [Draxl & Scheffler, J. Phys. Mater. 2, 011001 (2019)](https://iopscience.iop.org/article/10.1088/2515-7639/ab13bb)；[nomad-lab.eu](https://nomad-lab.eu/) |

**关键背景数字**：OQMD 论文报告其 DFT 形成能相对实验平均误差约 **0.105 eV/atom**（金属间化合物约 0.071 eV/atom）——这是评估一切 ML 模型精度时的"天花板基准"：当模型 MAE 进入 0.02–0.06 eV/atom 区间时，误差已低于 DFT 方法本身的系统误差，继续压低回归误差的意义让位于稳定性分类的正确率（见第 5.3 节）。

### 4.2 实验/文献数据库与专用数据集（实验性质建模的数据源）

| 数据库/数据集 | 维护方 | 规模 | 覆盖 | 入口/论文 |
|---|---|---|---|---|
| SpringerMaterials | Springer Nature | 29 万+ 物质体系、3,000+ 性质 | 相图、热/磁/光/电实验性质 | [materials.springer.com](https://materials.springer.com/) |
| MatWeb | MatWeb | >200,000 份数据表 | 金属/塑料/陶瓷/复合材料力/热/电性质 | [matweb.com](https://www.matweb.com/) |
| Citrine PDC | Citrine Informatics | 未公开总数；开放数据含 **630 组多主元合金（MPEA）力学/相观察数据** | 文献/实验聚合（GEMD 格式） | [MPEA 数据集](https://citrine.io/expanded-dataset-of-mechanical-properties-and-observed-phases-of-multi-principal-element-alloys/) |
| NIMS MDR | 日本 NIMS | 约 17,800 个数据集 | 多领域研究数据托管（含超导库） | [mdr.nims.go.jp](https://mdr.nims.go.jp/) |
| SuperCon / 3DSC / SuperMat | NIMS / KIT / INRIA | SuperCon 约 33,000 条（Stanev 清洗子集 16,400 条）；3DSC_MP 5,759 条、3DSC_ICSD 9,150 条 | 超导 Tc（±近似结构） | [Sommer et al., Sci. Data 10, 846 (2023)](https://www.nature.com/articles/s41597-023-02721-y) |
| 高熵合金数据集 | 多个团队 | ① 401 组 HEA 相数据（Huang 2019）；② 612 组硬度数据（2026，Al-Co-Cr-Cu-Fe-Ni-V 七元素体系） | 相分类（SS/IM/SS+IM）、硬度 | [Huang et al., Acta Mater. 173, 317 (2019)](https://www.sciencedirect.com/science/article/abs/pii/S1359645419301454) |
| PoLyInfo | NIMS | >500,000 条聚合物数据 | Tg、Tm、密度、力学/热/电 | [Ishii et al. 2024](https://www.tandfonline.com/doi/full/10.1080/27660400.2024.2354649) |
| Polymer Genome 数据 | Georgia Tech Ramprasad 组 | 文献 + 量子化学计算混合 | 聚合物带隙、Tg、介电常数、密度 | [Kim et al., J. Phys. Chem. C 122, 17575 (2018)](https://pubs.acs.org/jpccck/article/122/31/17575/1470511/Polymer-Genome-A-Data-Powered-Polymer-Informatics) |
| 电池材料数据库 | 多机构 | 292,313 条记录、214,617 组唯一化学-性质对 | 电极/电解质化学-性质关联 | [Huang et al., Sci. Data 7, 260 (2020)](https://www.nature.com/articles/s41597-020-00602-2) |
| 金属玻璃（GFA） | Ren 等 / Matbench | matbench_glass 5,680 条 | 玻璃形成能力分类 | [Ren et al., Sci. Adv. 4, eaaq1566 (2018)](https://www.science.org/doi/10.1126/sciadv.aaq1566) |

### 4.3 公共基准测试

- **Matbench**（[Dunn et al., npj Comput. Mater. 6, 138 (2020)](https://www.nature.com/articles/s41524-020-00406-3)）：13 个任务、5 折嵌套交叉验证，任务规模从 312 条（钢材屈服强度，纯成分输入）到 132,752 条（MP 形成能）。它把"成分输入"任务（steels、expt_gap、expt_is_metal、glass）与"结构输入"任务放在同一榜单下，是目前最系统的性质预测基准（[榜单](https://matbench.materialsproject.org/)）。
- **Matbench Discovery**（[Riebesell et al., Nat. Mach. Intell. 7, 836 (2025)](https://www.nature.com/articles/s42256-025-01055-1)）：模拟真实发现流程——从非弛豫结构预测弛豫后凸包距离、判定稳定相。测试集 WBM 假想晶体 215,488 个唯一原型结构（含 32,942 个相对 MP 凸包稳定相）。指标以 **F1、发现加速因子 DAF** 为主，而非 MAE。截至 2026 年榜单已收录 58 个合格模型（[榜单](https://matbench-discovery.materialsproject.org/)）。
- **Open Catalyst (OC20/OC22)**（Meta/CMU）：OC20 含 1,281,121 次 DFT 弛豫（约 2.5 亿单点计算），面向催化剂表面吸附能预测（[Chanussot et al., ACS Catal. 11, 6059 (2021)](https://pubs.acs.org/doi/10.1021/acscatal.0c04525)）。

### 4.4 数据库与评测协议层面的分析

1. **训练数据以计算数据为主、实验数据结构性薄弱**：五大 DFT 库合计数百万条、内部一致性好；而实验性质数据（硬度、服役性能）多为文献汇编，规模小、协议不一、缺失工艺条件——这正是成分优化模型在实验场景精度受限的根源。
2. **数据划分协议决定结论可信度**：随机 k 折交叉验证在"化学空间聚类"的数据上会高估泛化能力。已证的外推退化案例：MP2018 训练的模型在 MP2021 新增合金上 MAE 恶化 **3–14 倍**（ALIGNN 0.022 → 0.297 eV/atom，XGBoost 0.075 → 0.239，RF 0.088 → 0.382）（[Li, DeCost, Choudhary, arXiv:2210.13597](https://arxiv.org/abs/2210.13597)）。规范做法是留元素/留化学空间分组划分（MatFold，[Witman et al., Digital Discovery 4, 625 (2025)](https://pubs.rsc.org/dd/article/4/3/625/846149/)）与 LOCO-CV（工业平台标准协议）。
3. **形成能精度 ≠ 稳定性判断力**：[Bartel et al., npj Comput. Mater. 6, 55 (2020)](https://www.nature.com/articles/s41524-020-00362-y) 与 Matbench Discovery 均指出：高精度回归模型在凸包决策边界附近会产生大量假阳性，必须以分类指标评估。

---

## 5. 模型准确度评估

### 5.1 计算性质（DFT 数据）：形成能与带隙

**成分基模型（仅输入元素配比）的形成能预测演进：**

| 模型 | 数据 | MAE (eV/atom) | 来源 |
|---|---|---|---|
| Magpie 特征 + 随机森林 | OQMD 256,620 | 0.067 | [Goodall & Lee 2020 复现](https://pmc.ncbi.nlm.nih.gov/articles/PMC7722901/) |
| ElemNet（端到端成分网络） | OQMD | 0.055 | [Jha et al., Sci. Rep. 8, 17593 (2018)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6279928/) |
| ElemNet + 迁移学习（预测实验值） | 实验形成能 | 0.078–0.095 | [Jha et al. 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6874674/) |
| Roost（深度集合，集成） | OQMD 256,620 | **0.024–0.030** | [Goodall & Lee, Nat. Commun. 11, 6280 (2020)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7722901/) |
| CrabNet（成分注意力） | Matbench mp_e_form | 0.086 | [Matbench 榜单](https://matbench.materialsproject.org/) |

**引入晶体结构后的精度（对照）：**

| 模型 | 数据/任务 | MAE | 来源 |
|---|---|---|---|
| CGCNN | MP 形成能 | 0.039 eV/atom | [Xie & Grossman, PRL 120, 145301 (2018)](https://arxiv.org/abs/1710.10324) |
| MEGNet | MP 69,640 晶体 | 形成能 0.032 eV/atom；带隙 0.35 eV | [Chen et al., Chem. Mater. 31, 3564 (2019)](https://arxiv.org/abs/1812.05055) |
| ALIGNN | MP-2018 69,239 | 形成能 0.022 eV/atom；带隙（JARVIS-DFT）0.218 eV | [Choudhary & DeCost, npj Comput. Mater. 7, 185 (2021)](https://www.nature.com/articles/s41524-021-00650-1) |
| coGN（当前 Matbench 榜首） | Matbench mp_e_form | **0.0170 eV/atom** | [Matbench 榜单](https://matbench.materialsproject.org/) |
| GNoME（大规模主动学习 GNN） | 相对 MP 稳定性 | MAE 11 meV/atom；稳定预测精度 >80% | [Merchant et al., Nature 624, 80 (2023)](https://www.nature.com/articles/s41586-023-06735-9) |

**Matbench 榜单的定量结论**：在同一任务（mp_e_form）上，纯成分模型（CrabNet 0.086、Magpie+RF 0.117）的误差约为结构模型（coGN 0.017、ALIGNN 0.021）的 **3–5 倍**；但成分模型无需结构输入，可枚举全部配比空间，是成分优化的主力。

### 5.2 实验性质（合金、超导、玻璃等）

| 任务 | 模型/方法 | 精度 | 来源 |
|---|---|---|---|
| 高熵合金相分类（401 组数据） | ANN | SS/IM 86.7%；SS+IM/IM 94.3%；SS/SS+IM 78.9%；三相同分 KNN/SVM/ANN 68.6%/64.3%/74.3% | [Huang et al., Acta Mater. 173, 317 (2019)](https://www.sciencedirect.com/science/article/abs/pii/S1359645419301454) |
| 高熵合金硬度 | 可解释 ML（留一法） | R² 0.9716、RMSE 39.3 HV | [Ren et al. 2023](https://lanlexperts.elsevierpure.com/en/publications/prediction-and-design-of-high-hardness-high-entropy-alloy-through/) |
| 多元合金硬度/弹性模量 | ML（JAP 2026） | R² 0.93 / 0.88 | [J. Appl. Phys. 137, 195305 (2026)](https://pubs.aip.org/aip/jap/article/137/19/195305/3347209) |
| 超导 Tc（SuperCon >12,000 化合物） | RF/XGBoost | 分类准确率 ~92%；低 Tc 回归 R² ≈0.85 | [Stanev et al., npj Comput. Mater. 4, 29 (2018)](https://www.nature.com/articles/s41524-018-0085-8) |
| 金属玻璃形成能力（GFA，5,680 条） | MODNet | ROC-AUC 0.9603 | [Matbench 榜单](https://matbench.materialsproject.org/) |
| 实验带隙（成分输入，3,895 条） | Roost + MP 预训练迁移 | MAE 0.219 eV（直接训练 0.277 eV） | [Goodall & Lee 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7722901/) |
| 钢材屈服强度（312 条，成分输入） | MODNet | MAE 87.76 MPa（榜单最佳） | [Matbench 榜单](https://matbench.materialsproject.org/) |

### 5.3 Matbench Discovery：以"发现有效性"为标准的评估

这是与本报告主题最贴近的评测。截至 2026 年末榜单（unique prototypes 口径，58 个合格模型）：

| 排名/模型 | F1 | DAF | MAE (eV/atom) | R² | 年份 |
|---|---|---|---|---|---|
| #1 DPA-4.1-Max-OAM-PFT | **0.935** | 6.089 | 0.017 | 0.872 | 2026 |
| #2 DPA-4.1-Max-OAM | 0.933 | 6.160 | — | — | 2026 |
| 头部：EquiformerV3+DeNS / TECE / Prophet 等 | 0.928–0.931 | ~6 | — | — | 2025–2026 |
| CHGNet-0.3.0 | 0.613（unique prototypes）/ 0.851（全测试集） | — | — | — | 2023 |
| MACE-MP-0 | 0.669 | — | — | — | 2023 |
| 论文 v3 时期的模型谱系 F1 | 0.57–0.82 | 最高 6× | — | — | 2024 |

（数据源：[matbench-discovery.materialsproject.org](https://matbench-discovery.materialsproject.org/)；早期论文版本与现榜单因 WBM 标签更新存在口径差异，引用时须注明。）

**要点解读**：

1. **2023 → 2026 的进步是阶跃式的**：早期 UIP 模型 F1 0.57–0.82，2026 年头部的通用势基础模型（DPA-4.1、EquiformerV3 等）已达 F1 0.93+、MAE 0.017 eV/atom、DAF ≈ 6.1（理论上限约 6.5）——即"用模型排序前 1 万个候选，发现稳定新材料的效率约为随机筛选的 6 倍"。
2. **通用势模型吃掉了"结构已知"场景**：排名前列者全部是能量+力+应力联合训练的通用原子间势（MPtrj 数据集 158 万结构）。
3. **成分级代理模型仍是"快速枚举"不可替代的工具**：Wren（坐标无关）、CrabNet、Roost 等在无需结构的场景下维持可用精度，但其在分布外的稳定性判断明显逊于 UIP（这正是第 6 章"外推"挑战的量化证据）。

### 5.4 准确度数字的正确解读——三条纪律

1. **看口径**：同一模型在不同测试划分（全测试集 vs unique prototypes、随机 CV vs LOCO/留元素）下的指标差异可达数十个百分点；任何"R² 0.9+"的声明都应先问验证协议。
2. **看任务对齐**：形成能 MAE 0.02 eV/atom 不等于能发现稳定相（Bartel & Ceder 2020；Matbench Discovery 均证实）；对成分优化任务，F1/DAF/发现率比 MAE 更有决策价值。
3. **看数据规模与体系覆盖**：实验数据任务（数百~数千条）上的 R² 0.9 通常只在"近邻内插"成立；跨体系（如从 Al-Co-Cr-Fe-Ni 系换到耐火 HEA 体系）需要重新验证。

---

## 6. 挑战与可行性分析

本章将本领域公认的核心挑战归纳为三大类（数据、模型、工程/组织），对每项挑战给出**现状 → 现有缓解手段 → 可行性评级**。评级含义：**高**=方法已成熟、只待推广；**中**=已有可用方案但适用范围有限；**低**=尚无公认有效方案，属研究前沿。

### 6.1 数据层面

#### 挑战 1：实验数据稀缺、昂贵且系统性偏倚

- **现状**：新材料实验数据集通常只有几十到几千条；表征一个全新材料的成本可达数万美元（[Citrine 平台论文, arXiv:2607.25039](https://arxiv.org/abs/2607.25039)）。小数据困境是本领域被引最多的综述主题之一（[Xu et al., npj Comput. Mater. 9, 42 (2023)](https://www.nature.com/articles/s41524-023-01000-z)，被引 1000+）。更严重的是发表偏倚——只有"成功"的成分-性能数据点进入文献，失败样本系统性缺失；而 Raccuglia 等人证明**失败实验数据恰恰能显著提升模型质量**（[Raccuglia et al., Nature 533, 73 (2016)](https://www.nature.com/articles/nature17439)）。
- **缓解手段与可行性**：
  - 以高通量 DFT 数据增强（Materials Project 约 15 万结构级）——对计算性质**可行性高**，对加工依赖的实验性能（硬度、疲劳、服役寿命）**可行性中**，因为 0 K 基态计算与实验条件存在系统性鸿沟。
  - 大语言模型挖掘文献/报告中的结构化数据（如 [Yang et al., Digital Discovery (2026)](https://pubs.rsc.org/dd/article/5/5/1981/1229885/Large-language-models-in-materials-science-and-the)）；北科大基于 LLM 的钢材端到端设计流程（[宿彦京、姜雪等, Acta Materialia (2025)](https://bjmge.ustb.edu.cn/kexueyanjiu/keyanchengguo1/keyanchengguo/2025-04-27/396.html)）——**可行性中偏高**，但抽取质量控制与单位/条件错读是主要风险。
  - 数据模型标准化（GEMD、FAIR 原则、中国 CSTM 材料基因工程通则标准）——技术**可行性高**，但落地速度受组织与激励机制制约。

#### 挑战 2：DFT 数据与实验数据之间的鸿沟

- **现状**：Matbench Discovery 的核心发现之一是：**成分模型可以把 DFT 形成能预测到有用精度，但预测分解焓（凸包距离）时性能急剧恶化**——因为随机误差在"决策边界"（0 eV/atom 凸包距离）附近会系统性放大假阳性率（[Riebesell et al. 2024](https://arxiv.org/abs/2308.14920)）。换言之，"MAE 好看"不等于"发现有用"。
- **缓解手段与可行性**：以任务为导向的分类指标（F1、DAF）替代全局回归指标——**可行性高**（基准框架已建成）；让模型学习力与应力标签（UIP 路线）从非弛豫结构直接预测弛豫能量——已证明可将 DAF 提升至接近理论上限，**可行性高**（见第 5 节）。

### 6.2 模型层面

#### 挑战 3：分布外外推——成分优化本质上是在"训练集之外"搜索

- **现状**：优化算法天然把采样推向训练数据稀疏甚至从未出现过的区域（新元素组合、新配比区间）。随机 k 折交叉验证会高估此类场景的性能，必须使用留元素/留体系（Leave-One-Cluster-Out, LOCO）协议（由 Meredig 等人在成分空间筛选研究中提出，现为工业平台标准验证协议，见 [Citrine 平台论文综述](https://arxiv.org/abs/2607.25039)）。
- **缓解手段与可行性**：
  - 预训练基础模型 + 微调：2025–2026 年多项工作表明，通用机器学习势（U-MLIP）经少量体系内数据微调可达到接近从头算精度（[Radova et al., npj Comput. Mater. (2025)](https://www.nature.com/articles/s41524-025-01727-x)；[Hänseroth et al., J. Phys. Chem. Lett. (2026)](https://pubs.acs.org/jpclcd/article/17/11/3152/5074062/Fine-Tuning-Unifies-Foundational-Machine-Learned)）——在"近邻外推"场景**可行性高**，在全新化学空间仍有限。
  - 校准的不确定性量化：深度集成、读出层集成、保形预测（conformal prediction）用于决定"何时该相信模型"（[Bilbrey et al., npj Comput. Mater. (2025)](https://www.nature.com/articles/s41524-025-01572-y)；[Out-of-distribution ML for materials discovery, Chem. Phys. Rev. (2024)](https://pubs.aip.org/aip/cpr/article/7/1/011317/3384237/Out-of-distribution-machine-learning-for-materials)）——方法**可行性中偏高**，且必须与主动学习闭环捆绑使用才有意义。

#### 挑战 4：可合成性与可制造性约束

- **现状**：GNoME 预测的 220 万个晶体结构中 38.1 万个位于凸包上（[Merchant et al., Nature 624, 80 (2023)](https://www.nature.com/articles/s41586-023-06735-9)），但"热力学稳定"不等于"可合成"：真实合成受动力学、成核路径、原料可得性制约。A-Lab 论文宣称 17 天自动合成 41 个新化合物，随后受到系统性质疑（[Leeman et al., PRX Energy 3, 011002 (2024)](https://link.aps.org/doi/10.1103/PRXEnergy.3.011002)），Nature 已于 2026 年 1 月发布作者更正（[Author Correction, Nature (2026)](https://www.nature.com/articles/s41586-025-09992-y)）：修正后表述为 17 天合成 57 个目标中的 36 个，并澄清"新颖性"指"对预测平台新"而非"对科学界新"。这一事件是"生成式模型输出 × 自动合成验证"整条流水线可信度风险的典型案例。
- **缓解手段与可行性**：合成条件预测模型与文本挖掘仍在早期；目前工程上稳妥的做法是把可合成性作为设计空间的**硬约束**（已知相、前驱体、工艺窗口）而非软预测——**可行性中**。

#### 挑战 5：多目标、成本与工艺耦合

- **现状**：真实成分优化几乎总是多目标的（强度–延性–成本–可焊性等），且性能是"成分 × 工艺"的联合函数；仅以成分为变量的模型会遗漏工艺维度导致的性能方差。
- **缓解手段与可行性**：约束多目标 BO、Pareto 前沿 + 决策分析在算法上**可行性高**；瓶颈在"含工艺变量的数据"是否被系统记录（GEMD 类数据模型正是为此设计）。工业实践已证明该路线可用（Citrine 客户案例；中国高强高导铜合金 MLDS "成分→性能 / 性能→成分"双向模型体系，见[宿彦京等 2020](https://www.ams.org.cn/article/2020/0412-1961/0412-1961-56-10-1313.shtml)）。

#### 挑战 6：可解释性与工艺落地

- **现状**：即便预测准确，工艺师需要知道"为什么"才能指导熔炼/热处理参数调整。
- **缓解手段与可行性**：特征重要性（SHAP）、符号回归（SISSO）、物理描述符归因等可解释方法在高熵合金设计中已广泛使用（如可解释硬度模型 [Ren et al. 2023](https://lanlexperts.elsevierpure.com/en/publications/prediction-and-design-of-high-hardness-high-entropy-alloy-through/)，留一法 R² 达 0.97）——**可行性高**。

### 6.3 工程、基准与组织层面

#### 挑战 7：基准与可复现性

- **现状**：Matbench（13 个任务）与 Matbench Discovery（稳定性发现，2026 年末快照已收录 58 个合格模型）使学术比较标准化（[matbench-discovery.materialsproject.org](https://matbench-discovery.materialsproject.org/)）；但**工业私有数据上没有公共基准**，各家声明精度不可横向比较；自主实验室论文的"无人复核"问题（A-Lab 争议）暴露了闭环系统缺乏第三方验证机制。
- **可行性**：学术侧**高**；工业侧需要行业联盟与保密基准（联邦评测），**中**。

#### 挑战 8：闭环验证成本与硬件覆盖度

- **现状**：主动学习闭环必须以实验/计算为"评估器"。自主实验室资本开支高，且当前对无机固体的自动化合成主要覆盖氧化物/磷酸盐粉体与薄膜路线，对大块合金熔炼、变形热处理等冶金工艺的自动化程度低。
- **可行性**：以"人在环"的半自动闭环（模型推荐 + 常规实验执行）为过渡形态，**可行性高**；全自动固体合成实验室**中偏低**。

#### 挑战 9：数据孤岛与知识产权

- **现状**：高价值成分-工艺-性能数据沉淀在少数企业内部，公开学术数据稀疏，形成"数据富人/穷人"分化。
- **可行性**：平台化（SaaS）与数据信托/联邦学习模式正在探索，**中**；政策与标准（FAIR、CSTM）是加速器。

### 6.4 可行性总表

| 挑战 | 严重程度 | 现有最佳缓解 | 综合可行性判断 |
|---|---|---|---|
| 实验数据稀缺与偏倚 | 高 | DFT 增强 + LLM 文献挖掘 + 数据标准化 | 中-高（10 年尺度持续改善） |
| DFT-实验鸿沟 | 高 | UIP 基础模型 + 任务化指标 | 高（近 3 年进步最快） |
| 分布外外推 | 极高 | 预训练-微调 + 校准 UQ + 闭环 | 中（近邻外推高、远距外推低） |
| 可合成性 | 极高 | 设计空间硬约束 + 合成预测研究 | 低-中（研究前沿） |
| 多目标/工艺耦合 | 中 | 约束 BO + Pareto + GEMD 工艺数据 | 高 |
| 可解释性 | 中 | SHAP/SISSO/物理描述符 | 高 |
| 基准与可复现性 | 中 | Matbench/MBD、行业联盟 | 学术侧高、工业侧中 |
| 闭环成本 | 中-高 | 半自动闭环、云实验室 | 高（过渡形态） |
| 数据孤岛 | 高 | 平台化、联邦模式 | 中 |

**总体判断**：在"成分配比优化"这个具体任务上，限制因素已从**算法精度**转移到**数据生态与验证基础设施**——这正是判断产业化时间线的关键依据。

---

## 7. 产业化距离评估：距离"理想模型"的大规模应用还有多远？

### 7.1 先定义"理想模型"

综合本领域路线图文献，一个"理想"的成分优化模型应当同时满足：

1. **通用性**：跨元素周期表、跨材料类别的零样本迁移；
2. **全变量**：输入覆盖成分配比 + 工艺路径（温度/时间/形变/热处理），输出覆盖全套使用性能与服役寿命；
3. **校准的不确定性**：给出可信的概率区间，知道"自己不知道什么"；
4. **可合成性感知**：输出附带可合成性与制造可行性判断；
5. **成本可忽略**：单次评估毫秒级，可支撑 10⁹ 量级候选空间的枚举筛选；
6. **闭环集成**：与高通量计算、自动化实验、工艺执行系统打通，形成"设计→验证→反馈"闭环。

**当前没有任何单一模型同时满足 1–4。**

### 7.2 七条证据链：我们正处在什么位置

**（1）计算筛选：加速比已达 5–6.5 倍并逼近该基准的理论上限，且仍在快速进步。** Matbench Discovery 在 215,488 个候选中发现 32,942 个稳定相的任务上：2024 年论文时期最优模型（EquiformerV2+DeNS 等通用机器学习势）F1 0.57–0.82、前 1 万名候选 DAF 6.33（理论上限 ≈6.5）（[Riebesell et al. 2024](https://arxiv.org/abs/2308.14920)，正式版见 [Nat. Mach. Intell. 7, 836 (2025)](https://www.nature.com/articles/s42256-025-01055-1)）；到 2026 年末榜单，头部基础模型（DPA-4.1、EquiformerV3 等）已达 **F1 0.93+、MAE 0.017 eV/atom、DAF ≈ 6.1**（[matbench-discovery.materialsproject.org](https://matbench-discovery.materialsproject.org/)）。这意味着"ML 前置过滤 + DFT 确认"的两段式计算筛选已达工程可用水平。

**（2）生成式逆设计：从"可能"走向"按需生成"，但独立验证率仍低。** MatterGen 微调后可按目标磁/电/力学性质与目标化学计量生成全新稳定材料（[Zeni et al., Nature 639, 624 (2025)](https://www.nature.com/articles/s41586-025-08628-5)），并与实验方合作合成了新化合物 TaCr₂O₆（实测体模量 169 GPa vs 目标 200 GPa）；GNoME 预测的 220 万新晶体中已有 736 种被外部实验室独立合成（[DeepMind 官方博客](https://deepmind.google/blog/millions-of-new-materials-discovered-with-deep-learning/)；[伯克利实验室报道](https://newscenter.lbl.gov/2023/11/29/google-deepmind-new-compounds-materials-project/)）。但 Park 等在 Matter 上的批判性评估指出，生成式逆设计整体上尚未解决"给定性质→材料"问题（[Park et al., Matter (2024)](https://www.cell.com/matter/fulltext/S2590-2385(24)00242-X)）。

**（3）主动学习：工业案例证明 2–9 倍实验量削减。** Citrine 平台公开发表的客户案例（有机半导体、钯纳米颗粒自主合成、合金开发等）显示 FUELS 序贯学习相对随机搜索减少 2–9 倍实验量（[arXiv:2607.25039 (2026)](https://arxiv.org/abs/2607.25039)）；该公司自述已"从一次性演示进入常规工业实践"。

**（4）自主实验室：演示级到可信级之间仍有距离。** A-Lab（17 天合成目标化合物，修正后 36/57）及其后续争议（[Leeman et al. 2024](https://link.aps.org/doi/10.1103/PRXEnergy.3.011002)；[Nature 2026 作者更正](https://www.nature.com/articles/s41586-025-09992-y)）说明：闭环自动化在**速度**上已突破，在**可信度与可复核性**上仍需工程与规范建设。更早的利物浦"移动机器人化学家"（8 天自主完成 688 次实验、发现活性约为初始 6 倍的光催化剂，[Burger et al., Nature 583, 237 (2020)](https://www.nature.com/articles/s41586-020-2442-2)，被引 2197+）同样在 2026 年经历了更正与质疑（[C&EN](https://cen.acs.org/research-integrity/Nature-robot-chemist-paper-corrected/104/web/2026/01)）。

**（5）产业渗透：软件与专项已形成真实产值与可验证案例。** 材料信息学市场 2026 年约 2.5 亿美元，预测 2035 年达 13 亿美元（CAGR ≈9%，[Precedence Research](https://www.precedenceresearch.com/materials-informatics-market)）。可第三方验证的"成分/配方优化 → 真实材料"案例已有：QuesTek 的 Ferrium M54 钢获美国海军 T-45 舰载机着舰钩应用资格（[NIST 案例研究](https://www.nist.gov/document/materialsinnovationcasestudyquestek090616pdf)）；Alloyed（牛津衍生）的 ABD-900AM 增材制造镍基高温合金实现商业化（与 Aubert & Duval 合作，[报道](https://www.tctmagazine.com/alloyed-and-aubert-duval-team-up-on-release-of-nickel-superalloy/)）；Citrine 帮助 Panasonic 以 ML 加速有机半导体材料开发并产出专利申请（[案例](https://citrine.io/technical-case-study-machine-learning-accelerates-materials-development-for-panasonic/)）；GNoME 预测晶体中 736 种被外部实验室合成。资本面：Uncountable 2025 年 A 轮 2700 万美元、Albert Invent 2026 年 B 轮 5500 万美元、Orbital Materials（前 DeepMind 成员创立，生成式材料设计）2026 年 B 轮 5000 万美元；多伦多大学 Acceleration Consortium 自驱实验室获 2 亿加元联邦资助（目标把新材料上市周期从"平均 20 年/1 亿美元"压缩到"1 年/100 万美元"，[官方报道](https://acceleration.utoronto.ca/news/u-of-t-receives-200-million-grant-to-support-acceleration-consortiums-self-driving-labs-research)）。中国"材料基因工程"重点专项（>30 亿元投入）已产出工程化成果：ML 成分设计的二代耐热腐蚀镍基单晶高温合金 DD489、800 MPa 级高强高导铜合金（导电率 50% IACS）、400 km/h 高铁车轴钢、UO₂-BeO 复合核燃料（从设计到入堆考核不足 2 年，国际上通常约 10 年）（[宿彦京等 2020](https://www.ams.org.cn/article/2020/0412-1961/0412-1961-56-10-1313.shtml)）。

**（6）基础模型浪潮：2025–2026 年出现"材料基础模型"研究爆发。** 通用原子间势微调达到近从头算精度（[Radova 2025](https://www.nature.com/articles/s41524-025-01727-x)、[JPC Lett. 2026](https://pubs.acs.org/jpclcd/article/17/11/3152/5074062/Fine-Tuning-Unifies-Foundational-Machine-Learned)）、成分性质预测的在上下文学习基础模型（[Li et al., npj Comput. Mater. (2026)](https://www.nature.com/articles/s41524-026-02089-8)）相继发表，表明"预训练-微调"范式正在材料领域复制 NLP 的路线。但 Pyzer-Knapp 等指出，材料基础模型仍处早期，小数据专用模型 + 严格基准仍是当前主流（[Pyzer-Knapp et al., npj Comput. Mater. (2025)](https://www.nature.com/articles/s41524-025-01538-0)）。

**（7）评论界的共识（2020–2026 年路线图文献）。** 代表性观点包括：de Pablo 等的 MGI 前瞻（数据生态、复杂层级材料、面向制造，[npj Comput. Mater. 5, 41 (2019)](https://www.nature.com/articles/s41524-019-0173-4)）；Takahashi 的"材料信息学黄金时代"论（从早期采用向规模化过渡，数据生态与人才是关键，[J. Phys. Chem. Lett. 14, 4726 (2023)](https://pubs.acs.org/jpclcd/article/14/20/4726/361629)）；Tom 等的自主实验室权威综述（商业化受制于资本开支、标准化/互操作、数据与人才，建议"SDL 即服务"与共享基础设施，[Chem. Rev. 124, 9633 (2024)](https://pubs.acs.org/chreay/article/124/16/9633/154652)，被引 1100+）；Bauer 等的数据中心路线图（数据质量/FAIR/互操作决定落地速度，[IOP 2024](https://iopscience.iop.org/article/10.1088/1361-651X/ad4d0d)）；He 等的最新判断（高质量材料数据生态仍是最大瓶颈，[Natl. Sci. Rev. (2026)](https://academic.oup.com/nsr/article/13/7/nwag108/8483891)）。综合来看，评论界对"大规模落地"普遍持 **10 年尺度渐进**（而非指数爆发）的判断，与本报告 7.4 节的基准情景一致。

### 7.3 技术成熟度（TRL）分层评估

| 能力层 | 当前 TRL（估计） | 判断依据 |
|---|---|---|
| 特定体系成分-性能代理模型 + BO（如高熵合金硬度、铜合金强导） | **7–9** | 已嵌入企业日常研发与国家专项验收成果 |
| 约束多目标成分优化 + 工艺窗口设计 | **6–8** | Citrine/QuesTek/MLDS 等已商用 |
| MLIP 基础模型 + 主动计算/实验闭环（特定材料类） | **4–6** | DAF 5–6.5×、微调近从头算精度，但落地项目数量有限 |
| 生成式成分/结构逆设计（结构级） | **3–5** | MatterGen 等已发表 + 少量实验验证 |
| 全自主材料合成实验室 | **3–5** | A-Lab 及同类系统为演示级，可复核性待建 |
| 理想"通用成分×工艺×性能"模型（本报告定义） | **2–3** | 无单一模型同时满足通用性+工艺+服役+校准 UQ |

（TRL：1–3 研究验证，4–6 实验室/相关环境验证，7–9 工程验证与运行。估计为本报告的分析性判断。）

### 7.4 三情景时间表（分析性预测，非文献既定结论）

- **基准情景（概率最高）**：
  - **现在–3 年**：特定材料类（高熵合金、电池电解质、催化剂配方、合金牌号升级）的"专用闭环设计系统"在头部材料企业成为标准工具；TRL 7–9 层能力大规模复制；市场规模按 ~9% CAGR 扩张。
  - **3–7 年**：材料基础模型（U-MLIP + 成分预训练模型）商品化，成为研发流程的默认入口；自主实验室从演示级进入可信级（第三方复核规范建立）；可合成性预测取得实质突破。
  - **7–15 年**："理想模型"分步逼近——但只有在数据生态（FAIR 化、工艺数据沉淀、跨机构数据共享）与验证基础设施同步建设的条件下才成立。
- **乐观情景**：基础模型 + 自主实验室的组合在 2027–2030 年出现"材料设计 Copilot"级产品，专用场景闭环周期缩短到周级；但数据生态仍是硬约束。
- **悲观情景**：若数据孤岛与可合成性问题长期无解，"理想模型"停留在"专用系统集合"状态（即今天的状态），只是专用系统数量持续增多——这本身已具巨大产业价值，但不等于理想模型。

### 7.5 可核查的里程碑指标

判断本领域进展，建议跟踪以下可量化指标（当前值 → 理想值）：

1. 通用成分模型在**留元素外推**基准上的校准误差：当前明显劣于内插 → 达到与 DFT 一致的精度；
2. 生成式模型输出的**独立第三方实验验证成功率**：当前零星报道 → >50% 且有公开登记；
3. 自主实验室端到端"概念→验证材料"周期：A-Lab 级（17 天/批）→ 可复制的月级流程（含第三方复核）；
4. 工业研发中 ML 闭环渗透率与实验节省：已证 2–9× → 行业平均化；
5. FAIR/结构化工艺数据覆盖率：当前低 → 研发数据默认结构化入库。

### 7.6 结论：对"还有多远"的直接回答

- **对"最佳元素配比优化"这一具体任务**：大规模应用**已经开始**。凡是"已有数据积累 + 明确目标性能 + 常规验证手段"的场景（合金硬度/强度/导电、相形成、介电/催化性能），专用 ML 优化系统已进入工业日常，未来 2–5 年将从头部企业扩散到中腰部企业。
- **对"通用基础模型"**：处于从演示到商品化的拐点（TRL 4–6 → 7），预计 5–10 年内成为研发基础设施。
- **对"理想模型"（通用 + 全变量 + 校准 + 可合成 + 全闭环）**：**10–15 年量级**，且瓶颈不在算法，而在三件事——高质量实验/工艺数据生态、可合成性与可制造性建模、可信自主验证基础设施。这三件事的进度（而非更多模型论文）将决定产业化时间表。

---

## 8. 结论

1. **领域已跨过"可行性演示"阶段**。从 Meredig 2014 年扫描 160 万候选成分，到 Rao 2022 年在 Science 上以主动学习发现高熵 Invar 合金，再到 2025 年 MatterGen 按需生成稳定新材料、2026 年 Matbench Discovery 榜首模型 F1 达 0.93——十多年间，"ML 优化成分配比"从概念验证变成了可复现的工程能力。

2. **技术版图呈四层生态**：学术课题组（计算驱动的代理模型/基础模型 + 实验驱动的主动学习闭环）、国家实验室与数据库平台（MP/OQMD/AFLOW/JARVIS/NOMAD）、企业软件与设计服务（Citrine、QuesTek、Alloyed、Uncountable 等）、国家专项（美国 MGI、中国材料基因工程、日本 NIMS 材料 DX）。四层正在互相咬合。

3. **数据是最大的不对称**：计算数据已达数百万条且高度结构化；实验性质数据仍以数百~数千条的小数据集为主，且缺乏工艺条件与失败样本。这决定了：纯成分代理模型在"近邻内插 + 快速枚举"场景可靠，在"跨体系外推 + 服役性能"场景必须依赖闭环验证。

4. **精度数字要"看口径、看任务、看协议"**：形成能 MAE 已达 0.017–0.030 eV/atom（成分模型 0.024–0.117，低于 DFT 本身相对实验约 0.1 eV/atom 的系统误差）；实验任务上相分类 86–94%、硬度 R² ≈0.93–0.97、超导分类 ≈92%——但这些数字几乎全部来自内插型验证；留元素/分布漂移场景下 MAE 恶化 3–14 倍的实测是评估真实能力更诚实的标尺。

5. **对从业者三条务实建议**：
   - **数据治理优先于算法选型**：用 LOCO/留元素协议评估，把工艺变量与不确定性记录进数据模型（GEMD/FAIR）；
   - **用"发现加速"而非"回归误差"评估闭环**（F1/DAF/实验削减倍数），主动学习闭环是中小数据场景性价比最高的路线；
   - **把可合成性做成设计空间的硬约束**，并对生成式模型的输出保持独立实验验证的习惯（A-Lab 争议的教训）。

6. **距离大规模产业化：分层而非单一答案**。专用成分优化系统已在工业日常（未来 2–5 年普及到中腰部企业）；通用材料基础模型处于商品化拐点（约 5–10 年）；"理想模型"需 10 年以上，且等待的是数据生态与验证基础设施，而非算法突破。

---

## 9. 主要参考文献与数据来源

本报告正文采用行内链接引用；以下按主题汇总最核心的文献与数据来源（全部可公开访问，均已核实）。**来源纪律**：全文未使用 microsoft.com 与 news.northwestern.edu 域名资源（MatterGen 引 Nature 论文与 arXiv；Northwestern 相关工作引 npj/APS/Annual Reviews 等出版社页面）。

### 9.1 综述与立场性文献

1. Saal, Oliynyk & Meredig, "Machine learning in materials discovery: confirmed predictions and their underlying approaches", [Annu. Rev. Mater. Res. 50, 49 (2020)](https://par.nsf.gov/servlets/purl/10292820)——实验确认的 ML 材料预测案例盘点。
2. Lookman et al., "Active learning in materials science...", [npj Comput. Mater. 5, 21 (2019)](https://www.nature.com/articles/s41524-019-0153-8)。
3. de Pablo et al., "New frontiers for the materials genome initiative", [npj Comput. Mater. 5, 41 (2019)](https://www.nature.com/articles/s41524-019-0173-4)。
4. Takahashi, "Toward the Golden Age of Materials Informatics", [J. Phys. Chem. Lett. 14, 4726 (2023)](https://pubs.acs.org/jpclcd/article/14/20/4726/361629)。
5. Tom et al., "Self-driving laboratories for chemistry and materials science", [Chem. Rev. 124, 9633 (2024)](https://pubs.acs.org/chreay/article/124/16/9633/154652)。
6. Park et al., "Has generative artificial intelligence solved inverse materials design?", [Matter (2024)](https://www.cell.com/matter/fulltext/S2590-2385(24)00242-X)。
7. Bauer et al., "Roadmap on data-centric materials science", [IOP (2024)](https://iopscience.iop.org/article/10.1088/1361-651X/ad4d0d)。
8. He et al., "Towards a sustainable high-quality materials data ecosystem", [Natl. Sci. Rev. (2026)](https://academic.oup.com/nsr/article/13/7/nwag108/8483891)。
9. Pyzer-Knapp et al., [npj Comput. Mater. (2025)](https://www.nature.com/articles/s41524-025-01538-0)——材料基础模型现状评估。
10. 宿彦京等, "中国材料基因工程实施进展", [金属学报 56, 1313 (2020)](https://www.ams.org.cn/article/2020/0412-1961/0412-1961-56-10-1313.shtml)。

### 9.2 成分级模型与算法（本报告主题核心）

11. Ward et al.（MAGPIE）, [npj Comput. Mater. 2, 16028 (2016)](https://www.nature.com/articles/npjcompumats201628)。
12. Jha et al.（ElemNet）, [Sci. Rep. 8, 17593 (2018)](https://www.nature.com/articles/s41598-018-35934-y)。
13. Goodall & Lee（Roost）, [Nat. Commun. 11, 6280 (2020)](https://www.nature.com/articles/s41467-020-19964-7)。
14. Wang et al.（CrabNet）, [npj Comput. Mater. 7 (2021)](https://www.nature.com/articles/s41524-021-00545-1)。
15. Meredig et al., [Phys. Rev. B 89, 094104 (2014)](https://ui.adsabs.harvard.edu/abs/2014PhRvB..89i4104M/abstract)。
16. Xue et al.（主动学习奠基）, [PNAS 113, 13301 (2016)](https://pubmed.ncbi.nlm.nih.gov/27821777/)。
17. Rao et al.（高熵 Invar）, [Science 378, 78 (2022)](https://www.science.org/doi/10.1126/science.abo4940)。
18. Zhang, Apley & Chen（混合变量 BO）, [J. Mech. Des. 142, 111410 (2020)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7080833/)。
19. Dan et al.（MatGAN 成分生成）, [npj Comput. Mater. 6, 84 (2020)](https://www.nature.com/articles/s41524-020-00352-0)。
20. Gruver et al.（LLM 成分生成）, [ICLR 2024 / arXiv:2402.04379](https://arxiv.org/abs/2402.04379)。

### 9.3 结构级模型、通用势与生成式大模型

21. Xie & Grossman（CGCNN）, [PRL 120, 145301 (2018)](https://arxiv.org/abs/1710.10324)。
22. Chen et al.（MEGNet）, [arXiv:1812.05055 (2019)](https://arxiv.org/abs/1812.05055)。
23. Choudhary & DeCost（ALIGNN）, [npj Comput. Mater. 7, 185 (2021)](https://www.nature.com/articles/s41524-021-00650-1)。
24. Deng et al.（CHGNet）, [Nat. Mach. Intell. 5, 1031 (2023)](https://www.nature.com/articles/s42256-023-00716-3)。
25. Merchant et al.（GNoME）, [Nature 624, 80 (2023)](https://www.nature.com/articles/s41586-023-06735-9)。
26. Zeni et al.（MatterGen）, [Nature 639, 624 (2025)](https://www.nature.com/articles/s41586-025-08628-5)；arXiv 版 [arXiv:2312.03687](https://arxiv.org/abs/2312.03687)。
27. Xie et al.（CDVAE）, [NeurIPS 2022 / arXiv:2110.06197](https://arxiv.org/abs/2110.06197)。
28. Szymanski et al.（A-Lab）, [Nature 624, 86 (2023)](https://www.nature.com/articles/s41586-023-06734-w)；更正：[Nature Author Correction (2026)](https://www.nature.com/articles/s41586-025-09992-y)；批评：[Leeman et al., PRX Energy 3, 011002 (2024)](https://link.aps.org/doi/10.1103/PRXEnergy.3.011002)。
29. Burger et al.（机器人化学家）, [Nature 583, 237 (2020)](https://www.nature.com/articles/s41586-020-2442-2)。

### 9.4 数据库与基准

30. Jain et al.（Materials Project）, [APL Mater. 1, 011002 (2013)](https://doi.org/10.1063/1.4812323)；平台论文：Horton et al., [Nat. Mater. 24, 1522 (2025)](https://doi.org/10.1038/s41563-025-02272-0)。
31. Kirklin et al.（OQMD）, [npj Comput. Mater. 1, 15010 (2015)](https://www.nature.com/articles/npjcompumats201510)；[oqmd.org](https://www.oqmd.org/)。
32. Curtarolo et al.（AFLOW）, [Comput. Mater. Sci. 58, 218 (2012)](https://doi.org/10.1016/j.commatsci.2012.02.005)；[aflowlib.org](https://www.aflowlib.org/)。
33. Choudhary et al.（JARVIS）, [npj Comput. Mater. 6, 64 (2020)](https://www.nature.com/articles/s41524-020-00440-1)；[jarvis.nist.gov](https://jarvis.nist.gov/)。
34. Draxl & Scheffler（NOMAD）, [J. Phys. Mater. 2, 011001 (2019)](https://iopscience.iop.org/article/10.1088/2515-7639/ab13bb)；[nomad-lab.eu](https://nomad-lab.eu/)。
35. Dunn et al.（Matbench）, [npj Comput. Mater. 6, 138 (2020)](https://www.nature.com/articles/s41524-020-00406-3)；[matbench.materialsproject.org](https://matbench.materialsproject.org/)。
36. Riebesell et al.（Matbench Discovery）, [Nat. Mach. Intell. 7, 836 (2025)](https://www.nature.com/articles/s42256-025-01055-1)；[matbench-discovery.materialsproject.org](https://matbench-discovery.materialsproject.org/)。
37. Bartel et al.（形成能≠稳定性）, [npj Comput. Mater. 6, 55 (2020)](https://www.nature.com/articles/s41524-020-00362-y)。
38. Li, DeCost & Choudhary（分布漂移）, [arXiv:2210.13597](https://arxiv.org/abs/2210.13597)。
39. Chanussot et al.（OC20）, [ACS Catal. 11, 6059 (2021)](https://pubs.acs.org/doi/10.1021/acscatal.0c04525)。

### 9.5 数据来源与快照说明

- 数据库规模数字（OQMD 1,407,395、AFLOW ~393 万、NOMAD 1,940 万条、JARVIS 80,000+ 等）为 2026 年官网快照，随时间增长。
- Matbench / Matbench Discovery 榜单分数为 2026 年末抓取快照（unique prototypes 口径），引用时须注明口径与日期。
- 市场规模（2026 年 2.51 亿美元 → 2035 年 13.1 亿美元）来自 [Precedence Research](https://www.precedenceresearch.com/materials-informatics-market)。
- 中国材料基因工程专项数据（45 个项目、>30 亿元、>400 家单位）来自宿彦京等 2020 综述；官方专项页面未能直接核实，已标注。
- 报告中标注"未核实"的条目：A-Lab 的 Nature Matters Arising 正式链接（以预印本 + Author Correction 形式落地）、利物浦 2020 论文 2026 年更正的 Nature 原始链接（以 C&EN 报道佐证）、Kebotix 2024 年后动态、中国专项官方页面、个别课题组中文名汉字写法。

---


