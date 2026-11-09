# 机器学习/深度学习驱动的材料成分优化：全球活跃研究课题组调研

**核实方法与边界**：所有条目均通过 web_search / web_fetch 交叉核实（标题、作者、期刊与 URL 来自出版社页面、arXiv、PubMed/OSTI、课题组官网）；未核实处明确标注。优先 2018–2026 年论文并纳入近两年动态。全程未使用 www.microsoft.com、news.northwestern.edu 及其子域名作为来源（Microsoft Research 工作仅引 arXiv/Nature，Northwestern 工作仅引 npj/APS/ACS/Annual Reviews）。中国学者姓名仅在可核实时给出汉字，其余以拼音标注；外文姓名附通行中文译名。

## 一、金属与合金（高熵合金、形状记忆合金、钢/高温合金、金属玻璃）

**1. Turab Lookman（图拉布·卢克曼）** — 美国洛斯阿拉莫斯国家实验室（LANL），现佛罗里达大学。方向：主动学习（active learning）+ 贝叶斯自适应采样，加速形状记忆合金与铁电压电氧化物成分定向设计。
- Yuan et al., "Accelerated Discovery of Large Electrostrains in BaTiO3-Based Piezoelectrics Using Active Learning," *Adv. Mater.* 30, 1702884 (2018). https://advanced.onlinelibrary.wiley.com/doi/abs/10.1002/adma.201702884 — 用主动学习闭环在 BaTiO3 基无铅压电中搜索出大电致应变成分。
- Lookman et al., "Active learning in materials science with emphasis on adaptive sampling using uncertainties for targeted design," *npj Comput. Mater.* 5, 21 (2019). https://www.nature.com/articles/s41524-019-0153-8 — 系统综述不确定度驱动的自适应采样定向设计范式（其 2016 年 NiTi 形状记忆合金工作为奠基）。

**2. Wen Chen（汉字未核实）** — 美国马萨诸塞大学阿默斯特分校（UMass Amherst）。方向：高熵合金（HEA）数据驱动成分设计（硬度、固溶强化）与生成式/主动学习框架。
- Wen et al., "Machine learning assisted design of high entropy alloys with desired property," *Acta Mater.* 170 (2019). https://www.sciencedirect.com/science/article/abs/pii/S1359645419301430 — ML 代理模型+实验反馈闭环，以极少实验定位目标硬度 HEA 成分。
- Wen et al., "Modeling solid solution strengthening in high entropy alloys using machine learning," *Acta Mater.* 212, 116917 (2021). https://www.sciencedirect.com/science/article/abs/pii/S1359645421002974 — 建立 HEA 固溶强化（成分-摩擦应力）可解释 ML 模型。

**3. Raymundo Arróyave（雷蒙多·阿罗亚韦）** — 美国德克萨斯农工大学（Texas A&M）。方向：物理信息贝叶斯优化与热力学-ML 耦合的合金成分设计（NiTi 形状记忆合金、稀土化合物）。
- Khatamsaz et al., "A physics informed bayesian optimization approach for material design: application to NiTi shape memory alloys," *npj Comput. Mater.* 9 (2023). https://www.nature.com/articles/s41524-023-01173-7 — 物理信息 BO 多目标优化 NiTi 相变温度/滞后，实验验证。
- Singh et al., "Machine-learning enabled thermodynamic model for the design of new rare-earth compounds," *Acta Mater.* (2022). https://www.sciencedirect.com/science/article/abs/pii/S135964542200146X — ML 加速 CALPHAD 型热力学建模，用于新型稀土化合物成分筛选（与 Ames 实验室合作）。

