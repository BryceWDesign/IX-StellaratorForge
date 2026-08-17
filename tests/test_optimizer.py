from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ix_fusion.config import load_candidate
from ix_fusion.optimizer import objective_terms, optimize_seed, quick_objective


class OptimizerTests(unittest.TestCase):
    def test_terms_sum_to_objective(self) -> None:
        cfg = load_candidate(ROOT / "configs/candidates/c6_seed.json")
        terms = objective_terms(cfg)
        self.assertAlmostEqual(sum(terms.values()), quick_objective(cfg), places=12)

    def test_equal_budget_search_never_returns_worse_seen_start(self) -> None:
        cfg = load_candidate(ROOT / "configs/candidates/c6_seed.json")
        start = quick_objective(cfg)
        result, history = optimize_seed(cfg, passes=1)
        self.assertLessEqual(quick_objective(result), start + 1e-12)
        self.assertGreater(len(history), 1)

    def test_optimizer_deterministic(self) -> None:
        cfg = load_candidate(ROOT / "configs/candidates/c6_seed.json")
        a, _ = optimize_seed(cfg, passes=1)
        b, _ = optimize_seed(cfg, passes=1)
        self.assertEqual(a.to_dict(), b.to_dict())


if __name__ == "__main__":
    unittest.main()
