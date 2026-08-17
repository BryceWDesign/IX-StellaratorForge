from __future__ import annotations
import json
from math import pi
from pathlib import Path

import numpy as np

from ix_stellaratorforge.equilibrium_inputs import (
    analytic_boundary, make_seed, pressure_axis_for_quadratic_s_profile,
    reconstruct_boundary, render_vmec_input,
)
from ix_stellaratorforge.hts_screen import screen_curve_geometry
from ix_stellaratorforge.neutronics_constraints import breeding_coverage_constraint
from ix_stellaratorforge.plant_closure import plant_thresholds
from ix_stellaratorforge.vacuum_codesign import evaluate_helical_architecture
from ix_stellaratorforge.coil_screen import _poloidal_loop

ROOT=Path(__file__).resolve().parents[2]


def test_equilibrium_seed_fourier_boundary_is_exact():
    rng=np.random.default_rng(17)
    for nfp in (2,3,4,6):
        seed=make_seed(candidate_id=f"n{nfp}",nfp=nfp,R=8.0,a=1.7,field_T=6.0,beta=0.03)
        th=rng.uniform(0,2*pi,80); ph=rng.uniform(0,2*pi,80)
        r0,z0=analytic_boundary(seed,th,ph); r1,z1=reconstruct_boundary(seed,th,ph)
        assert np.max(np.abs(r0-r1)) < 1e-12
        assert np.max(np.abs(z0-z1)) < 1e-12
        text=render_vmec_input(seed)
        assert f"NFP = {nfp}" in text and "PRES_SCALE" in text and "PHIEDGE" in text


def test_equilibrium_pressure_seed_is_beta_derived_not_magic_number():
    p0=pressure_axis_for_quadratic_s_profile(0.03,6.0)
    assert 1.28e6 < p0 < 1.30e6


def test_new_helical_architecture_is_executed_and_not_false_promoted():
    r=evaluate_helical_architecture(nfp=4,R=8.0,a=1.7,clearance_m=1.35,target_B_T=6.0,sign_pattern="alternating",helical_to_tf_current_ratio=0.4,turns=2,steps_per_turn=32)
    assert np.isfinite(r.mean_iota)
    assert np.isfinite(r.max_radial_excursion_m)
    assert not r.combined_screen_pass


def test_hts_geometry_proxy_is_explicitly_only_geometry():
    curve=_poloidal_loop(0.0,8.0,3.05,nseg=240)
    s=screen_curve_geometry(curve)
    assert s.length_m > 19
    assert s.passes_geometry_strain_proxy
    assert "not_winding_pack_FEA" in s.authority


def test_neutronics_coverage_bound_is_exact():
    x=breeding_coverage_constraint(fusion_power_MW=1000,global_tbr_target=1.15,coverage_fraction=0.90)
    assert abs(x.required_local_tbr_if_uncovered_regions_breed_zero - 1.15/0.9) < 1e-12
    assert x.required_bred_tritium_kg_per_day > x.tritium_burn_kg_per_day


def test_net_electric_thresholds_reproduce_known_gap():
    p=plant_thresholds(current_fusion_power_MW=704.5706395923565,target_fusion_power_MW=1000,current_beta=0.03,blanket_multiplier=1.15,gross_efficiency=0.40,recirc_MW=120,net_floor_MW=300)
    assert abs(p.current_net_electric_MW-204.10249421248403) < 1e-9
    assert abs(p.fusion_power_required_for_net_floor_MW-913.0434782608696) < 1e-9
    assert abs(p.target_net_electric_MW-340.0) < 1e-12


def test_persisted_v040_evidence_never_claims_production_solver_closure():
    p=ROOT/'results/computational_closure/sfr1_v040.json'
    assert p.exists()
    d=json.loads(p.read_text())
    assert d['top_level_verdict']=='MAXIMUM_IN_REPO_COMPUTATIONAL_CLOSURE_COMPLETE__PRODUCTION_SOLVER_AND_HARDWARE_GATES_REMAIN'
    assert 'OPEN' in d['G1_equilibrium']['status']
    assert d['G9_hardware']['status']=='NOT_COMPUTATIONALLY_RESOLVABLE'
    assert d['G2_magnets']['classical_helical_any_pass'] is False
    assert d['G2_magnets']['current_potential_any_pass'] is False


def test_external_solver_seed_pack_present_for_all_fixed_nfp_candidates():
    expected={'input.SFR1_QA_2FP_REF','input.SFR1_QI_3FP','input.SFR1_QI_PWO_4FP','input.SFR1_C6_QI_6FP'}
    got={p.name for p in (ROOT/'external_solvers/inputs').glob('input.SFR1_*')}
    assert expected <= got
