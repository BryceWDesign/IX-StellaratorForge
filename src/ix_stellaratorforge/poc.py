"""Executable SFR-1 proof-of-concept evidence bundle.

The PoC proves that the *research/design pipeline* is executable and internally consistent.
It does not prove a fusion reactor, equilibrium, confinement, breeding blanket, or net power.
"""
from __future__ import annotations

from dataclasses import asdict
from math import pi
from typing import Any

from .burn import (
    confinement_requirement,
    required_uniform_beta_for_target,
    uniform_dt_burn_point,
)
from .closure import solver_availability
from .coil_hybrid import helical_hybrid_coil_screen
from .physics import dt_reaction_ledger, ecrh_frequency_ghz, power_balance
from .reactor import ReactorConfig, validate_reactor_config


def run_sfr1_poc(config: ReactorConfig) -> dict[str, Any]:
    raw = config.raw
    env = raw["reactor_envelope"]
    thermal = raw["thermal_power_conversion"]
    magnet = raw["magnet_system"]
    validation = validate_reactor_config(config)

    R = float(env["major_radius_m"])
    a = float(env["minor_radius_m"])
    B = float(env["magnetic_field_axis_T"])
    beta = float(env["volume_average_beta"])
    temperature = float(env["screening_temperature_keV"]["ion"])
    target_fusion = float(env["fusion_power_target_MW"])
    volume = 2.0 * pi**2 * R * a**2

    burn = uniform_dt_burn_point(
        temperature_keV=temperature,
        beta=beta,
        field_T=B,
        volume_m3=volume,
        target_fusion_power_MW=target_fusion,
    )
    q10 = confinement_requirement(
        burn=burn,
        major_radius_m=R,
        minor_radius_m=a,
        iota_screen=0.55,
        plasma_gain_Q=10.0,
    )
    ignition = confinement_requirement(
        burn=burn,
        major_radius_m=R,
        minor_radius_m=a,
        iota_screen=0.55,
        plasma_gain_Q=None,
    )

    target_power = power_balance(
        target_fusion,
        thermal["blanket_energy_multiplier_screening"],
        thermal["gross_thermal_to_electric_efficiency_target"],
        thermal["recirculating_power_MW_design_ceiling"],
    )
    screened_power = power_balance(
        burn.fusion_power_MW_uniform,
        thermal["blanket_energy_multiplier_screening"],
        thermal["gross_thermal_to_electric_efficiency_target"],
        thermal["recirculating_power_MW_design_ceiling"],
    )

    coil_results = {}
    for nfp in (2, 3, 4, 6):
        result = helical_hybrid_coil_screen(
            nfp=nfp,
            R=R,
            a=a,
            clearance_m=magnet["minimum_plasma_to_coil_distance_m_target"],
            target_B_T=B,
        )
        coil_results[str(nfp)] = asdict(result)

    dt = dt_reaction_ledger(target_fusion)
    tbr_target = float(raw["blanket_fuel_cycle"]["tbr_design_target"])
    floor = float(thermal["net_electric_power_MW_design_floor"])
    beta_needed = required_uniform_beta_for_target(burn)
    solvers = solver_availability()

    statements = {
        "architecture_invariants_pass": validation.passed,
        "uniform_burn_is_positive": burn.fusion_power_MW_uniform > 0.0,
        "target_power_ledger_meets_floor": target_power.net_electric_MW_at_recirc_ceiling >= floor,
        "current_uniform_screen_meets_floor": screened_power.net_electric_MW_at_recirc_ceiling >= floor,
        "any_fixed_hybrid_coil_basis_passes_0p5pct_rms_screen": any(
            item["passes_reconstruction_screen"] for item in coil_results.values()
        ),
        "high_fidelity_mhd_solver_available_here": bool(solvers["desc"] or solvers["vmecpp"]),
        "openmc_available_here": bool(solvers["openmc"]),
    }

    return {
        "program": "IX-StellaratorForge",
        "artifact": "SFR-1 executable proof of concept",
        "release": "0.4.0",
        "authority": "analytical_empirical_and_intermediate_magnetic_screening",
        "claim_boundary": (
            "This PoC validates the executable research/design pipeline only. It is not evidence "
            "of a solved finite-beta stellarator equilibrium, validated confinement, a qualified "
            "magnet, TBR self-sufficiency, ignition, net energy, or net electricity."
        ),
        "architecture_validation": {
            "passed": validation.passed,
            "errors": list(validation.errors),
            "warnings": list(validation.warnings),
        },
        "burn_screen": {
            **asdict(burn),
            "uniform_beta_needed_for_1GW_target": beta_needed,
            "power_gap_to_target_MW": target_fusion - burn.fusion_power_MW_uniform,
        },
        "confinement_requirements": {
            "Q10": asdict(q10),
            "ignition_limit": asdict(ignition),
        },
        "held_out_coil_reconstruction": {
            "acceptance_screen_rms_Bn_over_B": 5e-3,
            "results": coil_results,
            "interpretation": (
                "The richer fixed filament basis is evaluated on unseen surface nodes. A failure "
                "means real plasma/coil co-optimization is still mandatory; a pass would still "
                "not constitute a buildable REBCO magnet."
            ),
        },
        "rf_screen": {
            "axis_field_T": B,
            "fundamental_electron_cyclotron_GHz": ecrh_frequency_ghz(B),
            "nominal_ECRH_GHz": raw["heating_control"]["nominal_frequency_GHz"],
        },
        "neutronics_source_term": {
            "target_fusion_power_MW": target_fusion,
            "neutron_power_MW": dt.neutron_power_MW,
            "dt_reaction_rate_s": dt.reaction_rate_per_s,
            "tritium_burn_kg_day": dt.tritium_burn_kg_per_day,
            "tbr_target": tbr_target,
            "minimum_bred_tritium_kg_day_at_tbr_target": dt.tritium_burn_kg_per_day * tbr_target,
        },
        "power_balance": {
            "design_target": asdict(target_power),
            "uniform_burn_screen": asdict(screened_power),
            "net_electric_design_floor_MW": floor,
        },
        "external_solver_availability_in_build_runtime": solvers,
        "boolean_checks": statements,
        "verdict": "PIPELINE_POC_PASS__REACTOR_PHYSICS_NOT_CLOSED",
    }
