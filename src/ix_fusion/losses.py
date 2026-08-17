from __future__ import annotations

from .models import CandidateConfig, CandidateMetrics
from .optimizer import objective_terms


def loss_ledger(config: CandidateConfig, metrics: CandidateMetrics) -> dict[str, dict[str, object]]:
    terms = objective_terms(config)
    return {
        "bounce_averaged_radial_drift_surrogate": {
            "status": "SCREENED",
            "metric": metrics.omnigenity.action_variation_mean,
            "authority": "bounce-action variation proxy only",
        },
        "field_line_integrability": {
            "status": "SCREENED",
            "metric": metrics.trace.mean_radial_excursion,
            "authority": "reduced Hamiltonian field-line screen only",
        },
        "fast_particle_loss": {
            "status": "UNKNOWN",
            "metric": None,
            "authority": "requires guiding-center/particle code on solved field",
        },
        "mhd_stability": {
            "status": "UNKNOWN",
            "metric": None,
            "authority": "requires finite-pressure equilibrium and stability analysis",
        },
        "turbulent_transport": {
            "status": "UNKNOWN",
            "metric": None,
            "authority": "requires gyrokinetic or validated transport tooling",
        },
        "rf_plasma_coupling": {
            "status": "UNKNOWN",
            "metric": None,
            "authority": "requires full-wave/deposition modeling",
        },
        "divertor_heat_load": {
            "status": "UNKNOWN",
            "metric": None,
            "authority": "current heat metric is geometry-only screening proxy",
        },
        "neutron_blanket_performance": {
            "status": "UNKNOWN",
            "metric": None,
            "authority": "requires neutronics and breeding analysis",
        },
        "net_electric_power": {
            "status": "UNKNOWN",
            "metric": None,
            "authority": "requires complete reactor energy ledger",
        },
        "screening_objective_terms": {
            "status": "SCREENED",
            "metric": terms,
            "authority": "dimensionless reduced-order objective components",
        },
    }
