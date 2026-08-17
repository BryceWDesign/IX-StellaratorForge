from __future__ import annotations

from .engineering import engineering_metrics
from .models import CandidateConfig, CandidateMetrics
from .omnigenity import omnigenity_metrics
from .optimizer import quick_objective
from .tracing import trace_field_lines, trace_metrics


def evaluate_candidate(config: CandidateConfig) -> CandidateMetrics:
    trace = trace_field_lines(config)
    return CandidateMetrics(
        trace=trace_metrics(trace),
        omnigenity=omnigenity_metrics(config),
        engineering=engineering_metrics(config),
        quick_objective=quick_objective(config),
    )
