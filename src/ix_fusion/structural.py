from __future__ import annotations

import numpy as np

from .geometry import magnetic_axis
from .models import CandidateConfig, StructuralMetrics


def _curve_derivatives(points: np.ndarray, step: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    d1 = np.gradient(points, step, axis=0, edge_order=2)
    d2 = np.gradient(d1, step, axis=0, edge_order=2)
    d3 = np.gradient(d2, step, axis=0, edge_order=2)
    return d1, d2, d3


def structural_metrics(config: CandidateConfig, samples: int = 720) -> StructuralMetrics:
    phi = np.linspace(0.0, 2.0 * np.pi, samples, endpoint=False)
    points = magnetic_axis(phi, config)
    # close the periodic curve for robust central differences
    padded = np.vstack([points[-2:], points, points[:2]])
    h = 2.0 * np.pi / samples
    d1, d2, d3 = _curve_derivatives(padded, h)
    d1, d2, d3 = d1[2:-2], d2[2:-2], d3[2:-2]
    cross = np.cross(d1, d2)
    cross_norm = np.linalg.norm(cross, axis=1)
    speed = np.linalg.norm(d1, axis=1)
    curvature = cross_norm / np.maximum(speed**3, 1e-12)
    torsion = np.einsum("ij,ij->i", cross, d3) / np.maximum(cross_norm**2, 1e-12)
    # Screening-only burden. It intentionally has no stress units.
    burden = float(
        np.sqrt(np.mean(curvature**2))
        * (1.0 + 0.5 * np.sqrt(np.mean(torsion**2)))
        * (1.0 + 0.04 * config.nfp)
    )
    return StructuralMetrics(
        axis_curvature_rms=float(np.sqrt(np.mean(curvature**2))),
        axis_curvature_max=float(np.max(curvature)),
        axis_torsion_rms=float(np.sqrt(np.mean(torsion**2))),
        normalized_support_burden=burden,
    )
