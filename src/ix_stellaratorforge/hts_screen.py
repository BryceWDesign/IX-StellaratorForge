"""Geometry-level HTS winding screens for candidate filament centerlines.

These calculations quantify centerline length, curvature and a deliberately conservative
ribbon hard-way bending strain proxy.  They do not replace conductor Ic(B,T,angle), winding
pack mechanics, joints, insulation, quench analysis or finite-element support qualification.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import numpy as np


@dataclass(frozen=True)
class CoilGeometryScreen:
    length_m: float
    min_bend_radius_m: float
    max_curvature_per_m: float
    rms_curvature_per_m: float
    hard_way_strain_proxy_fraction: float
    strain_target_fraction: float
    strain_ceiling_fraction: float
    passes_geometry_strain_proxy: bool
    authority: str = "geometry_only_rebco_strain_proxy_not_winding_pack_FEA"


def _curvature(curve: np.ndarray) -> np.ndarray:
    if curve.ndim != 2 or curve.shape[1] != 3 or len(curve) < 8:
        raise ValueError("curve must be Nx3 with at least 8 points")
    prev = np.roll(curve, 1, axis=0)
    nxt = np.roll(curve, -1, axis=0)
    ds1 = np.linalg.norm(curve - prev, axis=1)
    ds2 = np.linalg.norm(nxt - curve, axis=1)
    t1 = (curve - prev) / np.maximum(ds1[:, None], 1e-12)
    t2 = (nxt - curve) / np.maximum(ds2[:, None], 1e-12)
    ds = 0.5 * (ds1 + ds2)
    return np.linalg.norm(t2 - t1, axis=1) / np.maximum(ds, 1e-12)


def screen_curve_geometry(
    curve: np.ndarray, *, tape_width_m: float = 0.012,
    strain_target_fraction: float = 0.0035, strain_ceiling_fraction: float = 0.004,
) -> CoilGeometryScreen:
    if tape_width_m <= 0:
        raise ValueError("positive tape width required")
    nxt = np.roll(curve, -1, axis=0)
    length = float(np.sum(np.linalg.norm(nxt - curve, axis=1)))
    k = _curvature(curve)
    kmax = float(np.max(k))
    # Worst-case hard-way strain if tape orientation were not optimized: epsilon ~= k*w/2.
    # Real REBCO optimization rotates the tape frame and must calculate strain over the full
    # winding pack, so a pass here is necessary-at-best and never sufficient.
    strain = kmax * tape_width_m / 2.0
    return CoilGeometryScreen(
        length_m=length,
        min_bend_radius_m=float(1.0 / max(kmax, 1e-12)),
        max_curvature_per_m=kmax,
        rms_curvature_per_m=float(np.sqrt(np.mean(k**2))),
        hard_way_strain_proxy_fraction=float(strain),
        strain_target_fraction=strain_target_fraction,
        strain_ceiling_fraction=strain_ceiling_fraction,
        passes_geometry_strain_proxy=bool(strain <= strain_ceiling_fraction),
    )


def as_jsonable(result: CoilGeometryScreen) -> dict[str, object]:
    return asdict(result)
