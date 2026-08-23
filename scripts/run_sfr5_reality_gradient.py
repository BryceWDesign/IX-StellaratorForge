from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ix_stellaratorforge.sfr5_inverse_design import render_result_markdown, run_sfr5_campaign


def main() -> int:
    raw = json.loads((ROOT / "configs/reactor/sfr5_reality_gradient_a.json").read_text(encoding="utf-8"))
    sfr4_result = json.loads((ROOT / raw["source_artifacts"]["sfr4_result"]).read_text(encoding="utf-8"))
    sfr4_config = json.loads((ROOT / raw["source_artifacts"]["sfr4_config"]).read_text(encoding="utf-8"))
    result = run_sfr5_campaign(raw, sfr4_result, sfr4_config)

    result_dir = ROOT / "results/sfr5"
    result_dir.mkdir(parents=True, exist_ok=True)
    json_path = result_dir / "sfr5_reality_gradient_a_v0100.json"
    md_path = result_dir / "SFR5_REALITY_GRADIENT_A_RESULT.md"
    json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    md_path.write_text(render_result_markdown(result), encoding="utf-8", newline="\n")

    diag = result["magnetic_autopsy"]["diagnostics"]
    print("SFR-5 REALITY GRADIENT A")
    print(f"verdict: {result['top_level_verdict']}")
    print(f"SFR-4 candidate count: {int(diag['sfr4_candidate_count'])}")
    print(f"SFR-4 combined passes: {int(diag['sfr4_combined_pass_count'])}")
    print(f"iota factor to minimum gate: {diag['iota_factor_to_minimum_gate']:.6f}x")
    print(f"excursion slack: {100.0 * diag['excursion_slack_fraction_of_limit']:.6f}%")
    print(f"held-out Bn/B factor over limit: {diag['normal_field_factor_over_limit']:.6f}x")
    print(f"decision: {result['magnetic_autopsy']['decision']}")
    print(f"wrote: {json_path.relative_to(ROOT)}")
    print(f"wrote: {md_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
