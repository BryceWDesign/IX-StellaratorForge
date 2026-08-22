"""Low-authority dual-boundary AHIS integration screen for SFR-3.

The user-proposed "inside-out" AHIS is translated into two independently monitored
engineering boundaries.  The inner boundary observes plasma-facing armor, first-wall
temperature/strain and coolant state.  The outer boundary observes the double-wall
vacuum vessel, shield, supports and magnet alignment.  Neither boundary mechanically
confines plasma.  Corrective authority is limited to power rundown, coolant isolation,
safe hold and the already-declared SFR-3 synthetic trim-coil layer.

The thermal calculation is one-dimensional steady conduction with declared effective
properties.  The fault campaign is deterministic logic coverage.  Neither is structural
FEA, CFD, neutronics, fracture mechanics, a safety case or physical confinement evidence.
"""
from __future__ import annotations

from typing import Any

from .sfr3_field_integrity import run_sfr3_field_integrity_screen

AUTHORITY = (
    "LOW__1D_thermal_resistance_plus_deterministic_fault_logic__not_safety_or_confinement"
)
PASS_VERDICT = (
    "DUAL_BOUNDARY_ARCHITECTURE_SCREEN_PASS__PHYSICAL_SURVIVABILITY_AND_CONFINEMENT_UNPROVEN"
)
FAIL_VERDICT = "DUAL_BOUNDARY_ARCHITECTURE_SCREEN_REQUIREMENTS_NOT_MET"


def _thermal_case(stack: dict[str, Any], heat_flux_MW_m2: float) -> dict[str, Any]:
    heat_flux_W_m2 = heat_flux_MW_m2 * 1.0e6
    coolant_C = float(stack["coolant_bulk_temperature_C"])
    h = float(stack["coolant_heat_transfer_coefficient_W_m2K"])
    film_r = 1.0 / h
    film_delta = heat_flux_W_m2 * film_r
    current_C = coolant_C + film_delta
    interfaces_from_coolant: list[dict[str, Any]] = []
    layer_results_by_id: dict[str, dict[str, Any]] = {}
    for layer in reversed(stack["solid_layers_plasma_to_coolant"]):
        resistance = float(layer["thickness_m"]) / float(layer["effective_k_W_mK"])
        delta = heat_flux_W_m2 * resistance
        cold_C = current_C
        current_C += delta
        result = {
            "layer_id": layer["id"],
            "material": layer["material"],
            "cold_face_temperature_C": cold_C,
            "hot_face_temperature_C": current_C,
            "temperature_rise_K": delta,
            "thermal_resistance_m2K_W": resistance,
            "declared_max_service_temperature_C": float(
                layer["declared_max_service_temperature_C"]
            ),
            "temperature_screen_pass": current_C
            <= float(layer["declared_max_service_temperature_C"]),
        }
        interfaces_from_coolant.append(result)
        layer_results_by_id[layer["id"]] = result
    plasma_order = [
        layer_results_by_id[layer["id"]]
        for layer in stack["solid_layers_plasma_to_coolant"]
    ]
    solid_resistance = sum(
        float(layer["thickness_m"]) / float(layer["effective_k_W_mK"])
        for layer in stack["solid_layers_plasma_to_coolant"]
    )
    surface_C = current_C
    cte_values = [
        float(layer["effective_cte_per_K"])
        for layer in stack["solid_layers_plasma_to_coolant"]
    ]
    mismatch_strain = (max(cte_values) - min(cte_values)) * (surface_C - coolant_C)
    return {
        "heat_flux_MW_m2": heat_flux_MW_m2,
        "coolant_bulk_temperature_C": coolant_C,
        "coolant_film_temperature_rise_K": film_delta,
        "solid_thermal_resistance_m2K_W": solid_resistance,
        "total_thermal_resistance_m2K_W": solid_resistance + film_r,
        "plasma_facing_surface_temperature_C": surface_C,
        "layers_plasma_to_coolant": plasma_order,
        "all_layer_temperature_screens_pass": all(
            layer["temperature_screen_pass"] for layer in plasma_order
        ),
        "raw_cte_mismatch_strain_proxy": mismatch_strain,
        "raw_cte_mismatch_strain_screen_pass": mismatch_strain
        <= float(stack["maximum_raw_cte_mismatch_strain_proxy"]),
    }


