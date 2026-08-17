from __future__ import annotations

import compileall
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from ix_fusion.evidence import validate_bundle


REQUIRED_FILES = (
    "LICENSE",
    "NOTICE",
    "README.md",
    "VALIDATION_REPORT.md",
    "PROOF_OF_CONCEPT.md",
    "CITATION.cff",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "BOM/SOFTWARE_BOM.md",
    "BOM/CONCEPTUAL_SYSTEM_BOM.md",
    "BOM/RESEARCH_BOM.md",
    "docs/02_CLAIM_BOUNDARY.md",
    "docs/08_BUILD_AND_VALIDATE.md",
    "docs/10_SAFETY_AND_SCOPE.md",
    "docs/12_MODEL_LIMITATIONS.md",
    "docs/13_KILL_CRITERIA.md",
    "docs/15_EXTERNAL_SOLVERS.md",
    "results/poc/POC_RESULT.md",
    "results/poc/verdict.json",
    "results/evidence/IXFUSION-POC-001.json",
    "results/evidence/loss_ledger.json",
    "MANIFEST.sha256",
)

JSON_DIRS = (
    ROOT / "configs",
    ROOT / "schemas",
    ROOT / "results",
    ROOT / "provenance",
)

TEXT_EXTENSIONS = {".py", ".md", ".json", ".toml", ".yml", ".yaml", ".cff"}
BANNED_MARKERS = ("TODO:", "FIXME:", "TBD:", "INSERT_HERE", "REPLACE_ME")


def run_step(name: str, command: list[str]) -> tuple[bool, str]:
    proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    output = (proc.stdout + proc.stderr).strip()
    return proc.returncode == 0, output


def check_required_files() -> list[str]:
    return [f"missing required file: {rel}" for rel in REQUIRED_FILES if not (ROOT / rel).exists()]


def check_json() -> list[str]:
    errors: list[str] = []
    for directory in JSON_DIRS:
        if not directory.exists():
            continue
        for path in sorted(directory.rglob("*.json")):
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except Exception as exc:  # noqa: BLE001 - validation gate reports parser detail
                errors.append(f"invalid JSON {path.relative_to(ROOT)}: {exc}")
    return errors


def check_no_scaffolding_markers() -> list[str]:
    errors: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        if path.resolve() == Path(__file__).resolve():
            continue
        if any(part in {".git", ".venv", "__pycache__"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for marker in BANNED_MARKERS:
            if marker in text:
                errors.append(f"scaffolding marker {marker!r} in {path.relative_to(ROOT)}")
    return errors


def check_license_contract() -> list[str]:
    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    required = (
        "IX-STELLARATORFORGE RESEARCH & EVALUATION LICENSE",
        "Evaluation Use",
        "No patent",
        "production",
        "operational",
    )
    return [f"license missing required concept: {term}" for term in required if term.lower() not in license_text.lower()]


def check_claim_boundary() -> list[str]:
    verdict = json.loads((ROOT / "results/poc/verdict.json").read_text(encoding="utf-8"))
    errors: list[str] = []
    if verdict.get("scientific_stage") != "geometry_hypothesis":
        errors.append("release 0.1 scientific stage must remain geometry_hypothesis")
    if verdict.get("reduced_model_verdict") not in {"PASS_REDUCED_MODEL", "FAIL_OR_INCONCLUSIVE"}:
        errors.append("unsupported reduced-model verdict")
    bundle = json.loads((ROOT / "results/evidence/IXFUSION-POC-001.json").read_text(encoding="utf-8"))
    errors.extend(f"evidence bundle: {e}" for e in validate_bundle(bundle))
    losses = json.loads((ROOT / "results/evidence/loss_ledger.json").read_text(encoding="utf-8"))
    for key in ("fast_particle_loss", "mhd_stability", "turbulent_transport", "net_electric_power"):
        if losses.get(key, {}).get("status") != "UNKNOWN":
            errors.append(f"high-authority loss ledger entry must remain UNKNOWN in release 0.1: {key}")
    return errors


def check_manifest() -> tuple[bool, str]:
    return run_step("manifest", [sys.executable, "scripts/verify_manifest.py"])


def main() -> int:
    print("IX-STELLARATORFORGE FOUNDATION QUALITY GATE")
    print()
    failures: list[str] = []

    checks = [
        ("Repository contract", check_required_files),
        ("JSON integrity", check_json),
        ("No scaffolding markers", check_no_scaffolding_markers),
        ("Evaluation license", check_license_contract),
        ("Claim boundary", check_claim_boundary),
    ]
    for label, fn in checks:
        errors = fn()
        if errors:
            print(f"{label:.<34} FAIL")
            failures.extend(errors)
        else:
            print(f"{label:.<34} PASS")

    compiled = compileall.compile_dir(ROOT / "src", quiet=1) and compileall.compile_dir(ROOT / "scripts", quiet=1)
    compiled = compiled and compileall.compile_dir(ROOT / "tests", quiet=1)
    if compiled:
        print(f"{'Python compilation':.<34} PASS")
    else:
        print(f"{'Python compilation':.<34} FAIL")
        failures.append("Python compilation failed")

    ok, output = run_step("unit tests", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"])
    print(f"{'Unit tests':.<34} {'PASS' if ok else 'FAIL'}")
    if not ok:
        failures.append("unit tests failed\n" + output)

    ok, output = run_step("reproduction", [sys.executable, "scripts/reproduce_release.py", "--verify"])
    print(f"{'Scientific reproduction':.<34} {'PASS' if ok else 'FAIL'}")
    if not ok:
        failures.append("release reproduction failed\n" + output)

    ok, output = check_manifest()
    print(f"{'Release manifest':.<34} {'PASS' if ok else 'FAIL'}")
    if not ok:
        failures.append("manifest verification failed\n" + output)

    print()
    if failures:
        print("IX-STELLARATORFORGE FOUNDATION: RED")
        print()
        for failure in failures:
            print("-", failure)
        return 1

    print("IX-STELLARATORFORGE FOUNDATION: GREEN")
    print("Meaning: internal repository integrity and reduced-order evidence reproduce.")
    print("It does NOT mean plasma confinement, ignition, net energy, or reactor feasibility is proven.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
