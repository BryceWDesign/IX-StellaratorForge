from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ix_fusion.ablations import build_ablations
from ix_fusion.config import load_candidate
from ix_fusion.sensitivity import geometry_error_monte_carlo


class SensitivityAblationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cfg = load_candidate(ROOT / "configs/candidates/c6_seed.json")

    def test_ablation_names_are_explicit(self) -> None:
        variants = build_ablations(self.cfg)
        self.assertIn("no_axis_helical_shaping", variants)
        self.assertIn("small_c3_correction", variants)
        self.assertIn("small_c9_correction", variants)

    def test_small_monte_carlo_reproducible(self) -> None:
        a = geometry_error_monte_carlo(self.cfg, samples=8, seed=9)
        b = geometry_error_monte_carlo(self.cfg, samples=8, seed=9)
        self.assertEqual(a, b)
        self.assertGreaterEqual(a["p95_degradation_ratio"], 0.0)


if __name__ == "__main__":
    unittest.main()
