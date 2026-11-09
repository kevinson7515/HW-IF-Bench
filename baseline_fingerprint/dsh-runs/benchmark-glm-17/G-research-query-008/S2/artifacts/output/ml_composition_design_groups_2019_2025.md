# 机器学习/深度学习驱动的材料成分（元素配比）设计：国际活跃课题组调研报告（2019–2025）

> 调研范围：欧洲、美国、日本、韩国等国际（非中国大陆/港澳台）活跃研究组，聚焦"以 ML/DL 优化材料元素成分/成分设计以获得最优材料性能"方向，重点 2019–2025 年（少量 2016–2018 奠基性工作作为背景收录）。
> 调研方法：全部事实均来自 web_search / web_fetch 检索到的公开网页（期刊页面、arXiv、PubMed、机构官网、作者主页等），每篇论文附来源 URL；未能核实的信息一律标注 **待核实**。
> 说明：nature.com、ScienceDirect 等页面存在访问限制时，引用信息经 PubMed / arXiv / 机构镜像 / 检索摘要交叉核实；卷期页码以 DOI 为最终锚点。

---

## 目录

- 第一部分：课题组明细（按国家/地区分组）
- 第二部分：方法学谱系（按方法分类）
- 第三部分：总览表
- 第四部分：待核实事项与更正清单

---

# 第一部分：课题组明细

## 一、美国

### 1. 麻省理工学院（MIT）— Gerbrand Ceder（格布兰德·塞德）

**机构与 PI**：MIT 材料科学与工程系教授；长期兼职于劳伦斯伯克利国家实验室（LBNL）。电池材料计算与实验设计领域代表人物。

**成分优化方向**：阳离子无序岩盐（DRX）正极与高熵电池材料的成分设计；自主实验室（A-Lab）闭环合成；实验电化学数据的深度学习（DRXNet）；电荷感知通用机器学习势（CHGNet）。

**代表论文**：

