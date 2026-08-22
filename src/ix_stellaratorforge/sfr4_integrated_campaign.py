"""SFR-4 integrated physical-promotion and heat-exhaust campaign.

This module attempts all seven requested computational workstreams with the strongest
methods available in the release runtime.  It uses direct filament Biot-Savart fields,
field-line integration, Bosch-Hale D-T reactivity, ISS04 confinement scaling, exact
source bookkeeping, one-dimensional thermal resistance, and deterministic hydraulic
and fault envelopes.  It fails closed where DESC, VMEC++, SIMSOPT, OpenMC, kinetic
transport, structural FEA, or physical qualification are required.

Passing a reduced screen can down-select an architecture.  It cannot demonstrate
equilibrium, confinement, ignition, component life, safety, or fusion.
"""
from __future__ import annotations

from dataclasses import asdict
import importlib.util
from math import pi, sqrt
from typing import Any

import numpy as np

from .burn import (
    DT_ALPHA_FRACTION,
    confinement_requirement,
    iss04_tau_E_s,
    uniform_dt_burn_point,
)
from .coil_hybrid import helical_hybrid_coil_screen
from .coil_screen import _poloidal_loop
from .hts_screen import screen_curve_geometry
from .neutronics_constraints import breeding_coverage_constraint
from .physics import dt_reaction_ledger
from .sfr3_dual_boundary import evaluate_stack
from .evidence_canonical import canonical_evidence
from .vacuum_codesign import evaluate_helical_architecture

AUTHORITY = (
    "MIXED_LOW_AND_INTERMEDIATE__DIRECT_FILAMENT_BIOT_SAVART_PLUS_ANALYTICAL_"
    "THERMAL_HYDRAULIC_BURN_AND_SOURCE_SCREENS__NOT_PRODUCTION_PHYSICS"
)
PASS_VERDICT = (
    "INTEGRATED_REDUCED_CAMPAIGN_COMPLETE__NOMINAL_HEAT_ENVELOPE_SCREEN_PASS__"
    "PHYSICAL_COIL_EQUILIBRIUM_CONFINEMENT_AND_FUSION_UNPROVEN"
)
FAIL_VERDICT = (
    "INTEGRATED_REDUCED_CAMPAIGN_COMPLETE__ONE_OR_MORE_REDUCED_GATES_FAIL__"
    "NO_FUSION_PROMOTION"
)

E_CHARGE = 1.602176634e-19
ALPHA_MASS_KG = 6.6446573357e-27
MU0 = 4e-7 * pi


def solver_availability() -> dict[str, bool]:
    return {
        name: importlib.util.find_spec(name) is not None
        for name in (
            "desc",
            "vmecpp",
            "simsopt",
            "openmc",
            "dolfinx",
            "fenics",
            "gmsh",
            "cadquery",
        )
    }


def _expanded_coil_scan(raw: dict[str, Any]) -> dict[str, Any]:
    scan = raw["coil_field_scan"]
    results: list[dict[str, Any]] = []
    for nfp in scan["field_periods"]:
        for pattern in scan["sign_patterns"]:
            for ratio in scan["helical_to_tf_current_ratios"]:
                result = evaluate_helical_architecture(
                    nfp=int(nfp),
                    R=float(scan["major_radius_m"]),
                    a=float(scan["minor_radius_m"]),
                    clearance_m=float(scan["plasma_to_coil_clearance_m"]),
                    target_B_T=float(scan["axis_field_T"]),
                    helical_coil_count=int(scan["helical_coil_count"]),
                    sign_pattern=str(pattern),
                    helical_to_tf_current_ratio=float(ratio),
                    turns=int(scan["field_line_turns"]),
                    steps_per_turn=int(scan["steps_per_turn"]),
                    iota_min=float(scan["iota_acceptance"][0]),
                    iota_max=float(scan["iota_acceptance"][1]),
                    max_excursion_fraction=float(scan["max_excursion_fraction"]),
                )
                results.append(asdict(result))

    def score(item: dict[str, Any]) -> tuple[float, float, float]:
        target = float(scan["iota_target"])
        excursion_penalty = max(
            0.0,
            float(item["normalized_max_excursion_over_a"])
            - float(scan["max_excursion_fraction"]),
        )
        return (
            abs(float(item["mean_iota"]) - target) + 3.0 * excursion_penalty,
            float(item["normalized_max_excursion_over_a"]),
            abs(float(item["helical_to_tf_current_ratio"])),
        )

    best = min(results, key=score)
    hybrid = helical_hybrid_coil_screen(
        nfp=int(best["nfp"]),
        R=float(scan["major_radius_m"]),
        a=float(scan["minor_radius_m"]),
        clearance_m=float(scan["plasma_to_coil_clearance_m"]),
        target_B_T=float(scan["axis_field_T"]),
        reconstruction_rms_limit=float(scan["normal_field_rms_limit"]),
    )
    coil_r = float(scan["minor_radius_m"]) + float(scan["plasma_to_coil_clearance_m"])
    tf_curve = _poloidal_loop(
        0.0, float(scan["major_radius_m"]), coil_r, nseg=240
    )
    hts_geometry = screen_curve_geometry(
        tf_curve,
        strain_target_fraction=float(scan["rebco_strain_target_fraction"]),
        strain_ceiling_fraction=float(scan["rebco_strain_ceiling_fraction"]),
    )
    return {
        "candidate_count": len(results),
        "best_candidate": best,
        "combined_pass_count": sum(bool(x["combined_screen_pass"]) for x in results),
        "held_out_hybrid_reconstruction": asdict(hybrid),
        "tf_centerline_geometry": asdict(hts_geometry),
        "physical_coil_promoted": bool(
            best["combined_screen_pass"]
            and hybrid.passes_reconstruction_screen
            and hts_geometry.passes_geometry_strain_proxy
        ),
        "authority": "direct_filament_Biot_Savart_and_field_line_screen_not_MHD_equilibrium",
    }


