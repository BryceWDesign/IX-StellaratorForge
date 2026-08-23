# SFR-3 Dual Boundary AHIS A, v0.8.0 result

## Verdict

`DUAL_BOUNDARY_ARCHITECTURE_SCREEN_PASS__PHYSICAL_SURVIVABILITY_AND_CONFINEMENT_UNPROVEN`

The requested inside/outside AHIS concept is retained as two monitored engineering boundaries. It does not mechanically push plasma inward and earns zero confinement, fusion, ignition or safety-qualification credit.

## Selected reduced-screen stack

`Segmented tungsten plus graded W-RAFM plus helium-cooled RAFM and DCLL blanket`

The 1-D nominal screen predicts a plasma-facing surface temperature of **420.7 C** at 0.25 MW/m2.
The deliberately steady upset upper bound predicts **632.9 C** at 1.0 MW/m2. This is not a disruption or lifetime result.
The raw CTE-mismatch strain proxy is **0.2121%**; real interface stress requires nonlinear FEA and irradiation data.

## Monitoring configuration

- 24 toroidal sectors aligned to the 24 SFR-3 trim channels.
- 192 paired inner/outer poloidal monitoring locations.
- Two independent sensing lanes.
- 1736 total declared sensing elements, including independent hard-vacuum channels.

## Fault findings

- A hotspot and coolant leak remain detectable after the declared single-channel failures.
- Loss of one inner or outer lane enters degraded monitoring, not a false nominal state.
- Loss of both sector buses, vacuum breach or total control power enters safe hold.
- Outer support movement can request the existing SFR-3 synthetic trim response of **65.46%**, but physical confinement credit remains zero.
- A silent armor crack below sensor sensitivity is deliberately not claimed as detected; periodic NDE remains mandatory.

## Decision

The dual-boundary arrangement helps safety observability, leak isolation, wall protection and magnetic alignment management. It does not change the repository's earned ignition proxy. Promote only after coupled thermal/CFD/FEA, fracture and irradiation lifetime, sensor qualification, 3-D magnetics, full neutronics and an instrumented sector prototype.
