from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ix_fusion.solver_contracts import SolverRunManifest, validate_solver_run


class SolverContractTests(unittest.TestCase):
    def test_converged_equilibrium_contract_can_pass(self) -> None:
        manifest = SolverRunManifest(
            solver="example-equilibrium-solver",
            solver_version="1.0",
            authority="equilibrium",
            converged=True,
            input_hashes={"input": "a" * 64},
            output_hashes={"output": "b" * 64},
            metrics={"force_balance_or_convergence": 1e-8, "rotational_transform_profile": [0.5, 0.55]},
        )
        self.assertEqual(validate_solver_run(manifest), [])

    def test_nonconverged_run_cannot_promote_authority(self) -> None:
        manifest = SolverRunManifest(
            solver="example-equilibrium-solver",
            solver_version="1.0",
            authority="equilibrium",
            converged=False,
            input_hashes={"input": "a" * 64},
            output_hashes={"output": "b" * 64},
            metrics={"force_balance_or_convergence": 1.0, "rotational_transform_profile": []},
        )
        self.assertTrue(validate_solver_run(manifest))


if __name__ == "__main__":
    unittest.main()
