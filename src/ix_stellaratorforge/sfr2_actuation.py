"""Low-authority phase-programmed magnetic-breathing screen for SFR-2.

This module does not solve a time-dependent stellarator equilibrium or wave/plasma
interaction.  It asks a narrower falsification question: if the existing SFR-2 Rev A
plasma inventory follows ideal monatomic adiabatic bookkeeping while auxiliary fields
change the sector cross-sectional areas, does any declared phase pattern improve both
the cycle-averaged optimistic ignition proxy and cycle-averaged fusion power?

The primary HTS field, vessel and baseline ABAB geometry remain unchanged.  No
magnetic-pumping, RF, shock, flux-compression, topology or three-body fusion credit is
invented.  A tri-lobe boundary harmonic is area-normalized, so reshaping alone receives
zero thermodynamic credit.
"""
from __future__ import annotations

from math import pi, radians, sin, sqrt
from typing import Any

from .burn import DT_ALPHA_FRACTION, DT_ENERGY_J, bosch_hale_dt_reactivity, iss04_tau_E_s
from .sfr2 import (
    DT_NEUTRON_FRACTION,
    GAMMA_MONATOMIC,
    geometry_from_sector_lengths,
    ideal_radial_compression_state,
    optimistic_ignition_proxy,
    solve_base_beta_for_target_fusion_power,
)

AUTHORITY = "LOW__zero_D_adiabatic_cycle_plus_ISS04_screen__not_dynamic_equilibrium"


def weighted_volume_ratio(
    *,
    sector_lengths_ft: list[float],
    depth_fraction: float,
    phase_offsets_deg: list[float],
    cycle_phase_rad: float,
) -> float:
    """Return V(t)/V0 for sector radius factors 1-depth*sin(phase+offset).

    Each sector volume is proportional to its axis length times minor-radius squared.
    This is geometry bookkeeping only; it does not assert that a realizable coil set can
    produce the boundary or that pressure equilibrates instantaneously between sectors.
    """
    if len(sector_lengths_ft) != len(phase_offsets_deg) or not sector_lengths_ft:
        raise ValueError("sector lengths and phase offsets must have the same nonzero length")
    if any(length <= 0 for length in sector_lengths_ft):
        raise ValueError("sector lengths must be positive")
    if not 0.0 <= depth_fraction <= 0.10:
        raise ValueError("breathing depth must be within [0, 0.10]")
    total_length = sum(sector_lengths_ft)
    return sum(
        length
        * (1.0 - depth_fraction * sin(cycle_phase_rad + radians(offset))) ** 2
        for length, offset in zip(sector_lengths_ft, phase_offsets_deg, strict=True)
    ) / total_length


def area_preserving_trilobe_geometry(amplitude_fraction: float) -> dict[str, float]:
    """Describe r(theta)=a*N*(1+eps*cos(3 theta)) with conserved cross-section area.

    The unnormalized polar area is multiplied by 1+eps^2/2.  N removes that area
    change, isolating the three-lobe shape from global compression.  Consequently this
    harmonic earns no density, temperature, fusion-power or ignition-proxy credit here.
    """
    if not 0.0 <= amplitude_fraction <= 0.20:
        raise ValueError("tri-lobe amplitude must be within [0, 0.20]")
    raw_area_ratio = 1.0 + 0.5 * amplitude_fraction**2
    normalization = 1.0 / sqrt(raw_area_ratio)
    return {
        "amplitude_fraction": amplitude_fraction,
        "area_normalization": normalization,
        "normalized_area_ratio": raw_area_ratio * normalization**2,
        "minimum_radius_over_a": normalization * (1.0 - amplitude_fraction),
        "maximum_radius_over_a": normalization * (1.0 + amplitude_fraction),
        "thermodynamic_ignition_credit": 0.0,
    }


