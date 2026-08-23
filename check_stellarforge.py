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
from ix_stellaratorforge.sfr2_actuation import (
    run_actuation_overlay_screen,
    validate_actuation_config,
)
from ix_stellaratorforge.sfr3_field_integrity import (
    PASS_VERDICT as SFR3_VERDICT,
    run_sfr3_field_integrity_screen,
    validate_sfr3_config,
)
from ix_stellaratorforge.sfr3_dual_boundary import (
    PASS_VERDICT as DUAL_BOUNDARY_VERDICT,
    run_dual_boundary_screen,
    validate_dual_boundary_config,
)
from ix_stellaratorforge.sfr4_integrated_campaign import (
    PASS_VERDICT as SFR4_VERDICT,
    run_integrated_campaign,
    validate_integrated_config,
)
from ix_stellaratorforge.sfr5_inverse_design import (
    PASS_VERDICT as SFR5_VERDICT,
    run_sfr5_campaign,
    validate_sfr5_config,
)

CONTACT = "https://www.linkedin.com/in/brycewdesign/"
LICENSE_REF = "LicenseRef-IX-StellaratorForge-Eval-Only-1.1"
V040_VERDICT = "MAXIMUM_IN_REPO_COMPUTATIONAL_CLOSURE_COMPLETE__PRODUCTION_SOLVER_AND_HARDWARE_GATES_REMAIN"
SFR2_PRIMARY_VERDICT = "NO_PRIMARY_CASE_CROSSES_OPTIMISTIC_IGNITION_PROXY"
ACTUATION_VERDICT = "NO_DECLARED_BREATHING_CASE_IMPROVES_BOTH_CYCLE_AVERAGE_PROXY_AND_FUSION_POWER"


def run(label: str, command: list[str]) -> bool:
    proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    ok = proc.returncode == 0
    print(f"{label:.<52} {'PASS' if ok else 'FAIL'}")
    if not ok:
        print(proc.stdout)
        print(proc.stderr)
    return ok


