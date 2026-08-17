"""Hard promotion gates for the multi-fidelity IX-Fusion vNext search."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .authority import Authority, EvidenceRef


@dataclass(frozen=True)
class GateSpec:
    gate_id: str
    required_authority: Authority
    required_evidence_ids: tuple[str, ...]


@dataclass(frozen=True)
class GateVerdict:
    gate_id: str
    passed: bool
    missing: tuple[str, ...]
    insufficient_authority: tuple[str, ...]
    failed: tuple[str, ...]


def evaluate_gate(spec: GateSpec, evidence: Iterable[EvidenceRef]) -> GateVerdict:
    by_id = {item.evidence_id: item for item in evidence}
    missing: list[str] = []
    insufficient: list[str] = []
    failed: list[str] = []
    for evidence_id in spec.required_evidence_ids:
        item = by_id.get(evidence_id)
        if item is None:
            missing.append(evidence_id)
        elif not item.passed:
            failed.append(evidence_id)
        elif item.authority < spec.required_authority:
            insufficient.append(evidence_id)
    passed = not missing and not insufficient and not failed
    return GateVerdict(
        gate_id=spec.gate_id,
        passed=passed,
        missing=tuple(missing),
        insufficient_authority=tuple(insufficient),
        failed=tuple(failed),
    )
