# 旧项目数据与中间文件清理记录

清理日期：2026-10-21。清理范围仅限 semi_project/P02–P07 内已被新版主线取代的旧项目产物。

## 清理内容
共删除 39 个旧文件，包括P02 Underfill DOE/SPC/PFMEA案例的数据、脚本、检查导出、工作簿、图表、结果表与报告；P05旧封装失效案例卡；P06旧设备FDC日志、生成脚本和Python缓存。

- `P02/8D.md`
- `P02/analysis_summary.json`
- `P02/analyze_p02.py`
- `P02/build_quality_workbooks.mjs`
- `P02/check_formulas.mjs`
- `P02/Control_Plan.xlsx`
- `P02/Control_Plan.xlsx.inspect.ndjson`
- `P02/doe_plan.csv`
- `P02/generate_data.py`
- `P02/interview_notes.md`
- `P02/OCAP.md`
- `P02/PFMEA.xlsx`
- `P02/PFMEA.xlsx.inspect.ndjson`
- `P02/process_flow.md`
- `P02/process_timeseries.csv`
- `P02/report.md`
- `P02/run_manifest.json`
- `P02/verify_quality_workbooks.mjs`
- `P02/data/doe_data.csv`
- `P02/data/process_timeseries.csv`
- `P02/figures/control_chart_void_ratio.png`
- `P02/figures/Control_Plan.png`
- `P02/figures/doe_interactions.png`
- `P02/figures/doe_main_effects.png`
- `P02/figures/model_coefficients.png`
- `P02/figures/PFMEA.png`
- `P02/figures/process_capability.png`
- `P02/figures/process_flow.png`
- `P02/tables/anova_results.csv`
- `P02/tables/control_chart_summary.csv`
- `P02/tables/control_chart_void_ratio.csv`
- `P02/tables/feasible_grid.csv`
- `P02/tables/main_effects.csv`
- `P02/tables/model_coefficients.csv`
- `P02/tables/process_capability.csv`
- `P05/case_card.md`
- `P06/generate_equipment_log.py`
- `P06/data/equipment_log.csv`
- `P06/__pycache__/generate_equipment_log.cpython-312.pyc`

## 本轮旧项目文档删除
以下6份旧项目定义文档已从projects目录删除，不再作为历史文档保留：
- `P02_packaging_doe_spc_pfmea.md`
- `P03_secom_yield_screening.md`
- `P04_wafer_map_defect_analysis.md`
- `P05_failure_analysis_case.md`
- `P06_equipment_fdc_yield.md`
- `P07_thermal_structural_simulation.md`

## 保留/保护项
- P02–P07新版README、status、resume_bullets、项目定义、source清单和新数据字典保留。
- P02/node_modules 是指向共享运行时的Junction，清理时没有进入或删除；目标未更改。
- P01、本科原始实验数据目录及其他项目目录不在清理范围内。

## 验收
已逐项确认清单中的39个旧载荷文件及上述6份旧项目定义文档均已删除；六个新版data_sources.md与文献审计文件存在，P02共享Junction仍有效且目标未更改。