def evaluate_stack(stack: dict[str, Any], thermal_screen: dict[str, Any]) -> dict[str, Any]:
    nominal = _thermal_case(stack, float(thermal_screen["nominal_heat_flux_MW_m2"]))
    upset = _thermal_case(stack, float(thermal_screen["upset_heat_flux_MW_m2"]))
    gates = stack["integration_gates"]
    weighted_score = sum(
        float(thermal_screen["decision_weights"][key]) * int(bool(value))
        for key, value in gates.items()
    )
    weighted_score += float(thermal_screen["decision_weights"]["thermal_screen_pass"]) * int(
        nominal["all_layer_temperature_screens_pass"]
        and upset["all_layer_temperature_screens_pass"]
        and upset["raw_cte_mismatch_strain_screen_pass"]
    )
    return {
        "id": stack["id"],
        "name": stack["name"],
        "status": stack["status"],
        "nominal": nominal,
        "upset_steady_upper_bound": upset,
        "integration_gates": gates,
        "declared_weighted_architecture_score": weighted_score,
        "physical_qualification_complete": False,
        "direct_plasma_confinement_credit": 0.0,
    }


def _monitoring_inventory(geometry: dict[str, Any]) -> dict[str, int]:
    sectors = int(geometry["toroidal_control_sectors"])
    nodes = int(geometry["poloidal_locations_per_sector"])
    lanes = int(geometry["independent_sensor_lanes"])
    paired_locations = sectors * nodes
    localized = (
        paired_locations
        * lanes
        * (
            len(geometry["inner_localized_sensor_types"])
            + len(geometry["outer_localized_sensor_types"])
        )
    )
    sector_channels = sectors * lanes * len(geometry["sector_sensor_types"])
    hard_vacuum = int(geometry["field_periods"]) * int(
        geometry["hard_vacuum_channels_per_field_period"]
    )
    return {
        "paired_inner_outer_monitoring_locations": paired_locations,
        "localized_sensing_elements": localized,
        "sector_sensing_elements": sector_channels,
        "independent_hard_vacuum_channels": hard_vacuum,
        "total_declared_sensing_elements": localized + sector_channels + hard_vacuum,
    }


def _signal_detected(
    signal: str,
    failed_channels: set[str],
    signal_channels: dict[str, list[str]],
) -> tuple[bool, list[str]]:
    candidates = signal_channels.get(signal, [])
    surviving = [channel for channel in candidates if channel not in failed_channels]
    return bool(surviving), surviving


def _fault_state(
    scenario: dict[str, Any],
    *,
    signal_channels: dict[str, list[str]],
    sfr3_nominal: dict[str, Any],
) -> dict[str, Any]:
    failed = set(scenario["failed_channels"])
    detections: dict[str, dict[str, Any]] = {}
    for signal in scenario["event_signals"]:
        detected, surviving = _signal_detected(signal, failed, signal_channels)
        detections[signal] = {
            "detected": detected,
            "surviving_channels": surviving,
        }
    all_signals_detected = all(value["detected"] for value in detections.values())
    latent = bool(scenario["latent_fault_without_declared_signal"])
    field_link: dict[str, Any] = {
        "requested": False,
        "available": False,
        "synthetic_rms_reduction_fraction": 0.0,
        "physical_confinement_credit": 0.0,
    }

    signals = set(scenario["event_signals"])
    if scenario["total_control_power_lost"]:
        state = "PASSIVE_HARD_SAFE_HOLD"
    elif scenario["observability_lost"]:
        state = "SAFE_HOLD_LOST_OBSERVABILITY"
    elif latent and not signals:
        state = "NO_AUTOMATIC_DETECTION__PERIODIC_NDE_REQUIRED"
    elif not all_signals_detected:
        state = "SAFE_HOLD_INCOMPLETE_EVENT_OBSERVABILITY"
    elif {"vacuum_loss", "coolant_leak"} & signals:
        state = "ISOLATE_AFFECTED_SECTOR_AND_SAFE_HOLD"
    elif "inner_temperature" in signals:
        state = "CONTROLLED_POWER_RUNDOWN_AND_INSPECT"
    elif {"outer_displacement", "flux_error"}.issubset(signals):
        field_link["requested"] = True
        field_link["available"] = bool(scenario["sfr3_active_trim_available"])
        if scenario["sfr3_active_trim_available"]:
            state = "ACTIVE_TRIM_THEN_CONTROLLED_INSPECTION"
            field_link["synthetic_rms_reduction_fraction"] = float(
                sfr3_nominal["total_rms_reduction_fraction"]
            )
        else:
            state = "SAFE_HOLD_ALIGNMENT_ERROR_UNCORRECTED"
    elif failed:
        state = "DEGRADED_MONITORING_SINGLE_LANE_RETAINED"
    else:
        state = "NOMINAL"

    return {
        "id": scenario["id"],
        "description": scenario["description"],
        "event_signals": scenario["event_signals"],
        "failed_channels": scenario["failed_channels"],
        "detections": detections,
        "all_declared_signals_detected": all_signals_detected,
        "control_state": state,
        "expected_control_state": scenario["expected_control_state"],
        "expected_state_pass": state == scenario["expected_control_state"],
        "latent_fault_retained_without_false_detection": latent and not signals,
        "sfr3_field_integrity_link": field_link,
        "mechanical_inward_plasma_force_credit": 0.0,
        "fusion_or_ignition_credit": 0.0,
    }


