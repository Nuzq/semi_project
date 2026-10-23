# P02 数据与文献来源清单

来源核对日期：2026-10-21。模型输出生成日期：2026-10-23。

| ID | 来源 | 核验方式 | 用途 | 限制 |
|---|---|---|---|---|
| P02-L01 | Kubulus et al., IEEE TPEL (2025), DOI 10.1109/TPEL.2024.3510037 | DOI书目与TU Eindhoven/Aalborg研究门户题名、作者、卷期页码核对；摘要级内容已核 | SiC紧凑模型研究语境、模型验证思路 | 不复刻其模型/实验，不用其器件参数做本项目数据 |
| P02-T01 | MIT OpenCourseWare 6.012（Fall 2009）Lecture 1、4–6、9–11 | MIT官方课程页/各讲义核对主题与标题 | 载流子统计、PN结静电与I–V、MOS阈值与长沟道I–V方程 | 课程讲义，不是期刊论文；适用于基础教学模型，不代表产品校准 |
| P02-T02 | COMSOL Semiconductor Module方程文档及P–N Junction 1D官方例 | COMSOL官方文档核对 | PN结数量级/趋势对照 | 官方技术资料，不是实测数据；不用于验证MOS模型所有假设 |
| P02-T03 | NIST CODATA 2022：元电荷、Boltzmann常数、真空介电率 | NIST常数页面核对数值与单位 | 物理常数与热电压计算 | 真空介电率是基础常数；硅/氧化层介电率还需相对介电常数 |
| P02-T04 | COMSOL Semiconductor Material Properties / Power Law Mobility Model（6.3文档） | 官方文档核对硅材料参数的名称、SI单位和简单温度迁移率模型 | 单位交叉检查、候选硅教学迁移率参数 | 软件材料参数是模型输入参考，不是器件实测值；幂律模型不等于完整迁移率模型 |
| P02-D01 | `src/p02_model.py` 与 `src/run_model.py` 按 `P02-EDU-V1` 计算生成的模型输出 | 参数输入、脚本、运行日期和 `model_summary_v1.json` 随输出保存；7 项单元测试与脚本预检查通过 | PN 结/理想二极管曲线、长沟道 nMOS 输出/转移特性 | 解析教学输出，非测量、TCAD/COMSOL 或产品拟合；预检查不等同于实验验证 |
| P02-D02 | Infineon IMZC120R012M2H官方数据手册Rev. 1.20 | 官方产品页/数据手册型号和文档版本核对 | 可选的SiC规格/量纲背景 | 不将手册曲线拟合成通用长沟道MOS模型 |

## 生成数据时的必填追溯项
公式/常数来源、参数单位和温度、教学假设、代码版本、输入参数文件、运行日期、模型输出类型。若数字化任何外部图表，需单独保存图号、坐标标定、读数误差，不能混入解析模型输出。

## 来源链接
- Kubulus et al.: https://doi.org/10.1109/TPEL.2024.3510037
- MIT 6.012 Fall 2009 Lectures 1, 4–6, 9–11: https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2009/resources/
- NIST CODATA 2022 constants: https://www.physics.nist.gov/cuu/pdf/wall_2022.pdf
- COMSOL silicon material properties: https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/comsol_ref_materials.25.47.html
- COMSOL power-law mobility model: https://doc.comsol.com/6.3/doc/com.comsol.help.semicond/semicond_ug_semiconductor.6.13.html
- COMSOL PN junction example: https://doc.comsol.com/6.4/doc/com.comsol.help.models.semicond/pn_junction_1d.html
- Infineon datasheet: https://www.infineon.com/assets/row/public/documents/60/49/infineon-imzc120r012m2h-datasheet-en.pdf
