# P04 数据与文献来源清单

核对日期：2026-10-21。当前尚无功耗表、热网络或温度场输出。

| ID | 来源 | 核验方式 | 用途 | 限制 |
|---|---|---|---|---|
| P04-L01 | Wang et al., Nature Reviews Electrical Engineering (2026), DOI 10.1038/s44287-026-00263-0 | Nature书目、摘要与Key points | 热管理/电热协同工程背景 | 未逐句核读全文Discussion；不是具体产品模型或数据 |
| P04-L02 | Yu et al., IEEE TPEL (2026), DOI 10.1109/TPEL.2025.3648326 | IEEE元数据与Ohio State作者稿全文结论 | 重复雪崩场景及退化指标背景 | 只对应论文特定器件/条件，不能移植阈值或失效结论 |
| P04-L03 | Shqair et al., Microelectronics Reliability 159, 115440 (2024), DOI 10.1016/j.microrel.2024.115440 | ScienceDirect出版记录/摘要 | 瞬态热FEM方法参照 | 2024方法文献；不使用未核全文的细节或阈值 |
| P04-D01 | Infineon IMZC120R012M2H datasheet Rev. 1.20 (2025-07-04) | Infineon官方数据手册型号/版本、Rth和Zth项核对 | 记录指定器件的电参数、热阻、热阻抗及测试条件 | 不代表Yu研究器件；典型/最大值与曲线条件不可混用 |
| P04-D02 | 本项目COMSOL/Python输出 | 留存模型文件、假设、网格、时间步和脚本版本 | 等效热路径温度结果 | 模型输出，不是产品内部温度实测 |
| P04-D03 | 数据手册曲线数字化值（若需要） | 逐图记录轴标、标定、拟合误差 | 作为整体热响应对照 | 派生读数，不是厂家原始测量点 |

每个热源值须注明来自数据手册指定测试条件、由公式换算，或为明确的情景假设。未知芯片层厚/界面热阻不得伪装成官方数据。

来源链接：
- Wang et al.: https://doi.org/10.1038/s44287-026-00263-0
- Yu et al.: https://doi.org/10.1109/TPEL.2025.3648326
- Shqair et al.: https://doi.org/10.1016/j.microrel.2024.115440
- Infineon datasheet: https://www.infineon.com/assets/row/public/documents/60/49/infineon-imzc120r012m2h-datasheet-en.pdf
