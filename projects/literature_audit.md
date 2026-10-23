# P02–P07 文献与数据来源交叉核验

核验日期：2026-10-21。范围：当前重构的SiC MOSFET基础建模、电热分析、可靠性与测试数据项目。书目真实性与“研究结论是否适用于项目”分开判断；来源真实，不等于其结果可以外推到别的器件/条件。

## 核验等级
- **A1**：出版社书目/摘要 + 可读全文或作者接受稿；全文结论只对已读版本作描述。
- **A2**：出版社书目/摘要或Key points已核；不能声称逐句核读全文Discussion/Conclusion。
- **B**：出版社书目与公开摘要核对；全文未读，只引用摘要层面的结论。
- **O**：官方软件文档、验证模型或厂商数据手册；不是期刊论文。

## 逐篇来源核验

| 来源 | 元数据/真实性核对 | 内容核对范围 | 可支持的项目内容 | 不可据此声称 |
|---|---|---|---|---|
| Kubulus et al., “Approximate SPICE Modeling of SiC MOSFETs,” IEEE TPEL 40(4), 5201–5211 (2025), DOI 10.1109/TPEL.2024.3510037 | IEEE DOI记录与TU Eindhoven/Aalborg研究门户的题名、作者、期刊、卷期页码相符；A2 | 已核对出版社/机构门户摘要：简化SiC MOSFET SPICE模型与仿真效率/精度比较。未把全文Discussion写为已读。 | P02模型验证理念与研究背景 | 复现其模型、实验或把论文器件参数当成本项目的PN/MOS参数 |
| Wang et al., “Packaging and integration of silicon carbide power devices,” Nature Reviews Electrical Engineering 3, 157–172 (2026), DOI 10.1038/s44287-026-00263-0 | Nature出版社书目记录、摘要和Key points；A2 | 可核信息支持SiC封装的高热流密度、热管理及电热协同问题。全文Discussion未逐句核读。 | P04/P07问题背景与热路径建模动机 | 声称逐句复现其展望或引用不可见全文的具体数值 |
| Wu, Grasser & Lanza, “Industrial reliability testing of transistor gate dielectrics,” Nature Electronics 9, 726–732 (2026), DOI 10.1038/s41928-026-01644-x | Nature书目、摘要、Supplementary Data 1 Excel条目及作者更正记录；A2 | 已核对公开页面对RVS击穿统计和V_MAX处理流程的描述。2026-07-30另有作者更正；逐图提取时必须用更新版本。未将其描述成SiC器件寿命研究。 | P05 Weibull/寿命指标流程练习与作者工具核算 | 把补充Excel称作原始样本库；把硅/二维介质数据外推为SiC寿命 |
| Yu et al., “Repetitive-Avalanche-Induced Degradation in 1.2-kV SiC Trench-Gate MOSFETs and a Practical R-UIS-Based Screening Method,” IEEE TPEL 41(6), 8857–8868 (2026), online 2025-12-26, DOI 10.1109/TPEL.2025.3648326 | IEEE记录与Ohio State公开作者接受稿书目相符；A1（全文依据为作者接受稿，书目依据为出版社） | 已阅读可访问作者稿的结论；作者报告的参数漂移、封装变化及其特定筛查条件只对应论文中的两类器件和测试条件。 | P03器件场景语境；P04电热/应力语境；P06指标选择；P07证据链结构 | 将作者筛查条件当作通用量产阈值；声称本项目做过R-UIS/TCAD实验复现 |
| Zhan et al., “Abnormal Behavior of Conduction Characteristics by Surge Current Stress in NO-Oxidation-Annealed SiC-MOSFETs,” IEEE TED 73(8), 4764–4774 (2026), DOI 10.1109/TED.2026.3698811 | IEEE出版记录与摘要；B | 只核到公开摘要/元数据，未逐项审阅全文Discussion/Conclusion。 | P06说明浪涌应力与导电特性是近期测试问题 | 任何未由摘要明确支持的具体机理、数值或完整结论 |
| Shqair et al., “Transient thermal 2D FEM analysis of SiC MOSFET in short-circuit operation including high-temperature material laws and phase transition of aluminum source electrode,” Microelectronics Reliability 159, 115440 (2024), DOI 10.1016/j.microrel.2024.115440 | ScienceDirect出版社书目/摘要记录；B | 摘要层面显示研究采用二维瞬态热FEM并讨论高温材料性质及铝相变；全文Discussion未逐句核读。本篇仅作较早的方法背景。 | P04复杂热FEM方法对照 | 直接移植其器件内部参数、短路阈值或未核验的实验结论 |