def _alpha_orbit_scope(raw: dict[str, Any], coil: dict[str, Any]) -> dict[str, Any]:
    cfg = raw["particle_screen"]
    energy_J = float(cfg["alpha_energy_MeV"]) * 1.0e6 * E_CHARGE
    speed = sqrt(2.0 * energy_J / ALPHA_MASS_KG)
    charge = 2.0 * E_CHARGE
    field = float(raw["coil_field_scan"]["axis_field_T"])
    gyro = ALPHA_MASS_KG * speed / (charge * field)
    a = float(raw["coil_field_scan"]["minor_radius_m"])
    best = coil["best_candidate"]
    field_line_gate = bool(best["combined_screen_pass"])
    return {
        "alpha_energy_MeV": float(cfg["alpha_energy_MeV"]),
        "alpha_speed_m_s_nonrelativistic": speed,
        "maximum_pitch_alpha_gyroradius_m": gyro,
        "gyroradius_over_minor_radius": gyro / a,
        "gyroradius_clearance_screen_pass": gyro / a
        <= float(cfg["maximum_gyroradius_over_minor_radius"]),
        "field_line_topology_prerequisite_pass": field_line_gate,
        "particle_confinement_promoted": False,
        "reason": (
            "A gyroradius scale and vacuum field-line test cannot establish guiding-center "
            "alpha retention. The physical coil candidate also fails its combined topology gate."
        ),
        "required_external_evidence": [
            "finite_beta_equilibrium",
            "Boozer_coordinates",
            "collisionless_and_collisional_guiding_center_orbits",
            "neoclassical_transport",
            "gyrokinetic_transport",
        ],
        "authority": "alpha_gyroradius_scope_only_not_orbit_retention",
    }


def _radiation_MW(*, electron_density_m3: float, temperature_keV: float,
                  volume_m3: float, zeff: float) -> float:
    # Common hydrogenic bremsstrahlung engineering approximation with T in keV.
    return 5.35e-37 * zeff * electron_density_m3**2 * sqrt(temperature_keV) * volume_m3 / 1e6


