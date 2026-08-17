# SFR-1 External Solver Execution Pack

## Purpose

v0.3.0 prepares the **promotion contract** for the high-authority calculations that could not be executed in the build runtime. It does not substitute local reduced models for DESC, VMEC++, transport, edge/RF or OpenMC results.

## Execution order

### G1 — finite-beta equilibrium

Run each frozen core candidate through DESC using archived pressure/current/profile assumptions and convergence tolerances. A candidate may be rejected on non-convergence or unacceptable force-balance/geometry behavior. Finalists must be independently cross-checked in VMEC++ and the input/output hashes retained.

Required evidence bundle: solver/version/build provenance; input geometry and profiles; converged status; force-balance/residual metrics; rotational-transform and magnetic-well/stability-relevant outputs; LCFS Fourier representation; machine-readable result summary.

### G2 — field realization and magnet engineering

Use the **solved G1 boundary**, not the current reduced surface, for plasma/coil co-optimization. Record field-normal error on held-out surface points, coil-plasma/coil-coil clearance, curvature, conductor field, current, REBCO strain, Lorentz loading, support stress/displacement and a manufacturing-error ensemble. A filament field fit alone cannot pass G2.

### G3/G4 — confinement and profiles

Run energetic-particle/direct-J and neoclassical calculations before nonlinear gyrokinetics. Couple heat and particle fluxes back into density/temperature profiles and plant auxiliary-power requirements. Record uncertainty/sensitivity rather than a single favorable point.

### G5 — exhaust

Resolve 3-D magnetic edge topology, target heat-flux distribution, pumping, radiation/detachment strategy and vessel/maintenance clearances. A core with no credible exhaust path is rejected even if its core confinement is strong.

### G6 — RF

Run 3-D ECRH propagation/absorption/deposition on the surviving equilibrium. Record launch geometry, accessible resonance surfaces, absorbed fraction, deposition profile, steering authority, port/wall loading and wall-plug efficiency.

### G7 — neutronics/TBR

Construct the selected reactor geometry as CAD/DAGMC or equivalent Monte Carlo geometry and execute OpenMC or an independently benchmarked equivalent. Include ports, gaps and penetrations. Required tallies include TBR with uncertainty, coil nuclear heating/dose, blanket/shield heating, relevant fluence/DPA and streaming weak zones.

### G8 — plant closure

Replace every target-ledger input with solver-derived or traceable engineering values. Recompute fusion power, blanket multiplication, heat removal, gross electrical conversion, itemized recirculating loads, tritium inventory/breeding, availability/maintenance and uncertainty propagation. Net electric power is a **prediction** until hardware exists.

### G9 — hardware

No simulation can close G9. Physical magnets, integrated subsystems, plasma experiments and ultimately an operating device are required.

## Prepared machine-readable contracts

The repository contains:

- `configs/closure/high_fidelity_solver_contract.json` — promotion requirements;
- `external_solvers/result_contract.schema.json` — common evidence envelope;
- `external_solvers/g1_candidate_matrix.json` — candidate/core matrix and expected outputs;
- `external_solvers/README.md` — execution/provenance rules.

No file in `external_solvers/` is evidence that an external solver actually ran.