def validate_dual_boundary_config(raw: dict[str, Any]) -> tuple[str, ...]:
    errors: list[str] = []
    try:
        if raw["baseline_overlay_id"] != "SFR3-FIELD-INTEGRITY-SHELL-A":
            errors.append("dual boundary must remain an overlay on SFR-3 Field Integrity Shell A")
        if raw["architecture"]["mechanically_pushes_plasma_inward"]:
            errors.append("the monitored wall cannot receive inward plasma-force credit")
        if not raw["architecture"]["vacuum_vessel_is_double_walled"]:
            errors.append("the requested architecture requires a double-wall vacuum vessel")
        geometry = raw["monitoring_geometry"]
        if int(geometry["field_periods"]) != 4:
            errors.append("the preserved four-field-period baseline changed")
        if int(geometry["toroidal_control_sectors"]) != 24:
            errors.append("dual-boundary sectors must align with the 24 SFR-3 trim channels")
        if int(geometry["independent_sensor_lanes"]) != 2:
            errors.append("two independent sensor lanes are required")
        inventory = _monitoring_inventory(geometry)
        if inventory["paired_inner_outer_monitoring_locations"] != 192:
            errors.append("monitoring geometry must contain 192 paired locations")
        stack_ids = [stack["id"] for stack in raw["wall_stack_candidates"]]
        if len(stack_ids) != 3 or len(set(stack_ids)) != 3:
            errors.append("exactly three unique wall-stack candidates are required")
        if raw["selected_stack_id"] not in stack_ids:
            errors.append("selected wall stack is missing")
        required_scenarios = {
            "nominal",
            "inner_hotspot_single_lane_failure",
            "coolant_leak_single_lane_failure",
            "outer_support_shift",
            "inner_lane_a_loss",
            "outer_lane_a_loss",
            "sector_dual_bus_loss",
            "vacuum_breach",
            "total_control_power_loss",
            "silent_armor_crack",
            "support_shift_trim_unavailable",
        }
        scenario_ids = {scenario["id"] for scenario in raw["fault_scenarios"]}
        if scenario_ids != required_scenarios:
            errors.append("the complete eleven-scenario fault campaign changed")
        boundary = raw["claim_boundary"]
        for key in (
            "mechanical_plasma_confinement_credit",
            "magnetic_confinement_gain_credit",
            "fusion_power_gain_credit",
            "ignition_gain_credit",
            "safety_qualification_credit",
        ):
            if float(boundary[key]) != 0.0:
                errors.append(f"{key} must remain zero")
        promotion = raw["promotion_status"]
        allowed = {
            "SFR3D_G0_DUAL_BOUNDARY_SPEC": "PASS_SPEC_ONLY",
            "SFR3D_G1_REDUCED_THERMAL_AND_FAULT_SCREEN": "PASS_LOW_AUTHORITY_SYNTHETIC_ONLY",
        }
        for gate, status in promotion.items():
            if gate in allowed:
                if status != allowed[gate]:
                    errors.append(f"{gate} must be {allowed[gate]}")
            elif status != "NOT_RUN":
                errors.append(f"{gate} must remain NOT_RUN")
    except (KeyError, TypeError, ValueError) as exc:
        errors.append(f"invalid dual-boundary config: {exc}")
    return tuple(errors)


