#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ix_stellaratorforge.sfr3_dual_boundary import run_dual_boundary_screen


def main() -> int:
    raw = json.loads(
        (ROOT / "configs/reactor/sfr3_dual_boundary_ahis_a.json").read_text(
            encoding="utf-8"
        )
    )
    sfr3_raw = json.loads(
        (ROOT / "configs/reactor/sfr3_field_integrity_shell_a.json").read_text(
            encoding="utf-8"
        )
    )
    result = run_dual_boundary_screen(raw, sfr3_raw)
    out_dir = ROOT / "results/sfr3_dual_boundary"
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "sfr3_dual_boundary_ahis_a_v080.json"
    md_path = out_dir / "SFR3_DUAL_BOUNDARY_AHIS_A_RESULT.md"
    json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    stack = next(
        item for item in result["wall_stack_results"] if item["id"] == result["selected_stack_id"]
    )
    monitoring = result["monitoring_inventory"]
    faults = {scenario["id"]: scenario for scenario in result["fault_scenarios"]}
    lines = [
        "# SFR-3 Dual Boundary AHIS A, v0.8.0 result",
        "",
        "## Verdict",
        "",
        f"`{result['top_level_verdict']}`",
        "",
        "The requested inside/outside AHIS concept is retained as two monitored engineering boundaries. It does not mechanically push plasma inward and earns zero confinement, fusion, ignition or safety-qualification credit.",
        "",
        "## Selected reduced-screen stack",
        "",
        f"`{stack['name']}`",
        "",
        f"The 1-D nominal screen predicts a plasma-facing surface temperature of **{stack['nominal']['plasma_facing_surface_temperature_C']:.1f} C** at 0.25 MW/m2.",
        f"The deliberately steady upset upper bound predicts **{stack['upset_steady_upper_bound']['plasma_facing_surface_temperature_C']:.1f} C** at 1.0 MW/m2. This is not a disruption or lifetime result.",
        f"The raw CTE-mismatch strain proxy is **{stack['upset_steady_upper_bound']['raw_cte_mismatch_strain_proxy']:.4%}**; real interface stress requires nonlinear FEA and irradiation data.",
        "",
        "## Monitoring configuration",
        "",
        f"- 24 toroidal sectors aligned to the 24 SFR-3 trim channels.",
        f"- 192 paired inner/outer poloidal monitoring locations.",
        f"- Two independent sensing lanes.",
        f"- {monitoring['total_declared_sensing_elements']} total declared sensing elements, including independent hard-vacuum channels.",
        "",
        "## Fault findings",
        "",
        "- A hotspot and coolant leak remain detectable after the declared single-channel failures.",
        "- Loss of one inner or outer lane enters degraded monitoring, not a false nominal state.",
        "- Loss of both sector buses, vacuum breach or total control power enters safe hold.",
        f"- Outer support movement can request the existing SFR-3 synthetic trim response of **{faults['outer_support_shift']['sfr3_field_integrity_link']['synthetic_rms_reduction_fraction']:.2%}**, but physical confinement credit remains zero.",
        "- A silent armor crack below sensor sensitivity is deliberately not claimed as detected; periodic NDE remains mandatory.",
        "",
        "## Decision",
        "",
        "The dual-boundary arrangement helps safety observability, leak isolation, wall protection and magnetic alignment management. It does not change the repository's earned ignition proxy. Promote only after coupled thermal/CFD/FEA, fracture and irradiation lifetime, sensor qualification, 3-D magnetics, full neutronics and an instrumented sector prototype.",
        "",
    ]
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(json_path.relative_to(ROOT))
    print(md_path.relative_to(ROOT))
    print(result["top_level_verdict"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
