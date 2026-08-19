from __future__ import annotations

import json
import math
from pathlib import Path

from ix_stellaratorforge.sfr2 import (
    geometry_from_sector_lengths,
    ideal_radial_compression_state,
    run_sfr2_screen,
    solve_base_beta_for_target_fusion_power,
    validate_sfr2_config,
)

ROOT = Path(__file__).resolve().parents[2]


def _config() -> dict:
    return json.loads((ROOT / "configs/reactor/sfr2_rev_a.json").read_text(encoding="utf-8"))


def test_sfr2_config_is_spec_only_and_high_authority_gates_are_unrun() -> None:
    raw = _config()
    assert validate_sfr2_config(raw) == ()
    assert raw["promotion_status"]["SFR2_G0_SPEC"] == "PASS_SPEC_ONLY"
    for gate, status in raw["promotion_status"].items():
        if gate != "SFR2_G0_SPEC":
            assert status == "NOT_RUN"


def test_23_26_23_26_geometry_is_one_closed_98_ft_path() -> None:
    g = geometry_from_sector_lengths((23, 26, 23, 26), screening_aspect_ratio=4.5)
    assert math.isclose(sum(g.sector_lengths_ft), 98.0, rel_tol=0, abs_tol=1e-12)
    assert math.isclose(g.total_axis_path_m, 98.0 * 0.3048, rel_tol=0, abs_tol=1e-12)
    assert 4.753 < g.equivalent_major_radius_m < 4.755
    assert 1.055 < g.screening_minor_radius_m < 1.058
    assert 104.6 < g.circular_torus_volume_m3 < 104.9


def test_ideal_10pct_radial_squeeze_obeys_declared_adiabatic_scalings() -> None:
    g = geometry_from_sector_lengths((23, 26, 23, 26), screening_aspect_ratio=4.5)
    base = ideal_radial_compression_state(
        geometry=g,
        base_temperature_keV=15.0,
        base_beta=0.03,
        axis_field_T=10.0,
        radial_squeeze_fraction=0.0,
    )
    squeezed = ideal_radial_compression_state(
        geometry=g,
        base_temperature_keV=15.0,
        base_beta=0.03,
        axis_field_T=10.0,
        radial_squeeze_fraction=0.10,
    )
    C = 1.0 / 0.9
    assert math.isclose(squeezed.ion_density_m3 / base.ion_density_m3, C**2, rel_tol=1e-12)
    assert math.isclose(squeezed.ion_temperature_keV / base.ion_temperature_keV, C ** (4.0 / 3.0), rel_tol=1e-12)
    assert math.isclose(squeezed.volume_m3 / base.volume_m3, 1.0 / C**2, rel_tol=1e-12)
    # No magnetic-flux compression is credited; beta rises at the unchanged axis field.
    assert math.isclose(squeezed.beta_at_fixed_B / base.beta_at_fixed_B, C ** (10.0 / 3.0), rel_tol=1e-12)


def test_target_power_beta_solver_reproduces_1GW_without_fabricated_target_copy() -> None:
    g = geometry_from_sector_lengths((23, 26, 23, 26), screening_aspect_ratio=4.5)
    beta = solve_base_beta_for_target_fusion_power(
        geometry=g,
        base_temperature_keV=15.0,
        axis_field_T=15.0,
        radial_squeeze_fraction=0.0,
        target_fusion_power_MW=1000.0,
    )
    state = ideal_radial_compression_state(
        geometry=g,
        base_temperature_keV=15.0,
        base_beta=beta,
        axis_field_T=15.0,
        radial_squeeze_fraction=0.0,
    )
    assert math.isclose(state.fusion_power_MW_uniform, 1000.0, rel_tol=1e-12)
    assert 0.0118 < beta < 0.0121


def test_primary_screen_does_not_claim_ignition_and_compression_is_negative_in_iss04_proxy() -> None:
    result = run_sfr2_screen(_config())
    primary = result["primary_screen"]
    assert primary["verdict"] == "NO_PRIMARY_CASE_CROSSES_OPTIMISTIC_IGNITION_PROXY"
    best = primary["best_case"]
    assert best["axis_field_T"] == 15.0
    assert best["iota_2over3"] == 0.9
    assert best["radial_squeeze_fraction"] == 0.0
    assert 0.960 < best["ignition"]["tau_ratio_to_optimistic_ignition"] < 0.962
    assert 1.039 < best["ignition"]["required_H_if_retention_is_one"] < 1.042

    comp = result["compression_sensitivity_at_max_B_max_iota"]
    ratios = [x["ignition"]["tau_ratio_to_optimistic_ignition"] for x in comp]
    assert ratios[0] > ratios[1] > ratios[2]
    assert [x["radial_squeeze_fraction"] for x in comp] == [0.0, 0.05, 0.1]


def test_rifling_sensitivity_is_monotonic_only_inside_the_empirical_proxy() -> None:
    result = run_sfr2_screen(_config())
    cases = result["rifling_sensitivity_at_max_B_no_compression"]
    iotas = [x["iota_2over3"] for x in cases]
    ratios = [x["ignition"]["tau_ratio_to_optimistic_ignition"] for x in cases]
    assert iotas == [0.6, 0.7, 0.8, 0.9]
    assert ratios == sorted(ratios)
    assert result["model_rules"]["staggering_confinement_credit"] == 0.0
    assert result["model_rules"]["dynamic_phase_heating_credit"] == 0.0
    assert result["model_rules"]["magnetic_flux_compression_credit"] == 0.0


def test_persisted_sfr2_result_matches_recomputation() -> None:
    expected = json.loads((ROOT / "results/sfr2/sfr2_rev_a_screen_v050.json").read_text(encoding="utf-8"))
    actual = run_sfr2_screen(_config())
    assert actual == expected
