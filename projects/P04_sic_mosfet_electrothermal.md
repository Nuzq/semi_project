# P04｜SiC MOSFET 简化损耗—热路径模型

## 定位
三项优先作品之一。以公开数据手册为参数参照，建立可解释的功耗输入与等效热路径模型，展示热源、热阻/热容、温度响应及边界条件之间的关系。COMSOL只承担简化热传导求解；不假称建立产品内部真实芯片结构或完整器件电—热TCAD。

## 研究依据
- Wang et al., “Packaging and integration of silicon carbide power devices,” Nature Reviews Electrical Engineering 3, 157–172 (2026), DOI [10.1038/s44287-026-00263-0](https://doi.org/10.1038/s44287-026-00263-0)。出版社摘要与Key points支持高热流密度、封装热管理和电—热协同是SiC工程问题；全文Discussion未作逐句核读，不能把摘要扩写为论文的具体实验结论。
- Yu et al. 2026 IEEE TPEL论文，DOI [10.1109/TPEL.2025.3648326](https://doi.org/10.1109/TPEL.2025.3648326)，作者公开稿报告重复雪崩器件的电参数退化、封装退化和电热/TCAD分析。用于应力场景背景，不复现其雪崩试验、微观损伤或筛查阈值。
- Shqair et al., “Transient thermal 2D FEM analysis of SiC MOSFET in short-circuit operation including high-temperature material laws and phase transition of aluminum source electrode,” Microelectronics Reliability 159, 115440 (2024), DOI [10.1016/j.microrel.2024.115440](https://doi.org/10.1016/j.microrel.2024.115440)。作为复杂热FEM方法参考；2024年论文不是近一年热点证据，本项目不采用其不可核验的器件内部参数或短路失效阈值。

## 数据与参数来源
- Infineon IMZC120R012M2H 官方数据手册 Rev. 1.20（2025-07-04）：记录RDS(on)、损耗测试条件、Rth(j-c)和Zth(j-c)曲线时，必须保留表/图号、温度、电流、电压、栅压和器件版本；典型值、最大值不混用。
- 功耗输入优先从数据手册指定测试条件计算，或明确标作情景假设。导通损耗可先采用 I²RDS(on)；开关损耗另列，不能把情景波形称为器件实测应用数据。
- COMSOL温度场是本项目求解输出；未公开的芯片尺寸、材料分层、界面热阻和热源位置均标为等效假设。模型目标是匹配外部等效热响应，不重建真实芯片内部温度场。
- 如读取数据手册瞬态热阻图，记录坐标标定、图号、读取/拟合误差；图上曲线派生点不是原始测量点。

## 验证和边界
用Rth(j-c)/Zth(j-c)作整体热响应校核，并以能量守恒、稳态极限、网格和时间步敏感性检查COMSOL输出。资料只支持手册指定器件和测试条件下的参数参照，不支持推出任意工况下的结温、可靠性寿命或失效因果。COMSOL授权/热传导接口未确认前，不声称已完成软件仿真。

## 进度
- [ ] 冻结数据手册版本、图表号和工况
- [ ] 建立Python功耗/热网络基线
- [ ] 建立等效热传导模型
- [ ] 完成稳态、能量、网格及时间步验证
- [ ] 完成温度场/曲线和参数敏感性
- [ ] 完成报告与简历条目
