from __future__ import annotations

from .models import CandidateConfig


def cryogenic_burden_proxy(config: CandidateConfig) -> float:
    """Dimensionless cryogenic/control burden; not refrigerator power or coil heat load."""
    spectral_complexity = sum(abs(h.amplitude) * (h.m + h.n) for h in config.harmonics)
    shaping = abs(config.axis_helical_amplitude) / max(config.minor_radius, 1e-12)
    return float(1.0 + 0.05 * config.nfp + 0.45 * spectral_complexity + 0.25 * shaping)
