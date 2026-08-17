from __future__ import annotations

from .external import ExternalSolverStatus
from .models import CandidateMetrics, GateResult, PocVerdict


STAGES = (
    "geometry_hypothesis",
    "magnetic_candidate",
    "confinement_candidate",
    "plasma_candidate",
    "fusion_performance_candidate",
)


def evaluate_reduced_gates(
    candidate: CandidateMetrics,
    baseline: CandidateMetrics,
    external: tuple[ExternalSolverStatus, ...],
) -> PocVerdict:
    improvement = (baseline.quick_objective - candidate.quick_objective) / max(
        abs(baseline.quick_objective), 1e-12
    )
    gates = [
        GateResult(
            "composite_improvement",
            "PASS" if improvement >= 0.02 else "FAIL",
            improvement,
            ">= 0.02",
            "Predeclared reduced-order advantage threshold; matched baseline uses equal optimizer budget.",
        ),
        GateResult(
            "bounce_action_proxy",
            "PASS"
            if candidate.omnigenity.action_variation_mean <= baseline.omnigenity.action_variation_mean
            else "FAIL",
            candidate.omnigenity.action_variation_mean,
            baseline.omnigenity.action_variation_mean,
            "Candidate may not buy composite score by worsening the trapped-particle screening proxy.",
        ),
        GateResult(
            "field_line_escape",
            "PASS" if candidate.trace.escape_fraction <= baseline.trace.escape_fraction + 1e-12 else "FAIL",
            candidate.trace.escape_fraction,
            baseline.trace.escape_fraction,
            "Reduced field-line screen must not increase escape fraction.",
        ),
        GateResult(
            "engineering_burden",
            "PASS"
            if candidate.engineering.engineering_burden_score
            <= 1.10 * baseline.engineering.engineering_burden_score
            else "FAIL",
            candidate.engineering.engineering_burden_score,
            1.10 * baseline.engineering.engineering_burden_score,
            "Candidate is allowed at most 10% higher screening-only engineering burden.",
        ),
    ]
    reduced_pass = all(g.status == "PASS" for g in gates)
    external_available = {s.name: s.available for s in external}
    high_fidelity_ready = bool(external_available.get("DESC") and external_available.get("SIMSOPT"))
    if reduced_pass:
        reduced_verdict = "PASS_REDUCED_MODEL"
        statement = (
            "The C6 seed passes the repository's reduced-order gate. This does not promote it to a "
            "magnetic or confinement candidate until equilibrium and coil-field validation are run."
        )
    else:
        reduced_verdict = "FAIL_OR_INCONCLUSIVE"
        statement = (
            "The C6 seed does not clear every predeclared reduced-order advantage gate. The hypothesis "
            "remains a geometry experiment and must not be described as a confinement improvement."
        )
    if high_fidelity_ready and reduced_pass:
        stage = "geometry_hypothesis"
    else:
        stage = "geometry_hypothesis"
    return PocVerdict(reduced_verdict, stage, tuple(gates), statement)
