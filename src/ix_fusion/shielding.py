from __future__ import annotations

from .models import CandidateConfig


def blanket_space_proxy(config: CandidateConfig) -> float:
    """Dimensionless plasma-to-magnet/blanket-space screen; larger is better.

    No neutron attenuation, tritium breeding, activation, or dose calculation is implied.
    """
    aspect = config.major_radius / config.minor_radius
    shaping_penalty = 1.0 + 8.0 * abs(config.axis_helical_amplitude) / config.major_radius
    field_period_penalty = 1.0 + 0.015 * max(config.nfp - 1, 0)
    return float(aspect / (shaping_penalty * field_period_penalty))


def penetration_burden_proxy(config: CandidateConfig, actuator_ports: int = 6) -> float:
    """Dimensionless penalty for maintaining diagnostic/RF penetrations through shielding."""
    return float((actuator_ports / 6.0) * (1.0 + 0.02 * config.nfp))
