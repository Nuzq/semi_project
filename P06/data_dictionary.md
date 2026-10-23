# P06 数据字典与来源口径

项目数据以自建、固定种子的合成教学样本为主；当前没有真实SiC器件或产线测试数据。

| 字段 | 含义 | 单位/规则 | 来源 |
|---|---|---|---|
| sample_id | 教学样本编号 | text | 本项目生成 |
| device_group | 教学条件分组 | category | 规则在生成脚本中公开 |
| stress_condition | 应力等级/条件标签 | text | 参考论文设计，不移植论文筛查阈值 |
| measurement_stage | before / after / retest | category | 教学矩阵 |
| vth_V | 阈值电压 | V | 参数定义/单位参考Yu论文，值为合成值 |
| rdson_ohm | 导通电阻 | Ω | 参数定义/测试条件须标注，值为合成值 |
| third_quadrant_metric | 第三象限电压/电流指标 | V or A | 来源定义逐项注明，值为合成值 |
| leakage_A | 栅/漏漏电指标 | A | 明确测量定义，值为合成值 |
| missing_or_retest_flag | 缺失/复测标记 | bool/category | 合成规则 |
| source_id / random_seed | 来源和随机种子 | text / integer | data_sources.md及生成脚本 |

论文图表数字化值若后续增加，另建数据文件，记录DOI、版本、图号、坐标和读取误差，不与合成样本混合。
