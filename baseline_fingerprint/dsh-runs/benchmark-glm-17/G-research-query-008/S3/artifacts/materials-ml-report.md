# 机器学习/深度学习优化材料元素组合配比：研究进展与模型应用现状

> 范围：以"成分/配比优化（composition / stoichiometry optimization）"为核心的材料逆设计（inverse design）。方法涵盖代理模型+优化算法、生成式模型、机器学习原子间势（MLIP）+高通量筛选、闭环自驱动实验室。信息经网络检索核实，检索时间 2026 年末。

## 1. 问题定义与技术路线

- **正向问题**：给定元素配比 → 预测性能（形成能、带隙、硬度、强度、容量等）。
- **逆向设计**：给定目标性能 → 在巨大成分空间中搜索最优配比。高熵合金等多元体系的成分空间近乎无限，穷举不可行，因此 ML 成为必然选择。
- **四条主流技术路线**：
  1. **代理模型 + 全局优化**：用成分描述子（Magpie 等）或图神经网络训练性能预测器，再用贝叶斯优化（BO）、主动学习、遗传算法、强化学习搜索成分空间；
  2. **生成式模型**：条件扩散/VAE 直接生成满足性能约束的成分或晶体结构（CDVAE、MatterGen、GNoME）；
  3. **MLIP + 高通量筛选**：用 MACE/CHGNet/M3GNet 等近 DFT 精度势函数大规模筛选稳定成分（Matbench Discovery 范式）；
  4. **闭环自驱动实验室**：AI 提出成分 → 机器人合成与表征 → 数据回流再训练（A-Lab、松山湖"机器人材料科学家"）。
- **典型材料体系**：高熵合金/Invar 合金、形状记忆合金、Ni 基高温合金、镁/铝合金、钙钛矿（光伏/热电）、锂电池正极与固态电解质、高熵陶瓷、催化剂、非晶合金。

## 2. 活跃研究课题组

### 国际

| 机构 | PI | 研究方向 | 代表工作 |
|---|---|---|---|
| UC Berkeley / LBNL（原 MIT） | Gerbrand Ceder | 高通量 DFT、Materials Project 联合创始人、自主合成 | A-Lab（Nature 2023）、CHGNet 通用势 |
| UC San Diego | Shyue Ping Ong | 图网络、通用 MLIP、材料数据库工具链 | M3GNet（Nat. Comput. Sci. 2022）、pymatgen/matminer |
| UC Berkeley / LBNL | Kristin Persson | Materials Project、数据基础设施 | Materials Project（Jain 2013） |
| Northwestern | Christopher Wolverton | 高通量 DFT + ML、成分特征工程 | OQMD、Magpie 特征（Ward 2016）、无约束成分空间组合筛选（Meredig & Wolverton PRB 2014） |
| MIT | Tonio Buonassisi | 闭环贝叶斯优化、光伏材料 | 钙钛矿电池闭环 BO（与 Atinary SDLabs 无代码平台合作）；过程优化知识约束 BO（Liu 2022，被引 270+） |
| LANL | Turab Lookman（现职待核实） | 主动学习/自适应实验设计 | Xue 2016（Nat. Commun.，NiTi 形状记忆合金闭环）；Lookman 2019 主动学习综述；Wen 2019 合作者 |
| Univ. of South Carolina | Jianjun Hu | 成分 ML、材料逆向设计 | k-fold 前向交叉验证、成分对称性预测、GAN 采样成分空间 |
| Caltech | John Gregoire | 高通量组合实验、太阳能燃料材料 | CuO–V2O5 体系光电极高通量发现（Adv. Energy Mater. 2015） |
| KAIST | Yousung Jung | 生成式材料设计、LLM | CDVAE（ICLR 2022）；LLM 预测无机合成（JACS 2024） |
| 东京大学 | Koji Tsuda | ML 材料、贝叶斯优化、AI+机器人闭环 | COMBO BO 库（2016）；NIMS-OS 自动化闭环软件（STAM Methods 2023） |
| 京都大学 | Isao Tanaka / Atsuto Seko | 描述子 ML、化合物筛选 | Seko 2014 系列 |
| 马普钢铁研究所（MPIE） | Dierk Raabe / Jörg Neugebauer / Fritz Körmann | 钢铁与高熵合金计算+ML | Rao et al. Science 2022（高熵 Invar 主动学习） |
| 多伦多大学 | Alán Aspuru-Guzik | 自驱动实验室 | Acceleration Consortium（2024 获 2 亿加元） |
| Duke | Stefano Curtarolo | AFLOW 高通量数据库 | AFLOW 生态 |
| Microsoft Research / DeepMind | — | 大规模生成与发现 | GNoME（Nature 2023）、MatterGen（Nature 2025） |

