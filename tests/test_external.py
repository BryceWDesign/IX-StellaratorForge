from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ix_fusion.external import detect_external_solvers


class ExternalSolverTests(unittest.TestCase):
    def test_solver_detection_returns_known_interfaces(self) -> None:
        statuses = {s.name: s for s in detect_external_solvers()}
        self.assertEqual(set(statuses), {"DESC", "SIMSOPT", "VMEC"})
        for status in statuses.values():
            self.assertIsInstance(status.available, bool)
            self.assertTrue(status.purpose)


if __name__ == "__main__":
    unittest.main()
