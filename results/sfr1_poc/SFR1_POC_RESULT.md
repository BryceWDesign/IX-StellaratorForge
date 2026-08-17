# SFR-1 Executable Proof of Concept — v0.4.0

**Verdict:** `PIPELINE_POC_PASS__REACTOR_PHYSICS_NOT_CLOSED`

This PoC demonstrates an executable, falsifiable reactor-design screening pipeline. It does **not** demonstrate a fusion reactor.

## Reproduced screening results

- Uniform D-T burn screen: **704.57 MW** vs **1000 MW** design target.
- Uniform-model beta required for the 1 GW target: **3.574%**.
- Design-target power ledger: **340.00 MWe** at the declared screening assumptions.
- Current uniform-burn screen power ledger: **204.10 MWe**.
- Electron-cyclotron fundamental at 6 T: **167.95 GHz**.

## Held-out filament-coil reconstruction

The richer fixed coil basis is solved on one surface grid and evaluated on an unseen, angularly offset grid.

| NFP | coils | validation RMS | validation mean | max | screen pass |
|---:|---:|---:|---:|---:|:---:|
| 2 | 120 | 0.01555 | 0.01321 | 0.04218 | FAIL |
| 3 | 120 | 0.02757 | 0.02419 | 0.05897 | FAIL |
| 4 | 120 | 0.03701 | 0.03218 | 0.07222 | FAIL |
| 6 | 120 | 0.06491 | 0.05487 | 0.14389 | FAIL |

The fixed-basis coil test remains a **negative result**. It does not justify promoting any core; single-stage plasma/coil optimization remains mandatory.

## High-authority gates still open

- finite-beta 3-D MHD equilibrium (DESC + VMEC++ cross-check)
- neoclassical / energetic-particle / nonlinear gyrokinetic confinement
- structural and REBCO-qualified magnet design
- 3-D edge/divertor solution
- full-wave/ray deposition validation for RF
- OpenMC/DAGMC blanket, shielding and TBR transport
- integrated experimental/hardware validation

See `docs/closure/07_PRODUCTION_SOLVER_HANDOFF.md` for the exact promotion evidence expected from those tools.