### 中国

| 机构 | 团队/PI | 研究方向 | 代表工作 |
|---|---|---|---|
| 中科院物理所 / 东莞材料所（所长） | 汪卫华（院士）、柳延辉 | 非晶/高熵合金 ML 成分设计、Atomly 数据库、数智研发平台 | Atomly（35 万+，物理所+松山湖共建）；柳延辉"智能设计-自动制备-自动表征"闭环平台（2025） |
| 香港城市大学 | 吕坚（讲座教授）、杨韬、刘锦川 | 高熵/非晶/超纳结构材料+计算模拟 | 晶体-玻璃高熵纳米复合材料（Adv. Mater. 2020）；HEA 综述（Mater. Today 2016） |
| 北京科技大学（北京材料基因工程高精尖中心） | 谢建新（主任）、宿彦京、吕昭平/刘雄军 | 材料基因工程、可解释 ML、HEA 成分 ML | **Wen 2019**（北科大+西安交大+力学所+LANL 合作）；Ti-Zr-Nb-Ta 难熔 HEA 目标硬度 ML（APL 2021）；可解释 ML 综述（AFM 2025）；高铁车轴钢/LNG 钢成分优化 |
| 上海交通大学 | 饶梓元 | ML+理论+实验合金设计 | Rao 2022 Science 一作（高熵 Invar、镁合金耐蚀） |
| 中科院金属所 | 刘轶 | ML 辅助高通量实验加速硬质高熵合金成分设计 | 机器学习+高通量实验系列 |
| 松山湖材料实验室 / 中科院东莞材料与所 | 胡远超（数据驱动团队） | 复杂无序材料、数据驱动材料设计 | "机器人材料科学家"：设计-合成-表征-迭代 7×24 无人化闭环；Atomly+GPTFF+MatChat |
| 清华大学 | 倪军（物理系）、张亮（燃烧能源中心） | 小样本生成式 ML；高熵电催化剂分层 ML | EFTGAN（npj Comput. Mater. 2025，GAN 数据增强）；HS2C-ML 分层框架（AFM 2026，筛 1.6 万种五元 HEA，制得碱性析氢过电位 26 mV@10 mA/cm² 的 CuZnPtRuRh） |
| 南京理工大学 | 材料学院团队 | ML 加速高熵合金相结构设计 | JMST 报道 |
| 南方科技大学 | 张文清（讲席教授） | ML 势函数、高效数据采样 | SUS-2-MLIP、半哈斯勒通用势+声子输运（论文 DOI 待核实） |
| 中南大学 | 李志明 等 | 先进钢铁/高熵合金 | Rao 2022 合作单位；难熔 HEA ML 综述（2024） |
| 北京航空航天大学 | 孙志梅 | 高通量集成计算+ML 势函数 | ALKEMIE 平台；Sb₂Te₃ 跨尺度 ML 势"Potential Mind"（能量精度 99.8% vs DFT） |
| 北京科学智能研究院（AISI）/ DeepModeling 社区 | 鄂维南、王涵等 | DPA 系列通用势函数、AI for Science 基础模型 | DPA-4.1 居 Matbench Discovery 榜首（F1≈0.93） |
| 上海科技大学 | TECE 团队 | 通用机器学习势 | TECE-OAM 进入榜单前列 |
| 深势科技（企业） | — | AI for Science 计算平台 | Bohrium、DeepMD/DPA 商业化 |

## 3. 代表性论文与里程碑

