"""Intermediate-authority Biot-Savart coil reconstruction diagnostic.

This module intentionally does not claim a buildable stellarator magnet. It asks a narrower
question: can a simple set of planar encircling filament coils reproduce a 6 T toroidal field
while keeping B.normal acceptably small on the current reduced plasma boundary? Failure is
useful evidence that shaping-coil or true single-stage optimization is mandatory.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from math import pi
import numpy as np

MU0 = 4e-7 * pi


@dataclass(frozen=True)
class CoilScreenResult:
    nfp: int
    coil_count: int
    mean_axis_field_T: float
    axis_field_std_T: float
    mean_abs_Bn_over_B: float
    rms_Bn_over_B: float
    max_abs_Bn_over_B: float
    max_filament_current_MA_turn: float
    clearance_m: float
    authority: str = "intermediate_biot_savart_filament_screen"


def _surface(
    R: float,
    a: float,
    nfp: int,
    axis_amp: float,
    nt: int = 14,
    npf: int = 24,
    theta_offset: float = 0.0,
    phi_offset: float = 0.0,
):
    """Return the reduced boundary and **analytic** unit normals.

    Earlier releases estimated surface derivatives using centered finite differences on the
    evaluation grid.  That made B.normal metrics mildly resolution dependent.  v0.3 uses
    exact derivatives of the reduced Fourier-like surface parameterization, so training and
    held-out grids can be compared without changing the geometry through the differencing
    stencil.  This remains a reduced boundary, not an MHD equilibrium.
    """
    th = theta_offset + np.linspace(0.0, 2 * pi, nt, endpoint=False)
    ph = phi_offset + np.linspace(0.0, 2 * pi, npf, endpoint=False)
    T, P = np.meshgrid(th, ph, indexing="ij")

    cnp = np.cos(nfp * P)
    snp = np.sin(nfp * P)
    rax = R + axis_amp * cnp
    zax = axis_amp * snp
    aa = a * (1.0 + 0.03 * cnp)

    rr = rax + aa * np.cos(T)
    zz = zax + aa * np.sin(T) + 0.05 * a * np.sin(T - nfp * P)

    daa_dphi = -0.03 * a * nfp * snp
    drax_dphi = -axis_amp * nfp * snp
    dzax_dphi = axis_amp * nfp * cnp

    drr_dtheta = -aa * np.sin(T)
    drr_dphi = drax_dphi + daa_dphi * np.cos(T)
    dzz_dtheta = aa * np.cos(T) + 0.05 * a * np.cos(T - nfp * P)
    dzz_dphi = (
        dzax_dphi
        + daa_dphi * np.sin(T)
        - 0.05 * a * nfp * np.cos(T - nfp * P)
    )

    xyz = np.stack((rr * np.cos(P), rr * np.sin(P), zz), axis=-1)
    dtheta = np.stack(
        (drr_dtheta * np.cos(P), drr_dtheta * np.sin(P), dzz_dtheta), axis=-1
    )
    dphi = np.stack(
        (
            drr_dphi * np.cos(P) - rr * np.sin(P),
            drr_dphi * np.sin(P) + rr * np.cos(P),
            dzz_dphi,
        ),
        axis=-1,
    )
    normal = np.cross(dtheta, dphi)
    normal /= np.linalg.norm(normal, axis=-1, keepdims=True)
    return xyz.reshape(-1, 3), normal.reshape(-1, 3)


def _poloidal_loop(phi0: float, R: float, coil_minor_radius: float, nseg: int = 120):
    t = np.linspace(0.0, 2*pi, nseg, endpoint=False)
    rr = R + coil_minor_radius*np.cos(t)
    z = coil_minor_radius*np.sin(t)
    return np.column_stack((rr*np.cos(phi0), rr*np.sin(phi0), z))


def _field_per_amp(eval_pts: np.ndarray, curve: np.ndarray) -> np.ndarray:
    nxt = np.roll(curve, -1, axis=0)
    dl = nxt - curve
    mid = 0.5*(nxt + curve)
    r = eval_pts[:, None, :] - mid[None, :, :]
    norm = np.linalg.norm(r, axis=2)
    cross = np.cross(dl[None, :, :], r)
    return MU0/(4*pi) * np.sum(cross/np.maximum(norm[:, :, None]**3, 1e-24), axis=1)


def planar_encircling_coil_screen(*, nfp: int, R: float, a: float, clearance_m: float, target_B_T: float, coil_count: int = 24, axis_amp: float = 0.15) -> CoilScreenResult:
    if nfp < 1 or min(R, a, clearance_m, target_B_T) <= 0 or coil_count < 4:
        raise ValueError("invalid coil screen inputs")
    boundary, normal = _surface(R, a, nfp, axis_amp)
    coil_r = a + clearance_m
    phis = np.linspace(0.0, 2*pi, coil_count, endpoint=False)
    curves = [_poloidal_loop(phi, R, coil_r) for phi in phis]
    b_boundary = np.stack([_field_per_amp(boundary, c) for c in curves], axis=2)
    A_n = np.einsum("pi,pic->pc", normal, b_boundary)

    pa = np.linspace(0.0, 2*pi, 24, endpoint=False)
    axis = np.column_stack((R*np.cos(pa), R*np.sin(pa), np.zeros_like(pa)))
    ephi = np.column_stack((-np.sin(pa), np.cos(pa), np.zeros_like(pa)))
    b_axis = np.stack([_field_per_amp(axis, c) for c in curves], axis=2)
    A_phi = np.einsum("pi,pic->pc", ephi, b_axis)

    # Strongly enforce axis field while minimizing normal field. Filament currents are
    # equivalent ampere-turns, not a conductor design.
    weight_axis = 100.0
    M = np.vstack((A_n, weight_axis*A_phi))
    y = np.concatenate((np.zeros(A_n.shape[0]), np.full(A_phi.shape[0], weight_axis*target_B_T)))
    currents, *_ = np.linalg.lstsq(M, y, rcond=None)

    B = np.einsum("pic,c->pi", b_boundary, currents)
    bmag = np.linalg.norm(B, axis=1)
    rel = np.abs(np.einsum("pi,pi->p", B, normal))/np.maximum(bmag, 1e-12)
    Baxis = np.einsum("pic,c->pi", b_axis, currents)
    bphi = np.einsum("pi,pi->p", Baxis, ephi)
    return CoilScreenResult(
        nfp=nfp,
        coil_count=coil_count,
        mean_axis_field_T=float(np.mean(bphi)),
        axis_field_std_T=float(np.std(bphi)),
        mean_abs_Bn_over_B=float(np.mean(rel)),
        rms_Bn_over_B=float(np.sqrt(np.mean(rel**2))),
        max_abs_Bn_over_B=float(np.max(rel)),
        max_filament_current_MA_turn=float(np.max(np.abs(currents))/1e6),
        clearance_m=clearance_m,
    )


def as_jsonable(result: CoilScreenResult) -> dict[str, float | int | str]:
    return asdict(result)