**4. Zi-Kui Liu（汉字未核实）** — 美国宾州州立大学（Penn State）。方向：CALPHAD+熵理论（zentropy）+机器学习的成分-相结构设计（难熔合金、高熵陶瓷）。
- Li et al., "Design and validation of refractory alloys using machine learning, CALPHAD, and experiments," *Int. J. Refract. Met. Hard Mater.* 121, 106673 (2024). https://doi.org/10.1016/j.ijrmhm.2024.106673 — ML+CALPHAD+实验闭环验证难熔合金成分。
- Debnath et al., "Generative deep learning as a tool for inverse design of high-entropy refractory alloys," *J. Mater. Inform.* 1, 3 (2021). https://doi.org/10.20517/jmi.2021.05 — 生成式深度网络直接逆向生成满足目标的难熔 HEA 成分。
- Olson & Liu, "Genomic materials design: CALculation of PHAse Dynamics," *CALPHAD* 82, 102590 (2023). https://doi.org/10.1016/j.calphad.2023.102590 — 提出材料"基因组"式相动力学计算设计框架。

**5. Ichiro Takeuchi（竹内一郎，音译）** — 美国马里兰大学。方向：组合薄膜实验+在线（on-the-fly）机器学习的相图构建与合金发现（形状记忆合金、磁体）。
- Kusne et al., "On-the-fly machine-learning for high-throughput experiments: search for rare-earth-free permanent magnets," *Sci. Rep.* 4, 6367 (2014). https://www.nature.com/articles/srep06367 — 开创高通量实验中实时 ML 边采集边学习的闭环范式。
- Al Hasan et al., "Combinatorial Exploration and Mapping of Phase Transformation in a Ni–Ti–Co Thin Film Library," *ACS Comb. Sci.* 22, 641 (2020). https://pubs.acs.org/acsccc/article/22/11/641/605953/Combinatorial-Exploration-and-Mapping-of-Phase — 组合薄膜库+ML 映射 Ni-Ti-Co 马氏体相变成分区间。

**6. Bryce Meredig（布莱斯·梅雷迪格）** — Citrine Informatics（美国）。方向：面向工业落地的无机材料成分-性质 ML 与"已验证预测"追踪。
- Meredig & Wolverton, "Combinatorial screening for new materials in unconstrained composition space with machine learning," *Phys. Rev. Lett.* 113, 015502 (2014). https://doi.org/10.1103/PhysRevLett.113.015502 — 首次演示 ML 在全成分空间进行新化合物筛选。
- Saal, Oliynyk & Meredig, "Machine Learning in Materials Discovery: Confirmed Predictions and Their Underlying Approaches," *Annu. Rev. Mater. Res.* 50, 49–69 (2020). https://par.nsf.gov/servlets/purl/10292820 — 系统盘点 ML 预测且经实验证实的材料案例。

**7. Dierk Raabe / Jörg Neugebauer（MPIE，德国马普钢铁研究所）+ Hongbin Zhang（汉字未核实，达姆施塔特工业大学）** — 德国。方向：主动学习+DFT+CALPHAD+实验四位一体的高熵合金（Invar 低膨胀合金）闭环设计。
- Rao et al., "Machine learning-enabled high-entropy alloy discovery," *Science* 378, 78–85 (2022). https://www.science.org/doi/10.1126/science.abo4940（预印本 https://arxiv.org/abs/2202.13753 ）— 从近无穷成分空间中经 17 次合成迭代锁定两种超低热膨胀高熵 Invar 合金。

**8. Wei Xu（许伟）团队 — 东北大学轧制技术及连轧自动化国家重点实验室（RAL）** — 中国。方向：物理冶金知识引导的 ML+实验设计，超高强不锈钢成分设计。
- Shen et al., "Physical metallurgy-guided machine learning and artificial intelligent design of ultrahigh-strength stainless steel," *Acta Mater.* 179, 201–214 (2019). https://www.sciencedirect.com/science/article/abs/pii/S1359645419305452 — 以位错强化等冶金机理为特征工程的钢成分 ML 设计（与代尔夫特理工、阿拉巴马大学合作）。

**9. Jinshan Li（李金山）团队 — 西北工业大学凝固技术国家重点实验室** — 中国。方向：数据挖掘+深度学习的钛合金/高熵合金强塑性协同成分设计（AI for Materials）。
- Zou et al., "Integrating data mining and machine learning to discover high-strength ductile titanium alloys," *Acta Mater.* 202, 211–221 (2021). https://doi.org/10.1016/j.actamat.2020.10.056 — 数据挖掘定位+ML 设计高强韧钛合金成分（与 Liu 等合作）。团队 2023–2025 年连发多篇 Acta Materialia AI 论文（见实验室官网 https://sklsp.nwpu.edu.cn/ ）。

