"""Maximum in-repository computational closure campaign for SFR-1 v0.4.0."""
from __future__ import annotations

from dataclasses import asdict
from math import pi
from pathlib import Path
from typing import Any

from .burn import confinement_requirement, uniform_dt_burn_point
from .closure import solver_availability
from .coil_hybrid import _helical_loop
from .coil_screen import _poloidal_loop
from .current_potential_screen import current_potential_screen
from .equilibrium_inputs import make_seed, seed_json, write_seed_pack
from .hts_screen import screen_curve_geometry
from .neutronics_constraints import coverage_sweep
from .plant_closure import plant_thresholds
from .reactor import ReactorConfig
from .vacuum_codesign import best_architecture, scan_classical_helical_family


def _equilibrium_seeds(config: ReactorConfig):
    env = config.raw["reactor_envelope"]
    mapping = {
        "SFR1_QA_2FP_REF": 2,
        "SFR1_QI_3FP": 3,
        "SFR1_QI_PWO_4FP": 4,
        "SFR1_C6_QI_6FP": 6,
    }
    return [
        make_seed(
            candidate_id=cid,
            nfp=nfp,
            R=float(env["major_radius_m"]),
            a=float(env["minor_radius_m"]),
            field_T=float(env["magnetic_field_axis_T"]),
            beta=float(env["volume_average_beta"]),
            iota_axis=0.50,
            iota_edge=0.60,
        )
        for cid, nfp in mapping.items()
    ]