1. **Meredig & Wolverton 2014**（PRB）与 **Ward et al. 2016**（npj Comput. Mater.）：无约束成分空间的 ML 组合筛选与 Magpie 通用成分特征——成分-only 预测的奠基工作。
2. **Raccuglia et al. 2016**（Nature）：利用"失败实验"数据训练 ML，证明负样本价值。
3. **Xie & Grossman 2018**：CGCNN 晶体图网络，结构-性能深度学习开端。
4. **Goodall & Lee 2020**：Roost 成分图网络，成分-only 形成能预测标杆。
5. **Xue et al. 2016**（Nat. Commun.）：自适应设计（贝叶斯+GP），80 万候选成分空间中 9 轮闭环、36 次实验找到目标 NiTi 基形状记忆合金（Ti50Ni46.7Cu0.8Fe2.3Pd0.2）——闭环成分优化的开山之作。
6. **Wen et al. 2019**（Acta Mater.，被引 1000+；北科大宿彦京+西安交大薛德祯+力学所+LANL 合作）：ML 代理 + 实验设计算法搜索高熵合金，少量实验即获得硬度超过训练集最优 10% 的合金。
7. **Rao et al. 2022**（Science，被引 870+）：MPIE 团队用主动学习在"近乎无限"成分空间中发现高熵 Invar 合金，闭环 ML+CALPHAD+实验。
8. **Merchant et al. 2023**（Nature，GNoME，被引 2500+）：深度学习发现 220 万新晶体，其中 38.1 万个相对 Materials Project 稳定。
9. **Szymanski et al. 2023**（Nature，A-Lab，被引 1700+）：17 天自主合成 41/58 个目标化合物（约 71%）；外部复核对其"新化合物"认定提出质疑（复核结论"未发现新材料"），Nature 于 2026-01 发文更正（Erratum）但核心争议未解。
10. **Zeni et al. 2025**（Nature 639, 624–632，MatterGen，被引 1200+）：扩散生成模型，可按化学/对称性/力-电-磁性质条件微调；生成的"稳定、唯一、新颖（SUN）"材料比例较基线翻倍以上，实验合成验证 1 个生成结构；已 MIT 开源并进入 Azure AI Foundry。
11. **Matbench Discovery（2023–）**：评估 ML 能量模型作为稳定性预筛器的框架（WBM 外推测试集）。
12. **中文综述**：李俊炎等 2025《材料导报》"机器学习辅助高熵合金设计的研究进展"；RSC Digital Discovery 2025"冶金知识嵌入的贝叶斯优化"综述。

**近三年趋势（2023–2026）**：成分配比优化正从"ML 预测+主动学习筛选"转向**"生成式模型（MatterGen/GNoME）＋全周期表基础模型（M3GNet/CHGNet/MatterSim）＋自驱动实验室闭环（A-Lab/NIMS-OS/松山湖）"三位一体的自主发现范式**。具体表现：
1. **范式从"预测"转向"生成"**：MatterGen/GNoME 把成分-结构生成做成基础模型，属性条件化生成成为主流；
2. **通用 MLIP 军备竞赛**：MPtrj/OMat24 等大规模轨迹数据 + MACE/DPA 类架构，Matbench Discovery 竞争白热化（58 个模型上榜，榜首 F1≈0.93）；
3. **LLM 与智能体进场**：Coscientist（GPT-4 多智能体自主实验）、MatChat 材料智能体、Microsoft Discovery 企业级 agentic 科研平台、LLM 预测无机合成（JACS 2024）；
4. **闭环硬件升级**：A-Lab、松山湖"机器人材料科学家"把"设计-合成-表征-迭代"做成 7×24 无人化产线；
5. **知识回归**：冶金/热力学知识嵌入 BO 与约束生成，对抗纯黑箱的外推失效；
6. **数据基础设施国家化**：中国材料基因工程专项、NOMAD/FAIRmat、Atomly 等自主数据库加速建设；中国团队在高熵合金/非晶成分优化上形成特色集群（北科大、上海交大、物理所、清华、松山湖等）。

## 4. 数据库

| 数据库 | 维护方 | 规模（约） | 类型 | 在成分优化中的用途 |
|---|---|---|---|---|
| Materials Project | LBNL/MIT | 15 万+ 条目（3 万+ 稳定） | DFT | 形成能/带隙训练、稳定性参照 |
| OQMD | Northwestern | 140 万+ | DFT | 高通量筛选、Roost 训练集 |
| AFLOW | Duke | 393 万化合物、8.17 亿计算性质 | DFT | 稳定性/热力学 |
| JARVIS | NIST | 8 万+ 材料 | DFT | 多性质基准、ALIGNN 基线 |
| NOMAD | EU（FHI 发起/FAIRmat） | 约 1900 万条目（400 万+ 材料）、>1 亿次计算 | 共享计算数据 | 复用/挖掘、模型训练语料 |
| GNoME DB | DeepMind | 220 万相对 MP 稳定、38.1 万在凸包上 | DFT（图网络发现） | 新候选库 |
| Alexandria | 波鸿鲁尔大学 ICAMS | 580 万结构、17.5 万在凸包上 | DFT | MLIP 训练、生成模型新颖性对照 |
| C2DB | 丹麦 DTU | 15,733 个二维材料 | DFT | 二维成分筛选 |
| Citrination | Citrine | 企业+公开混合（Open Citrination 已停用） | 实验+计算 | 工业 ML 工作流平台（历史地位） |
| MatWeb | 商业 | 20 万+ 数据表 | 实验手册数据 | 实验性能对照 |
| NIMS MatNavi | 日本 NIMS | 10 个子库（PoLyInfo/AtomWork 等） | 实验+计算+CALPHAD | 文献物性核对 |
| HTEM | NREL | 14 万+ 样本（2021 论文口径 17.4 万含表征） | 高通量实验（薄膜） | 成分-性能实验关联 |
| Pauling File / SpringerMaterials | MPDS | 约 200 万条数据条目 | 实验 | 相图/结构核对 |
| MatBench | LBNL | 13 个任务（mp_e_form 13.3 万条、steels 312 条） | 基准 | 模型公平评测 |
| Atomly | 中科院物理所 + 松山湖 | 35 万+ 条目 | DFT（自研） | 机器人科学家闭环、稳定性评估/反应路径 |
| 中国材料基因工程数据平台 | 科技部重点专项（2015 起，45 个项目、约 30 亿元、400+ 单位）；北科大高精尖中心、上海材料基因组研究院、物理所怀柔平台、深圳材料基因组大平台；MatCloud/OCPMDM 引擎；CSTM 标准委员会（2017）+ 首个通则标准（2019） | 多中心 | 计算+实验 | 国产数据底座（如 MLDS 高强高导铜合金 800 MPa/50% IACS） |