def main() -> int:
    print("IX-STELLARATORFORGE v0.10.0 QUALITY GATE\n")
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

    try:
        actuation_raw = json.loads(
            (ROOT / "configs/reactor/sfr2_actuation_overlay_a.json").read_text(encoding="utf-8")
        )
        actuation_errors = validate_actuation_config(actuation_raw)
        actuation_spec_ok = not actuation_errors
    except Exception as exc:  # noqa: BLE001
        actuation_raw = {}
        actuation_errors = (f"SFR-2 actuation overlay config parse/validation failed: {exc}",)
        actuation_spec_ok = False
    print(f"{'SFR-2 actuation-overlay invariants':.<52} {'PASS' if actuation_spec_ok else 'FAIL'}")
    failures.extend(actuation_errors)

    try:
        sfr3_raw = json.loads(
            (ROOT / "configs/reactor/sfr3_field_integrity_shell_a.json").read_text(
                encoding="utf-8"
            )
        )
        sfr3_errors = validate_sfr3_config(sfr3_raw)
        sfr3_spec_ok = not sfr3_errors
    except Exception as exc:  # noqa: BLE001
        sfr3_raw = {}
        sfr3_errors = (f"SFR-3 field-integrity config parse/validation failed: {exc}",)
        sfr3_spec_ok = False
    print(f"{'SFR-3 field-integrity invariants':.<52} {'PASS' if sfr3_spec_ok else 'FAIL'}")
    failures.extend(sfr3_errors)

    try:
        dual_boundary_raw = json.loads(
            (ROOT / "configs/reactor/sfr3_dual_boundary_ahis_a.json").read_text(
                encoding="utf-8"
            )
        )
        dual_boundary_errors = validate_dual_boundary_config(dual_boundary_raw)
        dual_boundary_spec_ok = not dual_boundary_errors
    except Exception as exc:  # noqa: BLE001
        dual_boundary_raw = {}
        dual_boundary_errors = (f"dual-boundary config parse/validation failed: {exc}",)
        dual_boundary_spec_ok = False
    print(f"{'SFR-3 dual-boundary invariants':.<52} {'PASS' if dual_boundary_spec_ok else 'FAIL'}")
    failures.extend(dual_boundary_errors)

    try:
        sfr4_raw = json.loads(
            (ROOT / "configs/reactor/sfr4_integrated_physical_promotion_a.json").read_text(
                encoding="utf-8"
            )
        )
        sfr4_errors = validate_integrated_config(sfr4_raw)
        sfr4_spec_ok = not sfr4_errors
    except Exception as exc:  # noqa: BLE001
        sfr4_raw = {}
        sfr4_errors = (f"SFR-4 config parse/validation failed: {exc}",)
        sfr4_spec_ok = False
    print(f"{'SFR-4 integrated-campaign invariants':.<52} {'PASS' if sfr4_spec_ok else 'FAIL'}")
    failures.extend(sfr4_errors)

    try:
        sfr5_raw = json.loads(
            (ROOT / "configs/reactor/sfr5_reality_gradient_a.json").read_text(encoding="utf-8")
        )
        sfr5_errors = validate_sfr5_config(sfr5_raw)
        sfr5_spec_ok = not sfr5_errors
    except Exception as exc:  # noqa: BLE001
        sfr5_raw = {}
        sfr5_errors = (f"SFR-5 config parse/validation failed: {exc}",)
        sfr5_spec_ok = False
    print(f"{'SFR-5 Reality Gradient invariants':.<52} {'PASS' if sfr5_spec_ok else 'FAIL'}")
    failures.extend(sfr5_errors)

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
        "configs/reactor/sfr2_actuation_overlay_a.json",
        "schemas/reactor/sfr2_actuation_overlay.schema.json",
        "provenance/SFR2_ACTUATION_TECHNICAL_BASIS_2026.json",
        "results/sfr2_actuation/sfr2_actuation_overlay_a_v060.json",
        "configs/reactor/sfr3_field_integrity_shell_a.json",
        "schemas/reactor/sfr3_field_integrity_shell.schema.json",
        "provenance/SFR3_FIELD_INTEGRITY_TECHNICAL_BASIS_2026.json",
        "external_solvers/sfr3_field_integrity_evidence_contract.json",
        "results/sfr3_field_integrity/sfr3_field_integrity_shell_a_v070.json",
        "configs/reactor/sfr3_dual_boundary_ahis_a.json",
        "schemas/reactor/sfr3_dual_boundary_ahis.schema.json",
        "provenance/SFR3_DUAL_BOUNDARY_TECHNICAL_BASIS_2026.json",
        "external_solvers/sfr3_dual_boundary_evidence_contract.json",
        "results/sfr3_dual_boundary/sfr3_dual_boundary_ahis_a_v080.json",
        "configs/reactor/sfr4_integrated_physical_promotion_a.json",
        "schemas/reactor/sfr4_integrated_physical_promotion.schema.json",
        "provenance/SFR4_INTEGRATED_TECHNICAL_BASIS_2026.json",
        "external_solvers/sfr4_integrated_evidence_contract.json",
        "results/sfr4_integrated/sfr4_integrated_physical_promotion_a_v090.json",
        "configs/reactor/sfr5_reality_gradient_a.json",
        "schemas/reactor/sfr5_reality_gradient.schema.json",
        "provenance/SFR5_REALITY_GRADIENT_TECHNICAL_BASIS_2026.json",
        "external_solvers/sfr5_inverse_design_evidence_contract.json",
        "results/sfr5/sfr5_reality_gradient_a_v0100.json",
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
            version == "0.10.0"
            and 'version = "0.10.0"' in pyproject
            and 'version: "0.10.0"' in citation
            and sbom["name"] == "IX-StellaratorForge-0.10.0-SBOM"
            and sbom["packages"][0]["versionInfo"] == "0.10.0"
        )
    except Exception as exc:  # noqa: BLE001
        version_ok = False
        failures.append(f"release-version consistency failed: {exc}")
    print(f"{'v0.10 release metadata consistency':.<52} {'PASS' if version_ok else 'FAIL'}")
    if not version_ok:
        failures.append("v0.10 release metadata inconsistent")

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

    try:
        with (ROOT / "BOM/SFR2_ACTUATION_OVERLAY_BOM.csv").open(
            newline="", encoding="utf-8"
        ) as f:
            actuation_rows = list(csv.DictReader(f))
        actuation_ids = [row["ID"] for row in actuation_rows]
        actuation_bom_ok = (
            len(actuation_rows) == 24
            and len(set(actuation_ids)) == 24
            and any(row["Quantity"] == "8" for row in actuation_rows)
            and any(row["Quantity"] == "24" for row in actuation_rows)
        )
    except Exception as exc:  # noqa: BLE001
        actuation_bom_ok = False
        failures.append(f"actuation BOM parse failed: {exc}")
    print(f"{'SFR-2 actuation 24-row architecture BOM':.<52} {'PASS' if actuation_bom_ok else 'FAIL'}")
    if not actuation_bom_ok:
        failures.append("actuation overlay BOM inventory check failed")

    try:
        with (ROOT / "BOM/SFR3_FIELD_INTEGRITY_SHELL_BOM.csv").open(
            newline="", encoding="utf-8"
        ) as f:
            sfr3_rows = list(csv.DictReader(f))
        sfr3_ids = [row["ID"] for row in sfr3_rows]
        dispositions = {row["Disposition"] for row in sfr3_rows}
        sfr3_bom_ok = (
            len(sfr3_rows) == 52
            and len(set(sfr3_ids)) == 52
            and {"KEEP", "ADAPT", "NEW", "DEFER", "REJECT", "SEPARATE"}.issubset(
                dispositions
            )
        )
    except Exception as exc:  # noqa: BLE001
        sfr3_bom_ok = False
        failures.append(f"SFR-3 BOM parse failed: {exc}")
    print(f"{'SFR-3 field-integrity 52-row BOM':.<52} {'PASS' if sfr3_bom_ok else 'FAIL'}")
    if not sfr3_bom_ok:
        failures.append("SFR-3 field-integrity BOM inventory check failed")

    try:
        with (ROOT / "BOM/SFR3_DUAL_BOUNDARY_AHIS_BOM.csv").open(
            newline="", encoding="utf-8"
        ) as f:
            dual_boundary_rows = list(csv.DictReader(f))
        dual_boundary_ids = [row["ID"] for row in dual_boundary_rows]
        dual_boundary_dispositions = {row["Disposition"] for row in dual_boundary_rows}
        dual_boundary_bom_ok = (
            len(dual_boundary_rows) == 64
            and len(set(dual_boundary_ids)) == 64
            and {"KEEP", "ADAPT", "NEW", "DEFER", "REJECT", "SEPARATE"}.issubset(
                dual_boundary_dispositions
            )
        )
    except Exception as exc:  # noqa: BLE001
        dual_boundary_bom_ok = False
        failures.append(f"dual-boundary BOM parse failed: {exc}")
    print(f"{'SFR-3 dual-boundary 64-row BOM':.<52} {'PASS' if dual_boundary_bom_ok else 'FAIL'}")
    if not dual_boundary_bom_ok:
        failures.append("dual-boundary BOM inventory check failed")

    try:
        with (ROOT / "BOM/SFR4_INTEGRATED_PROMOTION_BOM.csv").open(
            newline="", encoding="utf-8"
        ) as f:
            sfr4_rows = list(csv.DictReader(f))
        sfr4_ids = [row["id"] for row in sfr4_rows]
        sfr4_bom_ok = (
            len(sfr4_rows) == 64
            and len(set(sfr4_ids)) == 64
            and len({row["workstream"] for row in sfr4_rows}) == 7
        )
    except Exception as exc:  # noqa: BLE001
        sfr4_bom_ok = False
        failures.append(f"SFR-4 BOM parse failed: {exc}")
    print(f"{'SFR-4 integrated 64-row BOM':.<52} {'PASS' if sfr4_bom_ok else 'FAIL'}")
    if not sfr4_bom_ok:
        failures.append("SFR-4 integrated BOM inventory check failed")

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
        ("Full self-contained test suite", [sys.executable, "scripts/run_zero_arg_tests.py"]),
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

    try:
        persisted_actuation = json.loads(
            (ROOT / "results/sfr2_actuation/sfr2_actuation_overlay_a_v060.json").read_text(
                encoding="utf-8"
            )
        )
        recomputed_actuation = run_actuation_overlay_screen(actuation_raw)
        actuation_result = persisted_actuation["breathing_result"]
        image_result = persisted_actuation["concept_image_result"]
        actuation_screen_ok = (
            persisted_actuation == recomputed_actuation
            and persisted_actuation["release"] == "0.6.0"
            and actuation_result["verdict"] == ACTUATION_VERDICT
            and actuation_result["any_joint_cycle_average_improvement"] is False
            and actuation_result["any_cycle_average_proxy_pass"] is False
            and persisted_actuation["model_rules"]["baseline_geometry_changed"] is False
            and persisted_actuation["model_rules"]["magnetic_pumping_heating_credit"] == 0.0
            and persisted_actuation["model_rules"]["three_body_fusion_credit"] == 0.0
            and image_result["zero_D_closer_to_ignition_credit"] == 0.0
            and all(
                status == "NOT_RUN"
                for gate, status in persisted_actuation["promotion_status"].items()
                if gate != "SFR2A_G0_OVERLAY_SPEC"
            )
        )
    except Exception as exc:  # noqa: BLE001
        actuation_screen_ok = False
        failures.append(f"SFR-2 actuation persisted/recomputed screen failed: {exc}")
    print(f"{'SFR-2 breathing/tri-lobe no-overclaim screen':.<52} {'PASS' if actuation_screen_ok else 'FAIL'}")
    if not actuation_screen_ok:
        failures.append("SFR-2 actuation screen stale, overclaimed, or inconsistent")

    try:
        persisted_sfr3 = json.loads(
            (ROOT / "results/sfr3_field_integrity/sfr3_field_integrity_shell_a_v070.json").read_text(
                encoding="utf-8"
            )
        )
        recomputed_sfr3 = run_sfr3_field_integrity_screen(sfr3_raw)
        scenarios = {scenario["id"]: scenario for scenario in persisted_sfr3["scenarios"]}
        sfr3_screen_ok = (
            persisted_sfr3 == recomputed_sfr3
            and persisted_sfr3["release"] == "0.7.0"
            and persisted_sfr3["top_level_verdict"] == SFR3_VERDICT
            and persisted_sfr3["screen_pass"] is True
            and persisted_sfr3["model_definition"]["response_matrix_shape"] == [12, 24]
            and persisted_sfr3["model_definition"]["response_matrix_rank"] == 12
            and scenarios["nominal"]["total_rms_reduction_fraction"] >= 0.60
            and scenarios["single_actuator_unavailable"]["total_rms_reduction_fraction"] >= 0.55
            and scenarios["passive_transient_only"]["active_correction_allowed"] is False
            and scenarios["low_sensor_confidence"]["control_state"] == "PASSIVE_ONLY_SAFE_HOLD"
            and all(value == 0.0 for key, value in persisted_sfr3["claim_boundary"].items() if key.endswith("_credit"))
            and all(scenario["fusion_or_ignition_credit"] == 0.0 for scenario in persisted_sfr3["scenarios"])
            and all(
                status == "NOT_RUN"
                for gate, status in persisted_sfr3["promotion_status"].items()
                if gate not in {"SFR3_G0_ARCHITECTURE_SPEC", "SFR3_G1_SYNTHETIC_CONTROLLABILITY"}
            )
        )
    except Exception as exc:  # noqa: BLE001
        sfr3_screen_ok = False
        failures.append(f"SFR-3 persisted/recomputed screen failed: {exc}")
    print(f"{'SFR-3 synthetic controllability no-overclaim':.<52} {'PASS' if sfr3_screen_ok else 'FAIL'}")
    if not sfr3_screen_ok:
        failures.append("SFR-3 screen stale, overclaimed, or inconsistent")

    try:
        persisted_dual_boundary = json.loads(
            (ROOT / "results/sfr3_dual_boundary/sfr3_dual_boundary_ahis_a_v080.json").read_text(
                encoding="utf-8"
            )
        )
        recomputed_dual_boundary = run_dual_boundary_screen(dual_boundary_raw, sfr3_raw)
        dual_faults = {
            scenario["id"]: scenario
            for scenario in persisted_dual_boundary["fault_scenarios"]
        }
        selected_stack = next(
            stack
            for stack in persisted_dual_boundary["wall_stack_results"]
            if stack["id"] == persisted_dual_boundary["selected_stack_id"]
        )
        dual_boundary_screen_ok = (
            persisted_dual_boundary == recomputed_dual_boundary
            and persisted_dual_boundary["release"] == "0.8.0"
            and persisted_dual_boundary["top_level_verdict"] == DUAL_BOUNDARY_VERDICT
            and persisted_dual_boundary["screen_pass"] is True
            and persisted_dual_boundary["monitoring_inventory"][
                "paired_inner_outer_monitoring_locations"
            ]
            == 192
            and persisted_dual_boundary["monitoring_inventory"][
                "total_declared_sensing_elements"
            ]
            == 1736
            and selected_stack["nominal"]["all_layer_temperature_screens_pass"] is True
            and selected_stack["upset_steady_upper_bound"][
                "all_layer_temperature_screens_pass"
            ]
            is True
            and dual_faults["inner_hotspot_single_lane_failure"][
                "all_declared_signals_detected"
            ]
            is True
            and dual_faults["silent_armor_crack"]["control_state"].startswith(
                "NO_AUTOMATIC_DETECTION"
            )
            and all(
                value == 0.0
                for key, value in persisted_dual_boundary["claim_boundary"].items()
                if key.endswith("_credit")
            )
            and all(
                scenario["fusion_or_ignition_credit"] == 0.0
                for scenario in persisted_dual_boundary["fault_scenarios"]
            )
            and all(
                status == "NOT_RUN"
                for gate, status in persisted_dual_boundary["promotion_status"].items()
                if gate
                not in {
                    "SFR3D_G0_DUAL_BOUNDARY_SPEC",
                    "SFR3D_G1_REDUCED_THERMAL_AND_FAULT_SCREEN",
                }
            )
        )
    except Exception as exc:  # noqa: BLE001
        dual_boundary_screen_ok = False
        failures.append(f"dual-boundary persisted/recomputed screen failed: {exc}")
    print(f"{'SFR-3 dual-boundary no-overclaim screen':.<52} {'PASS' if dual_boundary_screen_ok else 'FAIL'}")
    if not dual_boundary_screen_ok:
        failures.append("dual-boundary screen stale, overclaimed, or inconsistent")

    try:
        persisted_sfr4 = json.loads(
            (ROOT / "results/sfr4_integrated/sfr4_integrated_physical_promotion_a_v090.json").read_text(
                encoding="utf-8"
            )
        )
        recomputed_sfr4 = run_integrated_campaign(sfr4_raw)
        coil = persisted_sfr4["workstreams"]["1_physical_coil_field"]
        particles = persisted_sfr4["workstreams"]["4_particle_confinement"]
        magnets = persisted_sfr4["workstreams"]["6_magnet_engineering"]
        systems = persisted_sfr4["workstreams"]["7_reactor_systems"]
        heat = persisted_sfr4["heat_exhaust_resolution"]
        promotion = persisted_sfr4["promotion_summary"]
        persisted_sfr4_core = dict(persisted_sfr4)
        recomputed_sfr4_core = dict(recomputed_sfr4)
        persisted_sfr4_core.pop("solver_availability", None)
        recomputed_sfr4_core.pop("solver_availability", None)
        sfr4_screen_ok = (
            persisted_sfr4_core == recomputed_sfr4_core
            and persisted_sfr4["release"] == "0.9.0"
            and persisted_sfr4["top_level_verdict"] == SFR4_VERDICT
            and coil["candidate_count"] == 80
            and coil["combined_pass_count"] == 0
            and coil["physical_coil_promoted"] is False
            and particles["particle_confinement_promoted"] is False
            and heat["nominal_and_declared_steady_heat_envelope_pass"] is True
            and heat["transient_disruption_heat_resolved"] is False
            and magnets["magnet_promoted"] is False
            and systems["full_3D_TBR_calculated"] is False
            and promotion["earned_fusion_progress_credit_fraction"] == 0.0
            and all(value == 0.0 for value in persisted_sfr4["claim_boundary"].values())
        )
    except Exception as exc:  # noqa: BLE001
        sfr4_screen_ok = False
        failures.append(f"SFR-4 persisted/recomputed campaign failed: {exc}")
    print(f"{'SFR-4 integrated no-overclaim campaign':.<52} {'PASS' if sfr4_screen_ok else 'FAIL'}")
    if not sfr4_screen_ok:
        failures.append("SFR-4 campaign stale, overclaimed, or inconsistent")

    try:
        persisted_sfr5 = json.loads(
            (ROOT / "results/sfr5/sfr5_reality_gradient_a_v0100.json").read_text(encoding="utf-8")
        )
        recomputed_sfr5 = run_sfr5_campaign(sfr5_raw, persisted_sfr4, sfr4_raw)
        diag = persisted_sfr5["magnetic_autopsy"]["diagnostics"]
        pressure = persisted_sfr5["constraint_pressure"]
        promotion5 = persisted_sfr5["promotion_status"]
        sfr5_screen_ok = (
            persisted_sfr5 == recomputed_sfr5
            and persisted_sfr5["release"] == "0.10.0"
            and persisted_sfr5["top_level_verdict"] == SFR5_VERDICT
            and persisted_sfr5["source_invariants"]["candidate_count"] == 80
            and persisted_sfr5["source_invariants"]["combined_pass_count"] == 0
            and persisted_sfr5["magnetic_autopsy"]["decision"] == "family_switch_required"
            and 3.82 < diag["iota_factor_to_minimum_gate"] < 3.84
            and 0.038 < diag["excursion_slack_fraction_of_limit"] < 0.040
            and 12.9 < diag["normal_field_factor_over_limit"] < 13.1
            and pressure["geometry_sensitivity_status"].startswith("NOT_RUN")
            and pressure["backward_reality_gradient_status"].startswith("NOT_COMPUTED")
            and persisted_sfr5["earned_fusion_progress_credit_fraction"] == 0.0
            and all(value == 0.0 for value in persisted_sfr5["claim_boundary"].values())
            and all(
                status == "NOT_RUN"
                for gate, status in promotion5.items()
                if gate != "SFR5_G0_SPEC_AND_AUTOPSY"
            )
        )
    except Exception as exc:  # noqa: BLE001
        sfr5_screen_ok = False
        failures.append(f"SFR-5 persisted/recomputed campaign failed: {exc}")
    print(f"{'SFR-5 Reality Gradient no-overclaim campaign':.<52} {'PASS' if sfr5_screen_ok else 'FAIL'}")
    if not sfr5_screen_ok:
        failures.append("SFR-5 campaign stale, overclaimed, or inconsistent")

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
    print("Meaning: release integrity, preserved SFR-1/SFR-2/SFR-3 evidence, the v0.9 SFR-4 integrated campaign, and the v0.10 SFR-5 adaptive inverse-design autopsy reproduce from committed inputs and code.")
    print("SFR-2 primary result: no H_ISS04=1 case crosses its optimistic ignition proxy; dynamic compression receives no unmodeled phase/RF or flux-compression credit.")
    print("SFR-2 actuation result: no declared breathing case improves both cycle-average proxy and fusion power; the tri-lobe translation receives zero unearned fusion credit.")
    print("SFR-3 result: the synthetic bounded control and fault cases pass their declared thresholds; physical confinement and fusion credit remain zero.")
    print("Dual-boundary result: reduced thermal and fault-routing screens pass; mechanical plasma-force, wall-lifetime, safety and fusion credit remain zero.")
    print("SFR-4 result: 80 direct-filament coil cases produce zero topology passes; the declared nominal and steady heat envelope passes, but equilibrium, transport, transient heat, qualified magnets, TBR and fusion remain unproven.")
    print("SFR-5 result: the failed magnetic family is rejected as the preferred brute-force search direction; the next search opens plasma boundary, winding surface and nonplanar coil geometry, while real sensitivities and production co-design remain unrun.")
    print("It does NOT mean finite-beta dynamic MHD, kinetic confinement, qualified high-field magnets, full-3D TBR, ignition, net-electric fusion, safety qualification, or hardware operation has been demonstrated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
