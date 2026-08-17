from __future__ import annotations

import importlib.util
import shutil
from dataclasses import dataclass


@dataclass(frozen=True)
class ExternalSolverStatus:
    name: str
    available: bool
    mechanism: str
    purpose: str


def detect_external_solvers() -> tuple[ExternalSolverStatus, ...]:
    return (
        ExternalSolverStatus(
            "DESC",
            importlib.util.find_spec("desc") is not None,
            "python module: desc",
            "3-D MHD equilibrium and optimization",
        ),
        ExternalSolverStatus(
            "SIMSOPT",
            importlib.util.find_spec("simsopt") is not None,
            "python module: simsopt",
            "stellarator optimization and coil/field tooling",
        ),
        ExternalSolverStatus(
            "VMEC",
            shutil.which("xvmec2000") is not None or shutil.which("vmec") is not None,
            "CLI executable if installed by evaluator",
            "3-D ideal-MHD equilibrium",
        ),
    )
