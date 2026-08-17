from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ix_fusion.config import load_candidate
from ix_fusion.tracing import poincare_points, trace_field_lines, trace_metrics


class TraceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cfg = load_candidate(ROOT / "configs/candidates/c6_seed.json")

    def test_trace_is_deterministic(self) -> None:
        a = trace_field_lines(self.cfg, turns=2, steps_per_turn=60)
        b = trace_field_lines(self.cfg, turns=2, steps_per_turn=60)
        self.assertTrue(np.array_equal(a["r"], b["r"]))
        self.assertTrue(np.array_equal(a["theta"], b["theta"]))

    def test_trace_metrics_are_bounded(self) -> None:
        metrics = trace_metrics(trace_field_lines(self.cfg, turns=4, steps_per_turn=80))
        self.assertGreaterEqual(metrics.mean_radial_excursion, 0.0)
        self.assertGreaterEqual(metrics.escape_fraction, 0.0)
        self.assertLessEqual(metrics.escape_fraction, 1.0)

    def test_poincare_sampling(self) -> None:
        trace = trace_field_lines(self.cfg, turns=3, steps_per_turn=40)
        r, theta = poincare_points(trace, steps_per_turn=40)
        self.assertEqual(r.shape[0], 4)
        self.assertTrue(np.all((theta >= 0.0) & (theta < 2 * np.pi)))


if __name__ == "__main__":
    unittest.main()
