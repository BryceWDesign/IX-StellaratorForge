from __future__ import annotations

from dataclasses import replace

import numpy as np

from .models import CandidateConfig, Harmonic
from .optimizer import quick_objective


def perturb_configuration(
    config: CandidateConfig,
    rng: np.random.Generator,
    amplitude_sigma_fraction: float,
    phase_sigma_deg: float,
    axis_sigma_fraction: float,
    iota_sigma: float,
) -> CandidateConfig:
    harmonics = []
    for h in config.harmonics:
        amp = h.amplitude * (1.0 + rng.normal(0.0, amplitude_sigma_fraction))
        phase = h.phase + rng.normal(0.0, np.deg2rad(phase_sigma_deg))
        harmonics.append(replace(h, amplitude=float(amp), phase=float(phase)))
    axis = max(0.0, config.axis_helical_amplitude * (1.0 + rng.normal(0.0, axis_sigma_fraction)))
    iota = float(np.clip(config.iota0 + rng.normal(0.0, iota_sigma), 0.2, 1.1))
    trial = replace(config, harmonics=tuple(harmonics), axis_helical_amplitude=float(axis), iota0=iota)
    trial.validate()
    return trial


def geometry_error_monte_carlo(
    config: CandidateConfig,
    samples: int = 160,
    seed: int = 260815,
    amplitude_sigma_fraction: float = 0.03,
    phase_sigma_deg: float = 2.0,
    axis_sigma_fraction: float = 0.02,
    iota_sigma: float = 0.004,
) -> dict[str, float]:
    rng = np.random.default_rng(seed)
    nominal = quick_objective(config)
    values = np.empty(samples, dtype=float)
    for idx in range(samples):
        values[idx] = quick_objective(
            perturb_configuration(
                config,
                rng,
                amplitude_sigma_fraction,
                phase_sigma_deg,
                axis_sigma_fraction,
                iota_sigma,
            )
        )
    ratios = values / max(nominal, 1e-12)
    return {
        "samples": float(samples),
        "nominal_objective": float(nominal),
        "median_objective": float(np.median(values)),
        "p95_objective": float(np.percentile(values, 95)),
        "median_degradation_ratio": float(np.median(ratios)),
        "p95_degradation_ratio": float(np.percentile(ratios, 95)),
        "worst_degradation_ratio": float(np.max(ratios)),
    }
