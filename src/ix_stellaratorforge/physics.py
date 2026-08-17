
"""Transparent screening arithmetic for SFR-1 Rev A.

These equations provide consistency checks only. They are not substitutes for equilibrium,
transport, neutronics, thermal-hydraulic, structural, or power-cycle solvers.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import pi

ELECTRON_CHARGE_C = 1.602176634e-19
ELECTRON_MASS_KG = 9.1093837139e-31
ATOMIC_MASS_UNIT_KG = 1.66053906660e-27
TRITIUM_ATOMIC_MASS_U = 3.01604928199
DEUTERIUM_ATOMIC_MASS_U = 2.01410177812
MU0_H_PER_M = 4.0e-7 * pi
DT_TOTAL_ENERGY_MEV = 17.6
DT_NEUTRON_ENERGY_MEV = 14.1
DT_ALPHA_ENERGY_MEV = 3.5
MEV_TO_J = 1.0e6 * ELECTRON_CHARGE_C
SECONDS_PER_DAY = 86400.0


@dataclass(frozen=True)
class DTReactionLedger:
    fusion_power_MW: float
    reaction_rate_per_s: float
    neutron_power_MW: float
    alpha_power_MW: float
    tritium_burn_kg_per_day: float
    deuterium_burn_kg_per_day: float


@dataclass(frozen=True)
class PowerBalance:
    fusion_power_MW: float
    blanket_multiplier: float
    thermal_power_MW_screening: float
    gross_efficiency: float
    gross_electric_MW_screening: float
    recirculating_power_MW_ceiling: float
    net_electric_MW_at_recirc_ceiling: float


@dataclass(frozen=True)
class PlasmaScreeningLedger:
    aspect_ratio: float
    circular_torus_volume_m3: float
    circular_torus_surface_area_m2: float
    neutron_wall_load_MW_m2_screening: float
    magnetic_pressure_Pa: float
    volume_average_plasma_pressure_Pa: float
    equal_temperature_density_m3_screening: float


def dt_reaction_ledger(fusion_power_MW: float) -> DTReactionLedger:
    if fusion_power_MW <= 0:
        raise ValueError("fusion power must be positive")
    fusion_power_W = fusion_power_MW * 1.0e6
    reaction_energy_J = DT_TOTAL_ENERGY_MEV * MEV_TO_J
    rate = fusion_power_W / reaction_energy_J
    tritium_mass_kg = TRITIUM_ATOMIC_MASS_U * ATOMIC_MASS_UNIT_KG
    deuterium_mass_kg = DEUTERIUM_ATOMIC_MASS_U * ATOMIC_MASS_UNIT_KG
    return DTReactionLedger(
        fusion_power_MW=fusion_power_MW,
        reaction_rate_per_s=rate,
        neutron_power_MW=fusion_power_MW * DT_NEUTRON_ENERGY_MEV / DT_TOTAL_ENERGY_MEV,
        alpha_power_MW=fusion_power_MW * DT_ALPHA_ENERGY_MEV / DT_TOTAL_ENERGY_MEV,
        tritium_burn_kg_per_day=rate * tritium_mass_kg * SECONDS_PER_DAY,
        deuterium_burn_kg_per_day=rate * deuterium_mass_kg * SECONDS_PER_DAY,
    )


def power_balance(
    fusion_power_MW: float,
    blanket_multiplier: float,
    gross_efficiency: float,
    recirculating_power_MW_ceiling: float,
) -> PowerBalance:
    if fusion_power_MW <= 0:
        raise ValueError("fusion power must be positive")
    if blanket_multiplier < 1.0:
        raise ValueError("screening blanket multiplier must be at least one")
    if not 0.0 < gross_efficiency < 1.0:
        raise ValueError("gross efficiency must be between zero and one")
    if recirculating_power_MW_ceiling < 0:
        raise ValueError("recirculating power cannot be negative")
    thermal = fusion_power_MW * blanket_multiplier
    gross = thermal * gross_efficiency
    return PowerBalance(
        fusion_power_MW=fusion_power_MW,
        blanket_multiplier=blanket_multiplier,
        thermal_power_MW_screening=thermal,
        gross_efficiency=gross_efficiency,
        gross_electric_MW_screening=gross,
        recirculating_power_MW_ceiling=recirculating_power_MW_ceiling,
        net_electric_MW_at_recirc_ceiling=gross - recirculating_power_MW_ceiling,
    )


def ecrh_frequency_ghz(magnetic_field_T: float, harmonic: int = 1) -> float:
    if magnetic_field_T <= 0:
        raise ValueError("magnetic field must be positive")
    if harmonic < 1:
        raise ValueError("harmonic must be at least one")
    frequency_hz = harmonic * ELECTRON_CHARGE_C * magnetic_field_T / (2.0 * pi * ELECTRON_MASS_KG)
    return frequency_hz / 1.0e9


def plasma_screening_ledger(
    major_radius_m: float,
    minor_radius_m: float,
    magnetic_field_T: float,
    beta: float,
    fusion_power_MW: float,
    electron_temperature_keV: float,
    ion_temperature_keV: float,
) -> PlasmaScreeningLedger:
    if min(major_radius_m, minor_radius_m, magnetic_field_T, fusion_power_MW) <= 0:
        raise ValueError("geometry, field and fusion power must be positive")
    if not 0.0 < beta < 1.0:
        raise ValueError("beta must be between zero and one")
    if min(electron_temperature_keV, ion_temperature_keV) <= 0:
        raise ValueError("screening temperatures must be positive")

    # Circular-torus proxies only. A solved stellarator surface will differ.
    volume = 2.0 * pi**2 * major_radius_m * minor_radius_m**2
    surface_area = 4.0 * pi**2 * major_radius_m * minor_radius_m
    neutron_power_MW = fusion_power_MW * DT_NEUTRON_ENERGY_MEV / DT_TOTAL_ENERGY_MEV
    magnetic_pressure = magnetic_field_T**2 / (2.0 * MU0_H_PER_M)
    plasma_pressure = beta * magnetic_pressure
    te_J = electron_temperature_keV * 1.0e3 * ELECTRON_CHARGE_C
    ti_J = ion_temperature_keV * 1.0e3 * ELECTRON_CHARGE_C
    # Screening assumes singly charged, equal electron/total-ion number densities and no impurities.
    density = plasma_pressure / (te_J + ti_J)
    return PlasmaScreeningLedger(
        aspect_ratio=major_radius_m / minor_radius_m,
        circular_torus_volume_m3=volume,
        circular_torus_surface_area_m2=surface_area,
        neutron_wall_load_MW_m2_screening=neutron_power_MW / surface_area,
        magnetic_pressure_Pa=magnetic_pressure,
        volume_average_plasma_pressure_Pa=plasma_pressure,
        equal_temperature_density_m3_screening=density,
    )