## 5. 模型与准确度评估

| 模型/方法 | 类型 | 任务 | 典型精度（已核实，MatBench 官方 5 折） |
|---|---|---|---|
| MODNet | 成分特征+神经网络 | 形成能（成分-only 榜首） | MAE 0.0448 eV/atom |
| Finder / CrabNet | 成分网络 | 形成能（成分-only） | MAE 0.0839 / 0.0862 eV/atom |
| Magpie + RF | 成分特征+树 | 形成能 | MAE 0.1165 eV/atom |
| Roost | 成分图网络 | 形成能（OQMD 25.7 万条、10% 留出） | ensemble MAE 0.0241 eV/atom（RF+Magpie 0.067、ElemNet 0.055）；实验带隙 0.243 eV |
| MODNet | 成分-only | 实验带隙（4,604 样本） | MAE 0.33 eV |
| TPOT-Mat / MODNet | 成分-only | 钢屈服强度（312 样本） | MAE 79.9 / 87.8 MPa |
| ALIGNN | 结构图网络 | 形成能/带隙/钙钛矿 | MAE 0.0215 eV/atom、0.1861 eV、0.0288 eV/cell |
| MEGNet / CGCNN | 结构图网络 | 形成能（MP 6.9 万晶体）/带隙 | MAE 0.032 eV/atom / 0.2972 eV |
| coGN | 结构图网络 | 形成能（MatBench 结构类榜首） | MAE 0.0170 eV/atom |
| MACE/CHGNet/M3GNet/DPA | MLIP | 能量与稳定性 | 能量 MAE：MACE ~6.2、CHGNet ~24–30、M3GNet <30 meV/atom；Matbench Discovery 58 个模型，榜首 F1 ≈0.93、MAE ≈17 meV/atom、DAF ≈6 |
| 代理模型（小数据实验集） | RF/GP/GBDT | HEA 屈服强度 | R² ~0.78–0.94（数据集 181–数百条） |
| 生成式（MatterGen/GNoME） | 扩散/图网络 | 候选生成 | MatterGen："新颖且稳定"比例为基线 2 倍+、距局部能量极小近 15 倍+；GNoME 220 万相对稳定结构 |
| 主动学习闭环 | — | 实验效率 | Xue 2016：80 万候选空间中 9 轮闭环、36 次实验找到目标合金（搜索空间压缩约 2 万倍）；Wen 2019、Rao 2022 类似 |

**评估方法**：MatBench 官方固定 5 折交叉验证（区分成分/结构输入）；留出测试（Roost：OQMD 10% 留出；Matbench Discovery 另设 WBM 外推集）；不确定性量化（高斯过程、深度集成，Roost ensemble 0.0297→0.0241）；闭环实验验证（最终金标准）；负样本纳入（Raccuglia 2016：失败反应数据训练后对新反应成功率预测达 89%，超过人类专家策略）。注意：文献精度多为"内插"精度，外推到训练分布之外性能显著下降。

## 6. 面临的挑战

