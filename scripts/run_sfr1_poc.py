from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ix_stellaratorforge.poc import run_sfr1_poc
from ix_stellaratorforge.reactor import load_reactor_config


def render_markdown(data: dict) -> str:
    burn = data["burn_screen"]
    pwr = data["power_balance"]
    coils = data["held_out_coil_reconstruction"]["results"]
    lines = [
        "# SFR-1 Executable Proof of Concept — v0.4.0",
        "",
        f"**Verdict:** `{data['verdict']}`",
        "",
        "This PoC demonstrates an executable, falsifiable reactor-design screening pipeline. It does **not** demonstrate a fusion reactor.",
        "",
        "## Reproduced screening results",
        "",
        f"- Uniform D-T burn screen: **{burn['fusion_power_MW_uniform']:.2f} MW** vs **{burn['target_fusion_power_MW']:.0f} MW** design target.",
        f"- Uniform-model beta required for the 1 GW target: **{100*burn['uniform_beta_needed_for_1GW_target']:.3f}%**.",
        f"- Design-target power ledger: **{pwr['design_target']['net_electric_MW_at_recirc_ceiling']:.2f} MWe** at the declared screening assumptions.",
        f"- Current uniform-burn screen power ledger: **{pwr['uniform_burn_screen']['net_electric_MW_at_recirc_ceiling']:.2f} MWe**.",
        f"- Electron-cyclotron fundamental at 6 T: **{data['rf_screen']['fundamental_electron_cyclotron_GHz']:.2f} GHz**.",
        "",
        "## Held-out filament-coil reconstruction",
        "",
        "The richer fixed coil basis is solved on one surface grid and evaluated on an unseen, angularly offset grid.",
        "",
        "| NFP | coils | validation RMS | validation mean | max | screen pass |",
        "|---:|---:|---:|---:|---:|:---:|",
    ]
    for nfp in (2, 3, 4, 6):
        c = coils[str(nfp)]
        lines.append(
            f"| {nfp} | {c['coil_count']} | {c['validation_rms_Bn_over_B']:.5f} | "
            f"{c['validation_mean_abs_Bn_over_B']:.5f} | {c['validation_max_abs_Bn_over_B']:.5f} | "
            f"{'PASS' if c['passes_reconstruction_screen'] else 'FAIL'} |"
        )
    lines += [
        "",
        "The fixed-basis coil test remains a **negative result**. It does not justify promoting any core; single-stage plasma/coil optimization remains mandatory.",
        "",
        "## High-authority gates still open",
        "",
        "- finite-beta 3-D MHD equilibrium (DESC + VMEC++ cross-check)",
        "- neoclassical / energetic-particle / nonlinear gyrokinetic confinement",
        "- structural and REBCO-qualified magnet design",
        "- 3-D edge/divertor solution",
        "- full-wave/ray deposition validation for RF",
        "- OpenMC/DAGMC blanket, shielding and TBR transport",
        "- integrated experimental/hardware validation",
        "",
        "See `docs/closure/07_PRODUCTION_SOLVER_HANDOFF.md` for the exact promotion evidence expected from those tools.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    config = load_reactor_config(ROOT / "configs/reactor/sfr1_rev_a.json")
    data = run_sfr1_poc(config)
    out_dir = ROOT / "results" / "sfr1_poc"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "sfr1_poc_v040.json").write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out_dir / "SFR1_POC_RESULT.md").write_text(render_markdown(data), encoding="utf-8")
    print(json.dumps({"verdict": data["verdict"], "output": str(out_dir)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
