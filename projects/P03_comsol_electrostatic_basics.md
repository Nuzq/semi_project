# P03｜COMSOL 半导体方程基准：一维硅 PN 结

## 定位
复现 COMSOL 官方 Semiconductor Module 一维 PN 结验证案例，熟悉几何、掺杂、物理接口、边界条件、网格、求解器和结果核查。该基准先限定为官方示例支持的一维硅结；不把它写成 SiC MOSFET 或二维器件仿真。

## 实施范围
- 依据 COMSOL 6.4 官方 P–N Junction 1D 案例设置硅材料、总计算域长度 5 μm、两侧净掺杂浓度各 1×10^15 cm⁻³，并复算 −4 V、0 V、0.5 V 偏压案例。
- 使用 Semiconductor 接口时，记录版本、模块、方程、掺杂、接触、边界、网格和求解设置；比较电势、载流子和电流密度趋势。
- 与官方示例所述有限元/有限体积解及P02解析模型做数量级与趋势对照；补做网格/求解容差敏感性。
- 若无 Semiconductor Module，另行标注为 Poisson/静电近似；该近似不等价于官方漂移—扩散 PN 结复现，也不能得到真实二极管 I–V。

## 研究文献依据
- Yu et al., “Repetitive-Avalanche-Induced Degradation in 1.2-kV SiC Trench-Gate MOSFETs and a Practical R-UIS-Based Screening Method,” IEEE Transactions on Power Electronics 41(6), 8857–8868 (2026), DOI [10.1109/TPEL.2025.3648326](https://doi.org/10.1109/TPEL.2025.3648326)。论文以器件实验、LTspice和Sentaurus TCAD分析特定沟槽器件的重复雪崩问题，可作“场分布与器件可靠性需依托边界/结构/验证条件”的工程语境。它不是本项目COMSOL模型的验证数据，也不支持把特定失效结果外推到本项目硅PN结。

## 数据/参数来源
| 来源 | 数据类型 | 使用方式 |
|---|---|---|
| COMSOL官方 P–N Junction 1D 示例 | 官方数值基准与模型参数 | 作为首轮可复现输入和求解结果对照；保留版本、参数和截图/导出值。 |
| P02解析模型 | 本项目代码计算值 | 对照偏压趋势和数量级，不把解析近似当作独立实验。 |
| COMSOL求解输出 | 自生成的仿真数据 | 标注为模型输出；保存模型文件、网格和求解日志。 |
| Yu等研究 | 论文研究背景 | 不抽取其器件测试曲线作为硅PN结输入。 |

## 核验状态与限制
COMSOL文档确认示例使用硅、5 μm 计算域、两侧1×10^15 cm⁻³净掺杂及三个偏压点，并说明与有限体积解/教材示例对照。相关IEEE论文的出版社元数据和Ohio State公开作者稿可交叉核对；作者稿结论已阅读，但其器件、应力和筛查条件不构成本项目参数。详细核验等级见 literature_audit.md。

## 进度
- [ ] 确认 COMSOL 版本和 Semiconductor Module 可用性
- [ ] 完成官方一维基准复算或明确降级替代方案
- [ ] 完成网格/容差敏感性
- [ ] 形成与P02的解析对照
- [ ] 导出模型文件、数据和复现说明
