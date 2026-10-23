# P06｜SiC MOSFET 参数变化筛查：测试指标与数据分析

## 定位
服务测试、产品、可靠性及失效分析岗位，建立“应力前—应力后”测试数据检查、分组比较和后续验证矩阵。项目只训练数据判读，不实施R-UIS、浪涌、ATE或探针台测试。

## 论文依据
- Yu et al., “Repetitive-Avalanche-Induced Degradation in 1.2-kV SiC Trench-Gate MOSFETs and a Practical R-UIS-Based Screening Method,” IEEE Transactions on Power Electronics 41(6), 8857–8868 (2026), DOI [10.1109/TPEL.2025.3648326](https://doi.org/10.1109/TPEL.2025.3648326)。IEEE记录和Ohio State公开作者稿元数据一致；作者稿全文Conclusion已核读。研究报告特定器件在重复雪崩条件下的Vth、RDS(on)、第三象限特性及封装变化，并结合实验、LTspice和Sentaurus TCAD。研究器件、应力条件和筛查阈值均特定，不移植到其他型号。
- Zhan et al., “Abnormal Behavior of Conduction Characteristics by Surge Current Stress in NO-Oxidation-Annealed SiC-MOSFETs,” IEEE Transactions on Electron Devices 73(8), 4764–4774 (2026), DOI [10.1109/TED.2026.3698811](https://doi.org/10.1109/TED.2026.3698811)。目前仅按IEEE书目记录和公开摘要引用；未把未见全文的Discussion/Conclusion写成本项目已核实结论，也不使用其具体数值作为输入。

## 数据来源
- 主要分析数据为本项目自行生成的合成教学数据：保留固定随机种子、生成规则、脚本版本、测量阶段、缺失/复测标记；每张图表都标记“合成数据”。
- 指标选择和测试条件定义参考Yu作者稿全文；不复制其研究样本或用作者筛查阈值标注本项目数据。
- Infineon IMZC120R012M2H官方数据手册只作字段范围/单位的独立器件参照，不代表Yu研究中的器件，也不是本项目测量结果。各字段的偏压、温度和测量定义应另列来源。
- 若后续使用论文图表数字化值，单独存储派生点，注明DOI、版本、图号、轴标和标定误差；不可称作样本级原始数据。

## 工作内容和交付
1. 建立样本ID、组别、应力等级、测量阶段、Vth、RDS(on)、第三象限参数及漏电等字段字典。
2. 完成数据完整性、单位、测量阶段配对、异常点复核和基线漂移检查。
3. 对前后变化计算效应量/置信区间，按组可视化并记录分析假设。
4. 建立“现象—候选机理—所需补测—证伪条件”矩阵，不把相关性写作因果。

## 真实性边界
统计输出只能说明“在所设教学数据中检测到变化”。不声称真实器件退化、筛出弱品、改善良率或完成失效根因确认。

## 进度
- [ ] 冻结指标、单位和来源映射
- [ ] 生成带标识的教学数据
- [ ] 完成数据质量与统计分析
- [ ] 完成机理假设/证伪矩阵
- [ ] 完成项目卡
