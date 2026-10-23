# P01 材料工艺窗口与过程质量分析

## 项目进度

- [x] 只读确认论文原稿与实验数据目录存在，并建立目录级清单（文件级样品映射仍待完成）
- [ ] 建立字段和单位字典
- [ ] 整理工艺参数与 CTQ（已按论文方法初步列项，原始数据字段映射待完成）
- [ ] 完成性能分布和因素影响图
- [ ] 完成异常样本复核
- [ ] 输出工艺窗口或历史实验复盘结论
- [ ] 完成项目报告和简历 bullet

## 项目属性

- 数据：本人本科科研实验数据；
- 项目类型：真实材料工艺项目；
- 目标岗位：材料/封装工艺、工艺工程师、制造质量/NPI、良率/测试数据、失效分析；
- 真实性边界：不写成半导体量产项目。

## 研究对象

生物质基氮掺杂多孔炭及其超级电容器应用。重点整理前驱体处理、热解/预炭化、活化、氮掺杂或金属负载等工艺条件。

## 建议字段

```text
run_id
precursor_type
pretreatment_condition
precarbonization_temperature
activation_temperature
activation_time
activator_ratio
nitrogen_doping_condition
BET_surface_area
specific_capacitance
energy_density
cycle_retention
measurement_batch
notes
```

## 分析任务

1. 只使用可以追溯到原始记录的数据，不补造缺失数据；
2. 将实验输入参数与输出 CTQ 分开；
3. 对比不同前驱体和工艺条件；
4. 分析性能波动和异常曲线；
5. 有完整实验设计时做 DOE；否则写成历史实验数据复盘；
6. 有规格限和重复实验时再计算 Cpk/Ppk；
7. 输出材料制备工艺流程、性能关系图和条件迭代建议。

## 最小交付物

- `data_dictionary.md`；
- `process_flow.png`；
- `process_data.csv`；
- 3–5 张因素—性能关系图；
- `outlier_review.md`；
- `report.md` 或 PDF；
- `resume_bullets.md`。

## 简历角度

### 材料/封装工艺

强调材料体系、工艺条件、工艺窗口、结构—性能关系。

### 制程/工艺工程师

强调参数—CTQ、实验条件迭代、异常复核和过程记录。

### 质量/NPI

强调数据追溯、重复性、异常样本和关键质量特性。

### 失效分析

强调 SEM-EDS、XRD、Raman、XPS、BET、CV、GCD、EIS 和证据链。

## 90 秒讲解结构

> 我把本科材料实验记录重新整理成输入工艺参数和输出 CTQ 两部分，重点分析热解、活化和掺杂条件对比表面积、电化学性能和循环稳定性的影响。对于异常样本，我先复核实验条件和测试曲线，再判断是工艺波动还是测量问题。这个项目虽然不是半导体产线，但训练了工艺参数管理、关键质量特性定义和异常复核能力。

## 实验/分析日志

| 日期 | 完成内容 | 产出 | 问题/待确认 |
|---|---|---|---|
|  |  |  |  |
|  |  |  |  |

## 本轮 P01 交付进展（2026-10-17）

已完成论文证据初审和原始资料目录级只读盘点，并写出岗位差异化的简历草稿。资料与边界说明见：

- [`P01/source_inventory.md`](../P01/source_inventory.md)
- [`P01/claim_evidence_audit.md`](../P01/claim_evidence_audit.md)
- [`P01/resume_versions.md`](../P01/resume_versions.md)

**当前状态：部分完成，不等于P01项目完成。** 尚未做原始数据逐文件映射、数据字典、复算、图表和异常复核。简历中的个人实验职责要经本人确认；未确认前保留“研究/参与”措辞。
