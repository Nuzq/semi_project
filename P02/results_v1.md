# P02 最小可复现模型｜第一版运行记录

- 参数集：`P02-EDU-V1`
- 运行日期：2026-10-23
- Python：`3.12.7`
- 输入：`parameters_v1.json`；完整输入分类见 `model_parameters_v1.md`。
- 输出性质：解析教学模型计算值，不是实验测量、COMSOL/TCAD 数值求解或产品预测。

## 本次计算出的关键量

- 300 K 热电压：25.85200 mV。
- PN 结内建电势：0.654791 V。
- 零偏总耗尽宽度：0.9651 μm；伸入 p 侧 0.0877 μm，伸入 n 侧 0.8774 μm。
- MOS 单位面积栅氧电容：0.00345313 F/m²。
- p 型衬底费米势：0.357159 V；由简化阈值公式计算的阈值电压：0.855334 V。
- `VGS=2 V, VDS=1 V` 时：过驱动电压 1.144666 V，漏极电流 3.223420 mA，模型工作区 `linear`。

## 自动预检查

- [x] `thermal_voltage_300K_is_about_25_85mV`
- [x] `built_in_potential_is_positive`
- [x] `depletion_charge_balance`
- [x] `depletion_sweep_stays_below_built_in_potential`
- [x] `mos_threshold_is_positive`
- [x] `mos_base_point_is_above_threshold`
- [x] `all_model_outputs_are_finite`

这些预检查是数值/边界自检，不是与实验或第三方器件仿真的验证。完整回归测试请运行 `python -m unittest src.test_p02_model -v`。

## 输出文件

- `data/pn_diode_iv_v1.csv`：理想二极管 I–V 扫描。
- `data/pn_depletion_v1.csv`：PN 结耗尽区随结偏压变化。
- `data/nmos_output_iv_v1.csv`：长沟道 nMOS 输出特性。
- `data/nmos_transfer_iv_v1.csv`：长沟道 nMOS 转移特性。
- `figures/*.png`：由上述冻结输入及解析模型生成的曲线图。
- `model_summary_v1.json`：派生值、运行环境和预检查状态。

## 未纳入第一版

本版固定 300 K，不含完整温度依赖、反向击穿、亚阈值电流、沟道长度调制、短沟道、高场速度饱和、界面陷阱、自热或 SiC 参数。后续逐项扩展时需新增参数来源和验证，不应把本版称为产品级器件模型。
