# P02｜PN结与MOSFET基础模型

项目定义见项目目录中的 P02_device_physics_foundations.md，数据和文献来源见 data_sources.md。当前第一版参数集为 `P02-EDU-V1`，实现硅 PN 结/二极管与硅基长沟道 nMOS 的解析教学模型；旧 Underfill 数据、图表和生成/分析脚本已清理。共享运行时 Junction 保留，不属于旧项目产物。

## 当前学习入口

- 初学者讲义与交互演示：learning/README.md、learning/index.html
- 方程、单位与来源技术底稿：equation_source_table.md

## 运行模型

在 P02 目录执行：

```powershell
python -m src.run_model
python -m unittest src.test_p02_model -v
```

计算输入固定在 `parameters_v1.json`，冻结说明见 `model_parameters_v1.md`。运行后生成 `data/` 中的 CSV、`figures/` 中的 PNG、`model_summary_v1.json` 和 `results_v1.md`。

**模型边界：**教学页面的滑块仍是概念示意；Python 脚本则按冻结参数计算解析模型曲线。两者都不是实测、COMSOL/TCAD 数值求解或产品预测。当前模型不含 SiC 器件参数、完整温度行为、反向击穿、亚阈值、短沟道、高场、自热或界面陷阱。
