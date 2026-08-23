"""Adaptive SFR-5 architecture-family search controller.

Repeated failure is treated as evidence about representation quality. The controller
can therefore request more geometry freedom or a family switch instead of silently
increasing scan density forever.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from .reality_gradient import ConstraintObservation


class SearchAction(StrEnum):
    REFINE_CURRENT_FAMILY = "refine_current_family"
    ADD_DEGREES_OF_FREEDOM = "add_degrees_of_freedom"
    SWITCH_ARCHITECTURE_FAMILY = "switch_architecture_family"
    PROMOTE_SOLVER_AUTHORITY = "promote_solver_authority"
    HOLD_FOR_MISSING_EVIDENCE = "hold_for_missing_evidence"


@dataclass(frozen=True, slots=True)
class IterationEvidence:
    iteration: int
    family: str
    observations: tuple[ConstraintObservation, ...]
    objective: float

    def __post_init__(self) -> None:
        if self.iteration < 1:
            raise ValueError("iteration must be >= 1")
        if not self.family.strip():
            raise ValueError("family must be non-empty")
        if not self.observations:
            raise ValueError("observations must be non-empty")

    @property
    def max_violation(self) -> float:
        return max((x.normalized_violation for x in self.observations), default=0.0)

    @property
    def failed_ids(self) -> tuple[str, ...]:
        return tuple(sorted(x.constraint_id for x in self.observations if not x.passed))


@dataclass(frozen=True, slots=True)
class SearchDecision:
    action: SearchAction
    reason: str
    failed_ids: tuple[str, ...]


@dataclass(slots=True)
class ArchitectureSearchController:
    """Detect stagnation and representation failure from evidence history."""

    stagnation_window: int = 4
    minimum_relative_improvement: float = 0.05
    history: list[IterationEvidence] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.stagnation_window < 2:
            raise ValueError("stagnation_window must be >= 2")
        if not 0.0 <= self.minimum_relative_improvement <= 1.0:
            raise ValueError("minimum_relative_improvement must be in [0, 1]")

    def add(self, evidence: IterationEvidence) -> None:
        if self.history and evidence.iteration <= self.history[-1].iteration:
            raise ValueError("iterations must be strictly increasing")
        self.history.append(evidence)

    def decide(self) -> SearchDecision:
        if not self.history:
            return SearchDecision(
                SearchAction.HOLD_FOR_MISSING_EVIDENCE,
                "No evaluated candidates.",
                (),
            )

        latest = self.history[-1]
        if latest.max_violation == 0.0:
            return SearchDecision(
                SearchAction.PROMOTE_SOLVER_AUTHORITY,
                "Current reduced constraints pass; move to a higher-authority solver without claiming physical closure.",
                latest.failed_ids,
            )

        if len(self.history) < self.stagnation_window:
            return SearchDecision(
                SearchAction.REFINE_CURRENT_FAMILY,
                "Insufficient history to diagnose structural stagnation.",
                latest.failed_ids,
            )

        window = self.history[-self.stagnation_window :]
        same_family = len({x.family for x in window}) == 1
        same_failures = len({x.failed_ids for x in window}) == 1
        start = max(window[0].max_violation, 1e-12)
        improvement = (window[0].max_violation - window[-1].max_violation) / start

        if same_family and same_failures and improvement < self.minimum_relative_improvement:
            return SearchDecision(
                SearchAction.SWITCH_ARCHITECTURE_FAMILY,
                (
                    f"Dominant failures persisted for {self.stagnation_window} evaluations "
                    f"with only {improvement:.3%} relative violation improvement."
                ),
                latest.failed_ids,
            )
        if same_family and same_failures:
            return SearchDecision(
                SearchAction.ADD_DEGREES_OF_FREEDOM,
                "The family is improving but the same constraints remain active; expand geometry before increasing brute-force sampling density.",
                latest.failed_ids,
            )
        return SearchDecision(
            SearchAction.REFINE_CURRENT_FAMILY,
            "Failure identity is still changing, so structural stagnation is not established.",
            latest.failed_ids,
        )
