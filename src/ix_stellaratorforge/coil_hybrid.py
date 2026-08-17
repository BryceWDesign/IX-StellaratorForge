"""Held-out Biot-Savart screen for a richer filament-coil basis.

This module is intentionally *not* a production stellarator coil optimizer.  It extends the
v0.2 planar-loop falsification test with helical and local saddle-loop basis coils, solves
only their ampere-turns by regularized linear least squares, and evaluates B.normal on a
separate offset surface grid.  A small training residual is therefore not allowed to hide
poor spatial generalization.

Authority: intermediate magnetic reconstruction screen.  Structural mechanics, finite
winding packs, REBCO strain/current density, joints, quench protection, free-boundary MHD,
and manufacturing tolerances remain outside this calculation.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from functools import lru_cache
from math import pi

import numpy as np

from .coil_screen import _field_per_amp, _poloidal_loop, _surface


@dataclass(frozen=True)
class HybridCoilScreenResult:
    nfp: int
    coil_count: int
    basis: str
    mean_axis_field_T: float
    axis_field_std_T: float
    train_mean_abs_Bn_over_B0: float
    train_rms_Bn_over_B0: float
    validation_mean_abs_Bn_over_B: float
    validation_rms_Bn_over_B: float
    validation_max_abs_Bn_over_B: float
    max_filament_current_MA_turn: float
    rms_filament_current_MA_turn: float
    clearance_m: float
    passes_reconstruction_screen: bool
    authority: str = "intermediate_held_out_biot_savart_filament_screen"


def _saddle_loop(
    phi0: float,
    R: float,
    coil_minor_radius: float,
    theta0: float,
    phi_width: float = 0.20,
    theta_span: float = 1.0,
    nseg: int = 96,
) -> np.ndarray:
    u = np.linspace(0.0, 2 * pi, nseg, endpoint=False)
    phi = phi0 + phi_width * np.sin(u)
    theta = theta0 + theta_span * np.cos(u)
    rr = R + coil_minor_radius * np.cos(theta)
    zz = coil_minor_radius * np.sin(theta)
    return np.column_stack((rr * np.cos(phi), rr * np.sin(phi), zz))


def _helical_loop(
    R: float,
    coil_minor_radius: float,
    helicity: int,
    phase: float,
    nseg: int = 360,
) -> np.ndarray:
    phi = np.linspace(0.0, 2 * pi, nseg, endpoint=False)
    theta = helicity * phi + phase
    rr = R + coil_minor_radius * np.cos(theta)
    zz = coil_minor_radius * np.sin(theta)
    return np.column_stack((rr * np.cos(phi), rr * np.sin(phi), zz))


def _basis_curves(*, nfp: int, R: float, coil_minor_radius: float) -> list[np.ndarray]:
    curves: list[np.ndarray] = []
    # 24 conventional encircling loops provide the gross toroidal field.
    for phi in np.linspace(0.0, 2 * pi, 24, endpoint=False):
        curves.append(_poloidal_loop(phi, R, coil_minor_radius, nseg=96))

    # Helical basis functions around the target periodicity.  Positive and negative
    # helicities are included so the least-squares solve is not handed a preferred sign.
    harmonics = sorted({nfp, -nfp, nfp + 1, -(nfp + 1), max(1, nfp - 1), -max(1, nfp - 1)})
    for helicity in harmonics:
        for phase in np.linspace(0.0, 2 * pi, 8, endpoint=False):
            curves.append(_helical_loop(R, coil_minor_radius, helicity, phase))

    # Local saddle basis functions provide additional 3-D normal-field authority.
    for phi in np.linspace(0.0, 2 * pi, 12, endpoint=False):
        for theta in np.linspace(0.0, 2 * pi, 4, endpoint=False):
            curves.append(_saddle_loop(phi, R, coil_minor_radius, theta))
    return curves


@lru_cache(maxsize=32)
def helical_hybrid_coil_screen(
    *,
    nfp: int,
    R: float,
    a: float,
    clearance_m: float,
    target_B_T: float,
    axis_amp: float = 0.15,
    regularization: float = 1e-14,
    reconstruction_rms_limit: float = 5e-3,
) -> HybridCoilScreenResult:
    """Fit a fixed richer coil basis and validate on an unseen surface grid.

    The default 5e-3 RMS reconstruction limit is a *screening* threshold, not a universal
    reactor acceptance criterion.  It is intentionally of the same order as published
    reactor-relevant filament-coil studies so percent-level solutions cannot be promoted.
    """
    if nfp < 1 or min(R, a, clearance_m, target_B_T) <= 0:
        raise ValueError("invalid hybrid coil screen inputs")
    if regularization < 0 or reconstruction_rms_limit <= 0:
        raise ValueError("invalid regularization or reconstruction limit")

    coil_r = a + clearance_m
    curves = _basis_curves(nfp=nfp, R=R, coil_minor_radius=coil_r)

    train_pts, train_normals = _surface(R, a, nfp, axis_amp, nt=18, npf=36)
    b_train = np.stack([_field_per_amp(train_pts, c) for c in curves], axis=2)
    A_n = np.einsum("pi,pic->pc", train_normals, b_train)

    pa = np.linspace(0.0, 2 * pi, 36, endpoint=False)
    axis = np.column_stack((R * np.cos(pa), R * np.sin(pa), np.zeros_like(pa)))
    ephi = np.column_stack((-np.sin(pa), np.cos(pa), np.zeros_like(pa)))
    b_axis = np.stack([_field_per_amp(axis, c) for c in curves], axis=2)
    A_phi = np.einsum("pi,pic->pc", ephi, b_axis)

    weight_axis = 100.0
    reg_block = np.sqrt(regularization) * np.eye(len(curves))
    M = np.vstack((A_n, weight_axis * A_phi, reg_block))
    y = np.concatenate(
        (
            np.zeros(A_n.shape[0]),
            np.full(A_phi.shape[0], weight_axis * target_B_T),
            np.zeros(len(curves)),
        )
    )
    currents, *_ = np.linalg.lstsq(M, y, rcond=1e-12)

    train_bn = A_n @ currents
    train_rel = np.abs(train_bn) / target_B_T

    # Offset both angular grids so validation nodes never coincide with training nodes.
    val_pts, val_normals = _surface(
        R,
        a,
        nfp,
        axis_amp,
        nt=19,
        npf=37,
        theta_offset=0.037,
        phi_offset=0.029,
    )
    val_B = np.zeros_like(val_pts)
    for curve, current in zip(curves, currents, strict=True):
        val_B += _field_per_amp(val_pts, curve) * current
    val_bmag = np.linalg.norm(val_B, axis=1)
    val_rel = np.abs(np.einsum("pi,pi->p", val_B, val_normals)) / np.maximum(val_bmag, 1e-12)

    axis_toroidal = A_phi @ currents
    val_rms = float(np.sqrt(np.mean(val_rel**2)))
    return HybridCoilScreenResult(
        nfp=nfp,
        coil_count=len(curves),
        basis="24_encircling_plus_helical_harmonics_plus_48_saddle_filaments",
        mean_axis_field_T=float(np.mean(axis_toroidal)),
        axis_field_std_T=float(np.std(axis_toroidal)),
        train_mean_abs_Bn_over_B0=float(np.mean(train_rel)),
        train_rms_Bn_over_B0=float(np.sqrt(np.mean(train_rel**2))),
        validation_mean_abs_Bn_over_B=float(np.mean(val_rel)),
        validation_rms_Bn_over_B=val_rms,
        validation_max_abs_Bn_over_B=float(np.max(val_rel)),
        max_filament_current_MA_turn=float(np.max(np.abs(currents)) / 1e6),
        rms_filament_current_MA_turn=float(np.sqrt(np.mean(currents**2)) / 1e6),
        clearance_m=clearance_m,
        passes_reconstruction_screen=bool(val_rms <= reconstruction_rms_limit),
    )


def as_jsonable(result: HybridCoilScreenResult) -> dict[str, float | int | str | bool]:
    return asdict(result)
