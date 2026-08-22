"""Low-authority harmonic controllability screen for the SFR-3 field-integrity shell.

The screen translates useful patterns from the donor repositories into a fusion-specific
architecture without importing their unrelated material physics.  A deterministic
Fourier response matrix asks whether a distributed trim-coil set has enough *synthetic*
authority to reduce a declared normal-field-error challenge.  Passive superconducting
loops attenuate only the declared time-varying component.  A resource gate suppresses
active commands when sensing, power, thermal or quench state is unacceptable.

This is not a Biot-Savart coil design, free-boundary equilibrium, island calculation,
particle-orbit calculation, transport model, MHD result, neutronics model or hardware
demonstration.  It earns zero confinement, fusion-power or ignition credit.
"""
from __future__ import annotations

from math import cos, exp, pi, sin, sqrt
from typing import Any

import numpy as np

AUTHORITY = "LOW__synthetic_linear_harmonic_controllability__not_physical_confinement"
PASS_VERDICT = (
    "SYNTHETIC_HARMONIC_CONTROL_DEMONSTRATED__PHYSICAL_CONFINEMENT_UNPROVEN"
)
FAIL_VERDICT = "SYNTHETIC_HARMONIC_CONTROL_REQUIREMENTS_NOT_MET"


def _rms(values: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(values))))


def build_response_matrix(screen: dict[str, Any]) -> np.ndarray:
    """Return the deterministic dimensionless mode/actuator response matrix.

    Actuator positions follow a declared helical index around a toroidal array.  The
    exponential factor is only a transparent gap/spectral attenuation heuristic.  It
    must eventually be replaced by a field solver response matrix.
    """
    count = int(screen["actuator_count"])
    field_periods = int(screen["field_periods"])
    helical_index = int(screen["actuator_helical_index"])
    gap_factor = float(screen["gap_attenuation_factor"])
    response_scale = float(screen["response_per_full_command_units"])
    rows: list[list[float]] = []
    for mode in screen["modes"]:
        m = int(mode["m"])
        n = int(mode["n"])
        attenuation = exp(-gap_factor * sqrt(m * m + (n / field_periods) ** 2))
        cosine_row: list[float] = []
        sine_row: list[float] = []
        for index in range(count):
            phi = 2.0 * pi * index / count
            theta = 2.0 * pi * ((helical_index * index) % count) / count
            phase = m * theta - n * phi
            cosine_row.append(response_scale * attenuation * cos(phase))
            sine_row.append(response_scale * attenuation * sin(phase))
        rows.extend((cosine_row, sine_row))
    return np.asarray(rows, dtype=float)


