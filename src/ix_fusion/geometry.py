from __future__ import annotations

import numpy as np

from .models import CandidateConfig


def magnetic_axis(phi: np.ndarray, config: CandidateConfig) -> np.ndarray:
    """Return a smooth, dimensionless 3-D magnetic-axis surrogate.

    This is geometry for screening and plotting. It is not a coil centerline or a solved
    MHD equilibrium axis.
    """
    phi = np.asarray(phi, dtype=float)
    r = config.major_radius + config.axis_helical_amplitude * np.cos(config.nfp * phi)
    z = config.axis_helical_amplitude * np.sin(config.nfp * phi)
    x = r * np.cos(phi)
    y = r * np.sin(phi)
    return np.column_stack((x, y, z))


def boundary_points(theta: np.ndarray, phi: np.ndarray, config: CandidateConfig) -> np.ndarray:
    """Map poloidal/toroidal angles to a reduced 3-D toroidal boundary surrogate."""
    theta = np.asarray(theta, dtype=float)
    phi = np.asarray(phi, dtype=float)
    helical = config.axis_helical_amplitude / max(config.minor_radius, 1e-12)
    local_a = config.minor_radius * (1.0 + 0.10 * helical * np.cos(config.nfp * phi))
    r_axis = config.major_radius + config.axis_helical_amplitude * np.cos(config.nfp * phi)
    z_axis = config.axis_helical_amplitude * np.sin(config.nfp * phi)
    r = r_axis + local_a * np.cos(theta)
    z = z_axis + local_a * np.sin(theta) + 0.08 * config.minor_radius * helical * np.sin(
        theta - config.nfp * phi
    )
    x = r * np.cos(phi)
    y = r * np.sin(phi)
    return np.column_stack((x, y, z))


def periodicity_error(config: CandidateConfig, samples: int = 128) -> float:
    phi = np.linspace(0.0, 2.0 * np.pi, samples, endpoint=False)
    theta = np.linspace(0.0, 2.0 * np.pi, samples, endpoint=False)
    p0 = boundary_points(theta, phi, config)
    shift = 2.0 * np.pi / config.nfp
    p1 = boundary_points(theta, phi + shift, config)
    # Rotate p0 around z by one field period before comparison.
    c, s = np.cos(shift), np.sin(shift)
    x = c * p0[:, 0] - s * p0[:, 1]
    y = s * p0[:, 0] + c * p0[:, 1]
    rotated = np.column_stack((x, y, p0[:, 2]))
    return float(np.max(np.linalg.norm(rotated - p1, axis=1)))
