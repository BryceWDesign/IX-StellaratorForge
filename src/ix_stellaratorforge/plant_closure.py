"""Conditional SFR-1 net-electric closure equations."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from math import sqrt


@dataclass(frozen=True)
class PlantClosureThresholds:
    current_fusion_power_MW: float
    current_net_electric_MW: float
    fusion_power_required_for_net_floor_MW: float
    gross_efficiency_required_at_current_fusion: float
    recirculating_power_max_for_net_floor_at_target_MW: float
    beta_required_for_net_floor_uniform_scaling: float
    beta_required_for_fusion_target_uniform_scaling: float
    target_net_electric_MW: float
    authority: str = "algebraic_conditional_plant_closure_not_integrated_reactor_prediction"


def plant_thresholds(
    *, current_fusion_power_MW: float, target_fusion_power_MW: float, current_beta: float,
    blanket_multiplier: float, gross_efficiency: float, recirc_MW: float, net_floor_MW: float,
) -> PlantClosureThresholds:
    if min(current_fusion_power_MW, target_fusion_power_MW, current_beta, blanket_multiplier, gross_efficiency) <= 0 or recirc_MW < 0:
        raise ValueError("invalid plant closure inputs")
    current_net = current_fusion_power_MW * blanket_multiplier * gross_efficiency - recirc_MW
    required_fusion = (net_floor_MW + recirc_MW) / (blanket_multiplier * gross_efficiency)
    required_eff = (net_floor_MW + recirc_MW) / (current_fusion_power_MW * blanket_multiplier)
    recirc_max = target_fusion_power_MW * blanket_multiplier * gross_efficiency - net_floor_MW
    # In the uniform fixed-T beta screen P_fusion scales as pressure^2 ~ beta^2.
    beta_net = current_beta * sqrt(required_fusion / current_fusion_power_MW)
    beta_target = current_beta * sqrt(target_fusion_power_MW / current_fusion_power_MW)
    target_net = target_fusion_power_MW * blanket_multiplier * gross_efficiency - recirc_MW
    return PlantClosureThresholds(
        current_fusion_power_MW=current_fusion_power_MW,
        current_net_electric_MW=current_net,
        fusion_power_required_for_net_floor_MW=required_fusion,
        gross_efficiency_required_at_current_fusion=required_eff,
        recirculating_power_max_for_net_floor_at_target_MW=recirc_max,
        beta_required_for_net_floor_uniform_scaling=beta_net,
        beta_required_for_fusion_target_uniform_scaling=beta_target,
        target_net_electric_MW=target_net,
    )


def as_jsonable(result: PlantClosureThresholds) -> dict[str, object]:
    return asdict(result)
