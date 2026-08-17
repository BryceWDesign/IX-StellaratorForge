from __future__ import annotations

import math

from .cryogenics import cryogenic_burden_proxy
from .models import CandidateConfig, EngineeringMetrics
from .shielding import blanket_space_proxy, penetration_burden_proxy
from .structural import structural_metrics
from .thermal import heat_spreading_proxy


def engineering_metrics(config: CandidateConfig) -> EngineeringMetrics:
    structural = structural_metrics(config)
    blanket = blanket_space_proxy(config)
    heat = heat_spreading_proxy(config)
    cryo = cryogenic_burden_proxy(config)
    penetration = penetration_burden_proxy(config)
    burden = (
        structural.normalized_support_burden
        + 0.22 / max(blanket, 1e-12)
        + 0.28 / max(heat, 1e-12)
        + 0.16 * math.log1p(cryo)
        + 0.04 * penetration
    )
    return EngineeringMetrics(
        structural=structural,
        blanket_space_proxy=blanket,
        heat_spreading_proxy=heat,
        cryogenic_burden_proxy=cryo,
        engineering_burden_score=float(burden),
    )
