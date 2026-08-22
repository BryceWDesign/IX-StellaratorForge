from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from ix_stellaratorforge.sfr4_integrated_campaign import (
    PASS_VERDICT,
    run_integrated_campaign,
    validate_integrated_config,
)

ROOT = Path(__file__).resolve().parents[2]


def _raw() -> dict:
    return json.loads(
        (ROOT / "configs/reactor/sfr4_integrated_physical_promotion_a.json").read_text(
            encoding="utf-8"
        )
    )


@lru_cache(maxsize=1)
def _result() -> dict:
    return run_integrated_campaign(_raw())


def test_config_declares_all_seven_workstreams_and_zero_credit():
    raw = _raw()
    assert validate_integrated_config(raw) == ()
    assert len(raw["workstreams"]) == 7
    assert all(value == 0.0 for value in raw["claim_boundary"].values())


def test_direct_biot_savart_scan_executes_and_rejects_current_family():
    coil = _result()["workstreams"]["1_physical_coil_field"]
    assert coil["candidate_count"] == 80
    assert coil["combined_pass_count"] == 0
    assert not coil["physical_coil_promoted"]
    assert coil["held_out_hybrid_reconstruction"]["validation_rms_Bn_over_B"] > 0.005


def test_equilibrium_and_codesign_fail_closed_when_production_solvers_absent():
    result = _result()
    equilibrium = result["workstreams"]["2_finite_beta_equilibrium"]
    codesign = result["workstreams"]["3_coil_plasma_codesign"]
    assert equilibrium["fail_closed"]
    assert not equilibrium["cross_code_equilibrium_completed"]
    assert not codesign["production_single_stage_codesign_completed"]


def test_alpha_scale_pass_cannot_promote_particle_confinement():
    particles = _result()["workstreams"]["4_particle_confinement"]
    assert particles["gyroradius_clearance_screen_pass"]
    assert not particles["field_line_topology_prerequisite_pass"]
    assert not particles["particle_confinement_promoted"]


def test_burn_requirement_includes_radiation_and_is_not_linked_to_failed_coil():
    burn = _result()["workstreams"]["5_self_consistent_burn"]
    assert burn["bremsstrahlung_MW_screen"] > 0.0
    assert burn["required_H_ISS04_with_bremsstrahlung_at_design_iota"] > 1.0
    assert not burn["physical_coil_linked_burn_promoted"]


def test_selected_heat_partition_and_both_component_stacks_pass_declared_steady_screen():
    heat = _result()["heat_exhaust_resolution"]
    assert heat["first_wall_peak_heat_flux_MW_m2"] < 0.5
    assert heat["divertor_peak_heat_flux_MW_m2"] < 10.0
    assert heat["divertor_thermal_screen"]["all_temperature_screens_pass"]
    assert heat["selected_first_wall_screen"]["nominal"]["all_layer_temperature_screens_pass"]
    assert heat["selected_first_wall_screen"]["upset_steady_upper_bound"]["all_layer_temperature_screens_pass"]
    assert heat["nominal_and_declared_steady_heat_envelope_pass"]


def test_heat_sensitivity_contains_pass_and_fail_regions():
    heat = _result()["heat_exhaust_resolution"]
    states = {point["heat_flux_limits_pass"] for point in heat["heat_partition_sensitivity"]}
    assert states == {False, True}
    assert heat["heat_partition_feasibility_window"]["selected_point_inside_flux_window"]


def test_transient_heat_and_magnet_qualification_remain_open():
    result = _result()
    assert not result["heat_exhaust_resolution"]["transient_disruption_heat_resolved"]
    magnet = result["workstreams"]["6_magnet_engineering"]
    assert not magnet["peak_field_on_conductor_calculated"]
    assert not magnet["structural_FEA_completed"]
    assert not magnet["magnet_promoted"]


def test_reactor_ledger_is_conditional_and_tbr_remains_unrun():
    systems = _result()["workstreams"]["7_reactor_systems"]
    assert systems["conditional_net_electric_MW"] > 0.0
    assert systems["breeding_coverage_constraint"]["required_local_tbr_if_uncovered_regions_breed_zero"] > 1.15
    assert not systems["full_3D_TBR_calculated"]
    assert not systems["net_electric_prediction_promoted"]


def test_top_level_pass_is_reduced_campaign_only_with_zero_fusion_credit():
    result = _result()
    assert result["top_level_verdict"] == PASS_VERDICT
    assert result["reduced_campaign_complete"]
    promotion = result["promotion_summary"]
    assert promotion["nominal_and_declared_steady_heat_envelope_screen_pass"]
    assert promotion["earned_fusion_progress_credit_fraction"] == 0.0
    assert not any(
        promotion[key]
        for key in (
            "production_equilibrium_pass",
            "physical_confinement_pass",
            "sustained_burn_pass",
            "magnet_qualification_pass",
            "full_3D_TBR_pass",
            "hardware_pass",
        )
    )


def test_persisted_result_matches_recomputation():
    expected = _result()
    path = ROOT / "results/sfr4_integrated/sfr4_integrated_physical_promotion_a_v090.json"
    persisted = json.loads(path.read_text(encoding="utf-8"))
    assert persisted == expected