def _burn_and_confinement(raw: dict[str, Any], coil: dict[str, Any]) -> dict[str, Any]:
    cfg = raw["burn_screen"]
    R = float(raw["coil_field_scan"]["major_radius_m"])
    a = float(raw["coil_field_scan"]["minor_radius_m"])
    B = float(raw["coil_field_scan"]["axis_field_T"])
    volume = 2.0 * pi**2 * R * a**2
    burn = uniform_dt_burn_point(
        temperature_keV=float(cfg["temperature_keV"]),
        beta=float(cfg["beta"]),
        field_T=B,
        volume_m3=volume,
        target_fusion_power_MW=float(cfg["target_fusion_power_MW"]),
    )
    design_iota = float(cfg["design_iota_for_requirement_only"])
    physical_iota = max(float(coil["best_candidate"]["mean_iota"]), 1.0e-3)
    q_design = confinement_requirement(
        burn=burn,
        major_radius_m=R,
        minor_radius_m=a,
        iota_screen=design_iota,
        plasma_gain_Q=float(cfg["plasma_gain_Q"]),
    )
    q_physical = confinement_requirement(
        burn=burn,
        major_radius_m=R,
        minor_radius_m=a,
        iota_screen=physical_iota,
        plasma_gain_Q=float(cfg["plasma_gain_Q"]),
    )
    brem = _radiation_MW(
        electron_density_m3=burn.ion_density_m3,
        temperature_keV=burn.temperature_keV,
        volume_m3=burn.volume_m3,
        zeff=float(cfg["zeff"]),
    )
    alpha_MW = burn.target_fusion_power_MW * DT_ALPHA_FRACTION
    deposited_alpha = alpha_MW * float(cfg["alpha_deposition_fraction_assumption"])
    auxiliary = burn.target_fusion_power_MW / float(cfg["plasma_gain_Q"])
    available = deposited_alpha + auxiliary - brem
    required_tau_with_brem = (
        q_design.total_thermal_energy_MJ / available if available > 0 else float("inf")
    )
    h_with_brem = required_tau_with_brem / q_design.iss04_tau_E_H1_s
    return {
        "uniform_burn_point": asdict(burn),
        "design_iota_requirement": asdict(q_design),
        "best_physical_coil_iota_requirement": asdict(q_physical),
        "bremsstrahlung_MW_screen": brem,
        "deposited_alpha_heating_MW_assumption": deposited_alpha,
        "auxiliary_heating_MW": auxiliary,
        "net_heating_after_bremsstrahlung_MW": available,
        "required_tau_E_with_bremsstrahlung_s": required_tau_with_brem,
        "required_H_ISS04_with_bremsstrahlung_at_design_iota": h_with_brem,
        "physical_coil_linked_burn_promoted": False,
        "reason": "The best direct-filament coil fails topology; a design-iota burn target cannot be assigned to it.",
        "authority": "uniform_Bosch_Hale_plus_ISS04_and_bremsstrahlung_screen_not_transport_or_burn_simulation",
    }


def _layer_temperatures(
    *, heat_flux_MW_m2: float, coolant_C: float, h_W_m2K: float,
    layers_coolant_to_surface: list[dict[str, Any]],
) -> dict[str, Any]:
    q = heat_flux_MW_m2 * 1.0e6
    temperature = coolant_C + q / h_W_m2K
    interfaces = [{"location": "coolant_film_wall", "temperature_C": temperature}]
    pass_all = True
    for layer in layers_coolant_to_surface:
        temperature += q * float(layer["thickness_m"]) / float(layer["k_W_mK"])
        layer_pass = temperature <= float(layer["declared_max_temperature_C"])
        interfaces.append(
            {
                "layer": layer["id"],
                "outer_temperature_C": temperature,
                "declared_max_temperature_C": float(layer["declared_max_temperature_C"]),
                "temperature_screen_pass": layer_pass,
            }
        )
        pass_all = pass_all and layer_pass
    return {
        "heat_flux_MW_m2": heat_flux_MW_m2,
        "surface_temperature_C": temperature,
        "interfaces": interfaces,
        "all_temperature_screens_pass": pass_all,
    }


