"""External solver contracts. Presence is checked; scientific results are never fabricated."""
from __future__ import annotations

from dataclasses import dataclass
from importlib.util import find_spec


@dataclass(frozen=True)
class SolverContract:
    name: str
    import_name: str | None
    role: str
    minimum_gate: str

    def locally_available(self) -> bool:
        return self.import_name is not None and find_spec(self.import_name) is not None


SOLVERS: tuple[SolverContract, ...] = (
    SolverContract("DESC", "desc", "3-D MHD equilibrium and differentiable optimization", "G1_EQUILIBRIUM"),
    SolverContract("SIMSOPT", "simsopt", "coil, field, orbit and optimization framework", "G2_COILS"),
    SolverContract("VMEC++", "vmecpp", "independent ideal-MHD equilibrium cross-check", "G1_EQUILIBRIUM"),
    SolverContract("FIRM3D", "firm3d", "energetic-particle guiding-center transport", "G3_ORBITS"),
    SolverContract("GX", None, "nonlinear gyrokinetic turbulent flux", "G4_TURBULENCE"),
    SolverContract("stella", None, "independent stellarator gyrokinetic cross-check", "G4_TURBULENCE"),
    SolverContract("OpenMC", "openmc", "3-D neutronics / shielding / heating", "G7_NEUTRONICS"),
    SolverContract("Raytrax", None, "ECRH ray/deposition model", "G6_RF"),
)
