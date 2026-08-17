from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ix_fusion.config import load_candidate
from ix_fusion.field import field_strength, helical_strength, resonant_overlap_proxy
from ix_fusion.geometry import boundary_points, magnetic_axis, periodicity_error


class GeometryFieldTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cfg = load_candidate(ROOT / "configs/candidates/c6_seed.json")

    def test_axis_is_finite(self) -> None:
        phi = np.linspace(0, 2 * np.pi, 100)
        axis = magnetic_axis(phi, self.cfg)
        self.assertEqual(axis.shape, (100, 3))
        self.assertTrue(np.all(np.isfinite(axis)))

    def test_boundary_is_periodic_by_field_period(self) -> None:
        self.assertLess(periodicity_error(self.cfg), 1e-10)

    def test_boundary_points_shape(self) -> None:
        theta = np.array([0.0, 1.0])
        phi = np.array([0.0, 1.0])
        points = boundary_points(theta, phi, self.cfg)
        self.assertEqual(points.shape, (2, 3))

    def test_field_strength_positive_in_screen(self) -> None:
        theta = np.linspace(0, 2 * np.pi, 60)[:, None]
        phi = np.linspace(0, 2 * np.pi, 80)[None, :]
        b = field_strength(theta, phi, self.cfg)
        self.assertGreater(float(np.min(b)), 0.5)

    def test_helical_strength_matches_declared_target(self) -> None:
        self.assertAlmostEqual(helical_strength(self.cfg), self.cfg.required_helical_strength, places=12)

    def test_resonant_proxy_nonnegative(self) -> None:
        self.assertGreaterEqual(resonant_overlap_proxy(self.cfg), 0.0)


if __name__ == "__main__":
    unittest.main()