## 官方模型和数据源

| 来源 | 核验结果 | 项目用途和限制 |
|---|---|---|
| COMSOL 6.4 Semiconductor Module, P–N Junction 1D | 官方模型页给出硅、一维总计算域5 μm、两侧净掺杂1×10^15 cm⁻³、−4/0/0.5 V偏压，并说明数值解与有限体积/参考例对照；O | P03首轮复现及P02数量级核查。不是期刊论文，不是实测数据；只支撑指定硅模型。 |
| Infineon IMZC120R012M2H datasheet Rev. 1.20, 2025-07-04 | Infineon官方产品/下载页可核对型号、文档修订及Rth/Zth相关规格；O | P02/P04/P06参数量级和字段语境。只代表该型号及数据手册条件；不代表Yu研究器件或本项目实测值。 |
| MIT OpenCourseWare 6.012器件讲义 | MIT官方课程页面和讲义用于检查基础PN结/MOS公式；O | P02理论来源；实施时需给出具体讲义标题、页码/式号，不以课程材料冒充论文。 |

## 数据真实性与交叉验证原则
- P02输出由解析方程生成；P03/P04输出是数值模型结果；P05/P06预定的主要分析样本为自建合成教学数据；P07只组合这些来源。以上都不是晶圆厂/ATE/实验室实测数据。
- 公开论文图表数字化点属于二次派生数据，必须保存DOI、版本、图号、坐标标定和误差；不得称为原始样本或大规模公开数据集。
- 任何具体外部参数必须记录source_id、页/表/图、单位、温度/电压/电流条件、文档版本和核对日期。文件下载后保存哈希值，避免无声替换版本。
- 若项目说明与出版社摘要、作者稿或数据手册版本冲突，以原始来源为准，修正项目文本；不得以二手摘要覆盖原始论文声明。
- 技术内容的核验结论是“该来源存在且文档中的概述不超出可访问证据”，不是对论文方法学作独立同行评审。

## 关键链接
- [Kubulus et al. DOI](https://doi.org/10.1109/TPEL.2024.3510037)
- [Wang et al. DOI](https://doi.org/10.1038/s44287-026-00263-0)
- [Wu et al. DOI](https://doi.org/10.1038/s41928-026-01644-x)
- [Wu et al. author correction DOI](https://doi.org/10.1038/s41928-026-01690-5)
- [Yu et al. DOI](https://doi.org/10.1109/TPEL.2025.3648326)
- [Yu et al. Ohio State public accepted manuscript](https://bpb-us-w2.wpmucdn.com/u.osu.edu/dist/f/88613/files/2026/01/Repetitive-Avalanche-Induced_Degradation_in_1.2-kV_SiC_Trench-Gate_MOSFETs_and_a_Practical_R-UIS-Based_Screening_Method.pdf)
- [Zhan et al. DOI](https://doi.org/10.1109/TED.2026.3698811)
- [Shqair et al. DOI](https://doi.org/10.1016/j.microrel.2024.115440)
- [COMSOL 6.4 P–N Junction 1D example](https://doc.comsol.com/6.4/doc/com.comsol.help.models.semicond.pn_junction_1d/pn_junction_1d.html)
- [Infineon IMZC120R012M2H datasheet](https://www.infineon.com/assets/row/public/documents/60/49/infineon-imzc120r012m2h-datasheet-en.pdf)
