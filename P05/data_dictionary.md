# P05 数据字典与来源口径

主要样本计划为自建合成教学数据；Nature Electronics作者补充Excel作为计算流程参照，不按原始样本数据库处理。

| 字段 | 含义 | 单位/类型 | 来源规则 |
|---|---|---|---|
| sample_id | 教学样本编号 | text | 本项目生成 |
| dataset_type | synthetic / digitized_public / author_tool_example | category | 每行或每文件显著标注 |
| stress_voltage / stress_temperature | 应力条件 | V / °C | 指定来源或合成场景，不跨体系外推 |
| time_to_failure_or_voltage | 失效时间或击穿电压 | s / V | 合成数据或论文图表派生点，严格分文件 |
| censored | 右删失状态 | bool | 生成规则/原始来源 |
| weibull_shape | Weibull形状参数 | dimensionless | 拟合输出，不是输入的原始测量 |
| weibull_scale | Weibull尺度参数 | same as response | 拟合输出 |
| confidence_interval | 参数区间 | numeric bounds | 统计方法输出 |
| source_id / source_locator | DOI、补充文件或图号 | text | data_sources.md |
| random_seed / generator_version | 随机种子/脚本版本 | integer / text | 合成数据必填 |

补充Excel是作者计算工具，只有工具输入/公式可核验时才作为方法对照，不自动构成原始可靠性数据。
