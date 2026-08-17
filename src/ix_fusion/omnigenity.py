from __future__ import annotations

import numpy as np

from .field import field_strength, field_strength_cv
from .models import CandidateConfig, OmnigenityMetrics


def bounce_action_proxy(
    config: CandidateConfig,
    alphas: np.ndarray | None = None,
    lambdas: np.ndarray | None = None,
    samples: int = 1024,
    turns: int = 4,
) -> np.ndarray:
    """Return a reduced bounce-action-variation proxy.

    The proxy samples B along idealized field lines theta = alpha + iota*phi and integrates
    sqrt(max(1-lambda*B, 0)). It is useful for comparative screening only; it is not the
    second adiabatic invariant from a solved equilibrium and must not be reported as such.
    """
    if alphas is None:
        alphas = np.linspace(0.0, 2.0 * np.pi, 24, endpoint=False)
    if lambdas is None:
        # Dimensionless pitch values chosen from the field-strength range.
        lambdas = np.array([0.90, 0.94, 0.98], dtype=float)
    phi = np.linspace(0.0, turns * 2.0 * np.pi, samples, endpoint=False)
    result = np.empty((len(lambdas), len(alphas)), dtype=float)
    for ia, alpha in enumerate(alphas):
        theta = alpha + config.iota0 * phi
        b = field_strength(theta, phi, config)
        b = b / np.mean(b)
        for il, lam in enumerate(lambdas):
            parallel = np.sqrt(np.clip(1.0 - lam * b, 0.0, None))
            result[il, ia] = float(np.trapezoid(parallel, phi) / (phi[-1] - phi[0]))
    return result


def omnigenity_metrics(config: CandidateConfig) -> OmnigenityMetrics:
    actions = bounce_action_proxy(config)
    means = np.mean(actions, axis=1)
    variations = np.std(actions, axis=1) / np.maximum(np.abs(means), 1e-12)
    theta = np.linspace(0, 2 * np.pi, 72, endpoint=False)[:, None]
    phi = np.linspace(0, 2 * np.pi, 96, endpoint=False)[None, :]
    b = field_strength(theta, phi, config)
    mirror_ratio = float((np.max(b) - np.min(b)) / np.mean(b))
    return OmnigenityMetrics(
        action_variation_mean=float(np.mean(variations)),
        action_variation_p95=float(np.percentile(variations, 95)),
        field_strength_cv=field_strength_cv(config),
        mirror_ratio=mirror_ratio,
    )
