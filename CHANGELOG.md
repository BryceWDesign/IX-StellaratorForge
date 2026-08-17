# Changelog

## 0.4.0 — 2026-08-16 — SFR-1 Maximum Computational Closure

- Added exact SFR-1 reduced-boundary to VMEC Fourier conversion and generated finite-pressure 2FP/3FP/4FP/6FP solver inputs.
- Added real DESC and VMEC++ execution adapters that fail closed when the production solver is unavailable.
- Added a 40-case TF+classical-helical Biot-Savart/field-line architecture scan; no candidate simultaneously passes transform and nestedness screens.
- Added an independent continuous winding-surface Fourier current-potential reconstruction with held-out validation; all 2/3/4/6FP cases remain above the 0.5% RMS screen.
- Added geometry-only REBCO bend/strain screening without mislabeling it winding-pack or FEA qualification.
- Added exact TBR blanket-coverage bounds plus an executable OpenMC axisymmetric CSG proxy builder and 3-D statepoint TBR analyzer.
- Added conditional net-electric threshold calculations tied to the actual ~704.57 MW in-repo burn screen.
- Increased the full test suite to 73 passing tests before release packaging and strengthened the scientific claim boundary.

## 0.3.0 — 2026-08-16 — SFR-1 Engineering PoC

- Added an executable SFR-1 PoC with a strict claim boundary between screening calculations, design targets, solver results and hardware evidence.
- Replaced finite-difference reduced-surface normals in the Biot-Savart diagnostic with analytic derivatives.
- Added a richer 120-filament fixed coil basis with ridge current solution and an unseen angularly offset validation surface; all 2FP/3FP/4FP/6FP variants still fail the 0.5% RMS screening threshold, so no magnet is promoted.
- Added a complete 87-row SFR-1 system-category BOM/design inventory and CSV companion. It is explicitly not a fabrication/procurement BOM.
- Added an external-solver execution pack and result contracts for G1-G8 without fabricating missing DESC/VMEC++/SIMSOPT/OpenMC evidence.
- Updated the custom evaluation-only license to version 1.1 and added the owner licensing/permission contact route: https://www.linkedin.com/in/brycewdesign/ .
- Updated README, NOTICE, licensing guide, citation metadata, software BOM, readiness reporting and quality gates for the v0.3 evidence state.

## 0.2.0 — 2026-08-16 — Closure Campaign

- Added Bosch-Hale D-T burn scoping and fixed-pressure temperature sensitivity.
- Quantified the Rev A uniform-plasma screening point (~704.57 MW) and the uniform-model beta threshold (~3.574%) for the 1 GW target.
- Added ISS04 confinement requirement screens for Q=10 and ignition-limit operation while keeping neoclassical/gyrokinetic validation explicitly open.
- Added an intermediate Biot-Savart coil reconstruction diagnostic for 2/3/4/6 field periods; encircling-only coils fail the promotion criterion and shaping/single-stage optimization is now mandatory.
- Added neutron source / breeding-rate requirements and contrasted target versus uniform-burn plant power balances.
- Added G5 and G9 explicit non-closure states, a machine-readable high-fidelity solver contract, closure documentation and tests.
- Preserved every high-fidelity gate as OPEN where DESC/VMEC++/SIMSOPT/OpenMC-class execution was unavailable; no solver evidence was fabricated.


## 0.1.0 — 2026-08-16

- Created the independent `IX-StellaratorForge` reactor-design program while preserving the IX-Fusion lineage.
- Retained the IX-Fusion v0.2.0-vNext scientific kernel, reduced-model evidence, seed league, and promotion gates as inherited evidence only.
- Added SFR-1 Rev A: a parameterized D-T stellarator reference-reactor envelope with 3FP/4FP/6FP QI/QI-pwO core competitors, a 2FP QA engineering reference, and a direct-J assumption-breaker search branch.
- Added reactor power-balance, D-T burn, cyclotron-frequency, plasma-envelope, radial-build, tritium, magnet, divertor, maintenance, control, and safety contracts.
- Added explicit parameter-authority classifications so targets cannot be mistaken for solver results.
- Added a reactor readiness report and a top-level quality gate.
