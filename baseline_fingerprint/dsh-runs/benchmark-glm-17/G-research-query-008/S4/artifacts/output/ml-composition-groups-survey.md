# 机器学习优化材料成分配比（成分/成分–工艺→性能）：国际活跃课题组调研（18组）

链接均经 web_search / web_fetch 实见页面核实（检索时间 2026-03）；未使用禁用域名；个别未核实项已标注。

## 1. Shyue Ping Ong — UCSD Materials Virtual Lab
通用GNN原子间势（M3GNet/CHGNet生态）与成分→性质模型，支撑全元素空间高通量筛选与成分优化。
- C. Chen 等，Graph Networks as a Universal Machine Learning Framework for Molecules and Crystals，Chem. Mater.，2019. https://arxiv.org/abs/1812.05055
- C. Chen & S. P. Ong，A Universal Graph Deep Learning Interatomic Potential for the Periodic Table（M3GNet），npj Comput. Mater.，2022. https://doi.org/10.1038/s43588-022-00349-3

## 2. Gerbrand Ceder — MIT → 现 UC Berkeley/LBNL
ML势函数+自主合成实验室+文本挖掘前驱体推荐，打通成分–工艺–性能闭环（电池/固态材料）。
- B. Deng 等，CHGNet as a pretrained universal neural network potential for solid-state materials，Nat. Mach. Intell.，2023. https://www.nature.com/articles/s42256-023-00716-3
- N. J. Szymanski 等，An autonomous laboratory for the accelerated synthesis of novel materials，Nature，2023. https://www.nature.com/articles/s41586-023-06734-w
- T. He 等，Precursor recommendation for inorganic synthesis by materials similarity，Science Advances，2023. https://www.science.org/doi/10.1126/sciadv.adg8180

## 3. Kristin A. Persson — LBNL/UC Berkeley（Materials Project）
高通量DFT数据库 + 成分–性质基准评测（Matbench Discovery），面向全成分空间稳定性筛选。
- A. Jain 等，The Materials Project: A materials genome approach to accelerating materials innovation，APL Materials，2013. https://pubs.aip.org/aip/apm/article/1/1/011002/119685/Commentary-The-Materials-Project-A-materials
- J. Riebesell 等，A framework to evaluate machine learning crystal stability predictions，Nat. Mach. Intell.，2025. https://www.nature.com/articles/s42256-025-01055-1

## 4. Chris Wolverton — Northwestern（OQMD/Magpie）
OQMD数据库+Magpie成分描述子，全（无约束）成分空间的ML筛选与成分设计。
- B. Meredig 等，Combinatorial screening for new materials in unconstrained composition space with machine learning，Phys. Rev. B，2014. https://link.aps.org/doi/10.1103/PhysRevB.89.094104
- L. Ward 等，A general-purpose machine learning framework for predicting properties of inorganic materials，npj Comput. Mater.，2016. https://www.nature.com/articles/npjcompumats201628

## 5. James M. Rondinelli — Northwestern
功能氧化物/铁电与金属–绝缘体转变材料的物理信息ML筛选+主动学习。
- A. B. Georgescu 等，Database, Features, and Machine Learning Model to Identify Metal-Insulator Transition Compounds，Chem. Mater.，2021. https://pubs.acs.org/doi/10.1021/acs.chemmater.1c00905
- K. D. Miller 等，Decoratypes: An Extensible Crystal Taxonomy for Machine Learning-Guided Materials Discovery，Phys. Rev. Materials，2025. https://arxiv.org/abs/2509.07853

## 6. Anubhav Jain — LBNL（matminer/Matbench）
材料数据挖掘工具链与成分→性质基准（matminer、Matbench/Automatminer）。
- L. Ward 等，Matminer: An open source toolkit for materials data mining，Comput. Mater. Sci.，2018. https://www.sciencedirect.com/science/article/abs/pii/S0927025618303252
- A. Dunn 等，Benchmarking materials property prediction methods: the Matbench test set and Automatminer reference algorithm，npj Comput. Mater.，2020. https://www.nature.com/articles/s41524-020-00406-3

