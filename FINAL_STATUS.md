# IX-StellaratorForge v0.4.0 — Maximum Computational Closure status

## Current verdict

`MAXIMUM_IN_REPO_COMPUTATIONAL_CLOSURE_COMPLETE__PRODUCTION_SOLVER_AND_HARDWARE_GATES_REMAIN`

This release resolves every remaining item **to the highest authority actually executable inside the repository/build runtime** and packages the production-solver jump without inventing its output.

## What was newly executed

- exact VMEC-family boundary/input generation for the 2FP, 3FP, 4FP and 6FP SFR-1 seed league;
- 40-case classical helical TF+helix Biot-Savart / field-line architecture scan;
- independent continuous winding-surface current-potential reconstruction with held-out validation;
- geometry-level HTS centerline length/bend/strain screens;
- exact D-T source, tritium burn and blanket-coverage/TBR constraints;
- conditional net-electric thresholds tied to the actual in-repo burn screen;
- production adapters for DESC, VMEC++, OpenMC proxy construction and OpenMC 3-D TBR statepoint analysis.

## Key negative result

No tested low/intermediate-authority magnet architecture is promoted.

The best classical-helical scan keeps the radial-excursion screen but generates only ~0.0389 mean rotational transform, far below the 0.25 minimum screening target. The current-potential fits also fail the held-out 0.5% RMS `Bn/B0` threshold for every 2/3/4/6FP reduced boundary.

This changes the design instruction: **do not force a magnet onto the current reduced plasma boundary. Solve finite-beta equilibrium and coil geometry as a co-design problem.**

## Plant closure result

The uniform 6 T / 3% beta / 15 keV screen remains ~704.57 MW fusion and ~204.10 MWe under the current plant assumptions. The 300 MWe floor requires ~913.04 MW fusion, or ~3.415% beta under the deliberately simple fixed-temperature uniform scaling. The 1 GW target corresponds to ~3.574% beta in that same screen and yields 340 MWe conditional net power.

These are algebraic/screening thresholds, not a net-electric reactor prediction.

## Remaining authority jumps

- **G1:** execute and converge finite-beta DESC; independently cross-check finalists with VMEC++.
- **G2:** optimize coils with the solved equilibrium; qualify REBCO Ic/strain, EM loads/support FEA, manufacturing tolerance and quench.
- **G3/G4:** alpha/guiding-center, neoclassical/bootstrap, gyrokinetic and profile-transport closure.
- **G5:** 3-D edge/divertor/SOL heat-flux solution.
- **G6:** 3-D RF propagation/deposition and wall-plug accounting.
- **G7:** full 3-D OpenMC/DAGMC/ParaStell-class neutronics including ports/penetrations.
- **G8:** couple real G1–G7 outputs into thermal-hydraulic and plant balance.
- **G9:** physical hardware demonstration.

No production-solver or hardware result is fabricated in this release.
