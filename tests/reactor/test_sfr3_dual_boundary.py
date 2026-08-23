from __future__ import annotations

import json
from pathlib import Path

from ix_stellaratorforge.sfr3_dual_boundary import (
    PASS_VERDICT,
    run_dual_boundary_screen,
    validate_dual_boundary_config,
)

ROOT = Path(__file__).resolve().parents[2]


def _configs() -> tuple[dict, dict]:
    raw = json.loads(
        (ROOT / "configs/reactor/sfr3_dual_boundary_ahis_a.json").read_text(
            encoding="utf-8"
        )
    )
    sfr3 = json.loads(
        (ROOT / "configs/reactor/sfr3_field_integrity_shell_a.json").read_text(
            encoding="utf-8"
        )
    )
    return raw, sfr3


def test_dual_boundary_preserves_magnetic_not_mechanical_confinement() -> None:
    raw, _ = _configs()
    assert validate_dual_boundary_config(raw) == ()
    assert raw["architecture"]["vacuum_vessel_is_double_walled"] is True
    assert raw["architecture"]["mechanically_pushes_plasma_inward"] is False
    assert all(
        value == 0.0
        for key, value in raw["claim_boundary"].items()
        if key.endswith("_credit")
    )


def test_monitoring_geometry_has_two_lanes_and_192_paired_locations() -> None:
    raw, sfr3 = _configs()
    result = run_dual_boundary_screen(raw, sfr3)
    inventory = result["monitoring_inventory"]
    assert inventory["paired_inner_outer_monitoring_locations"] == 192
    assert inventory["total_declared_sensing_elements"] == 1736


def test_selected_dcll_stack_passes_declared_1d_thermal_screens() -> None:
    raw, sfr3 = _configs()
    result = run_dual_boundary_screen(raw, sfr3)
    selected = next(
        stack
        for stack in result["wall_stack_results"]
        if stack["id"] == result["selected_stack_id"]
    )
    assert selected["id"] == "DB-A_DCLL_MONITORED_RAFT"
    assert selected["nominal"]["all_layer_temperature_screens_pass"] is True
    assert selected["upset_steady_upper_bound"]["all_layer_temperature_screens_pass"] is True
    assert selected["upset_steady_upper_bound"]["raw_cte_mismatch_strain_screen_pass"] is True
    assert 420.0 < selected["nominal"]["plasma_facing_surface_temperature_C"] < 421.0
    assert 632.0 < selected["upset_steady_upper_bound"]["plasma_facing_surface_temperature_C"] < 634.0


def test_fault_logic_keeps_single_lane_detection_and_fails_closed() -> None:
    raw, sfr3 = _configs()
    result = run_dual_boundary_screen(raw, sfr3)
    by_id = {scenario["id"]: scenario for scenario in result["fault_scenarios"]}
    assert by_id["inner_hotspot_single_lane_failure"]["all_declared_signals_detected"] is True
    assert by_id["coolant_leak_single_lane_failure"]["all_declared_signals_detected"] is True
    assert by_id["sector_dual_bus_loss"]["control_state"] == "SAFE_HOLD_LOST_OBSERVABILITY"
    assert by_id["vacuum_breach"]["control_state"] == "ISOLATE_AFFECTED_SECTOR_AND_SAFE_HOLD"
    assert by_id["total_control_power_loss"]["control_state"] == "PASSIVE_HARD_SAFE_HOLD"


def test_silent_crack_is_retained_as_unobservable_negative_evidence() -> None:
    raw, sfr3 = _configs()
    result = run_dual_boundary_screen(raw, sfr3)
    silent = next(
        scenario for scenario in result["fault_scenarios"] if scenario["id"] == "silent_armor_crack"
    )
    assert silent["latent_fault_retained_without_false_detection"] is True
    assert silent["control_state"] == "NO_AUTOMATIC_DETECTION__PERIODIC_NDE_REQUIRED"


def test_sfr3_trim_link_remains_synthetic_and_zero_credit() -> None:
    raw, sfr3 = _configs()
    result = run_dual_boundary_screen(raw, sfr3)
    shift = next(
        scenario for scenario in result["fault_scenarios"] if scenario["id"] == "outer_support_shift"
    )
    assert shift["sfr3_field_integrity_link"]["synthetic_rms_reduction_fraction"] > 0.60
    assert shift["sfr3_field_integrity_link"]["physical_confinement_credit"] == 0.0
    assert shift["fusion_or_ignition_credit"] == 0.0


def test_dual_boundary_result_passes_only_at_low_authority() -> None:
    raw, sfr3 = _configs()
    result = run_dual_boundary_screen(raw, sfr3)
    assert result["top_level_verdict"] == PASS_VERDICT
    assert result["screen_pass"] is True
    assert result["promotion_status"]["SFR3D_G0_DUAL_BOUNDARY_SPEC"] == "PASS_SPEC_ONLY"
    assert all(
        status == "NOT_RUN"
        for gate, status in result["promotion_status"].items()
        if gate not in {
            "SFR3D_G0_DUAL_BOUNDARY_SPEC",
            "SFR3D_G1_REDUCED_THERMAL_AND_FAULT_SCREEN",
        }
    )


def test_persisted_dual_boundary_result_matches_recomputation() -> None:
    raw, sfr3 = _configs()
    expected = json.loads(
        (ROOT / "results/sfr3_dual_boundary/sfr3_dual_boundary_ahis_a_v080.json").read_text(
            encoding="utf-8"
        )
    )
    assert run_dual_boundary_screen(raw, sfr3) == expected
