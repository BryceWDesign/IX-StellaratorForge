from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from ix_stellaratorforge.coil_hybrid import helical_hybrid_coil_screen


def test_hybrid_coil_screen_is_held_out_and_does_not_overclaim() -> None:
    result = helical_hybrid_coil_screen(
        nfp=4,
        R=8.0,
        a=1.7,
        clearance_m=1.35,
        target_B_T=6.0,
    )
    assert result.coil_count > 24
    assert abs(result.mean_axis_field_T - 6.0) < 0.02
    assert result.validation_rms_Bn_over_B > 0
    # Current reduced target + fixed basis is expected to fail the stringent 0.5% screen.
    # If this ever flips, the result still needs independent high-fidelity confirmation.
    assert result.passes_reconstruction_screen is False
