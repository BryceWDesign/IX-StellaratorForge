"""Exact source-term and breeding-coverage constraints before OpenMC transport."""
from __future__ import annotations

from dataclasses import asdict, dataclass

from .physics import dt_reaction_ledger


@dataclass(frozen=True)
class BreedingCoverageConstraint:
    fusion_power_MW: float
    global_tbr_target: float
    breeding_surface_coverage_fraction: float
    required_local_tbr_if_uncovered_regions_breed_zero: float
    neutron_power_MW: float
    neutron_source_rate_s: float
    tritium_burn_kg_per_day: float
    required_bred_tritium_kg_per_day: float
    authority: str = "exact_source_and_geometric_coverage_bound_not_neutron_transport"


def breeding_coverage_constraint(*, fusion_power_MW: float, global_tbr_target: float, coverage_fraction: float) -> BreedingCoverageConstraint:
    if fusion_power_MW <= 0 or global_tbr_target <= 0 or not (0 < coverage_fraction <= 1):
        raise ValueError("invalid breeding constraint inputs")
    ledger = dt_reaction_ledger(fusion_power_MW)
    return BreedingCoverageConstraint(
        fusion_power_MW=fusion_power_MW,
        global_tbr_target=global_tbr_target,
        breeding_surface_coverage_fraction=coverage_fraction,
        required_local_tbr_if_uncovered_regions_breed_zero=global_tbr_target / coverage_fraction,
        neutron_power_MW=ledger.neutron_power_MW,
        neutron_source_rate_s=ledger.reaction_rate_per_s,
        tritium_burn_kg_per_day=ledger.tritium_burn_kg_per_day,
        required_bred_tritium_kg_per_day=ledger.tritium_burn_kg_per_day * global_tbr_target,
    )


def coverage_sweep(*, fusion_power_MW: float, global_tbr_target: float) -> list[BreedingCoverageConstraint]:
    return [breeding_coverage_constraint(fusion_power_MW=fusion_power_MW, global_tbr_target=global_tbr_target, coverage_fraction=f) for f in (1.0, 0.95, 0.90, 0.85, 0.80, 0.75)]


def as_jsonable(result: BreedingCoverageConstraint) -> dict[str, object]:
    return asdict(result)