1. **小样本与发表偏倚**：成功案例发表、失败数据缺失，导致模型偏乐观；Raccuglia 2016 证明失败数据可显著提升精度（npj Comput. Mater. 2023 综述；Nature 2024 关于负面结果发表难的报道）。
2. **外推能力弱**：成分空间近乎无限，模型仅在内插区可靠；系统评测发现"多数所谓 OOD 测试实为内插，高估泛化能力"（npj Comput. Mater. 2024）。
3. **成分-only 的局限**：真实性能取决于"成分-工艺-组织-性能"全链条；忽略加工历史、缺陷、相分数与亚稳结构的模型在结构合金上失效（RSC DD 2025 提出冶金知识嵌入 BO 缓解）。
4. **可合成性预测不成熟**：synthesizability 分类器仍是研究热点而非可靠工具；GNoME/MatterGen 生成候选的合成验证率低，且有后续研究批评生成模型部分产出"复现训练集已知化合物"（Mater. Horiz. 2026，待核实原文）。
5. **多目标优化**：工业需求几乎都是多目标（强度-韧性-成本-可加工性），Pareto 前沿搜索难度高（J. Mater. Inf. 2024 综述）。
6. **不确定性量化不足**：多数论文只报点估计，决策风险不可控（贝叶斯神经网络等方案仍在研究阶段）。
7. **数据标准化（FAIR）不足**：单位、测试条件、批次信息不一致，跨库融合成本高（CODATA 2026）；产业侧障碍还包括技能差距与文化阻力。
8. **DFT-实验系统误差**：以 DFT 数据训练的模型直接预测实验性能存在偏差（Phys. Rev. Materials 2024 对 PBE/杂化泛函 vs 实验生成能的系统对比）。
9. **验证成本与通量**：闭环实验设备昂贵、表征速度成为瓶颈；A-Lab 争议（复核认为"未发现新材料"，Nature 2026-01 更正）直接暴露"自主合成结果可信度"问题。
10. **可解释性与领域接受度**：冶金学家对黑箱推荐的信任有限；"从预测到理解"被列为当前中心挑战（npj Comput. Mater. 2022 XAI 综述）。

## 7. 模型可行性分析（分路线）

| 路线 | 成熟度（TRL 估计，分析性） | 可行性判断 |
|---|---|---|
| 代理模型 + BO/主动学习 | 6–8 | **最可行**。小数据友好、可嵌入专家约束、已有企业落地（松下/昭和电工/Cabot/Syensqo）；适合有实验闭环的团队。局限：单点优化、外推弱、跨体系迁移差。 |
| 生成式模型 | 3–4 | 研究热点。候选生成能力突破性（GNoME 38 万稳定结构），但仅论文级验证（MatterGen 实验合成 1 例）、无工业闭环验证，且受"复现训练集化合物"批评；适合"候选库扩充"而非直接交付配方。 |
| MLIP + 高通量筛选 | 5–7 | 对晶体稳定性/亚稳筛选可靠（近 DFT 精度、低成本），但对成分配比优化是间接手段；适合无机晶体类。 |
| 自驱动实验室 | 4–6（分域） | 小分子合成/配方演示较成熟（Coscientist、Acceleration Consortium）；固相无机合成可信度存争议（A-Lab 纠偏）；商业模式未跑通（ECL 关停、IBM RXN 停服）。是未来 5–10 年的关键放大器。 |

**体系维度**：性能指标明确且可快速表征（硬度、相形成、带隙、电池容量）的体系可行性最高；强工艺依赖、长周期性能（疲劳、蠕变、断裂韧性、耐蚀）可行性低。

## 8. 距离大规模应用与产业化的评估

**已落地的产业化证据**：
- Citrine Informatics：松下（有机电子材料：4 个新分子、其一空穴迁移率 +25%）、昭和电工（Showa Denko，溶剂配方 5 个月评估 >1 亿组合）；累计融资约 5200 万美元；
- QuesTek International：Ferrium M54/S53 系**ICME 设计**（NIST 以其作为上市周期基线），近年以 ICMD SaaS 平台与 ML/AI 增强（2024 年称用于新型高强铝合金设计）；
- Uncountable：Cabot 案例"测试到结果周期缩短 50%+"，2025-06 获 2700 万美元 A 轮（超额认购）；
- Albert Invent：客户含 AkzoNobel/BASF/Henkel 等，2026-10 获 5500 万美元 B 轮；已进入 Gartner 材料信息学方案评测类别；
- Microsoft MatterGen：Nature 2025 发表时实验合成验证 1 个生成结构；MIT 开源、进入 Azure AI Foundry 模型目录、企业级平台 Microsoft Discovery；2025 年与 Syensqo 签 MoU，2026-04 扩展阶段称"创新周期从数年压缩到数月"（半导体传热流体）；
- Microsoft × PNNL：AI+HPC 从 3200 万候选中数周内锁定并合成新固态电解质 N2116（锂用量减少约 70%，已做成原型电池）；
- 深势科技：Bohrium 平台 + DeepMD/DPA 商业化，2025-12 C 轮超 8 亿元人民币；
- 中国材料信息化企业：创腾科技（ELN/AI 材料设计）、鸿之微（Physics AI 材料智能研发平台）；Atinary（无代码 BO 平台，MIT 钙钛矿闭环）；
- 多伦多 Acceleration Consortium 2024 年获 CFREF 2 亿加元资助，建设规模化自驱动实验室；
- 松山湖"机器人材料科学家"接入 Atomly 数据库与 GPTFF 力场。

