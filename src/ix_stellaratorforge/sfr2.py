"""SFR-2 staggered high-field / dynamic-compression screening.

Authority
---------
This module is deliberately low authority.  It combines exact geometry bookkeeping,
Bosch-Hale D-T reactivity, an ideal adiabatic radial-compression upper-bound, and ISS04
empirical stellarator confinement scaling.  It does *not* solve a 3-D equilibrium,
magnetic islands, MHD stability, RF deposition, coil fields/stress, radiation,
alpha-orbit confinement, turbulence, divertor loads, neutronics, or a plant.

The four user-specified 23/26/23/26 ft values are treated as consecutive arc-length
sectors of one closed plasma system.  They are not modeled as four independent plasma
machines connected by ducts.  No confinement credit is awarded merely for staggering.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from math import pi, sqrt
from typing import Any, Iterable

from .burn import (
    DT_ALPHA_FRACTION,
    DT_ENERGY_J,
    bosch_hale_dt_reactivity,
    iss04_tau_E_s,
    uniform_dt_burn_point,
)

FT_TO_M = 0.3048
DT_NEUTRON_FRACTION = 14.1 / 17.6
GAMMA_MONATOMIC = 5.0 / 3.0


@dataclass(frozen=True)
class SFR2Geometry:
    sector_lengths_ft: tuple[float, ...]
    sector_lengths_m: tuple[float, ...]
    total_axis_path_m: float
    equivalent_major_radius_m: float
    screening_aspect_ratio: float
    screening_minor_radius_m: float
    circular_torus_volume_m3: float
    circular_torus_surface_area_m2: float


@dataclass(frozen=True)
class CompressionState:
    radial_squeeze_fraction: float
    radial_compression_ratio: float
    minor_radius_m: float
    volume_m3: float
    ion_density_m3: float
    ion_temperature_keV: float
    pressure_Pa: float
    beta_at_fixed_B: float
    fusion_power_MW_uniform: float
    alpha_heating_MW_uniform: float
    neutron_power_MW_uniform: float
    neutron_wall_load_MW_m2_circular_proxy: float
    thermal_energy_MJ: float


@dataclass(frozen=True)
class IgnitionProxy:
    iota_2over3: float
    H_ISS04: float
    transient_confinement_retention: float
    required_tau_E_s_optimistic: float
    iss04_tau_E_s: float
    effective_tau_E_s_after_retention: float
    tau_ratio_to_optimistic_ignition: float
    required_H_if_retention_is_one: float
    minimum_retention_if_H_is_fixed: float | None
    proxy_pass: bool


@dataclass(frozen=True)
class TargetPowerMatchedCase:
    axis_field_T: float
    iota_2over3: float
    H_ISS04: float
    radial_squeeze_fraction: float
    transient_confinement_retention: float
    base_beta: float
    state: CompressionState
    ignition: IgnitionProxy
    authority: str


def geometry_from_sector_lengths(
    sector_lengths_ft: Iterable[float], *, screening_aspect_ratio: float
) -> SFR2Geometry:
    lengths_ft = tuple(float(x) for x in sector_lengths_ft)
    if len(lengths_ft) != 4:
        raise ValueError("SFR-2 Rev A requires exactly four consecutive sectors")
    if any(x <= 0 for x in lengths_ft):
        raise ValueError("sector lengths must be positive")
    if screening_aspect_ratio <= 1.0:
        raise ValueError("screening aspect ratio must exceed one")
    lengths_m = tuple(x * FT_TO_M for x in lengths_ft)
    circumference = sum(lengths_m)
    R = circumference / (2.0 * pi)
    a = R / screening_aspect_ratio
    volume = 2.0 * pi**2 * R * a**2
    surface = 4.0 * pi**2 * R * a
    return SFR2Geometry(
        sector_lengths_ft=lengths_ft,
        sector_lengths_m=lengths_m,
        total_axis_path_m=circumference,
        equivalent_major_radius_m=R,
        screening_aspect_ratio=screening_aspect_ratio,
        screening_minor_radius_m=a,
        circular_torus_volume_m3=volume,
        circular_torus_surface_area_m2=surface,
    )


def ideal_radial_compression_state(
    *,
    geometry: SFR2Geometry,
    base_temperature_keV: float,
    base_beta: float,
    axis_field_T: float,
    radial_squeeze_fraction: float,
) -> CompressionState:
    """Return a conservative-geometry / optimistic-thermodynamic compression state.

    Assumptions:
    - major radius stays fixed;
    - both cross-section dimensions shrink by (1-s), so V scales as (1-s)^2;
    - particle number is conserved, so n scales as C^2 with C=1/(1-s);
    - an ideal monatomic adiabatic law is used, T scales as n^(gamma-1)=C^(4/3);
    - axis magnetic field receives *no* flux-compression credit and stays fixed;
    - no extra RF/magnetic-pumping energy is credited;
    - uniform 50/50 D-T, Te=Ti, no impurities/ash/radiation.

    These assumptions intentionally make the thermodynamic compression an upper-bound
    while refusing to invent a field-amplification or phase-heating benefit.
    """
    if not 0.0 <= radial_squeeze_fraction < 0.5:
        raise ValueError("radial squeeze must be in [0, 0.5)")
    if not 0.0 < base_beta < 1.0:
        raise ValueError("base beta must be between zero and one")
    if min(base_temperature_keV, axis_field_T) <= 0:
        raise ValueError("temperature and field must be positive")

    base = uniform_dt_burn_point(
        temperature_keV=base_temperature_keV,
        beta=base_beta,
        field_T=axis_field_T,
        volume_m3=geometry.circular_torus_volume_m3,
        target_fusion_power_MW=1.0,
    )
    C = 1.0 / (1.0 - radial_squeeze_fraction)
    density = base.ion_density_m3 * C**2
    temperature = base_temperature_keV * C ** (2.0 * (GAMMA_MONATOMIC - 1.0))
    volume = geometry.circular_torus_volume_m3 / C**2
    pressure = base.pressure_Pa * C ** (2.0 * GAMMA_MONATOMIC)
    beta = base_beta * C ** (2.0 * GAMMA_MONATOMIC)
    minor_radius = geometry.screening_minor_radius_m / C

    reactivity = bosch_hale_dt_reactivity(temperature)
    reaction_rate_density = 0.25 * density**2 * reactivity
    fusion_W = reaction_rate_density * DT_ENERGY_J * volume
    fusion_MW = fusion_W / 1.0e6
    alpha_MW = fusion_MW * DT_ALPHA_FRACTION
    neutron_MW = fusion_MW * DT_NEUTRON_FRACTION
    compressed_surface = 4.0 * pi**2 * geometry.equivalent_major_radius_m * minor_radius
    thermal_energy_MJ = 1.5 * pressure * volume / 1.0e6

    return CompressionState(
        radial_squeeze_fraction=radial_squeeze_fraction,
        radial_compression_ratio=C,
        minor_radius_m=minor_radius,
        volume_m3=volume,
        ion_density_m3=density,
        ion_temperature_keV=temperature,
        pressure_Pa=pressure,
        beta_at_fixed_B=beta,
        fusion_power_MW_uniform=fusion_MW,
        alpha_heating_MW_uniform=alpha_MW,
        neutron_power_MW_uniform=neutron_MW,
        neutron_wall_load_MW_m2_circular_proxy=neutron_MW / compressed_surface,
        thermal_energy_MJ=thermal_energy_MJ,
    )


def optimistic_ignition_proxy(
    *,
    geometry: SFR2Geometry,
    state: CompressionState,
    axis_field_T: float,
    iota_2over3: float,
    H_ISS04: float = 1.0,
    transient_confinement_retention: float = 1.0,
) -> IgnitionProxy:
    """Compare ISS04 tau_E to an optimistic alpha-only ignition balance.

    Required tau_E = plasma thermal energy / alpha heating.  Radiation, impurity,
    exhaust and other losses are omitted, so crossing ratio 1 is *not* an ignition claim.
    ISS04 is an empirical extrapolation here; it is not a dynamic-compression model.
    """
    if min(axis_field_T, iota_2over3, H_ISS04) <= 0:
        raise ValueError("field, iota and H must be positive")
    if not 0.0 < transient_confinement_retention <= 1.0:
        raise ValueError("retention must be in (0, 1]")
    if state.alpha_heating_MW_uniform <= 0:
        raise ValueError("alpha heating must be positive")

    required_tau = state.thermal_energy_MJ / state.alpha_heating_MW_uniform
    tau_iss04 = iss04_tau_E_s(
        a_m=state.minor_radius_m,
        R_m=geometry.equivalent_major_radius_m,
        absorbed_power_MW=state.alpha_heating_MW_uniform,
        ne_1e19_m3=state.ion_density_m3 / 1.0e19,
        B_T=axis_field_T,
        iota=iota_2over3,
        H=H_ISS04,
    )
    effective_tau = tau_iss04 * transient_confinement_retention
    ratio = effective_tau / required_tau
    # Since tau_ISS04 is linear in H, this is the H required at retention=1.
    tau_h1 = tau_iss04 / H_ISS04
    required_H = required_tau / tau_h1
    min_retention = required_tau / tau_iss04
    if min_retention > 1.0:
        min_retention_out: float | None = None
    else:
        min_retention_out = min_retention
    return IgnitionProxy(
        iota_2over3=iota_2over3,
        H_ISS04=H_ISS04,
        transient_confinement_retention=transient_confinement_retention,
        required_tau_E_s_optimistic=required_tau,
        iss04_tau_E_s=tau_iss04,
        effective_tau_E_s_after_retention=effective_tau,
        tau_ratio_to_optimistic_ignition=ratio,
        required_H_if_retention_is_one=required_H,
        minimum_retention_if_H_is_fixed=min_retention_out,
        proxy_pass=ratio >= 1.0,
    )


def solve_base_beta_for_target_fusion_power(
    *,
    geometry: SFR2Geometry,
    base_temperature_keV: float,
    axis_field_T: float,
    radial_squeeze_fraction: float,
    target_fusion_power_MW: float,
    beta_floor: float = 1.0e-5,
    beta_ceiling: float = 0.095,
) -> float:
    """Bisection solve for base beta making the compressed uniform model hit target power."""
    if target_fusion_power_MW <= 0:
        raise ValueError("target fusion power must be positive")
    lo, hi = beta_floor, beta_ceiling
    f_lo = ideal_radial_compression_state(
        geometry=geometry,
        base_temperature_keV=base_temperature_keV,
        base_beta=lo,
        axis_field_T=axis_field_T,
        radial_squeeze_fraction=radial_squeeze_fraction,
    ).fusion_power_MW_uniform
    f_hi = ideal_radial_compression_state(
        geometry=geometry,
        base_temperature_keV=base_temperature_keV,
        base_beta=hi,
        axis_field_T=axis_field_T,
        radial_squeeze_fraction=radial_squeeze_fraction,
    ).fusion_power_MW_uniform
    if not (f_lo <= target_fusion_power_MW <= f_hi):
        raise ValueError(
            "target fusion power is outside the declared beta search interval "
            f"[{f_lo:.6g}, {f_hi:.6g}] MW"
        )
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        f_mid = ideal_radial_compression_state(
            geometry=geometry,
            base_temperature_keV=base_temperature_keV,
            base_beta=mid,
            axis_field_T=axis_field_T,
            radial_squeeze_fraction=radial_squeeze_fraction,
        ).fusion_power_MW_uniform
        if f_mid < target_fusion_power_MW:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def target_power_matched_case(
    *,
    geometry: SFR2Geometry,
    base_temperature_keV: float,
    target_fusion_power_MW: float,
    axis_field_T: float,
    iota_2over3: float,
    radial_squeeze_fraction: float,
    H_ISS04: float,
    transient_confinement_retention: float,
) -> TargetPowerMatchedCase:
    beta = solve_base_beta_for_target_fusion_power(
        geometry=geometry,
        base_temperature_keV=base_temperature_keV,
        axis_field_T=axis_field_T,
        radial_squeeze_fraction=radial_squeeze_fraction,
        target_fusion_power_MW=target_fusion_power_MW,
    )
    state = ideal_radial_compression_state(
        geometry=geometry,
        base_temperature_keV=base_temperature_keV,
        base_beta=beta,
        axis_field_T=axis_field_T,
        radial_squeeze_fraction=radial_squeeze_fraction,
    )
    ignition = optimistic_ignition_proxy(
        geometry=geometry,
        state=state,
        axis_field_T=axis_field_T,
        iota_2over3=iota_2over3,
        H_ISS04=H_ISS04,
        transient_confinement_retention=transient_confinement_retention,
    )
    return TargetPowerMatchedCase(
        axis_field_T=axis_field_T,
        iota_2over3=iota_2over3,
        H_ISS04=H_ISS04,
        radial_squeeze_fraction=radial_squeeze_fraction,
        transient_confinement_retention=transient_confinement_retention,
        base_beta=beta,
        state=state,
        ignition=ignition,
        authority="analytical_empirical_low_authority_screen__not_equilibrium_or_ignition_evidence",
    )


def validate_sfr2_config(raw: dict[str, Any]) -> tuple[str, ...]:
    errors: list[str] = []
    try:
        study = raw["study_envelope"]
        geometry_from_sector_lengths(
            study["sector_lengths_ft"],
            screening_aspect_ratio=float(study["screening_aspect_ratio"]),
        )
        if study["sector_pattern"] != "ABAB":
            errors.append("SFR-2 Rev A sector_pattern must remain ABAB")
        if raw["topology"]["independent_plasma_machines"]:
            errors.append("SFR-2 must be one continuous plasma topology, not connected independent plasmas")
        if raw["dynamic_actuation"]["credits_unmodeled_phase_heating"]:
            errors.append("Rev A forbids numerical credit for unmodeled phase/RF heating")
        if raw["dynamic_actuation"]["reverses_primary_confinement_field"]:
            errors.append("Rev A keeps the primary confinement field steady")
        phases = raw["dynamic_actuation"]["phase_offsets_deg"]
        if phases != [0, 90, 180, 270]:
            errors.append("Rev A traveling-wave phase offsets must be 0/90/180/270 degrees")
        if max(study["radial_squeeze_fraction_sweep"]) > 0.10:
            errors.append("Rev A compression sweep is capped at 10% radial squeeze")
        if max(study["iota_2over3_sweep"]) > 0.90:
            errors.append("Rev A iota screening sweep is capped at 0.90 until equilibrium evidence exists")
        if min(study["axis_field_T_sweep"]) <= 0:
            errors.append("axis-field sweep must remain positive")
        if raw["promotion_status"]["SFR2_G0_SPEC"] != "PASS_SPEC_ONLY":
            errors.append("SFR2_G0_SPEC must be PASS_SPEC_ONLY")
        for gate, status in raw["promotion_status"].items():
            if gate != "SFR2_G0_SPEC" and status != "NOT_RUN":
                errors.append(f"{gate} must remain NOT_RUN until matching high-authority evidence exists")
    except (KeyError, TypeError, ValueError) as exc:
        errors.append(f"invalid SFR-2 config: {exc}")
    return tuple(errors)


def run_sfr2_screen(raw: dict[str, Any]) -> dict[str, Any]:
    errors = validate_sfr2_config(raw)
    if errors:
        raise ValueError("; ".join(errors))
    study = raw["study_envelope"]
    geometry = geometry_from_sector_lengths(
        study["sector_lengths_ft"],
        screening_aspect_ratio=float(study["screening_aspect_ratio"]),
    )
    cases: list[TargetPowerMatchedCase] = []
    for B in study["axis_field_T_sweep"]:
        for iota in study["iota_2over3_sweep"]:
            for squeeze in study["radial_squeeze_fraction_sweep"]:
                for H in study["H_ISS04_sweep"]:
                    for retention in study["transient_confinement_retention_sweep"]:
                        # A transient retention penalty has no meaning when compression is zero.
                        if squeeze == 0.0 and retention != 1.0:
                            continue
                        cases.append(
                            target_power_matched_case(
                                geometry=geometry,
                                base_temperature_keV=float(study["base_temperature_keV"]),
                                target_fusion_power_MW=float(study["target_fusion_power_MW"]),
                                axis_field_T=float(B),
                                iota_2over3=float(iota),
                                radial_squeeze_fraction=float(squeeze),
                                H_ISS04=float(H),
                                transient_confinement_retention=float(retention),
                            )
                        )

    # Primary authority comparison: H=1, retention=1. This prevents favorable sensitivity
    # assumptions from being mistaken for the actual result.
    primary = [c for c in cases if c.H_ISS04 == 1.0 and c.transient_confinement_retention == 1.0]
    best_primary = max(primary, key=lambda c: c.ignition.tau_ratio_to_optimistic_ignition)
    best_dynamic_primary = max(
        (c for c in primary if c.radial_squeeze_fraction > 0.0),
        key=lambda c: c.ignition.tau_ratio_to_optimistic_ignition,
    )
    best_any_sensitivity = max(cases, key=lambda c: c.ignition.tau_ratio_to_optimistic_ignition)

    # Isolate what the proposed "magnetic rifling" does at the highest field in the declared
    # sweep, with no compression and H=1.
    max_B = max(float(x) for x in study["axis_field_T_sweep"])
    rifling = sorted(
        (
            c for c in primary
            if c.axis_field_T == max_B and c.radial_squeeze_fraction == 0.0
        ),
        key=lambda c: c.iota_2over3,
    )

    # Isolate compression at the most favorable declared B/iota but still H=1, retention=1.
    max_iota = max(float(x) for x in study["iota_2over3_sweep"])
    compression = sorted(
        (
            c for c in primary
            if c.axis_field_T == max_B and c.iota_2over3 == max_iota
        ),
        key=lambda c: c.radial_squeeze_fraction,
    )

    return {
        "program": "IX-StellaratorForge",
        "release": "0.5.0",
        "candidate": raw["design_id"],
        "candidate_role": "assumption_breaker_dynamic_stellarator_derived_candidate",
        "authority": "LOW__analytical_plus_empirical_scaling_only",
        "claim_boundary": raw["claim_boundary"],
        "geometry": _geometry_json(geometry),
        "model_rules": {
            "sector_interpretation": "four consecutive arc-length sectors of one closed toroidal plasma system",
            "staggering_confinement_credit": 0.0,
            "dynamic_phase_heating_credit": 0.0,
            "magnetic_flux_compression_credit": 0.0,
            "compression_thermodynamics": "ideal monatomic adiabatic upper-bound at fixed axis B",
            "confinement_model": "ISS04 empirical scaling; extrapolated; not dynamic-MHD evidence",
            "ignition_balance": "thermal energy / alpha heating only; radiation/ash/transport channels omitted beyond ISS04 proxy",
        },
        "primary_screen": {
            "definition": "H_ISS04=1.0 and transient_confinement_retention=1.0",
            "best_case": _case_json(best_primary),
            "best_dynamic_compression_case": _case_json(best_dynamic_primary),
            "verdict": (
                "NO_PRIMARY_CASE_CROSSES_OPTIMISTIC_IGNITION_PROXY"
                if not any(c.ignition.proxy_pass for c in primary)
                else "AT_LEAST_ONE_PRIMARY_CASE_CROSSES_LOW_AUTHORITY_PROXY__HIGH_AUTHORITY_GATES_STILL_OPEN"
            ),
        },
        "rifling_sensitivity_at_max_B_no_compression": [_case_json(c) for c in rifling],
        "compression_sensitivity_at_max_B_max_iota": [_case_json(c) for c in compression],
        "favorable_sensitivity_only": {
            "best_case": _case_json(best_any_sensitivity),
            "warning": "H>1 and/or retention assumptions are sensitivity variables, not earned SFR-2 performance.",
        },
        "high_authority_required": [
            "3-D finite-beta equilibrium for the ABAB boundary/axis",
            "magnetic-island/stochastic-region assessment during the full actuation cycle",
            "ideal/resistive MHD stability under time-varying perturbation",
            "neoclassical/bootstrap plus nonlinear gyrokinetic/profile transport",
            "alpha-particle orbit confinement during actuation",
            "self-consistent RF/wave deposition and phase-control calculation",
            "coil/current/field/stress/quench design proving the demanded fields are physically realizable",
            "3-D edge/divertor/first-wall transient heat-flux solution",
            "full 3-D neutronics/TBR/shielding and integrated plant closure",
            "hardware experiment",
        ],
        "promotion_status": raw["promotion_status"],
    }



def _geometry_json(geometry: SFR2Geometry) -> dict[str, Any]:
    d = asdict(geometry)
    d["sector_lengths_ft"] = list(geometry.sector_lengths_ft)
    d["sector_lengths_m"] = list(geometry.sector_lengths_m)
    return d

def _case_json(case: TargetPowerMatchedCase) -> dict[str, Any]:
    d = asdict(case)
    # Compact, explicit interpretation fields derived from the numbers.
    d["interpretation"] = {
        "low_authority_proxy_pass": case.ignition.proxy_pass,
        "distance_from_proxy_ratio_1_fraction": case.ignition.tau_ratio_to_optimistic_ignition - 1.0,
        "compression_is_not_credited_for_phase_heating": True,
    }
    return d