**10. 香港城市大学（CityU HK）— Shijun Zhao（汉字未核实）与 Yang Yang（汉字未核实）** — 中国香港。方向：机器学习设计高熵陶瓷（碳化物）与共晶成分复杂合金；图注意力深度学习设计高熵电催化剂。
- Zhang et al., "Design high-entropy carbide ceramics from machine learning," *npj Comput. Mater.* 8, 5 (2022). https://doi.org/10.1038/s41524-021-00678-3 — 预测单相高熵碳化物形成能力并实验验证。
- Chen et al., "Design high-entropy electrocatalyst via interpretable deep graph attention learning," *Joule* 7, 1832–1851 (2023). https://doi.org/10.1016/j.joule.2023.06.003 — 可解释图注意力模型逆向设计高熵电催化剂成分。
- Chen, Shang, Liu & Yang, "Accelerated discovery of eutectic compositionally complex alloys by generative machine learning," *npj Comput. Mater.* 10, 204 (2024). https://doi.org/10.1038/s41524-024-01385-5 — CVAE 生成模型直接生成四元至六元共晶合金新成分。

**11. Jun Ni（倪军）— 清华大学物理系** — 中国。方向：小样本生成式对抗网络+元素特征迁移预测高熵合金性质并探索成分空间。
- Sun, ... Ni, "EFTGAN: Elemental features and transferring corrected data augmentation for the study of high-entropy alloys," *npj Comput. Mater.* 11 (2025). https://doi.org/10.1038/s41524-025-01548-y — 元素特征迁移 GAN 增强小样本数据，免结构计算即可在广阔成分空间预测形成能与磁矩（另有通用 ML 框架工作，论文未核实，见系里报道 https://www.phys.tsinghua.edu.cn/info/1066/2012.htm ）。

**12. Jianxin Xie（谢建新）/ Huadong Fu（付华栋）/ Hongtao Zhang（张洪涛）— 北京科技大学（北京材料基因工程高精尖创新中心）** — 中国。方向：可解释 ML 的高端合金（钢铁）成分-工艺设计。
- Zhang et al., "Empowering the Sustainable Development of High-End Alloys via Interpretive Machine Learning," *Adv. Mater.* 36, 2404478 (2024). https://advanced.onlinelibrary.wiley.com/doi/10.1002/adma.202404478 — 可解释 ML 框架驱动高端合金成分设计。
- Feng, Fu, ... Dong, "A general and transferable deep learning framework for predicting phase formation in materials," *npj Comput. Mater.* 7, 24 (2021). https://www.nature.com/articles/s41524-020-00488-z — 深度学习从成分直接预测相形成（与英国莱斯特大学董洪标合作）。
- 谢建新, "机器学习在材料研发中的应用," 《金属学报》57(11), 1343 (2021). https://www.ams.org.cn/article/2021/0412-1961/0412-1961-2021-57-11-1343.shtml — 中文权威综述，梳理材料特征与逆向设计路线。

**13. Lijun Zhang（张利军）— 中南大学粉末冶金国家重点实验室** — 中国。方向：CALPHAD 计算热力学+ML 耦合的铸造铝合金成分/元素配比设计。
- Yi et al., "Boosting for concept design of casting aluminum alloys driven by combining computational thermodynamics and machine learning techniques," *J. Mater. Inform.* 1, 10 (2021). https://www.oaepublish.com/articles/jmi.2021.10 — 综述并提出 CT+ML 耦合铸造铝合金概念设计范式。
- 其 JMST 2022 论文（ML 确定 A356 铝合金 Sr 最优添加量，共同一作易旺、刘光琛）经团队报道核实，论文标题/DOI 未核实：http://www.ecorr.org.cn/dhTJDAOHANG/cjzl/yejiedongtai/2022-01-05/182667.html

