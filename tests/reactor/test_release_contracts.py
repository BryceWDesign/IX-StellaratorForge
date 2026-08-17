from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTACT = "https://www.linkedin.com/in/brycewdesign/"


def test_license_has_explicit_contact_and_no_implied_grant() -> None:
    texts = [(ROOT / name).read_text(encoding="utf-8") for name in ("LICENSE", "LICENSING.md", "NOTICE", "README.md")]
    assert all(CONTACT in text for text in texts)
    license_text = texts[0]
    assert "LicenseRef-IX-StellaratorForge-Eval-Only-1.1" in license_text
    assert "does not" in license_text.lower() and "grant" in license_text.lower()


def test_full_bom_has_87_unique_rows_and_all_maturity_classes() -> None:
    with (ROOT / "BOM/SFR1_FULL_SYSTEM_BOM.csv").open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 87
    assert len({row["ID"] for row in rows}) == 87
    assert {"DEFINED", "CANDIDATE", "SOLVER_DEPENDENT", "HARDWARE_DEPENDENT"}.issubset({row["Maturity"] for row in rows})


def test_external_solver_matrix_is_explicitly_unexecuted() -> None:
    matrix = json.loads((ROOT / "external_solvers/g1_candidate_matrix.json").read_text(encoding="utf-8"))
    assert matrix["executed"] is False
    assert len(matrix["candidates"]) == 5