**自驱动实验室的警示信号**（产业化难度的直接证据）：A-Lab 论文 2026-01 被 Nature 发文更正，核心争议未解；Emerald Cloud Lab 加州实验室 2023 年永久关闭；IBM RXN for Chemistry 云服务 2026-10 停止（EOL）——闭环自动化平台的商业模式尚未跑通。

**市场规模信号**：全球材料信息学市场 2025 年约 1.7 亿美元 → 2030 年约 4.1 亿美元（CAGR 19.2%，MarketsandMarkets）；IDTechEx 估计 2037 年外部服务约 6 亿美元——绝对值小、增速高，说明仍处早期导入期。

**主要瓶颈（按影响排序）**：① 高质量专有实验数据稀缺且不共享；② 候选验证的实验通量与成本；③ 模型外推与可合成性预测不可靠；④ 与企业现有研发流程/标准集成度低；⑤ 材料+AI 复合人才短缺；⑥ 数据 IP 与共享机制未理顺。

**时间线判断**（综合文献、业界表述与市场预测；"5–10 年"类结论为分析性综合，非单一出处）：
- 现在–3 年：AI 辅助成分设计成为头部企业研发"标配工具"（代理模型+BO 路线已达到；Syensqo 称"数年→数月"）；
- 3–7 年：生成式模型 + 自驱动实验室组合在特定体系（电池材料、催化剂、高熵合金）实现"周级"闭环发现，出现规模化商业平台；
- 7–15 年：跨体系通用的"理想模型"（输入多目标性能 → 输出可合成、可放大生产的最优配比与工艺窗口）仍需数据基础设施、可合成性理论与标准化流程的同步成熟。
- 参照系：Mission Innovation IC6 报告（2018）设想"研究的摩尔定律"（研究速率每两年翻倍）；美国工程院 MGI 专辑设想"未来十年"内 SDL 自主设计聚合物；市场预测（2030 年约 4.1 亿美元、2037 年约 6 亿美元）隐含未来 5–10 年材料信息学仍属低速渗透的利基市场。

**结论**：该领域已跨过"概念验证"阶段，进入"单点落地、体系受限"的早期产业化阶段：代理模型+BO 路线（TRL 6–8）已在头部企业常态化使用；生成式模型与自驱动实验室（TRL 3–6）仍处"论文级/试点级"。距离理想模型（输入多目标性能 → 输出可合成、可放大生产的最优配比与工艺窗口）的大规模应用，核心差距不在算法（成分-only 与结构模型的预测精度已接近数据噪声与 DFT 误差极限），而在**数据（规模、质量、共享）、验证（实验通量与可合成性）与工程化（流程集成、标准、人才）**。综合判断：5–10 年内 AI 成分设计将覆盖大部分新材料的研发前端并成为标配；端到端"无人化"材料研发的大规模产业化仍需 10 年以上，且高度依赖数据基础设施与自驱动实验室成本的同步下降。

## 9. 主要参考来源

