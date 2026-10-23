# P03 数据字典与COMSOL基准来源

当前未生成求解数据。基准输入来自COMSOL官方 P–N Junction 1D 示例；求解输出需标记为数值模型结果，不是实验数据。

| 字段 | 含义 | 单位/值 | 来源 |
|---|---|---|---|
| source_id | 输入来源ID | text | data_sources.md |
| model_version | COMSOL版本/模块 | text | 运行环境记录 |
| domain_length_um | 一维总计算域长度 | 5 μm | 官方COMSOL示例 |
| material | 半导体材料 | Silicon | 官方COMSOL示例 |
| net_doping_cm3 | 两侧净掺杂浓度 | 1×10^15 cm⁻³ each | 官方COMSOL示例 |
| bias_V | 端口偏压 | −4, 0, 0.5 V | 官方COMSOL示例 |
| mesh_id / element_count | 网格版本/数量 | text / integer | COMSOL模型导出 |
| potential_V | 静电势/电势 | V | 模型输出 |
| n_m3 / p_m3 | 电子/空穴浓度 | m⁻³ | Semiconductor接口模型输出 |
| current_density_A_m2 | 电流密度 | A/m² | Semiconductor接口模型输出 |

记录官方示例版本、模型文件、偏压、网格、求解器、收敛状态和导出时间。Poisson-only替代模型需要另设model_id，不得与官方漂移—扩散模型混称。
