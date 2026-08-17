from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class Harmonic:
    m: int
    n: int
    amplitude: float
    phase: float = 0.0

    def validate(self) -> None:
        if self.m <= 0:
            raise ValueError("harmonic m must be positive")
        if self.n < 0:
            raise ValueError("harmonic n must be non-negative")
        if abs(self.amplitude) > 0.2:
            raise ValueError("reduced-model harmonic amplitude exceeds bounded screen")


@dataclass(frozen=True)
class CandidateConfig:
    name: str
    role: str
    description: str
    nfp: int
    major_radius: float
    minor_radius: float
    axis_helical_amplitude: float
    iota0: float
    shear: float
    mirror_amplitude: float
    required_helical_strength: float
    harmonics: tuple[Harmonic, ...]
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.name:
            raise ValueError("name is required")
        if self.role not in {"candidate", "matched_baseline", "negative_control", "ablation"}:
            raise ValueError(f"unsupported role: {self.role}")
        if self.nfp < 1 or self.nfp > 12:
            raise ValueError("nfp must be in [1, 12] for this reduced model")
        if self.major_radius <= self.minor_radius or self.minor_radius <= 0:
            raise ValueError("major radius must exceed positive minor radius")
        if not 0.05 <= self.iota0 <= 1.5:
            raise ValueError("iota0 outside reduced-model bounds")
        if not -0.5 <= self.shear <= 0.5:
            raise ValueError("shear outside reduced-model bounds")
        if not 0 <= self.mirror_amplitude <= 0.3:
            raise ValueError("mirror amplitude outside reduced-model bounds")
        if not 0 <= self.required_helical_strength <= 0.1:
            raise ValueError("required_helical_strength outside reduced-model bounds")
        if not self.harmonics and self.role != "negative_control":
            raise ValueError("non-control configurations require harmonics")
        for harmonic in self.harmonics:
            harmonic.validate()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TraceMetrics:
    mean_radial_excursion: float
    p95_radial_excursion: float
    max_radial_excursion: float
    escape_fraction: float
    mean_surface_spread: float
    iota_estimate_mean: float
    iota_estimate_std: float


@dataclass(frozen=True)
class OmnigenityMetrics:
    action_variation_mean: float
    action_variation_p95: float
    field_strength_cv: float
    mirror_ratio: float


@dataclass(frozen=True)
class StructuralMetrics:
    axis_curvature_rms: float
    axis_curvature_max: float
    axis_torsion_rms: float
    normalized_support_burden: float


@dataclass(frozen=True)
class RFMetrics:
    target_mode_purity: float
    sideband_power: float
    amplitude_ripple: float


@dataclass(frozen=True)
class RobustnessMetrics:
    open_loop_purity_median: float
    feedback_purity_median: float
    open_loop_purity_p05: float
    feedback_purity_p05: float
    unwanted_power_reduction_factor: float


@dataclass(frozen=True)
class EngineeringMetrics:
    structural: StructuralMetrics
    blanket_space_proxy: float
    heat_spreading_proxy: float
    cryogenic_burden_proxy: float
    engineering_burden_score: float


@dataclass(frozen=True)
class CandidateMetrics:
    trace: TraceMetrics
    omnigenity: OmnigenityMetrics
    engineering: EngineeringMetrics
    quick_objective: float


@dataclass(frozen=True)
class GateResult:
    name: str
    status: str
    value: float | str | None
    threshold: float | str | None
    rationale: str


@dataclass(frozen=True)
class PocVerdict:
    reduced_model_verdict: str
    scientific_stage: str
    gates: tuple[GateResult, ...]
    statement: str
