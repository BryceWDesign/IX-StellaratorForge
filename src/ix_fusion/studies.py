from __future__ import annotations

from pathlib import Path

from .ablations import evaluate_ablations
from .analysis import evaluate_candidate
from .config import load_json
from .evidence import load_json as load_result_json, write_json
from .losses import loss_ledger
from .models import CandidateConfig, Harmonic
from .sensitivity import geometry_error_monte_carlo


def optimized_config_from_result(data: dict) -> CandidateConfig:
    item = data["optimized"]
    return CandidateConfig(
        name=item["name"],
        role=item["role"],
        description=item["description"],
        nfp=int(item["nfp"]),
        major_radius=float(item["major_radius"]),
        minor_radius=float(item["minor_radius"]),
        axis_helical_amplitude=float(item["axis_helical_amplitude"]),
        iota0=float(item["iota0"]),
        shear=float(item["shear"]),
        mirror_amplitude=float(item["mirror_amplitude"]),
        required_helical_strength=float(item["required_helical_strength"]),
        harmonics=tuple(Harmonic(**h) for h in item["harmonics"]),
        metadata=item.get("metadata", {}),
    )


def run_secondary_studies(repo_root: Path, results_root: Path | None = None) -> dict[str, dict]:
    repo_root = repo_root.resolve()
    results_root = (results_root or repo_root / "results").resolve()
    candidate_result = load_result_json(results_root / "poc/c6_candidate.json")
    baseline_result = load_result_json(results_root / "baselines/matched_helical_5fp.json")
    candidate = optimized_config_from_result(candidate_result)
    baseline = optimized_config_from_result(baseline_result)
    ablations = evaluate_ablations(candidate)
    sens_cfg = load_json(repo_root / "configs/system/geometry_error_monte_carlo.json")
    candidate_mc = geometry_error_monte_carlo(candidate, **sens_cfg)
    baseline_mc = geometry_error_monte_carlo(baseline, **sens_cfg)
    candidate_metrics = evaluate_candidate(candidate)
    losses = loss_ledger(candidate, candidate_metrics)
    write_json(results_root / "ablations/c6_ablations.json", ablations)
    write_json(
        results_root / "monte_carlo/geometry_error_robustness.json",
        {"candidate": candidate_mc, "baseline": baseline_mc},
    )
    write_json(results_root / "evidence/loss_ledger.json", losses)
    return {"ablations": ablations, "candidate_mc": candidate_mc, "baseline_mc": baseline_mc, "losses": losses}