def run_computational_closure(config: ReactorConfig, *, seed_output_dir: Path | None = None) -> dict[str, Any]:
    raw = config.raw
    env = raw["reactor_envelope"]
    mag = raw["magnet_system"]
    therm = raw["thermal_power_conversion"]
    blanket = raw["blanket_fuel_cycle"]
    R, a, B = map(float, (env["major_radius_m"], env["minor_radius_m"], env["magnetic_field_axis_T"]))
    beta = float(env["volume_average_beta"])
    target = float(env["fusion_power_target_MW"])
    temperature = float(env["screening_temperature_keV"]["ion"])
    volume = 2 * pi**2 * R * a**2

    burn = uniform_dt_burn_point(
        temperature_keV=temperature, beta=beta, field_T=B, volume_m3=volume,
        target_fusion_power_MW=target,
    )
    q10 = confinement_requirement(
        burn=burn, major_radius_m=R, minor_radius_m=a, iota_screen=0.55, plasma_gain_Q=10.0
    )

    # Two genuinely different magnet architecture experiments.
    helical_scan = scan_classical_helical_family(
        R=R, a=a, clearance_m=float(mag["minimum_plasma_to_coil_distance_m_target"]), target_B_T=B
    )
    best = best_architecture(helical_scan)
    current_potential = {
        str(nfp): asdict(current_potential_screen(
            nfp=nfp, R=R, a=a,
            clearance_m=float(mag["minimum_plasma_to_coil_distance_m_target"]), target_B_T=B,
        ))
        for nfp in (2, 3, 4, 6)
    }

    coil_r = a + float(mag["minimum_plasma_to_coil_distance_m_target"])
    tf_curve = _poloidal_loop(0.0, R, coil_r, nseg=240)
    helix_curve = _helical_loop(R, coil_r, best.nfp, 0.0, nseg=720)
    hts_tf = screen_curve_geometry(
        tf_curve,
        strain_target_fraction=float(mag["winding_strain_target_fraction"]),
        strain_ceiling_fraction=float(mag["winding_strain_hard_ceiling_fraction"]),
    )
    hts_helix = screen_curve_geometry(
        helix_curve,
        strain_target_fraction=float(mag["winding_strain_target_fraction"]),
        strain_ceiling_fraction=float(mag["winding_strain_hard_ceiling_fraction"]),
    )

    breeding = coverage_sweep(fusion_power_MW=target, global_tbr_target=float(blanket["tbr_design_target"]))
    plant = plant_thresholds(
        current_fusion_power_MW=burn.fusion_power_MW_uniform,
        target_fusion_power_MW=target,
        current_beta=beta,
        blanket_multiplier=float(therm["blanket_energy_multiplier_screening"]),
        gross_efficiency=float(therm["gross_thermal_to_electric_efficiency_target"]),
        recirc_MW=float(therm["recirculating_power_MW_design_ceiling"]),
        net_floor_MW=float(therm["net_electric_power_MW_design_floor"]),
    )

    seeds = _equilibrium_seeds(config)
    seed_paths: list[str] = []
    if seed_output_dir is not None:
        seed_paths = [str(p) for p in write_seed_pack(seeds, seed_output_dir)]

    solvers = solver_availability()
    any_helical_pass = any(r.combined_screen_pass for r in helical_scan)
    any_cp_pass = any(v["passes_reconstruction_screen"] for v in current_potential.values())
    return {
        "program": "IX-StellaratorForge",
        "campaign": "SFR-1 Maximum Computational Closure v0.4.0",
        "claim_boundary": (
            "This campaign executes analytical and independent reduced/intermediate calculations. "
            "It does not substitute those calculations for DESC/VMEC++ force balance, production "
            "coil optimization/FEA, gyrokinetics/neoclassical transport, OpenMC neutron transport, "
            "or hardware demonstration."
        ),
        "external_solver_availability_in_build_runtime": solvers,
        "G1_equilibrium": {
            "status": "INPUTS_COMPLETE__PRODUCTION_MHD_EXECUTION_OPEN" if not (solvers["desc"] or solvers["vmecpp"]) else "SOLVER_AVAILABLE__EXECUTION_REQUIRED",
            "candidate_inputs": [seed_json(s) for s in seeds],
            "written_input_paths": seed_paths,
            "cross_code_rule": "A candidate cannot be promoted from G1 until a converged finite-beta equilibrium is independently cross-checked by DESC and VMEC++ or an explicitly justified equivalent pair.",
        },
        "G2_magnets": {
            "classical_helical_scan_count": len(helical_scan),
            "classical_helical_best": asdict(best),
            "classical_helical_any_pass": any_helical_pass,
            "current_potential_results": current_potential,
            "current_potential_any_pass": any_cp_pass,
            "hts_geometry_screen_best_helical": asdict(hts_helix),
            "hts_geometry_screen_tf_reference": asdict(hts_tf),
            "status": "NEW_ARCHITECTURES_EXECUTED__NO_COIL_SET_PROMOTED" if not (any_helical_pass or any_cp_pass) else "LOW_AUTHORITY_MAGNET_SCREEN_PASS__PRODUCTION_OPTIMIZATION_OPEN",
            "interpretation": "Field performance and HTS geometry are separate gates. Geometry-only strain proxies cannot qualify REBCO winding packs; percent-level Bn failure prevents promotion regardless of geometric bendability.",
        },
        "G3_G4_confinement": {
            "Q10_requirement": asdict(q10),
            "vacuum_field_line_best": asdict(best),
            "status": "CONFINEMENT_REQUIREMENTS_AND_VACUUM_TOPOLOGY_QUANTIFIED__KINETIC_TRANSPORT_OPEN",
            "required_production_evidence": ["guiding_center_alpha_orbits", "neoclassical_transport_and_bootstrap", "linear_and_nonlinear_gyrokinetics", "profile_transport_iteration"],
        },
        "G7_neutronics": {
            "coverage_constraints": [asdict(x) for x in breeding],
            "status": "SOURCE_AND_COVERAGE_BOUNDS_CLOSED__OPENMC_3D_TRANSPORT_OPEN",
            "interpretation": "The coverage bound is exact under its stated zero-breeding uncovered-area assumption; it is not a TBR prediction.",
        },
        "G8_net_electric": {
            "conditional_thresholds": asdict(plant),
            "status": "CONDITIONAL_PLANT_EQUATIONS_CLOSED__INTEGRATED_PREDICTION_WAITS_ON_G1_TO_G7",
        },
        "G9_hardware": {
            "status": "NOT_COMPUTATIONALLY_RESOLVABLE",
            "reason": "Actual net-electric fusion requires an operating physical device and calibrated measurements.",
        },
        "top_level_verdict": "MAXIMUM_IN_REPO_COMPUTATIONAL_CLOSURE_COMPLETE__PRODUCTION_SOLVER_AND_HARDWARE_GATES_REMAIN",
    }
