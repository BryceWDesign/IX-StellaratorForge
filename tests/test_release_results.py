from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ix_fusion.evidence import validate_bundle


class ReleaseResultTests(unittest.TestCase):
    def test_committed_verdict_is_not_overclaimed(self) -> None:
        data = json.loads((ROOT / "results/poc/verdict.json").read_text(encoding="utf-8"))
        self.assertEqual(data["scientific_stage"], "geometry_hypothesis")
        self.assertIn(data["reduced_model_verdict"], {"PASS_REDUCED_MODEL", "FAIL_OR_INCONCLUSIVE"})

    def test_current_release_does_not_claim_c6_advantage(self) -> None:
        data = json.loads((ROOT / "results/poc/verdict.json").read_text(encoding="utf-8"))
        self.assertEqual(data["reduced_model_verdict"], "FAIL_OR_INCONCLUSIVE")

    def test_evidence_bundle_valid(self) -> None:
        bundle = json.loads((ROOT / "results/evidence/IXFUSION-POC-001.json").read_text(encoding="utf-8"))
        self.assertEqual(validate_bundle(bundle), [])

    def test_loss_ledger_keeps_net_power_unknown(self) -> None:
        data = json.loads((ROOT / "results/evidence/loss_ledger.json").read_text(encoding="utf-8"))
        self.assertEqual(data["net_electric_power"]["status"], "UNKNOWN")
        self.assertEqual(data["mhd_stability"]["status"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
