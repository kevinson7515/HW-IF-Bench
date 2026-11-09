# 机器学习/深度学习优化材料成分设计（元素配比）方向——中国活跃课题组调研报告

**调研时间范围**：重点 2019–2025 年（个别背景性事实追溯至更早，个别最新成果延伸至 2026 年初）
**调研范围**：中国大陆、香港、台湾
**方法**：全部事实来自本次调研实际检索/抓取到的网页（web_search + web_fetch），每条事实附来源 URL；无法核实的信息明确标注"**待核实**"；未编造任何论文标题或数据。
**说明**：本文件为独立调研产物，与 output/ 目录下其他报告互补（同目录已有更宏观的 ML 成分优化综述类文件）。

---

## 目录

1. 上海大学材料基因组工程研究院（张统一院士团队）
2. 北京科学智能研究院 AISI / 深势科技 DP Technology（鄂维南、张林峰）
3. 中南大学（杜勇团队；张利军团队）
4. 哈尔滨工业大学（用户所记 PI 核实结果）
5. 中科院金属研究所（沈阳）
6. 中科院宁波材料技术与工程研究所
7. 中科院物理研究所
8. 清华大学
9. 北京大学（AI for Science 路线）
10. 中国科学技术大学（江俊/罗毅：机器化学家）
11. 浙江大学
12. 上海交通大学（饶梓元）
13. 北京科技大学（宿彦京/姜雪团队，北京材料基因工程高精尖创新中心）
14. 大连理工大学（王清/董闯）
15. 南京理工大学（刘伟）
16. 松山湖材料实验室（张富祥）
17. 香港城市大学（杨勇）
18. 香港科技大学（广州）（张统一团队工具平台）
19. 香港大学（黄明欣——核实结果）
20. 台湾新竹清华大学（叶均蔚）与国家高速网络与计算中心（NCHC）
21. 中文期刊综述（2020–2025）
22. 国家层面布局（材料基因工程重点专项、AI for Science）
23. 总结与"待核实"清单

---

## 1. 上海大学材料基因组工程研究院（张统一院士团队）

