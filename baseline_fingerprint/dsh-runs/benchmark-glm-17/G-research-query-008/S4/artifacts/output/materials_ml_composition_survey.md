# 机器学习/深度学习优化材料成分配比：课题组·算法·LLM 智能体调研

## 一、中国及华人活跃课题组（8 个，均有可核实来源）

1. **中南大学（粉末冶金国家重点实验室）｜张利军（Lijun Zhang，英文姓名已核实）**｜高熵/难熔合金 ML 设计、HT-CALPHAD
   - Gao T., …, Zhang L. *Data-driven design of novel lightweight refractory high-entropy alloys with superb hardness and corrosion resistance*, npj Comput. Mater. 10 (2024)。[链接](https://www.nature.com/articles/s41524-024-01457-6)
   - Yang S., …, Zhang L. *Revisit the VEC rule in high entropy alloys (HEAs) with high-throughput CALPHAD approach…*, Acta Mater. (2020)。[链接](https://www.sciencedirect.com/science/article/abs/pii/S1359645420302263)
2. **北京科技大学｜谢建新院士团队（Jianxin Xie）**｜性能导向 ML 合金设计、短流程钢
   - Wang C. et al. *A property-oriented design strategy for high performance copper alloys via machine learning*, npj Comput. Mater. 5 (2019)。[链接](https://www.nature.com/articles/s41524-019-0227-7)
   - 谢建新《机器学习在材料研发中的应用》，金属学报 57(11):1343 (2021)。[链接](https://www.ams.org.cn/article/2021/0412-1961/0412-1961-2021-57-11-1343.shtml)
   - 相关综述：Xu P. et al. *Multi-objective optimization in machine learning assisted materials design and discovery*, J. Mater. Inf. 5:26 (2025)（与谢团队的从属关系未逐条核实）。[链接](https://www.oaepublish.com/articles/jmi.2024.108)
3. **南方科技大学/香港科技大学（广州）｜张统一院士（Tong-Yi Zhang）**｜材料信息学、领域知识引导 ML、J. Mater. Inf. 主编
   - Xiong J., Shi S.Q., Zhang T.-Y. *A machine-learning approach to predicting and understanding the properties of amorphous metallic alloys*, Mater. Des. 187 (2020)。[学者主页](https://scholar.google.com/citations?user=73CwaSUAAAAJ&hl=zh-CN)
4. **香港城市大学｜杨涛（Tao Yang；资深合作者 C.T. Liu）**｜多组元/高熵合金 ML 计算设计
   - Zhao Y.M., Zhang J.Y., Liaw P.K., Yang T. *Machine Learning-Based Computational Design Methods for High-Entropy Alloys*, High Entropy Alloys Mater. 3:41-100 (2025)。[链接](https://scholars.cityu.edu.hk/en/publications/machine-learning-based-computational-design-methods-for-high-entr/)
5. **清华大学物理系｜倪军（Jun Ni）**｜小样本生成式 ML＋元素图神经网络
   - Sun Y.（孙一博）, …, Ni J. *EFTGAN: Elemental features and transferring corrected data augmentation for the study of high-entropy alloys*, npj Comput. Mater. (2025)。[DOI](https://doi.org/10.1038/s41524-025-01548-y)｜[系新闻](https://www.phys.tsinghua.edu.cn/info/1268/6313.htm)
   - 另：清华燃烧能源中心张亮副教授，ML 辅助高熵合金电催化剂设计。[链接](https://www.cce.tsinghua.edu.cn/info/1012/4567.htm)
6. **上海大学材料基因组工程研究院｜杨炯（Jiong Yang）**｜热电材料 ML 与逆向设计（TEID 框架）
   - 《人工智能在热电材料研究中的应用》，集成技术 (2025)。[链接](https://jcjs.siat.ac.cn/en/article/pdf/preview/10.12146/j.issn.2095-3135.20250715001.pdf)｜[学者主页](https://www.researchgate.net/profile/Jiong-Yang-8)
7. **中国科学院物理研究所｜孟胜（Sheng Meng）、刘淼（Miao Liu）等**｜生成式 AI＋材料合成预测
   - Chen Z. et al. *MatChat: A Large Language Model and Application Service Platform for Materials Science*, Chin. Phys. B 32:118104 (2023)。[链接](https://arxiv.org/abs/2310.07197)
8. **南洋理工大学（新加坡，华人学者）｜孙世静（Shijing Sun）**｜ML 闭环优化钙钛矿成分
   - Sun S. et al. *A data fusion approach to optimize compositional stability of halide perovskites*, Matter 4 (2021)。[链接](https://www.sciencedirect.com/science/article/pii/S2590238521000084)

补充：中科院上海硅酸盐所热电转换材料与器件课题组已设"AI＋热电材料"方向（[招聘页](https://www.sic.cas.cn/glbm/rlzyc/kygl/202605/t20260507_8196800.html)），代表性 ML 论文未核实。

## 二、算法与体系案例

**贝叶斯优化/主动学习**
- Xue D., Balachandran P.V., …, Lookman T. *Accelerated search for materials with targeted properties by adaptive design*, Nat. Commun. 7:11241 (2016)：NiTi 形状记忆合金；9 轮反馈×每轮 4 个成分＝36 次实验，从约 80 万候选成分中获 Ti₅₀.₀Ni₄₆.₇Cu₀.₈Fe₂.₃Pd₀.₂，热滞 ΔT=1.84 K；36 个新成分中 14 个优于初始 22 样本全部。[链接](https://www.nature.com/articles/ncomms11241)
- 同组压电：Xue D. et al., PNAS 113 (2016)（贝叶斯＋相图＋Landau-Devonshire，BaTiO₃ 基大电致应变）[链接](https://www.pnas.org/doi/10.1073/pnas.1607412113)；Yuan R. et al., Adv. Mater. 30:1702884 (2018) [链接](https://advanced.onlinelibrary.wiley.com/doi/abs/10.1002/adma.201702884)
- Trehern W. et al., Acta Mater. (2022)：AIMS 框架设计 SMA（最小相变区间＋≥50 MPa 下≥1.5% 驱动应变）。[链接](https://www.sciencedirect.com/science/article/abs/pii/S1359645422001379)
- FLARE：Vandermause J. et al. *On-the-fly active learning of interpretable Bayesian force fields*, npj Comput. Mater. 6 (2020)。[链接](https://www.nature.com/articles/s41524-020-0283-z)
- "Lookman 组用差分进化（DE）在单个实验批次内完成成分优化"的具体论文：**未核实**（DE 方法学见 Stokes Z. et al., Chemom. Intell. Lab. Syst. 199:103955 (2020) [链接](https://pmc.ncbi.nlm.nih.gov/articles/PMC7088454/)；Lookman 组综述：npj Comput. Mater. 5 (2019) [链接](https://www.nature.com/articles/s41524-019-0153-8)）
- Ishiyama T. et al. (2024)：贝叶斯优化提升多组元 III-V 多晶薄膜热电性能（Nature Portfolio npj 系列，刊名未能核实）。[链接](https://www.nature.com/articles/s41427-024-00536-w)

**遗传算法/NSGA-II 多目标**
- Xu P. et al., J. Mater. Inf. 5:26 (2025)：Pareto 前沿、NSGA-II、虚拟样本生成综述（链接同上）。
- Gao T. et al., npj Comput. Mater. 10 (2024)：ML＋多目标优化设计轻质难熔高熵合金（链接同上）。

**强化学习**
- *AIMATDESIGN: knowledge-augmented reinforcement learning for inverse materials design under data scarcity*, npj Comput. Mater. 12:74 (2026)。[链接](https://www.nature.com/articles/s41524-025-01894-x)

**GFlowNet 生成**
- AI4Science, Zhang D., Bengio Y. 等 *Crystal-GFN: sampling crystals with desirable properties and constraints*, NeurIPS 2023 / arXiv:2310.04925（按空间群→成分→晶格顺序生成）。[链接](https://arxiv.org/abs/2310.04925)
- Nguyen T.M. et al. *Hierarchical GFlowNet for Crystal Structure Generation*, NeurIPS 2023。[链接](https://openreview.net/pdf?id=HipfLjyLUW)

**CALPHAD＋ML 混合**
- Yang S., Zhang L., Acta Mater. (2020)：HT-CALPHAD 重审 VEC 规则（Al–Co–Cr–Fe–Ni，链接同上）。
- *How Can Machine Learning Accelerate CALPHAD Free Energy Models?* arXiv (2026)。[链接](https://arxiv.org/html/2606.01305v1)

**体系量化案例**
- 铝合金：Jiang L. et al., npj Comput. Mater. 9:26 (2023)：样本数据迁移 ML 设计出超高强高韧"E2"铝合金（作者单位未核实）。[链接](https://www.nature.com/articles/s41524-023-00979-9)
- 铜合金：Wang C. et al. (2019，链接同上）。
- 钙钛矿：Sun S. et al., Matter (2021)：闭环数据融合优化铅卤钙钛矿成分抗湿热降解稳定性（链接同上）。
- 介电聚合物：Mannodi-Kanakkithodi A. et al. *Machine Learning Strategy for Accelerated Design of Polymer Dielectrics*, Sci. Rep. 6:20952 (2016)。[链接](https://www.nature.com/articles/srep20952)
- NiTi 基高弹热合金 ML 设计：Metals 14:1193 (2024)。[链接](https://www.mdpi.com/2075-4701/14/10/1193)

## 三、LLM/智能体在材料设计与合成中的应用

- **Coscientist**：Boiko D.A. et al. *Autonomous chemical research with large language models*, Nature 624 (2023)：GPT-4 驱动，联网检索→方案规划→代码→机器人执行闭环；自主规划并经液体处理机器人执行钯催化偶联（Suzuki/Sonogashira）类反应，验证效能与可解释性。[链接](https://www.nature.com/articles/s41586-023-06792-0)
- **ChemCrow**：Bran A.M. et al. *Augmenting large language models with chemistry tools*, Nat. Mach. Intell. 6 (2024)：GPT-4＋18 个专家工具（合成规划等）。[链接](https://www.nature.com/articles/s42256-024-00832-8)｜[arXiv:2304.05376](https://arxiv.org/abs/2304.05376)
- **ChemLLM**：Zhang D. et al., arXiv:2402.06852 (2024)：化学专用 LLM（ChemData 指令微调＋ChemBench 评测），九大化学任务上与 GPT-4 相当。[链接](https://arxiv.org/abs/2402.06852)
- **MatChat**（中科院物理所）：LLaMA2-7B＋13,878 条结构化材料知识微调，预测无机材料合成路径（见第一节）；另见 LLM 驱动的端到端合成开发平台 (2026)。[链接](https://www.oaepublish.com/articles/cs.2026.35)