## 7. Kamal Choudhary — NIST（JARVIS）
JARVIS数据库+ALIGNN图神经网络，成分→性质预测与逆向材料设计。
- K. Choudhary 等，The joint automated repository for various integrated simulations (JARVIS) data repository，npj Comput. Mater.，2020. https://www.nature.com/articles/s41524-020-00440-1
- K. Choudhary 等，Atomistic Line Graph Neural Network for improved materials property predictions，npj Comput. Mater.，2021. https://www.nature.com/articles/s41524-021-00650-1

## 8. Rampi Ramprasad — Georgia Tech（Polymer Genome）
聚合物成分（单体/共聚配比）→性质信息学平台与逆向设计。
- C. Kim 等，Polymer Genome: A Data-Powered Polymer Informatics Platform for Property Predictions，J. Phys. Chem. C，2018. https://pubs.acs.org/jpccck/article/122/31/17575/1470511/Polymer-Genome-A-Data-Powered-Polymer-Informatics
- L. Chen 等，Polymer informatics: Current status and critical next steps，Prog. Mater. Sci.，2021. https://arxiv.org/abs/2011.00508

## 9. Turab Lookman — Los Alamos National Laboratory
主动学习/贝叶斯自适应实验设计，直接优化成分配比（掺杂压电陶瓷、形状记忆合金）。
- D. Xue 等，Accelerated search for materials with targeted properties by adaptive design，Nat. Commun.，2016. https://www.nature.com/articles/ncomms11241
- R. Yuan 等，Accelerated Discovery of Large Electrostrains in BaTiO3-Based Piezoelectrics Using Active Learning，Adv. Mater.，2018. https://doi.org/10.1002/adma.201702884
- T. Lookman 等，Active learning in materials science with emphasis on adaptive sampling using uncertainties for targeted design，npj Comput. Mater.，2019. https://www.nature.com/articles/s41524-019-0153-8

## 10. Ichiro Takeuchi — University of Maryland
组合薄膜+贝叶斯优化的自主闭环实验（成分–工艺→性能）。
- Y. K. Wakabayashi 等，Machine-learning-assisted thin-film growth: Bayesian optimization in molecular beam epitaxy of SrRuO3 thin films，APL Materials，2019. https://pubs.aip.org/aip/apm/article/7/10/101114/149090/Machine-learning-assisted-thin-film-growth
- A. G. Kusne 等，On-the-fly closed-loop materials discovery via Bayesian active learning，Nat. Commun.，2020. https://www.nature.com/articles/s41467-020-19597-w

## 11. Raymundo Arroyave — Texas A&M University
CALPHAD热力学+贝叶斯优化的合金成分设计与自主实验（含增材制造）。
- D. Khatamsaz 等，A physics informed Bayesian optimization approach for material design: application to NiTi shape memory alloys，npj Comput. Mater.，2023. https://www.nature.com/articles/s41524-023-01173-7
- D. Khatamsaz 等，Towards Autonomous Experimentation: Bayesian Optimization over Problem Formulation Space for Accelerated Alloy Development，arXiv，2025. https://arxiv.org/abs/2502.05735

## 12. Lijun Zhang（张利军）— Central South University（原吉林大学）
CALPHAD+机器学习集成的高熵合金/铸造铝合金成分设计。
- W. Yi 等，Efficient alloy design of Sr-modified A356 alloys driven by computational thermodynamics and machine learning，J. Mater. Sci. Technol.，2022. https://www.jmst.org/EN/10.1016/j.jmst.2021.09.061
- T. Gao 等，Data-driven design of novel lightweight refractory high-entropy alloys with superb hardness and corrosion resistance，npj Comput. Mater.，2024. https://www.nature.com/articles/s41524-024-01457-6

