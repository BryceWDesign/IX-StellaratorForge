from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from ix_stellaratorforge.architecture_search import (
    ArchitectureSearchController,
    IterationEvidence,
    SearchAction,
)
from ix_stellaratorforge.reality_gradient import (
    ArchitectureMemory,
    AugmentedLagrangianState,
    ConstraintObservation,
    RejectedFamilyRecord,
    Relation,
    backward_reality_gradient,
    finite_difference_sensitivities,
)
from ix_stellaratorforge.sfr5_inverse_design import (
    CURRENT_FAMILY,
    PASS_VERDICT,
    magnetic_autopsy_from_sfr4,
    run_sfr5_campaign,
    validate_sfr5_config,
)

ROOT = Path(__file__).resolve().parents[2]


def _raw() -> dict:
    return json.loads((ROOT / "configs/reactor/sfr5_reality_gradient_a.json").read_text(encoding="utf-8"))


def _sfr4_result() -> dict:
    return json.loads((ROOT / "results/sfr4_integrated/sfr4_integrated_physical_promotion_a_v090.json").read_text(encoding="utf-8"))


def _sfr4_config() -> dict:
    return json.loads((ROOT / "configs/reactor/sfr4_integrated_physical_promotion_a.json").read_text(encoding="utf-8"))


def _result() -> dict:
    return run_sfr5_campaign(_raw(), _sfr4_result(), _sfr4_config())


def test_sfr5_config_is_fail_closed_and_declares_movable_geometry() -> None:
    raw = _raw()
    assert validate_sfr5_config(raw) == ()
    groups = {item["group"] for item in raw["movable_design_variables"]}
    assert {"plasma_boundary", "winding_surface", "coil_geometry", "coil_currents"} <= groups
    assert all(value == 0.0 for value in raw["claim_boundary"].values())
    assert all(
        status == "NOT_RUN"
        for gate, status in raw["promotion_status"].items()
        if gate != "SFR5_G0_SPEC_AND_AUTOPSY"
    )


def test_autopsy_is_derived_from_sfr4_evidence_not_magic_numbers() -> None:
    raw = _raw()
    result = magnetic_autopsy_from_sfr4(
        _sfr4_result(),
        _sfr4_config(),
        next_families=tuple(raw["search_policy"]["candidate_families"]),
    )
    diag = result.diagnostics
    assert np.isclose(diag["iota_factor_to_minimum_gate"], 3.8265231015)
    assert np.isclose(diag["normal_field_factor_over_limit"], 12.982549752)
    assert np.isclose(diag["excursion_slack_fraction_of_limit"], 0.0388736315)
    assert result.lanes[0].lane != result.lanes[1].lane


def test_sfr5_rejects_current_family_without_rejecting_stellarators() -> None:
    result = _result()
    assert result["top_level_verdict"] == PASS_VERDICT
    assert result["magnetic_autopsy"]["decision"] == "family_switch_required"
    assert result["source_invariants"]["candidate_count"] == 80
    assert result["source_invariants"]["combined_pass_count"] == 0
    assert result["rejected_family_memory"]["family"] == CURRENT_FAMILY
    assert result["rejected_family_memory"]["silent_reopen_allowed"] is False
    assert result["earned_fusion_progress_credit_fraction"] == 0.0


def test_sfr5_does_not_fabricate_geometry_gradient() -> None:
    result = _result()
    pressure = result["constraint_pressure"]
    assert pressure["active_pressure"]["mean_iota_min"] > 0.0
    assert pressure["active_pressure"]["validation_rms_Bn_over_B"] > 0.0
    assert pressure["active_pressure"]["normalized_max_excursion"] == 0.0
    assert pressure["geometry_sensitivity_status"].startswith("NOT_RUN")
    assert pressure["backward_reality_gradient_status"].startswith("NOT_COMPUTED")


def test_persisted_sfr5_result_matches_recomputation() -> None:
    persisted = json.loads((ROOT / "results/sfr5/sfr5_reality_gradient_a_v0100.json").read_text(encoding="utf-8"))
    assert persisted == _result()


def test_augmented_lagrangian_and_black_box_sensitivity_contract() -> None:
    def evaluate(x: np.ndarray) -> tuple[ConstraintObservation, ...]:
        return (
            ConstraintObservation("sum", "toy", x[0] + 2.0 * x[1], Relation.LE, limit=1.0),
            ConstraintObservation("floor", "toy", x[0], Relation.GE, limit=0.4),
        )

    point = np.array([0.8, 0.3])
    observations = evaluate(point)
    sensitivity = finite_difference_sensitivities(
        point,
        variable_names=("x0", "x1"),
        evaluator=evaluate,
    )
    state = AugmentedLagrangianState(rho=2.0)
    state.update(observations)
    gradient = backward_reality_gradient(observations, state, sensitivity)
    assert gradient["x0"] > 0.0
    assert gradient["x1"] > gradient["x0"]


def test_rejected_family_requires_declared_new_evidence_to_reopen() -> None:
    record = RejectedFamilyRecord.create(
        family="old_family",
        reason="failed",
        evidence_ids=("E1",),
        reopen_conditions=("new_geometry", "new_solver_evidence"),
    )
    memory = ArchitectureMemory()
    memory.reject(record)
    assert not memory.may_reopen("old_family", ())
    assert not memory.may_reopen("old_family", ("more_of_same",))
    assert memory.may_reopen("old_family", ("new_geometry",))
    assert memory.may_reopen("unseen_family", ())


def test_search_controller_switches_stagnant_family_and_promotes_clean_lane() -> None:
    controller = ArchitectureSearchController(stagnation_window=4, minimum_relative_improvement=0.05)
    for idx, value in enumerate((0.10, 0.099, 0.0985, 0.098), start=1):
        obs = (ConstraintObservation("bn", "hybrid", value, Relation.LE, limit=0.005),)
        controller.add(IterationEvidence(idx, "fixed_hybrid_basis", obs, objective=value))
    assert controller.decide().action is SearchAction.SWITCH_ARCHITECTURE_FAMILY

    clean = ArchitectureSearchController()
    clean.add(
        IterationEvidence(
            1,
            "modular",
            (
                ConstraintObservation("iota", "candidate", 0.4, Relation.RANGE, lower=0.25, upper=0.8),
                ConstraintObservation("excursion", "candidate", 0.1, Relation.LE, limit=0.2),
            ),
            objective=0.1,
        )
    )
    assert clean.decide().action is SearchAction.PROMOTE_SOLVER_AUTHORITY