**14. Tejs Vegge（泰斯·韦格）团队 — 丹麦技术大学（DTU）** — 丹麦。方向：贝叶斯优化驱动高熵合金电催化成分设计。
- Pedersen et al., "Bayesian Optimization of High-Entropy Alloy Compositions for Electrocatalytic Oxygen Reduction," *Angew. Chem. Int. Ed.* 60, 24144–24152 (2021). https://onlinelibrary.wiley.com/doi/abs/10.1002/anie.202108116 — BO 从庞大 HEA 成分空间搜索高活性 ORR 催化剂成分。

## 二、DFT 高通量计算与通用性质预测（与成分设计强相关）

**15. Shyue Ping Ong（汉字未核实）** — 美国加州大学圣地亚哥分校（UCSD）。方向：图网络通用性质预测（MEGNet）与机器学习原子间势（Materials Project 生态）。
- Chen et al., "Graph Networks as a Universal Machine Learning Framework for Molecules and Crystals (MEGNet)," arXiv:1812.05055（*Chem. Mater.* 31, 3564 (2019)）. https://arxiv.org/abs/1812.05055 — 从成分/结构图直接预测晶体与分子性质。
- "Machine Learning Interatomic Potentials for Modeling Solid-State Batteries," *Chem. Mater.* 38, 9623 (2025). https://pubs.acs.org/cmatex/article/38/19/9623/5440208/Machine-Learning-Interatomic-Potentials-for — MLIP 用于固态电池材料模拟的综述。

**16. Kristin Persson（克里斯汀·佩尔森）** — 美国劳伦斯伯克利国家实验室（LBNL）/ UC Berkeley，Materials Project 创始人。方向：材料大数据平台+ML 筛选双金属电催化剂、高通量成分-性质关系。
- Horton et al., "Accelerated data-driven materials science with the Materials Project," *Nat. Mater.* 24, 1522–1532 (2025). https://doi.org/10.1038/s41563-025-02272-0 — 数据平台如何塑造数据驱动材料发现。
- Tran et al., "Screening of bimetallic electrocatalysts for water purification with machine learning," *J. Chem. Phys.* 157, 074102 (2022). https://pubmed.ncbi.nlm.nih.gov/35987588/ — ML 预测形成能/表面性质以筛选双金属催化剂成分。

**17. Anubhav Jain（阿努巴夫·贾因）** — LBNL。方向：高通量工作流（Atomate/FireWorks）+ NLP/LLM 材料合成规划（与成分设计闭环衔接）。
- Dagdelen et al., "Structured information extraction from scientific text with large language models," *Nat. Commun.* 15, 1418 (2024). https://www.nature.com/articles/s41467-024-45563-x — 用 LLM 结构化抽取合成配方，反哺合成设计。
- Wang et al., "Dataset of solution-based inorganic materials synthesis routes," *Sci. Data* 9, 205 (2022). https://www.nature.com/articles/s41597-022-01317-2 — 大规模溶液法合成路线数据集支撑 ML 模型。

**18. Gerbrand Ceder（格布兰德·塞德）** — 美国麻省理工学院（MIT）/LBNL。方向：钙钛矿稳定性描述符、自动化实验室（A-Lab）与电池材料 ML 设计。
- Bartel et al., "Physical descriptor for the Gibbs energy of inorganic crystalline solids and temperature-dependent materials chemistry," *Nat. Commun.* 9, 4168 (2018). https://www.nature.com/articles/s41467-018-06682-4 — 由成分描述符预测吉布斯自由能，支撑成分稳定性筛选。
- Bartel et al., "New tolerance factor to predict the stability of perovskite oxides and halides," *Sci. Adv.* 5, eaav0693 (2019). https://doi.org/10.1126/sciadv.aav0693 — 新容忍因子从成分判断钙钛矿稳定性。
- Szymanski et al., "An autonomous laboratory for the accelerated synthesis of novel materials," *Nature* 624, 462 (2023). https://doi.org/10.1038/s41586-023-06734-w — A-Lab 自主合成计算预测的新化合物。

