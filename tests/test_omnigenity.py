from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ix_fusion.config import load_candidate
from ix_fusion.omnigenity import bounce_action_proxy, omnigenity_metrics


class OmnigenityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cfg = load_candidate(ROOT / "configs/candidates/c6_seed.json")

    def test_action_proxy_shape(self) -> None:
        actions = bounce_action_proxy(
            self.cfg,
            alphas=np.linspace(0, 2 * np.pi, 8, endpoint=False),
            lambdas=np.array([0.92, 0.97]),
            samples=256,
            turns=2,
        )
        self.assertEqual(actions.shape, (2, 8))
        self.assertTrue(np.all(actions >= 0.0))

    def test_metrics_finite(self) -> None:
        m = omnigenity_metrics(self.cfg)
        self.assertTrue(np.isfinite(m.action_variation_mean))
        self.assertGreaterEqual(m.mirror_ratio, 0.0)


if __name__ == "__main__":
    unittest.main()