- MatterGen：https://www.nature.com/articles/s41586-025-08628-5 ；https://www.microsoft.com/en-us/research/blog/mattergen-a-new-paradigm-of-materials-design-with-generative-ai/
- GNoME：https://www.nature.com/articles/s41586-023-06735-9 ；https://deepmind.google/blog/millions-of-new-materials-discovered-with-deep-learning/
- Rao et al. 2022：https://www.science.org/doi/10.1126/science.abo4940 （MPIE，Raabe/Neugebauer 团队）
- A-Lab：https://pmc.ncbi.nlm.nih.gov/articles/PMC10700133/ ；争议：https://www.chemistryworld.com/news/new-analysis-raises-doubts-over-autonomous-labs-materials-discoveries/4018791.article
- Wen et al. 2019：https://www.sciencedirect.com/science/article/abs/pii/S1359645419301430
- MatBench：https://matbench.materialsproject.org/ ；Matbench Discovery：https://matbench-discovery.materialsproject.org/ ；论文：https://nature.com/articles/s42256-025-01055-1 ；arXiv 版：https://arxiv.org/html/2308.14920v3
- Citrine × 松下：https://citrine.io/technical-case-study-machine-learning-accelerates-materials-development-for-panasonic/
- Microsoft × PNNL：https://news.microsoft.com/source/features/innovation/how-ai-and-hpc-are-speeding-up-scientific-discovery/ ；https://azure.microsoft.com/en-us/blog/quantum/2024/01/09/unlocking-a-new-era-for-scientific-discovery-with-ai-how-microsofts-ai-screened-over-32-million-candidates-to-find-a-better-battery/ ；BBC：https://www.bbc.com/news/technology-67912033
- Acceleration Consortium：https://acceleration.utoronto.ca/ ；2 亿加元资助：https://accelerationconsortium.substack.com/p/u-of-ts-acceleration-consortium-receives
- 材料信息学市场：https://www.precedenceresearch.com/materials-informatics-market
- 松山湖机器人材料科学家：https://dimst.cas.cn/AI/202511/t20251127_8017807.html ；Atomly：https://atomly.matchat.cn/ ；https://www.iop.cas.cn/xwzx/kydt/202207/t20220720_6483007.html
- 清华倪军组高熵合金 ML：https://www.phys.tsinghua.edu.cn/info/1268/6313.htm
- QuesTek（ICME）：https://questek.com/webinars/ ；Albert Invent：https://www.albertinvent.com/ ；Uncountable：https://www.uncountable.com/informatics-what-is-materials-informatics
- 中文综述（高熵合金 ML）：https://www.mater-rep.com/CN/abstract/abstract7790.shtml ；科学网 HEA ML 综述：https://news.sciencenet.cn/htmlpaper/2025/9/202593162142326139210.shtm
- 冶金知识嵌入 BO 综述：https://pubs.rsc.org/dd/article/5/9/3474/1290072/
- 深势科技：https://www.dp.tech/ ；Bohrium：https://www.dp.tech/product/bohrium/workspace
- uMLIP 基准：https://pubs.acs.org/jctcce/article/21/16/8142/3693403/
- 数据库规模：OQMD https://www.oqmd.org/ ；AFLOW https://www.aflowlib.org/ ；JARVIS https://jarvis.nist.gov/ ；MP https://next-gen.materialsproject.org/
- Atinary × MIT 钙钛矿闭环：https://atinary.com/use-cases/mit-no-code-bayesian-optimization-perovskite/ ；知识约束 BO：https://www.sciencedirect.com/science/article/pii/S2542435122001301
- 挑战文献：小数据综述 https://www.nature.com/articles/s41524-023-01000-z ；OOD 评测 https://www.nature.com/articles/s43246-024-00731-w ；可合成性 https://pubs.acs.org/acsodf/article/8/9/8210/344172/ ；多目标 https://www.oaepublish.com/articles/jmi.2024.108 ；XAI https://www.nature.com/articles/s41524-022-00884-7 ；DFT-实验误差 https://link.aps.org/doi/10.1103/PhysRevMaterials.8.043803
- 产业化案例：Citrine-Showa Denko https://citrine.io/case-study-solvent-blend-discovery-accelerated/ ；Uncountable-Cabot https://www.casestudies.com/company/uncountable/case-study/cabot-corporation-cuts-test-to-results-time-50-with-uncountable ；Albert Invent B 轮 https://www.albertinvent.com/press-release-post/albert-raises-55m-series-b-to-scale-the-first-chemistry-native-ai ；QuesTek https://questek.com/products-client-services/alloy-design/
- MatterGen 生态：Azure 目录 https://ai.azure.com/catalog/models/MatterGen ；Syensqo MoU https://www.syensqo.com/en/press-release/syensqo-and-microsoft-sign-memorandum-understanding ；扩展 https://www.plastech.pl/en/news/syensqo-to-scale-ai-driven-discovery-and-growth-with-22172
- A-Lab 更正（C&EN 2026-01）：https://cen.acs.org/research-integrity/Nature-robot-chemist-paper-corrected/104/web/2026/01 ；Coscientist https://www.nature.com/articles/s41586-023-06792-0 ；IBM RoboRXN https://research.ibm.com/blog/roborxn-automating-chemical-synthesis
- 市场与 TRL：MarketsandMarkets https://www.marketsandmarkets.com/PressReleases/material-informatics.asp ；IDTechEx https://www.idtechex.com/en/research-report/materials-informatics/1183 ；MLTRL 框架 https://www.nature.com/articles/s41467-022-33128-9
- 中国企业：鸿之微 https://www.hzwtech.com/ ；创腾科技 https://www.neotrident.com/ ；深势科技融资 https://www.iyiou.com/news/202512241117948
- 模型论文：Roost https://www.nature.com/articles/s41467-020-19964-7 ；Xue 2016 https://www.nature.com/articles/ncomms11241 ；Raccuglia 2016 https://www.nature.com/articles/nature17439 ；CGCNN https://link.aps.org/doi/10.1103/PhysRevLett.120.145301 ；Magpie https://www.nature.com/articles/npjcompumats201628 ；ALIGNN https://arxiv.org/abs/2106.01829 ；MEGNet（Nat. Commun. 2019）；CDVAE https://arxiv.org/abs/2110.06197 ；M3GNet https://www.nature.com/articles/s43588-022-00349-3 ；CHGNet https://arxiv.org/abs/2302.14231 ；MatterSim https://arxiv.org/abs/2405.04967 ；MACE/M3GNet 基准 https://arxiv.org/html/2510.22999v2
- MatBench 分任务榜：mp_e_form https://matbench.materialsproject.org/Leaderboards%20Per-Task/matbench_v0.1_matbench_mp_e_form/ ；steels https://matbench.materialsproject.org/Leaderboards%20Per-Task/matbench_v0.1_matbench_steels/
- 数据库官网：NOMAD https://nomad-lab.eu/ ；MatWeb https://www.matweb.com/ ；MatNavi https://mits.nims.go.jp/en/ ；Alexandria https://alexandria.icams.rub.de/ ；C2DB https://c2db.fysik.dtu.dk/ ；HTEM https://www.sciencedirect.com/science/article/pii/S266638992100235X ；MPDS https://tutorial.mpds.io/ ；北科大材料数据库 https://bjmge.ustb.edu.cn/yanjiuduiwu/yanjiutuandui/cljxgczysjk/clsjk/
- 课题组主页/论文：A-Lab DOI 10.1038/s41586-023-06734-w ；Wen 2019 DOI 10.1016/j.actamat.2019.03.010 ；COMBO https://www.sciencedirect.com/science/article/pii/S2352924516300035 ；NIMS-OS DOI 10.1080/27660400.2023.2232297 ；JACS LLM 合成预测 DOI 10.1021/jacs.4c05840 ；Seko PRB https://link.aps.org/doi/10.1103/PhysRevB.95.144110 ；Gregoire https://gregoire.people.caltech.edu/ ；城大吕坚 https://www.hkias.cityu.edu.hk/zh-cn/our-people/senior-fellows/professor-jian-lu ；上交饶梓元 https://smse.sjtu.edu.cn/people/detail_new/20436 ；柳延辉数智平台 https://www.iop.cas.cn/xwzx/kydt/202511/t20251107_8008239.html ；USTB APL 2021 DOI 10.1063/5.0065303 ；USTB AFM 2025 DOI 10.1002/adfm.202507734 ；EFTGAN DOI 10.1038/s41524-025-01548-y ；清华张亮 HS2C-ML https://www.cce.tsinghua.edu.cn/info/1012/4567.htm ；南科大张文清 https://www.sustech.edu.cn/zh/faculties/zhangwenqing.html ；松山湖胡远超 https://www.gaoxiaojob.com/announcement/detail/329415.html ；北航 Potential Mind https://mse.buaa.edu.cn/info/1064/1806.htm
- Jianjun Hu 主页：https://www.cse.sc.edu/~jianjunh/ ；中国工程院 Engineering 生成式材料综述：https://www.engineering.org.cn/engi/EN/10.1016/j.eng.2024.07.008
- 北科大材料基因中心：https://bjmge.ustb.edu.cn/xinwendongtai/2025-10-31/413.html ；《中国材料基因工程研究进展》：https://www.ams.org.cn/article/2020/0412-1961/0412-1961-56-10-1313.shtml
- 北航 ALKEMIE：https://zhuanlan.zhihu.com/p/27757203995 ；https://shi.buaa.edu.cn/sunzhimei/zh_CN/kyxm/10125/content/5642.htm

## 10. 待核实清单（诚实性声明）

以下条目在调研中未能找到可靠公开来源，使用时请注意：
1. MatterGen 对特定公司的商业授权案例（未检索到公开报道，仅有 Syensqo MoU 与 Azure 目录）；
2. 华为云是否存在独立"材料大模型"产品（仅见盘古科学计算大模型概览提及化学材料）；
3. Emerald Cloud Lab 奥斯汀实验室当前运营状态（加州实验室 2023 年已关停）；
4. Mater. Horiz. 2026 对生成模型"复现训练集化合物"的具体论断（仅据检索摘要）；
5. 松山湖"机器人材料科学家"的对外商业化程度；
6. Lookman 现职；南科大张文清、北航 Potential Mind、清华张亮 HS2C-ML 的论文 DOI；
7. 中国材料基因工程平台的数据总量；Citrine 2019 年后的融资与经营现状；
8. EleGANT 模型精度、Roost 的 MatBench 官方数值、MatterGen 生成结构的具体稳定率百分比。
