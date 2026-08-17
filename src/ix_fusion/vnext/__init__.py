"""IX-Fusion vNext: multi-family, multi-fidelity scientific promotion layer."""
from .authority import Authority, EvidenceRef
from .gates import GateSpec, GateVerdict, evaluate_gate
from .protocol import GATES
from .seed_league import SeedFamily, load_seed_league
from .solver_registry import SOLVERS, SolverContract

__all__ = [
    "Authority",
    "EvidenceRef",
    "GateSpec",
    "GateVerdict",
    "GATES",
    "SOLVERS",
    "SeedFamily",
    "SolverContract",
    "evaluate_gate",
    "load_seed_league",
]
