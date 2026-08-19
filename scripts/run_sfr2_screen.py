#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ix_stellaratorforge.sfr2 import run_sfr2_screen


def main() -> int:
    config_path = ROOT / "configs" / "reactor" / "sfr2_rev_a.json"
    raw = json.loads(config_path.read_text(encoding="utf-8"))
    result = run_sfr2_screen(raw)

    out_dir = ROOT / "results" / "sfr2"
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "sfr2_rev_a_screen_v050.json"
    md_path = out_dir / "SFR2_REVA_SCREEN_RESULT.md"
    json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    primary = result["primary_screen"]
    best = primary["best_case"]
    dyn = primary["best_dynamic_compression_case"]
    sens = result["favorable_sensitivity_only"]["best_case"]
    g = result["geometry"]
    lines = [
        "# SFR-2 Rev A — v0.5.0 low-authority screening result",
        "",
        "## Verdict",
        "",
        f"`{primary['verdict']}`",
        "",
        "This result is **not evidence of ignition or achieved fusion hardware**. It is an analytical/empirical screening artifact.",
        "",
        "## Geometry bookkeeping",
        "",
        f"- Sector sequence: `{result['candidate']}` uses 23 / 26 / 23 / 26 ft as four consecutive sectors of **one closed toroidal plasma system**.",
        f"- Total axis-path proxy: {g['total_axis_path_m']:.6f} m.",
        f"- Equivalent circular major radius: {g['equivalent_major_radius_m']:.6f} m.",
        f"- Screening aspect ratio: {g['screening_aspect_ratio']:.3f}.",
        f"- Screening minor radius: {g['screening_minor_radius_m']:.6f} m.",
        "- The ABAB staggering receives **zero confinement credit** in this model.",
        "",
        "## Primary screen — H_ISS04 = 1.0, no assumed transient confinement penalty",
        "",
        f"- Best primary case: B_axis={best['axis_field_T']:.1f} T, iota(2/3)={best['iota_2over3']:.2f}, radial squeeze={best['radial_squeeze_fraction']:.2%}.",
        f"- Optimistic ignition-proxy tau ratio: **{best['ignition']['tau_ratio_to_optimistic_ignition']:.6f}**.",
        f"- Required H_ISS04 at unit retention: **{best['ignition']['required_H_if_retention_is_one']:.6f}**.",
        f"- Uniform target-power-matched fusion screen: {best['state']['fusion_power_MW_uniform']:.3f} MW.",
        f"- Circular neutron wall-load proxy: {best['state']['neutron_wall_load_MW_m2_circular_proxy']:.3f} MW/m².",
        "",
        "## Dynamic-compression check",
        "",
        f"- Best H=1 dynamic case: B_axis={dyn['axis_field_T']:.1f} T, iota(2/3)={dyn['iota_2over3']:.2f}, squeeze={dyn['radial_squeeze_fraction']:.2%}.",
        f"- Optimistic ignition-proxy tau ratio: **{dyn['ignition']['tau_ratio_to_optimistic_ignition']:.6f}**.",
        "- In the target-power-matched ISS04 screen, compression does **not** automatically improve the ignition proxy; shrinking the minor radius penalizes empirical confinement. This is a useful negative result, not a failed repository run.",
        "- No RF resonance, magnetic pumping, traveling-wave phase gain, or flux-compression field amplification is numerically credited.",
        "",
        "## Favorable sensitivity only — not earned performance",
        "",
        f"- Best declared sensitivity case: H_ISS04={sens['H_ISS04']:.1f}, B_axis={sens['axis_field_T']:.1f} T, iota(2/3)={sens['iota_2over3']:.2f}, squeeze={sens['radial_squeeze_fraction']:.2%}, retention={sens['transient_confinement_retention']:.2f}.",
        f"- Tau ratio: {sens['ignition']['tau_ratio_to_optimistic_ignition']:.6f}.",
        "- H>1 and retention values are scenario variables. SFR-2 has not earned them from equilibrium/transport evidence.",
        "",
        "## What changed relative to the conversational exploration",
        "",
        "Earlier chat percentages were heuristic and are **not retained as repository evidence**. The v0.5.0 implementation recalculates the candidate from explicit equations and exposes an important correction: once fusion power is normalized to the same 1 GW target, ideal radial compression can worsen the ISS04 ignition proxy even while increasing density and temperature. The repository result supersedes those exploratory percentages.",
        "",
        "## Authority boundary",
        "",
        "A low-authority pass may justify more computation; it may not declare ignition. A low-authority failure may reject a candidate. Dynamic finite-beta equilibrium, islands/stochasticity, MHD, kinetic transport, alpha orbits, RF deposition, real coils, transient heat flux, neutronics and hardware remain open.",
        "",
    ]
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(json_path.relative_to(ROOT))
    print(md_path.relative_to(ROOT))
    print(primary["verdict"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