def validate_actuation_config(raw: dict[str, Any]) -> tuple[str, ...]:
    errors: list[str] = []
    try:
        if raw["baseline_design_id"] != "SFR-2-RevA":
            errors.append("actuation overlay must preserve SFR-2-RevA as its baseline")
        if raw["mechanical_architecture"]["flexible_vacuum_vessel"]:
            errors.append("the vacuum vessel must remain rigid")
        if raw["mechanical_architecture"]["pulses_primary_hts_coils"]:
            errors.append("the primary HTS confinement coils must remain steady")
        study = raw["screen"]
        geometry_from_sector_lengths(
            study["sector_lengths_ft"],
            screening_aspect_ratio=float(study["screening_aspect_ratio"]),
        )
        if study["sector_pattern"] != "ABAB":
            errors.append("baseline sector pattern must remain ABAB")
        if study["sample_count_per_cycle"] < 360:
            errors.append("cycle screen requires at least 360 samples")
        if min(study["depth_fraction_sweep"]) < 0 or max(study["depth_fraction_sweep"]) > 0.05:
            errors.append("declared breathing-depth sweep must remain within 0 to 5 percent")
        patterns = study["phase_patterns_deg"]
        if patterns["synchronous"] != [0, 0, 0, 0]:
            errors.append("synchronous phase pattern is invalid")
        if patterns["abab_opposed"] != [0, 180, 0, 180]:
            errors.append("ABAB-opposed phase pattern is invalid")
        if patterns["traveling_quadrature"] != [0, 90, 180, 270]:
            errors.append("traveling-quadrature phase pattern is invalid")
        tri = raw["concept_image_translation"]
        if tri["global_toroidal_lobe_count"] != 3 or tri["baseline_field_periods"] != 4:
            errors.append("the declared 3-lobe versus 4-field-period comparison changed")
        if tri["credits_three_body_fusion"]:
            errors.append("D-T fusion must not receive three-body collision credit")
        if tri["credits_astrophysical_gravity_or_accretion"]:
            errors.append("reactor screen must not credit astrophysical gravity or accretion")
        if not tri["area_normalize_repeated_poloidal_m3"]:
            errors.append("tri-lobe shape must be area-normalized before comparison")
        for gate, status in raw["promotion_status"].items():
            if gate != "SFR2A_G0_OVERLAY_SPEC" and status != "NOT_RUN":
                errors.append(f"{gate} must remain NOT_RUN without high-authority evidence")
    except (KeyError, TypeError, ValueError) as exc:
        errors.append(f"invalid SFR-2 actuation overlay config: {exc}")
    return tuple(errors)


def _cycle_case(
    *,
    geometry: Any,
    base: Any,
    depth: float,
    pattern_name: str,
    phase_offsets_deg: list[float],
    sector_lengths_ft: list[float],
    axis_field_T: float,
    iota_2over3: float,
    sample_count: int,
) -> dict[str, Any]:
    samples: list[dict[str, float]] = []
    for index in range(sample_count):
        phase = 2.0 * pi * index / sample_count
        volume_ratio = weighted_volume_ratio(
            sector_lengths_ft=sector_lengths_ft,
            depth_fraction=depth,
            phase_offsets_deg=phase_offsets_deg,
            cycle_phase_rad=phase,
        )
        density_ratio = 1.0 / volume_ratio
        density = base.ion_density_m3 * density_ratio
        temperature = base.ion_temperature_keV * density_ratio ** (GAMMA_MONATOMIC - 1.0)
        volume = base.volume_m3 * volume_ratio
        pressure = base.pressure_Pa * density_ratio**GAMMA_MONATOMIC
        beta = base.beta_at_fixed_B * density_ratio**GAMMA_MONATOMIC
        reactivity = bosch_hale_dt_reactivity(temperature)
        fusion_MW = 0.25 * density**2 * reactivity * DT_ENERGY_J * volume / 1.0e6
        alpha_MW = fusion_MW * DT_ALPHA_FRACTION
        thermal_MJ = 1.5 * pressure * volume / 1.0e6
        effective_minor_radius = geometry.screening_minor_radius_m * sqrt(volume_ratio)
        tau_iss04 = iss04_tau_E_s(
            a_m=effective_minor_radius,
            R_m=geometry.equivalent_major_radius_m,
            absorbed_power_MW=alpha_MW,
            ne_1e19_m3=density / 1.0e19,
            B_T=axis_field_T,
            iota=iota_2over3,
            H=1.0,
        )
        required_tau = thermal_MJ / alpha_MW
        samples.append(
            {
                "cycle_phase_deg": 360.0 * index / sample_count,
                "volume_ratio_to_baseline": volume_ratio,
                "equivalent_radial_squeeze_fraction": 1.0 - sqrt(volume_ratio),
                "ion_density_m3": density,
                "ion_temperature_keV": temperature,
                "beta_at_fixed_B": beta,
                "fusion_power_MW_uniform": fusion_MW,
                "alpha_heating_MW_uniform": alpha_MW,
                "neutron_power_MW_uniform": fusion_MW * DT_NEUTRON_FRACTION,
                "thermal_energy_MJ": thermal_MJ,
                "optimistic_ignition_tau_ratio": tau_iss04 / required_tau,
            }
        )

    def mean(key: str) -> float:
        return sum(sample[key] for sample in samples) / len(samples)

    ratio_peak = max(samples, key=lambda sample: sample["optimistic_ignition_tau_ratio"])
    fusion_peak = max(samples, key=lambda sample: sample["fusion_power_MW_uniform"])
    avg_ratio = mean("optimistic_ignition_tau_ratio")
    avg_fusion = mean("fusion_power_MW_uniform")
    baseline_ratio = base._baseline_ignition_ratio  # attached by run function; internal only
    baseline_fusion = base.fusion_power_MW_uniform
    return {
        "pattern": pattern_name,
        "phase_offsets_deg": phase_offsets_deg,
        "depth_fraction": depth,
        "cycle_average": {
            "optimistic_ignition_tau_ratio": avg_ratio,
            "distance_from_ratio_one_fraction": avg_ratio - 1.0,
            "fusion_power_MW_uniform": avg_fusion,
            "alpha_heating_MW_uniform": mean("alpha_heating_MW_uniform"),
            "beta_at_fixed_B": mean("beta_at_fixed_B"),
        },
        "full_cycle": {
            "minimum_optimistic_ignition_tau_ratio": min(s["optimistic_ignition_tau_ratio"] for s in samples),
            "maximum_optimistic_ignition_tau_ratio": ratio_peak["optimistic_ignition_tau_ratio"],
            "minimum_fusion_power_MW_uniform": min(s["fusion_power_MW_uniform"] for s in samples),
            "maximum_fusion_power_MW_uniform": fusion_peak["fusion_power_MW_uniform"],
            "maximum_beta_at_fixed_B": max(s["beta_at_fixed_B"] for s in samples),
        },
        "closest_instantaneous_proxy_point": ratio_peak,
        "maximum_fusion_point": fusion_peak,
        "screen_decision": {
            "cycle_average_proxy_pass": avg_ratio >= 1.0,
            "entire_cycle_proxy_pass": all(s["optimistic_ignition_tau_ratio"] >= 1.0 for s in samples),
            "cycle_average_ratio_improves_over_baseline": avg_ratio > baseline_ratio,
            "cycle_average_fusion_improves_over_baseline": avg_fusion > baseline_fusion,
            "joint_average_improvement": avg_ratio > baseline_ratio and avg_fusion > baseline_fusion,
            "net_power_claim_permitted": False,
        },
    }


