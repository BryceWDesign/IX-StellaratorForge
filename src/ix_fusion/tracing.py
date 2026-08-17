from __future__ import annotations

import numpy as np

from .field import derivatives
from .models import CandidateConfig, TraceMetrics


def trace_field_lines(
    config: CandidateConfig,
    initial_radii: np.ndarray | None = None,
    initial_thetas: np.ndarray | None = None,
    turns: int = 24,
    steps_per_turn: int = 180,
) -> dict[str, np.ndarray]:
    if initial_radii is None:
        initial_radii = np.array([0.18, 0.35, 0.52, 0.68, 0.82], dtype=float)
    if initial_thetas is None:
        initial_thetas = np.linspace(0.0, 2.0 * np.pi, len(initial_radii), endpoint=False)
    r = np.asarray(initial_radii, dtype=float).copy()
    theta = np.asarray(initial_thetas, dtype=float).copy()
    if r.shape != theta.shape:
        raise ValueError("initial_radii and initial_thetas must have matching shapes")
    total_steps = turns * steps_per_turn
    h = 2.0 * np.pi / steps_per_turn
    rs = np.empty((total_steps + 1, len(r)), dtype=float)
    thetas = np.empty_like(rs)
    phis = np.arange(total_steps + 1, dtype=float) * h
    rs[0] = r
    thetas[0] = theta
    for idx in range(total_steps):
        phi = phis[idx]
        k1r, k1t = derivatives(r, theta, phi, config)
        k2r, k2t = derivatives(r + 0.5 * h * k1r, theta + 0.5 * h * k1t, phi + 0.5 * h, config)
        k3r, k3t = derivatives(r + 0.5 * h * k2r, theta + 0.5 * h * k2t, phi + 0.5 * h, config)
        k4r, k4t = derivatives(r + h * k3r, theta + h * k3t, phi + h, config)
        r = r + (h / 6.0) * (k1r + 2 * k2r + 2 * k3r + k4r)
        theta = theta + (h / 6.0) * (k1t + 2 * k2t + 2 * k3t + k4t)
        rs[idx + 1] = r
        thetas[idx + 1] = theta
    return {"phi": phis, "r": rs, "theta": thetas}


def trace_metrics(trace: dict[str, np.ndarray]) -> TraceMetrics:
    r = trace["r"]
    theta = trace["theta"]
    phi = trace["phi"]
    radial_excursion = np.max(r, axis=0) - np.min(r, axis=0)
    escaped = np.any((r <= 0.02) | (r >= 0.98), axis=0)
    spread = np.std(r, axis=0)
    total_phi = phi[-1] - phi[0]
    iota = (theta[-1] - theta[0]) / total_phi
    return TraceMetrics(
        mean_radial_excursion=float(np.mean(radial_excursion)),
        p95_radial_excursion=float(np.percentile(radial_excursion, 95)),
        max_radial_excursion=float(np.max(radial_excursion)),
        escape_fraction=float(np.mean(escaped)),
        mean_surface_spread=float(np.mean(spread)),
        iota_estimate_mean=float(np.mean(iota)),
        iota_estimate_std=float(np.std(iota)),
    )


def poincare_points(trace: dict[str, np.ndarray], steps_per_turn: int = 180) -> tuple[np.ndarray, np.ndarray]:
    r = trace["r"][::steps_per_turn]
    theta = np.mod(trace["theta"][::steps_per_turn], 2.0 * np.pi)
    return r, theta
