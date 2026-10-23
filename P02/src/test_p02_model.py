"""Focused regression tests for the frozen first-version P02 models."""

from __future__ import annotations

import math
import unittest
from pathlib import Path

try:
    from . import p02_model as model
except ImportError:  # Allow direct execution as a script.
    import p02_model as model


class P02ModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = model.load_parameters(Path(__file__).resolve().parents[1] / "parameters_v1.json")
        cls.constants = cls.config["constants"]
        cls.q = cls.constants["elementary_charge_C"]
        cls.kb = cls.constants["boltzmann_constant_J_per_K"]
        cls.eps0 = cls.constants["vacuum_permittivity_F_per_m"]

    def test_si_conversions(self) -> None:
        self.assertEqual(model.cm3_to_m3(1e16), 1e22)
        self.assertAlmostEqual(model.cm2_vs_to_m2_vs(1448), 0.1448)
        with self.assertRaises(ValueError):
            model.cm3_to_m3(0)

    def test_thermal_voltage_at_300_kelvin(self) -> None:
        self.assertAlmostEqual(model.thermal_voltage(300, self.kb, self.q), 0.0258519997864, places=11)

    def test_pn_builtin_potential_and_charge_balance(self) -> None:
        pn = self.config["pn_diode"]
        na = model.cm3_to_m3(pn["acceptor_concentration_cm3"])
        nd = model.cm3_to_m3(pn["donor_concentration_cm3"])
        ni = model.cm3_to_m3(pn["intrinsic_concentration_cm3"])
        eps_si = model.silicon_permittivity(pn["silicon_relative_permittivity"], self.eps0)
        v_bi = model.built_in_potential(pn["temperature_K"], na, nd, ni, self.kb, self.q)
        total, p_side, n_side = model.depletion_widths(0, v_bi, na, nd, eps_si, self.q)
        self.assertGreater(v_bi, 0.6)
        self.assertLess(v_bi, 0.7)
        self.assertAlmostEqual(na * p_side, nd * n_side, delta=na * p_side * 1e-12)
        self.assertAlmostEqual(total, p_side + n_side, places=15)
        self.assertGreater(n_side, p_side)

    def test_depletion_width_responds_to_bias_direction(self) -> None:
        pn = self.config["pn_diode"]
        na = model.cm3_to_m3(pn["acceptor_concentration_cm3"])
        nd = model.cm3_to_m3(pn["donor_concentration_cm3"])
        ni = model.cm3_to_m3(pn["intrinsic_concentration_cm3"])
        eps_si = model.silicon_permittivity(pn["silicon_relative_permittivity"], self.eps0)
        v_bi = model.built_in_potential(pn["temperature_K"], na, nd, ni, self.kb, self.q)
        reverse = model.depletion_widths(-0.2, v_bi, na, nd, eps_si, self.q)[0]
        zero = model.depletion_widths(0, v_bi, na, nd, eps_si, self.q)[0]
        forward = model.depletion_widths(0.3, v_bi, na, nd, eps_si, self.q)[0]
        self.assertGreater(reverse, zero)
        self.assertGreater(zero, forward)
        with self.assertRaises(ValueError):
            model.depletion_widths(v_bi + 0.01, v_bi, na, nd, eps_si, self.q)

    def test_diode_zero_reverse_and_forward_current(self) -> None:
        vt = model.thermal_voltage(300, self.kb, self.q)
        isat = 1e-15
        self.assertEqual(model.ideal_diode_current(0, isat, 1, vt), 0)
        self.assertLess(model.ideal_diode_current(-0.2, isat, 1, vt), 0)
        self.assertAlmostEqual(model.ideal_diode_current(-0.2, isat, 1, vt), -isat, delta=isat * 1e-3)
        self.assertGreater(model.ideal_diode_current(0.7, isat, 1, vt), 1e-4)
        with self.assertRaises(ValueError):
            model.ideal_diode_current(100, isat, 1, vt)

    def test_mos_threshold_and_regions(self) -> None:
        mos = self.config["nmos"]
        na = model.cm3_to_m3(mos["substrate_acceptor_concentration_cm3"])
        ni = model.cm3_to_m3(mos["intrinsic_concentration_cm3"])
        eps_si = model.silicon_permittivity(mos["silicon_relative_permittivity"], self.eps0)
        cox = model.oxide_capacitance_per_area(
            mos["oxide_relative_permittivity"], self.eps0, mos["oxide_thickness_m"]
        )
        vth, _ = model.mos_threshold_voltage(
            mos["temperature_K"], na, ni, mos["flat_band_voltage_V"],
            eps_si, cox, self.kb, self.q
        )
        mu = model.cm2_vs_to_m2_vs(mos["electron_mobility_cm2_per_Vs"])
        common = (vth, mu, cox, mos["channel_width_m"], mos["channel_length_m"])
        off_current, off_region = model.long_channel_nmos_current(0.5, 0.1, *common)
        linear_current, linear_region = model.long_channel_nmos_current(vth + 1, 0.2, *common)
        sat_current, sat_region = model.long_channel_nmos_current(vth + 1, 1, *common)
        self.assertGreater(vth, 0.5)
        self.assertEqual((off_current, off_region), (0.0, "cutoff"))
        self.assertGreater(linear_current, 0)
        self.assertEqual(linear_region, "linear")
        self.assertGreater(sat_current, linear_current)
        self.assertEqual(sat_region, "saturation")
        with self.assertRaises(ValueError):
            model.long_channel_nmos_current(2, -0.1, *common)

    def test_mos_piecewise_current_is_continuous_at_saturation_boundary(self) -> None:
        mos = self.config["nmos"]
        na = model.cm3_to_m3(mos["substrate_acceptor_concentration_cm3"])
        ni = model.cm3_to_m3(mos["intrinsic_concentration_cm3"])
        eps_si = model.silicon_permittivity(mos["silicon_relative_permittivity"], self.eps0)
        cox = model.oxide_capacitance_per_area(
            mos["oxide_relative_permittivity"], self.eps0, mos["oxide_thickness_m"]
        )
        vth, _ = model.mos_threshold_voltage(
            mos["temperature_K"], na, ni, mos["flat_band_voltage_V"],
            eps_si, cox, self.kb, self.q
        )
        mu = model.cm2_vs_to_m2_vs(mos["electron_mobility_cm2_per_Vs"])
        vgs = vth + 0.8
        args = (vgs,)
        current_at_boundary, region_at_boundary = model.long_channel_nmos_current(
            *args, 0.8, vth, mu, cox, mos["channel_width_m"], mos["channel_length_m"]
        )
        current_after_boundary, region_after_boundary = model.long_channel_nmos_current(
            *args, 0.80000001, vth, mu, cox, mos["channel_width_m"], mos["channel_length_m"]
        )
        self.assertEqual(region_at_boundary, "linear")
        self.assertEqual(region_after_boundary, "saturation")
        self.assertTrue(math.isclose(current_at_boundary, current_after_boundary, rel_tol=1e-7))


if __name__ == "__main__":
    unittest.main()
