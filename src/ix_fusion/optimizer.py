from __future__ import annotations

import math
from dataclasses import replace

import numpy as np

from .engineering import engineering_metrics
from .field import field_strength_cv, helical_strength, resonant_overlap_proxy
from .models import CandidateConfig, Harmonic
from .omnigenity import omnigenity_metrics


def objective_terms(config: CandidateConfig) -> dict[str, float]:
    omni = omnigenity_metrics(config)
    strength_delta = helical_strength(config) - config.required_helical_strength
    engineering = engineering_metrics(config)
    return {
        "bounce_action": 50.0 * omni.action_variation_mean,
        "resonant_overlap": 0.45 * resonant_overlap_proxy(config),
        "field_strength_cv": 0.05 * field_strength_cv(config),
        "spectral_complexity": 0.00018
        * sum(h.amplitude**2 * (h.m**2 + h.n**2) for h in config.harmonics),
        "helical_strength_constraint": 280.0 * strength_delta**2,
        "mirror_regularization": 1.50 * (config.mirror_amplitude - 0.08) ** 2,
        "engineering_screen": 0.018 * engineering.engineering_burden_score,
    }


def quick_objective(config: CandidateConfig) -> float:
    """Composite reduced-order objective used only for seed screening.

    Lower is better. Terms are dimensionless and intentionally conservative. The objective
    is not a reactor performance metric and is not comparable to Q, triple product, or power.
    """
    return float(sum(objective_terms(config).values()))


def _normalize_strength(harmonics: tuple[Harmonic, ...], target: float) -> tuple[Harmonic, ...]:
    strength = sum(abs(h.amplitude) for h in harmonics)
    if strength <= 1e-15 or target <= 0:
        return harmonics
    scale = target / strength
    return tuple(replace(h, amplitude=float(np.clip(h.amplitude * scale, -0.04, 0.04))) for h in harmonics)


def optimize_seed(
    config: CandidateConfig,
    passes: int = 4,
    amplitude_step: float = 0.0025,
    phase_step: float = math.radians(10.0),
    iota_step: float = 0.012,
    mirror_step: float = 0.008,
) -> tuple[CandidateConfig, list[dict[str, float]]]:
    """Deterministic equal-budget coordinate search over physics and geometry screens."""
    if config.role == "negative_control" or not config.harmonics:
        return config, [{"iteration": 0.0, "objective": quick_objective(config)}]
    current = config
    best = quick_objective(current)
    history: list[dict[str, float]] = [{"iteration": 0.0, "objective": best}]
    iteration = 0
    amp_step = amplitude_step
    ph_step = phase_step
    io_step = iota_step
    mi_step = mirror_step

    def consider(trial: CandidateConfig) -> None:
        nonlocal current, best, iteration
        trial.validate()
        value = quick_objective(trial)
        iteration += 1
        history.append({"iteration": float(iteration), "objective": value})
        if value + 1e-12 < best:
            current, best = trial, value

    for _pass in range(passes):
        for idx in range(len(current.harmonics)):
            for delta in (-amp_step, amp_step):
                hs = list(current.harmonics)
                h = hs[idx]
                hs[idx] = replace(h, amplitude=float(np.clip(h.amplitude + delta, -0.04, 0.04)))
                consider(replace(current, harmonics=_normalize_strength(tuple(hs), current.required_helical_strength)))
            for delta in (-ph_step, ph_step):
                hs = list(current.harmonics)
                h = hs[idx]
                hs[idx] = replace(h, phase=float((h.phase + delta) % (2.0 * np.pi)))
                consider(replace(current, harmonics=tuple(hs)))
        for delta in (-io_step, io_step):
            consider(replace(current, iota0=float(np.clip(current.iota0 + delta, 0.2, 1.1))))
        for delta in (-mi_step, mi_step):
            consider(
                replace(
                    current,
                    mirror_amplitude=float(np.clip(current.mirror_amplitude + delta, 0.0, 0.20)),
                )
            )
        amp_step *= 0.6
        ph_step *= 0.6
        io_step *= 0.6
        mi_step *= 0.6
    return current, history