def _heat_exhaust(raw: dict[str, Any], burn: dict[str, Any]) -> dict[str, Any]:
    cfg = raw["heat_exhaust"]
    target_fusion = float(raw["burn_screen"]["target_fusion_power_MW"])
    alpha = target_fusion * DT_ALPHA_FRACTION
    auxiliary = target_fusion / float(raw["burn_screen"]["plasma_gain_Q"])
    exhaust = alpha * float(raw["burn_screen"]["alpha_deposition_fraction_assumption"]) + auxiliary
    radiation_fraction = float(cfg["controlled_radiation_fraction"])
    radiated = exhaust * radiation_fraction
    divertor = exhaust - radiated
    R = float(raw["coil_field_scan"]["major_radius_m"])
    a = float(raw["coil_field_scan"]["minor_radius_m"])
    first_wall_area = 4.0 * pi**2 * R * a * float(cfg["first_wall_area_multiplier"])
    wall_peak = radiated / first_wall_area * float(cfg["first_wall_peaking_factor"])
    target_peak = (
        divertor
        / float(cfg["effective_divertor_wetted_area_m2"])
        * float(cfg["divertor_peaking_factor"])
    )
    first_wall_limit = float(cfg["first_wall_nominal_limit_MW_m2"])
    divertor_limit = float(cfg["divertor_steady_limit_MW_m2"])
    minimum_radiation_for_selected_area = max(
        0.0,
        1.0
        - divertor_limit
        * float(cfg["effective_divertor_wetted_area_m2"])
        / (exhaust * float(cfg["divertor_peaking_factor"])),
    )
    maximum_radiation_from_first_wall_limit = min(
        1.0,
        first_wall_limit
        * first_wall_area
        / (exhaust * float(cfg["first_wall_peaking_factor"])),
    )
    minimum_area_at_selected_radiation = (
        exhaust
        * (1.0 - radiation_fraction)
        * float(cfg["divertor_peaking_factor"])
        / divertor_limit
    )
    sensitivity: list[dict[str, Any]] = []
    for radiation in cfg["radiation_fraction_sensitivity"]:
        for area in cfg["wetted_area_sensitivity_m2"]:
            q_wall = exhaust * float(radiation) / first_wall_area * float(
                cfg["first_wall_peaking_factor"]
            )
            q_target = exhaust * (1.0 - float(radiation)) / float(area) * float(
                cfg["divertor_peaking_factor"]
            )
            sensitivity.append(
                {
                    "controlled_radiation_fraction": float(radiation),
                    "effective_wetted_area_m2": float(area),
                    "first_wall_peak_MW_m2": q_wall,
                    "divertor_peak_MW_m2": q_target,
                    "heat_flux_limits_pass": bool(
                        q_wall <= first_wall_limit and q_target <= divertor_limit
                    ),
                }
            )

    divertor_thermal = _layer_temperatures(
        heat_flux_MW_m2=target_peak,
        coolant_C=float(cfg["divertor_coolant_bulk_temperature_C"]),
        h_W_m2K=float(cfg["divertor_heat_transfer_coefficient_W_m2K"]),
        layers_coolant_to_surface=cfg["divertor_layers_coolant_to_surface"],
    )
    water = cfg["divertor_water_loop"]
    cp = float(water["specific_heat_J_kgK"])
    delta_T = float(water["outlet_minus_inlet_K"])
    mass_flow = divertor * 1e6 / (cp * delta_T)
    channels = int(water["parallel_channels"])
    area_channel = float(water["channel_width_m"]) * float(water["channel_height_m"])
    velocity = mass_flow / (float(water["density_kg_m3"]) * channels * area_channel)
    hydraulic_diameter = 2.0 * float(water["channel_width_m"]) * float(water["channel_height_m"]) / (
        float(water["channel_width_m"]) + float(water["channel_height_m"])
    )
    dynamic_pressure = 0.5 * float(water["density_kg_m3"]) * velocity**2
    pressure_drop = (
        float(water["darcy_friction_factor"])
        * float(water["channel_length_m"])
        / hydraulic_diameter
        * dynamic_pressure
        + float(water["minor_loss_coefficient"]) * dynamic_pressure
    )
    pumping = pressure_drop * (mass_flow / float(water["density_kg_m3"])) / float(water["pump_efficiency"]) / 1e6

    first_wall_stack = raw["selected_first_wall_stack"]
    first_wall = evaluate_stack(
        first_wall_stack,
        {
            "nominal_heat_flux_MW_m2": wall_peak,
            "upset_heat_flux_MW_m2": float(cfg["first_wall_upset_heat_flux_MW_m2"]),
            "decision_weights": raw["first_wall_decision_weights"],
        },
    )
    steady_pass = all(
        (
            wall_peak <= first_wall_limit,
            target_peak <= divertor_limit,
            divertor_thermal["all_temperature_screens_pass"],
            first_wall["nominal"]["all_layer_temperature_screens_pass"],
            first_wall["upset_steady_upper_bound"]["all_layer_temperature_screens_pass"],
            velocity <= float(water["maximum_velocity_m_s"]),
            pumping <= float(water["maximum_pumping_power_MW"]),
        )
    )
    return {
        "plasma_exhaust_power_MW": exhaust,
        "controlled_radiation_MW": radiated,
        "divertor_power_MW": divertor,
        "first_wall_effective_area_m2": first_wall_area,
        "first_wall_peak_heat_flux_MW_m2": wall_peak,
        "divertor_peak_heat_flux_MW_m2": target_peak,
        "heat_partition_feasibility_window": {
            "minimum_controlled_radiation_fraction_at_selected_area": minimum_radiation_for_selected_area,
            "maximum_controlled_radiation_fraction_from_first_wall_limit": maximum_radiation_from_first_wall_limit,
            "minimum_effective_wetted_area_m2_at_selected_radiation": minimum_area_at_selected_radiation,
            "selected_point_inside_flux_window": bool(
                minimum_radiation_for_selected_area
                <= radiation_fraction
                <= maximum_radiation_from_first_wall_limit
                and float(cfg["effective_divertor_wetted_area_m2"])
                >= minimum_area_at_selected_radiation
            ),
        },
        "heat_partition_sensitivity": sensitivity,
        "divertor_thermal_screen": divertor_thermal,
        "selected_first_wall_screen": first_wall,
        "divertor_hydraulics": {
            "mass_flow_kg_s": mass_flow,
            "parallel_channels": channels,
            "mean_channel_velocity_m_s": velocity,
            "pressure_drop_Pa_screen": pressure_drop,
            "pumping_power_MW_screen": pumping,
        },
        "nominal_and_declared_steady_heat_envelope_pass": steady_pass,
        "transient_disruption_heat_resolved": False,
        "water_PbLi_separation_requirement": cfg["water_PbLi_separation_requirement"],
        "heat_verdict": (
            "NOMINAL_AND_DECLARED_STEADY_HEAT_ENVELOPE_SCREEN_PASS__DETACHMENT_"
            "EDGE_TOPOLOGY_TRANSIENTS_FATIGUE_AND_HARDWARE_UNPROVEN"
            if steady_pass
            else "DECLARED_HEAT_ENVELOPE_SCREEN_FAIL"
        ),
        "authority": "power_partition_plus_1D_conduction_and_hydraulics_not_edge_plasma_CFD_FEA_or_CHF_qualification",
    }


