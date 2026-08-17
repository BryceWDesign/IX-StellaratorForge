"""Low/intermediate-authority vacuum-field co-design experiments.

The purpose is falsification and architecture search before production MHD/coil solvers.
Fields are calculated directly from filament Biot-Savart law.  A family of toroidal-field
loops plus helical windings is scanned and field lines are integrated in toroidal angle.
No result in this module is a finite-beta equilibrium or a qualified magnet.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from functools import lru_cache
from math import pi

import numpy as np

from .coil_screen import MU0, _poloidal_loop
from .coil_hybrid import _helical_loop


@dataclass(frozen=True)
class VacuumCoDesignResult:
    nfp: int
    helical_coil_count: int
    sign_pattern: str
    helical_to_tf_current_ratio: float
    tf_current_MA_turn_per_filament: float
    mean_iota: float
    iota_std: float
    mean_radial_excursion_m: float
    max_radial_excursion_m: float
    normalized_max_excursion_over_a: float
    nestedness_screen_pass: bool
    transform_screen_pass: bool
    combined_screen_pass: bool
    authority: str = "intermediate_vacuum_biot_savart_field_line_screen"


def _segments(curves: list[np.ndarray], currents: list[float]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    mids, dls, amps = [], [], []
    for curve, current in zip(curves, currents, strict=True):
        nxt = np.roll(curve, -1, axis=0)
        mids.append(0.5 * (nxt + curve))
        dls.append(nxt - curve)
        amps.append(np.full(len(curve), current))
    return np.concatenate(mids), np.concatenate(dls), np.concatenate(amps)


def _field(pts: np.ndarray, mid: np.ndarray, dl: np.ndarray, current: np.ndarray) -> np.ndarray:
    r = pts[:, None, :] - mid[None, :, :]
    norm = np.linalg.norm(r, axis=2)
    cross = np.cross(dl[None, :, :], r)
    return MU0 / (4 * pi) * np.sum(
        cross * (current[None, :, None] / np.maximum(norm[:, :, None] ** 3, 1e-30)),
        axis=1,
    )


def _tf_current_for_axis_field(R: float, coil_r: float, target_B_T: float, coil_count: int = 24) -> tuple[list[np.ndarray], float]:
    phis = np.linspace(0.0, 2 * pi, coil_count, endpoint=False)
    curves = [_poloidal_loop(phi, R, coil_r, nseg=36) for phi in phis]
    mid, dl, unit = _segments(curves, [1.0] * coil_count)
    pa = np.linspace(0.0, 2 * pi, 24, endpoint=False)
    axis = np.column_stack((R * np.cos(pa), R * np.sin(pa), np.zeros_like(pa)))
    ephi = np.column_stack((-np.sin(pa), np.cos(pa), np.zeros_like(pa)))
    B = _field(axis, mid, dl, unit)
    per_amp = float(np.mean(np.einsum("ij,ij->i", B, ephi)))
    return curves, target_B_T / per_amp


def _rhs(phi: float, Rvals: np.ndarray, Zvals: np.ndarray, segments: tuple[np.ndarray, np.ndarray, np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    mid, dl, current = segments
    pts = np.column_stack((Rvals * np.cos(phi), Rvals * np.sin(phi), Zvals))
    B = _field(pts, mid, dl, current)
    ephi = np.column_stack((-np.sin(phi) * np.ones_like(Rvals), np.cos(phi) * np.ones_like(Rvals), np.zeros_like(Rvals)))
    er = np.column_stack((np.cos(phi) * np.ones_like(Rvals), np.sin(phi) * np.ones_like(Rvals), np.zeros_like(Rvals)))
    Bphi = np.einsum("ij,ij->i", B, ephi)
    Br = np.einsum("ij,ij->i", B, er)
    safe = np.where(np.abs(Bphi) < 1e-8, np.sign(Bphi) * 1e-8 + (Bphi == 0) * 1e-8, Bphi)
    return Rvals * Br / safe, Rvals * B[:, 2] / safe


def evaluate_helical_architecture(
    *, nfp: int, R: float, a: float, clearance_m: float, target_B_T: float,
    helical_coil_count: int = 4, sign_pattern: str = "alternating",
    helical_to_tf_current_ratio: float = 0.25, turns: int = 3, steps_per_turn: int = 48,
    iota_min: float = 0.25, iota_max: float = 0.80, max_excursion_fraction: float = 0.20,
) -> VacuumCoDesignResult:
    if nfp < 1 or helical_coil_count < 2 or min(R, a, clearance_m, target_B_T) <= 0:
        raise ValueError("invalid vacuum co-design inputs")
    if sign_pattern not in {"same", "alternating"}:
        raise ValueError("sign_pattern must be same or alternating")
    coil_r = a + clearance_m
    tf, Itf = _tf_current_for_axis_field(R, coil_r, target_B_T)
    phases = np.linspace(0.0, 2 * pi, helical_coil_count, endpoint=False)
    helical = [_helical_loop(R, coil_r, nfp, phase, nseg=120) for phase in phases]
    signs = np.ones(helical_coil_count)
    if sign_pattern == "alternating":
        signs[1::2] = -1.0
    currents = [Itf] * len(tf) + list(Itf * helical_to_tf_current_ratio * signs)
    segments = _segments(tf + helical, currents)

    radii0 = np.array([0.25, 0.50, 0.75]) * a
    Rvals = R + radii0
    Zvals = np.zeros_like(Rvals)
    theta_prev = np.zeros_like(Rvals)
    theta_unwrapped = np.zeros_like(Rvals)
    rmin = np.full_like(Rvals, np.inf)
    rmax = np.zeros_like(Rvals)
    dphi = 2 * pi / steps_per_turn
    for step in range(turns * steps_per_turn):
        phi = step * dphi
        k1R, k1Z = _rhs(phi, Rvals, Zvals, segments)
        k2R, k2Z = _rhs(phi + 0.5 * dphi, Rvals + 0.5 * dphi * k1R, Zvals + 0.5 * dphi * k1Z, segments)
        Rvals = Rvals + dphi * k2R
        Zvals = Zvals + dphi * k2Z
        radial = np.hypot(Rvals - R, Zvals)
        rmin = np.minimum(rmin, radial)
        rmax = np.maximum(rmax, radial)
        theta = np.arctan2(Zvals, Rvals - R)
        delta = (theta - theta_prev + pi) % (2 * pi) - pi
        theta_unwrapped += delta
        theta_prev = theta
        if not np.all(np.isfinite(Rvals)) or np.max(np.abs(Rvals - R)) > 4 * a or np.max(np.abs(Zvals)) > 4 * a:
            break

    iotas = theta_unwrapped / (2 * pi * max(turns, 1))
    excursions = rmax - rmin
    mean_iota = float(np.mean(np.abs(iotas)))
    max_exc = float(np.max(excursions))
    nested = bool(max_exc / a <= max_excursion_fraction)
    transform = bool(iota_min <= mean_iota <= iota_max)
    return VacuumCoDesignResult(
        nfp=nfp,
        helical_coil_count=helical_coil_count,
        sign_pattern=sign_pattern,
        helical_to_tf_current_ratio=helical_to_tf_current_ratio,
        tf_current_MA_turn_per_filament=float(Itf / 1e6),
        mean_iota=mean_iota,
        iota_std=float(np.std(np.abs(iotas))),
        mean_radial_excursion_m=float(np.mean(excursions)),
        max_radial_excursion_m=max_exc,
        normalized_max_excursion_over_a=max_exc / a,
        nestedness_screen_pass=nested,
        transform_screen_pass=transform,
        combined_screen_pass=bool(nested and transform),
    )


@lru_cache(maxsize=8)
def scan_classical_helical_family(*, R: float, a: float, clearance_m: float, target_B_T: float) -> tuple[VacuumCoDesignResult, ...]:
    """Deterministic architecture scan used as negative/positive evidence, never as G1/G2 proof."""
    results: list[VacuumCoDesignResult] = []
    for nfp in (2, 3, 4, 6):
        for pattern in ("same", "alternating"):
            for ratio in (0.08, 0.15, 0.25, 0.40, 0.60):
                results.append(evaluate_helical_architecture(
                    nfp=nfp, R=R, a=a, clearance_m=clearance_m, target_B_T=target_B_T,
                    sign_pattern=pattern, helical_to_tf_current_ratio=ratio,
                ))
    return tuple(results)


def best_architecture(results: tuple[VacuumCoDesignResult, ...]) -> VacuumCoDesignResult:
    if not results:
        raise ValueError("no results")
    def score(r: VacuumCoDesignResult) -> float:
        iota_penalty = 0.0 if 0.25 <= r.mean_iota <= 0.80 else min(abs(r.mean_iota - 0.25), abs(r.mean_iota - 0.80))
        excursion_penalty = max(0.0, r.normalized_max_excursion_over_a - 0.20)
        return iota_penalty + 2.0 * excursion_penalty + 0.05 * r.iota_std
    return min(results, key=score)


def as_jsonable(result: VacuumCoDesignResult) -> dict[str, object]:
    return asdict(result)