**19. Chris Wolverton（克里斯·沃尔弗顿）** — 美国西北大学（Northwestern）。方向：成分描述符驱动的通用性质预测与相形成深度学习。
- Jha et al., "A general-purpose machine learning framework for predicting properties of inorganic materials," *npj Comput. Mater.* 2, 16028 (2016). https://www.researchgate.net/publication/304641366 — 奠基性成分向量→性质通用 ML 框架。
- Meredig & Wolverton, "Combinatorial screening for new materials in unconstrained composition space," *PRL* 113, 015502 (2014). https://doi.org/10.1103/PhysRevLett.113.015502 — 无约束成分空间 ML 新材料筛选（同上 Meredig 条目）。

**20. Stefano Curtarolo（斯特凡诺·库塔罗洛）** — 美国杜克大学。方向：AFLOW 高通量数据库+机器学习势/性质预测。
- Roberts et al., "Machine learned interatomic potentials for ternary carbides trained on the AFLOW database," *npj Comput. Mater.* 10, 142 (2024). https://www.nature.com/articles/s41524-024-01321-7 — 以 AFLOW 数据训练三元碳化物 MLIP。
- Curtarolo et al., "AFLOW: An automatic framework for high-throughput materials discovery," *Comput. Mater. Sci.* 58, 218 (2012). https://doi.org/10.1016/j.commatsci.2012.02.005 — 高通量材料发现自动框架（经典）。

**21. Logan Ward（洛根·沃德）** — 美国芝加哥大学（2024 年起，原 Argonne）。方向：材料数据挖掘工具链（Matminer/Magpie）与自动化特征工程。
- Ward et al., "Matminer: An open source toolkit for materials data mining," *Comput. Mater. Sci.* 152, 60 (2018). https://www.osti.gov/pages/biblio/1532339 — 标准化特征提取工具，支撑成分-性质建模。
- 作为共同作者的 Jha 2016 npj 论文（见 19）为成分描述符奠基工作。

**22. Kamal Choudhary（卡马尔·乔杜里）** — 美国 NIST（现兼职约翰霍普金斯大学）。方向：JARVIS 数据库与通用 ML/MLIP 性质预测。
- Choudhary et al., "The joint automated repository for various integrated simulations (JARVIS) for data-driven materials design," *npj Comput. Mater.* 6, 64 (2020). https://www.nature.com/articles/s41524-020-00440-1 — 整合 DFT/ML 数据的国家数据库。
- Choudhary & DeCost, "Recent advances and applications of deep learning in materials science," *npj Comput. Mater.* 8, 59 (2022). https://www.nature.com/articles/s41524-022-00734-6 — 深度学习材料科学应用综述（作者列表见原文）。

**23. Yousung Jung（汉字未核实）** — 韩国首尔国立大学（SNU）化学生物工程系。**注：用户提示中的"KAIST"有误，Jung 在 SNU（已核实）。** 方向：AI+电子结构方法；LLM 预测新材料可合成性（连接成分设计与合成）。
- Kim et al., "Large Language Models for Inorganic Synthesis Predictions," *J. Am. Chem. Soc.* 146, 10124 (2024). https://doi.org/10.1021/jacs.4c05840 — LLM 从数万篇论文学习并预测无机合成路线。
- Kim et al., "Explainable Synthesizability Prediction of Inorganic Crystal Polymorphs using Large Language Models," *Angew. Chem. Int. Ed.* (2025). https://doi.org/10.1002/anie.202423950 — 可解释评估新成分的可合成性。

**24. Atsuto Seko（汉字未核实）** — 日本京都大学。方向：成分描述符/推荐系统+机器学习势。
- Seko et al., "Compositional descriptor-based recommender system for the materials discovery," *J. Chem. Phys.* 148, 241719 (2018). https://pubs.aip.org/aip/jcp/article/148/24/241719/961129/Compositional-descriptor-based-recommender-system — 成分描述符推荐系统从未知组合中推荐候选材料。
- Seko et al., "Representation of compounds for machine-learning prediction of materials properties," *Phys. Rev. B* 95, 144110 (2017). https://link.aps.org/doi/10.1103/PhysRevB.95.144110 — 化合物成分表示方法比较。

