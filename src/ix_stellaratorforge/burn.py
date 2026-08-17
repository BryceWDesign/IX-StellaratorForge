"""D-T burn and stellarator confinement scoping for IX-StellaratorForge.

Authority: analytical / empirical-screening.  Bosch-Hale thermal reactivity is used for
Maxwellian D-T ions.  ISS04 is used only as an empirical confinement reference, not as a
replacement for gyrokinetic or transport simulation.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from math import exp, pi, sqrt

E_CHARGE = 1.602176634e-19
MU0 = 4e-7 * pi
DT_ENERGY_J = 17.6e6 * E_CHARGE
DT_ALPHA_FRACTION = 3.5 / 17.6


@dataclass(frozen=True)
class BurnPoint:
    temperature_keV: float
    beta: float
    field_T: float
    volume_m3: float
    pressure_Pa: float
    ion_density_m3: float
    dt_reactivity_m3_s: float
    fusion_power_MW_uniform: float
    target_fusion_power_MW: float
    target_to_uniform_ratio: float


@dataclass(frozen=True)
class ConfinementPoint:
    plasma_gain_Q: float | None
    iota_screen: float
    total_thermal_energy_MJ: float
    alpha_heating_MW: float
    auxiliary_heating_MW: float
    required_tau_E_s: float
    iss04_tau_E_H1_s: float
    required_H_ISS04: float


def bosch_hale_dt_reactivity(temperature_keV: float) -> float:
    """Return Maxwellian D-T <sigma v> in m^3/s using Bosch-Hale (1992).

    Validity of the published fit is 0.2-100 keV. Coefficients follow Table VII and
    equations 12-14 of Bosch & Hale, Nuclear Fusion 32 (1992) 611.
    """
    if not 0.2 <= temperature_keV <= 100.0:
        raise ValueError("Bosch-Hale D-T fit is restricted here to 0.2-100 keV")
    c1, c2, c3, c4 = 1.17302e-9, 1.51361e-2, 7.51886e-2, 4.60643e-3
    c5, c6, c7 = 1.35000e-2, -1.06750e-4, 1.36600e-5
    bg, mrc2 = 34.3827, 1_124_656.0
    t = temperature_keV
    theta = t / (1.0 - t * (c2 + t * (c4 + t * c6)) / (1.0 + t * (c3 + t * (c5 + t * c7))))
    xi = (bg * bg / (4.0 * theta)) ** (1.0 / 3.0)
    # Bosch-Hale expression yields cm^3/s for these coefficients; convert to m^3/s.
    return c1 * theta * sqrt(xi / (mrc2 * t**3)) * exp(-3.0 * xi) * 1.0e-6


def uniform_dt_burn_point(
    *, temperature_keV: float, beta: float, field_T: float, volume_m3: float, target_fusion_power_MW: float
) -> BurnPoint:
    """Uniform-pressure 50/50 D-T burn screen.

    Te=Ti=temperature_keV, ne=ni, no impurities. It deliberately omits profile peaking,
    ash dilution, radiation, alpha redistribution, and transport. It is therefore a
    consistency screen, not a reactor prediction.
    """
    if not 0 < beta < 1 or min(field_T, volume_m3, target_fusion_power_MW) <= 0:
        raise ValueError("invalid burn inputs")
    pressure = beta * field_T**2 / (2.0 * MU0)
    kT_J = temperature_keV * 1.0e3 * E_CHARGE
    ni = pressure / (2.0 * kT_J)
    reactivity = bosch_hale_dt_reactivity(temperature_keV)
    rate_density = 0.25 * ni**2 * reactivity
    fusion_W = rate_density * DT_ENERGY_J * volume_m3
    fusion_MW = fusion_W / 1.0e6
    return BurnPoint(
        temperature_keV=temperature_keV,
        beta=beta,
        field_T=field_T,
        volume_m3=volume_m3,
        pressure_Pa=pressure,
        ion_density_m3=ni,
        dt_reactivity_m3_s=reactivity,
        fusion_power_MW_uniform=fusion_MW,
        target_fusion_power_MW=target_fusion_power_MW,
        target_to_uniform_ratio=target_fusion_power_MW / fusion_MW,
    )


def iss04_tau_E_s(*, a_m: float, R_m: float, absorbed_power_MW: float, ne_1e19_m3: float, B_T: float, iota: float, H: float = 1.0) -> float:
    """ISS04 stellarator energy confinement scaling in seconds."""
    if min(a_m, R_m, absorbed_power_MW, ne_1e19_m3, B_T, iota, H) <= 0:
        raise ValueError("ISS04 inputs must be positive")
    return 0.134 * H * a_m**2.28 * R_m**0.64 * absorbed_power_MW**(-0.61) * ne_1e19_m3**0.54 * B_T**0.84 * iota**0.41



def required_uniform_beta_for_target(burn: BurnPoint) -> float:
    """Return beta needed for target power at fixed B, T and volume in this uniform model.

    At fixed temperature, field and volume the model has P_fus proportional to beta^2.
    This is a transparent scaling diagnostic, not an MHD-stability assertion.
    """
    if burn.fusion_power_MW_uniform <= 0:
        raise ValueError("uniform fusion power must be positive")
    return burn.beta * sqrt(burn.target_fusion_power_MW / burn.fusion_power_MW_uniform)


def fixed_pressure_optimum_temperature_keV(
    *, beta: float, field_T: float, volume_m3: float, target_fusion_power_MW: float,
    lower_keV: float = 5.0, upper_keV: float = 40.0, step_keV: float = 0.1,
) -> tuple[float, float]:
    """Grid-search the temperature maximizing uniform D-T power at fixed beta/B/volume.

    Returns (temperature_keV, fusion_power_MW). The grid and assumptions are explicit so
    this remains a reproducible scoping calculation rather than an optimizer claim.
    """
    if not (0.2 <= lower_keV < upper_keV <= 100.0) or step_keV <= 0:
        raise ValueError("invalid temperature scan range")
    n = int(round((upper_keV - lower_keV) / step_keV))
    best_t = lower_keV
    best_p = -1.0
    for i in range(n + 1):
        t = min(lower_keV + i * step_keV, upper_keV)
        point = uniform_dt_burn_point(
            temperature_keV=t, beta=beta, field_T=field_T, volume_m3=volume_m3,
            target_fusion_power_MW=target_fusion_power_MW,
        )
        if point.fusion_power_MW_uniform > best_p:
            best_t, best_p = t, point.fusion_power_MW_uniform
    return best_t, best_p

def confinement_requirement(
    *, burn: BurnPoint, major_radius_m: float, minor_radius_m: float, iota_screen: float, plasma_gain_Q: float | None
) -> ConfinementPoint:
    """Required tau_E and ISS04 enhancement for target fusion power.

    Radiation and ash losses are omitted, so this is optimistic. Q=None represents the
    ignition limit (no external auxiliary heating in steady state).
    """
    volume = burn.volume_m3
    thermal_energy_J = 1.5 * burn.pressure_Pa * volume
    alpha_MW = burn.target_fusion_power_MW * DT_ALPHA_FRACTION
    aux_MW = 0.0 if plasma_gain_Q is None else burn.target_fusion_power_MW / plasma_gain_Q
    heating_MW = alpha_MW + aux_MW
    tau_req = thermal_energy_J / (heating_MW * 1.0e6)
    tau_h1 = iss04_tau_E_s(
        a_m=minor_radius_m,
        R_m=major_radius_m,
        absorbed_power_MW=heating_MW,
        ne_1e19_m3=burn.ion_density_m3 / 1.0e19,
        B_T=burn.field_T,
        iota=iota_screen,
    )
    return ConfinementPoint(
        plasma_gain_Q=plasma_gain_Q,
        iota_screen=iota_screen,
        total_thermal_energy_MJ=thermal_energy_J / 1.0e6,
        alpha_heating_MW=alpha_MW,
        auxiliary_heating_MW=aux_MW,
        required_tau_E_s=tau_req,
        iss04_tau_E_H1_s=tau_h1,
        required_H_ISS04=tau_req / tau_h1,
    )


def as_jsonable(obj: BurnPoint | ConfinementPoint) -> dict[str, float | None]:
    return asdict(obj)
