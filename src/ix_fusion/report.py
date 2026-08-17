from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from .models import CandidateConfig, CandidateMetrics, PocVerdict, RobustnessMetrics


def _pct(value: float) -> str:
    return f"{100.0 * value:.4f}%"


def render_poc_markdown(
    candidate: CandidateConfig,
    baseline: CandidateConfig,
    candidate_metrics: CandidateMetrics,
    baseline_metrics: CandidateMetrics,
    verdict: PocVerdict,
    robustness: RobustnessMetrics,
) -> str:
    lines = [
        "# IX-Fusion Proof of Concept Result",
        "",
        "> **Authority boundary:** reduced-order computational screening only. This document is not",
        "> an MHD equilibrium result, a reactor design, or evidence of net-positive fusion energy.",
        "",
        f"**Candidate:** `{candidate.name}`  ",
        f"**Matched baseline:** `{baseline.name}`  ",
        f"**Reduced-model verdict:** **{verdict.reduced_model_verdict}**  ",
        f"**Scientific stage:** `{verdict.scientific_stage}`",
        "",
        "## Predeclared gates",
        "",
        "| Gate | Status | Candidate/value | Threshold/reference |",
        "|---|---:|---:|---:|",
    ]
    for gate in verdict.gates:
        value = f"{gate.value:.8g}" if isinstance(gate.value, float) else str(gate.value)
        threshold = f"{gate.threshold:.8g}" if isinstance(gate.threshold, float) else str(gate.threshold)
        lines.append(f"| {gate.name} | **{gate.status}** | {value} | {threshold} |")
    lines.extend(
        [
            "",
            "## Reduced-order metrics",
            "",
            "| Metric | C6 seed | Matched baseline |",
            "|---|---:|---:|",
            f"| Composite screening objective (lower better) | {candidate_metrics.quick_objective:.8f} | {baseline_metrics.quick_objective:.8f} |",
            f"| Bounce-action variation proxy | {_pct(candidate_metrics.omnigenity.action_variation_mean)} | {_pct(baseline_metrics.omnigenity.action_variation_mean)} |",
            f"| Field-strength coefficient of variation | {_pct(candidate_metrics.omnigenity.field_strength_cv)} | {_pct(baseline_metrics.omnigenity.field_strength_cv)} |",
            f"| Mean radial excursion proxy | {candidate_metrics.trace.mean_radial_excursion:.8f} | {baseline_metrics.trace.mean_radial_excursion:.8f} |",
            f"| Field-line escape fraction | {_pct(candidate_metrics.trace.escape_fraction)} | {_pct(baseline_metrics.trace.escape_fraction)} |",
            f"| Engineering burden proxy | {candidate_metrics.engineering.engineering_burden_score:.8f} | {baseline_metrics.engineering.engineering_burden_score:.8f} |",
            "",
            "## Active-control robustness screen",
            "",
            f"Six-source target-mode purity, median open loop: **{_pct(robustness.open_loop_purity_median)}**  ",
            f"Six-source target-mode purity, median with abstract feedback: **{_pct(robustness.feedback_purity_median)}**  ",
            f"Median unwanted-mode power reduction factor: **{robustness.unwanted_power_reduction_factor:.3f}x**",
            "",
            "This signal-processing result does not demonstrate plasma heating, current drive, mode suppression,",
            "or full-wave coupling. It only verifies that a distributed phased-actuator abstraction can be tested",
            "under deterministic geometry/phase/amplitude error and feedback assumptions.",
            "",
            "## Verdict",
            "",
            verdict.statement,
            "",
            "## Required next authority gates",
            "",
            "1. Solved 3-D equilibrium from DESC/VMEC-class tooling.",
            "2. Coil realization and normal-field error from SIMSOPT-class tooling.",
            "3. Guiding-center / fast-particle confinement against matched controls.",
            "4. Finite-pressure MHD stability.",
            "5. Turbulent transport and edge/divertor analysis.",
            "6. RF full-wave / deposition modeling.",
            "7. Blanket, neutronics, cryogenic and recirculating-power accounting.",
            "",
            "Until those gates are passed, IX-Fusion remains a **geometry hypothesis and evaluation framework**.",
            "",
        ]
    )
    return "\n".join(lines)


def write_markdown(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def metrics_dict(metrics: CandidateMetrics) -> dict:
    return asdict(metrics)