**25. Koji Tsuda / Ryo Tamura（汉字未核实）— 东京大学 + NIMS/RIKEN** — 日本。方向：贝叶斯优化（PHYSBO）与 AI-机器人闭环自主实验（NIMS-OS）。
- Tamura et al., "NIMS-OS: an automation software to implement a closed loop between artificial intelligence and robotic experiments in materials science," *STAM Methods* 3, 2232297 (2023). https://doi.org/10.1080/27660400.2023.2232297 （arXiv: https://arxiv.org/abs/2304.13927 ）— 开源 AI×机器人闭环材料探索软件。
- Motoyama et al., "Bayesian optimization package: PHYSBO," *Comput. Phys. Commun.* 278 (2022). https://www.sciencedirect.com/science/article/pii/S0010465522001242 — 面向物理/材料的可扩展 BO 库。
- Yoshikawa et al., "Self-driving laboratories in Japan," *Digital Discovery* 4, 1384 (2025). https://doi.org/10.1039/D4DD00387J — 日本自主实验室全景综述。近况：2026 年 aLLoyM 合金相图 LLM（npj Comput. Mater. 12, 97）。

**26. 工业界大模型（补充）**：**Google DeepMind GNoME** — Merchant et al., "Scaling deep learning for materials discovery," *Nature* 624, 80–85 (2023). https://www.nature.com/articles/s41586-023-06735-9 — 图网络发现 220 万种新稳定成分。**Microsoft Research MatterGen** — Zeni et al., "A generative model for inorganic materials design," *Nature* 639, 624–632 (2025). https://www.nature.com/articles/s41586-025-08628-5 （arXiv: https://arxiv.org/abs/2312.03687 ）— 按目标性质微调的成分+结构生成式扩散模型。（按要求仅引 arXiv/Nature。）

## 三、聚合物、玻璃、陶瓷/钙钛矿、电池、催化剂方向的成分优化

**27. Rampi Ramprasad（拉姆普拉萨德，音译）** — 美国佐治亚理工学院。方向：聚合物信息学（Polymer Genome）成分/重复单元级性质预测与设计。
- Kim et al., "Polymer Genome: A Data-Powered Polymer Informatics Platform for Property Predictions," *J. Phys. Chem. C* 122, 17575 (2018). https://pubs.acs.org/jpccck/article/122/31/17575/1470511/Polymer-Genome-A-Data-Powered-Polymer-Informatics — 聚合物成分指纹→多性质预测平台。
- Gurnani et al., "Polymer Informatics at Scale with Multitask Graph Neural Networks," *Chem. Mater.* (2023). https://pmc.ncbi.nlm.nih.gov/articles/PMC9979603/ — 多任务图网络将聚合物信息学扩展到大规模数据。

**28. A. Lindsay Greer（林赛·格里尔）** — 英国剑桥大学。方向：金属玻璃（BMG）成分的机器学习预测+演化设计。
- Forrest & Greer, "Evolutionary design of machine-learning-predicted bulk metallic glasses," *Digital Discovery* 2, 202–218 (2023). https://doi.org/10.1039/D2DD00078D — ML 预测玻璃形成能力+演化算法搜索新 BMG 成分。

**29. Zachary Ulissi（扎卡里·乌利西）** — 美国卡内基梅隆大学（CMU）。方向：电催化剂高通量 DFT+主动学习成分筛选。
- Tran & Ulissi, "Active learning across intermetallics to guide discovery of electrocatalysts for CO2 reduction and H2 evolution," *Nat. Catal.* 1, 696–703 (2018). https://www.osti.gov/biblio/1543784 — 主动学习跨金属间化合物筛选 CO2RR/HER 催化剂成分。
- Tran et al., 2022 *J. Chem. Phys.*（见 16 Persson 条目，为共同作者）。

