from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ix_fusion.rf import actuator_weights, monte_carlo_robustness, rf_metrics


class RFTests(unittest.TestCase):
    def test_ideal_six_source_mode_is_pure(self) -> None:
        metrics = rf_metrics(actuator_weights(6, 1), 1)
        self.assertGreater(metrics.target_mode_purity, 0.999999999)
        self.assertLess(metrics.sideband_power, 1e-12)

    def test_feedback_improves_median_mode_purity(self) -> None:
        result = monte_carlo_robustness(samples=300, seed=123)
        self.assertGreater(result.feedback_purity_median, result.open_loop_purity_median)
        self.assertGreater(result.unwanted_power_reduction_factor, 1.0)

    def test_monte_carlo_reproducible(self) -> None:
        a = monte_carlo_robustness(samples=100, seed=77)
        b = monte_carlo_robustness(samples=100, seed=77)
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
