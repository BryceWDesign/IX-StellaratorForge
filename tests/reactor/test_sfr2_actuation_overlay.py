from __future__ import annotations

import json
import math
from pathlib import Path

from ix_stellaratorforge.sfr2_actuation import (
    area_preserving_trilobe_geometry,
    run_actuation_overlay_screen,
    validate_actuation_config,
    weighted_volume_ratio,
)

ROOT = Path(__file__).resolve().parents[2]


def _config() -> dict:
    return json.loads(
        (ROOT / "configs/reactor/sfr2_actuation_overlay_a.json").read_text(encoding="utf-8")
    )


def test_overlay_preserves_rigid_vessel_steady_hts_and_open_high_authority_gates() -> None:
    raw = _config()
    assert validate_actuation_config(raw) == ()
    assert raw["mechanical_architecture"]["flexible_vacuum_vessel"] is False
    assert raw["mechanical_architecture"]["pulses_primary_hts_coils"] is False
    assert raw["promotion_status"]["SFR2A_G0_OVERLAY_SPEC"] == "PASS_SPEC_ONLY"
    assert all(
        status == "NOT_RUN"
        for gate, status in raw["promotion_status"].items()
        if gate != "SFR2A_G0_OVERLAY_SPEC"
    )


def test_traveling_quadrature_has_no_first_order_global_compression() -> None:
    values = [
        weighted_volume_ratio(
            sector_lengths_ft=[23.0, 26.0, 23.0, 26.0],
            depth_fraction=0.05,
            phase_offsets_deg=[0.0, 90.0, 180.0, 270.0],
            cycle_phase_rad=2.0 * math.pi * index / 720,
        )
        for index in range(720)
    ]
    assert min(values) > 1.0011
    assert max(values) < 1.0014
    assert max(values) - min(values) < 0.0002


def test_area_normalized_m3_trilobe_gets_zero_thermodynamic_credit() -> None:
    shape = area_preserving_trilobe_geometry(0.10)
    assert math.isclose(shape["normalized_area_ratio"], 1.0, rel_tol=0, abs_tol=1e-15)
    assert shape["minimum_radius_over_a"] < 0.90
    assert shape["maximum_radius_over_a"] > 1.09
    assert shape["thermodynamic_ignition_credit"] == 0.0


def test_breathing_screen_rejects_joint_cycle_average_improvement() -> None:
    result = run_actuation_overlay_screen(_config())
    assert result["baseline_design_id"] == "SFR-2-RevA"
    assert math.isclose(
        result["baseline"]["optimistic_ignition_tau_ratio"],
        0.9610772489928403,
        rel_tol=1e-12,
    )
    breathing = result["breathing_result"]
    assert breathing["verdict"] == (
        "NO_DECLARED_BREATHING_CASE_IMPROVES_BOTH_CYCLE_AVERAGE_PROXY_AND_FUSION_POWER"
    )
    assert breathing["any_joint_cycle_average_improvement"] is False
    assert breathing["any_cycle_average_proxy_pass"] is False
    closest = breathing["closest_cycle_average_case"]
    assert closest["pattern"] == "traveling_quadrature"
    assert closest["depth_fraction"] == 0.05
    assert 0.9615 < closest["cycle_average"]["optimistic_ignition_tau_ratio"] < 0.9616
    assert closest["cycle_average"]["fusion_power_MW_uniform"] < 1000.0


def test_image_translation_does_not_claim_three_body_or_global_three_lobe_gain() -> None:
    image = run_actuation_overlay_screen(_config())["concept_image_result"]
    assert image["global_three_toroidal_lobes_compatible_with_4fp_baseline"] is False
    assert image["repeated_poloidal_m3_bookkeeping_compatible_with_4fp"] is True
    assert image["three_point_collision_is_dt_fusion_mechanism"] is False
    assert image["zero_D_closer_to_ignition_credit"] == 0.0


def test_persisted_overlay_result_matches_recomputation() -> None:
    expected = json.loads(
        (ROOT / "results/sfr2_actuation/sfr2_actuation_overlay_a_v060.json").read_text(
            encoding="utf-8"
        )
    )
    assert run_actuation_overlay_screen(_config()) == expected
