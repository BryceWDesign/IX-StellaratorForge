"""Evidence-authority types for IX-Fusion vNext.

The module deliberately separates computational convenience from scientific authority.
A reduced-order result cannot silently satisfy a higher-fidelity gate.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum


class Authority(IntEnum):
    HYPOTHESIS = 0
    REDUCED_MODEL = 1
    EQUILIBRIUM_SOLVER = 2
    COIL_REALIZATION = 3
    ORBIT_TRANSPORT = 4
    MULTIPHYSICS = 5
    EXPERIMENTAL = 6


@dataclass(frozen=True)
class EvidenceRef:
    evidence_id: str
    authority: Authority
    passed: bool
    source: str
    note: str = ""

    def satisfies(self, required: Authority) -> bool:
        return self.passed and self.authority >= required
