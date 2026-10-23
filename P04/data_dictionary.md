# P04 数据字典与等效热模型来源

当前无温度场或时间序列结果。未来来源包括手册指定参数、明确的情景输入和COMSOL/Python模型输出；不能将输出解释成产品内部实测温度。

| 字段 | 含义 | 单位/规则 | 来源类型 |
|---|---|---|---|
| source_id / source_locator | 数据来源及页/表/图号 | text | data_sources.md |
| device_id / datasheet_rev | 手册参考器件及版本 | IMZC120R012M2H / Rev. 1.20 | 官方手册，仅特定型号 |
| condition_id | 电压、电流、栅压、Tj和开关条件 | text | 手册测试条件或情景假设 |
| loss_W | 设定/计算热源功率 | W | 由参数或假设计算，不是实测应用波形 |
| material_property | k、rho、Cp等热物性 | SI units | 每项单独登记出处/假设 |
| thermal_resistance_K_W | 热阻 | K/W | 数据手册值/等效拟合参数需区分 |
| time_s | 瞬态求解时间 | s | 求解设置 |
| temperature_C | 计算温度 | °C | COMSOL/Python输出 |
| zth_K_W | 瞬态热阻 | K/W | 手册图数字化值或模型输出须分列 |
| mesh_id / timestep_s | 网格及时间步 | text / s | 求解日志 |

若数字化Zth曲线，另记图号、数据手册修订、坐标标定和拟合残差；严禁把图上读取值说成厂家原始采样点。