**30. Andrew I. Cooper（安德鲁·库珀）** — 英国利物浦大学 Leverhulme 功能材料设计研究中心。方向：机器人化学家+贝叶斯优化的自主材料/分子配方发现。
- Burger et al., "A mobile robotic chemist," *Nature* 583, 237–241 (2020). https://www.nature.com/articles/s41586-020-2442-2 — 移动机器人 8 天自主完成 688 个实验优化光催化配方。
- Li et al., "Sequential closed-loop Bayesian optimization as a guide for organic molecular metallophotocatalyst formulation discovery," *Nat. Chem.* (2024). https://pmc.ncbi.nlm.nih.gov/articles/PMC11321994/ — 序贯闭环 BO 加速金属光催化剂配方发现。

**交叉引用**（成分优化相关、已在前文核实）：功能氧化物/钙钛矿——Lookman（Yuan 2018 BaTiO3 主动学习）、Ceder（Bartel 2018/2019 稳定性描述符）、Persson（Sr2Nb2O7 掺 V 设计，Chem. Mater. 2022，见课题组论文页 https://perssongroup.lbl.gov/publications.html ）；高熵陶瓷/催化剂——CityU Zhao（npj 2022、Joule 2023）；电池材料——Ceder（A-Lab 2023）、Ong（固态电池 MLIP 2025）；金属玻璃——Greer（2023）、MPIE（Rao 2022）；形状记忆合金——Lookman、Arróyave、Takeuchi。

## 四、覆盖说明与未核实项（诚实披露）

- **上海交通大学、华南理工大学、中国科学院金属研究所**：本轮中英文多轮检索未核实到"机器学习成分优化"方向的代表性论文（上交 2026 年 AI 燃料性质预测属燃料物性，非材料成分；金属所钛合金研究部以实验为主，见 http://imr.cas.cn/jgsz/synl/202604/t20260410_8183704.html ）。建议后续单独深挖。
- **中科院物理所/宁波材料所管鹏飞团队**（AI+材料计算与设计，金属玻璃）：机构信息已核实（https://aircenter.nimte.ac.cn/view-31545.html ），但代表性论文本轮未逐篇核实，故未单列。
- 中南大学 JMST 2022 论文、清华倪军早期框架论文、MPIE/DTU/Greer/东北大学等条目的"第二篇"论文未核实，均已在上文标注。
- 所有链接均为可直接访问的出版社/arXiv/PubMed/OSTI/官网页面；未经 web_search/web_fetch 核实的信息未写入。

## 五、汇总表