def _magnet_engineering(raw: dict[str, Any], coil: dict[str, Any]) -> dict[str, Any]:
    cfg = raw["magnet_engineering"]
    B = float(raw["coil_field_scan"]["axis_field_T"])
    magnetic_pressure = B**2 / (2.0 * MU0)
    R = float(raw["coil_field_scan"]["major_radius_m"])
    a = float(raw["coil_field_scan"]["minor_radius_m"])
    plasma_volume = 2.0 * pi**2 * R * a**2
    stored_proxy = magnetic_pressure * plasma_volume / 1e9
    current = float(coil["best_candidate"]["tf_current_MA_turn_per_filament"])
    return {
        "magnetic_pressure_MPa_axis_field_proxy": magnetic_pressure / 1e6,
        "stored_magnetic_energy_GJ_plasma_volume_proxy": stored_proxy,
        "best_candidate_tf_current_MA_turn_per_filament": current,
        "centerline_geometry_screen_pass": bool(coil["tf_centerline_geometry"]["passes_geometry_strain_proxy"]),
        "declared_peak_field_on_conductor_limit_T": float(cfg["peak_field_on_conductor_limit_T"]),
        "peak_field_on_conductor_calculated": False,
        "quench_protection_qualified": False,
        "structural_FEA_completed": False,
        "magnet_promoted": False,
        "authority": "magnetic_pressure_energy_and_centerline_geometry_scope_not_winding_pack_or_support_FEA",
    }


def _reactor_systems(raw: dict[str, Any], heat: dict[str, Any]) -> dict[str, Any]:
    cfg = raw["reactor_systems"]
    target = float(raw["burn_screen"]["target_fusion_power_MW"])
    ledger = dt_reaction_ledger(target)
    breeding = breeding_coverage_constraint(
        fusion_power_MW=target,
        global_tbr_target=float(cfg["global_tbr_target"]),
        coverage_fraction=float(cfg["breeding_coverage_fraction"]),
    )
    thermal = target * float(cfg["blanket_energy_multiplier"])
    gross = thermal * float(cfg["gross_thermal_efficiency"])
    recirc = float(cfg["base_recirculating_power_MW"]) + float(
        heat["divertor_hydraulics"]["pumping_power_MW_screen"]
    )
    net = gross - recirc
    return {
        "dt_source_ledger": asdict(ledger),
        "breeding_coverage_constraint": asdict(breeding),
        "conditional_thermal_power_MW": thermal,
        "conditional_gross_electric_MW": gross,
        "conditional_recirculating_power_MW": recirc,
        "conditional_net_electric_MW": net,
        "full_3D_TBR_calculated": False,
        "net_electric_prediction_promoted": False,
        "authority": "exact_source_and_conditional_plant_ledger_not_3D_neutronics_or_integrated_plant",
    }


