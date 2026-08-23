from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from ix_stellaratorforge.sfr3_field_integrity import (
    PASS_VERDICT,
    build_response_matrix,
    run_sfr3_field_integrity_screen,
    validate_sfr3_config,
)

ROOT = Path(__file__).resolve().parents[2]


def _config() -> dict:
    return json.loads(
        (ROOT / "configs/reactor/sfr3_field_integrity_shell_a.json").read_text(
            encoding="utf-8"
        )
    )


def test_sfr3_spec_preserves_steady_field_rigid_vessel_and_zero_material_credit() -> None:
    raw = _config()
    assert validate_sfr3_config(raw) == ()
    assert raw["architecture"]["primary_field_is_steady"] is True
    assert raw["architecture"]["vacuum_vessel_is_flexible"] is False
    assert raw["architecture"]["passive_material_claimed_to_confine_plasma"] is False
    assert all(value == 0.0 for key, value in raw["claim_boundary"].items() if key.endswith("_credit"))


def test_synthetic_response_is_full_row_rank_but_not_physical_evidence() -> None:
    raw = _config()
    matrix = build_response_matrix(raw["harmonic_screen"])
    assert matrix.shape == (12, 24)
    assert np.linalg.matrix_rank(matrix) == 12
    result = run_sfr3_field_integrity_screen(raw)
    assert result["authority"].startswith("LOW__synthetic")
    assert "analytic heuristic" in result["model_definition"]["response_matrix_source"]


def test_nominal_and_single_failure_synthetic_controllability_pass() -> None:
    result = run_sfr3_field_integrity_screen(_config())
    by_id = {scenario["id"]: scenario for scenario in result["scenarios"]}
    assert result["top_level_verdict"] == PASS_VERDICT
    assert result["screen_pass"] is True
    assert by_id["nominal"]["total_rms_reduction_fraction"] >= 0.60
    assert by_id["single_actuator_unavailable"]["total_rms_reduction_fraction"] >= 0.55
    assert by_id["nominal"]["diagnostics"]["peak_command_utilization"] <= 1.0


def test_passive_loops_only_attenuate_transients_and_safe_hold_is_fail_closed() -> None:
    result = run_sfr3_field_integrity_screen(_config())
    by_id = {scenario["id"]: scenario for scenario in result["scenarios"]}
    passive = by_id["passive_transient_only"]
    assert passive["active_correction_allowed"] is False
    assert math.isclose(passive["passive_only_rms_reduction_fraction"], 0.55, abs_tol=1e-12)
    low_confidence = by_id["low_sensor_confidence"]
    assert low_confidence["control_state"] == "PASSIVE_ONLY_SAFE_HOLD"
    assert "sensor confidence below threshold" in low_confidence["resource_gate_reasons"]
    loop_quench = by_id["passive_loop_quench"]
    assert loop_quench["passive_loops_healthy"] is False
    assert loop_quench["passive_transient_attenuation_fraction_applied"] == 0.0
    active_quench = by_id["active_coil_quench"]
    assert active_quench["control_state"] == "PASSIVE_ONLY_SAFE_HOLD"
    assert "active-coil quench detected" in active_quench["resource_gate_reasons"]
    thermal = by_id["thermal_margin_exhausted"]
    assert thermal["control_state"] == "PASSIVE_ONLY_SAFE_HOLD"
    assert "trim thermal margin below threshold" in thermal["resource_gate_reasons"]


def test_high_authority_gates_remain_unrun_and_no_fusion_credit_is_created() -> None:
    result = run_sfr3_field_integrity_screen(_config())
    assert result["promotion_status"]["SFR3_G0_ARCHITECTURE_SPEC"] == "PASS_SPEC_ONLY"
    assert result["promotion_status"]["SFR3_G1_SYNTHETIC_CONTROLLABILITY"] == (
        "PASS_LOW_AUTHORITY_SYNTHETIC_ONLY"
    )
    assert all(
        status == "NOT_RUN"
        for gate, status in result["promotion_status"].items()
        if gate not in {"SFR3_G0_ARCHITECTURE_SPEC", "SFR3_G1_SYNTHETIC_CONTROLLABILITY"}
    )
    assert all(scenario["fusion_or_ignition_credit"] == 0.0 for scenario in result["scenarios"])


def test_persisted_sfr3_result_matches_recomputation() -> None:
    expected = json.loads(
        (ROOT / "results/sfr3_field_integrity/sfr3_field_integrity_shell_a_v070.json").read_text(
            encoding="utf-8"
        )
    )
    assert run_sfr3_field_integrity_screen(_config()) == expected
