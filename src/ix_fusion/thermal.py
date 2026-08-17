from __future__ import annotations

from .models import CandidateConfig


def heat_spreading_proxy(config: CandidateConfig) -> float:
    """Dimensionless plasma-facing heat-distribution screen; larger is better.

    This function has no material model, surface temperature, coolant model, or MW/m^2
    authority. It exists only so geometry complexity cannot be treated as engineering-free.
    """
    harmonic_energy = sum(h.amplitude**2 for h in config.harmonics)
    shaping = abs(config.axis_helical_amplitude) / max(config.minor_radius, 1e-12)
    return float(1.0 / (1.0 + 35.0 * harmonic_energy + 0.12 * shaping + 0.02 * config.nfp))
