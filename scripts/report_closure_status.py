from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "results" / "closure" / "sfr1_v030_closure_campaign.json"

def main() -> int:
    r = json.loads(P.read_text(encoding="utf-8"))
    print("IX-STELLARATORFORGE SFR-1 CLOSURE STATUS")
    print("verdict:", r["top_level_verdict"])
    b = r["burn_scoping"]
    print(f"uniform D-T burn screen: {b['fusion_power_MW_uniform']:.3f} MW")
    print(f"uniform beta required for 1 GW at fixed B/T/V: {100*b['uniform_model_beta_required_for_target']:.3f}%")
    q = r["G3_G4_confinement_scoping"]["Q10"]
    print(f"Q=10 tau_E requirement: {q['required_tau_E_s']:.3f} s; H_ISS04 screen: {q['required_H_ISS04']:.3f}")
    print("G1:", r["G1_equilibrium"]["status"])
    print("G2:", r["G2_coil_diagnostic"]["status"])
    print("G7:", r["G7_neutronics"]["status"])
    print("G8:", r["G8_system"]["status"])
    print("G9:", r["G9_hardware"]["status"])
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
