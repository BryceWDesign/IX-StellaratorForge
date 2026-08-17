from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ix_fusion.claims import STAGES
from ix_fusion.plant import EnergyLedger


class PlantClaimTests(unittest.TestCase):
    def test_incomplete_energy_ledger_refuses_net_power(self) -> None:
        ledger = EnergyLedger(fusion_power=10.0)
        with self.assertRaises(ValueError):
            ledger.net_electric_power()

    def test_complete_ledger_computes_arithmetic_only(self) -> None:
        ledger = EnergyLedger(
            fusion_power=100.0,
            external_heating_power=10.0,
            magnet_power=2.0,
            cryogenic_power=3.0,
            pumping_power=1.0,
            rf_power=4.0,
            thermal_conversion_efficiency=0.4,
        )
        self.assertAlmostEqual(ledger.net_electric_power(), 20.0)

    def test_stage_order_is_conservative(self) -> None:
        self.assertEqual(STAGES[0], "geometry_hypothesis")
        self.assertEqual(STAGES[-1], "fusion_performance_candidate")


if __name__ == "__main__":
    unittest.main()
