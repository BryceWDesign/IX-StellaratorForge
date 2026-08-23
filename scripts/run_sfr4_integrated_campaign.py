#!/usr/bin/env python3
"""Run and persist the SFR-4 v0.9 integrated physical-promotion campaign."""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ix_stellaratorforge.sfr4_integrated_campaign import run_integrated_campaign


def _summary(result: dict) -> str:
    coil = result["workstreams"]["1_physical_coil_field"]
    best = coil["best_candidate"]
    particles = result["workstreams"]["4_particle_confinement"]
    burn = result["workstreams"]["5_self_consistent_burn"]
    heat = result["heat_exhaust_resolution"]
    hydraulics = heat["divertor_hydraulics"]
    systems = result["workstreams"]["7_reactor_systems"]
    available = [name for name, value in result["solver_availability"].items() if value]
    unavailable = [name for name, value in result["solver_availability"].items() if not value]
    lines = [
        "# SFR-4 Integrated Physical-Promotion Campaign A",
        "",
        f"Verdict: `{result['top_level_verdict']}`",
        "",
        "## Seven-workstream result",
        "",
        f"1. Physical coil field: {coil['candidate_count']} direct-filament candidates executed; {coil['combined_pass_count']} passes. Best reduced candidate has mean iota {best['mean_iota']:.6f} and normalized maximum radial excursion {best['normalized_max_excursion_over_a']:.6f}. No coil is promoted.",
        f"2. Finite-beta equilibrium: not run. Available production tools: {', '.join(available) if available else 'none'}. Unavailable: {', '.join(unavailable)}.",
        "3. Coil/plasma co-design: reduced geometry/current scan executed; production single-stage co-design not run.",
        f"4. Particle confinement: 3.5 MeV alpha gyroradius scope is {particles['maximum_pitch_alpha_gyroradius_m']:.6f} m, but no guiding-center retention is credited because the topology prerequisite fails.",
        f"5. Burn: design-iota Q=20 screen requires H_ISS04 {burn['required_H_ISS04_with_bremsstrahlung_at_design_iota']:.6f} after the declared bremsstrahlung and alpha-deposition assumptions. It is not linked to a passing physical coil.",
        "6. Magnet engineering: magnetic-pressure, stored-energy and centerline geometry scopes executed; peak conductor field, winding-pack FEA and quench qualification remain open.",
        f"7. Reactor systems: exact D-T source and breeding-coverage constraints plus conditional plant ledger executed. Conditional net electric algebra is {systems['conditional_net_electric_MW']:.3f} MWe, with no prediction credit.",
        "",
        "## Heat result",
        "",
        f"Plasma exhaust in the declared Q=20 target ledger: **{heat['plasma_exhaust_power_MW']:.3f} MW**.",
        f"Controlled radiation requirement: **{heat['controlled_radiation_MW']:.3f} MW**, producing a first-wall peak screen of **{heat['first_wall_peak_heat_flux_MW_m2']:.3f} MW/m2**.",
        f"Divertor power: **{heat['divertor_power_MW']:.3f} MW**, producing a selected peak screen of **{heat['divertor_peak_heat_flux_MW_m2']:.3f} MW/m2** over 24 m2 effective wetted area.",
        f"Divertor tungsten surface screen: **{heat['divertor_thermal_screen']['surface_temperature_C']:.1f} C**.",
        f"First-wall surface screen: **{heat['selected_first_wall_screen']['nominal']['plasma_facing_surface_temperature_C']:.1f} C nominal**, **{heat['selected_first_wall_screen']['upset_steady_upper_bound']['plasma_facing_surface_temperature_C']:.1f} C at the declared 1 MW/m2 steady upper bound**.",
        f"Water-loop screen: **{hydraulics['mass_flow_kg_s']:.1f} kg/s**, **{hydraulics['mean_channel_velocity_m_s']:.2f} m/s**, **{hydraulics['pumping_power_MW_screen']:.3f} MW** across 960 parallel channels.",
        f"Selected heat-flux envelope pass: **{heat['nominal_and_declared_steady_heat_envelope_pass']}**.",
        "",
        "The heat result is a requirement-level resolution for nominal and declared steady conditions. Stable detachment, 3-D island footprints, critical heat flux, erosion, cyclic fatigue, disruptions, coolant accidents and component qualification remain unproven.",
        "",
        "## Scientific boundary",
        "",
        "Earned fusion-progress credit remains exactly **0.0** because no physical coil passes, no finite-beta equilibrium is solved, and no particle/transport or sustained-burn calculation is promoted.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    config_path = ROOT / "configs/reactor/sfr4_integrated_physical_promotion_a.json"
    raw = json.loads(config_path.read_text(encoding="utf-8"))
    result = run_integrated_campaign(raw)
    out = ROOT / "results/sfr4_integrated"
    out.mkdir(parents=True, exist_ok=True)
    (out / "sfr4_integrated_physical_promotion_a_v090.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (out / "SFR4_INTEGRATED_PHYSICAL_PROMOTION_A_RESULT.md").write_text(
        _summary(result), encoding="utf-8"
    )
    print(json.dumps({
        "verdict": result["top_level_verdict"],
        "output": str(out),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
