from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .models import CandidateConfig, CandidateMetrics, RobustnessMetrics
from .tracing import poincare_points, trace_field_lines


def plot_poincare(config: CandidateConfig, path: Path) -> None:
    trace = trace_field_lines(config)
    r, theta = poincare_points(trace)
    fig, ax = plt.subplots(figsize=(7.2, 5.2))
    for idx in range(r.shape[1]):
        ax.scatter(theta[:, idx], r[:, idx], s=8, label=f"line {idx + 1}")
    ax.set_xlabel("poloidal angle mod 2π")
    ax.set_ylabel("normalized radius")
    ax.set_title(f"Reduced field-line Poincaré screen — {config.name}")
    ax.set_xlim(0, 2 * np.pi)
    ax.legend(loc="best", fontsize=8)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160)
    plt.close(fig)


def plot_metric_comparison(
    candidate: CandidateMetrics,
    baseline: CandidateMetrics,
    path: Path,
) -> None:
    labels = ["action variation", "field CV", "radial excursion", "engineering burden"]
    c = np.array(
        [
            candidate.omnigenity.action_variation_mean,
            candidate.omnigenity.field_strength_cv,
            candidate.trace.mean_radial_excursion,
            candidate.engineering.engineering_burden_score,
        ]
    )
    b = np.array(
        [
            baseline.omnigenity.action_variation_mean,
            baseline.omnigenity.field_strength_cv,
            baseline.trace.mean_radial_excursion,
            baseline.engineering.engineering_burden_score,
        ]
    )
    scale = np.maximum(np.maximum(c, b), 1e-12)
    x = np.arange(len(labels))
    width = 0.35
    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    ax.bar(x - width / 2, c / scale, width, label="C6 seed")
    ax.bar(x + width / 2, b / scale, width, label="matched baseline")
    ax.set_xticks(x, labels, rotation=20, ha="right")
    ax.set_ylabel("normalized to larger value in each metric")
    ax.set_title("IX-Fusion reduced-order comparison (lower is better)")
    ax.legend()
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160)
    plt.close(fig)


def plot_rf_robustness(robustness: RobustnessMetrics, path: Path) -> None:
    labels = ["median purity", "5th percentile purity"]
    open_values = [robustness.open_loop_purity_median, robustness.open_loop_purity_p05]
    fb_values = [robustness.feedback_purity_median, robustness.feedback_purity_p05]
    x = np.arange(2)
    width = 0.35
    fig, ax = plt.subplots(figsize=(7.0, 4.8))
    ax.bar(x - width / 2, open_values, width, label="open loop")
    ax.bar(x + width / 2, fb_values, width, label="abstract feedback")
    ax.set_xticks(x, labels)
    ax.set_ylim(0.8, 1.001)
    ax.set_ylabel("target spatial-mode purity")
    ax.set_title("Distributed phased-actuator robustness screen")
    ax.legend()
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160)
    plt.close(fig)