## 13. Tong-Yi Zhang（张统一）— HKUST/南方科技大学 → 现上海大学
材料信息学（J. Mater. Informatics 创刊主编）、AI材料生成与atomly.net数据库（atomly专门论文未核实）。
- T.-Y. Zhang，Informatics is fueling new materials discovery，J. Mater. Inform.，2021. https://www.oaepublish.com/articles/jmi.2021.09
- Z. Li 等（含 T.-y. Zhang），Materials Generation in the Era of Artificial Intelligence: A Comprehensive Survey，arXiv，2025. https://arxiv.org/abs/2505.16379
- 专著：T.-Y. Zhang，An Introduction to Materials Informatics，De Gruyter. https://www.ebooks.com/en-us/book/211176408/an-introduction-to-materials-informatics/tongyi-zhang/

## 14. Matthias Scheffler & Luca M. Ghiringhelli — FHI Berlin（NOMAD）
NOMAD数据库+描述子学习（SISSO符号回归），成分→相稳定性/性质的可解释建模。
- L. M. Ghiringhelli 等，Big Data of Materials Science: Critical Role of the Descriptor，Phys. Rev. Lett.，2015. https://link.aps.org/doi/10.1103/PhysRevLett.114.105503
- R. Ouyang 等，SISSO: A compressed-sensing method for identifying the best low-dimensional descriptors in an immensity of offered candidates，Phys. Rev. Materials，2018. https://link.aps.org/doi/10.1103/PhysRevMaterials.2.083802
- C. Draxl & M. Scheffler，The NOMAD Laboratory: from data sharing to artificial intelligence，J. Phys.: Mater.，2019. https://nomad-laboratory.de/uploads/publications/th/Draxl_2019_J._Phys._Mater._2_036001.pdf

## 15. Google DeepMind 材料团队（GNoME）
大规模GNN+主动学习发现新成分（220万新晶体、约38万稳定相）；团队公开论文集中于GNoME，其余未核实。
- A. Merchant 等，Scaling deep learning for materials discovery，Nature，2023. https://www.nature.com/articles/s41586-023-06735-9
- 代码/数据：https://github.com/google-deepmind/materials_discovery

## 16. Microsoft Research — MatterGen/MatterSim 团队
扩散生成模型按目标性质生成新成分与结构；通用机器学习原子级势。
- C. Zeni 等，A generative model for inorganic materials design（MatterGen），Nature，2025. https://www.nature.com/articles/s41586-025-08628-5
- H. Yang 等，MatterSim: A Deep Learning Atomistic Model Across Elements, Temperatures and Pressures，arXiv，2024. https://arxiv.org/abs/2405.04967

## 17. Citrine Informatics — Bryce Meredig
工业级材料信息学平台与"配方→性能"ML优化（Citrination）；Meredig 为Northwestern出身后创业。
- B. Meredig 等，Combinatorial screening for new materials in unconstrained composition space with machine learning，Phys. Rev. B，2014. https://link.aps.org/doi/10.1103/PhysRevB.89.094104
- J. E. Saal 等，Machine Learning in Materials Discovery: Confirmed Predictions and Their Underlying Approaches，Annu. Rev. Mater. Res.，2020. https://www.annualreviews.org/content/journals/10.1146/annurev-matsci-090319-010954

## 18. Preferred Networks — Matlantis/PFP
商用通用机器学习势（PFP），任意元素组合的高通量模拟与成分筛选。
- S. Takamoto 等，Towards universal neural network potential for material discovery applicable to arbitrary combination of 45 elements，Nat. Commun.，2022. https://www.nature.com/articles/s41467-022-30687-9
- C. Shinagawa 等，Matlantis-PFP v8: Universal Machine Learning Interatomic Potential with Better Experimental Agreements via r2SCAN Functional，arXiv，2026. https://arxiv.org/abs/2603.11063

---
备注：共18组（超出要求的15组下限）；每篇论文的标题/期刊/年份/一作均来自检索实见页面；Meredig 2014（PRB）为Northwestern与Citrine交叉成果，故两组均相关。
