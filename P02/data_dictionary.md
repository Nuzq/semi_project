# P02 数据字典与来源口径

当前没有导入原始样本数据。四个 CSV 均由 `P02-EDU-V1` 解析模型计算生成；`output_class` 明确标识其为教学模型输出，不是实验测量。

| 字段 | 含义 | 单位/类型 | 来源/规则 |
|---|---|---|---|
| `model_id` | 单个解析关系的标识，如 `pn_diode_ideal_iv`、`long_channel_nmos_square_law` | 文本 | CSV 中的模型类型 |
| `parameter_set_id` | 参数集版本，此版为 `P02-EDU-V1` | 文本 | 对应 `parameters_v1.json` 与 `model_parameters_v1.md` |
| `output_class` | `analytical_teaching_model_output_not_measurement` | 文本 | 防止将模型输出误称为实测数据 |
| `diode_voltage_V`, `diode_current_A` | 理想二极管端电压和计算电流 | V、A | `pn_diode_iv_v1.csv` |
| `applied_junction_voltage_V`, `total_depletion_width_m` | PN 结外加偏压和总耗尽宽度 | V、m | `pn_depletion_v1.csv`；同时提供 p/n 侧宽度及 μm 列 |
| `gate_source_voltage_V`, `drain_source_voltage_V`, `drain_current_A` | MOSFET 栅源电压、漏源电压及计算漏极电流 | V、V、A | 两份 nMOS CSV；输出特性另含 `operating_region` |
| `operating_region` | `cutoff`、`linear` 或 `saturation` | 类别 | 本版强反型长沟道分段模型的区域标签 |
| `check_id` / `check_result` | 温度数量级、耗尽区电荷平衡、偏置范围、有限值等预检查 | 文本 / 布尔 | 汇总在 `model_summary_v1.json`；单元测试另见 `src/test_p02_model.py` |

每次导出保存公式版本、参数来源、模型假设、参数集 ID 和运行日期。外部曲线数字化如有发生，须进入独立文件并记图号/轴标，不能混入模型输出表。