def validate_sfr3_config(raw: dict[str, Any]) -> tuple[str, ...]:
    errors: list[str] = []
    try:
        if raw["baseline_design_id"] != "SFR-1-RevA":
            errors.append("SFR-3 must remain an overlay on SFR-1-RevA")
        architecture = raw["architecture"]
        if not architecture["primary_field_is_steady"]:
            errors.append("the primary stellarator field must remain steady")
        if architecture["vacuum_vessel_is_flexible"]:
            errors.append("the vacuum vessel must remain rigid")
        if architecture["passive_material_claimed_to_confine_plasma"]:
            errors.append("passive material cannot receive plasma-confinement credit")
        screen = raw["harmonic_screen"]
        count = int(screen["actuator_count"])
        if count < 2 * len(screen["modes"]):
            errors.append("actuator count must be at least twice the harmonic count")
        if count < 12 or count > 256:
            errors.append("actuator count must remain within the declared screening range")
        if int(screen["field_periods"]) != 4:
            errors.append("the SFR-1 four-field-period baseline changed")
        if not 0.0 < float(screen["passive_transient_attenuation_fraction"]) < 1.0:
            errors.append("passive transient attenuation must be strictly between zero and one")
        if float(screen["max_abs_command"]) <= 0.0:
            errors.append("trim-coil command limit must be positive")
        coefficient_count = 2 * len(screen["modes"])
        for name in ("static_error_coefficients", "transient_error_coefficients"):
            if len(screen[name]) != coefficient_count:
                errors.append(f"{name} must contain cosine/sine coefficients for every mode")
        matrix = build_response_matrix(screen)
        if matrix.shape != (coefficient_count, count):
            errors.append("response matrix shape is inconsistent")
        if np.linalg.matrix_rank(matrix) < coefficient_count:
            errors.append("declared trim array does not span every screened harmonic")
        scenario_ids = [scenario["id"] for scenario in raw["scenarios"]]
        required = {
            "nominal",
            "single_actuator_unavailable",
            "low_sensor_confidence",
            "passive_loop_quench",
            "active_coil_quench",
            "thermal_margin_exhausted",
            "passive_transient_only",
        }
        if not required.issubset(scenario_ids):
            errors.append("required nominal, fault and passive-only scenarios are missing")
        promotion = raw["promotion_status"]
        allowed = {
            "SFR3_G0_ARCHITECTURE_SPEC": "PASS_SPEC_ONLY",
            "SFR3_G1_SYNTHETIC_CONTROLLABILITY": "PASS_LOW_AUTHORITY_SYNTHETIC_ONLY",
        }
        for gate, status in promotion.items():
            if gate in allowed:
                if status != allowed[gate]:
                    errors.append(f"{gate} must be {allowed[gate]}")
            elif status != "NOT_RUN":
                errors.append(f"{gate} must remain NOT_RUN without higher-authority evidence")
        boundary = raw["claim_boundary"]
        for key in (
            "confinement_gain_credit",
            "fusion_power_gain_credit",
            "ignition_gain_credit",
            "net_electric_gain_credit",
        ):
            if float(boundary[key]) != 0.0:
                errors.append(f"{key} must remain zero")
    except (KeyError, TypeError, ValueError) as exc:
        errors.append(f"invalid SFR-3 field-integrity config: {exc}")
    return tuple(errors)


def _resource_gate(
    scenario: dict[str, Any], thresholds: dict[str, Any]
) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if not scenario["active_correction_requested"]:
        reasons.append("active correction not requested")
    if float(scenario["sensor_confidence"]) < float(thresholds["minimum_sensor_confidence"]):
        reasons.append("sensor confidence below threshold")
    if not scenario["trim_power_available"]:
        reasons.append("trim power unavailable")
    if float(scenario["trim_thermal_margin_fraction"]) < float(
        thresholds["minimum_trim_thermal_margin_fraction"]
    ):
        reasons.append("trim thermal margin below threshold")
    if scenario["active_coil_quench_detected"]:
        reasons.append("active-coil quench detected")
    if not scenario["independent_watchdog_healthy"]:
        reasons.append("independent watchdog unhealthy")
    return not reasons, reasons


def _bounded_ridge_solution(
    matrix: np.ndarray,
    error: np.ndarray,
    *,
    failed_actuators: list[int],
    regularization: float,
    max_abs_command: float,
) -> tuple[np.ndarray, dict[str, Any]]:
    available = matrix.copy()
    for index in failed_actuators:
        available[:, index] = 0.0
    lhs = available.T @ available + regularization * np.eye(available.shape[1])
    command = np.linalg.solve(lhs, -(available.T @ error))
    unconstrained_peak = float(np.max(np.abs(command)))
    scaled_to_limit = unconstrained_peak > max_abs_command
    if scaled_to_limit:
        command *= max_abs_command / unconstrained_peak
    nonfailed = [index for index in range(matrix.shape[1]) if index not in failed_actuators]
    available_singular_values = np.linalg.svd(available[:, nonfailed], compute_uv=False)
    regularized_condition = float(
        np.linalg.cond(available @ available.T + regularization * np.eye(available.shape[0]))
    )
    diagnostics = {
        "failed_actuators": failed_actuators,
        "unconstrained_peak_command": unconstrained_peak,
        "scaled_to_command_limit": scaled_to_limit,
        "peak_command_utilization": float(np.max(np.abs(command)) / max_abs_command),
        "available_response_rank": int(np.linalg.matrix_rank(available[:, nonfailed])),
        "available_response_singular_values": [float(value) for value in available_singular_values],
        "regularized_condition_number": regularized_condition,
    }
    return command, diagnostics


