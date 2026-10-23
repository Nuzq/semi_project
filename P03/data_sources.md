# P03 数据与文献来源清单

核对日期：2026-10-21。当前尚无COMSOL求解输出。

| ID | 来源 | 核验方式 | 用途 | 限制 |
|---|---|---|---|---|
| P03-D01 | COMSOL 6.4 Semiconductor Module, P–N Junction 1D | COMSOL官方模型页核对硅材料、5 μm总域、两侧1×10^15 cm⁻³净掺杂、−4/0/0.5 V偏压及求解对照说明 | 复现基线、输入参数及数值结果对照 | 一维硅模型；COMSOL技术案例不是实验样本或期刊论文 |
| P03-L01 | Yu et al., IEEE TPEL (2026), DOI 10.1109/TPEL.2025.3648326 | IEEE书目 + Ohio State公开作者接受稿元数据；全文结论以接受稿核读 | 器件场/应力问题的工程语境 | 不作为COMSOL参数或PN结基准；不移植应力阈值 |
| P03-D02 | 本项目COMSOL导出结果 | 模型文件、版本、模块、网格和求解日志留存 | 电势/载流子/电流密度结果 | 数值仿真，不是实验数据 |
| P03-D03 | P02解析模型输出 | 与P02模型版本和参数文件关联 | 趋势/数量级交叉检查 | 两模型假设不同，不构成独立实验验证 |

## 降级方案
若无Semiconductor Module，可做单独标注的Poisson静电近似；需明确其方程、空间电荷和边界设置，不写作官方漂移—扩散PN结示例复现。不得输出或宣称真实PN结I–V。

来源链接：
- COMSOL官方示例：https://doc.comsol.com/6.4/doc/com.comsol.help.models.semicond.pn_junction_1d/pn_junction_1d.html
- Yu et al. DOI：https://doi.org/10.1109/TPEL.2025.3648326
- Ohio State作者接受稿：https://bpb-us-w2.wpmucdn.com/u.osu.edu/dist/f/88613/files/2026/01/Repetitive-Avalanche-Induced_Degradation_in_1.2-kV_SiC_Trench-Gate_MOSFETs_and_a_Practical_R-UIS-Based_Screening_Method.pdf
