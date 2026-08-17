from __future__ import annotations

import numpy as np

from .models import CandidateConfig


def helical_strength(config: CandidateConfig) -> float:
    return float(sum(abs(h.amplitude) for h in config.harmonics))


def field_strength(theta: np.ndarray, phi: np.ndarray, config: CandidateConfig) -> np.ndarray:
    """Reduced field-strength spectrum B/B0 on angular coordinates.

    It is intentionally dimensionless. It supports screening symmetry, mirror and trapped-
    particle proxies; it is not a Biot-Savart or MHD equilibrium solution.
    """
    theta = np.asarray(theta, dtype=float)
    phi = np.asarray(phi, dtype=float)
    b = np.ones(np.broadcast(theta, phi).shape, dtype=float)
    b += config.mirror_amplitude * np.cos(config.nfp * phi)
    for harmonic in config.harmonics:
        phase = harmonic.m * theta - harmonic.n * phi + harmonic.phase
        b += harmonic.amplitude * np.cos(phase)
    return b


def derivatives(r: np.ndarray, theta: np.ndarray, phi: float, config: CandidateConfig) -> tuple[np.ndarray, np.ndarray]:
    """Reduced field-line ODE used only for falsifiable screening.

    The radial envelope damps perturbations near the axis and last closed screening surface.
    This is not a substitute for equilibrium-derived B field integration.
    """
    r = np.asarray(r, dtype=float)
    theta = np.asarray(theta, dtype=float)
    envelope = np.clip(r * (1.0 - r), 0.0, None)
    dr = np.zeros_like(r)
    dtheta = config.iota0 + config.shear * (r - 0.5)
    for harmonic in config.harmonics:
        phase = harmonic.m * theta - harmonic.n * phi + harmonic.phase
        dr += harmonic.amplitude * envelope * np.sin(phase)
        dtheta += 0.08 * harmonic.amplitude * np.cos(phase)
    return dr, dtheta


def resonant_overlap_proxy(config: CandidateConfig) -> float:
    total = 0.0
    for harmonic in config.harmonics:
        detuning = abs(harmonic.m * config.iota0 - harmonic.n)
        total += harmonic.amplitude**2 / (0.02 + detuning**2)
    return float(total)


def field_strength_cv(config: CandidateConfig, ntheta: int = 48, nphi: int = 72) -> float:
    theta = np.linspace(0, 2 * np.pi, ntheta, endpoint=False)[:, None]
    phi = np.linspace(0, 2 * np.pi, nphi, endpoint=False)[None, :]
    b = field_strength(theta, phi, config)
    return float(np.std(b) / np.mean(b))