class _BaselineCarrier:
    """Small mutable carrier used only to attach the baseline proxy to a state."""

    def __init__(self, state: Any, ignition_ratio: float) -> None:
        self.__dict__.update(state.__dict__)
        self._baseline_ignition_ratio = ignition_ratio


def run_actuation_overlay_screen(raw: dict[str, Any]) -> dict[str, Any]:
    errors = validate_actuation_config(raw)
    if errors:
        raise ValueError("; ".join(errors))
    screen = raw["screen"]
    geometry = geometry_from_sector_lengths(
        screen["sector_lengths_ft"],
        screening_aspect_ratio=float(screen["screening_aspect_ratio"]),
    )
    axis_field_T = float(screen["axis_field_T"])
    iota = float(screen["iota_2over3"])
    base_beta = solve_base_beta_for_target_fusion_power(
        geometry=geometry,
        base_temperature_keV=float(screen["base_temperature_keV"]),
        axis_field_T=axis_field_T,
        radial_squeeze_fraction=0.0,
        target_fusion_power_MW=float(screen["target_fusion_power_MW"]),
    )
    state = ideal_radial_compression_state(
        geometry=geometry,
        base_temperature_keV=float(screen["base_temperature_keV"]),
        base_beta=base_beta,
        axis_field_T=axis_field_T,
        radial_squeeze_fraction=0.0,
    )
    ignition = optimistic_ignition_proxy(
        geometry=geometry,
        state=state,
        axis_field_T=axis_field_T,
        iota_2over3=iota,
        H_ISS04=1.0,
        transient_confinement_retention=1.0,
    )
    base = _BaselineCarrier(state, ignition.tau_ratio_to_optimistic_ignition)

    cases = [
        _cycle_case(
            geometry=geometry,
            base=base,
            depth=float(depth),
            pattern_name=name,
            phase_offsets_deg=[float(value) for value in phases],
            sector_lengths_ft=[float(value) for value in screen["sector_lengths_ft"]],
            axis_field_T=axis_field_T,
            iota_2over3=iota,
            sample_count=int(screen["sample_count_per_cycle"]),
        )
        for depth in screen["depth_fraction_sweep"]
        for name, phases in screen["phase_patterns_deg"].items()
    ]
    active_cases = [case for case in cases if case["depth_fraction"] > 0.0]
    closest_average = max(
        active_cases,
        key=lambda case: case["cycle_average"]["optimistic_ignition_tau_ratio"],
    )
    closest_instantaneous = max(
        active_cases,
        key=lambda case: case["full_cycle"]["maximum_optimistic_ignition_tau_ratio"],
    )

    tri = raw["concept_image_translation"]
    tri_cases = [
        area_preserving_trilobe_geometry(float(amplitude))
        for amplitude in tri["poloidal_m3_amplitude_fraction_sweep"]
    ]
    any_joint_improvement = any(
        case["screen_decision"]["joint_average_improvement"] for case in active_cases
    )
    any_average_pass = any(
        case["screen_decision"]["cycle_average_proxy_pass"] for case in active_cases
    )
    return {
        "program": "IX-StellaratorForge",
        "release": "0.6.0",
        "study_id": raw["study_id"],
        "baseline_design_id": raw["baseline_design_id"],
        "authority": AUTHORITY,
        "claim_boundary": raw["claim_boundary"],
        "baseline": {
            "axis_field_T": axis_field_T,
            "iota_2over3": iota,
            "base_temperature_keV": float(screen["base_temperature_keV"]),
            "base_beta": base_beta,
            "fusion_power_MW_uniform": state.fusion_power_MW_uniform,
            "optimistic_ignition_tau_ratio": ignition.tau_ratio_to_optimistic_ignition,
            "distance_from_ratio_one_fraction": ignition.tau_ratio_to_optimistic_ignition - 1.0,
        },
        "model_rules": {
            "baseline_geometry_changed": False,
            "vacuum_vessel_flex_credit": 0.0,
            "primary_hts_pulsing_credit": 0.0,
            "magnetic_pumping_heating_credit": 0.0,
            "rf_phase_heating_credit": 0.0,
            "shock_heating_credit": 0.0,
            "astrophysical_gravity_or_accretion_credit": 0.0,
            "three_body_fusion_credit": 0.0,
            "actuator_and_cryogenic_power_debited": False,
            "thermodynamics": "fixed particle inventory; ideal monatomic adiabatic global-volume response",
            "confinement": "instantaneous ISS04 geometry proxy; not valid as dynamic MHD evidence",
        },
        "breathing_cases": cases,
        "breathing_result": {
            "closest_cycle_average_case": closest_average,
            "closest_instantaneous_case": closest_instantaneous,
            "any_joint_cycle_average_improvement": any_joint_improvement,
            "any_cycle_average_proxy_pass": any_average_pass,
            "verdict": (
                "NO_DECLARED_BREATHING_CASE_IMPROVES_BOTH_CYCLE_AVERAGE_PROXY_AND_FUSION_POWER"
                if not any_joint_improvement
                else "LOW_AUTHORITY_JOINT_IMPROVEMENT_REQUIRES_HIGH_AUTHORITY_REVIEW"
            ),
        },
        "concept_image_result": {
            "useful_translation": "area-preserving poloidal m=3 actuator harmonic repeated in every one of the four ABAB field periods",
            "global_three_toroidal_lobes_compatible_with_4fp_baseline": False,
            "repeated_poloidal_m3_bookkeeping_compatible_with_4fp": True,
            "three_point_collision_is_dt_fusion_mechanism": False,
            "tri_lobe_cases": tri_cases,
            "zero_D_closer_to_ignition_credit": 0.0,
            "verdict": "IMAGE_SUGGESTS_A_TESTABLE_ACTUATOR_SYMMETRY_BUT_ADDS_NO_EARNED_FUSION_GAIN",
        },
        "required_next_evidence": [
            "time-sliced free-boundary finite-beta equilibria over a complete actuation cycle",
            "Poincare and island/stochasticity maps for every phase",
            "coil-current solution plus eddy-current, force, fatigue, cooling and quench analysis",
            "kinetic magnetic-pumping calculation resolving frequency, collisionality and phase lag",
            "alpha-particle orbit confinement through the complete cycle",
            "transport and nonlinear MHD response",
            "actuator wall-plug power debit and integrated burn balance",
        ],
        "promotion_status": raw["promotion_status"],
    }
