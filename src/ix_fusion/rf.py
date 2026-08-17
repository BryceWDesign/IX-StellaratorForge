from __future__ import annotations

import numpy as np

from .models import RFMetrics, RobustnessMetrics


def actuator_weights(count: int, target_mode: int = 1, phase_offset: float = 0.0) -> np.ndarray:
    if count < 2:
        raise ValueError("at least two actuators are required")
    k = np.arange(count)
    return np.exp(1j * (phase_offset + 2.0 * np.pi * target_mode * k / count))


def spatial_spectrum(weights: np.ndarray) -> np.ndarray:
    weights = np.asarray(weights, dtype=complex)
    spec = np.fft.fft(weights) / len(weights)
    return np.abs(spec) ** 2


def rf_metrics(weights: np.ndarray, target_mode: int = 1) -> RFMetrics:
    spec = spatial_spectrum(weights)
    total = float(np.sum(spec))
    idx = target_mode % len(weights)
    purity = float(spec[idx] / total) if total > 0 else 0.0
    sideband = 1.0 - purity
    amplitude_ripple = float(np.std(np.abs(weights)) / max(np.mean(np.abs(weights)), 1e-12))
    return RFMetrics(target_mode_purity=purity, sideband_power=sideband, amplitude_ripple=amplitude_ripple)


def _realized_weights(
    count: int,
    rng: np.random.Generator,
    target_mode: int,
    geometry_sigma_deg: float,
    phase_sigma_deg: float,
    amplitude_sigma_fraction: float,
    feedback: bool,
    measurement_residual_fraction: float,
) -> np.ndarray:
    base = actuator_weights(count, target_mode)
    geom = rng.normal(0.0, np.deg2rad(geometry_sigma_deg), count)
    phase = rng.normal(0.0, np.deg2rad(phase_sigma_deg), count)
    amp = 1.0 + rng.normal(0.0, amplitude_sigma_fraction, count)
    if feedback:
        correction_geom = geom * (1.0 - measurement_residual_fraction)
        correction_phase = phase * (1.0 - measurement_residual_fraction)
        correction_amp = (amp - 1.0) * (1.0 - measurement_residual_fraction)
        geom = geom - correction_geom
        phase = phase - correction_phase
        amp = amp - correction_amp
    location_phase = target_mode * geom
    return base * amp * np.exp(1j * (phase + location_phase))


def monte_carlo_robustness(
    count: int = 6,
    target_mode: int = 1,
    samples: int = 4000,
    seed: int = 240601,
    geometry_sigma_deg: float = 1.0,
    phase_sigma_deg: float = 5.0,
    amplitude_sigma_fraction: float = 0.05,
    measurement_residual_fraction: float = 0.30,
) -> RobustnessMetrics:
    rng_open = np.random.default_rng(seed)
    rng_fb = np.random.default_rng(seed)
    open_purity = np.empty(samples, dtype=float)
    feedback_purity = np.empty(samples, dtype=float)
    for idx in range(samples):
        w_open = _realized_weights(
            count,
            rng_open,
            target_mode,
            geometry_sigma_deg,
            phase_sigma_deg,
            amplitude_sigma_fraction,
            False,
            measurement_residual_fraction,
        )
        w_fb = _realized_weights(
            count,
            rng_fb,
            target_mode,
            geometry_sigma_deg,
            phase_sigma_deg,
            amplitude_sigma_fraction,
            True,
            measurement_residual_fraction,
        )
        open_purity[idx] = rf_metrics(w_open, target_mode).target_mode_purity
        feedback_purity[idx] = rf_metrics(w_fb, target_mode).target_mode_purity
    open_unwanted = max(1.0 - float(np.median(open_purity)), 1e-15)
    fb_unwanted = max(1.0 - float(np.median(feedback_purity)), 1e-15)
    return RobustnessMetrics(
        open_loop_purity_median=float(np.median(open_purity)),
        feedback_purity_median=float(np.median(feedback_purity)),
        open_loop_purity_p05=float(np.percentile(open_purity, 5)),
        feedback_purity_p05=float(np.percentile(feedback_purity, 5)),
        unwanted_power_reduction_factor=float(open_unwanted / fb_unwanted),
    )
