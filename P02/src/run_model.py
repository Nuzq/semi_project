"""Generate deterministic CSVs and figures from the frozen P02 parameter set."""

from __future__ import annotations

import argparse
import csv
import json
import math
import platform
import sys
from datetime import date
from pathlib import Path
from typing import Any, Iterable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    from . import p02_model as model
except ImportError:  # Allow direct execution as `python src/run_model.py`.
    import p02_model as model


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def add_provenance(row: dict[str, Any], parameter_set_id: str, model_id: str) -> dict[str, Any]:
    return {
        **row,
        "model_id": model_id,
        "parameter_set_id": parameter_set_id,
        "output_class": "analytical_teaching_model_output_not_measurement",
    }


def run(config_path: Path, output_root: Path) -> dict[str, Any]:
    config = model.load_parameters(config_path)
    constants = config["constants"]
    pn = config["pn_diode"]
    mos = config["nmos"]
    q = constants["elementary_charge_C"]
    kb = constants["boltzmann_constant_J_per_K"]
    eps0 = constants["vacuum_permittivity_F_per_m"]
    parameter_set_id = config["parameter_set_id"]

    pn_temp = pn["temperature_K"]
    pn_vt = model.thermal_voltage(pn_temp, kb, q)
    eps_si_pn = model.silicon_permittivity(pn["silicon_relative_permittivity"], eps0)
    pn_na = model.cm3_to_m3(pn["acceptor_concentration_cm3"])
    pn_nd = model.cm3_to_m3(pn["donor_concentration_cm3"])
    pn_ni = model.cm3_to_m3(pn["intrinsic_concentration_cm3"])
    v_bi = model.built_in_potential(pn_temp, pn_na, pn_nd, pn_ni, kb, q)

    diode_range = pn["diode_voltage_sweep_V"]
    diode_voltages = model.evenly_spaced_values(
        diode_range["start"], diode_range["stop"], diode_range["points"]
    )
    diode_rows = []
    for voltage in diode_voltages:
        current = model.ideal_diode_current(
            voltage, pn["reverse_saturation_current_A"], pn["ideality_factor"], pn_vt
        )
        diode_rows.append(add_provenance({
            "diode_voltage_V": f"{voltage:.12g}",
            "diode_current_A": f"{current:.12g}",
            "diode_current_mA": f"{current * 1e3:.12g}",
        }, parameter_set_id, "pn_diode_ideal_iv"))
    write_csv(output_root / "data" / "pn_diode_iv_v1.csv",
              ["diode_voltage_V", "diode_current_A", "diode_current_mA", "model_id", "parameter_set_id", "output_class"],
              diode_rows)

    depletion_range = pn["applied_junction_voltage_sweep_V"]
    applied_voltages = model.evenly_spaced_values(
        depletion_range["start"], depletion_range["stop"], depletion_range["points"]
    )
    depletion_rows = []
    for voltage in applied_voltages:
        total, p_side, n_side = model.depletion_widths(
            voltage, v_bi, pn_na, pn_nd, eps_si_pn, q
        )
        depletion_rows.append(add_provenance({
            "applied_junction_voltage_V": f"{voltage:.12g}",
            "built_in_voltage_V": f"{v_bi:.12g}",
            "total_depletion_width_m": f"{total:.12g}",
            "p_side_depletion_width_m": f"{p_side:.12g}",
            "n_side_depletion_width_m": f"{n_side:.12g}",
            "total_depletion_width_um": f"{total * 1e6:.12g}",
        }, parameter_set_id, "pn_junction_depletion_approximation"))
    write_csv(output_root / "data" / "pn_depletion_v1.csv",
              ["applied_junction_voltage_V", "built_in_voltage_V", "total_depletion_width_m",
               "p_side_depletion_width_m", "n_side_depletion_width_m", "total_depletion_width_um",
               "model_id", "parameter_set_id", "output_class"], depletion_rows)

    mos_temp = mos["temperature_K"]
    eps_si_mos = model.silicon_permittivity(mos["silicon_relative_permittivity"], eps0)
    eps_ox = model.silicon_permittivity(mos["oxide_relative_permittivity"], eps0)
    c_ox = model.oxide_capacitance_per_area(
        mos["oxide_relative_permittivity"], eps0, mos["oxide_thickness_m"]
    )
    mos_na = model.cm3_to_m3(mos["substrate_acceptor_concentration_cm3"])
    mos_ni = model.cm3_to_m3(mos["intrinsic_concentration_cm3"])
    v_th, phi_f = model.mos_threshold_voltage(
        mos_temp, mos_na, mos_ni, mos["flat_band_voltage_V"], eps_si_mos,
        c_ox, kb, q
    )
    mu_n = model.cm2_vs_to_m2_vs(mos["electron_mobility_cm2_per_Vs"])

    vds_range = mos["drain_voltage_sweep_V"]
    drain_voltages = model.evenly_spaced_values(
        vds_range["start"], vds_range["stop"], vds_range["points"]
    )
    output_rows = []
    for gate_voltage in mos["output_curve_gate_voltages_V"]:
        for drain_voltage in drain_voltages:
            current, region = model.long_channel_nmos_current(
                gate_voltage, drain_voltage, v_th, mu_n, c_ox,
                mos["channel_width_m"], mos["channel_length_m"]
            )
            output_rows.append(add_provenance({
                "gate_source_voltage_V": f"{gate_voltage:.12g}",
                "drain_source_voltage_V": f"{drain_voltage:.12g}",
                "drain_current_A": f"{current:.12g}",
                "drain_current_mA": f"{current * 1e3:.12g}",
                "operating_region": region,
            }, parameter_set_id, "long_channel_nmos_square_law"))
    write_csv(output_root / "data" / "nmos_output_iv_v1.csv",
              ["gate_source_voltage_V", "drain_source_voltage_V", "drain_current_A",
               "drain_current_mA", "operating_region", "model_id", "parameter_set_id", "output_class"],
              output_rows)

    vgs_range = mos["gate_voltage_sweep_V"]
    gate_voltages = model.evenly_spaced_values(
        vgs_range["start"], vgs_range["stop"], vgs_range["points"]
    )
    fixed_vds = mos["transfer_curve_drain_voltage_V"]
    transfer_rows = []
    for gate_voltage in gate_voltages:
        current, region = model.long_channel_nmos_current(
            gate_voltage, fixed_vds, v_th, mu_n, c_ox,
            mos["channel_width_m"], mos["channel_length_m"]
        )
        transfer_rows.append(add_provenance({
            "gate_source_voltage_V": f"{gate_voltage:.12g}",
            "drain_source_voltage_V": f"{fixed_vds:.12g}",
            "drain_current_A": f"{current:.12g}",
            "drain_current_mA": f"{current * 1e3:.12g}",
            "operating_region": region,
        }, parameter_set_id, "long_channel_nmos_square_law"))
    write_csv(output_root / "data" / "nmos_transfer_iv_v1.csv",
              ["gate_source_voltage_V", "drain_source_voltage_V", "drain_current_A",
               "drain_current_mA", "operating_region", "model_id", "parameter_set_id", "output_class"],
              transfer_rows)

    zero_depletion = model.depletion_widths(0.0, v_bi, pn_na, pn_nd, eps_si_pn, q)
    base_vgs = 2.0
    base_vov = base_vgs - v_th
    base_ids, base_region = model.long_channel_nmos_current(
        base_vgs, 1.0, v_th, mu_n, c_ox,
        mos["channel_width_m"], mos["channel_length_m"]
    )
    checks = {
        "thermal_voltage_300K_is_about_25_85mV": abs(pn_vt - 0.025852) < 2e-6,
        "built_in_potential_is_positive": v_bi > 0,
        "depletion_charge_balance": abs(pn_na * zero_depletion[1] - pn_nd * zero_depletion[2])
        / max(pn_na * zero_depletion[1], pn_nd * zero_depletion[2]) < 1e-12,
        "depletion_sweep_stays_below_built_in_potential": depletion_range["stop"] < v_bi,
        "mos_threshold_is_positive": v_th > 0,
        "mos_base_point_is_above_threshold": base_vov > 0 and base_ids > 0,
        "all_model_outputs_are_finite": all(
            math.isfinite(float(row["diode_current_A"])) for row in diode_rows
        ) and all(math.isfinite(float(row["drain_current_A"])) for row in output_rows + transfer_rows),
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise RuntimeError(f"Model preflight checks failed: {failed}")

    summary = {
        "parameter_set_id": parameter_set_id,
        "model_scope": config["model_scope"],
        "run_date": date.today().isoformat(),
        "python_version": platform.python_version(),
        "derived_values": {
            "pn_thermal_voltage_V": pn_vt,
            "pn_built_in_potential_V": v_bi,
            "pn_zero_bias_depletion_total_m": zero_depletion[0],
            "pn_zero_bias_depletion_p_side_m": zero_depletion[1],
            "pn_zero_bias_depletion_n_side_m": zero_depletion[2],
            "mos_oxide_capacitance_per_area_F_per_m2": c_ox,
            "mos_fermi_potential_V": phi_f,
            "mos_threshold_voltage_V": v_th,
            "mos_overdrive_at_VGS_2V_V": base_vov,
            "mos_drain_current_at_VGS_2V_VDS_1V_A": base_ids,
            "mos_operating_region_at_VGS_2V_VDS_1V": base_region,
            "silicon_mobility_m2_per_Vs": mu_n,
            "oxide_permittivity_F_per_m": eps_ox,
        },
        "checks": checks,
        "generated_files": [
            "data/pn_diode_iv_v1.csv",
            "data/pn_depletion_v1.csv",
            "data/nmos_output_iv_v1.csv",
            "data/nmos_transfer_iv_v1.csv",
            "figures/pn_diode_iv_v1.png",
            "figures/pn_depletion_v1.png",
            "figures/nmos_output_iv_v1.png",
            "figures/nmos_transfer_iv_v1.png",
        ],
        "output_class": "analytical_teaching_model_output_not_measurement",
    }

    figure_dir = output_root / "figures"
    figure_dir.mkdir(parents=True, exist_ok=True)
    configure_plot_style()
    create_figures(
        figure_dir, diode_voltages, [float(row["diode_current_A"]) for row in diode_rows],
        applied_voltages,
        [[float(row[key]) for row in depletion_rows]
         for key in ("total_depletion_width_um", "p_side_depletion_width_m", "n_side_depletion_width_m")],
        output_rows, transfer_rows, parameter_set_id, v_th
    )
    output_root.mkdir(parents=True, exist_ok=True)
    (output_root / "model_summary_v1.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_results_note(output_root, summary)
    return summary


def configure_plot_style() -> None:
    plt.rcParams.update({
        "font.family": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
        "axes.unicode_minus": False,
        "figure.facecolor": "white",
        "axes.facecolor": "#fbfcfd",
        "axes.edgecolor": "#52636b",
        "axes.labelcolor": "#24333a",
        "xtick.color": "#43545b",
        "ytick.color": "#43545b",
        "text.color": "#1d2b31",
        "grid.color": "#d8e0e3",
        "grid.alpha": 0.8,
    })


def finish_figure(fig: Any, path: Path) -> None:
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def create_figures(
    figure_dir: Path,
    diode_voltages: list[float],
    diode_currents: list[float],
    applied_voltages: list[float],
    depletion_series: list[list[float]],
    output_rows: list[dict[str, Any]],
    transfer_rows: list[dict[str, Any]],
    parameter_set_id: str,
    threshold_voltage_V: float,
) -> None:
    fig, ax = plt.subplots(figsize=(8.2, 5.0))
    ax.plot(diode_voltages, diode_currents, color="#006f70", linewidth=2.2)
    ax.axhline(0, color="#62757c", linewidth=0.8)
    ax.axvline(0, color="#62757c", linewidth=0.8)
    ax.set_yscale("symlog", linthresh=1e-15)
    ax.set_xlabel("Diode voltage (V)")
    ax.set_ylabel("Diode current (A, symlog)")
    ax.set_title(f"PN diode ideal I–V | {parameter_set_id}\nAnalytical teaching model; not measurement or product prediction")
    ax.grid(True, which="both")
    finish_figure(fig, figure_dir / "pn_diode_iv_v1.png")

    total, p_side_m, n_side_m = depletion_series
    fig, ax = plt.subplots(figsize=(8.2, 5.0))
    ax.plot(applied_voltages, total, color="#006f70", linewidth=2.2, label="Total depletion width")
    ax.plot(applied_voltages, [value * 1e6 for value in p_side_m], color="#d17852", linewidth=1.8, label="Into p side")
    ax.plot(applied_voltages, [value * 1e6 for value in n_side_m], color="#426b9a", linewidth=1.8, label="Into n side")
    ax.set_xlabel("Applied junction voltage Va (V; positive = forward bias)")
    ax.set_ylabel("Depletion width (μm)")
    ax.set_title(f"PN depletion approximation | {parameter_set_id}\nAnalytical teaching model; below breakdown")
    ax.legend(frameon=False)
    ax.grid(True)
    finish_figure(fig, figure_dir / "pn_depletion_v1.png")

    fig, ax = plt.subplots(figsize=(8.2, 5.0))
    gate_levels = sorted({float(row["gate_source_voltage_V"]) for row in output_rows})
    colors = ["#87969c", "#b1843b", "#a7504b", "#147b78", "#566fa3"]
    for gate_voltage, color in zip(gate_levels, colors):
        series = [row for row in output_rows if float(row["gate_source_voltage_V"]) == gate_voltage]
        ax.plot([float(row["drain_source_voltage_V"]) for row in series],
                [float(row["drain_current_mA"]) for row in series],
                color=color, linewidth=2, label=f"VGS = {gate_voltage:g} V")
    ax.set_xlabel("Drain-source voltage VDS (V)")
    ax.set_ylabel("Drain current ID (mA)")
    ax.set_title(f"Long-channel nMOS output characteristics | {parameter_set_id}\nSquare-law analytical teaching model")
    ax.legend(frameon=False, ncol=2)
    ax.grid(True)
    finish_figure(fig, figure_dir / "nmos_output_iv_v1.png")

    fig, ax = plt.subplots(figsize=(8.2, 5.0))
    ax.plot([float(row["gate_source_voltage_V"]) for row in transfer_rows],
            [float(row["drain_current_mA"]) for row in transfer_rows],
            color="#a7504b", linewidth=2.2)
    ax.axvline(threshold_voltage_V, color="#426b9a", linestyle="--", linewidth=1.4,
               label=f"Vth = {threshold_voltage_V:.3f} V")
    ax.set_xlabel("Gate-source voltage VGS (V)")
    ax.set_ylabel("Drain current ID (mA)")
    ax.set_title(f"Long-channel nMOS transfer characteristic | {parameter_set_id}\nFixed VDS = 0.1 V; strong-inversion model")
    ax.legend(frameon=False)
    ax.grid(True)
    finish_figure(fig, figure_dir / "nmos_transfer_iv_v1.png")


def write_results_note(output_root: Path, summary: dict[str, Any]) -> None:
    values = summary["derived_values"]
    checks = summary["checks"]
    lines = [
        "# P02 最小可复现模型｜第一版运行记录",
        "",
        f"- 参数集：`{summary['parameter_set_id']}`",
        f"- 运行日期：{summary['run_date']}",
        f"- Python：`{summary['python_version']}`",
        "- 输入：`parameters_v1.json`；完整输入分类见 `model_parameters_v1.md`。",
        "- 输出性质：解析教学模型计算值，不是实验测量、COMSOL/TCAD 数值求解或产品预测。",
        "",
        "## 本次计算出的关键量",
        "",
        f"- 300 K 热电压：{values['pn_thermal_voltage_V'] * 1e3:.5f} mV。",
        f"- PN 结内建电势：{values['pn_built_in_potential_V']:.6f} V。",
        f"- 零偏总耗尽宽度：{values['pn_zero_bias_depletion_total_m'] * 1e6:.4f} μm；伸入 p 侧 {values['pn_zero_bias_depletion_p_side_m'] * 1e6:.4f} μm，伸入 n 侧 {values['pn_zero_bias_depletion_n_side_m'] * 1e6:.4f} μm。",
        f"- MOS 单位面积栅氧电容：{values['mos_oxide_capacitance_per_area_F_per_m2']:.6g} F/m²。",
        f"- p 型衬底费米势：{values['mos_fermi_potential_V']:.6f} V；由简化阈值公式计算的阈值电压：{values['mos_threshold_voltage_V']:.6f} V。",
        f"- `VGS=2 V, VDS=1 V` 时：过驱动电压 {values['mos_overdrive_at_VGS_2V_V']:.6f} V，漏极电流 {values['mos_drain_current_at_VGS_2V_VDS_1V_A'] * 1e3:.6f} mA，模型工作区 `{values['mos_operating_region_at_VGS_2V_VDS_1V']}`。",
        "",
        "## 自动预检查",
        "",
    ]
    lines.extend(f"- [{'x' if passed else ' '}] `{name}`" for name, passed in checks.items())
    lines.extend([
        "",
        "这些预检查是数值/边界自检，不是与实验或第三方器件仿真的验证。完整回归测试请运行 `python -m unittest src.test_p02_model -v`。",
        "",
        "## 输出文件",
        "",
        "- `data/pn_diode_iv_v1.csv`：理想二极管 I–V 扫描。",
        "- `data/pn_depletion_v1.csv`：PN 结耗尽区随结偏压变化。",
        "- `data/nmos_output_iv_v1.csv`：长沟道 nMOS 输出特性。",
        "- `data/nmos_transfer_iv_v1.csv`：长沟道 nMOS 转移特性。",
        "- `figures/*.png`：由上述冻结输入及解析模型生成的曲线图。",
        "- `model_summary_v1.json`：派生值、运行环境和预检查状态。",
        "",
        "## 未纳入第一版",
        "",
        "本版固定 300 K，不含完整温度依赖、反向击穿、亚阈值电流、沟道长度调制、短沟道、高场速度饱和、界面陷阱、自热或 SiC 参数。后续逐项扩展时需新增参数来源和验证，不应把本版称为产品级器件模型。",
        "",
    ])
    (output_root / "results_v1.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=PROJECT_ROOT / "parameters_v1.json")
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT)
    args = parser.parse_args()
    summary = run(args.config, args.output)
    print(f"Generated P02 model outputs for {summary['parameter_set_id']} in {args.output}")
    print(f"Checks passed: {sum(summary['checks'].values())}/{len(summary['checks'])}")


if __name__ == "__main__":
    main()
