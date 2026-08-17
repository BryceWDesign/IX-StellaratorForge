
"""SFR-1 reactor configuration loader and invariant checks."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .physics import ecrh_frequency_ghz, power_balance


@dataclass(frozen=True)
class ReactorConfig:
    raw: dict[str, Any]

    @property
    def design_id(self) -> str:
        return str(self.raw["design_id"])


@dataclass(frozen=True)
class ReactorValidation:
    passed: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]


def load_reactor_config(path: str | Path) -> ReactorConfig:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return ReactorConfig(raw=raw)


def validate_reactor_config(config: ReactorConfig) -> ReactorValidation:
    raw = config.raw
    errors: list[str] = []
    warnings: list[str] = []

    core = raw["core_policy"]
    if core.get("selected_core") is not None:
        errors.append("Rev A must not select a core before G1-G5 comparative evidence exists")
    if core.get("privileged_core") is not None:
        errors.append("Rev A forbids a privileged core before promotion evidence exists")
    roles = [item["role"] for item in core["competitors"]]
    if roles.count("candidate") < 3:
        errors.append("at least three non-privileged physics candidates are required")
    ids = [item["id"] for item in core["competitors"]]
    if len(ids) != len(set(ids)):
        errors.append("core competitor IDs must be unique")

    env = raw["reactor_envelope"]
    if env["major_radius_m"] <= env["minor_radius_m"]:
        errors.append("major radius must exceed minor radius")
    if not 0.0 < env["volume_average_beta"] < 0.10:
        errors.append("Rev A beta must remain within the declared conservative screening envelope")

    magnet = raw["magnet_system"]
    if magnet["minimum_plasma_to_coil_distance_m_target"] < magnet["minimum_plasma_to_coil_distance_m_hard_floor"]:
        errors.append("plasma-to-coil target cannot be below the hard floor")
    if magnet["winding_strain_target_fraction"] > magnet["winding_strain_hard_ceiling_fraction"]:
        errors.append("winding strain target cannot exceed the hard ceiling")
    if magnet["maximum_field_on_conductor_T_ceiling"] < env["magnetic_field_axis_T"]:
        errors.append("on-conductor field ceiling cannot be below the on-axis target field")
    if magnet["routine_maintenance_may_remove_primary_coils"]:
        errors.append("routine maintenance is not allowed to depend on primary-coil removal")

    radial = raw["radial_build"]
    radial_sum = sum(float(v) for k, v in radial.items() if k.endswith("_m"))
    if abs(radial_sum - magnet["minimum_plasma_to_coil_distance_m_target"]) > 1e-9:
        errors.append("radial build reservation must equal the target plasma-to-coil distance")

    blanket = raw["blanket_fuel_cycle"]
    if blanket["tbr_design_target"] < blanket["tbr_hard_floor_full_3d"]:
        errors.append("TBR design target must exceed the full-3D hard floor")
    if blanket["tritium_self_sufficiency_claimed"]:
        errors.append("Rev A cannot claim tritium self-sufficiency before G7/G8 evidence")

    thermal = raw["thermal_power_conversion"]
    balance = power_balance(
        env["fusion_power_target_MW"],
        thermal["blanket_energy_multiplier_screening"],
        thermal["gross_thermal_to_electric_efficiency_target"],
        thermal["recirculating_power_MW_design_ceiling"],
    )
    if balance.net_electric_MW_at_recirc_ceiling < thermal["net_electric_power_MW_design_floor"]:
        errors.append("screening power ledger cannot meet the declared net-electric design floor")

    ecrh = raw["heating_control"]
    fundamental = ecrh_frequency_ghz(env["magnetic_field_axis_T"])
    if abs(ecrh["nominal_frequency_GHz"] - fundamental) > 5.0:
        warnings.append("nominal ECRH frequency is more than 5 GHz from the first-harmonic 6 T screening resonance")

    promotion = raw["promotion_status"]
    for gate in ("G1_EQUILIBRIUM", "G2_COILS", "G3_ORBITS", "G4_TURBULENCE", "G5_EDGE", "G6_RF", "G7_NEUTRONICS", "G8_SYSTEM", "G9_HARDWARE"):
        if promotion.get(gate) != "NOT_RUN":
            errors.append(f"{gate} must remain NOT_RUN in Rev A until matching evidence is committed")

    return ReactorValidation(passed=not errors, errors=tuple(errors), warnings=tuple(warnings))