def _evaluate_scenario(
    scenario: dict[str, Any],
    *,
    screen: dict[str, Any],
    thresholds: dict[str, Any],
    matrix: np.ndarray,
) -> dict[str, Any]:
    static = np.asarray(screen["static_error_coefficients"], dtype=float) * float(
        scenario["static_error_scale"]
    )
    transient = np.asarray(screen["transient_error_coefficients"], dtype=float) * float(
        scenario["transient_error_scale"]
    )
    initial = static + transient
    passive_healthy = bool(scenario["passive_loops_available"]) and not bool(
        scenario["passive_loop_quench_detected"]
    )
    passive_fraction = (
        float(screen["passive_transient_attenuation_fraction"]) if passive_healthy else 0.0
    )
    after_passive = static + transient * (1.0 - passive_fraction)
    active_allowed, gate_reasons = _resource_gate(scenario, thresholds)
    if active_allowed:
        command, diagnostics = _bounded_ridge_solution(
            matrix,
            after_passive,
            failed_actuators=[int(value) for value in scenario["failed_actuator_indices"]],
            regularization=float(screen["ridge_regularization"]),
            max_abs_command=float(screen["max_abs_command"]),
        )
        final = after_passive + matrix @ command
        state = "ACTIVE_TRIM"
    else:
        command = np.zeros(matrix.shape[1])
        final = after_passive
        state = "PASSIVE_ONLY_SAFE_HOLD" if passive_healthy else "BASELINE_SAFE_HOLD"
        diagnostics = {
            "failed_actuators": [int(value) for value in scenario["failed_actuator_indices"]],
            "unconstrained_peak_command": 0.0,
            "scaled_to_command_limit": False,
            "peak_command_utilization": 0.0,
            "available_response_rank": None,
            "available_response_singular_values": [],
            "regularized_condition_number": None,
        }
    initial_rms = _rms(initial)
    after_passive_rms = _rms(after_passive)
    final_rms = _rms(final)
    passive_reduction = 0.0 if initial_rms == 0.0 else 1.0 - after_passive_rms / initial_rms
    final_reduction = 0.0 if initial_rms == 0.0 else 1.0 - final_rms / initial_rms
    coefficient_unit = float(screen["coefficient_unit_Bn_over_Baxis"])
    return {
        "id": scenario["id"],
        "description": scenario["description"],
        "control_state": state,
        "active_correction_allowed": active_allowed,
        "resource_gate_reasons": gate_reasons,
        "passive_loops_healthy": passive_healthy,
        "passive_transient_attenuation_fraction_applied": passive_fraction,
        "initial_error_rms_coefficient_units": initial_rms,
        "after_passive_error_rms_coefficient_units": after_passive_rms,
        "final_error_rms_coefficient_units": final_rms,
        "initial_error_rms_Bn_over_Baxis": initial_rms * coefficient_unit,
        "final_error_rms_Bn_over_Baxis": final_rms * coefficient_unit,
        "passive_only_rms_reduction_fraction": passive_reduction,
        "total_rms_reduction_fraction": final_reduction,
        "commands": [float(value) for value in command],
        "diagnostics": diagnostics,
        "fusion_or_ignition_credit": 0.0,
    }


