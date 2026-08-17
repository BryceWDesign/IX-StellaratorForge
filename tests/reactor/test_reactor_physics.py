
from __future__ import annotations

import math
from pathlib import Path

from ix_stellaratorforge.physics import dt_reaction_ledger, ecrh_frequency_ghz, plasma_screening_ledger, power_balance
from ix_stellaratorforge.reactor import load_reactor_config, validate_reactor_config

ROOT = Path(__file__).resolve().parents[2]


def test_dt_energy_partition_and_burn_rate():
    ledger = dt_reaction_ledger(1000.0)
    assert math.isclose(ledger.neutron_power_MW + ledger.alpha_power_MW, 1000.0, rel_tol=0, abs_tol=1e-9)
    assert 0.153 < ledger.tritium_burn_kg_per_day < 0.154
    assert 0.102 < ledger.deuterium_burn_kg_per_day < 0.103


def test_first_harmonic_ecrh_near_168_ghz_at_6_t():
    assert 167.9 < ecrh_frequency_ghz(6.0) < 168.1


def test_reference_power_ledger_has_positive_net_margin():
    p = power_balance(1000.0, 1.15, 0.40, 120.0)
    assert p.thermal_power_MW_screening == 1150.0
    assert p.gross_electric_MW_screening == 460.0
    assert p.net_electric_MW_at_recirc_ceiling == 340.0


def test_plasma_screening_is_transparent_proxy():
    s = plasma_screening_ledger(8.0, 1.7, 6.0, 0.03, 1000.0, 15.0, 15.0)
    assert 4.70 < s.aspect_ratio < 4.71
    assert 456.0 < s.circular_torus_volume_m3 < 457.0
    assert 1.49 < s.neutron_wall_load_MW_m2_screening < 1.50
    assert 8.9e19 < s.equal_temperature_density_m3_screening < 9.0e19


def test_rev_a_invariants_pass_and_no_core_is_selected():
    c = load_reactor_config(ROOT / "configs" / "reactor" / "sfr1_rev_a.json")
    v = validate_reactor_config(c)
    assert v.passed, v.errors
    assert c.raw["core_policy"]["selected_core"] is None
    assert c.raw["core_policy"]["privileged_core"] is None


def test_high_authority_gates_remain_unrun():
    c = load_reactor_config(ROOT / "configs" / "reactor" / "sfr1_rev_a.json")
    status = c.raw["promotion_status"]
    assert all(status[g] == "NOT_RUN" for g in status if g != "G0_SEED")
