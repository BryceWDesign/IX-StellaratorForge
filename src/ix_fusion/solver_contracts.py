from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SolverRunManifest:
    solver: str
    solver_version: str
    authority: str
    converged: bool
    input_hashes: dict[str, str]
    output_hashes: dict[str, str]
    metrics: dict[str, Any]
    notes: tuple[str, ...] = ()


REQUIRED_METRICS: dict[str, tuple[str, ...]] = {
    "equilibrium": ("force_balance_or_convergence", "rotational_transform_profile"),
    "coil_realization": ("normal_field_error", "minimum_coil_spacing_or_equivalent"),
    "particle_orbits": ("loss_fraction", "integration_horizon"),
    "stability": ("stability_metric",),
    "transport": ("transport_metric",),
    "rf_full_wave": ("deposition_or_coupling_metric",),
    "neutronics": ("shielding_metric", "breeding_or_fuel_cycle_metric"),
}


def validate_solver_run(manifest: SolverRunManifest) -> list[str]:
    errors: list[str] = []
    if not manifest.solver.strip():
        errors.append("solver name is required")
    if not manifest.solver_version.strip():
        errors.append("solver version is required")
    if manifest.authority not in REQUIRED_METRICS:
        errors.append(f"unsupported authority: {manifest.authority}")
        return errors
    if not manifest.converged:
        errors.append("solver run did not converge; authority cannot be promoted")
    if not manifest.input_hashes:
        errors.append("input hashes are required")
    if not manifest.output_hashes:
        errors.append("output hashes are required")
    for metric in REQUIRED_METRICS[manifest.authority]:
        if metric not in manifest.metrics:
            errors.append(f"missing required metric for {manifest.authority}: {metric}")
    return errors
