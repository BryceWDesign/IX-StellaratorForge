from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "reproduce_release.py"
spec = importlib.util.spec_from_file_location("ixfusion_reproduce_release", SCRIPT)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ReproductionToleranceTests(unittest.TestCase):
    def test_tiny_cross_platform_float_noise_is_accepted(self) -> None:
        expected = {"metric": 0.123456789012345, "nested": [1.0, 2.0]}
        actual = {"metric": 0.123456789012346, "nested": [1.0 + 1e-13, 2.0]}
        self.assertEqual(module._json_mismatches(expected, actual), [])

    def test_scientifically_meaningful_numeric_change_is_rejected(self) -> None:
        expected = {"metric": 0.123456789}
        actual = {"metric": 0.123466789}
        mismatches = module._json_mismatches(expected, actual)
        self.assertTrue(mismatches)
        self.assertIn("$.metric", mismatches[0])

    def test_structure_and_non_numeric_values_remain_exact(self) -> None:
        self.assertTrue(module._json_mismatches({"status": "PASS"}, {"status": "FAIL"}))
        self.assertTrue(module._json_mismatches({"a": 1}, {"a": 1, "b": 2}))
        self.assertTrue(module._json_mismatches({"flag": True}, {"flag": False}))


if __name__ == "__main__":
    unittest.main()