def run_dual_boundary_screen(
    raw: dict[str, Any], sfr3_raw: dict[str, Any]
) -> dict[str, Any]:
    errors = validate_dual_boundary_config(raw)
    if errors:
        raise ValueError("; ".join(errors))
    sfr3 = run_sfr3_field_integrity_screen(sfr3_raw)
    sfr3_by_id = {scenario["id"]: scenario for scenario in sfr3["scenarios"]}
    stack_results = [
        evaluate_stack(stack, raw["thermal_screen"])
        for stack in raw["wall_stack_candidates"]
    ]
    stack_by_id = {stack["id"]: stack for stack in stack_results}
    selected = stack_by_id[raw["selected_stack_id"]]
    best_score = max(stack["declared_weighted_architecture_score"] for stack in stack_results)
    selected_stack_pass = (
        selected["declared_weighted_architecture_score"] == best_score
        and selected["nominal"]["all_layer_temperature_screens_pass"]
        and selected["upset_steady_upper_bound"]["all_layer_temperature_screens_pass"]
        and selected["upset_steady_upper_bound"]["raw_cte_mismatch_strain_screen_pass"]
    )
    scenarios = [
        _fault_state(
            scenario,
            signal_channels=raw["signal_channels"],
            sfr3_nominal=sfr3_by_id["nominal"],
        )
        for scenario in raw["fault_scenarios"]
    ]
    scenario_logic_pass = all(scenario["expected_state_pass"] for scenario in scenarios)
    by_id = {scenario["id"]: scenario for scenario in scenarios}
    single_lane_faults_detected = all(
        by_id[scenario_id]["all_declared_signals_detected"]
        for scenario_id in (
            "inner_hotspot_single_lane_failure",
            "coolant_leak_single_lane_failure",
        )
    )
    silent_fault_honest = by_id["silent_armor_crack"][
        "latent_fault_retained_without_false_detection"
    ] and by_id["silent_armor_crack"]["control_state"].startswith("NO_AUTOMATIC_DETECTION")
    field_link_no_overclaim = (
        by_id["outer_support_shift"]["sfr3_field_integrity_link"][
            "synthetic_rms_reduction_fraction"
        ]
        > 0.0
        and by_id["outer_support_shift"]["sfr3_field_integrity_link"][
            "physical_confinement_credit"
        ]
        == 0.0
    )
    screen_pass = all(
        (
            selected_stack_pass,
            scenario_logic_pass,
            single_lane_faults_detected,
            silent_fault_honest,
            field_link_no_overclaim,
        )
    )
    return {
        "program": "IX-StellaratorForge",
        "release": "0.8.0",
        "study_id": raw["study_id"],
        "baseline_overlay_id": raw["baseline_overlay_id"],
        "authority": AUTHORITY,
        "top_level_verdict": PASS_VERDICT if screen_pass else FAIL_VERDICT,
        "screen_pass": screen_pass,
        "architecture": raw["architecture"],
        "monitoring_inventory": _monitoring_inventory(raw["monitoring_geometry"]),
        "wall_stack_results": stack_results,
        "selected_stack_id": raw["selected_stack_id"],
        "selected_stack_screen_pass": selected_stack_pass,
        "fault_scenarios": scenarios,
        "requirement_results": {
            "selected_stack_is_top_ranked_in_declared_reduced_screen": selected_stack_pass,
            "all_expected_fault_states_reproduce": scenario_logic_pass,
            "declared_single_lane_faults_retain_detection": single_lane_faults_detected,
            "silent_armor_crack_is_not_falsely_detected": silent_fault_honest,
            "sfr3_trim_link_remains_synthetic_only": field_link_no_overclaim,
        },
        "claim_boundary": raw["claim_boundary"],
        "promotion_status": raw["promotion_status"],
        "next_required_evidence": raw["next_required_evidence"],
    }
