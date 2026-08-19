# SFR-2 promotion gates

SFR-2 is intentionally prevented from inheriting SFR-1 evidence by name alone. Every gate below requires candidate-specific evidence.

## SFR2-G0 — specification

**Current:** `PASS_SPEC_ONLY`

Required: machine-readable Rev A specification, explicit topology, equations, assumption ledger, deterministic screen, tests, result artifact, and claim boundary.

## SFR2-G1 — dynamic equilibrium

**Current:** `NOT_RUN`

Required: converged finite-beta 3-D equilibrium for the ABAB candidate plus time-resolved or quasi-static equilibria spanning the proposed actuation/compression cycle. A static circular-torus proxy cannot pass G1.

## SFR2-G2 — coils and field

**Current:** `NOT_RUN`

Required: coil/current solution that produces the required equilibrium and perturbation fields while respecting conductor field, strain, structural load, clearance, tolerance and protection constraints.

## SFR2-G3 — particle and alpha orbits

**Current:** `NOT_RUN`

Required: thermal and fusion-born alpha orbit confinement across the full dynamic cycle.

## SFR2-G4 — transport and MHD

**Current:** `NOT_RUN`

Required: neoclassical/bootstrap, gyrokinetic/profile transport, ideal/resistive MHD and explicit island/stochastic-region assessment under actuation.

## SFR2-G5 — edge and transient heat flux

**Current:** `NOT_RUN`

Required: 3-D edge/SOL/divertor solution including time-dependent wall loads caused by compression and actuation.

## SFR2-G6 — RF and phase control

**Current:** `NOT_RUN`

Required: wave propagation/deposition and control model establishing whether the traveling phase sequence transfers useful energy without unacceptable topology/stability damage. Rev A assigns **zero numerical gain** before this gate.

## SFR2-G7 — neutronics and TBR

**Current:** `NOT_RUN`

Required: full 3-D neutron/photon transport with actual ports, coils, blanket/shield layout and time-averaged operating scenario.

## SFR2-G8 — integrated burn and plant

**Current:** `NOT_RUN`

Required: coupled power balance using outputs from G1–G7. No net-energy or net-electric claim may be made from the low-authority SFR-2 screen.

## SFR2-G9 — hardware

**Current:** `NOT_RUN`

Required: calibrated experimental evidence from physical hardware. Computation cannot promote this gate.

## Authority rule

A low-authority model may reject a candidate. It may not declare one successful. Crossing the v0.5.0 empirical ignition proxy can only justify the next calculation; it cannot promote SFR2-G1 through G9.
