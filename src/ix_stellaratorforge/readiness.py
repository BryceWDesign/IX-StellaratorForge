
"""Machine-readable reactor readiness reporting."""
from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
from typing import Any

from .physics import dt_reaction_ledger, ecrh_frequency_ghz, plasma_screening_ledger, power_balance
from .closure import run_closure_campaign
from .reactor import ReactorConfig, validate_reactor_config


def build_readiness_report(config: ReactorConfig) -> dict[str, Any]:
    raw = config.raw
    env = raw["reactor_envelope"]
    thermal = raw["thermal_power_conversion"]
    validation = validate_reactor_config(config)
    dt = dt_reaction_ledger(env["fusion_power_target_MW"])
    power = power_balance(
        env["fusion_power_target_MW"],
        thermal["blanket_energy_multiplier_screening"],
        thermal["gross_thermal_to_electric_efficiency_target"],
        thermal["recirculating_power_MW_design_ceiling"],
    )
    plasma = plasma_screening_ledger(
        env["major_radius_m"],
        env["minor_radius_m"],
        env["magnetic_field_axis_T"],
        env["volume_average_beta"],
        env["fusion_power_target_MW"],
        env["screening_temperature_keV"]["electron"],
        env["screening_temperature_keV"]["ion"],
    )
    closure = run_closure_campaign(config)
    tracked_v04 = None
    tracked_path = Path(__file__).resolve().parents[2] / "results/computational_closure/sfr1_v040.json"
    if tracked_path.exists():
        try:
            tracked_v04 = json.loads(tracked_path.read_text(encoding="utf-8"))
        except Exception:
            tracked_v04 = None
    report = {
        "design_id": config.design_id,
        "maturity": raw["maturity"],
        "architecture_validation": {
            "passed": validation.passed,
            "errors": list(validation.errors),
            "warnings": list(validation.warnings),
        },
        "core_selection": {
            "selected": raw["core_policy"]["selected_core"],
            "competitors": [x["id"] for x in raw["core_policy"]["competitors"]],
            "statement": "No core has earned selection. 3FP/4FP/6FP QI-family candidates compete with a QA reference and direct-J search branch."
        },
        "derived_screening": {
            "dt_reaction_ledger": asdict(dt),
            "power_balance": asdict(power),
            "plasma_envelope": asdict(plasma),
            "ecrh_first_harmonic_GHz_at_axis_field": ecrh_frequency_ghz(env["magnetic_field_axis_T"]),
        },
        "promotion_status": raw["promotion_status"],
        "closure_campaign_v0_3": {
            "verdict": closure["top_level_verdict"],
            "G1": closure["G1_equilibrium"]["status"],
            "G2": closure["G2_coil_diagnostic"]["status"],
            "G3_G4": closure["G3_G4_confinement_scoping"]["status"],
            "G5": closure["G5_exhaust"]["status"],
            "G6": closure["G6_RF"]["status"],
            "G7": closure["G7_neutronics"]["status"],
            "G8": closure["G8_system"]["status"],
            "G9": closure["G9_hardware"]["status"],
        },
        # Compatibility alias retained so v0.2 readers/tests do not silently lose the closure block.
        "closure_campaign_v0_2": {
            "verdict": closure["top_level_verdict"],
            "G1": closure["G1_equilibrium"]["status"],
            "G2": closure["G2_coil_diagnostic"]["status"],
            "G3_G4": closure["G3_G4_confinement_scoping"]["status"],
            "G5": closure["G5_exhaust"]["status"],
            "G6": closure["G6_RF"]["status"],
            "G7": closure["G7_neutronics"]["status"],
            "G8": closure["G8_system"]["status"],
            "G9": closure["G9_hardware"]["status"],
        },
        "current_verdict": closure["top_level_verdict"],
        "what_green_means": "Repository and reference-design invariants reproduce. It does not mean SFR-1 produces fusion or net electricity."
    }
    if tracked_v04 is not None:
        report["maximum_computational_closure_v0_4"] = {
            "verdict": tracked_v04["top_level_verdict"],
            "G1": tracked_v04["G1_equilibrium"]["status"],
            "G2": tracked_v04["G2_magnets"]["status"],
            "G3_G4": tracked_v04["G3_G4_confinement"]["status"],
            "G7": tracked_v04["G7_neutronics"]["status"],
            "G8": tracked_v04["G8_net_electric"]["status"],
            "G9": tracked_v04["G9_hardware"]["status"],
        }
        report["maximum_computational_closure_v0_4"]["authority_note"] = "Supplemental in-repo closure layer; formal G1-G9 promotion_status remains unchanged until production evidence is committed."
    return report
