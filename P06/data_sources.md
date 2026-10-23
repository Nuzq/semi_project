# P06 数据与文献来源清单

核对日期：2026-10-21。当前没有真实测试数据或合成分析样本。

| ID | 来源 | 核验方式 | 用途 | 限制 |
|---|---|---|---|---|
| P06-L01 | Yu et al., IEEE TPEL (2026), DOI 10.1109/TPEL.2025.3648326 | IEEE元数据 + Ohio State公开作者接受稿全文/Conclusion | 指标与研究问题设计 | 其两类器件、应力方法和筛查条件只对原研究成立 |
| P06-L02 | Zhan et al., IEEE TED (2026), DOI 10.1109/TED.2026.3698811 | IEEE出版记录/摘要 | 确认浪涌后导电行为是相关研究问题 | 仅摘要级核验；不据此引用具体数值、机理或完整结论 |
| P06-D01 | 本项目Python合成样本 | 生成后固定seed、生成器版本和规则 | 主分析数据 | 仅流程演练；图表必须写明“合成教学数据” |
| P06-D02 | Infineon IMZC120R012M2H手册Rev.1.20 | Infineon官方手册及产品记录 | 量纲、字段和独立器件参数背景 | 不是Yu文章的器件、不是本项目测试对象或数据 |
| P06-D03 | 论文图表数字化点（可选） | DOI、文章版本、图号、坐标标定、读数误差 | 单独的趋势复核 | 不构成样本级数据；不和合成样本合并 |

差异核验时保留应力方法、偏压、温度、样本器件和测试定义；不得照抄研究中的筛查限值。每列参数均需可追溯到来源及测量定义。

来源链接：
- Yu et al. DOI：https://doi.org/10.1109/TPEL.2025.3648326
- Yu et al. Ohio State作者接受稿：https://bpb-us-w2.wpmucdn.com/u.osu.edu/dist/f/88613/files/2026/01/Repetitive-Avalanche-Induced_Degradation_in_1.2-kV_SiC_Trench-Gate_MOSFETs_and_a_Practical_R-UIS-Based_Screening_Method.pdf
- Zhan et al. DOI：https://doi.org/10.1109/TED.2026.3698811
- Infineon datasheet：https://www.infineon.com/assets/row/public/documents/60/49/infineon-imzc120r012m2h-datasheet-en.pdf
