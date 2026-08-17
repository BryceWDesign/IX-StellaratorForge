"""Integrated SFR-1 closure campaign using only computations reproducible in-repo."""
from __future__ import annotations

from dataclasses import asdict
import importlib.util
from math import pi
from typing import Any

from .burn import (
    confinement_requirement, fixed_pressure_optimum_temperature_keV,
    required_uniform_beta_for_target, uniform_dt_burn_point,
)
from .coil_screen import planar_encircling_coil_screen
from .coil_hybrid import helical_hybrid_coil_screen
from .physics import dt_reaction_ledger, ecrh_frequency_ghz, power_balance
from .reactor import ReactorConfig


def solver_availability() -> dict[str, bool]:
    return {name: importlib.util.find_spec(name) is not None for name in ("desc", "vmecpp", "simsopt", "openmc")}


def run_closure_campaign(config: ReactorConfig) -> dict[str, Any]:
    raw = config.raw
    env = raw["reactor_envelope"]
    R, a, B = env["major_radius_m"], env["minor_radius_m"], env["magnetic_field_axis_T"]
    V = 2*pi*pi*R*a*a
    T = env["screening_temperature_keV"]["ion"]
    target = env["fusion_power_target_MW"]
    burn = uniform_dt_burn_point(temperature_keV=T, beta=env["volume_average_beta"], field_T=B, volume_m3=V, target_fusion_power_MW=target)
    beta_for_target = required_uniform_beta_for_target(burn)
    optimum_T, optimum_uniform_MW = fixed_pressure_optimum_temperature_keV(
        beta=env["volume_average_beta"], field_T=B, volume_m3=V, target_fusion_power_MW=target
    )
    iota_screen = 0.55
    q10 = confinement_requirement(burn=burn, major_radius_m=R, minor_radius_m=a, iota_screen=iota_screen, plasma_gain_Q=10.0)
    ignition = confinement_requirement(burn=burn, major_radius_m=R, minor_radius_m=a, iota_screen=iota_screen, plasma_gain_Q=None)
    magnet = raw["magnet_system"]
    coil = {
        str(nfp): asdict(planar_encircling_coil_screen(
            nfp=nfp, R=R, a=a,
            clearance_m=magnet["minimum_plasma_to_coil_distance_m_target"],
            target_B_T=B,
        ))
        for nfp in (2, 3, 4, 6)
    }
    held_out_coil = {
        str(nfp): asdict(helical_hybrid_coil_screen(
            nfp=nfp, R=R, a=a,
            clearance_m=magnet["minimum_plasma_to_coil_distance_m_target"],
            target_B_T=B,
        ))
        for nfp in (2, 3, 4, 6)
    }
    thermal = raw["thermal_power_conversion"]
    target_power = power_balance(target, thermal["blanket_energy_multiplier_screening"], thermal["gross_thermal_to_electric_efficiency_target"], thermal["recirculating_power_MW_design_ceiling"])
    uniform_power = power_balance(burn.fusion_power_MW_uniform, thermal["blanket_energy_multiplier_screening"], thermal["gross_thermal_to_electric_efficiency_target"], thermal["recirculating_power_MW_design_ceiling"])
    dt = dt_reaction_ledger(target)
    required_tbr_margin = raw["blanket_fuel_cycle"]["tbr_design_target"] - 1.0
    return {
        "campaign": "SFR-1 Closure Campaign v0.3.0",
        "authority": "mixed_analytical_empirical_intermediate; external high-fidelity solvers not available in this runtime",
        "external_solver_availability": solver_availability(),
        "G1_equilibrium": {
            "status": "OPEN_EXTERNAL_SOLVER_REQUIRED",
            "reason": "No DESC/VMEC++ executable is available in this runtime; no 3-D MHD force-balance result is fabricated.",
        },
        "burn_scoping": {
            **asdict(burn),
            "uniform_model_beta_required_for_target": beta_for_target,
            "fixed_pressure_optimum_temperature_keV_grid": optimum_T,
            "fixed_pressure_optimum_uniform_fusion_MW_grid": optimum_uniform_MW,
            "interpretation": "The uniform model is a lower-authority consistency screen; profile peaking, impurities, ash, radiation and transport are unresolved.",
        },
        "G3_G4_confinement_scoping": {
            "Q10": asdict(q10),
            "ignition_limit": asdict(ignition),
            "status": "SCREENED_NOT_VALIDATED",
            "note": "ISS04 is empirical. Gyrokinetic, neoclassical and energetic-particle solvers remain required.",
        },
        "G2_coil_diagnostic": {
            "encircling_only_results": coil,
            "held_out_hybrid_results": held_out_coil,
            "held_out_acceptance_screen_rms_Bn_over_B": 5e-3,
            "status": "FAILS_FIXED_BASIS_SCREEN__OPTIMIZED_COIL_SET_OPEN",
            "note": (
                "Analytic reduced-surface normals are used. Simple encircling coils and the richer "
                "fixed filament basis remain screening tools. The richer basis is fitted on one "
                "surface grid and evaluated on an angularly offset held-out grid; no passing case "
                "may be called buildable without solved-boundary co-optimization, REBCO strain, "
                "support FEA and manufacturing-error evidence."
            ),
        },
        "G5_exhaust": {
            "status": "OPEN_3D_EDGE_AND_DIVERTOR_SOLVER_REQUIRED",
            "reason": "No self-consistent edge topology, SOL transport, detachment or target heat-flux solution is available in this runtime.",
        },
        "G6_RF": {
            "first_harmonic_GHz": ecrh_frequency_ghz(B),
            "nominal_GHz": raw["heating_control"]["nominal_frequency_GHz"],
            "status": "RESONANCE_SCREEN_PASS__DEPOSITION_OPEN",
        },
        "G7_neutronics": {
            "target_neutron_power_MW": dt.neutron_power_MW,
            "target_neutron_source_rate_s": dt.reaction_rate_per_s,
            "TBR_target": raw["blanket_fuel_cycle"]["tbr_design_target"],
            "TBR_net_margin_above_replacement": required_tbr_margin,
            "minimum_target_tritium_production_kg_per_day_at_TBR_target": dt.tritium_burn_kg_per_day * raw["blanket_fuel_cycle"]["tbr_design_target"],
            "status": "SOURCE_TERM_DEFINED__3D_MONTE_CARLO_OPEN",
        },
        "G8_system": {
            "target_power_balance": asdict(target_power),
            "uniform_burn_power_balance": asdict(uniform_power),
            "status": "TARGET_LEDGER_CLOSES__PHYSICS_COUPLED_CLOSURE_OPEN",
        },
        "G9_hardware": {
            "status": "OPEN_REQUIRES_PHYSICAL_HARDWARE",
            "reason": "No computational workflow can demonstrate net-electric fusion or qualify the integrated reactor without hardware.",
        },
        "top_level_verdict": "EXECUTABLE_SFR1_POC_AND_FULL_DESIGN_INVENTORY__HIGH_FIDELITY_G1_G2_G3_G4_G5_G7_NOT_CLOSED",
    }
