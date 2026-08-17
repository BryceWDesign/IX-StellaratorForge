from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from ix_stellaratorforge.poc import run_sfr1_poc
from ix_stellaratorforge.reactor import load_reactor_config


def test_sfr1_poc_keeps_target_and_screen_separate() -> None:
    data = run_sfr1_poc(load_reactor_config(ROOT / "configs/reactor/sfr1_rev_a.json"))
    assert data["verdict"] == "PIPELINE_POC_PASS__REACTOR_PHYSICS_NOT_CLOSED"
    assert data["architecture_validation"]["passed"] is True
    assert data["burn_screen"]["fusion_power_MW_uniform"] < data["burn_screen"]["target_fusion_power_MW"]
    assert data["boolean_checks"]["target_power_ledger_meets_floor"] is True
    assert data["boolean_checks"]["current_uniform_screen_meets_floor"] is False
    assert data["boolean_checks"]["any_fixed_hybrid_coil_basis_passes_0p5pct_rms_screen"] is False
