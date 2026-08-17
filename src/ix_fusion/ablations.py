from __future__ import annotations

from dataclasses import replace

from .analysis import evaluate_candidate
from .models import CandidateConfig, Harmonic


def _rescale_with_added(config: CandidateConfig, added: Harmonic) -> CandidateConfig:
    target = config.required_helical_strength
    remaining = max(target - abs(added.amplitude), 0.0)
    base_strength = sum(abs(h.amplitude) for h in config.harmonics)
    scale = remaining / max(base_strength, 1e-12)
    harmonics = tuple(replace(h, amplitude=h.amplitude * scale) for h in config.harmonics) + (added,)
    return replace(config, harmonics=harmonics, role="ablation")


def build_ablations(config: CandidateConfig) -> dict[str, CandidateConfig]:
    return {
        "no_axis_helical_shaping": replace(config, role="ablation", axis_helical_amplitude=0.0),
        "no_mirror_term": replace(config, role="ablation", mirror_amplitude=0.0),
        "collapsed_harmonic_phase": replace(
            config,
            role="ablation",
            harmonics=tuple(replace(h, phase=0.0) for h in config.harmonics),
        ),
        "small_c3_correction": _rescale_with_added(
            config,
            Harmonic(m=6, n=3, amplitude=0.0015, phase=0.0),
        ),
        "small_c9_correction": _rescale_with_added(
            config,
            Harmonic(m=16, n=9, amplitude=0.0015, phase=0.0),
        ),
    }


def evaluate_ablations(config: CandidateConfig) -> dict[str, dict]:
    nominal = evaluate_candidate(config)
    output: dict[str, dict] = {}
    for name, variant in build_ablations(config).items():
        metrics = evaluate_candidate(variant)
        output[name] = {
            "quick_objective": metrics.quick_objective,
            "objective_ratio_to_nominal": metrics.quick_objective / max(nominal.quick_objective, 1e-12),
            "action_variation_mean": metrics.omnigenity.action_variation_mean,
            "radial_excursion_mean": metrics.trace.mean_radial_excursion,
            "engineering_burden_score": metrics.engineering.engineering_burden_score,
        }
    return output