def validate_integrated_config(raw: dict[str, Any]) -> tuple[str, ...]:
    errors: list[str] = []
    try:
        if raw["schema_version"] != "0.9.0":
            errors.append("schema_version must be 0.9.0")
        if raw["study_id"] != "SFR4-INTEGRATED-PHYSICAL-PROMOTION-A":
            errors.append("unexpected study_id")
        if set(raw["workstreams"]) != {
            "physical_coil_field",
            "finite_beta_equilibrium",
            "coil_plasma_codesign",
            "particle_confinement",
            "self_consistent_burn",
            "magnet_engineering",
            "reactor_systems",
        }:
            errors.append("all seven workstreams are required")
        if float(raw["claim_boundary"]["fusion_progress_credit_fraction"]) != 0.0:
            errors.append("fusion progress credit must remain zero before promotion")
        if not raw["heat_exhaust"]["water_PbLi_separation_requirement"]:
            errors.append("water divertor and PbLi blanket require independent double boundaries")
        if float(raw["heat_exhaust"]["divertor_steady_limit_MW_m2"]) > 10.0:
            errors.append("declared steady divertor limit may not exceed 10 MW/m2")
        if int(raw["heat_exhaust"]["divertor_water_loop"]["parallel_channels"]) < 100:
            errors.append("divertor channel count is not reactor distributed")
    except (KeyError, TypeError, ValueError) as exc:
        errors.append(f"invalid integrated config: {exc}")
    return tuple(errors)

@canonical_evidence
def run_integrated_campaign(raw: dict[str, Any]) -> dict[str, Any]:
    errors = validate_integrated_config(raw)
    if errors:
        raise ValueError("; ".join(errors))
    solvers = solver_availability()
    coil = _expanded_coil_scan(raw)
    particles = _alpha_orbit_scope(raw, coil)
    burn = _burn_and_confinement(raw, coil)
    heat = _heat_exhaust(raw, burn)
    magnets = _magnet_engineering(raw, coil)
    systems = _reactor_systems(raw, heat)
    equilibrium = {
        "desc_available": solvers["desc"],
        "vmecpp_available": solvers["vmecpp"],
        "cross_code_equilibrium_completed": False,
        "status": "NOT_RUN__PRODUCTION_SOLVERS_UNAVAILABLE_IN_BUILD_RUNTIME",
        "fail_closed": True,
    }
    codesign = {
        "direct_filament_candidate_count": coil["candidate_count"],
        "simsopt_available": solvers["simsopt"],
        "production_single_stage_codesign_completed": False,
        "status": "REDUCED_SCAN_EXECUTED__PRODUCTION_CODESIGN_NOT_RUN",
    }
    reduced_complete = all(
        (
            coil["candidate_count"] > 0,
            heat["nominal_and_declared_steady_heat_envelope_pass"],
            systems["conditional_net_electric_MW"] > 0.0,
            equilibrium["fail_closed"],
            not particles["particle_confinement_promoted"],
            not magnets["magnet_promoted"],
        )
    )
    return {
        "program": "IX-StellaratorForge",
        "release": "0.9.0",
        "study_id": raw["study_id"],
        "authority": AUTHORITY,
        "top_level_verdict": PASS_VERDICT if reduced_complete else FAIL_VERDICT,
        "reduced_campaign_complete": reduced_complete,
        "solver_availability": solvers,
        "workstreams": {
            "1_physical_coil_field": coil,
            "2_finite_beta_equilibrium": equilibrium,
            "3_coil_plasma_codesign": codesign,
            "4_particle_confinement": particles,
            "5_self_consistent_burn": burn,
            "6_magnet_engineering": magnets,
            "7_reactor_systems": systems,
        },
        "heat_exhaust_resolution": heat,
        "promotion_summary": {
            "nominal_and_declared_steady_heat_envelope_screen_pass": heat[
                "nominal_and_declared_steady_heat_envelope_pass"
            ],
            "production_equilibrium_pass": False,
            "physical_confinement_pass": False,
            "sustained_burn_pass": False,
            "magnet_qualification_pass": False,
            "full_3D_TBR_pass": False,
            "hardware_pass": False,
            "earned_fusion_progress_credit_fraction": 0.0,
        },
        "claim_boundary": raw["claim_boundary"],
    }
