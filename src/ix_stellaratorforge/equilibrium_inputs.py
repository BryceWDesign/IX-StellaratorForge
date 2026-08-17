"""High-fidelity equilibrium input generation for SFR-1.

This module does not solve MHD equilibrium.  It converts the current analytic SFR-1
screening boundary and design-point pressure/flux targets into reproducible VMEC-family
input files.  DESC 0.17.x can ingest VMEC input files directly, while VMEC++ can run the
same fixed-boundary namelist.  Solver output must be imported before G1 can be promoted.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from math import pi
from pathlib import Path
from typing import Iterable

import numpy as np

MU0 = 4e-7 * pi


@dataclass(frozen=True)
class EquilibriumSeed:
    candidate_id: str
    nfp: int
    major_radius_m: float
    minor_radius_m: float
    axis_helical_amplitude_m: float
    field_axis_T: float
    volume_average_beta_target: float
    toroidal_flux_Wb_screen: float
    pressure_axis_Pa_screen: float
    iota_axis_target: float
    iota_edge_target: float
    authority: str = "solver_input_seed_not_equilibrium_evidence"


def volume_average_pressure_from_beta(beta: float, field_T: float) -> float:
    if not (0 < beta < 1) or field_T <= 0:
        raise ValueError("beta must be in (0,1) and field must be positive")
    return beta * field_T**2 / (2 * MU0)


def pressure_axis_for_quadratic_s_profile(beta: float, field_T: float) -> float:
    """Axis pressure for p(s)=p0(1-s)^2 using a circular-volume screening average.

    For a circular torus with s=rho^2, the volume measure is approximately uniform in s,
    so <(1-s)^2> = 1/3 and p0 = 3 <p>.  This is only an input seed; the solved beta must be
    read back from DESC/VMEC++ rather than assumed from this relation.
    """
    return 3.0 * volume_average_pressure_from_beta(beta, field_T)


def toroidal_flux_screen(field_T: float, minor_radius_m: float) -> float:
    if field_T <= 0 or minor_radius_m <= 0:
        raise ValueError("positive field and minor radius required")
    return field_T * pi * minor_radius_m**2


def make_seed(
    *, candidate_id: str, nfp: int, R: float, a: float, field_T: float, beta: float,
    axis_amp: float = 0.15, iota_axis: float = 0.50, iota_edge: float = 0.60,
) -> EquilibriumSeed:
    if nfp < 1 or min(R, a, field_T) <= 0 or axis_amp < 0:
        raise ValueError("invalid equilibrium seed")
    return EquilibriumSeed(
        candidate_id=candidate_id,
        nfp=nfp,
        major_radius_m=R,
        minor_radius_m=a,
        axis_helical_amplitude_m=axis_amp,
        field_axis_T=field_T,
        volume_average_beta_target=beta,
        toroidal_flux_Wb_screen=toroidal_flux_screen(field_T, a),
        pressure_axis_Pa_screen=pressure_axis_for_quadratic_s_profile(beta, field_T),
        iota_axis_target=iota_axis,
        iota_edge_target=iota_edge,
    )


def vmec_boundary_coefficients(seed: EquilibriumSeed) -> dict[str, dict[tuple[int, int], float]]:
    """Return exact Fourier coefficients for the reduced boundary used by v0.3/v0.4.

    VMEC convention here is R=sum RBC(n,m) cos(m*theta-n*NFP*phi) and
    Z=sum ZBS(n,m) sin(m*theta-n*NFP*phi).
    """
    R, a, A = seed.major_radius_m, seed.minor_radius_m, seed.axis_helical_amplitude_m
    rbc = {
        (0, 0): R,
        (0, 1): a,
        (1, 0): A,
        (1, 1): 0.015 * a,
        (-1, 1): 0.015 * a,
    }
    zbs = {
        (0, 1): a,
        (1, 0): -A,
        (1, 1): 0.065 * a,
        (-1, 1): 0.015 * a,
    }
    return {"RBC": rbc, "ZBS": zbs}


def reconstruct_boundary(seed: EquilibriumSeed, theta: np.ndarray, phi: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    coeffs = vmec_boundary_coefficients(seed)
    R = np.zeros(np.broadcast(theta, phi).shape, dtype=float)
    Z = np.zeros_like(R)
    for (n, m), c in coeffs["RBC"].items():
        R += c * np.cos(m * theta - n * seed.nfp * phi)
    for (n, m), c in coeffs["ZBS"].items():
        Z += c * np.sin(m * theta - n * seed.nfp * phi)
    return R, Z


def analytic_boundary(seed: EquilibriumSeed, theta: np.ndarray, phi: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    R0, a, A, nfp = (
        seed.major_radius_m, seed.minor_radius_m,
        seed.axis_helical_amplitude_m, seed.nfp,
    )
    cnp = np.cos(nfp * phi)
    rax = R0 + A * cnp
    zax = A * np.sin(nfp * phi)
    aa = a * (1.0 + 0.03 * cnp)
    rr = rax + aa * np.cos(theta)
    zz = zax + aa * np.sin(theta) + 0.05 * a * np.sin(theta - nfp * phi)
    return rr, zz


def render_vmec_input(seed: EquilibriumSeed) -> str:
    """Render a fixed-boundary finite-pressure VMEC/VMEC++ seed namelist.

    The iota profile and flux are design seeds, not outputs.  G1 requires convergence and
    force-residual evidence from an actual solver plus a cross-code comparison.
    """
    coeffs = vmec_boundary_coefficients(seed)
    # AI is in normalized toroidal flux s.  Linear interpolation from axis to edge.
    ai1 = seed.iota_edge_target - seed.iota_axis_target
    lines = [
        "&INDATA",
        "  LFREEB = F",
        "  LASYM = F",
        f"  NFP = {seed.nfp}",
        "  NCURR = 0",
        "  GAMMA = 0",
        f"  PHIEDGE = {seed.toroidal_flux_Wb_screen:.12g}",
        f"  PRES_SCALE = {seed.pressure_axis_Pa_screen:.12g}",
        '  PMASS_TYPE = "power_series"',
        "  AM = 1.0 -2.0 1.0",
        f"  AI = {seed.iota_axis_target:.12g} {ai1:.12g}",
        f"  RAXIS = {seed.major_radius_m:.12g}",
        "  ZAXIS = 0.0",
        "  MPOL = 8",
        "  NTOR = 4",
        "  NS_ARRAY = 16 32 64 128 256",
        "  NITER_ARRAY = 4000 8000 12000 16000 24000",
        "  FTOL_ARRAY = 1e-8 1e-9 1e-10 1e-11 1e-12",
    ]
    for key in ("RBC", "ZBS"):
        for (n, m), val in sorted(coeffs[key].items()):
            lines.append(f"  {key}({n},{m}) = {val:.12g}")
    lines += ["/", "&END", ""]
    return "\n".join(lines)


def write_seed_pack(seeds: Iterable[EquilibriumSeed], directory: Path) -> list[Path]:
    directory.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for seed in seeds:
        path = directory / f"input.{seed.candidate_id}"
        path.write_text(render_vmec_input(seed), encoding="utf-8")
        written.append(path)
    return written


def seed_json(seed: EquilibriumSeed) -> dict[str, object]:
    d = asdict(seed)
    d["boundary_coefficients"] = {
        key: {f"n={n},m={m}": value for (n, m), value in vals.items()}
        for key, vals in vmec_boundary_coefficients(seed).items()
    }
    return d
