"""Analytical silicon PN-junction and long-channel nMOS teaching models."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


def load_parameters(path: Path | None = None) -> dict[str, Any]:
    config_path = path or Path(__file__).resolve().parents[1] / "parameters_v1.json"
    with config_path.open(encoding="utf-8") as stream:
        return json.load(stream)


def cm3_to_m3(concentration_cm3: float) -> float:
    if concentration_cm3 <= 0:
        raise ValueError("Concentration must be positive.")
    return concentration_cm3 * 1e6


def cm2_vs_to_m2_vs(mobility_cm2_vs: float) -> float:
    if mobility_cm2_vs <= 0:
        raise ValueError("Mobility must be positive.")
    return mobility_cm2_vs * 1e-4


def thermal_voltage(temperature_K: float, boltzmann_J_per_K: float, charge_C: float) -> float:
    if temperature_K <= 0:
        raise ValueError("Temperature must be above 0 K.")
    return boltzmann_J_per_K * temperature_K / charge_C


def silicon_permittivity(relative_permittivity: float, vacuum_permittivity_F_per_m: float) -> float:
    if relative_permittivity <= 0 or vacuum_permittivity_F_per_m <= 0:
        raise ValueError("Permittivity values must be positive.")
    return relative_permittivity * vacuum_permittivity_F_per_m


def built_in_potential(
    temperature_K: float,
    acceptor_m3: float,
    donor_m3: float,
    intrinsic_m3: float,
    boltzmann_J_per_K: float,
    charge_C: float,
) -> float:
    if min(acceptor_m3, donor_m3, intrinsic_m3) <= 0:
        raise ValueError("Carrier and dopant concentrations must be positive.")
    v_thermal = thermal_voltage(temperature_K, boltzmann_J_per_K, charge_C)
    return v_thermal * math.log((acceptor_m3 * donor_m3) / (intrinsic_m3**2))


def depletion_widths(
    applied_voltage_V: float,
    built_in_voltage_V: float,
    acceptor_m3: float,
    donor_m3: float,
    silicon_permittivity_F_per_m: float,
    charge_C: float,
) -> tuple[float, float, float]:
    """Return total, p-side, and n-side widths under the abrupt-junction approximation."""
    barrier_V = built_in_voltage_V - applied_voltage_V
    if barrier_V < 0:
        raise ValueError("Applied forward bias exceeds built-in voltage.")
    if min(acceptor_m3, donor_m3, silicon_permittivity_F_per_m, charge_C) <= 0:
        raise ValueError("Concentrations and constants must be positive.")
    total = math.sqrt(
        (2.0 * silicon_permittivity_F_per_m / charge_C)
        * (1.0 / acceptor_m3 + 1.0 / donor_m3)
        * barrier_V
    )
    p_side = donor_m3 / (acceptor_m3 + donor_m3) * total
    n_side = acceptor_m3 / (acceptor_m3 + donor_m3) * total
    return total, p_side, n_side


def ideal_diode_current(
    diode_voltage_V: float,
    saturation_current_A: float,
    ideality_factor: float,
    v_thermal_V: float,
) -> float:
    if saturation_current_A <= 0 or ideality_factor <= 0 or v_thermal_V <= 0:
        raise ValueError("Diode parameters must be positive.")
    exponent = diode_voltage_V / (ideality_factor * v_thermal_V)
    if exponent > 700:
        raise ValueError("Voltage is outside the numerically supported ideal-diode range.")
    return saturation_current_A * math.expm1(exponent)


def oxide_capacitance_per_area(
    relative_permittivity: float,
    vacuum_permittivity_F_per_m: float,
    oxide_thickness_m: float,
) -> float:
    if oxide_thickness_m <= 0:
        raise ValueError("Oxide thickness must be positive.")
    return silicon_permittivity(relative_permittivity, vacuum_permittivity_F_per_m) / oxide_thickness_m


def mos_threshold_voltage(
    temperature_K: float,
    substrate_acceptor_m3: float,
    intrinsic_m3: float,
    flat_band_voltage_V: float,
    silicon_permittivity_F_per_m: float,
    oxide_capacitance_F_per_m2: float,
    boltzmann_J_per_K: float,
    charge_C: float,
) -> tuple[float, float]:
    if min(substrate_acceptor_m3, intrinsic_m3, silicon_permittivity_F_per_m,
           oxide_capacitance_F_per_m2, charge_C) <= 0:
        raise ValueError("MOS concentrations and material parameters must be positive.")
    if substrate_acceptor_m3 <= intrinsic_m3:
        raise ValueError("This p-substrate teaching model requires NA > ni.")
    v_thermal = thermal_voltage(temperature_K, boltzmann_J_per_K, charge_C)
    fermi_potential = v_thermal * math.log(substrate_acceptor_m3 / intrinsic_m3)
    depletion_charge_term = math.sqrt(
        4.0 * charge_C * silicon_permittivity_F_per_m
        * substrate_acceptor_m3 * fermi_potential
    ) / oxide_capacitance_F_per_m2
    threshold = flat_band_voltage_V + 2.0 * fermi_potential + depletion_charge_term
    return threshold, fermi_potential


def long_channel_nmos_current(
    gate_source_voltage_V: float,
    drain_source_voltage_V: float,
    threshold_voltage_V: float,
    electron_mobility_m2_vs: float,
    oxide_capacitance_F_per_m2: float,
    channel_width_m: float,
    channel_length_m: float,
) -> tuple[float, str]:
    """Return drain current and operating region for nonnegative drain bias."""
    if drain_source_voltage_V < 0:
        raise ValueError("This first-version nMOS model supports VDS >= 0 only.")
    if min(electron_mobility_m2_vs, oxide_capacitance_F_per_m2,
           channel_width_m, channel_length_m) <= 0:
        raise ValueError("MOS geometry and electrical parameters must be positive.")
    overdrive_V = gate_source_voltage_V - threshold_voltage_V
    if overdrive_V <= 0:
        return 0.0, "cutoff"
    beta_A_per_V2 = (
        electron_mobility_m2_vs * oxide_capacitance_F_per_m2
        * channel_width_m / channel_length_m
    )
    if drain_source_voltage_V <= overdrive_V:
        current = beta_A_per_V2 * (
            overdrive_V * drain_source_voltage_V - 0.5 * drain_source_voltage_V**2
        )
        return current, "linear"
    current = 0.5 * beta_A_per_V2 * overdrive_V**2
    return current, "saturation"


def evenly_spaced_values(start: float, stop: float, points: int) -> list[float]:
    if points < 2:
        raise ValueError("A sweep requires at least two points.")
    return [start + (stop - start) * index / (points - 1) for index in range(points)]

