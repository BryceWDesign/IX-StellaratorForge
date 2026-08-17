from __future__ import annotations

import sys
import unittest
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ix_fusion.config import load_candidate


class ConfigTests(unittest.TestCase):
    def test_candidate_loads_and_validates(self) -> None:
        cfg = load_candidate(ROOT / "configs/candidates/c6_seed.json")
        self.assertEqual(cfg.nfp, 6)
        self.assertEqual(cfg.role, "candidate")
        self.assertEqual(len(cfg.harmonics), 3)

    def test_matched_baseline_loads(self) -> None:
        cfg = load_candidate(ROOT / "configs/baselines/matched_helical_5fp.json")
        self.assertEqual(cfg.nfp, 5)
        self.assertEqual(cfg.role, "matched_baseline")

    def test_invalid_geometry_rejected(self) -> None:
        cfg = load_candidate(ROOT / "configs/candidates/c6_seed.json")
        bad = replace(cfg, major_radius=0.5, minor_radius=0.9)
        with self.assertRaises(ValueError):
            bad.validate()

    def test_overlarge_harmonic_rejected(self) -> None:
        cfg = load_candidate(ROOT / "configs/candidates/c6_seed.json")
        h = replace(cfg.harmonics[0], amplitude=0.5)
        bad = replace(cfg, harmonics=(h,) + cfg.harmonics[1:])
        with self.assertRaises(ValueError):
            bad.validate()


if __name__ == "__main__":
    unittest.main()