**机构与 PI**：上海大学材料基因组工程研究院；**张统一（Tong-Yi Zhang）**——中国科学院院士（2011 年当选）、香港工程科学院院士（2012 年）、上海大学材料基因组工程研究院院长、《中国科学：技术科学》（中英文卷）主编、Journal of Materials Informatics（JMI）首任主编、中国材料学会材料基因组工程分会主任。学术标签："Materials/mechanics (M/M) informatics、AI for M/M"。另据科学网 2015 年报道，"上海材料基因组工程研究院（筹）"揭牌时徐匡迪任名誉院长、张统一任院长（上海大学材料基因组工程研究院建院年份：**待核实**）。近年张统一教授同时在香港科技大学（广州）活动（其团队自述为"香港科技大学（广州）的张统一教授团队"）。
- 来源：[上海材料前沿论坛·张统一简介](https://shmat.shu.edu.cn/info/1098/1121.htm)、[JMI 主编页](https://www.oaepublish.com/jmi/editor/1476)、[科学网 2015 报道](https://news.sciencenet.cn/htmlnews/2015/4/317546.shtm)、[华南师大讲座报道](http://sce.scnu.edu.cn/a/20250606/1573.html)

**研究方向（成分优化相关）**：材料信息学与力学信息学；团队自述成果包括"专业知识指导下的无铅焊料开发、锂电池的疲劳寿命预测"以及"材料预测和设计的无需编程 AI 平台"；上海大学设有"材料信息学（0805J3，材料基因组工程研究院）"交叉学科博士点，提出"数据+AI+材料领域知识"驱动的材料科学研究新体系。院内核心骨干包括**施思齐教授**（电池材料机器学习）等。

**代表性论文/成果**：

1. **A machine-learning approach to predicting and understanding the properties of amorphous metallic alloys**（J. Xiong, S.Q. Shi, T.Y. Zhang），*Materials & Design* 187 (2020) 108378。
   - 方法/成果：基于 **6471 个合金**的数据集构建 ML 预测模型，预测并解释非晶（金属玻璃）合金性能——典型"成分→性能"数据驱动设计工作；被引约 329 次。
   - URL: https://www.sciencedirect.com/science/article/pii/S0264127519308160
2. **Machine learning prediction of glass-forming ability in bulk metallic glasses**（J. Xiong, S. Shi, T. Zhang），*Computational Materials Science* 192 (2021) 110362。
   - 方法/成果：ML 预测大块金属玻璃玻璃形成能力（成分设计关键指标）。（出处经 JMI 综述引用核实）
   - 来源：[JMI 综述引用页](https://www.oaepublish.com/articles/jmi.2021.12)
3. **Bgolearn 主动学习库 + MLMD 无需编程 AI 平台**（香港科技大学（广州）张统一团队，开源工具）。
   - 方法/成果：Bgolearn 为面向科研的 Python 贝叶斯全局优化（BGO）框架，支持高斯过程、SVM、随机森林、AdaBoost、MLP 等代理模型及 EI/AEI 等采集函数，用于数据驱动的材料发现、实验设计与虚拟筛选；团队以 EI/REI/UCB 主动学习完成高硬度 AlCoCrCuFeNi 高熵合金成分设计，所得成分与原始实验结果一致。MLMD 为面向材料设计的"无需编程"AI 平台。
   - URL: https://github.com/Bin-Cao/Bgolearn 、[知乎团队介绍（检索摘要）](https://zhuanlan.zhihu.com/p/709701013)
4. **Machine Learning Embedded with Materials Domain Knowledge**（Yue Liu, Xinxin Zou, Zhengwei Yang, Siqi Shi），《硅酸盐学报》(*Journal of the Chinese Ceramic Society*) 50(3): 863-876, 2022。
   - 方法/成果：综述提出"嵌入材料领域知识的机器学习方法"，系统讨论 ML 在材料设计（成分-性能建模）中的三大矛盾与对策；作者单位含上海大学计算机学院、材料学院与材料基因组工程研究院。
   - DOI: [10.14062/j.issn.0454-5648.20220093](https://www.sciopen.com/article/10.14062/j.issn.0454-5648.20220093)
5. 施思齐团队相关：**A general framework to govern machine learning oriented materials data quality**（Y. Liu 等，施思齐参与），*Materials Science and Engineering: R: Reports* (2025)，被引约 55 次——提出 ML 导向材料数据质量的九维治理框架（涉及 17 个数据集），支撑高质量成分-性能数据建模。
   - URL: https://www.sciencedirect.com/science/article/abs/pii/S0927796X25001275
6. 张统一创办并主编的 **Journal of Materials Informatics**（OAE 出版）是材料信息学方向新刊，代表论文如 **Data-driven design of eutectic high entropy alloys**（Zhaoqi Chen, Yong Yang），*J. Mater. Inf.* 2023;3:10（被引 27 次）。
   - URL: https://www.oaepublish.com/articles/jmi.2023.06

---

## 2. 北京科学智能研究院 AISI / 深势科技 DP Technology（鄂维南、张林峰）

**机构与 PI**：
- **北京科学智能研究院（AI for Science Institute, Beijing, AISI）**：成立于 **2021 年 9 月**，致力于将人工智能技术与科学研究结合（官网）。**鄂维南院士**（中国科学院院士、北京大学数学科学学院讲席教授、北京大数据研究院院长、北京大学国际机器学习研究中心主任）为 AISI 创始领导人——2023 年报道称其任"北京科学智能研究院院长"，北大深圳研究生院科学智能学院页面现称其为"北京科学智能研究院学术委员会主任"（两处表述不一致，以官网为准，**现任职务待核实**）。鄂维南 2023 年获 ICIAM 麦克斯韦奖。
- **深势科技（DP Technology）**：成立于 **2018 年**，北京/上海/深圳/宜宾设有研发中心，自称"全球 AI for Science 开拓者"；创始人**张林峰**（AISI 副院长、深势科技创始人兼 CSO）与创始人/CEO **孙伟杰**。
- 来源：[AISI 官网](https://www.aisi.ac.cn/)、[新华网：张林峰报道](http://www.news.cn/tech/20230530/04daf7d660334a2baa46ccb0a5f43849/c.html)、[CAM 鄂维南访谈](https://www.global-sci.com/cam/article/view/22214)、[北大深研院鄂维南简介](https://ai4s.pkusz.edu.cn/info/1034/1245.htm)、[深势科技官网](https://www.dp.tech/)、[关于我们](https://www.dp.tech/about)

**研究方向（成分优化相关）**：以"AI for Science"基础设施支撑材料模拟与设计：通用机器学习势（大原子模型）、分子表征大模型、科学计算云平台。对"成分设计"的影响在于用 DPA-2 类通用势把 DFT 级精度计算扩展到任意成分的多组元体系，从而支撑成分空间的低成本高通量评估（物理所 2025 年学术论坛亦将其总结为"从小数据小模型到大数据大模型"的合金设计范式转变，见第 7 节）。

**代表性成果**：

1. **DPA-2: a large atomic model as a multi-task learner**（Duo Zhang, Xinzijian Liu, Xiangyu Zhang, …, Weinan E（鄂维南）, Linfeng Zhang, Han Wang 等 38 位作者），*npj Computational Materials* (2024)。
   - 方法/成果：提出"大原子模型（LAM）"——将不同元素体系机器学习势统一到多任务预训练框架，经微调与蒸馏得到兼顾精度与效率的通用机器学习势（覆盖元素范围与精度指标：**待核实**，需查阅原文）。arXiv 提交于 2023-12-24；被引约 199 次。
   - DOI: [10.1038/s41524-024-01493-2](https://www.nature.com/articles/s41524-024-01493-2)；arXiv: https://arxiv.org/abs/2312.15492
2. **Uni-Mol: A Universal 3D Molecular Representation Learning Framework**（Gengmo Zhou, Zhifeng Gao, Qiankun Ding 等），ICLR 2023（poster）。
   - 方法/成果：通用三维分子表征学习框架，显著扩展分子表征能力与应用范围（含蛋白-配体结合构象预测、分子构象生成等）；DP Technology 参与，代码开源。
   - URL: https://iclr.cc/virtual/2023/poster/11617 、https://github.com/dptech-corp/Uni-Mol 、[ChemRxiv 预印本](https://chemrxiv.org/doi/10.26434/chemrxiv-2022-jjm0j)
3. **Bohrium（玻尔）科学计算平台**：深势科技为科研人群打造的科学计算云平台，提供海量 CPU/GPU 算力与集群化弹性调度，预装并优化传统计算软件并集成 AI for Science 工具链，支撑材料高通量计算与机器学习工作流。
   - URL: https://www.dp.tech/product/bohrium/workspace 、https://www.bohrium.com/
4. **AI for Science 布局（与 AISI 深度绑定）**：科技部 2023 年 3 月启动"人工智能驱动的科学研究"（AI for Science）专项部署，鄂维南公开表示"借助机器学习在高维问题的表示能力，人类可以更加真实细致地刻画复杂系统的机理"；2023 科学智能峰会发布 2023 版《科学智能(AI4S)全球发展观察与展望》。
   - 来源：[北京市科委转载科技部新闻](https://kw.beijing.gov.cn/xwdt/kcyx/xwdtcyfz/202303/t20230328_3817948.html)、[21 世纪经济报道](https://www.21jingji.com/article/20230811/herald/3adf5175382a920e52ef9bb3c334a15d.html)

---

## 3. 中南大学（粉末冶金研究院/国家重点实验室）

### 3.1 杜勇团队（相图、相变及材料智能设计科学中心）

**机构与 PI**：中南大学粉末冶金研究院，**杜勇教授**（长江学者特聘教授、国家杰青；国际刊物 *CALPHAD* 副主编、*Journal of Phase Equilibria and Diffusion* 副主编、*Journal of Materials Informatics* 副主编（2021.4 至今）；973 首席科学家）。团队："中南大学相图、相变及材料设计与制备科学中心"+中德"微结构"联合实验室+中德"电化学存储系统集成计算材料工程"联合实验室，含杜勇、陈利、刘树红、李凯 4 位教授及孔毅、汪炯、王建川、刘钰玲、文诗艺等副教授/讲师梯队；官网研究方向明确包含**"材料信息学与人工智能""材料智能设计软件"**。
- 来源：[杜勇教师主页](https://faculty.csu.edu.cn/duyong/zh_CN/index.htm)、[科学中心介绍](https://pmri.csu.edu.cn/info/1283/4740.htm)

**研究方向（成分优化相关）**：CALPHAD 相图计算+高通量第一性原理+机器学习的多组元合金成分设计（涂层、轻合金、硬质合金、高温合金等）。

**代表性成果**（据科学中心官方页面）：
1. **TiAlTMN 涂层成分设计**：结合高通量第一性原理与机器学习建立高效 TiAlTMN 涂层成分设计策略，开发多种高性能涂层并应用于切削刀具。发表于 *Acta Materialia* 2024（DOI: 10.1016/j.actamat.2024.120139，具体题目**待核实**）。
2. **耐热高强铝合金设计**：θ′ 相+C/L 相复合强化的耐热铝合金成分设计路线，发表于 *Nature Communications* 14 (2023) 2959（DOI: 10.1038/s41467-023-38730-z，作者与题目归属科学中心，**具体作者待核实**）。
3. 最新延伸：**CALPHAD-based cross-system knowledge transfer**（W. Mo 等，中南大学），*npj Computational Materials* (2026)。
   - URL: https://www.nature.com/articles/s41524-026-02073-2

### 3.2 张利军团队（另需单列的重要课题组）

**机构与 PI**：中南大学粉末冶金国家重点实验室，**张利军（Lijun Zhang）教授**（另与合作者姚健等）。
**研究方向**：机器学习+CALPHAD/热力学计算的多主元（高熵）合金成分设计、Cu 合金成分-工艺 Pareto 前沿优化、难熔高熵合金 ML 设计。

**代表性论文**：
1. **Revisit the VEC rule in high entropy alloys (HEAs) with high-throughput CALPHAD approach and its applications for material design—A case study with Al–Co–Cr–Fe–Ni**（S. Yang 等），*Acta Materialia* (2020)。
   - 方法/成果：用高通量 CALPHAD（HT-CALPHAD）重新审视 VEC（价电子浓度）经验规则，指导 FCC/BCC 相结构选择与成分设计；被引约 242 次。
   - URL: https://www.sciencedirect.com/science/article/abs/pii/S1359645420302263
2. **Design of NiCoCrAl eutectic high entropy alloys by combining machine learning with CALPHAD method**（Feng Liu, Xiangyou Xiao 等 5 位作者），*Materials Today Communications* 30 (2022) 103172。
   - 方法/成果：ML+CALPHAD 快速定位 Ni-Co-Cr-Al 体系两个新共晶成分；被引约 75 次（团队归属以原文为准，**通讯作者单位待核实**——检索显示与中南大学粉末冶金研究院关联）。
   - URL: https://www.sciencedirect.com/science/article/abs/pii/S2352492822000496
3. 中文综述：**机器学习驱动难熔高熵合金设计的现状与展望**（高田创、高建宝、李谦、张利军 等），《材料工程》2024, 52(1)（详见第 21 节）。

---

## 4. 哈尔滨工业大学（用户所记 PI 核实结果）

**核实结论**：用户提示的两位 PI 姓名**均未能核实**：
- "**苏彦梅**"：中英文多轮检索（含与"高熵合金/机器学习/材料"组合）**未发现**任何名为"苏彦梅"的哈工大学者及其相关论文——**待核实/疑为姓名有误**。
- "**刘丽月**"：仅检索到 2001 年《材料研究学报》论文《新型氧敏薄膜材料》（作者：徐明霞、郑嘹赢、刘丽月、樊丽莹、徐廷献，[链接](https://www.cjmr.org/CN/Y2001/V15/I1/17)）中的同名作者，与哈工大及 ML 高熵合金无关；**未发现**其在高熵合金机器学习方向的任何记录——**待核实/疑为误传**。

**哈工大在该方向实际检索到的线索**：
- 哈工大学者库（scholar.hit.edu.cn）收录综述 **Machine learning-assisted design of lightweight refractory high-entropy alloys**（第一作者 L. Chen，2026，被引约 52 次）——表明哈工大确有学者从事 ML 辅助轻质难熔高熵合金设计的综述研究，但**具体 PI 与院系待核实**（该校学者库页面重定向至第三方站点，未能直接抓取作者详情）。URL: https://scholar.hit.edu.cn/en/publications/machine-learning-assisted-design-of-lightweight-refractory-high-e/
- 哈工大宋晓国团队 2026 年报道开发 **CoCrFeNiCux 高熵合金钎料**（半固态钎焊策略）——属高熵合金成分相关工作但**非 ML 成分设计**。URL: https://news.hit.edu.cn/2026/0518/c11819a242312/page.htm
- 相邻院校线索（可能与用户记忆混淆）：**哈尔滨理工大学**有"基于机器学习预测高熵合金硬度"的硕士论文（杨志远 2022、邹瑞 2023，见《材料导报》2025 综述参考文献），并参与"2024 第二届数据驱动的高熵非晶材料大会"；该会议亦列出"哈尔滨工业大学·高熵合金塑性成形"报告（[会议通知](https://mse.fyust.edu.cn/info/1571/2571.htm)）。
- 哈工大材料科学与工程学院官网科研方向列表中未见"机器学习材料成分设计"专门方向（[官网](http://mse.hit.edu.cn/)）。

**结论**：哈工大在"ML 高熵合金成分设计"方向的公开代表性课题组信息不足，建议以学者库上述综述为线索进一步核实具体 PI。

---

## 5. 中科院金属研究所（沈阳）

**机构与 PI**：
- **胡青苗研究员、杨锐研究员**（轻质高强材料研究部）；
- 新设**材料人工智能研究部**（主任：**陈星秋**），属沈阳材料科学国家研究中心。

**代表性成果**：
1. **《对更好合金的无尽寻索》（"endless search for better alloys"述评）**（胡青苗、杨锐），*Science* 378(6615): 26-27，2022 年 10 月 6 日在线。
   - 内容：应 Science 邀请评述 ML 用于材料成分筛选的现状——指出 ML 已成功用于因瓦高熵合金、铁电、压电等功能材料成分筛选（结构材料因组织敏感性难度更大），并评述了马普钢铁所 Raabe 团队从约百万种成分组合中筛选 17 种 Fe-Co-Cr-Ni(-Cu) 因瓦高熵合金的 Science 论文；展望"面向指定性能需求的定制化材料成分及工艺优化设计"。
   - DOI: [10.1126/science.ade5503](https://doi.org/10.1126/science.ade5503)；所内报道: http://www.imr.cas.cn/xwzx/kydt/202210/t20221009_6520658.html
2. **材料人工智能研究部**（主任陈星秋）：方向包括 AI 驱动的材料跨尺度计算模拟、材料 AI-Ready 数据库、材料智能设计与智能制备（AI for Materials）、智能体驱动的材料逆向设计；成果包括"精度与效率兼顾的**多元合金机器学习势模型**等材料计算方法与软件""构建了**合金 AI 大模型和电化学腐蚀大模型**"（页面发布于 2026-04）。
   - URL: http://imr.cas.cn/jgsz/synl/202604/t20260410_8183678.html

---

## 6. 中科院宁波材料技术与工程研究所（NIMTE）

**机构与 PI**：宁波材料所**非晶合金磁电功能特性团队**——通讯作者**王军强研究员、霍军涛研究员**（合作者含宋丽建、高萌、张岩研究员等；中国科学院磁性材料与器件重点实验室）。

**研究方向**：机器学习驱动的铁基非晶/纳米晶软磁合金成分设计（超高饱和磁感 Bs+超低矫顽力 Hc）。

**代表性论文**：
1. **Designing Fe-Based Amorphous Alloys With both Ultra-High Magnetization and Ultra-Low Coercivity Through Artificial Intelligence**（第一作者：博士研究生杨世玉；通讯：王军强、霍军涛），*Advanced Functional Materials* 2025, 2425588。
   - 方法：构建 XGBoost/随机森林/SVM 三种 ML 模型预测铁基非晶合金 Bs；**XGBoost 测试集 R²>0.85、RMSE≤0.12 T**；SHAP 分析得到设计准则（C_Fe>75 at.%、ΔH_mix 介于 −18.7~−14 kJ/mol、δχ<0.07）；第一性原理验证机理；据此设计 Fe-Co-Ni-Si-B、Fe-Co-Ni-B-P-C、Fe-Co-N-B-P-C-V 等系列合金。
   - 关键成果（实验验证）：磁场退火后 **Bs 均>1.85 T、Hc 低至 1.2 A/m**；其中 (Fe82Co18)85.5Ni1.5B9P3C1 与 Fe69Co16Ni1Si3B11 的 **Bs 达 1.92 T**，综合软磁性能超越硅钢。
   - DOI: [10.1002/adfm.202425588](https://advanced.onlinelibrary.wiley.com/doi/10.1002/adfm.202425588)；团队报道: https://non-crystal.nimte.ac.cn/view-31283.html
2. 其他：宁波材料所招聘"AI 辅助材料创制、机器学习与多尺度理论计算"方向博士后，职责含"金属陶瓷复合材料/多元合金/多元涂层"的**逆向设计**（[招聘页](https://recruit.nimte.ac.cn/system/userInfo/positionInfo?id=1802509568478314497&isDelivery=null)）——表明该所有多个 ML 成分设计团队在扩充（具体 PI **待核实**）。

---

## 7. 中科院物理研究所

**机构与 PI**：**汪卫华院士**团队（含白海洋、柳延辉研究员等）；**翁红明**研究员团队（AI 生成模型方向）。

**代表性成果/线索**：
1. **Metallic glass roadmap**（W.H. Wang（汪卫华）等），*Materials Futures*（IOPscience，2025），被引约 36 次——系统路线图性综述，明确将**机器学习**列为金属玻璃（多元合金成分设计）未来设计手段之一。
   - URL: https://iopscience.iop.org/article/10.1088/2752-5724/adcfb6
2. 早期背景（2017）：汪卫华研究组（孙奕韬，导师汪卫华、白海洋及中国人民大学李茂枝）用 ML 预测二元合金玻璃形成能力（[科学网报道](https://news.sciencenet.cn/htmlpaper/20177211334485544507.shtm)）——国内非晶成分 ML 设计早期代表。
3. **翁红明团队**：在 CDVAE 基础上引入属性嵌入（PropEmb）等两个新模块，增强**多属性条件下的晶体/成分生成能力**（Con-CDVAE 模型），被《计算物理》综述作为"性能→结构/成分"生成式逆向设计典型案例引用（[综述 PDF](http://jswl.xml-journal.net/cn/article/pdf/preview/10.19596/j.cnki.1001-246x.9157.pdf)）。
4. 2025 年物理所"极端室学术论坛(67)"由**柳延辉**邀请上海交大**饶梓元**做题为"基于机器学习和人工智能的合金设计——从小数据小模型到大数据大模型"的报告（含 ML 开发近零热膨胀高熵因瓦合金等实例），显示物理所非晶团队与 ML 合金设计前沿的紧密互动。URL: https://www.iop.cas.cn/xshd/xsbg/202503/t20250321_7561864.html
5. 注：汪卫华团队 2024 年"单质非晶金属"突破（激光快冷+助熔剂）为实验工艺创新、非 ML 成分设计（[报道](https://www.iop.cas.cn/xwzx/kydt/202408/t20240806_7243387.html)）。物理所 2019–2025 年以 ML 成分设计为主题的独立代表作**待进一步核实**。

---

## 8. 清华大学

**机构与 PI**：清华大学物理系**倪军教授**（与合作者日本东北大学陈迎教授）；此外材料学院牵头国家材料基因工程专项"高通量并发式材料计算算法和软件"项目（10 家单位参与，目标为新材料研发从"经验指导实验"向"理论预测+实验验证"模式转变，[清华材料学院新闻](https://www.mse.tsinghua.edu.cn/info/1062/1527.htm)）。

**代表性论文**：
1. **EFTGAN: Elemental features and transferring corrected data augmentation for the study of high-entropy alloys**（第一作者：博士生孙一博；通讯作者：倪军；合作者：陈迎），*npj Computational Materials* (2025)。
   - 方法/成果：针对小样本高熵合金数据，提出"元素特征迁移对抗网络"——元素卷积图神经网络提取元素特征+信息最大化生成对抗网络（InfoMax GAN）数据增强+迭代反馈，**无需第一性原理结构计算**即可在高熵合金广阔成分空间预测形成能、磁矩、自由能等性质，显著提高小样本预测精度。
   - DOI: [10.1038/s41524-025-01548-y](https://doi.org/10.1038/s41524-025-01548-y)；报道: https://www.phys.tsinghua.edu.cn/info/1268/6313.htm
2. 相关背景：清华材料学院姚可夫团队从事大块金属玻璃研究（如 *Materials* 15(5):1669, 2022，Ti20Hf20Cu20Ni20Be20 等 HE-BMG，断裂强度>2300 MPa，[PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC8911233/)）——但其 2022 年该文采用"相似元素替代/添加+δ′ 参数"而非 ML（列出供对照）。

---

## 9. 北京大学（AI for Science 路线）

**核实结果**：检索范围内，北京大学在"合金/电池/催化成分 ML 设计"方向最具代表性的力量即**鄂维南院士及 AISI/深势科技生态**（见第 2 节；鄂维南为北大数学科学学院讲席教授、北大国际机器学习研究中心主任，北大深圳研究生院设"科学智能学院"且鄂维南任名誉院长）。北大材料学科内以 ML 成分设计为主的独立课题组：**未检索到明确信息，待核实**。
- 来源：[北大深研院科学智能学院·鄂维南](https://ai4s.pkusz.edu.cn/info/1034/1245.htm)

---

## 10. 中国科学技术大学（江俊/罗毅：机器化学家）

**机构与 PI**：中国科学技术大学化学物理系**江俊教授**（实验室负责人；合肥微尺度物质科学国家研究中心）、**罗毅教授**（时任化学物理系执行主任，现任合肥微尺度物质科学国家研究中心主任）；联合信息学院尚伟伟副教授（机器人）。

**研究方向**：数据智能驱动的"机器化学家"（机器人+化学大脑），实现文献阅读→实验设计→自主优化全流程，用于**催化剂成分/配方寻优**（多元素组合空间中搜索最优配比）。

**代表性论文/成果**：
1. **An all-round AI-Chemist with a scientific mind**（Qing Zhu 等），*National Science Review* 9(10): nwac190 (2022)，被引约 247 次。
   - 成果：全球首个集阅读文献、设计实验、自主优化于一体的机器化学家平台（2 台移动机器人+19 个智能化学工作站+高通量计算+化学大脑）。
   - URL: https://academic.oup.com/nsr/article/9/10/nwac190/6694008
2. **Automated synthesis of oxygen-producing catalysts from Martian meteorites by a robotic AI-chemist**（Q. Zhu 等），*Nature Synthesis* 3: 319- (2024)，被引约 173 次。
   - 成果：以火星陨石为原料自动合成产氧电催化剂——5 种火星矿石成分存在**超过 376 万种配方组合**，人工试错约需 2000 年，机器化学家**5 个星期**完成并给出优化配方。
   - URL: https://www.nature.com/natsynth/volumes/3/issues/3 ；ADS: 2024NatSy...3..319Z
3. **A robotic AI-Chemist system for multi-modal AI-ready database**（S. Feng 等），*National Science Review* 10(12): nwad332 (2023)。
   - 成果：机器化学家+多模态 AI-ready 数据库（文献数据挖掘+高性能模拟+高精度实验融合）。
   - URL: https://academic.oup.com/nsr/article/10/12/nwad332/7502796
4. 高熵产氧催化剂案例（据中科院/科大官方报道）：从 **29 种非贵金属元素中选 5 种形成>55 万种配比组合**，机器化学家阅读 **1.6 万篇**催化论文、融合 **2.5 万组**理论计算与 **207 组**全流程机器实验数据建立预测模型，将创制周期缩短为 **5 个星期**（人工试错约需 1400 年）。支撑：中科院 2021 年"数据驱动的化学、材料和生物科学的机器科学家"揭榜挂帅项目（2021–2025，2000 万元）+ 中国科大"双一流"学科重点项目（1000 万元）。
   - 来源：[中国科学报（2024-04-11，科大新闻网转载）](https://news.ustc.edu.cn/info/1056/86925.htm)

---

## 11. 浙江大学

**机构与 PI**：浙江大学氢能研究院**陈立新教授**（浙江氢能储输技术及装备全省重点实验室副主任；研究方向：新型储氢材料、氢化物工程等）、**肖学章教授**（合作通讯）。

**代表性论文**：
1. **Machine Learning in Solid-State Hydrogen Storage Materials: Challenges and Perspectives**（第一作者：周盼盼（河海大学）、周倩雯（浙江大学）），*Advanced Materials*（2024 年末在线发表；卷期页**待核实**）。
   - 内容：系统综述 ML 在固态储氢材料（成分-性能优化）中的前沿探索、应用案例与发展前瞻，指出"以往储氢材料成分与性能优化多依赖试错法"，ML 为高性能新型储氢材料定制化研发提供新途径。
   - 来源（含学者名片）：http://h2.zju.edu.cn/news_detail/id-74.html
2. 浙大工程师学院设有"未来材料与 AI 驱动的材料"项目：基于人工智能开展"成分-工艺-组织"相关性研究，加快新材料**成分及结构设计**与增材工艺协同优化（[项目页](https://pi.zju.edu.cn/wlclyAIqddclxm/list.htm)）。
3. 另：上海大学施思齐教授曾应邀在浙大相关院系作"高质量数据和领域知识协同驱动的电池材料构效关系研究"报告（[厦门大学报道](https://chem.xmu.edu.cn/info/1275/28824.htm)）——浙大与材料信息学团队互动密切（具体浙大校内 ML 电池成分设计 PI **待核实**）。

---

## 12. 上海交通大学（饶梓元等）

**机构与 PI**：上海交通大学材料科学与工程学院**饶梓元副教授**（2024 年 7 月回国加入；海外优秀青年科学基金项目及上海领军人才（海外）获得者；德国亚琛工业大学博士、德国马普钢铁研究所博士后及研究组组长）。长期从事基于人工智能的材料科学研究（因瓦合金、磁性合金、高温合金、高熵合金）。此前**李金富教授**（上交大材料学院，非平衡凝固与亚稳材料课题组：非晶合金、高熵合金、钛铝合金）为该方向相关团队，但**未检索到其 ML 成分设计代表作（待核实）**。
- 来源：[物理所学术报告介绍](https://www.iop.cas.cn/xshd/xsbg/202503/t20250321_7561864.html)、[李金富教师页](https://smse.sjtu.edu.cn/people/detail_new/20313)、[课题组页](https://nes.sjtu.edu.cn/group/faculty/lijinfu.htm)

**代表性论文**：
1. **Machine learning–enabled high-entropy alloy discovery**（**Ziyuan Rao（饶梓元）** 等，Dierk Raabe、Fritz Körmann 团队，马普钢铁研究所），*Science* 378(6615): 78-85 (2022)，被引约 873 次。
   - 方法/成果：主动学习策略在" practically infinite"成分空间加速设计高熵因瓦合金——结合 ML、第一性原理、热力学计算与实验验证，从约**百万种候选成分**中筛选出 **17 种** Fe-Co-Cr-Ni 及 Fe-Co-Cr-Ni-Cu 因瓦高熵合金（据金属所 Science 述评转述）。
   - DOI: [10.1126/science.abo4940](https://www.science.org/doi/10.1126/science.abo4940)；PubMed: https://pubmed.ncbi.nlm.nih.gov/36201584/
2. 饶梓元在物理所报告内容（2025-03）：小数据集条件下 ML 加速合金设计（近零热膨胀高熵因瓦合金、提升镁合金抗腐蚀能力）；大语言模型用于文本挖掘、材料领域专业大模型微调与检索增强（镁合金设计与相图研究）。URL: https://www.iop.cas.cn/xshd/xsbg/202503/t20250321_7561864.html

---

## 13. 北京科技大学（宿彦京/姜雪团队；北京材料基因工程高精尖创新中心）

**机构与 PI**：北京科技大学**宿彦京教授**、**姜雪副教授**（北京材料基因工程高精尖创新中心，USTB）；核心成员含文成（Acta 2019 论文第一作者、2022 年北科大博士）、Turab Lookman 等。

**代表性论文**：
1. **Machine learning assisted design of high entropy alloys with desired property**（Cheng Wen, Yan Zhang, Changxin Wang, Dezhen Xue, Yang Bai, Stoichko Antonov, Lanhong Dai, Turab Lookman, Yanjing Su），*Acta Materialia* 170 (2019) 109-117，被引约 1079 次。
   - 方法/成果：ML 代理模型+实验设计（主动学习）策略，在高熵合金成分空间搜索目标性能成分——国内高熵合金 ML 成分设计被引最高的代表作之一。
   - URL: https://www.sciencedirect.com/science/article/abs/pii/S1359645419301430 （作者名单见 [LANL 馆藏记录](https://laro.lanl.gov/esploro/outputs/journalArticle/Machine-learning-assisted-design-of-high/9916370820503761)）
2. **Steel design based on a large language model**（第一作者 Shaohan Tian；通讯：宿彦京、姜雪、Turab Lookman），*Acta Materialia* (2024)，DOI: 10.1016/j.actamat.2024.120663。
   - 方法/成果：SteelBERT 材料语言编码器+多模态深度学习，从文献文本+成分+工艺序列端到端预测钢材力学性能：**YS/UTS/EL 的 R² 分别达 78.17%（±3.40%）/82.56%（±1.96%）/81.44%（±2.98%）**；仅用 15Cr 奥氏体不锈钢 **64 个实验样本**微调后 R² 达 **89.85%/88.34%/87.24%**；通过优化工艺文本序列获得 **YS 960 MPa、UTS 1138 MPa、EL 32.5%** 的优化钢（超过已报道 15Cr 奥氏体不锈钢性能）。
   - URL: https://bjmge.ustb.edu.cn/kexueyanjiu/keyanchengguo1/keyanchenggu/2025-04-27/396.html
3. **机器学习辅助难熔高熵合金强韧性协同设计**（文成, 张闫, 王长鑫, 黄海友, 吴渊, Turab Lookman, 宿彦京），*Engineering* 46(3): 214-223 (2025)。
   - 方法/成果：ML（SVM，高温屈服强度模型 **R²>0.85**）+遗传搜索+聚类分析+实验设计的迭代框架；在约 **2×10⁹ 候选成分**中经 **6 次反馈循环迭代合成 24 种新成分合金**，其中 4 种形成新 Pareto 前沿（高温屈服强度 714–1061 MPa，室温断裂应变 17.2%–50.0%）；**Zr0.13Nb0.27Mo0.26Hf0.13Ta0.21** 兼具 **1200 ℃ 屈服强度约 940 MPa 与室温断裂应变 17.2%**。
   - DOI: [10.1016/j.eng.2023.11.026](https://www.engineering.org.cn/engi/CN/10.1016/j.eng.2023.11.026)
4. 综述/政策文献：宿彦京等，《中国材料基因工程研究进展》，金属学报 56(10): 1313- (2020)（详见第 21、22 节）。

---

## 14. 大连理工大学（王清/董闯）

**机构与 PI**：大连理工大学材料科学与工程学院**王清（Qing Wang）教授**、**董闯（Chuang Dong）教授**（"团簇+连接原子（cluster-plus-glue-atom）"模型提出者/发展者）。

**研究方向**：团簇式（cluster formula）嵌入机器学习的高熵合金/多组元合金成分设计（结构与性能导向）。

**代表性论文/成果**：
1. **Cluster-formula-embedded machine learning for design of high-entropy alloys**（F. Yang 等），*npj Computational Materials* (2020)，被引约 96 次。
   - 方法/成果：将"团簇式"成分构造单元嵌入机器学习框架，面向性能设计高熵合金（大连理工团队）。
   - DOI: [10.1038/s41524-020-00372-w](https://www.nature.com/articles/s41524-020-00372-w)
2. 据百度百科（王清词条）：2020 年在 npj Computational Materials 发表"团簇式嵌入机器学习"成果；**2022 年在《Advanced Materials》报道新型 Al1.5Co4Fe2Cr 软磁高熵合金突破性进展**（具体论文题目/DOI **待核实**）。URL: https://baike.baidu.com/item/%E7%8E%8B%E6%B8%85/19929144
3. RG 主页另见 **Developing novel low-density high-entropy superalloys with high strength and superior creep resistance guided by automated machine learning**（自动化机器学习导向的低密度高熵高温合金设计；期刊与量化数据**待核实**）。URL: https://www.researchgate.net/profile/Qing-Wang-38

---

## 15. 南京理工大学（刘伟）

**机构与 PI**：南京理工大学材料学院**刘伟教授**课题组（高熵合金研究始于 2015 年，制备与发展新型高熵合金并研究其性能/变形机理）。

**代表性论文**：
1. **Predicting single-phase solid solutions in as-sputtered high entropy alloys: High-throughput screening with machine-learning model**（J.C. Ren 等），*Journal of Materials Science & Technology* (2023)。
   - 方法/成果：集成机器学习模型（AS-RF），仅基于原子特征直接预测五元相图/相结构，高通量筛选单相固溶体高熵合金；成功预测单相固溶体、双相固溶体、金属间化合物和非晶相在内的高熵合金（薄膜）相结构，**平均预测精度 94.5%**；被引约 62 次。
   - DOI: [10.1016/j.jmst.2022.07.059](https://www.jmst.org/EN/10.1016/j.jmst.2022.07.059)；报道: https://smse.njust.edu.cn/a8/de/c10309a305374/page.htm

---

## 16. 松山湖材料实验室（张富祥）【检索中补充】

**机构与 PI**：松山湖材料实验室**高熵合金材料及应用团队**，负责人**张富祥研究员**（研究方向：高熵合金基础科学问题、成分/熵调控等）。
- URL: https://www.sslab.org.cn/core/coredetail?id=210319141520736055A8B438C
**ML 相关线索**：2024 第二届数据驱动的高熵非晶材料大会列有松山湖材料实验室**裴超群**报告"机器学习助力高熵合金材料设计"（[会议通知](https://mse.fyust.edu.cn/info/1571/2571.htm)）——该实验室确有 ML+高熵合金设计工作，**具体论文待核实**。

---

## 17. 香港城市大学（杨勇）

**机构与 PI**：香港城市大学机械工程系**杨勇（Yang Yong）教授**团队。

**研究方向**：生成式深度学习逆向设计块体金属玻璃（性能→成分）；机器学习指导高熵合金相设计。

**代表性论文**：
1. **A generative deep learning framework for inverse design of compositionally complex bulk metallic glasses**（Z. Zhou 等，通讯 Yang Yong），*npj Computational Materials* 9: 15 (2023)，被引约 81 次。
   - 方法/成果：无监督生成式对抗网络（GAN）+监督型提升树（boosted trees）深度学习框架；系统研究不同数据描述符（成分描述符 D1、玻璃形成能力描述符 CD1 等）对生成模型有效性的影响，发现半经验描述符不普适、需理论指导构建新描述符；实现 Tg/Tx/Tl 目标性能的成分逆向设计并**实验验证**；生成**八元合金 Zr27.3Cu26.1Hf16.9Al9.6Ti7.2Ni6.4Ag5.9Nb0.4（φ2 mm 铸棒，XRD 证实非晶）**。
   - DOI: [10.1038/s41524-023-00968-y](https://www.nature.com/articles/s41524-023-00968-y)；中文解读: https://news.qq.com/rain/a/20231024A03PYD00 ；CityU 学者库: https://scholars.cityu.edu.hk/en/publications/a-generative-deep-learning-framework-for-inverse-design-of-compos/
2. **Machine learning guided appraisal and exploration of phase design for high entropy alloys**（Z. Zhou 等），*npj Computational Materials* 5: 1-9 (2019)，被引约 351 次。
   - 方法/成果：用多种 ML 模型批判性评估高熵合金常用经验设计规则，并经实验验证设计 Fe-Cr-Ni-Zr-Cu 系新合金。
   - URL: https://www.nature.com/articles/s41524-019-0265-1 ；[CityU 全文 PDF](https://scholars.cityu.edu.hk/ws/portalfiles/portal/86074146/82269007.pdf)
3. 综述：**Data-driven design of eutectic high entropy alloys**（Zhaoqi Chen, Yong Yang），*Journal of Materials Informatics* 2023;3:10（共晶高熵合金数据驱动设计综述）。
   - URL: https://www.oaepublish.com/articles/jmi.2023.06

---

## 18. 香港科技大学 / 香港科技大学（广州）

**机构与 PI**：**香港科技大学（广州）张统一教授团队**（张统一原任香港科技大学机械与航空航天工程系教授，现为上大材料基因组工程研究院院长；其 HKUST(GZ) 团队开发 Bgolearn/MLMD 平台，见第 1 节）。
- 来源：[知乎团队介绍（检索摘要）](https://zhuanlan.zhihu.com/p/709701013)、[JMI 主编页](https://www.oaepublish.com/jmi/editor/1476)
**香港科技大学（清水湾）**：检索到的材料 AI 成果为 **GrainBot**（显微图像微结构自动量化 AI 工具，[科大新闻](https://hkust.edu.hk/zh-hans/news/hkust-develops-first-ai-toolkit-grainbot-automate-quantitative-microstructure-analysis)）——属组织表征而非成分设计；以 ML 合金成分设计为主的 HKUST 本部课题组**待核实**。

---

## 19. 香港大学（核实结果）

**核实结果**：香港大学机械工程系**黄明欣（Mingxin Huang）教授**为超高强钢领域著名学者（D&P 钢；其团队"发明超级钢，创造强度、延展性和韧性两项世界纪录"，获 HKU 创新者奖；设计理念为"位错工程"）。**未检索到**其团队以机器学习成分设计为主的代表性论文——**待核实**；港大其他 ML 材料成分设计课题组亦未在本次检索中确认。
- 来源：[HKU 创新者奖页面](https://www.ke.hku.hk/sc/story/video/prof-mingxin-huang-from-the-department-of-mechanical-engineering-wins-the-hku-innovator-award)、[海南大学讲座报道](https://mse.hainanu.edu.cn/info/1012/2664.htm)

---

## 20. 台湾新竹清华大学（叶均蔚）与国家高速网络与计算中心（NCHC）

**机构与 PI**：台湾清华大学（新竹）材料科学工程学系特聘研究讲座教授**叶均蔚（Jien-Wei Yeh）**——高熵合金概念提出者（2004 年，被 NTHU 官网称为"Father of High-Entropy Alloys"，中研院新科院士）；其参与推动的**清华大学高熵材料研发中心**与**国家高速网络与计算中心（NCHC，国家实验研究院）**合作建设机器学习材料研发平台。

**代表性成果（据 NCHC 官网新闻，2025-03-31）**：
- 以机器学习全面提升高熵材料研发效率：NCHC 与清华高熵材料研发中心合作，开发以 ML 加速成分设计的平台（整合 NCHC 算力、数据库与材料设计工具）。
- **量化结果**：ML 预测+实验验证获得 **3 个新的 AlCoCrFeMnNi 基成分，硬度均超过 600 HV，最高 650 HV**，超过文献报道纪录 539 HV 约 **20%**；并利用生成式网络模型"可视化材料设计空间"，缩小实验试错范围。
- 来源：[NCHC 官网新闻](https://www.nchc.org.tw/Active/ActiveView/750?mid=172&page=1)、[NTHU 叶均蔚官方介绍](https://nthu-en.site.nthu.edu.tw/p/404-1003-263114.php)
- 注：叶均蔚团队 2019–2025 年以 ML 成分设计为主题的**具体论文题目/DOI 待核实**（本次检索未直接命中期刊论文，以官方新闻为准）。

---

## 21. 中文期刊综述（2020–2025）

1. **李俊炎, 张伟强, 高志玉. 机器学习辅助高熵合金设计的研究进展**（沈阳理工大学材料科学与工程学院），《材料导报》2025, 39(18): 24080091-10。
   - 要点：综述 ML 辅助高熵合金**相结构预测、成分设计、性能预测及多目标优化**；指出"机器学习模型能通过正向预测或逆向设计在高熵合金巨大的成分空间中搜索更优的成分及比例"。
   - DOI: [10.11896/cldb.24080091](https://doi.org/10.11896/cldb.24080091)；页面: https://www.mater-rep.com/CN/abstract/abstract7790.shtml
2. **高田创, 高建宝, 李谦, 张利军 等. 机器学习驱动难熔高熵合金设计的现状与展望**（中南大学粉末冶金国家重点实验室、重庆大学国家镁合金材料工程技术研究中心），《材料工程》2024, 52(1)（页码**待核实**；被引约 3 次）。
   - 要点：难熔高熵合金 ML 设计路线（成分复杂、设计难度高）。
   - 检索入口: https://openurl.ebsco.com/fulltext/gcd:175245640?sid=ebsco:plink:crawler-gcd&id=ebsco:gcd:175245640&crl=f&jrnl=10014381 ；ResearchGate: https://www.researchgate.net/publication/378215842
3. **谢建新. 机器学习在材料研发中的应用**（北京科技大学/新金属材料国家重点实验室，院士），《金属学报》2021, 57(11): 1343-（被引约 59 次）。
   - 要点：以材料预测和优化设计为主线、金属结构材料为案例，综述材料特征构建与筛选、ML 建模与优化设计。
   - URL: https://www.ams.org.cn/article/2021/0412-1961/0412-1961-2021-57-11-1343.shtml
4. **宿彦京 等. 中国材料基因工程研究进展**，《金属学报》2020, 56(10): 1313-（被引约 52 次）——含材料基因工程专项与数据平台对材料设计范式的影响。
   - URL: https://www.ams.org.cn/article/2020/0412-1961/0412-1961-56-10-1313.shtml
5. **Z. Wu 等. 机器学习在镁合金应用中的研究进展**，《工程科学学报》2024（DOI: 10.13374/j.issn2095-9389.2024.03.10.002，被引约 5 次）——镁合金性能/工艺/组织/逆向设计 ML 应用综述。
   - URL: http://cje.ustb.edu.cn/en/article/pdf/preview/10.13374/j.issn2095-9389.2024.03.10.002.pdf
6. **机器学习赋能新材料设计：从经验试错到数据驱动的范式变革**，《计算物理》（DOI: 10.19596/j.cnki.1001-246x.9157）——含翁红明团队 Con-CDVAE 多属性条件生成模型等案例（作者**待核实**）。
   - URL: http://jswl.xml-journal.net/cn/article/pdf/preview/10.19596/j.cnki.1001-246x.9157.pdf

---

## 22. 国家层面布局

### 22.1 材料基因工程重点专项（"材料基因工程关键技术与支撑平台"重点专项）

- 据《金属学报》2020 年宿彦京等《中国材料基因工程研究进展》："**科技部于 2015 年启动了'材料基因工程关键技术与支撑平台'重点专项**，开展材料基因工程基础研究……"（该专项属国家重点研发计划框架，"十三五"期间持续实施；启动年份不同口径有 2015/2016 之别——以原文 2015 年为准）。URL: https://www.ams.org.cn/article/2020/0412-1961/0412-1961-56-10-1313.shtml
- 专项目标（据清华材料学院承担项目介绍）：融合高通量并发式集成计算关键技术，"实现新材料研发由'经验指导实验'的传统模式向'**理论预测+实验验证**'的新模式转变"——该专项由清华牵头"高通量并发式材料计算算法和软件"项目（10 家单位参加），直接支撑高通量计算+数据库+机器学习的成分设计生态。URL: https://www.mse.tsinghua.edu.cn/info/1062/1527.htm
- 对成分设计的影响：宁波材料所 AFM 2025 论文获"国家重点研发计划（2024YFB3813700）"支持；上海大学"材料信息学"交叉学科博士点依托材料基因组工程研究院建设——专项与学科建设直接哺育了本报告第 1、6 节等课题组的 ML 成分设计工作。

### 22.2 "AI for Science"布局

- **科技部 2023 年 3 月启动"人工智能驱动的科学研究"（AI for Science）专项部署工作**；鄂维南表示："借助机器学习在高维问题的表示能力，人类可以更加真实细致地刻画复杂系统的机理……"（北京市科委网站转载）。URL: https://kw.beijing.gov.cn/xwdt/kcyx/xwdtcyfz/202303/t20230328_3817948.html
- **北京科学智能研究院（AISI）2021 年 9 月成立**（北京，鄂维南院士牵头），与深势科技等共同构成 AI for Science 基础设施（Bohrium 平台、DPA-2 大原子模型、Uni-Mol 等，见第 2 节）。URL: https://www.aisi.ac.cn/
- 2023 科学智能峰会发布 2023 版《科学智能(AI4S)全球发展观察与展望》；鄂维南称"AI for Science 是中国科技创新历史上最好的机会"（21 世纪经济报道，2023-08-11）。URL: https://www.21jingji.com/article/20230811/herald/3adf5175382a920e52ef9bb3c334a15d.html
- **中国科学院 2021 年**发布重大科学问题清单并"揭榜挂帅"："数据驱动的化学、材料和生物科学的机器科学家"项目由中科大江俊团队揭榜，获 2021–2025 年连续 5 年共 2000 万元稳定支持（直接催生"机器化学家"成果，见第 10 节）。URL: https://news.ustc.edu.cn/info/1056/86925.htm
- **对成分设计的影响综述**：从专项数据/平台积累 → 小样本主动学习（Acta 2019 文成论文等）→ 生成式模型/大模型（CityU GAN 逆向设计 2023、DPA-2 大原子模型 2024、宿彦京团队 LLM 钢材设计 2024/2025、物理所"从小数据小模型到大数据大模型"报告 2025）的技术演进路径清晰可见。

---

## 23. 总结与"待核实"清单

**核实完成（有可靠网页来源）的核心结论**：
- 中国大陆在"ML/DL 优化材料成分设计"方向已形成**完整谱系**：被动预测（上大张统一 Materials & Design 2020；北科大宿彦京 Acta 2019）→ 主动学习/贝叶斯优化（Science 2022 因瓦 HEA，第一作者饶梓元，现职上交大；张统一团队 Bgolearn）→ 生成式逆向设计（CityU 杨勇 npj 2023 金属玻璃 GAN；物理所翁红明 Con-CDVAE）→ 大模型/机器人闭环（宿彦京 LLM 钢材设计 2024；中科大江俊机器化学家 NSR 2022/Nat. Synth. 2024；DPA-2 大原子模型 2024）。
- CALPHAD+ML 融合路线以**中南大学**（杜勇、张利军）最具系统性；软磁/非晶成分 ML 设计以**宁波材料所**（王军强/霍军涛）和 **CityU**（杨勇）为代表；合金相结构 ML 预测另有南理工刘伟、大连理工王清/董闯等团队。
- 台湾以**叶均蔚（新竹清华）+ NCHC** 的 ML 高熵材料平台（650 HV，超纪录 20%）为代表。

**待核实清单（重要）**：
1. 哈工大"苏彦梅/刘丽月"——未检索到任何证据，疑为讹误；哈工大 ML-RHEA 综述（L. Chen, 2026）的作者/院系待核实。
2. 上海大学材料基因组工程研究院建院年份；张统一在 AISI 的现任职务表述（院长 vs 学术委员会主任）两处来源不一致。
3. 中南大学：Acta Materialia 2024（TiAlTMN，DOI 10.1016/j.actamat.2024.120139）与 Nat. Commun. 14:2959 (2023) 的完整题目/作者；NiCoCrAl 论文（Mater. Today Commun. 30:103172）的通讯作者单位。
4. 大连理工王清 2022 年《Advanced Materials》软磁高熵合金论文与自动化 ML 高熵高温合金论文的完整引用。
5. 香港大学（黄明欣）、香港科技大学本部、香港中文大学/理工大学、北京大学材料学科的 ML 成分设计课题组（本次检索未命中）。
6. 叶均蔚团队 ML 成分设计具体期刊论文。
7. 《材料工程》2024 难熔 HEA ML 综述页码；《计算物理》综述作者；《Advanced Materials》浙大储氢综述卷期页。
8. DPA-2 覆盖元素数目与精度指标（需原文）。

---

*报告完。本报告所有事实均附来源 URL；"待核实"项均为本次检索未能确认的信息，未作任何臆测填充。*
