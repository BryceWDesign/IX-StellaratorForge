from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ix_fusion.evidence import evidence_bundle, sha256_file, validate_bundle, write_json


class EvidenceTests(unittest.TestCase):
    def test_hash_stable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "x.txt"
            p.write_text("abc\n", encoding="utf-8")
            self.assertEqual(sha256_file(p), sha256_file(p))

    def test_bundle_requires_limitations(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "c.json"
            p.write_text("{}\n", encoding="utf-8")
            bundle = evidence_bundle("run", "model", 1, [p], {}, ["a"], ["l"])
            self.assertEqual(validate_bundle(bundle), [])
            bundle["limitations"] = []
            self.assertTrue(validate_bundle(bundle))

    def test_write_json_sorted_and_parseable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "x.json"
            write_json(p, {"b": 1, "a": 2})
            self.assertEqual(json.loads(p.read_text()), {"a": 2, "b": 1})


if __name__ == "__main__":
    unittest.main()
