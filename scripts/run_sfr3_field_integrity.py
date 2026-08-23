#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ix_stellaratorforge.sfr3_field_integrity import run_sfr3_field_integrity_screen


def main() -> int:
    config_path = ROOT / "configs/reactor/sfr3_field_integrity_shell_a.json"
    result = run_sfr3_field_integrity_screen(
        json.loads(config_path.read_text(encoding="utf-8"))
    )
    out_dir = ROOT / "results/sfr3_field_integrity"
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "sfr3_field_integrity_shell_a_v070.json"
    md_path = out_dir / "SFR3_FIELD_INTEGRITY_SHELL_A_RESULT.md"
    json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    by_id = {scenario["id"]: scenario for scenario in result["scenarios"]}
    nominal = by_id["nominal"]
    failed = by_id["single_actuator_unavailable"]
    passive = by_id["passive_transient_only"]
    lines = [
        "# SFR-3 Field Integrity Shell A, v0.7.0 result",
        "",
        "## Verdict",
        "",
        f"`{result['top_level_verdict']}`",
        "",
        "This is a deterministic low-authority harmonic controllability screen. It does not solve physical coils, equilibrium, islands, or plasma confinement, and it earns zero fusion or ignition credit.",
        "",
        "## What passed",
        "",
        f"- Nominal synthetic RMS field-error reduction: **{nominal['total_rms_reduction_fraction']:.2%}**.",
        f"- Single-actuator-unavailable reduction: **{failed['total_rms_reduction_fraction']:.2%}**.",
        f"- Passive-only transient attenuation: **{passive['passive_only_rms_reduction_fraction']:.2%}**; passive loops receive no DC correction credit.",
        "- Low sensor confidence commands passive-only safe hold rather than active correction.",
        "- A passive-loop quench removes passive credit while leaving the independently gated active layer bounded.",
        "- An active-coil quench or exhausted thermal margin blocks powered correction and retains only healthy passive response.",
        "",
        "## What did not pass",
        "",
        "Biot-Savart coil response, free-boundary equilibrium, magnetic-island suppression, particle and alpha confinement, finite-beta transport/MHD, coil stress and quench, 3-D neutronics/TBR, integrated burn, net electricity and hardware are all unexecuted.",
        "",
        "## Decision",
        "",
        "Retain Field Integrity Shell A as the leading new confinement-support architecture. Promote it only after the analytic response matrix is replaced by physical coil/equilibrium evidence. It currently improves the repo's testability and fault tolerance, not its earned distance to fusion.",
        "",
    ]
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(json_path.relative_to(ROOT))
    print(md_path.relative_to(ROOT))
    print(result["top_level_verdict"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