| 课题组 | 机构（国家/地区） | 研究方向 | 代表论文年份 | 关键链接 |
|---|---|---|---|---|
| Turab Lookman | LANL→佛罗里达大学（美） | 主动学习设计形状记忆合金/压电氧化物 | 2018, 2019 | nature.com/articles/s41524-019-0153-8 |
| Wen Chen | UMass Amherst（美） | ML 设计高熵合金硬度/固溶强化 | 2019, 2021 | sciencedirect.com/…S1359645419301430 |
| Raymundo Arróyave | Texas A&M（美） | 物理信息 BO 设计 NiTi/稀土化合物 | 2022, 2023 | nature.com/articles/s41524-023-01173-7 |
| Zi-Kui Liu | Penn State（美） | ML+CALPHAD+生成式难熔合金/陶瓷 | 2021–2024 | doi.org/10.1016/j.ijrmhm.2024.106673 |
| Ichiro Takeuchi | 马里兰大学（美） | 组合实验+在线 ML 相图/合金 | 2014, 2020 | nature.com/articles/srep06367 |
| Bryce Meredig | Citrine Informatics（美） | 无约束成分空间 ML 筛选 | 2014, 2020 | par.nsf.gov/servlets/purl/10292820 |
| Raabe/Neugebauer/Hongbin Zhang | MPIE+达姆施塔特工大（德） | 主动学习闭环高熵 Invar 合金 | 2022 | science.org/doi/10.1126/science.abo4940 |
| Wei Xu 许伟 | 东北大学 RAL（中） | 冶金引导 ML 超高强不锈钢 | 2019 | sciencedirect.com/…S1359645419305452 |
| Jinshan Li 李金山 | 西北工业大学（中） | 数据挖掘+深度学习钛合金 | 2021 | doi.org/10.1016/j.actamat.2020.10.056 |
| Shijun Zhao & Yang Yang | 香港城市大学（中） | 高熵陶瓷/催化剂、生成式共晶合金 | 2022–2024 | doi.org/10.1038/s41524-024-01385-5 |
| Jun Ni 倪军 | 清华大学（中） | 生成对抗网络 HEA 性质/成分探索 | 2025 | doi.org/10.1038/s41524-025-01548-y |
| 谢建新/付华栋/张洪涛 | 北京科技大学（中） | 可解释 ML 高端合金成分设计 | 2021–2024 | doi.org/10.1002/adma.202404478 |
| Lijun Zhang 张利军 | 中南大学（中） | CALPHAD+ML 铸造铝合金 | 2021, 2022 | oaepublish.com/articles/jmi.2021.10 |
| Tejs Vegge | DTU（丹麦） | BO 设计高熵合金电催化剂 | 2021 | doi.org/10.1002/anie.202108116 |
| Shyue Ping Ong | UCSD（美） | MEGNet 图网络/MLIP | 2019, 2025 | arxiv.org/abs/1812.05055 |
| Kristin Persson | LBNL/UC Berkeley（美） | Materials Project+催化剂 ML 筛选 | 2022, 2025 | doi.org/10.1038/s41563-025-02272-0 |
| Anubhav Jain | LBNL（美） | 工作流+NLP/LLM 合成规划 | 2022, 2024 | nature.com/articles/s41467-024-45563-x |
| Gerbrand Ceder | MIT/LBNL（美） | 钙钛矿描述符、A-Lab 自主合成 | 2018–2023 | doi.org/10.1038/s41586-023-06734-w |
| Chris Wolverton | 西北大学（美） | 成分向量通用性质预测 | 2014, 2016 | researchgate.net/publication/304641366 |
| Stefano Curtarolo | 杜克大学（美） | AFLOW+ML 势/性质 | 2012, 2024 | nature.com/articles/s41524-024-01321-7 |
| Logan Ward | 芝加哥大学（美） | Matminer 特征工程工具链 | 2016, 2018 | osti.gov/pages/biblio/1532339 |
| Kamal Choudhary | NIST/JHU（美） | JARVIS 数据+通用 ML | 2020, 2022 | nature.com/articles/s41524-020-00440-1 |
| Yousung Jung | 首尔国立大学（韩） | LLM 可合成性/材料设计 | 2024, 2025 | doi.org/10.1021/jacs.4c05840 |
| Atsuto Seko | 京都大学（日） | 成分推荐系统/ML 势 | 2017, 2018 | pubs.aip.org/…/241719 |
| Koji Tsuda/Ryo Tamura | 东京大学+NIMS（日） | PHYSBO BO/NIMS-OS 闭环 | 2022–2025 | arxiv.org/abs/2304.13927 |
| DeepMind GNoME | Google DeepMind（英/美） | 图网络新稳定成分发现 | 2023 | nature.com/articles/s41586-023-06735-9 |
| MatterGen | Microsoft Research（英/美） | 目标性质生成式成分设计 | 2023, 2025 | nature.com/articles/s41586-025-08628-5 |
| Rampi Ramprasad | 佐治亚理工（美） | Polymer Genome 聚合物成分设计 | 2018, 2023 | pmc.ncbi.nlm.nih.gov/articles/PMC9979603 |
| A. L. Greer | 剑桥大学（英） | 金属玻璃 ML+演化成分设计 | 2023 | doi.org/10.1039/D2DD00078D |
| Zachary Ulissi | CMU（美） | 主动学习电催化剂成分筛选 | 2018, 2022 | osti.gov/biblio/1543784 |
| Andrew I. Cooper | 利物浦大学（英） | 机器人化学家+BO 自主发现 | 2020, 2024 | nature.com/articles/s41586-020-2442-2 |

（注：表中机构/论文均经核实；上海交大、华南理工、中科院金属所未核实到相关代表性论文，故未入表。）
