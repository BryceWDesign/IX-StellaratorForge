#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ix_stellaratorforge.sfr2_actuation import run_actuation_overlay_screen


def main() -> int:
    config_path = ROOT / "configs" / "reactor" / "sfr2_actuation_overlay_a.json"
    result = run_actuation_overlay_screen(json.loads(config_path.read_text(encoding="utf-8")))
    out_dir = ROOT / "results" / "sfr2_actuation"
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "sfr2_actuation_overlay_a_v060.json"
    md_path = out_dir / "SFR2_ACTUATION_OVERLAY_A_RESULT.md"
    json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    baseline = result["baseline"]
    breathing = result["breathing_result"]
    closest = breathing["closest_cycle_average_case"]
    instant = breathing["closest_instantaneous_case"]
    image = result["concept_image_result"]
    lines = [
        "# SFR-2 Actuation Overlay A, v0.6.0 result",
        "",
        "## Verdict",
        "",
        f"`{breathing['verdict']}`",
        "",
        "This is a low-authority analytical and empirical falsification screen. It is not a dynamic equilibrium, magnetic-pumping, ignition, sustained-burn, net-energy or hardware result.",
        "",
        "## Preserved baseline",
        "",
        "The SFR-2 Rev A 23 / 26 / 23 / 26 ft ABAB geometry, rigid vessel and steady primary HTS field remain unchanged.",
        f"The baseline H_ISS04=1 optimistic ignition ratio is **{baseline['optimistic_ignition_tau_ratio']:.9f}**, a ratio gap of **{abs(baseline['distance_from_ratio_one_fraction']):.4%}**. This is not a percentage distance from physical ignition.",
        f"The target-matched uniform fusion screen is **{baseline['fusion_power_MW_uniform']:.3f} MW**.",
        "",
        "## Timed squeeze and expansion test",
        "",
        f"The closest cycle-average case is `{closest['pattern']}` at {closest['depth_fraction']:.2%} depth.",
        f"Its cycle-average optimistic ignition ratio is **{closest['cycle_average']['optimistic_ignition_tau_ratio']:.9f}** and its cycle-average uniform fusion power is **{closest['cycle_average']['fusion_power_MW_uniform']:.3f} MW**.",
        f"Joint average improvement over the unchanged baseline: **{closest['screen_decision']['joint_average_improvement']}**.",
        f"No declared case crosses the cycle-average proxy: **{not breathing['any_cycle_average_proxy_pass']}**.",
        "",
        "The closest instantaneous point occurs in "
        f"`{instant['pattern']}` at {instant['depth_fraction']:.2%} depth and reaches "
        f"**{instant['full_cycle']['maximum_optimistic_ignition_tau_ratio']:.9f}**. "
        f"That point is a {abs(instant['closest_instantaneous_proxy_point']['equivalent_radial_squeeze_fraction']):.2%} expansion, not a squeeze, with uniform fusion power reduced to "
        f"**{instant['closest_instantaneous_proxy_point']['fusion_power_MW_uniform']:.3f} MW**. "
        "It is not credited as ignition capture or sustained burn, and actuator power is not yet debited.",
        "",
        "## Trinity image translation",
        "",
        f"`{image['verdict']}`",
        "",
        "The astrophysical accretion, gravity, shock-front and multiple-star claims are not imported into reactor physics. D-T fusion is treated as a binary reaction, so a three-point collision receives zero fusion credit.",
        "A global three-toroidal-lobe pattern conflicts with the unchanged four-field-period baseline. The defensible translation is an area-preserving poloidal m=3 actuator harmonic repeated inside every one of the four ABAB periods.",
        "Because the tri-lobe harmonic is normalized to preserve cross-sectional area, reshaping alone produces no density, temperature, fusion-power or ignition-proxy gain in this screen.",
        "",
        "## Decision",
        "",
        "Do not promote magnetic breathing or the tri-lobe image geometry as a closer-to-fusion result. Retain them as an optional actuator hypothesis for high-authority equilibrium, topology, kinetic, alpha-orbit, electromagnetic and integrated-power testing.",
        "",
    ]
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(json_path.relative_to(ROOT))
    print(md_path.relative_to(ROOT))
    print(breathing["verdict"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
