from __future__ import annotations

import argparse
import json
import math
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ix_fusion.poc import run_poc
from ix_fusion.studies import run_secondary_studies


COMPARE_FILES = (
    "poc/c6_candidate.json",
    "baselines/matched_helical_5fp.json",
    "poc/verdict.json",
    "monte_carlo/rf_robustness.json",
    "ablations/c6_ablations.json",
    "monte_carlo/geometry_error_robustness.json",
    "evidence/loss_ledger.json",
    "poc/POC_RESULT.md",
)

# Numerical scientific outputs can differ by a few last bits across operating
# systems, Python patch releases, CPU math libraries, and NumPy builds.  The
# reproduction gate therefore requires exact structure/text and extremely
# tight numerical agreement rather than byte-for-byte float identity.
FLOAT_REL_TOL = 1.0e-10
FLOAT_ABS_TOL = 1.0e-12
MAX_REPORTED_MISMATCHES = 8


def _canonical_json(path: Path) -> Any:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data.pop("created_utc", None)
    return data


def _json_mismatches(expected: Any, actual: Any, location: str = "$") -> list[str]:
    """Return structural/value mismatches, allowing only tiny float noise."""
    if isinstance(expected, bool) or isinstance(actual, bool):
        return [] if expected is actual else [f"{location}: {expected!r} != {actual!r}"]

    if isinstance(expected, int) and isinstance(actual, int):
        return [] if expected == actual else [f"{location}: {expected!r} != {actual!r}"]

    if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
        left = float(expected)
        right = float(actual)
        if math.isfinite(left) and math.isfinite(right) and math.isclose(
            left,
            right,
            rel_tol=FLOAT_REL_TOL,
            abs_tol=FLOAT_ABS_TOL,
        ):
            return []
        return [f"{location}: {left:.17g} != {right:.17g}"]

    if type(expected) is not type(actual):
        return [
            f"{location}: type mismatch {type(expected).__name__} != {type(actual).__name__}"
        ]

    if isinstance(expected, dict):
        expected_keys = set(expected)
        actual_keys = set(actual)
        errors: list[str] = []
        if expected_keys != actual_keys:
            missing = sorted(expected_keys - actual_keys)
            extra = sorted(actual_keys - expected_keys)
            if missing:
                errors.append(f"{location}: missing keys {missing}")
            if extra:
                errors.append(f"{location}: extra keys {extra}")
            if len(errors) >= MAX_REPORTED_MISMATCHES:
                return errors[:MAX_REPORTED_MISMATCHES]
        for key in sorted(expected_keys & actual_keys):
            errors.extend(_json_mismatches(expected[key], actual[key], f"{location}.{key}"))
            if len(errors) >= MAX_REPORTED_MISMATCHES:
                return errors[:MAX_REPORTED_MISMATCHES]
        return errors

    if isinstance(expected, list):
        if len(expected) != len(actual):
            return [f"{location}: length {len(expected)} != {len(actual)}"]
        errors = []
        for index, (left, right) in enumerate(zip(expected, actual, strict=True)):
            errors.extend(_json_mismatches(left, right, f"{location}[{index}]"))
            if len(errors) >= MAX_REPORTED_MISMATCHES:
                return errors[:MAX_REPORTED_MISMATCHES]
        return errors

    return [] if expected == actual else [f"{location}: {expected!r} != {actual!r}"]


def _mismatches(expected: Path, actual: Path) -> list[str]:
    if expected.suffix == ".json":
        return _json_mismatches(_canonical_json(expected), _canonical_json(actual))
    if expected.read_text(encoding="utf-8") == actual.read_text(encoding="utf-8"):
        return []
    return ["text differs"]


def reproduce(repo_root: Path, verify: bool) -> list[str]:
    errors: list[str] = []
    with tempfile.TemporaryDirectory(prefix="ixfusion-repro-") as tmp:
        out = Path(tmp) / "results"
        run_poc(repo_root, out, generate_figures=False)
        run_secondary_studies(repo_root, out)
        if verify:
            committed = repo_root / "results"
            for rel in COMPARE_FILES:
                generated = out / rel
                expected = committed / rel
                if not expected.exists():
                    errors.append(f"missing committed result: {rel}")
                    continue
                mismatches = _mismatches(expected, generated)
                if mismatches:
                    errors.append(f"reproduction mismatch: {rel}: " + "; ".join(mismatches))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    errors = reproduce(ROOT, args.verify)
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print(
        "release reproduction: PASS "
        f"(float tolerances rtol={FLOAT_REL_TOL:g}, atol={FLOAT_ABS_TOL:g})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
