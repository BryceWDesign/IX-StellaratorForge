"""Fail-closed constraint-pressure primitives for SFR-5 inverse design.

The Reality Gradient layer is deliberately solver-agnostic. It does not claim a
plasma equilibrium, confinement, buildable coils, ignition, or fusion. Its job is
to preserve constraint identity and evidence authority, quantify how badly a
candidate misses declared gates, and map those failures back onto upstream design
degrees of freedom when real sensitivities are available.

Engineering failure is therefore retained as design information instead of being
collapsed to a bare boolean.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from hashlib import sha256
import json
from typing import Callable, Iterable, Sequence

import numpy as np


class Relation(StrEnum):
    """Supported constraint relations."""

    LE = "le"
    GE = "ge"
    RANGE = "range"


class ArchitectureDecision(StrEnum):
    """Fail-closed architecture decisions emitted by an autopsy."""

    CONTINUE = "continue"
    HOLD = "hold"
    FAMILY_SWITCH_REQUIRED = "family_switch_required"
    PROMOTE_TO_HIGHER_AUTHORITY = "promote_to_higher_authority"


@dataclass(frozen=True, slots=True)
class ConstraintObservation:
    """One measured constraint in one explicit evidence lane."""

    constraint_id: str
    lane: str
    value: float
    relation: Relation
    limit: float | None = None
    lower: float | None = None
    upper: float | None = None
    unit: str = "dimensionless"
    authority: str = "unknown"
    source: str = "unknown"
    uncertainty_fraction: float = 0.0

    def __post_init__(self) -> None:
        if not self.constraint_id.strip() or not self.lane.strip():
            raise ValueError("constraint_id and lane must be non-empty")
        if not np.isfinite(self.value):
            raise ValueError("constraint value must be finite")
        if self.uncertainty_fraction < 0:
            raise ValueError("uncertainty_fraction must be non-negative")
        if self.relation in (Relation.LE, Relation.GE):
            if self.limit is None or not np.isfinite(self.limit):
                raise ValueError("LE/GE constraints require a finite limit")
        elif self.relation is Relation.RANGE:
            if (
                self.lower is None
                or self.upper is None
                or not np.isfinite(self.lower)
                or not np.isfinite(self.upper)
                or self.lower >= self.upper
            ):
                raise ValueError("RANGE requires finite lower < upper")

    @property
    def passed(self) -> bool:
        if self.relation is Relation.LE:
            return self.value <= float(self.limit)
        if self.relation is Relation.GE:
            return self.value >= float(self.limit)
        return float(self.lower) <= self.value <= float(self.upper)

    @property
    def signed_residual(self) -> float:
        """Return c(x) in canonical inequality form c(x) <= 0."""

        if self.relation is Relation.LE:
            return self.value - float(self.limit)
        if self.relation is Relation.GE:
            return float(self.limit) - self.value
        assert self.lower is not None and self.upper is not None
        return max(self.lower - self.value, self.value - self.upper)

    @property
    def scale(self) -> float:
        if self.relation in (Relation.LE, Relation.GE):
            return max(abs(float(self.limit)), 1e-12)
        assert self.lower is not None and self.upper is not None
        return max(abs(self.lower), abs(self.upper), self.upper - self.lower, 1e-12)

    @property
    def normalized_violation(self) -> float:
        return max(0.0, self.signed_residual) / self.scale

    @property
    def normalized_slack(self) -> float:
        return max(0.0, -self.signed_residual) / self.scale

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["relation"] = self.relation.value
        payload["passed"] = self.passed
        payload["signed_residual"] = self.signed_residual
        payload["normalized_violation"] = self.normalized_violation
        payload["normalized_slack"] = self.normalized_slack
        return payload


@dataclass(frozen=True, slots=True)
class LaneAutopsy:
    """Constraint observations that genuinely belong to one model/evidence lane."""

    lane: str
    observations: tuple[ConstraintObservation, ...]

    @property
    def failures(self) -> tuple[ConstraintObservation, ...]:
        return tuple(x for x in self.observations if not x.passed)

    @property
    def passes(self) -> tuple[ConstraintObservation, ...]:
        return tuple(x for x in self.observations if x.passed)

    @property
    def max_violation(self) -> float:
        return max((x.normalized_violation for x in self.observations), default=0.0)

    def dominant_failure(self) -> ConstraintObservation | None:
        if not self.failures:
            return None
        return max(self.failures, key=lambda x: x.normalized_violation)


@dataclass(slots=True)
class AugmentedLagrangianState:
    """Multiplier state for normalized inequality constraints c_i(x) <= 0."""

    rho: float = 2.0
    multipliers: dict[str, float] = field(default_factory=dict)

    def update(self, observations: Iterable[ConstraintObservation]) -> None:
        if self.rho <= 0:
            raise ValueError("rho must be positive")
        for obs in observations:
            lam = self.multipliers.get(obs.constraint_id, 0.0)
            normalized_c = obs.signed_residual / obs.scale
            self.multipliers[obs.constraint_id] = max(0.0, lam + self.rho * normalized_c)

    def pressure(self, observation: ConstraintObservation) -> float:
        """Return active normalized pressure including declared uncertainty."""

        c = observation.signed_residual / observation.scale
        lam = self.multipliers.get(observation.constraint_id, 0.0)
        uncertainty = 1.0 + observation.uncertainty_fraction
        return max(0.0, lam + self.rho * c) * uncertainty


@dataclass(frozen=True, slots=True)
class SensitivityResult:
    variable_names: tuple[str, ...]
    constraint_ids: tuple[str, ...]
    jacobian: np.ndarray

    def __post_init__(self) -> None:
        expected = (len(self.constraint_ids), len(self.variable_names))
        if self.jacobian.shape != expected:
            raise ValueError(f"jacobian shape {self.jacobian.shape} != {expected}")
        if not np.all(np.isfinite(self.jacobian)):
            raise ValueError("jacobian must be finite")


def finite_difference_sensitivities(
    x: Sequence[float],
    *,
    variable_names: Sequence[str],
    evaluator: Callable[[np.ndarray], Sequence[ConstraintObservation]],
    relative_step: float = 1e-4,
) -> SensitivityResult:
    """Finite-difference Jacobian of normalized signed constraint residuals.

    Production differentiable solvers should provide analytic or automatic
    derivatives. This deterministic fallback exists for black-box low-authority
    components and for testing the controller contract.
    """

    point = np.asarray(x, dtype=float)
    if point.ndim != 1 or len(point) != len(variable_names):
        raise ValueError("x and variable_names must have equal 1-D length")
    if not np.all(np.isfinite(point)):
        raise ValueError("x must be finite")
    if relative_step <= 0:
        raise ValueError("relative_step must be positive")

    base = tuple(evaluator(point.copy()))
    ids = tuple(o.constraint_id for o in base)
    if not ids or len(set(ids)) != len(ids):
        raise ValueError("evaluator must return unique constraint ids")

    def normalized_map(obs: Sequence[ConstraintObservation]) -> dict[str, float]:
        return {o.constraint_id: o.signed_residual / o.scale for o in obs}

    jac = np.zeros((len(base), len(point)), dtype=float)
    for j in range(len(point)):
        h = relative_step * max(1.0, abs(point[j]))
        xp = point.copy()
        xm = point.copy()
        xp[j] += h
        xm[j] -= h
        plus = normalized_map(tuple(evaluator(xp)))
        minus = normalized_map(tuple(evaluator(xm)))
        if set(plus) != set(ids) or set(minus) != set(ids):
            raise ValueError("evaluator changed constraint identity across perturbation")
        for i, cid in enumerate(ids):
            jac[i, j] = (plus[cid] - minus[cid]) / (2.0 * h)
    return SensitivityResult(tuple(variable_names), ids, jac)


def backward_reality_gradient(
    observations: Sequence[ConstraintObservation],
    state: AugmentedLagrangianState,
    sensitivity: SensitivityResult,
) -> dict[str, float]:
    """Map active constraint pressure backward onto upstream design variables."""

    obs_by_id = {o.constraint_id: o for o in observations}
    if set(obs_by_id) != set(sensitivity.constraint_ids):
        raise ValueError("observation ids do not match sensitivity ids")
    pressure = np.array(
        [state.pressure(obs_by_id[cid]) for cid in sensitivity.constraint_ids],
        dtype=float,
    )
    grad = sensitivity.jacobian.T @ pressure
    return {
        name: float(value)
        for name, value in zip(sensitivity.variable_names, grad, strict=True)
    }


@dataclass(frozen=True, slots=True)
class RejectedFamilyRecord:
    """Auditable record preventing silent resurrection of a rejected family."""

    family: str
    reason: str
    evidence_ids: tuple[str, ...]
    reopen_conditions: tuple[str, ...]
    fingerprint: str

    @classmethod
    def create(
        cls,
        *,
        family: str,
        reason: str,
        evidence_ids: Sequence[str],
        reopen_conditions: Sequence[str],
    ) -> "RejectedFamilyRecord":
        if not family.strip() or not reason.strip() or not evidence_ids:
            raise ValueError("family, reason, and at least one evidence id are required")
        payload = {
            "family": family,
            "reason": reason,
            "evidence_ids": list(evidence_ids),
            "reopen_conditions": list(reopen_conditions),
        }
        digest = sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        return cls(
            family,
            reason,
            tuple(evidence_ids),
            tuple(reopen_conditions),
            digest,
        )


@dataclass(slots=True)
class ArchitectureMemory:
    """Minimal fail-closed family rejection memory."""

    rejected: dict[str, RejectedFamilyRecord] = field(default_factory=dict)

    def reject(self, record: RejectedFamilyRecord) -> None:
        self.rejected[record.family] = record

    def may_reopen(self, family: str, supplied_new_evidence: Sequence[str]) -> bool:
        record = self.rejected.get(family)
        if record is None:
            return True
        supplied = set(supplied_new_evidence)
        return bool(supplied) and any(
            condition in supplied for condition in record.reopen_conditions
        )
