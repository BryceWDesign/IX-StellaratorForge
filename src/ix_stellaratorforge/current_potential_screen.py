"""Continuous winding-surface current-potential reconstruction screen.

This is a REGCOIL-like *idea-level* independent implementation, not REGCOIL and not DESC's
FourierCurrentPotentialField.  A secular current-potential term supplies the gross toroidal
field and periodic Fourier current-potential modes attempt to reduce B.normal on the reduced
SFR-1 boundary.  Fitting and validation grids are offset.  Percent-level failure is useful
negative evidence that the boundary and magnet must be co-optimized by production tools.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from functools import lru_cache
from math import pi

import numpy as np

from .coil_screen import MU0, _surface


@dataclass(frozen=True)
class CurrentPotentialScreenResult:
    nfp: int
    basis_count: int
    winding_patch_count: int
    mean_axis_field_T: float
    axis_field_std_T: float
    train_rms_Bn_over_B0: float
    validation_rms_Bn_over_B0: float
    validation_max_abs_Bn_over_B0: float
    max_current_potential_coefficient_MA: float
    passes_reconstruction_screen: bool
    authority: str = "intermediate_surface_current_potential_screen_not_regcoil_or_buildable_coils"


def _winding_grid(R: float, aw: float, nt: int, npf: int):
    theta = (np.arange(nt) + 0.5) * 2 * pi / nt
    phi = (np.arange(npf) + 0.5) * 2 * pi / npf
    T, P = np.meshgrid(theta, phi, indexing="ij")
    rho = R + aw * np.cos(T)
    pos = np.stack((rho * np.cos(P), rho * np.sin(P), aw * np.sin(T)), axis=-1)
    etheta = np.stack((-np.sin(T) * np.cos(P), -np.sin(T) * np.sin(P), np.cos(T)), axis=-1)
    ephi = np.stack((-np.sin(P), np.cos(P), np.zeros_like(P)), axis=-1)
    dS = aw * rho * (2 * pi / nt) * (2 * pi / npf)
    return T.ravel(), P.ravel(), rho.ravel(), pos.reshape(-1, 3), etheta.reshape(-1, 3), ephi.reshape(-1, 3), dS.ravel()


def _basis(R: float, aw: float, nfp: int, mmax: int, nmax: int, nt: int, npf: int):
    T, P, rho, pos, etheta, ephi, dS = _winding_grid(R, aw, nt, npf)
    basis: list[np.ndarray] = []
    names: list[str] = []
    # Secular Phi~phi term: dPhi/dphi=1 gives poloidal surface current and toroidal B.
    K = (1.0 / rho)[:, None] * etheta
    basis.append(K * dS[:, None])
    names.append("secular_phi")
    for m in range(mmax + 1):
        for nmult in range(nmax + 1):
            if m == 0 and nmult == 0:
                continue
            alpha = m * T - nmult * nfp * P
            # Phi = sin(alpha)
            dtheta = m * np.cos(alpha)
            dphi = -nmult * nfp * np.cos(alpha)
            K = -(dtheta / aw)[:, None] * ephi + (dphi / rho)[:, None] * etheta
            basis.append(K * dS[:, None])
            names.append(f"sin_m{m}_n{nmult*nfp}")
            # Phi = cos(alpha)
            dtheta = -m * np.sin(alpha)
            dphi = nmult * nfp * np.sin(alpha)
            K = -(dtheta / aw)[:, None] * ephi + (dphi / rho)[:, None] * etheta
            basis.append(K * dS[:, None])
            names.append(f"cos_m{m}_n{nmult*nfp}")
    return pos, basis, names


def _field(eval_pts: np.ndarray, pos: np.ndarray, current_elements_per_A: np.ndarray) -> np.ndarray:
    out = np.zeros((len(eval_pts), 3))
    for start in range(0, len(eval_pts), 64):
        pts = eval_pts[start : start + 64]
        r = pts[:, None, :] - pos[None, :, :]
        norm = np.linalg.norm(r, axis=2)
        cross = np.cross(current_elements_per_A[None, :, :], r)
        out[start : start + 64] = MU0 / (4 * pi) * np.sum(
            cross / np.maximum(norm[:, :, None] ** 3, 1e-30), axis=1
        )
    return out


@lru_cache(maxsize=16)
def current_potential_screen(
    *, nfp: int, R: float, a: float, clearance_m: float, target_B_T: float,
    axis_amp: float = 0.15, mmax: int = 5, nmax: int = 3,
    reconstruction_rms_limit: float = 5e-3,
) -> CurrentPotentialScreenResult:
    if nfp < 1 or min(R, a, clearance_m, target_B_T) <= 0:
        raise ValueError("invalid current-potential screen inputs")
    aw = a + clearance_m
    train, normals = _surface(R, a, nfp, axis_amp, nt=12, npf=24)
    val, val_normals = _surface(R, a, nfp, axis_amp, nt=13, npf=25, theta_offset=0.071, phi_offset=0.041)
    pa = np.linspace(0.0, 2 * pi, 32, endpoint=False)
    axis = np.column_stack((R * np.cos(pa), R * np.sin(pa), np.zeros_like(pa)))
    ephi_axis = np.column_stack((-np.sin(pa), np.cos(pa), np.zeros_like(pa)))
    pos, basis, _ = _basis(R, aw, nfp, mmax, nmax, nt=16, npf=32)

    train_cols, val_cols, axis_cols = [], [], []
    for element in basis:
        train_cols.append(np.einsum("ij,ij->i", _field(train, pos, element), normals))
        val_cols.append(np.einsum("ij,ij->i", _field(val, pos, element), val_normals))
        axis_cols.append(np.einsum("ij,ij->i", _field(axis, pos, element), ephi_axis))
    A = np.stack(train_cols, axis=1)
    Aval = np.stack(val_cols, axis=1)
    Aaxis = np.stack(axis_cols, axis=1)

    weight_axis = 100.0
    # Small Tikhonov term suppresses ill-conditioned high-amplitude Fourier combinations.
    reg = 1e-14
    M = np.vstack((A, weight_axis * Aaxis, np.sqrt(reg) * np.eye(A.shape[1])))
    y = np.concatenate((np.zeros(len(train)), np.full(len(axis), weight_axis * target_B_T), np.zeros(A.shape[1])))
    coeff, *_ = np.linalg.lstsq(M, y, rcond=1e-12)
    bn = A @ coeff
    bn_val = Aval @ coeff
    axis_field = Aaxis @ coeff
    val_rms = float(np.sqrt(np.mean((bn_val / target_B_T) ** 2)))
    return CurrentPotentialScreenResult(
        nfp=nfp,
        basis_count=len(basis),
        winding_patch_count=len(pos),
        mean_axis_field_T=float(np.mean(axis_field)),
        axis_field_std_T=float(np.std(axis_field)),
        train_rms_Bn_over_B0=float(np.sqrt(np.mean((bn / target_B_T) ** 2))),
        validation_rms_Bn_over_B0=val_rms,
        validation_max_abs_Bn_over_B0=float(np.max(np.abs(bn_val / target_B_T))),
        max_current_potential_coefficient_MA=float(np.max(np.abs(coeff)) / 1e6),
        passes_reconstruction_screen=bool(val_rms <= reconstruction_rms_limit),
    )


def as_jsonable(result: CurrentPotentialScreenResult) -> dict[str, object]:
    return asdict(result)
