from __future__ import annotations
from math import isclose
from pathlib import Path

from ix_stellaratorforge.burn import (
    bosch_hale_dt_reactivity,
    fixed_pressure_optimum_temperature_keV,
    required_uniform_beta_for_target,
    uniform_dt_burn_point,
)
from ix_stellaratorforge.closure import run_closure_campaign
from ix_stellaratorforge.reactor import load_reactor_config

ROOT = Path(__file__).resolve().parents[2]


def test_bosch_hale_dt_reactivity_at_15kev_is_stable() -> None:
    assert isclose(bosch_hale_dt_reactivity(15.0), 2.7399296107880726e-22, rel_tol=1e-12)


def test_sfr1_uniform_burn_and_beta_threshold() -> None:
    point = uniform_dt_burn_point(
        temperature_keV=15.0,
        beta=0.03,
        field_T=6.0,
        volume_m3=456.37050750637184,
        target_fusion_power_MW=1000.0,
    )
    assert isclose(point.fusion_power_MW_uniform, 704.5706395923565, rel_tol=1e-10)
    assert isclose(required_uniform_beta_for_target(point), 0.03574036503978043, rel_tol=1e-10)


def test_fixed_pressure_temperature_scan_has_explicit_grid_result() -> None:
    t, p = fixed_pressure_optimum_temperature_keV(
        beta=0.03,
        field_T=6.0,
        volume_m3=456.37050750637184,
        target_fusion_power_MW=1000.0,
    )
    assert isclose(t, 13.5, abs_tol=1e-12)
    assert p > 710.0


def test_campaign_never_fabricates_high_fidelity_closure() -> None:
    cfg = load_reactor_config(ROOT / "configs" / "reactor" / "sfr1_rev_a.json")
    result = run_closure_campaign(cfg)
    assert result["G1_equilibrium"]["status"] == "OPEN_EXTERNAL_SOLVER_REQUIRED"
    assert "NOT_CLOSED" in result["top_level_verdict"]
    assert result["G2_coil_diagnostic"]["status"].startswith("FAILS_")
    assert result["G7_neutronics"]["status"].endswith("_OPEN")
    assert result["G9_hardware"]["status"] == "OPEN_REQUIRES_PHYSICAL_HARDWARE"
    assert result["G8_system"]["target_power_balance"]["net_electric_MW_at_recirc_ceiling"] == 340.0
    assert result["G8_system"]["uniform_burn_power_balance"]["net_electric_MW_at_recirc_ceiling"] < 300.0


def test_readiness_surfaces_closure_campaign_without_promoting_base_gates() -> None:
    from ix_stellaratorforge.readiness import build_readiness_report
    cfg = load_reactor_config(ROOT / "configs" / "reactor" / "sfr1_rev_a.json")
    report = build_readiness_report(cfg)
    assert report["current_verdict"].endswith("NOT_CLOSED")
    assert report["promotion_status"]["G1_EQUILIBRIUM"] == "NOT_RUN"
    assert report["closure_campaign_v0_2"]["G2"].startswith("FAILS_")