1. **《An autonomous laboratory for the accelerated synthesis of novel materials》**（A-Lab）
   - 作者：N. J. Szymanski 等（通讯 G. Ceder）
   - 期刊：*Nature* 624(7990), 86–91 (2023). DOI: 10.1038/s41586-023-06734-w
   - 来源：[Nature 文章页](https://www.nature.com/articles/s41586-023-06734-w)（摘要经 PubMed/检索核实）
   - 方法：机器人自主合成 + 第一性原理数据库 + 机器学习驱动的数据解释，形成闭环
   - 关键成果：17 天连续运行中，从 58 个目标化合物成功合成 **41 个新化合物**（含 XRD 自动解析）

2. **《Cation-disordered rocksalt-type high-entropy cathodes for Li-ion batteries》**
   - 作者：Z. Lun, B. Ouyang, D. H. Kwon, Y. Ha, E. E. Foley, …, G. Ceder
   - 期刊：*Nature Materials* 20(2), 214–221 (2021). DOI: 10.1038/s41563-020-00816-0
   - 来源：[ORNL Impact 页（含完整引用与摘要）](https://impact.ornl.gov/en/publications/cation-disordered-rocksalt-type-high-entropy-cathodes-for-li-ion-/)
   - 方法：高熵（HE）成分设计理念 + 短程有序分析 + 成分相容性分析（23 种过渡金属离子）
   - 关键成果：6 种过渡金属的 DRX 正极在 20 mA g⁻¹ 下达 **307 mAh g⁻¹（955 Wh kg⁻¹）**，2000 mA g⁻¹ 高倍率下仍保持 >170 mAh g⁻¹；合成出含 **12 种过渡金属**的单相高熵 DRX 化合物

3. **《Deep learning of experimental electrochemistry for battery cathodes across diverse compositions》**（DRXNet）
   - 作者：P. Zhong, B. Deng, T. He, Z. Lun, G. Ceder
   - 期刊：*Joule* (2024). DOI: 10.1016/j.joule.2024.03.010（卷期页码待核实）
   - 来源：[arXiv:2304.04986](https://arxiv.org/abs/2304.04986)｜[ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2542435124001454)
   - 方法：面向实验放电曲线的深度学习模型（DRXNet）
   - 关键成果：基于 **19,000+ 条放电电压曲线、覆盖 14 种金属元素**的数据集，跨化学体系预测 Li–Mn–O–F 与高熵 DRX 正极的放电容量，用于成分优化

4. **《CHGNet as a pretrained universal neural network potential for charge-informed atomistic modelling》**
   - 作者：B. Deng 等（Ceder 组）
   - 期刊：*Nature Machine Intelligence* 5 (2023). DOI: 10.1038/s42256-023-00716-3
   - 来源：[Nature 文章页](https://www.nature.com/articles/s42256-023-00716-3)
   - 方法：电荷感知（磁矩输入）通用神经网络势，在 Materials Project 弛豫轨迹上预训练
   - 关键成果：可对异价体系做大规模原子模拟，支撑成分空间的快速结构弛豫与筛选

---

### 2. 麻省理工学院（MIT）— Rafael Gómez-Bombarelli（拉斐尔·戈麦斯-邦巴雷利）

**机构与 PI**：MIT 材料科学与工程系教授。

**成分优化方向**：材料连续（潜空间）表示与逆向设计；生成式分子/材料设计。

**代表论文**：

1. **《Inverse Design of Solid-State Materials via a Continuous Representation》**
   - 作者：J. Noh, J. Kim, H. S. Stein, …, R. Gómez-Bombarelli
   - 期刊：*Matter* 1(5), 1370–1384 (2019). DOI: 10.1016/j.matt.2019.08.017
   - 来源：[ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2590238519301754)
   - 方法：变分自编码器（VAE）学习成分/结构的连续潜表示 + 全局优化
   - 关键成果：在 Mg–Mn–O 三元氧化物空间中演示逆向设计，被后续多篇综述作为固相材料生成式逆向设计的代表工作（[综述引用](https://www.oaepublish.com/articles/jmi.2021.07)）

2. **《Automatic chemical design using a data-driven continuous representation of molecules》**（背景性工作）
   - 作者：R. Gómez-Bombarelli 等
   - 期刊：*Chemical Science* 9, 2869 (2018)
   - 来源：[Google Scholar 作者页](https://scholar.google.com/citations?user=jJ5JkCQAAAAJ&hl=es)
   - 方法：分子连续表示 + 逆向设计框架（材料逆向设计的方法学源头之一）

---

### 3. 麻省理工学院（MIT CSAIL）— Tian Xie（谢天，音译待核实）等（CDVAE）

**机构与 PI**：MIT 计算机科学与人工智能实验室（Regina Barzilay、Tommi Jaakkola 组）。

**成分优化方向**：晶体材料的扩散生成模型（生成新成分+新结构）。

**代表论文**：

1. **《Crystal Diffusion Variational Autoencoder for Periodic Material Generation》**（CDVAE）
   - 作者：T. Xie, X. Fu, O.-E. Ganea, R. Barzilay, T. Jaakkola
   - 期刊：ICLR 2022；arXiv:2110.06197
   - 来源：[arXiv:2110.06197](https://arxiv.org/abs/2110.06197)
   - 方法：扩散式变分自编码器，以扩散过程生成周期性晶体（成分+坐标）
   - 关键成果：生成稳定、新颖的晶体材料，成为周期性材料生成模型的基准之一（注意：该工作属 MIT CSAIL，非 Gómez-Bombarelli 组）

---

### 4. 加州大学伯克利分校 / 劳伦斯伯克利国家实验室（LBNL）— Kristin A. Persson（克里斯汀·A·佩尔松）

**机构与 PI**：UC Berkeley 材料科学与工程系教授；LBNL 高级教职员科学家；Materials Project 创始人/主任。

**成分优化方向**：大规模开放材料数据库（Materials Project）与数据基础设施、特征工程工具链（matminer）、ML 最佳实践——为全球成分筛选类研究提供数据底座。

**代表论文**：

1. **《Accelerated data-driven materials science with the Materials Project》**
   - 作者：M. K. Horton 等（含 K. A. Persson）
   - 期刊：*Nature Materials* 24(10), 1522–1532 (2025). DOI: 10.1038/s41563-025-02272-0
   - 来源：[Nature 文章页](https://www.nature.com/articles/s41563-025-02272-0)
   - 方法/成果：综述 Materials Project 十余年数据基础设施如何加速数据驱动材料发现（含成分筛选）

2. **《Matminer: An open source toolkit for materials data mining》**
   - 作者：L. Ward 等（Persson 组）
   - 期刊：*Computational Materials Science* 152, 60–69 (2018)
   - 来源：[ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0927025618303252)｜[LBL PDF](https://perssongroup.lbl.gov/papers/ward-2018-matminer.pdf)
   - 方法：开源特征（描述符）生成工具链，支撑树模型/经典 ML 的成分建模

3. **《Machine Learning for Materials Scientists: An Introductory Guide Toward Best Practices》**
   - 作者：A. Y.-T. Wang, R. J. Murdock, S. K. Kauwe, …, K. A. Persson
   - 期刊：*Chemistry of Materials* 32(12), 4954–4965 (2020)
   - 来源：[ACS](https://pubs.acs.org/doi/10.1021/acs.chemmater.0c01907)（引用信息经检索核实）
   - 方法/成果：材料 ML 建模（含成分建模）的最佳实践指南，被广泛引用

**备注**：Persson 组的"成分优化"更多体现为数据基础设施 + 下游生态（GNoME、M3GNet、A-Lab 等均建立在 Materials Project 数据之上）。

---

### 5. 加州大学圣地亚哥分校（UCSD）— Shyue Ping Ong（中文名待核实；Ong 为"王"姓的闽南/新加坡拼法）

**机构与 PI**：UCSD 纳米工程系教授；Materials Virtual Lab（MVL）主任；pymatgen 联合开发者。

**成分优化方向**：图神经网络材料性质模型（MEGNet）、通用机器学习势（M3GNet）+ 大规模虚拟成分/结构筛选。

**代表论文**：

1. **《Graph Networks as a Universal Machine Learning Framework for Molecules and Crystals》**（MEGNet）
   - 作者：C. Chen, W. Ye, Y. Zuo, C. Zheng, S. P. Ong
   - 期刊：*Chemistry of Materials* 31(9), 3564–3572 (2019)
   - 来源：[ACS](https://pubs.acs.org/doi/10.1021/acs.chemmater.9b01294)
   - 方法：图神经网络（图网络）统一建模分子与晶体性质
   - 关键成果：在多种材料性质数据集（涵盖分子与晶体）上建立强基线，成为成分-性质建模的标准工具之一

2. **《A universal graph deep learning interatomic potential for the periodic table》**（M3GNet）
   - 作者：C. Chen, S. P. Ong
   - 期刊：*Nature Computational Science* 2 (2022). DOI: 10.1038/s43588-022-00349-3
   - 来源：[arXiv:2202.02450](https://arxiv.org/abs/2202.02450)｜[Nature 文章页](https://www.nature.com/articles/s43588-022-00349-3)
   - 方法：覆盖全元素周期表的通用图深度学习原子间势
   - 关键成果：对 **3100 万个假想晶体结构**做稳定性筛选，得到 **180 万个潜在稳定结构**；对排名前 2000 的结构做 DFT 验证，**1578 个被确认为稳定**（≈79%）

---

### 6. 西北大学（Northwestern）— Chris Wolverton（克里斯·沃尔弗顿）

**机构与 PI**：西北大学材料科学与工程系教授；Open Quantum Materials Database（OQMD）负责人。

**成分优化方向**：无约束成分空间的 ML 筛选、失败实验数据利用、尺度不变 GNN 筛选四元硫族化物、金属玻璃成分设计。

**代表论文**：

1. **《Combinatorial screening for new materials in unconstrained composition space with machine learning》**（奠基性）
   - 作者：B. Meredig, A. Agrawal, S. Kirklin, J. E. Saal, J. W. Doak, A. Thompson, H. Zhang, A. Chasnow, C. Wolverton
   - 期刊：*Physical Review B* 89, 094104 (2014)
   - 来源：[APS](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.89.094104)（引用信息经检索核实）
   - 方法：DFT 数据训练梯度提升树，在无约束成分空间外推预测新化合物
   - 关键成果：首次系统演示"ML 在训练集成分空间之外发现新化合物"

2. **《Machine-learning-assisted materials discovery using failed experiments》**
   - 作者：P. Raccuglia 等（含 S. A. Friedler、C. Wolverton）
   - 期刊：*Nature* 533(7601), 73–76 (2016). DOI: 10.1038/nature17439
   - 来源：[Nature 文章页](https://www.nature.com/articles/nature17439)
   - 方法：以"失败"（未结晶）的水热合成实验数据训练 ML，预测新化合物的可合成性与成分
   - 关键成果：模型指导合成出新的结晶化合物，证明负样本数据的价值

3. **《Accelerated discovery of metallic glasses through iteration of machine learning and high-throughput experiments》**
   - 作者：F. Ren, L. Ward, T. Williams, K. J. Laws, C. Wolverton, J. Hattrick-Simpers, A. Mehta（SLAC/Northwestern/NIST/UNSW 合作；注意：作者列表中无 Schroers，见第 14 节更正说明）
   - 期刊：*Science Advances* 4(4), eaaq1566 (2018). DOI: 10.1126/sciadv.aaq1566
   - 来源：[PMC 全文（含完整作者列表）](https://pmc.ncbi.nlm.nih.gov/articles/PMC5898831/)
   - 方法：ML 模型（历史数据 + 物理化学理论参数 + 合成方法相关性）+ 高通量共溅射实验迭代闭环
   - 关键成果：在 **Co–V–Zr 三元体系**中发现新的金属玻璃（赝二元玻璃形成带）；后续迭代扩展至 Co–Ti–Zr、Co–Fe–Zr、Fe–Ti–Nb 三个新三元体系

4. **《Scale-invariant machine-learning model accelerates the discovery of quaternary chalcogenides with ultralow lattice thermal conductivity》**
   - 作者：西北大学 Wolverton 组
   - 期刊：*npj Computational Materials* 8, 48 (2022). DOI: 10.1038/s41524-022-00732-8
   - 来源：[Nature 文章页](https://www.nature.com/articles/s41524-022-00732-8)
   - 方法：尺度不变（成分归一化）的 CGCNN 类图神经网络
   - 关键成果：加速发现具有超低晶格热导率的四元硫族化物（热电/隔热候选）

**备注**：OQMD 数据库现收录 **1,407,395+** 个材料条目（[oqmd.org](http://www.oqmd.org)）；Citrine Informatics（Meredig、Saal、Ward 等创办）亦源于该生态。

---

### 7. 西北大学（Northwestern）— Wei Chen（陈伟，音译待核实）

**机构与 PI**：西北大学机械工程系教授（设计优化 + ML）。

**成分优化方向**：高熵合金成分设计的深度集合（Deep Sets）学习。

**代表论文**：

1. **《Composition design of high-entropy alloys with deep sets learning》**
   - 作者：J. Zhang, J. Cai, G. Kim, Y. Wang, W. Chen
   - 期刊：*npj Computational Materials* 8, 89 (2022). DOI: 10.1038/s41524-022-00779-7
   - 来源：[Nature 文章页](https://www.nature.com/articles/s41524-022-00779-7)
   - 方法：Deep Sets 神经网络（置换不变，天然适配成分向量）+ 关联规则挖掘
   - 关键成果：在多主元合金成分空间中比传统描述符模型具有更好的泛化能力，指导高熵合金成分设计

---

### 8. 杜克大学（Duke）— Stefano Curtarolo（斯特凡诺·库塔罗洛）

**机构与 PI**：杜克大学机械工程与材料科学系教授；AFLOW 生态系统与 Duke 材料极端性能中心负责人。

**成分优化方向**：熵描述符/DEED 描述符驱动的高熵陶瓷发现；贝叶斯主动学习自主闭环（CAMEO）；合金 ML。

**代表论文**：

1. **《High-entropy high-hardness metal carbides discovered by entropy descriptors》**
   - 作者：P. Sarker 等（Duke/UCSD 合作）
   - 期刊：*Nature Communications* 9, 4980 (2018). DOI: 10.1038/s41467-018-07160-7
   - 来源：[Nature 文章页](https://www.nature.com/articles/s41467-018-07160-7)
   - 方法：熵描述符（构型熵）+ ML 分类
   - 关键成果：发现高硬度单相高熵碳化物（岩盐结构），实验验证

2. **《Discovery of high-entropy ceramics via machine learning》**
   - 作者：K. Kaufmann 等
   - 期刊：*npj Computational Materials* 6, 42 (2020). DOI: 10.1038/s41524-020-0317-6
   - 来源：[Nature 文章页](https://www.nature.com/articles/s41524-020-0317-6)
   - 方法：ML 分类（决策树系）预测高熵氧化物形成
   - 关键成果：实验验证多个新的单相高熵陶瓷（萤石/钙钛矿等）

3. **《On-the-fly closed-loop materials discovery via Bayesian active learning》**（CAMEO）
   - 作者：A. G. Kusne 等（合作者含 J. Hattrick-Simpers、S. Curtarolo、A. Mehta、I. Takeuchi；NIST/UMD 等）
   - 期刊：*Nature Communications* 11, 5966 (2020). DOI: 10.1038/s41467-020-19597-w
   - 来源：[Nature 文章页](https://www.nature.com/articles/s41467-020-19597-w)｜[NIST 新闻](https://www.nist.gov/news-events/news/2020/11/nist-ai-system-discovers-new-material)
   - 方法：CAMEO 自主实验系统——贝叶斯主动学习 + 自主 XRD/合成表征闭环（无需人工干预）
   - 关键成果：在 **Ge–Sb–Te 三元体系**中自主识别出用于光子开关器件的最优相变存储（PCM）材料

4. **《Disordered enthalpy–entropy descriptor for high-entropy ceramics discovery》**（DEED）
   - 作者：S. Divilov 等
   - 期刊：*Nature* 625, 66–73 (2024). DOI: 10.1038/s41586-023-06786-y
   - 来源：[Nature 文章页](https://www.nature.com/articles/s41586-023-06786-y)
   - 方法：无序焓–熵描述符（DEED），判别多组元陶瓷的功能可合成性
   - 关键成果：在碳化物、硼化物、氮化物等多类高熵陶瓷中实现单相/复相判别与发现

5. **《Machine learning for alloys》**（综述）
   - 作者：G. L. W. Hart, T. Mueller, C. Toher, S. Curtarolo
   - 期刊：*Nature Reviews Materials* 6(8), 730–755 (2021). DOI: 10.1038/s41578-021-00340-w
   - 来源：[Nature 文章页](https://www.nature.com/articles/s41578-021-00340-w)（DOI 据 ResearchGate/Duke Scholars 核实）
   - 方法/成果：合金成分-组织-性能 ML 建模的系统性综述

6. **《aflow.org: A web ecosystem of databases, software and tools》**
   - 作者：M. Esters 等
   - 期刊：*Computational Materials Science* 216, 111808 (2023)（DOI 待核实）
   - 来源：[ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0927025622005195)｜[arXiv:2207.09842](https://arxiv.org/abs/2207.09842)
   - 方法/成果：AFLOW 数据库与工具生态（成分筛选的数据底座之一）

---

### 9. 马里兰大学（UMD）— Ichiro Takeuchi（竹内一郎）

**机构与 PI**：马里兰大学材料科学与工程系教授；组合材料学（combinatorial materials）先驱。

**成分优化方向**：高通量组合薄膜合成 + 闭环主动学习（CAMEO 的实验侧共同负责人）；日本自驱动实验室网络的参与者。

**代表论文**：

1. **《On-the-fly closed-loop materials discovery via Bayesian active learning》**（CAMEO，与 Curtarolo、Mehta、Hattrick-Simpers 等合作）
   - 期刊：*Nature Communications* 11, 5966 (2020). DOI: 10.1038/s41467-020-19597-w
   - 来源：[Nature 文章页](https://www.nature.com/articles/s41467-020-19597-w)
   - 方法/成果：见上（Curtarolo 节）；Takeuchi 为共同通讯作者，负责自主实验平台

2. **《Self-driving laboratories in Japan》**（合作综述）
   - 作者：N. Yoshikawa, …, I. Takeuchi, R. Tamura, K. Tsuda, Y. Ushiku 等
   - 期刊：*Digital Discovery* 4, 1384–1403 (2025). DOI: 10.1039/D4DD00387J
   - 来源：[RSC](https://pubs.rsc.org/en/content/articlelanding/2025/dd/d4dd00387j)
   - 方法/成果：日本自驱动实验室（SDL）全景综述

---

### 10. 洛斯阿拉莫斯国家实验室（LANL，前）— Turab Lookman（图拉布·卢克曼）

**机构与 PI**：曾任 LANL（洛斯阿拉莫斯国家实验室）科学家；现况：已离开 LANL（[美国司法部新闻稿](https://www.justice.gov/usao-nm/pr/former-employee-los-alamos-national-laboratory-sentenced-probation-making-false)称其为"前 LANL 雇员"，2020 年 9 月宣判）。其学术贡献（主动学习加速材料发现）仍是该领域基石。

**成分优化方向**：主动学习/自适应采样驱动的成分空间搜索（形状记忆合金、压电、铁电等）。

**代表论文**：

1. **《Accelerated search for materials with targeted properties by adaptive design》**（奠基性；部分引用列表作 "Accelerated search for new materials with targeted properties by active learning"，标题以 PNAS 官方页面为准，待核实）
   - 作者：D. Xue, P. V. Balachandran, R. Yuan, …, T. Lookman
   - 期刊：*PNAS* 113(47), 13301–13306 (2016). DOI: 10.1073/pnas.1607412113
   - 来源：[Objective-UQ 论文列表](https://objectiveuq.org/papers/)｜[引用 PDF](https://kjc.ecust.edu.cn/_upload/article/files/33/49/f673dfa54421b7819b8b14e3b482/46ded20f-c1a9-4b4a-9abf-df5f42e0a93d.pdf)
   - 方法：自适应设计闭环（ML 代理模型 + 期望改进类采集函数 + 实验）
   - 关键成果：以多组元 NiTi 基形状记忆合金的低热滞为目标，用远少于穷举的实验次数发现新材料

2. **《Active learning in materials science with emphasis on adaptive sampling using uncertainties for targeted design》**（综述）
   - 作者：T. Lookman 等
   - 期刊：*npj Computational Materials* 5, 21 (2019). DOI: 10.1038/s41524-019-0153-8
   - 来源：[ADS](http://ui.adsabs.harvard.edu/abs/2019npjCM...5...21L/abstract)
   - 方法/成果：主动学习/自适应采样在材料发现中的权威综述（被引约 973 次，据 ADS/Google Scholar）

---

### 11. 卡内基梅隆大学（CMU）→ Meta FAIR — Zack Ulissi（扎克·乌利西）

**机构与 PI**：现任 Meta FAIR AI 研究总监（Director of AI Research）；CMU 化学工程系兼职教授（[个人主页](https://zulissi.github.io/)）。

**成分优化方向**：电催化剂成分（金属间化合物/合金表面）的主动学习筛选；大规模催化数据集。

**代表论文**：

1. **《Active learning across intermetallics to guide discovery of electrocatalysts for CO2 reduction and H2 evolution》**
   - 作者：K. Tran, Z. W. Ulissi
   - 期刊：*Nature Catalysis* 1, 660–668 (2018). DOI: 10.1038/s41929-018-0142-1
   - 来源：[ResearchGate（含 DOI）](https://www.researchgate.net/publication/327603917_Active_learning_across_intermetallics_to_guide_discovery_of_electrocatalysts_for_CO2_reduction_and_H2_evolution)｜[OSTI](https://www.osti.gov/biblio/1543784)
   - 方法：主动学习（代理模型 + 采集函数）跨金属间化合物成分空间筛选
   - 关键成果：以远少于穷举 DFT 的计算量圈定 CO2RR/HER 催化剂候选成分

2. **《The Open Catalyst 2020 (OC20) Dataset and Community Challenges》**
   - 作者：L. Chanussot 等（Meta AI + CMU 等，含 Z. W. Ulissi）
   - 期刊：arXiv:2010.09990 (2020)
   - 来源：[arXiv:2010.09990](https://arxiv.org/abs/2010.09990)
   - 方法：大规模 DFT 数据集 + 社区基准
   - 关键成果：**超过 120 万次**分子吸附-表面弛豫 DFT 计算，成为吸附催化剂成分/表面筛选的标准数据底座

---

### 12. 卡内基梅隆大学（CMU）— Gabriel dos Passos Gomes / Carla Gomes（Coscientist）

**机构与 PI**：CMU 化学系（Gomes 组，COSMOS 中心）。

**成分优化方向**：LLM 智能体自主化学研究（含钯催化偶联反应条件/成分优化）。

**代表论文**：

1. **《Autonomous chemical research with large language models》**（Coscientist）
   - 作者：D. A. Boiko, R. MacKnight, B. Kline, G. dos Passos Gomes
   - 期刊：*Nature* 624(7992), 570–578 (2023). DOI: 10.1038/s41586-023-06792-0
   - 来源：[Nature 文章页](https://www.nature.com/articles/s41586-023-06792-0)｜[PubMed](https://pubmed.ncbi.nlm.nih.gov/38123806/)
   - 方法：GPT-4 驱动的 LLM 智能体（网络/文档/代码工具调用）自主设计-执行-分析实验
   - 关键成果：自主规划并完成钯催化偶联反应的实验设计与优化，展示 LLM 智能体在实验科学中的闭环能力

---

### 13. 斯坦福大学（Stanford）— Evan J. Reed（埃文·J·里德）

**机构与 PI**：斯坦福大学材料科学与工程系教授。

**成分优化方向**：固态锂离子导体成分的 ML 筛选（迁移学习应对小数据）。

**代表论文**：

1. **《Machine Learning-Assisted Discovery of Solid Li-Ion Conducting Materials》**
   - 作者：A. D. Sendek 等（含 Y. Cui、E. J. Reed）
   - 期刊：*Chemistry of Materials* 31(8), 3449–3457 (2019)
   - 来源：[斯坦福 PDF](https://web.stanford.edu/group/cui_group/papers/Austin_Cui_Reed_CHEMMATER_2019.pdf)
   - 方法：ML 分类器引导 DFT 筛选（其 2017 年前序工作已对 12,000+ 种含锂候选做过整体计算筛选）
   - 关键成果：发现多种室温快离子导体候选，并经 DFT 验证其超离子传导

2. **《Screening billions of candidates for solid lithium-ion conductors: A transfer learning approach for small data》**
   - 作者：E. D. Cubuk, A. D. Sendek, E. J. Reed
   - 期刊：*Journal of Chemical Physics* 150(21), 214701 (2019)
   - 来源：[PubMed](https://pubmed.ncbi.nlm.nih.gov/31176329/)｜[Reed 组页面](https://reedgroup.stanford.edu/staff/asendek2.html)
   - 方法：迁移学习（大数据预训练 → 小数据微调）
   - 关键成果：将筛选范围扩展到**数十亿**候选成分，识别出新的固态锂离子导体候选

---

### 14. 耶鲁大学（Yale）— Jan Schroers（扬·施罗尔斯）

**机构与 PI**：耶鲁大学机械工程与材料科学系教授（2023 年任 Robert Higgin 讲席教授，[院系新闻](https://seas.yale.edu/news-events/news/jan-schroers-appointed-robert-higgin-professor-mechanical-engineering)）。

**成分优化方向**：金属玻璃（块体非晶合金）成分设计；玻璃形成能力（GFA）的 ML 预测与描述符。

**代表论文**：

1. **《Machine learning versus human learning in predicting glass-forming ability of metallic glasses》**
   - 作者：G. Liu, S. Sohn, C. S. O'Hern, A. C. Gilbert, J. Schroers
   - 期刊：*Acta Materialia* 243, 118497 (2023)
   - 来源：[Schroers 组出版物页](https://schroerslab.com/publications)｜[Yale 论文 PDF](https://jamming.research.yale.edu/files/papers/human.pdf)
   - 方法：ML 模型与人类专家在玻璃形成能力（GFA）预测上的系统对比
   - 关键成果：量化 ML 与人类直觉的互补性与局限（玻璃成分 GFA 预测"需要人类帮助"），指导金属玻璃成分筛选策略

2. **《Soliquidy: a descriptor for atomic geometrical confusion》**
   - 作者：H. Eckert, S. A. Kube, S. Divilov, A. Guest, A. C. Zettel, D. Hicks, …, S. Curtarolo, J. Schroers（列于 Schroers 组出版物 #267）
   - 期刊：*npj Computational Materials* 11, 40 (2025)
   - 来源：[Nature 文章页](https://www.nature.com/articles/s41524-025-01529-1)｜[Schroers 组出版物页](https://schroerslab.com/publications)
   - 方法：原子几何"混乱度"描述符（soliquidy）
   - 关键成果：以描述符判别玻璃形成倾向，服务于金属玻璃成分的理性设计（Duke Curtarolo 组合作）

**更正说明**：部分综述与任务清单常把 Ren 等 *Science Advances* 4, eaaq1566 (2018)（ML+高通量实验发现 Co–V–Zr 等新金属玻璃）归于 Schroers 名下；经 PMC 作者列表核实，**该文作者为 F. Ren、L. Ward、T. Williams、K. J. Laws、C. Wolverton、J. Hattrick-Simpers、A. Mehta，不含 Schroers**（应归属 SLAC/Stanford、Northwestern、NIST、UNSW 团队，详见第 6 节）。金属玻璃 ML 方向与 Schroers 生态密切相关（其合作者 K. J. Laws、Curtarolo 等参与该文）。

---

### 15. 佐治亚理工学院（Georgia Tech）— Rampi Ramprasad（兰皮·拉姆普拉萨德）

**机构与 PI**：佐治亚理工材料科学与工程系教授（前 GE 全球研究科学家）；聚合物信息学（Polymer Genome）创始人。

**成分优化方向**：聚合物重复单元（化学成分）信息学；AI 辅助高温介电材料发现。

**代表论文**：

1. **《Polymer Genome: A Data-Powered Polymer Informatics Platform for Property Predictions》**
   - 作者：C. Kim 等
   - 期刊：*Journal of Physical Chemistry C* 122(31), 17575–17601 (2018)
   - 来源：[ACS](https://pubs.acs.org/jpccck/article/122/31/17575/1470511/Polymer-Genome-A-Data-Powered-Polymer-Informatics)
   - 方法：聚合物描述符 + 多性质回归模型 + 在线平台
   - 关键成果：Polymer Genome 平台成为聚合物成分-性质设计的标准工具

2. **《Polymer informatics with multi-task learning》**
   - 作者：C. Kuenneth, R. Ramprasad
   - 期刊：*Patterns* 2(4), 100238 (2021)
   - 来源：[PubMed](https://pubmed.ncbi.nlm.nih.gov/33982028/)｜[ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2666389921000581)
   - 方法：多任务学习同时预测多种聚合物性质
   - 关键成果：实现多性质联合建模，提升小数据场景下的泛化能力

3. **《AI-assisted discovery of high-temperature dielectrics for energy storage》**
   - 作者：R. Gurnani, …, R. Ramprasad
   - 期刊：*Nature Communications* 15, 6107 (2024). DOI: 10.1038/s41467-024-50413-x
   - 来源：[Nature 文章页](https://www.nature.com/articles/s41467-024-50413-x)
   - 方法：AI（Polymer Genome 类模型）+ 既有聚合物化学知识 + 分子工程，人机协同闭环
   - 关键成果：发现一组高温介电储能聚合物材料并实验验证

---

### 16. 弗吉尼亚大学（UVA）— Prasanna V. Balachandran（普拉桑纳·V·巴拉昌德兰）

**机构与 PI**：弗吉尼亚大学材料科学与工程系/机械与航空航天工程系副教授（Lookman 学派）。

**成分优化方向**：多主元合金（MPEA）相结构的可解释 ML 预测。

**代表论文**：

1. **《Phase classification of multi-principal element alloys via interpretable machine learning》**
   - 作者：K. Lee 等
   - 期刊：*npj Computational Materials* 8, 25 (2022). DOI: 10.1038/s41524-022-00704-y
   - 来源：[Nature 文章页](https://www.nature.com/articles/s41524-022-00704-y)｜[PMC 引用](https://pmc.ncbi.nlm.nih.gov/articles/PMC9270422/)
   - 方法：可解释 ML（树模型与特征归因分析）
   - 关键成果：对多主元合金的相（单相固溶体 vs. 混合相）做高精度分类，给出物理可解释的判据

---

### 17. 北卡罗来纳州立大学（NC State）— Milad Abolhasani（米拉德·阿博尔哈萨尼）

**机构与 PI**：北卡州立大学化学与生物分子工程系教授。

**成分优化方向**：自驱动微流控平台对纳米材料成分的自主优化。

**代表论文**：

1. **《Artificial Chemist: An Autonomous Quantum Dot Synthesis Bot》**
   - 作者：R. W. Epps, …, M. Abolhasani
   - 期刊：*Advanced Materials* 32, 1901266 (2020)
   - 来源：[PubMed](https://pubmed.ncbi.nlm.nih.gov/32495399/)
   - 方法：流动化学机器人 + 自主闭环优化（"Artificial Chemist"）
   - 关键成果：自主合成"按需定制"的钙钛矿量子点并优化其量子产率（成分/前驱体比例的闭环优化）

---

### 18. 美国国家标准与技术研究院（NIST）— Kamal Choudhary（卡马尔·乔杜里）

**机构与 PI**：NIST 材料测量实验室（Material Measurement Laboratory）研究员。

**成分优化方向**：JARVIS 数据库/工具链；ALIGNN 图神经网络（成分/结构-性质建模的国家级基础设施）。

**代表论文**：

1. **《Atomistic Line Graph Neural Network for improved materials property predictions》**（ALIGNN）
   - 作者：K. Choudhary, B. DeCost
   - 期刊：*npj Computational Materials* 7, 185 (2021). DOI: 10.1038/s41524-021-00650-1
   - 来源：[Nature 文章页](https://www.nature.com/articles/s41524-021-00650-1)｜[NIST 复现性研究](https://www.nist.gov/publications/reproducibility-study-graph-neural-networks-materials-property-prediction)
   - 方法：原子图 + 键连线图（line graph）双层 GNN
   - 关键成果：在 JARVIS 数据库的数十种材料性质基准上刷新纪录，成为成分/结构-性质建模的标准模型

2. **《The joint automated repository for various integrated simulations (JARVIS) for data-driven materials design》**
   - 作者：K. Choudhary 等
   - 期刊：*npj Computational Materials* 6, 173 (2020). DOI: 10.1038/s41524-020-00440-1
   - 来源：[Nature 文章页](https://www.nature.com/articles/s41524-020-00440-1)｜[JARVIS 官网](https://jarvis.nist.gov)
   - 方法/成果：JARVIS 数据库（DFT/经典力场/ML 多层次数据）与工具生态

---

## 二、加拿大

### 19. 多伦多大学（University of Toronto）— Alán Aspuru-Guzik（阿兰·阿斯普鲁-古齐克）

**机构与 PI**：多伦多大学化学系与计算机科学系教授；Matter Lab 主任；CIFAR AI 讲席教授（自驱动实验室方向代表人物）。

**成分优化方向**：自驱动实验室（SDL）软硬件与算法框架（含材料成分/分子优化）。

**代表论文**：

1. **《Self-Driving Laboratories for Chemistry and Materials Science》**
   - 作者：G. Tom, …, A. Aspuru-Guzik
   - 期刊：*Chemical Reviews* 124(16), 9633–9732 (2024). DOI: 10.1021/acs.chemrev.4c00055
   - 来源：[ACS](https://pubs.acs.org/doi/10.1021/acs.chemrev.4c00055)
   - 方法/成果：自驱动实验室（机器人 + 贝叶斯优化/主动学习 + 编排软件）在化学与材料（含成分优化）中的权威综述

**备注**：其 Matter Lab 亦开发了 ChemOS、去中心化 SDL 等基础设施（详见 [Matter Lab 官网](https://matter.toronto.edu/)，具体论文此处从略）。

---

## 三、欧洲

### 20. 德国马普可持续材料研究所（MPIE，原马普钢铁研究所）— Dierk Raabe（迪尔克·拉贝）& Ziyuan Rao（饶子源，音译待核实）

**机构与 PI**：Dierk Raabe，马普钢铁研究所（Max-Planck-Institut für Eisenforschung，2024 年更名为 **Max Planck Institute for Sustainable Materials**，杜塞尔多夫）所长。Ziyuan Rao 曾在 MPIE 设立并领导 "AI for Materials Science" 研究组（[MPIE 官网](https://www.mpie.de/4870481)）；ResearchGate 显示其现为上海交通大学副教授（待核实）。

**成分优化方向**：高熵合金/成分复杂材料（CCA）的主动学习闭环设计（ML + DFT + CALPHAD + 实验）；物理信息 AI（CM-Net）。

**代表论文**：

1. **《Machine learning-enabled high-entropy alloy discovery》**
   - 作者：Z. Rao, P.-Y. Tung, R. Xie, Y. Wei, H. Zhang, A. Ferrari, T. P. C. Klaver, F. Körmann, P. T. Sukumar, A. Kwiatkowski da Silva, Y. Chen, Z. Li, D. Ponge, J. Neugebauer, O. Gutfleisch, S. Bauer, D. Raabe
   - 期刊：*Science* 378(6615), 78–85 (2022). DOI: 10.1126/science.abo4940
   - 来源：[arXiv:2202.13753（含完整作者与摘要）](https://arxiv.org/abs/2202.13753)
   - 方法：主动学习闭环（ML 代理 + DFT + 热力学计算 + 合成/表征实验），在"近乎无限"的成分空间中搜索
   - 关键成果：从数百万候选成分中仅制备并表征 **17 个新合金**，即发现 **2 个高熵 Invar 合金**（300 K 下热膨胀系数约 2×10⁻⁶ K⁻¹）

2. **《Accelerating the design of compositionally complex materials via physics-informed artificial intelligence》**
   - 作者：Z. Rao 等（MPIE）
   - 期刊：*Nature Computational Science* 3(3), 198–209 (2023). DOI: 10.1038/s43588-023-00412-7
   - 来源：[Nature 文章页](https://www.nature.com/articles/s43588-023-00412-7)（DOI 据 Dierk Raabe 官网论文 PDF 核实）
   - 方法：物理信息神经网络（CM-Net，融合热力学/力学先验）
   - 关键成果：对成分复杂合金的力学性能做跨体系预测与设计加速

---

### 21. 德国柏林弗里茨·哈伯研究所（FHI Berlin）— Matthias Scheffler（马蒂亚斯·舍夫勒）

**机构与 PI**：柏林弗里茨·哈伯研究所（马普学会，Fritz-Haber-Institut der Max-Planck-Gesellschaft）理论系主任；NOMAD 实验室联合主任（与柏林洪堡大学 Claudia Draxl）；IR-Adlershof 主任。

**成分优化方向**：SISSO 符号回归描述符发现；NOMAD/FAIRmat 数据基础设施；AI 工具包（面向成分-性质关系的可解释建模）。

**代表论文**：

1. **《SISSO: A compressed-sensing method for identifying the best low-dimensional descriptors in an immensity of offered candidates》**
   - 作者：R. Ouyang, S. Curtarolo, E. Ahmetcik, M. Scheffler, L. M. Ghiringhelli
   - 期刊：*Physical Review Materials* 2, 083802 (2018). DOI: 10.1103/PhysRevMaterials.2.083802
   - 来源：[APS](https://journals.aps.org/prmaterials/abstract/10.1103/PhysRevMaterials.2.083802)（引用信息经检索核实）
   - 方法：压缩感知 + 符号回归，从海量候选描述符中筛选低维解析描述符
   - 关键成果：给出成分-性质的解析公式（可解释），成为"描述符工程"的代表方法

2. **《The NOMAD laboratory: from data sharing to artificial intelligence》**
   - 作者：C. Draxl, M. Scheffler
   - 期刊：*Journal of Physics: Materials* 2, 036001 (2019). DOI: 10.1088/2515-7639/ab13bb
   - 来源：[IOPscience](https://iopscience.iop.org/article/10.1088/2515-7639/ab13bb)（含 HU Berlin 镜像核实）
   - 方法/成果：NOMAD——全球最大第一性原理计算数据仓库 + AI 分析生态

3. **《The NOMAD Artificial-Intelligence Toolkit: turning materials-science data into knowledge and understanding》**
   - 作者：L. Sbailò 等（含 L. M. Ghiringhelli、M. Scheffler）
   - 期刊：*npj Computational Materials* 8, 250 (2022). DOI: 10.1038/s41524-022-00935-z
   - 来源：[Nature 文章页](https://www.nature.com/articles/s41524-022-00935-z)｜[arXiv:2205.15686](https://arxiv.org/abs/2205.15686)
   - 方法/成果：在线 AI 工具包（含 SISSO 等描述符发现工具），把数据变成成分-性质知识

---

### 22. 丹麦哥本哈根大学（KU）— Jan Rossmeisl（扬·罗斯梅斯尔）团队（Jack Kirk Pedersen、Vladislav A. Mints 等）

**机构与 PI**：哥本哈根大学化学系（Rossmeisl 现亦任职于瑞士伯尔尼大学，据 [伯尔尼大学机构库](https://boris-portal.unibe.ch/bitstreams/ddaa34e7-7b3d-40b3-9825-99f818ee315f/download)）；第一作者 Jack Kirk Pedersen、Vladislav A. Mints 等为 KU 团队成员。

**成分优化方向**：高熵合金电催化剂成分的贝叶斯优化（ORR、H2/CO 氧化）。

**代表论文**：

1. **《Bayesian Optimization of High-Entropy Alloy Compositions for Electrocatalytic Oxygen Reduction》**
   - 作者：J. K. Pedersen, C. M. Clausen, O. A. Krysiak, …（通讯含 Rossmeisl 团队）
   - 期刊：*Angewandte Chemie International Edition* 60(45), 24144–24152 (2021). DOI: 10.1002/anie.202108116
   - 来源：[Wiley](https://onlinelibrary.wiley.com/doi/abs/10.1002/anie.202108116)｜[伯尔尼大学 PDF](https://boris-portal.unibe.ch/bitstreams/ddaa34e7-7b3d-40b3-9825-99f818ee315f/download)
   - 方法：贝叶斯优化（DFT 计算作为目标函数）搜索高熵合金成分空间
   - 关键成果：在巨大的 HEA 成分空间中高效定位 ORR 活性最优成分（被引约 280 次，据 Wiley/Google Scholar）

2. **《Exploring the Composition Space of High-Entropy Alloy Nanoparticles for the Electrocatalytic H2/CO Oxidation with Bayesian Optimization》**
   - 作者：V. A. Mints, J. K. Pedersen, A. Bagger 等
   - 期刊：*ACS Catalysis* 12, 11263–11271 (2022)
   - 来源：[KU 研究门户（含页码）](https://researchprofiles.ku.dk/en/publications/exploring-the-composition-space-of-high-entropy-alloy-nanoparticl/)
   - 方法：贝叶斯优化 + DFT，探索 HEA 纳米粒子成分空间
   - 关键成果：为 H2/CO 氧化电催化定位高活性成分区域

**更正说明（重要）**：任务清单中提到的 "G. A. Sulley（哥本哈根大学，2024，Materials & Design）" 经核实存在两处出入：
- Sulley 等的 2024 年论文实际发表于 **Scripta Materialia**：G. A. Sulley, J. Raush, M. M. Montemore 等，《Accelerating high-entropy alloy discovery: efficient exploration via active learning》，*Scripta Materialia* 249, 116180 (2024)（[ScienceDirect](https://www.sciencedirect.com/science/article/pii/S135964622400215X)；DOI: 10.1016/j.scriptamat.2024.116180）。方法：主动学习 + 神经网络；关键成果：仅用 2198 个合金实验数据集约 **27%** 的样本即达到 **95%** 的预测精度。
- G. A. Sulley 的隶属机构为 **美国杜兰大学（Tulane University）**（Montemore 组），并非哥本哈根大学（[ResearchGate](https://www.researchgate.net/scientific-contributions/Gloria-A-Sulley-2221035080)）。"Materials & Design" 出处未检索到对应论文，待核实。

---

### 23. 英国剑桥大学（University of Cambridge）— Gareth Conduit（加雷斯·康迪特）

**机构与 PI**：剑桥大学材料科学与冶金系研究员/组长；同时为 Intellegens 公司研究总监（Alchemite 深度学习商业平台）。

**成分优化方向**：镍基高温合金等多目标成分设计（概率神经网络）；物理描述符建模。

**代表论文**：

1. **《Design of a nickel-base superalloy using a neural network》**
   - 作者：B. D. Conduit, N. G. Jones, H. J. Stone, G. J. Conduit
   - 期刊：*Materials & Design* 131, 358–365 (2017). DOI: 10.1016/j.matdes.2017.06.007
   - 来源：[ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0264127517305907)（DOI 据 Intellegens/剑桥引文核实）
   - 方法：概率神经网络（多性质联合建模 + 不确定性驱动采样）
   - 关键成果：设计出满足多目标（蠕变强度/密度/成本等）的新型镍基高温合金并实验验证

2. **《Machine learning superalloy microchemistry and creep strength from physical descriptors》**
   - 作者：P. L. Taylor, G. J. Conduit
   - 期刊：*Computational Materials Science* 227, 112265 (2023)
   - 来源：[ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0927025623002598)｜[Conduit 个人站 PDF](https://garethconduit.org/papers/TaylorConduit23.pdf)｜[Intellegens 说明页](https://intellegens.com/machine-learning-superalloy-microchemistry-and-creep-strength-from-physical-descriptors/)
   - 方法：物理描述符 + ML 回归
   - 关键成果：由成分预测高温合金微观化学与蠕变强度，支撑成分设计

**备注**：Intellegens/Alchemite 已将该方法用于工业合金成分优化（[Intellegens 官网](https://intellegens.com/)）。

---

### 24. 英国利物浦大学（University of Liverpool）— Andrew I. Cooper（安德鲁·I·库珀）

**机构与 PI**：利物浦大学化学系教授；材料创新工厂（Materials Innovation Factory）与 Leverhulme 功能材料发现研究中心主任。

**成分优化方向**：自主移动机器人化学家（机器人 + 贝叶斯优化闭环，用于光催化剂成分/条件优化）。

**代表论文**：

1. **《A mobile robotic chemist》**
   - 作者：B. Burger, P. M. Maffettone 等（A. I. Cooper 组）
   - 期刊：*Nature* 583(7815), 237–241 (2020). DOI: 10.1038/s41586-020-2442-2
   - 来源：[PubMed](https://pubmed.ncbi.nlm.nih.gov/32641813/)｜[斯特拉斯克莱德大学 PDF](https://strathprints.strath.ac.uk/74759/1/Burger_etal_Nature_2020_A_mobile_robotic.pdf)
   - 方法：1.75 m 高自主移动机器人 + 批量贝叶斯搜索
   - 关键成果：**8 天内自主完成 688 个实验**（10 变量实验空间），发现活性提升的光催化剂配方

2. **《Autonomous mobile robots for exploratory synthetic chemistry》**
   - 作者：T. Dai 等（Leverhulme 研究中心/Cooper 团队）
   - 期刊：*Nature* 635(8040), 890–897 (2024). DOI: 10.1038/s41586-024-08173-7
   - 来源：[PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11602721/)｜[ResearchGate（含卷期页码）](https://www.researchgate.net/publication/385592709_Autonomous_mobile_robots_for_exploratory_synthetic_chemistry)
   - 方法：多移动机器人协作 + LLM 辅助任务编排（自主探索性合成）
   - 关键成果：机器人团队自主完成探索性合成化学任务（含反应/条件优化）

---

### 25. 瑞士洛桑联邦理工学院（EPFL）— 备注（诚实说明）

在本轮检索（2019–2025，成分优化方向）中，未找到 EPFL 专门的"元素成分优化"旗舰课题组或代表论文。EPFL 相关的活跃方向为：
- **COSMO 实验室（Michele Ceriotti 教授）**：机器学习力场、原子尺度模拟与不确定性量化（偏结构/模拟，非成分优化）；
- **NCCR MARVEL**（Marzari 主持的国家级计算材料生态）：高通量筛选与数据基础设施。

若需锁定 EPFL 的成分优化具体工作，建议进一步核实（**待核实**）。

---

## 四、企业实验室

### 26. Google DeepMind（英国伦敦）— GNoME 团队

**机构与 PI**：Google DeepMind；第一作者 Amil Merchant（阿米尔·默钱特，音译），资深作者 Ekin Dogus Cubuk（埃金·多乌斯·楚丘克，音译）等。

**成分优化方向**：图网络 + 主动学习的大规模晶体（成分+结构）发现。

**代表论文**：

1. **《Scaling deep learning for materials discovery》**（GNoME）
   - 作者：A. Merchant 等（资深作者 Ekin Dogus Cubuk）
   - 期刊：*Nature* 624(7990), 80–85 (2023). DOI: 10.1038/s41586-023-06735-9
   - 来源：[Nature 文章页](https://www.nature.com/articles/s41586-023-06735-9)｜[DeepMind 博客](https://deepmind.google/blog/millions-of-new-materials-discovered-with-deep-learning/)
   - 方法：图网络（GNoME）+ 主动学习管线（模型筛选 → DFT 验证 → 数据回流）
   - 关键成果：预测 **220 万个新晶体结构**，其中约 **38 万个**为热力学稳定候选；DeepMind 称其相当于近 **800 年**"知识当量"的发现量

---

### 27. 微软研究院（Microsoft Research）AI4Science — MatterGen / MatterSim 团队

**机构与 PI**：Microsoft Research AI4Science（剑桥/雷德蒙德）；MatterGen 第一作者 Claudio Zeni（克劳迪奥·泽尼），MatterSim 第一作者 Han Yang 等。

**成分优化方向**：无机材料的扩散生成模型（按目标性质生成新成分+结构）；跨元素/温度/压力的通用机器学习势。

**代表论文**：

1. **《A generative model for inorganic materials design》**（MatterGen）
   - 作者：C. Zeni, R. Pinsler 等（Microsoft Research AI4Science）
   - 期刊：*Nature* 639(8055), 624–632 (2025). DOI: 10.1038/s41586-025-08628-5
   - 来源：[Nature 文章页](https://www.nature.com/articles/s41586-025-08628-5)｜[Microsoft 出版页](https://www.microsoft.com/en-us/research/publication/mattergen-a-generative-model-for-inorganic-materials-design/)
   - 方法：扩散生成模型（对周期性结构的成分、晶格、坐标联合去噪）+ 针对目标性质/化学/对称度的微调
   - 关键成果：微调后可生成满足目标化学成分、空间群与力学/电子/磁学性质的新稳定材料；据 Nature 文章：生成结构"新颖且稳定"的可能性约为以往生成方法的 **2 倍以上**，且比以往方法**高 10 倍以上**接近局部能量极小（[Nature 参考文献 PDF](https://www.nature.com/articles/s41586-025-08628-5_reference.pdf)）

2. **《MatterSim: A Deep Learning Atomistic Model Across Elements, Temperatures and Pressures》**
   - 作者：H. Yang 等（Microsoft Research AI4Science）
   - 期刊：arXiv:2405.04967 (2024)（截至检索时仍为预印本）
   - 来源：[arXiv:2405.04967](https://arxiv.org/abs/2405.04967)
   - 方法：深度学习原子间势（主动学习生成第一性原理训练数据 + 微调）
   - 关键成果：覆盖 **0–5000 K、最高 1000 GPa**；Gibbs 自由能预测精度达 **15 meV/atom**（≤1000 K，对比实验数据），据 arXiv 摘要

---

## 五、日本

### 28. RIKEN CEMS / 东京大学 / NIMS — 津田研一（Koji Tsuda，つだ けんいち）生态圈

**机构与 PI**：
- **津田研一（Koji Tsuda）**：东京大学大学院新领域创成科学研究科教授，同时任职于 RIKEN（[津田实验室](https://www.tsudalab.org/en/)）。
- **田村亮（Ryo Tamura，たむら りょう）**：NIMS / RIKEN（[个人论文列表](https://www.nims.go.jp/group/da/ryo_tamura/tamura_original_papers_e.html)）。
- **侯柱峰（Zhufeng Hou，音译待核实）**：磁热材料 ML 工作完成于 RIKEN CEMS 时期；ResearchGate 显示现隶属中国科学院（待核实）。
- **上野刚志（Tsuyoshi Ueno，音译待核实）**：东京大学（津田组），COMBO/PHYSBO 贝叶斯优化库作者。

**成分优化方向**：贝叶斯优化库（COMBO/PHYSBO）、晶体结构预测加速（LAQA）、偏好学习数据整合、磁热材料 ML 指导发现、相图构建 ML、自驱动实验室软件（NIMS-OS）、LLM 相图预测（aLLoyM）。

**代表论文**（均经田村亮论文列表/期刊页核实）：

1. **《Fine-grained optimization method for crystal structure prediction》**（LAQA）
   - 作者：K. Terayama, T. Yamashita, T. Oguchi, K. Tsuda
   - 期刊：*npj Computational Materials* 4, 32 (2018). DOI: 10.1038/s41524-018-0090-y
   - 来源：[寺山圭个人主页（含卷号与 DOI）](https://sites.google.com/site/terayamaweb/index_e)｜[津田实验室](https://www.tsudalab.org/en/publication/2018-terayama-finegrained/)
   - 方法：LAQA——对每个候选结构维护局部质量估计，替代全局随机采样
   - 关键成果：大幅减少晶体结构预测所需的第一性原理弛豫次数

2. **《COMBO: An efficient Bayesian optimization library for materials science》**
   - 作者：T. Ueno, T. D. Rhone, Z. Hou, T. Mizoguchi, K. Tsuda
   - 期刊：*Materials Discovery* 4 (2016)
   - 来源：[ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2352924516300035)｜[津田实验室](https://www.tsudalab.org/en/publication/2016-ueno-combo/)
   - 方法：Thompson 采样 + 随机特征图 + Cholesky 更新的高效 BO 库
   - 关键成果：材料科学 BO 的标准开源工具之一（被引约 446 次，据 ScienceDirect/Google Scholar）

3. **《Bayesian optimization package: PHYSBO》**
   - 作者：Y. Motoyama, R. Tamura, K. Yoshimi, K. Terayama, T. Ueno, K. Tsuda
   - 期刊：*Computer Physics Communications* 278, 108405 (2022). DOI: 10.1016/j.cpc.2022.108405
   - 来源：[Elsevier](https://doi.org/10.1016/j.cpc.2022.108405)
   - 方法/成果：COMBO 的后继 BO 库（面向物理/材料，支持并行/批量 BO）

4. **《Data Integration for Accelerated Materials Design via Preference Learning》**
   - 作者：X. Sun, Z. Hou, M. Sumita, S. Ishihara, R. Tamura, K. Tsuda
   - 期刊：*New Journal of Physics* 22, 055001 (2020). DOI: 10.1088/1367-2630/ab82b9
   - 来源：[IOPscience](https://iopscience.iop.org/article/10.1088/1367-2630/ab82b9)
   - 方法：偏好学习（preference learning）整合多源数据（实验/计算/文献）
   - 关键成果：以磁热材料为演示，把分散数据整合为统一的成分-性质排序模型

5. **《Machine Learning Guided Discovery of Gigantic Magnetocaloric Effect in HoB2 Near Hydrogen Liquefaction Temperature》**
   - 作者：P. B. de Castro, K. Terashima, T. D. Yamamoto, Z. Hou 等
   - 期刊：*NPG Asia Materials* 12, 35 (2020). DOI: 10.1038/s41427-020-0214-y
   - 来源：[Nature 文章页](https://www.nature.com/articles/s41427-020-0214-y)
   - 方法：ML 指导的磁热材料成分筛选（侯柱峰负责 ML 部分）
   - 关键成果：发现 HoB2 在 15 K（近氢液化温度）呈现巨磁热效应，**ΔS = 40.1 J kg⁻¹ K⁻¹（5 T）**

6. **《Optimization of Heterogeneous Ternary Li3PO4-Li3BO3-Li2SO4 Mixture for Li-ion Conductivity by Machine Learning》**
   - 作者：K. Homma, Y. Liu, M. Sumita, R. Tamura, N. Fushimi, J. Iwata, K. Tsuda, C. Kaneta
   - 期刊：*The Journal of Physical Chemistry C* 124(24), 12865–12870 (2020). DOI: 10.1021/acs.jpcc.9b11654
   - 来源：[ACS](https://pubs.acs.org/doi/10.1021/acs.jpcc.9b11654)
   - 方法：ML + 实验（三组分混合比例优化）
   - 关键成果：优化 Li3PO4–Li3BO3–Li2SO4 三元异质混合物的锂离子电导率

7. **《Pushing property limits in materials discovery via boundless objective-free exploration》**（BLOX）
   - 作者：K. Terayama, M. Sumita, R. Tamura, D. T. Payne, M. K. Chahal, S. Ishihara, K. Tsuda
   - 期刊：*Chemical Science* 11(23), 5959–5968 (2020). DOI: 10.1039/d0sc00982b
   - 来源：[RSC](https://pubs.rsc.org/en/content/articlelanding/2020/SC/d0sc00982b)
   - 方法：无目标（objective-free）探索 + 逆强化学习式偏好
   - 关键成果：在无预设目标函数的情况下突破材料性质边界（发现性质极限附近的新材料）

8. **《Acceleration of phase diagram construction by machine learning incorporating Gibbs' phase rule》**
   - 作者：K. Terayama, K. Han, R. Katsube, I. Ohnuma, T. Abe, Y. Nose, R. Tamura
   - 期刊：*Scripta Materialia* 208, 114335 (2022). DOI: 10.1016/j.scriptamat.2021.114335
   - 来源：[ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1359646221006151)
   - 方法：ML + 吉布斯相律约束的相图构建
   - 关键成果：以更少实验点构建可靠相图（成分设计的基础设施）

9. **《A framework to predict binary liquidus by combining machine learning and CALPHAD assessments》**
   - 作者：G. Deffrennes, K. Terayama, T. Abe, E. Ogamino, R. Tamura
   - 期刊：*Materials & Design* 232, 112111 (2023). DOI: 10.1016/j.matdes.2023.112111
   - 来源：[ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0264127523005269)
   - 方法：ML + CALPHAD 评估数据融合
   - 关键成果：预测二元液相线（成分-温度关系），弥补 CALPHAD 数据缺口

10. **《NIMS-OS: An automation software to implement a closed loop between artificial intelligence and robotic experiments in materials science》**
    - 作者：R. Tamura, K. Tsuda, S. Matsuda
    - 期刊：*Science and Technology of Advanced Materials: Methods* 3, 2232297 (2023). DOI: 10.1080/27660400.2023.2232297
    - 来源：[Taylor & Francis](https://www.tandfonline.com/doi/full/10.1080/27660400.2023.2232297)
    - 方法/成果：NIMS-OS——把 AI（BO 等）与机器人实验闭环编排的开源软件（自驱动实验室操作系统）

11. **《AIPHAD, an active learning web application for visual understanding of phase diagrams》**
    - 作者：R. Tamura, H. Morito, G. Deffrennes, M. Naito, Y. Nose, T. Abe, K. Terayama
    - 期刊：*Communications Materials* 5, 139 (2024). DOI: 10.1038/s43246-024-00580-7
    - 来源：[Nature 文章页](https://www.nature.com/articles/s43246-024-00580-7)
    - 方法：主动学习 + 可视化相图构建 Web 应用
    - 关键成果：以主动学习减少相图测定所需实验量

12. **《Autonomous closed-loop exploration of composition-spread films for the anomalous Hall effect》**
    - 作者：R. Toyama, R. Tamura, S. Matsuda, Y. Iwasaki, Y. Sakuraba
    - 期刊：*npj Computational Materials* 11, 329 (2025). DOI: 10.1038/s41524-025-01828-7
    - 来源：[Nature 文章页](https://www.nature.com/articles/s41524-025-01828-7)
    - 方法：自主闭环（AI + 成分展宽薄膜高通量实验）
    - 关键成果：自主探索反常霍尔效应最优成分

13. **《Self-driving laboratories in Japan》**
    - 作者：N. Yoshikawa, Y. Asano, D. N. Futaba, K. Harada, T. Hitosugi, G. N. Kanda, S. Matsuda, …, I. Takeuchi, R. Tamura, K. Tsuda, Y. Ushiku
    - 期刊：*Digital Discovery* 4, 1384–1403 (2025). DOI: 10.1039/D4DD00387J
    - 来源：[RSC](https://pubs.rsc.org/en/content/articlelanding/2025/dd/d4dd00387j)
    - 方法/成果：日本全国自驱动实验室（SDL）网络综述（含成分优化案例）

14. **《aLLoyM: a large language model for alloy phase diagram prediction》**（2026，超出 2019–2025 窗口，作为最新动态收录）
    - 作者：Y. Oikawa, G. Deffrennes, R. Shimayoshi, T. Abe, R. Tamura, K. Tsuda
    - 期刊：*npj Computational Materials* 12, 97 (2026). DOI: 10.1038/s41524-026-01966-6
    - 来源：[Nature 文章页](https://doi.org/10.1038/s41524-026-01966-6)
    - 方法：面向合金相图预测的大语言模型
    - 关键成果：LLM 直接预测合金相图（成分设计的语言模型新路线）

15. **《Large-language-model-driven adaptive search space definition for autonomous closed-loop materials exploration》**（2026，最新动态）
    - 作者：Y. Iwasaki, R. Toyama, R. Tamura, S. Matsuda, Y. Sakuraba, M. Kotsugi, Y. Igarashi, K. Sodeyama
    - 期刊：*Communications Materials* 7, 202 (2026). DOI: 10.1038/s43246-026-01304-9
    - 来源：[Nature 文章页](https://www.nature.com/articles/s43246-026-01304-9)
    - 方法：LLM 驱动的自适应搜索空间定义 + 自主闭环
    - 关键成果：LLM 根据文献自动收缩成分搜索空间，加速自主材料探索

**关于任务清单中"Tomoki Ueno（东北大学）"的核实结果（重要）**：
- 未检索到名为 Tomoki Ueno 的东北大学材料信息学研究者（日文检索亦未命中）。
- LAQA 的第一作者为**寺山圭（Kei Terayama）**（津田组）；COMBO/PHYSBO 的作者为**上野刚志（Tsuyoshi Ueno，东京大学津田组）**。任务清单中的"Tomoki Ueno（东北大学）"很可能是对 Tsuyoshi Ueno（东京大学）的误记，**待核实**。
- 东北大学方面：WPI-AIMR 的 **Hao Li / Shin-ichi Orimo 团队**于 2026 年发布基于 LLM 多智能体的储氢材料发现工作流 **DIVE**（[WPI-AIMR 新闻稿](https://www.wpi-aimr.tohoku.ac.jp/en/achievements/press/2026/20260204_002126.html)），超出 2019–2025 窗口，作为最新动态收录。

**其他日本相关组（简要）**：
- **统计数理研究所（ISM）吉田亮（Ryo Yoshida，よしだ りょう）**（数据科学中心主任，据 [ISM/研讨会介绍](https://aithermworkshop.nd.edu/speakers/ryo-yoshida/)）：Kusaba, M., Liu, C., Yoshida, R. "Crystal structure prediction with machine learning-based element substitution"，*Computational Materials Science* 211, 111496 (2022)，[arXiv:2201.11188](https://arxiv.org/abs/2201.11188)｜[ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0927025622002555)——基于元素替换的 ML 晶体结构预测。

---

## 六、韩国

### 29. 韩国中央大学（Chung-Ang University）/ 浦项科技大学（POSTECH）— Hyoung Seop Kim（金炯燮，音译待核实）& Byeong-Joo Lee（李炳周，音译待核实）

**机构与 PI**：Hyoung Seop Kim，中央大学新材料工程系教授（韩国材料研究学会前会长）；Byeong-Joo Lee，POSTECH 材料科学与工程系教授（CALPHAD 热力学专家，[POSTECH 主页](https://cmse.postech.ac.kr/professor)）。

**成分优化方向**：神经网络 + 热力学数据的高熵合金成分设计。

**代表论文**：

1. **《A neural network model for high entropy alloy design》**
   - 作者：J. Wang, H. Kwon, H. S. Kim, B.-J. Lee
   - 期刊：*npj Computational Materials* 9, 60 (2023). DOI: 10.1038/s41524-023-01010-x
   - 来源：[Nature 文章页](https://www.nature.com/articles/s41524-023-01010-x)
   - 方法：神经网络（融合热力学特征）在广阔 HEA 成分空间中搜索
   - 关键成果：设计并实验验证新的高熵合金成分（力学性能导向）

---

# 第二部分：方法学谱系（按方法分类）

> 以下把第一部分的工作按核心方法归类（一篇论文可能出现在多个类别）。

## 1. 描述符 + 树模型 / 经典机器学习

| 工作 | 组 | 方法要点 |
|---|---|---|
| Meredig et al., PRB 89, 094104 (2014) | Wolverton（西北） | 梯度提升树 + 成分特征，无约束成分空间外推 |
| Raccuglia et al., Nature 533, 73 (2016) | Wolverton | 失败实验数据 + 随机森林类分类，预测可合成性 |
| Sarker et al., Nat. Commun. 9, 4980 (2018) | Curtarolo（杜克） | 熵描述符筛选高熵碳化物 |
| Kaufmann et al., npj Comput. Mater. 6, 42 (2020) | Curtarolo | ML 分类发现高熵陶瓷 |
| Ouyang et al., PRM 2, 083802 (2018)（SISSO） | Scheffler（FHI） | 压缩感知符号回归，解析描述符 |
| Divilov et al., Nature 625, 66 (2024)（DEED） | Curtarolo | 无序焓–熵描述符判别高熵陶瓷可合成性 |
| Lee et al., npj Comput. Mater. 8, 25 (2022) | Balachandran（UVA） | 可解释树模型 + 归因分析，MPEA 相分类 |
| Taylor & Conduit, Comput. Mater. Sci. 227, 112265 (2023) | Conduit（剑桥） | 物理描述符 + ML，高温合金微观化学/蠕变 |
| Wang et al., npj Comput. Mater. 9, 60 (2023) | Kim/Lee（韩国） | 神经网络 + 热力学特征，HEA 设计 |
| Kim et al., J. Phys. Chem. C 122, 17575 (2018)（Polymer Genome） | Ramprasad（佐治亚理工） | 聚合物成分描述符 + 多性质回归 |

## 2. 图神经网络（GNN）

| 工作 | 组 | 方法要点 |
|---|---|---|
| Chen et al., Chem. Mater. 31, 3564 (2019)（MEGNet） | Ong（UCSD） | 图网络统一分子/晶体性质建模 |
| Choudhary & DeCost, npj Comput. Mater. 7, 185 (2021)（ALIGNN） | Choudhary（NIST） | 原子图 + 键连线图双层 GNN |
| 西北大学 npj Comput. Mater. 8, 48 (2022) | Wolverton | 尺度不变 CGCNN，四元硫族化物发现 |
| Merchant et al., Nature 624, 80 (2023)（GNoME） | DeepMind | 图网络 + 主动学习，220 万新晶体 |
| Zhang et al., npj Comput. Mater. 8, 89 (2022) | Wei Chen（西北） | Deep Sets（置换不变网络），HEA 成分设计 |
| Zhong et al., Joule (2024)（DRXNet） | Ceder（MIT） | 面向实验放电曲线的深度学习（非图模型，但同为深度学习成分-性能建模） |

## 3. 通用机器学习势（Universal MLIP）

| 工作 | 组 | 方法要点 |
|---|---|---|
| Chen & Ong, Nat. Comput. Sci. 2 (2022)（M3GNet） | Ong（UCSD） | 全周期表通用势；3100 万假想结构筛选 |
| Deng et al., Nat. Mach. Intell. 5 (2023)（CHGNet） | Ceder（MIT） | 电荷/磁矩感知通用势 |
| Yang et al., arXiv:2405.04967 (2024)（MatterSim） | Microsoft | 0–5000 K、1000 GPa 通用势；Gibbs 自由能 15 meV/atom |

## 4. 贝叶斯优化 / 主动学习（闭环）

| 工作 | 组 | 方法要点 |
|---|---|---|
| Xue et al., PNAS 113, 13301 (2016) | Lookman（前 LANL） | 自适应设计闭环（NiTi SMA） |
| Lookman et al., npj Comput. Mater. 5, 21 (2019) | Lookman | 权威综述（被引约 973） |
| Tran & Ulissi, Nat. Catal. 1, 660 (2018) | Ulissi（CMU→Meta） | 跨金属间化合物主动学习筛选电催化剂 |
| Kusne et al., Nat. Commun. 11, 5966 (2020)（CAMEO） | Curtarolo/Takeuchi/Mehta | 自主实验系统（Ge–Sb–Te 相变材料） |
| Ren et al., Sci. Adv. 4, eaaq1566 (2018) | Mehta/Wolverton（SLAC/西北/NIST/UNSW） | ML+高通量实验迭代闭环（Co–V–Zr 金属玻璃） |
| Rao et al., Science 378, 78 (2022) | Raabe/Rao（MPIE） | ML+DFT+CALPHAD+实验闭环；17 合金→2 个高熵 Invar |
| Pedersen et al., Angew 60, 24144 (2021) | Rossmeisl 团队（哥本哈根） | BO 优化 HEA 成分（ORR） |
| Mints et al., ACS Catal. 12, 11263 (2022) | Rossmeisl 团队 | BO 探索 HEA 纳米粒子成分（H2/CO 氧化） |
| Sulley et al., Scripta Mater. 249, 116180 (2024) | Montemore（杜兰） | 主动学习 + 神经网络；27% 数据达 95% 精度 |
| Terayama et al., npj Comput. Mater. 4, 32 (2018)（LAQA） | Tsuda（东大/RIKEN） | 局部质量估计的细粒度优化（结构预测） |
| Ueno et al., Mater. Discov. 4 (2016)（COMBO）；Motoyama et al., CPC 278, 108405 (2022)（PHYSBO） | Tsuda/Ueno（东大） | 高效 BO 库（Thompson 采样等） |
| Sun et al., NJP 22, 055001 (2020) | Tsuda/Hou/Tamura | 偏好学习整合多源数据 |
| Homma et al., JPCC 124, 12865 (2020) | Tsuda/Tamura | 三元混合物锂电导率 ML 优化 |
| de Castro et al., NPG Asia Mater. 12, 35 (2020) | Hou（RIKEN 时期） | ML 指导发现 HoB2 巨磁热效应 |
| Burger et al., Nature 583, 237 (2020) | Cooper（利物浦） | 移动机器人 + 批量贝叶斯搜索（688 实验/8 天） |
| Epps et al., Adv. Mater. 32, 1901266 (2020) | Abolhasani（NC State） | "Artificial Chemist" 自主量子点合成 |
| Tamura et al., Commun. Mater. 5, 139 (2024)（AIPHAD） | Tamura（NIMS） | 主动学习相图构建 |
| Toyama et al., npj Comput. Mater. 11, 329 (2025) | Tamura（NIMS） | 成分展宽薄膜自主闭环（反常霍尔） |
| Gurnani et al., Nat. Commun. 15, 6107 (2024) | Ramprasad | AI + 既有化学知识的人机协同闭环 |

## 5. 生成模型（逆向设计）

| 工作 | 组 | 方法要点 |
|---|---|---|
| Noh et al., Matter 1, 1370 (2019) | Gómez-Bombarelli（MIT） | VAE 连续表示 + 全局优化（Mg–Mn–O） |
| Xie et al., ICLR 2022（CDVAE） | MIT CSAIL | 晶体扩散 VAE，生成新成分+结构 |
| Zeni et al., Nature 639, 624 (2025)（MatterGen） | Microsoft | 扩散生成 + 目标性质微调 |
| （对照）Merchant et al., Nature 624, 80 (2023)（GNoME） | DeepMind | 判别式图网络 + 主动学习（非生成式，但同为"大规模虚拟筛选"路线） |

## 6. 多目标优化

| 工作 | 组 | 方法要点 |
|---|---|---|
| Conduit et al., Mater. Des. 131, 358 (2017) | Conduit（剑桥） | 概率神经网络多性质联合设计镍基高温合金 |
| Rao et al., Science 378, 78 (2022) | Raabe/Rao（MPIE） | 多性质（热膨胀/磁性/电学）联合搜索 |
| Mints et al., ACS Catal. 12, 11263 (2022) | Rossmeisl 团队 | 多目标 BO（活性/稳定性权衡） |
| Sun et al., NJP 22, 055001 (2020) | Tsuda 团队 | 偏好学习（隐式多目标） |
| Terayama et al., Chem. Sci. 11, 5959 (2020)（BLOX） | Tsuda 团队 | 无目标探索（突破性质极限） |

## 7. CALPHAD + ML

| 工作 | 组 | 方法要点 |
|---|---|---|
| Rao et al., Science 378, 78 (2022) | Raabe/Rao（MPIE） | 闭环中嵌入热力学（CALPHAD）计算 |
| Terayama et al., Scripta Mater. 208, 114335 (2022) | Terayama/Tamura | 吉布斯相律约束的 ML 相图构建 |
| Deffrennes et al., Mater. Des. 232, 112111 (2023) | Tamura（NIMS） | ML + CALPHAD 评估预测二元液相线 |
| Deffrennes et al., Calphad 87, 102745 (2024) | Tamura（NIMS） | 液相混合焓的数据驱动研究 |
| Oikawa et al., npj Comput. Mater. 12, 97 (2026)（aLLoyM） | Tamura/Tsuda | LLM 预测合金相图（语言模型 × CALPHAD 知识） |
| Wang et al., npj Comput. Mater. 9, 60 (2023) | Kim/Lee（韩国） | 神经网络 + 热力学特征（Lee 为 CALPHAD 专家） |

## 8. LLM / 智能体 / 自主实验室（含机器人闭环）

| 工作 | 组 | 方法要点 |
|---|---|---|
| Boiko et al., Nature 624, 570 (2023)（Coscientist） | Gomes（CMU） | GPT-4 智能体自主化学研究 |
| Szymanski et al., Nature 624, 86 (2023)（A-Lab） | Ceder（MIT/LBNL） | 机器人自主合成 + ML 数据解释（41/58 新化合物/17 天） |
| Tamura et al., STAM: Methods 3, 2232297 (2023)（NIMS-OS） | Tamura/Tsuda（NIMS） | AI-机器人闭环编排软件 |
| Yoshikawa et al., Digital Discovery 4, 1384 (2025) | 日本 SDL 联盟 | 日本自驱动实验室综述 |
| Tom et al., Chem. Rev. 124, 9633 (2024) | Aspuru-Guzik（多伦多） | 自驱动实验室权威综述 |
| Burger et al., Nature 583, 237 (2020)；Dai et al., Nature 635, 890 (2024) | Cooper（利物浦） | 移动机器人化学家（批量贝叶斯 + LLM 辅助编排） |
| Iwasaki et al., Commun. Mater. 7, 202 (2026) | Tamura 团队 | LLM 驱动自适应搜索空间 + 自主闭环 |
| 东北大学 DIVE（2026，新闻稿） | 东北大学 WPI-AIMR | LLM 智能体储氢材料发现工作流 |

---

# 第三部分：总览表

| # | 机构 | PI（中文译名） | 国家 | 核心方法 | 旗舰成果（2019–2025） |
|---|---|---|---|---|---|
| 1 | MIT | Gerbrand Ceder（格布兰德·塞德） | 美国 | 自主实验室、深度学习、通用势 | A-Lab 17 天 41 个新化合物；高熵 DRX 正极 955 Wh/kg |
| 2 | MIT | Rafael Gómez-Bombarelli（拉斐尔·戈麦斯-邦巴雷利） | 美国 | VAE 连续表示逆向设计 | Mg–Mn–O 逆向设计（Matter 2019） |
| 3 | MIT CSAIL | Tian Xie 等 | 美国 | 晶体扩散生成（CDVAE） | 周期性材料生成基准模型 |
| 4 | UC Berkeley/LBNL | Kristin Persson（克里斯汀·佩尔松） | 美国 | 数据基础设施 | Materials Project（Nature Materials 2025 综述） |
| 5 | UCSD | Shyue Ping Ong | 美国 | GNN、通用势 | M3GNet：3100 万结构筛选→180 万潜在稳定 |
| 6 | Northwestern | Chris Wolverton（克里斯·沃尔弗顿） | 美国 | 树模型、CGCNN | 尺度不变 GNN 发现超低热导四元硫族化物 |
| 7 | Northwestern | Wei Chen（陈伟，待核实） | 美国 | Deep Sets | 高熵合金成分设计（npj 2022） |
| 8 | Duke | Stefano Curtarolo（斯特凡诺·库塔罗洛） | 美国 | 熵/DEED 描述符、CAMEO | DEED（Nature 2024）；CAMEO 自主发现 Ge–Sb–Te 相变材料 |
| 9 | UMD | Ichiro Takeuchi（竹内一郎） | 美国 | 组合实验+闭环 | CAMEO 实验侧共同负责人 |
| 10 | LANL（前） | Turab Lookman（图拉布·卢克曼） | 美国 | 主动学习 | PNAS 2016 奠基；npj 2019 综述（被引约 973） |
| 11 | CMU→Meta | Zack Ulissi（扎克·乌利西） | 美国 | 主动学习 | 电催化剂筛选（Nat. Catal. 2018）；OC20 数据集 |
| 12 | CMU | G. dos Passos Gomes / Carla Gomes | 美国 | LLM 智能体 | Coscientist（Nature 2023） |
| 13 | Stanford | Evan Reed（埃文·里德） | 美国 | 迁移学习 | 数十亿候选固态锂导体筛选 |
| 14 | Yale | Jan Schroers（扬·施罗尔斯） | 美国 | ML 对比研究、描述符 | ML vs 人类 GFA 预测（Acta Mater. 2023）；Soliquidy 玻璃形成描述符（npj 2025） |
| 15 | Georgia Tech | Rampi Ramprasad（兰皮·拉姆普拉萨德） | 美国 | 聚合物信息学 | AI 辅助高温介电材料（Nat. Commun. 2024） |
| 16 | UVA | Prasanna Balachandran（普拉桑纳·巴拉昌德兰） | 美国 | 可解释 ML | MPEA 相分类（npj 2022） |
| 17 | NC State | Milad Abolhasani（米拉德·阿博尔哈萨尼） | 美国 | 微流控+BO | Artificial Chemist 自主量子点合成 |
| 18 | NIST | Kamal Choudhary（卡马尔·乔杜里） | 美国 | GNN、数据库 | ALIGNN（npj 2021）；JARVIS |
| 19 | Toronto | Alán Aspuru-Guzik（阿兰·阿斯普鲁-古齐克） | 加拿大 | 自驱动实验室 | Chem. Rev. 2024 SDL 综述 |
| 20 | MPIE（德国） | Dierk Raabe（迪尔克·拉贝）/ Ziyuan Rao | 德国 | 主动学习闭环 | Science 2022：17 合金→2 个高熵 Invar |
| 21 | FHI Berlin | Matthias Scheffler（马蒂亚斯·舍夫勒） | 德国 | SISSO、数据基础设施 | NOMAD/FAIRmat 生态 |
| 22 | KU Copenhagen | Jan Rossmeisl（扬·罗斯梅斯尔）团队 | 丹麦 | 贝叶斯优化 | HEA 电催化剂成分 BO（Angew 2021） |
| 23 | Cambridge | Gareth Conduit（加雷斯·康迪特） | 英国 | 概率神经网络 | 多目标高温合金设计（+Intellegens 商业化） |
| 24 | Liverpool | Andrew Cooper（安德鲁·库珀） | 英国 | 移动机器人+BO | 8 天 688 实验发现光催化剂配方 |
| 25 | EPFL | （未锁定专门组，待核实） | 瑞士 | — | COSMO/Ceriotti（ML 力场方向） |
| 26 | Google DeepMind | A. Merchant / E. D. Cubuk 等 | 英国 | 图网络+主动学习 | GNoME：220 万新晶体、38 万稳定 |
| 27 | Microsoft Research | C. Zeni / Han Yang 等 | 英国/美国 | 扩散生成、通用势 | MatterGen（Nature 2025）；MatterSim |
| 28 | RIKEN/东大/NIMS | 津田研一、田村亮、侯柱峰、上野刚志 | 日本 | BO 库、偏好学习、SDL | HoB2 巨磁热效应；PHYSBO/NIMS-OS/aLLoyM |
| 29 | 中央大学/POSTECH | Hyoung Seop Kim / Byeong-Joo Lee | 韩国 | 神经网络+热力学 | HEA 设计（npj 2023） |

---

# 第四部分：待核实事项与更正清单

## 对任务清单的更正（经检索核实）

1. **"G. A. Sulley（哥本哈根大学，2024，Materials & Design）"**：
   - 实际论文：Sulley, Raush, Montemore 等，*Scripta Materialia* 249, 116180 (2024)（非 Materials & Design）；
   - Sulley 隶属**杜兰大学（Tulane）**（Montemore 组），非哥本哈根大学；
   - 哥本哈根大学的对应工作为 Rossmeisl 团队（Pedersen 2021 Angew、Mints 2022 ACS Catal.）。
2. **"Tomoki Ueno（东北大学）"**：未检索到该人；LAQA 一作为寺山圭（Kei Terayama），BO 库（COMBO/PHYSBO）作者为上野刚志（Tsuyoshi Ueno，东京大学津田组）。疑为误记，待核实。
3. **"Zhufeng Hou（RIKEN）"**：其被引工作（HoB2 磁热、偏好学习）确为 RIKEN CEMS 时期；ResearchGate 显示现隶属中国科学院（待核实）。
4. **"Zack Ulissi（CMU）"**：现为 Meta FAIR AI 研究总监、CMU 兼职教授。
5. **"Turab Lookman（LANL）"**：已离开 LANL（美国司法部新闻稿——2020 年 9 月宣判——称其为"前 LANL 雇员"）。
6. **"MPIE"**：该所 2024 年更名为 Max Planck Institute for Sustainable Materials（马普可持续材料研究所）。
7. **"Ziyuan Rao（MPIE）"**：ResearchGate 显示其现为上海交通大学副教授（其被引核心工作为 MPIE 时期，待核实现职）。
8. **"MatterSim"**：截至检索时仍为 arXiv 预印本（arXiv:2405.04967），未见期刊正式发表。
9. **"Ren et al. 2018 与 Schroers"**：Ren 等 *Sci. Adv.* 4, eaaq1566 (2018) 常被归于 Schroers 名下，但经 PMC 作者列表核实，作者为 F. Ren、L. Ward、T. Williams、K. J. Laws、C. Wolverton、J. Hattrick-Simpers、A. Mehta，**不含 Schroers**（详见第 6、14 节）。

## 数据级待核实项

- DRXNet（Zhong et al., Joule 2024）的卷期页码（DOI: 10.1016/j.joule.2024.03.010 已核实）。
- CHGNet（Nat. Mach. Intell. 5, 2023）的页码/文章号。
- M3GNet（Nat. Comput. Sci. 2, 2022）的页码。
- COMBO（Materials Discovery 4, 2016）的页码。
- Esters et al.（Comput. Mater. Sci. 216, 111808, 2023）的 DOI。
- Xue et al. PNAS 2016 论文的准确标题（"adaptive design" 与 "active learning" 两种引用并存，以 PNAS 官方页面为准）。
- EPFL 是否存在专门的成分优化课题组（本轮未锁定）。
- 各中文音译姓名（标注"音译待核实"者）。

---

## 参考来源说明

本报告全部事实来自以下类型的已检索网页（正文内均已以链接形式标注）：Nature/Nature 系列文章页、ScienceDirect、ACS、RSC、IOPscience、APS、arXiv、PubMed/PMC、ORNL Impact、OSTI、NIST、MPIE 官网、NIMS/田村亮论文列表、津田实验室、寺山圭个人主页、Schroers 实验室、Reed 组、POSTECH、WPI-AIMR 新闻稿、DeepMind/Microsoft 博客、ResearchGate、Google Scholar/ADS 检索摘要。nature.com 与 ScienceDirect 直接抓取受限时，引用信息经 PubMed、arXiv、机构镜像与检索摘要交叉核实。
