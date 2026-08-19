from __future__ import annotations

import compileall
import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from ix_stellaratorforge.reactor import load_reactor_config, validate_reactor_config
from ix_stellaratorforge.sfr2 import run_sfr2_screen, validate_sfr2_config

CONTACT = "https://www.linkedin.com/in/brycewdesign/"
LICENSE_REF = "LicenseRef-IX-StellaratorForge-Eval-Only-1.1"
V040_VERDICT = "MAXIMUM_IN_REPO_COMPUTATIONAL_CLOSURE_COMPLETE__PRODUCTION_SOLVER_AND_HARDWARE_GATES_REMAIN"
SFR2_PRIMARY_VERDICT = "NO_PRIMARY_CASE_CROSSES_OPTIMISTIC_IGNITION_PROXY"


def run(label: str, command: list[str]) -> bool:
    proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    ok = proc.returncode == 0
    print(f"{label:.<52} {'PASS' if ok else 'FAIL'}")
    if not ok:
        print(proc.stdout)
        print(proc.stderr)
    return ok


def main() -> int:
    print("IX-STELLARATORFORGE v0.5.0 QUALITY GATE\n")
    failures: list[str] = []

    config = load_reactor_config(ROOT / "configs/reactor/sfr1_rev_a.json")
    validation = validate_reactor_config(config)
    print(f"{'SFR-1 Rev A design invariants':.<52} {'PASS' if validation.passed else 'FAIL'}")
    failures.extend(validation.errors)

    try:
        sfr2_raw = json.loads((ROOT / "configs/reactor/sfr2_rev_a.json").read_text(encoding="utf-8"))
        sfr2_errors = validate_sfr2_config(sfr2_raw)
        sfr2_spec_ok = not sfr2_errors
    except Exception as exc:  # noqa: BLE001
        sfr2_raw = {}
        sfr2_errors = (f"SFR-2 config parse/validation failed: {exc}",)
        sfr2_spec_ok = False
    print(f"{'SFR-2 Rev A assumption-breaker invariants':.<52} {'PASS' if sfr2_spec_ok else 'FAIL'}")
    failures.extend(sfr2_errors)

    json_files = (
        "configs/reactor/parameter_ledger.json",
        "provenance/EXTERNAL_TECHNICAL_BASIS_2026.json",
        "schemas/reactor/sfr1_reference.schema.json",
        "configs/closure/high_fidelity_solver_contract.json",
        "external_solvers/result_contract.schema.json",
        "external_solvers/g1_candidate_matrix.json",
        "external_solvers/confinement_evidence_contract.json",
        "results/computational_closure/sfr1_v040.json",
        "configs/reactor/sfr2_rev_a.json",
        "schemas/reactor/sfr2_reference.schema.json",
        "provenance/SFR2_TECHNICAL_BASIS_2026.json",
        "results/sfr2/sfr2_rev_a_screen_v050.json",
        "sbom.spdx.json",
    )
    json_ok = True
    for rel in json_files:
        try:
            json.loads((ROOT / rel).read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            json_ok = False
            failures.append(f"invalid JSON {rel}: {exc}")
    print(f"{'Reactor / solver-contract JSON integrity':.<52} {'PASS' if json_ok else 'FAIL'}")

    try:
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
        sbom = json.loads((ROOT / "sbom.spdx.json").read_text(encoding="utf-8"))
        version_ok = (
            version == "0.5.0"
            and 'version = "0.5.0"' in pyproject
            and 'version: "0.5.0"' in citation
            and sbom["name"] == "IX-StellaratorForge-0.5.0-SBOM"
            and sbom["packages"][0]["versionInfo"] == "0.5.0"
        )
    except Exception as exc:  # noqa: BLE001
        version_ok = False
        failures.append(f"release-version consistency failed: {exc}")
    print(f"{'v0.5 release metadata consistency':.<52} {'PASS' if version_ok else 'FAIL'}")
    if not version_ok:
        failures.append("v0.5 release metadata inconsistent")

    texts = [(ROOT / name).read_text(encoding="utf-8") for name in ("LICENSE", "LICENSING.md", "NOTICE", "README.md")]
    license_ok = all(CONTACT in text for text in texts) and LICENSE_REF in texts[0]
    print(f"{'Eval-only license + exact LinkedIn contact':.<52} {'PASS' if license_ok else 'FAIL'}")
    if not license_ok:
        failures.append("license/contact contract incomplete")

    try:
        with (ROOT / "BOM/SFR1_FULL_SYSTEM_BOM.csv").open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        ids = [row["ID"] for row in rows]
        maturities = {row["Maturity"] for row in rows}
        bom_ok = len(rows) == 87 and len(set(ids)) == 87 and {"DEFINED", "CANDIDATE", "SOLVER_DEPENDENT", "HARDWARE_DEPENDENT"}.issubset(maturities)
    except Exception as exc:  # noqa: BLE001
        bom_ok = False
        failures.append(f"BOM parse failed: {exc}")
    print(f"{'SFR-1 full 87-row design inventory':.<52} {'PASS' if bom_ok else 'FAIL'}")
    if not bom_ok:
        failures.append("full system BOM inventory check failed")

    compiled = compileall.compile_dir(ROOT / "src/ix_stellaratorforge", quiet=1)
    compiled = compiled and compileall.compile_dir(ROOT / "tests/reactor", quiet=1)
    compiled = compiled and compileall.compile_dir(ROOT / "external_solvers/adapters", quiet=1)
    print(f"{'Python + production-adapter compilation':.<52} {'PASS' if compiled else 'FAIL'}")
    if not compiled:
        failures.append("Python compilation failed")

    inputs = {p.name for p in (ROOT / "external_solvers/inputs").glob("input.SFR1_*")}
    required_inputs = {"input.SFR1_QA_2FP_REF", "input.SFR1_QI_3FP", "input.SFR1_QI_PWO_4FP", "input.SFR1_C6_QI_6FP"}
    seed_ok = required_inputs <= inputs
    print(f"{'Finite-pressure DESC/VMEC++ seed pack':.<52} {'PASS' if seed_ok else 'FAIL'}")
    if not seed_ok:
        failures.append("G1 seed pack incomplete")

    for label, command in (
        ("Inherited IX-Fusion/vNext gate", [sys.executable, "check_vnext.py"]),
        ("Full pytest suite", [sys.executable, "-m", "pytest", "-q"]),
        ("Release manifest", [sys.executable, "scripts/verify_manifest.py"]),
    ):
        if not run(label, command):
            failures.append(f"{label} failed")

    try:
        poc = json.loads((ROOT / "results/sfr1_poc/sfr1_poc_v040.json").read_text(encoding="utf-8"))
        comp = json.loads((ROOT / "results/computational_closure/sfr1_v040.json").read_text(encoding="utf-8"))
        readiness = json.loads((ROOT / "results/reactor/sfr1_rev_a_readiness.json").read_text(encoding="utf-8"))
        artifacts_ok = (
            poc["release"] == "0.4.0"
            and poc["verdict"] == "PIPELINE_POC_PASS__REACTOR_PHYSICS_NOT_CLOSED"
            and comp["top_level_verdict"] == V040_VERDICT
            and readiness["maximum_computational_closure_v0_4"]["verdict"] == V040_VERDICT
            and readiness["current_verdict"].endswith("NOT_CLOSED")
            and comp["G2_magnets"]["classical_helical_any_pass"] is False
            and comp["G2_magnets"]["current_potential_any_pass"] is False
            and "OPEN" in comp["G1_equilibrium"]["status"]
            and comp["G9_hardware"]["status"] == "NOT_COMPUTATIONALLY_RESOLVABLE"
        )
    except Exception as exc:  # noqa: BLE001
        artifacts_ok = False
        failures.append(f"generated evidence artifact check failed: {exc}")
    print(f"{'v0.4 PoC / closure / readiness consistency':.<52} {'PASS' if artifacts_ok else 'FAIL'}")
    if not artifacts_ok:
        failures.append("v0.4 evidence artifacts stale/inconsistent")

    try:
        persisted_sfr2 = json.loads((ROOT / "results/sfr2/sfr2_rev_a_screen_v050.json").read_text(encoding="utf-8"))
        recomputed_sfr2 = run_sfr2_screen(sfr2_raw)
        best = persisted_sfr2["primary_screen"]["best_case"]
        sfr2_screen_ok = (
            persisted_sfr2 == recomputed_sfr2
            and persisted_sfr2["release"] == "0.5.0"
            and persisted_sfr2["primary_screen"]["verdict"] == SFR2_PRIMARY_VERDICT
            and persisted_sfr2["model_rules"]["staggering_confinement_credit"] == 0.0
            and persisted_sfr2["model_rules"]["dynamic_phase_heating_credit"] == 0.0
            and persisted_sfr2["model_rules"]["magnetic_flux_compression_credit"] == 0.0
            and best["ignition"]["proxy_pass"] is False
            and best["radial_squeeze_fraction"] == 0.0
            and all(
                status == "NOT_RUN"
                for gate, status in persisted_sfr2["promotion_status"].items()
                if gate != "SFR2_G0_SPEC"
            )
        )
    except Exception as exc:  # noqa: BLE001
        sfr2_screen_ok = False
        failures.append(f"SFR-2 persisted/recomputed screen check failed: {exc}")
    print(f"{'SFR-2 reproducible no-overclaim screen':.<52} {'PASS' if sfr2_screen_ok else 'FAIL'}")
    if not sfr2_screen_ok:
        failures.append("SFR-2 screen stale, overclaimed, or inconsistent")

    openmc_adapter = (ROOT / "external_solvers/adapters/build_openmc_axisymmetric_proxy.py").read_text(encoding="utf-8")
    adapters_ok = "NOT the G7 final 3-D stellarator model" in openmc_adapter and "(n,Xt)" in openmc_adapter
    print(f"{'External solver fail-closed / OpenMC proxy boundary':.<52} {'PASS' if adapters_ok else 'FAIL'}")
    if not adapters_ok:
        failures.append("external-solver claim boundary missing")

    print()
    if failures:
        print("IX-STELLARATORFORGE: RED")
        for failure in failures:
            print("-", failure)
        return 1
    print("IX-STELLARATORFORGE: GREEN")
    print("Meaning: release integrity, preserved SFR-1 v0.4 evidence, and the SFR-2 v0.5 assumption-breaker screen reproduce from committed inputs and code.")
    print("SFR-2 primary result: no H_ISS04=1 case crosses its optimistic ignition proxy; dynamic compression receives no unmodeled phase/RF or flux-compression credit.")
    print("It does NOT mean finite-beta dynamic MHD, kinetic confinement, qualified high-field magnets, full-3D TBR, ignition, net-electric fusion, safety qualification, or hardware operation has been demonstrated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
