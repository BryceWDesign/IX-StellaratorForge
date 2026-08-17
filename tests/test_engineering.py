from __future__ import annotations

import sys
import unittest
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ix_fusion.config import load_candidate
from ix_fusion.cryogenics import cryogenic_burden_proxy
from ix_fusion.engineering import engineering_metrics
from ix_fusion.shielding import blanket_space_proxy
from ix_fusion.structural import structural_metrics
from ix_fusion.thermal import heat_spreading_proxy


class EngineeringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cfg = load_candidate(ROOT / "configs/candidates/c6_seed.json")

    def test_structural_metrics_positive(self) -> None:
        m = structural_metrics(self.cfg, samples=240)
        self.assertGreater(m.axis_curvature_rms, 0.0)
        self.assertGreater(m.normalized_support_burden, 0.0)

    def test_blanket_space_increases_with_major_radius(self) -> None:
        larger = replace(self.cfg, major_radius=7.0)
        self.assertGreater(blanket_space_proxy(larger), blanket_space_proxy(self.cfg))

    def test_heat_proxy_is_bounded(self) -> None:
        value = heat_spreading_proxy(self.cfg)
        self.assertGreater(value, 0.0)
        self.assertLessEqual(value, 1.0)

    def test_cryo_burden_positive(self) -> None:
        self.assertGreater(cryogenic_burden_proxy(self.cfg), 0.0)

    def test_composite_engineering_metrics_finite(self) -> None:
        m = engineering_metrics(self.cfg)
        self.assertGreater(m.engineering_burden_score, 0.0)


if __name__ == "__main__":
    unittest.main()