def run_sfr3_field_integrity_screen(raw: dict[str, Any]) -> dict[str, Any]:
    """Run the declared SFR-3 screen and return a deterministic evidence artifact."""
    errors = validate_sfr3_config(raw)
    if errors:
        raise ValueError("; ".join(errors))
    screen = raw["harmonic_screen"]
    matrix = build_response_matrix(screen)
    scenarios = [
        _evaluate_scenario(
            scenario,
            screen=screen,
            thresholds=raw["resource_gate_thresholds"],
            matrix=matrix,
        )
        for scenario in raw["scenarios"]
    ]
    by_id = {scenario["id"]: scenario for scenario in scenarios}
    nominal = by_id["nominal"]
    single_failure = by_id["single_actuator_unavailable"]
    passive_only = by_id["passive_transient_only"]
    nominal_pass = (
        nominal["active_correction_allowed"]
        and nominal["total_rms_reduction_fraction"]
        >= float(screen["minimum_nominal_rms_reduction_fraction"])
        and nominal["diagnostics"]["regularized_condition_number"]
        <= float(screen["maximum_regularized_condition_number"])
    )
    single_failure_pass = (
        single_failure["active_correction_allowed"]
        and single_failure["total_rms_reduction_fraction"]
        >= float(screen["minimum_single_failure_rms_reduction_fraction"])
    )
    passive_transient_pass = (
        not passive_only["active_correction_allowed"]
        and passive_only["passive_only_rms_reduction_fraction"]
        >= float(screen["minimum_passive_transient_reduction_fraction"])
    )
    low_confidence_safe = (
        by_id["low_sensor_confidence"]["control_state"] == "PASSIVE_ONLY_SAFE_HOLD"
        and not by_id["low_sensor_confidence"]["active_correction_allowed"]
    )
    loop_quench_safe = (
        by_id["passive_loop_quench"]["control_state"] == "ACTIVE_TRIM"
        and not by_id["passive_loop_quench"]["passive_loops_healthy"]
    )
    active_quench_safe = (
        by_id["active_coil_quench"]["control_state"] == "PASSIVE_ONLY_SAFE_HOLD"
        and not by_id["active_coil_quench"]["active_correction_allowed"]
    )
    thermal_margin_safe = (
        by_id["thermal_margin_exhausted"]["control_state"] == "PASSIVE_ONLY_SAFE_HOLD"
        and not by_id["thermal_margin_exhausted"]["active_correction_allowed"]
    )
    screen_pass = all(
        (
            nominal_pass,
            single_failure_pass,
            passive_transient_pass,
            low_confidence_safe,
            loop_quench_safe,
            active_quench_safe,
            thermal_margin_safe,
        )
    )
    return {
        "program": "IX-StellaratorForge",
        "release": "0.7.0",
        "study_id": raw["study_id"],
        "baseline_design_id": raw["baseline_design_id"],
        "authority": AUTHORITY,
        "top_level_verdict": PASS_VERDICT if screen_pass else FAIL_VERDICT,
        "screen_pass": screen_pass,
        "architecture": raw["architecture"],
        "claim_boundary": raw["claim_boundary"],
        "model_definition": {
            "field_periods": int(screen["field_periods"]),
            "actuator_count": int(screen["actuator_count"]),
            "mode_count": len(screen["modes"]),
            "coefficient_count": 2 * len(screen["modes"]),
            "coefficient_unit_Bn_over_Baxis": float(screen["coefficient_unit_Bn_over_Baxis"]),
            "response_matrix_rank": int(np.linalg.matrix_rank(matrix)),
            "response_matrix_shape": list(matrix.shape),
            "response_matrix_source": "deterministic analytic heuristic; replace with Biot-Savart/free-boundary response",
            "passive_loops_have_dc_correction_credit": False,
        },
        "requirements": {
            "nominal_rms_reduction_fraction": float(
                screen["minimum_nominal_rms_reduction_fraction"]
            ),
            "single_failure_rms_reduction_fraction": float(
                screen["minimum_single_failure_rms_reduction_fraction"]
            ),
            "passive_transient_reduction_fraction": float(
                screen["minimum_passive_transient_reduction_fraction"]
            ),
            "maximum_regularized_condition_number": float(
                screen["maximum_regularized_condition_number"]
            ),
        },
        "requirement_results": {
            "nominal_synthetic_controllability_pass": nominal_pass,
            "single_actuator_failure_pass": single_failure_pass,
            "passive_transient_screen_pass": passive_transient_pass,
            "low_confidence_enters_safe_hold": low_confidence_safe,
            "passive_loop_quench_isolated_without_active_overclaim": loop_quench_safe,
            "active_coil_quench_enters_passive_only_safe_hold": active_quench_safe,
            "thermal_margin_loss_enters_passive_only_safe_hold": thermal_margin_safe,
        },
        "scenarios": scenarios,
        "donor_translation": raw["donor_translation"],
        "promotion_status": raw["promotion_status"],
        "next_required_evidence": raw["next_required_evidence"],
    }
