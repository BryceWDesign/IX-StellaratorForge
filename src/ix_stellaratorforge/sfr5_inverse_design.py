"""SFR-5 Reality Gradient and adaptive inverse-design campaign.

SFR-5 does not run a production coil/plasma optimizer in the base release. It turns
the committed SFR-4 magnetic failure into a reproducible, provenance-preserving
architecture decision and defines the exact evidence required before any replacement
coil family may be promoted.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .reality_gradient import (
    ArchitectureDecision,
    ArchitectureMemory,
    AugmentedLagrangianState,
    ConstraintObservation,
    LaneAutopsy,
    RejectedFamilyRecord,
    Relation,
)

PASS_VERDICT = (
    "REALITY_GRADIENT_AUTOPSY_COMPLETE__CURRENT_MAGNETIC_FAMILY_REJECTED__"
    "ADAPTIVE_INVERSE_DESIGN_PATH_DEFINED__NO_PHYSICS_PROMOTION"
)
CURRENT_FAMILY = "fixed_helical_plus_fixed_hybrid_filament_basis"


@dataclass(frozen=True, slots=True)
class MagneticAutopsy:
    lanes: tuple[LaneAutopsy, ...]
    decision: ArchitectureDecision
    rationale: tuple[str, ...]
    next_families: tuple[str, ...]
    diagnostics: dict[str, float]

    def to_dict(self) -> dict[str, Any]:
        return {
            "lanes": [
                {
                    "lane": lane.lane,
                    "observations": [obs.to_dict() for obs in lane.observations],
                    "max_violation": lane.max_violation,
                }
                for lane in self.lanes
            ],
            "decision": self.decision.value,
            "rationale": list(self.rationale),
            "next_families": list(self.next_families),
            "diagnostics": self.diagnostics,
        }


def validate_sfr5_config(raw: dict[str, Any]) -> tuple[str, ...]:
    errors: list[str] = []
    try:
        if raw.get("schema_version") != "0.10.0":
            errors.append("schema_version must be 0.10.0")
        if raw.get("study_id") != "SFR5-REALITY-GRADIENT-A":
            errors.append("study_id must be SFR5-REALITY-GRADIENT-A")
        if raw.get("source_release") != "0.9.0":
            errors.append("source_release must remain 0.9.0")

        sources = raw["source_artifacts"]
        for key in ("sfr4_result", "sfr4_config"):
            if not str(sources.get(key, "")).strip():
                errors.append(f"source_artifacts.{key} must be non-empty")

        search = raw["search_policy"]
        if int(search["stagnation_window"]) < 2:
            errors.append("search_policy.stagnation_window must be >= 2")
        improvement = float(search["minimum_relative_improvement"])
        if not 0.0 <= improvement <= 1.0:
            errors.append("search_policy.minimum_relative_improvement must be in [0, 1]")
        families = list(search["candidate_families"])
        if len(families) < 3 or len(set(families)) != len(families):
            errors.append("search_policy.candidate_families must contain >=3 unique families")
        if not bool(search["forbid_bruteforce_same_family_after_rejection"]):
            errors.append("rejected-family brute-force continuation must remain forbidden")

        dof_groups = {str(x["group"]) for x in raw["movable_design_variables"]}
        required_groups = {
            "plasma_boundary",
            "winding_surface",
            "coil_geometry",
            "coil_currents",
        }
        if not required_groups.issubset(dof_groups):
            errors.append("movable_design_variables omit required inverse-design groups")

        claim = raw["claim_boundary"]
        if not claim or any(float(value) != 0.0 for value in claim.values()):
            errors.append("all SFR-5 claim-boundary credits must remain exactly zero")

        gates = raw["promotion_status"]
        if gates.get("SFR5_G0_SPEC_AND_AUTOPSY") != "PASS_REDUCED":
            errors.append("SFR5_G0_SPEC_AND_AUTOPSY must be PASS_REDUCED")
        for gate, status in gates.items():
            if gate != "SFR5_G0_SPEC_AND_AUTOPSY" and status != "NOT_RUN":
                errors.append(f"{gate} must remain NOT_RUN in the base SFR-5 release")
    except (KeyError, TypeError, ValueError) as exc:
        errors.append(f"invalid SFR-5 config: {exc}")
    return tuple(errors)


def magnetic_autopsy_from_sfr4(
    sfr4_result: dict[str, Any],
    sfr4_config: dict[str, Any],
    *,
    next_families: tuple[str, ...],
) -> MagneticAutopsy:
    """Derive the SFR-5 diagnosis from committed SFR-4 evidence and gates."""

    if sfr4_result.get("release") != "0.9.0":
        raise ValueError("SFR-5 source result must be the committed v0.9.0 SFR-4 result")
    coil = sfr4_result["workstreams"]["1_physical_coil_field"]
    scan = sfr4_config["coil_field_scan"]
    best = coil["best_candidate"]
    reconstruction = coil["held_out_hybrid_reconstruction"]

    iota_min = float(scan["iota_acceptance"][0])
    excursion_limit = float(scan["max_excursion_fraction"])
    bn_limit = float(scan["normal_field_rms_limit"])

    topology_lane = "direct_filament_helical_topology"
    reconstruction_lane = "held_out_hybrid_reconstruction"
    topology = LaneAutopsy(
        lane=topology_lane,
        observations=(
            ConstraintObservation(
                constraint_id="mean_iota_min",
                lane=topology_lane,
                value=float(best["mean_iota"]),
                relation=Relation.GE,
                limit=iota_min,
                authority=str(best["authority"]),
                source="results/sfr4_integrated/...v090.json:workstreams.1_physical_coil_field.best_candidate",
            ),
            ConstraintObservation(
                constraint_id="normalized_max_excursion",
                lane=topology_lane,
                value=float(best["normalized_max_excursion_over_a"]),
                relation=Relation.LE,
                limit=excursion_limit,
                authority=str(best["authority"]),
                source="results/sfr4_integrated/...v090.json:workstreams.1_physical_coil_field.best_candidate",
            ),
        ),
    )
    held_out = LaneAutopsy(
        lane=reconstruction_lane,
        observations=(
            ConstraintObservation(
                constraint_id="validation_rms_Bn_over_B",
                lane=reconstruction_lane,
                value=float(reconstruction["validation_rms_Bn_over_B"]),
                relation=Relation.LE,
                limit=bn_limit,
                authority=str(reconstruction["authority"]),
                source="results/sfr4_integrated/...v090.json:workstreams.1_physical_coil_field.held_out_hybrid_reconstruction",
            ),
        ),
    )

    iota_obs, excursion_obs = topology.observations
    bn_obs = held_out.observations[0]
    if iota_obs.value <= 0 or bn_limit <= 0:
        raise ValueError("SFR-4 magnetic evidence is outside SFR-5 diagnostic domain")

    diagnostics = {
        "iota_factor_to_minimum_gate": iota_min / iota_obs.value,
        "excursion_slack_fraction_of_limit": excursion_obs.normalized_slack,
        "normal_field_factor_over_limit": bn_obs.value / bn_limit,
        "sfr4_candidate_count": float(coil["candidate_count"]),
        "sfr4_combined_pass_count": float(coil["combined_pass_count"]),
    }
    rationale = (
        f"The SFR-4 helical topology lane needs {diagnostics['iota_factor_to_minimum_gate']:.3f}x its present mean transform just to reach the minimum gate.",
        f"That same lane retains only {100.0 * diagnostics['excursion_slack_fraction_of_limit']:.2f}% normalized excursion slack before its declared nestedness ceiling.",
        f"The independent held-out richer basis is {diagnostics['normal_field_factor_over_limit']:.3f}x above its RMS normal-field limit.",
        "The topology and held-out reconstruction values come from different reduced representations and are not merged into a fictitious physical coil set.",
        "The evidence rejects brute-force continuation of the present fixed helical/fixed-basis family as the preferred next move; it does not reject stellarators or fusion.",
    )
    return MagneticAutopsy(
        lanes=(topology, held_out),
        decision=ArchitectureDecision.FAMILY_SWITCH_REQUIRED,
        rationale=rationale,
        next_families=next_families,
        diagnostics=diagnostics,
    )


def run_sfr5_campaign(
    raw: dict[str, Any],
    sfr4_result: dict[str, Any],
    sfr4_config: dict[str, Any],
) -> dict[str, Any]:
    errors = validate_sfr5_config(raw)
    if errors:
        raise ValueError("; ".join(errors))

    next_families = tuple(str(x) for x in raw["search_policy"]["candidate_families"])
    autopsy = magnetic_autopsy_from_sfr4(
        sfr4_result,
        sfr4_config,
        next_families=next_families,
    )

    observations = tuple(
        obs for lane in autopsy.lanes for obs in lane.observations
    )
    pressure_state = AugmentedLagrangianState(rho=float(raw["constraint_pressure"]["rho"]))
    pressure_state.update(observations)
    pressure = {
        obs.constraint_id: pressure_state.pressure(obs)
        for obs in observations
    }

    record = RejectedFamilyRecord.create(
        family=CURRENT_FAMILY,
        reason="SFR-4 produced zero combined topology passes and the independent held-out reconstruction also failed its declared normal-field gate.",
        evidence_ids=(
            "SFR4_PHYSICAL_COIL_SCAN_80_OF_80_REJECTED",
            "SFR4_HELD_OUT_HYBRID_RECONSTRUCTION_FAIL",
        ),
        reopen_conditions=tuple(str(x) for x in raw["reopen_conditions"]),
    )
    memory = ArchitectureMemory()
    memory.reject(record)

    source_coil = sfr4_result["workstreams"]["1_physical_coil_field"]
    source_invariants = {
        "sfr4_release": sfr4_result["release"],
        "candidate_count": source_coil["candidate_count"],
        "combined_pass_count": source_coil["combined_pass_count"],
        "physical_coil_promoted": source_coil["physical_coil_promoted"],
        "held_out_reconstruction_pass": source_coil["held_out_hybrid_reconstruction"][
            "passes_reconstruction_screen"
        ],
    }

    return {
        "release": "0.10.0",
        "study_id": raw["study_id"],
        "top_level_verdict": PASS_VERDICT,
        "source_artifacts": raw["source_artifacts"],
        "source_invariants": source_invariants,
        "magnetic_autopsy": autopsy.to_dict(),
        "constraint_pressure": {
            "method": "normalized_augmented_lagrangian_pressure_without_fabricated_geometry_gradient",
            "rho": pressure_state.rho,
            "multipliers": dict(sorted(pressure_state.multipliers.items())),
            "active_pressure": dict(sorted(pressure.items())),
            "geometry_sensitivity_status": "NOT_RUN__REQUIRES_REAL_MOVABLE_GEOMETRY_EVALUATOR",
            "backward_reality_gradient_status": "NOT_COMPUTED__NO_FAKE_SENSITIVITY_CREDIT",
        },
        "rejected_family_memory": {
            "family": record.family,
            "reason": record.reason,
            "evidence_ids": list(record.evidence_ids),
            "reopen_conditions": list(record.reopen_conditions),
            "fingerprint_sha256": record.fingerprint,
            "silent_reopen_allowed": False,
        },
        "inverse_design_program": {
            "movable_design_variables": raw["movable_design_variables"],
            "candidate_families": list(next_families),
            "primary_next_family": next_families[0],
            "search_policy": raw["search_policy"],
            "required_external_methods": raw["required_external_methods"],
        },
        "promotion_status": raw["promotion_status"],
        "claim_boundary": raw["claim_boundary"],
        "earned_fusion_progress_credit_fraction": 0.0,
        "research_decision": (
            "STOP_BRUTE_FORCE_FIXED_HELICAL_FAMILY__MOVE_TO_MOVABLE_PLASMA_BOUNDARY_"
            "WINDING_SURFACE_AND_NONPLANAR_COIL_CODESIGN__PROMOTE_ONLY_WITH_EXTERNAL_EVIDENCE"
        ),
    }


def render_result_markdown(result: dict[str, Any]) -> str:
    diag = result["magnetic_autopsy"]["diagnostics"]
    lines = [
        "# SFR-5 Reality Gradient and Adaptive Inverse Design A",
        "",
        "## Executed result",
        "",
        f"Top-level verdict: `{result['top_level_verdict']}`",
        "",
        "SFR-5 derives its diagnosis from the committed v0.9 SFR-4 magnetic result and its declared thresholds. It does not merge the direct-filament topology lane with the independent held-out reconstruction lane.",
        "",
        f"- SFR-4 direct-filament cases: **{int(diag['sfr4_candidate_count'])}**.",
        f"- Combined topology passes: **{int(diag['sfr4_combined_pass_count'])}**.",
        f"- Transform factor required merely to reach the minimum iota gate: **{diag['iota_factor_to_minimum_gate']:.4f}x**.",
        f"- Remaining normalized excursion slack: **{100.0 * diag['excursion_slack_fraction_of_limit']:.3f}%** of the declared limit.",
        f"- Held-out RMS normal-field error relative to its limit: **{diag['normal_field_factor_over_limit']:.4f}x**.",
        "",
        "## Decision",
        "",
        "The present fixed helical plus fixed hybrid filament-basis family is rejected as the preferred next search family. The next program must allow the plasma boundary, winding surface, nonplanar coil geometry, and currents to move together under explicit engineering constraints.",
        "",
        "The primary next family is `single_stage_nonplanar_modular_fourier_coils_with_movable_plasma_boundary`. Winding-surface proxy/global optimization, discrete filament realization, finite-beta equilibrium, particle/transport checks, 3-D neutronics, magnet engineering, and hardware remain promotion gates rather than assumed capabilities.",
        "",
        "## Reality Gradient status",
        "",
        "SFR-5 computes normalized constraint pressure from the existing evidence but deliberately does **not** fabricate a geometry gradient. A backward gradient is only valid after a real movable-geometry evaluator supplies analytic, automatic-differentiation, or controlled finite-difference sensitivities.",
        "",
        "## Claim boundary",
        "",
        "This release does not demonstrate a viable replacement coil set, finite-beta equilibrium, kinetic confinement, TBR, ignition, net-electric power, magnet qualification, safety qualification, or hardware operation. Earned fusion-progress credit remains exactly zero.",
        "",
    ]
    return "\n".join(lines)
