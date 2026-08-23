# Changelog

## 0.10.0 — 2026-08-22 — Reality Gradient and Adaptive Inverse Design

- Added SFR-5 Reality Gradient as a fail-closed architecture-search layer above the preserved SFR-4 evidence.
- Derived the magnetic autopsy directly from committed v0.9 result/config artifacts: 80 candidates, zero combined topology passes, 3.8265x transform gap to the minimum gate, 3.887% normalized excursion slack, and a held-out normal-field error 12.9825x above its limit.
- Added explicit independent evidence lanes so the direct-filament topology result and held-out reconstruction result cannot be merged into a fictitious physical coilset.
- Added normalized augmented-Lagrangian-style constraint pressure while deliberately withholding any backward geometry gradient until a real movable-geometry evaluator supplies sensitivities.
- Added rejected-family memory, architecture-stagnation logic, movable plasma/winding-surface/coil degrees of freedom, and a production-solver promotion contract.
- Added SFR-5 config/schema, deterministic runner, persisted result, provenance, documentation, external evidence contract, release checks and tests.
- Preserved zero earned fusion-progress credit and all high-authority equilibrium, confinement, TBR, net-electric, magnet, safety and hardware gates as open.

## 0.9.0 — 2026-08-22 — Integrated Physical Promotion and Heat Exhaust

- Attempted all seven requested workstreams in one fail-closed campaign: physical coils, finite-beta equilibrium, coil/plasma co-design, particle confinement, burn, magnet engineering and reactor systems.
- Expanded the physical filament scan to 80 direct Biot-Savart cases. Zero cases pass both transform and radial-excursion gates, so the scanned classical helical family is rejected.
- Explicitly attempted DESC, VMEC++ and OpenMC adapters. Each stopped because its production dependency is unavailable; the package installation route was also blocked by runtime network policy.
- Added a 3.5 MeV alpha gyroradius scope without assigning guiding-center retention credit.
- Added a Q=20 burn requirement with finite alpha deposition and explicit bremsstrahlung; the design-iota requirement is about H_ISS04 2.00 and is not linked to the failed coil family.
- Split heat into first-wall radiation, island-divertor exhaust and blanket neutron heating.
- Selected a separated helium first-wall, PbLi blanket and independent water-cooled W/Cu/CuCrZr divertor architecture.
- Passed the nominal and declared steady reduced heat envelope at about 0.294 MW/m2 first-wall peak and 5.724 MW/m2 divertor peak, while retaining edge topology, transients, CHF, fatigue, irradiation and hardware as open gates.
- Added a 64-row integrated campaign BOM, evidence contract, schema, provenance, decision records and eleven focused regression tests.

## 0.8.0 — 2026-08-22 — Dual Boundary Integrity Network

- Translated the proposed inside-out and outside AHIS concept into two independently monitored engineering boundaries without assigning mechanical plasma-confinement credit.
- Added three comparable wall-stack branches and selected a balanced tungsten / graded W-RAFM / helium-cooled RAFM / DCLL reference under explicit reduced-screen weights.
- Added a 1-D nominal and steady-upset thermal-resistance screen with interface temperature and raw CTE-mismatch strain bookkeeping.
- Added 24 toroidal monitoring sectors, 192 paired inner/outer locations, two independent lanes and 1,736 declared sensing elements.
- Added eleven deterministic fault scenarios covering hotspot, coolant leak, support shift, single-lane losses, dual-bus loss, vacuum breach, power loss, trim unavailability and an intentionally undetected silent armor crack.
- Linked measured support displacement to existing bounded SFR-3 trim logic while retaining exactly zero physical confinement, fusion, ignition and safety-qualification credit.
- Added a 64-row integration BOM, materials decision record, fault campaign, promotion gates, technical provenance, high-authority evidence contract, eight model tests and one BOM contract test.

## 0.7.0 — 2026-08-21 — Field Integrity Shell

- Audited AHIS, PressureX, IX-Vibe, IX-Breath, IX-GCR-SPE, IX-Shield and IX-HfTaZen-Shield as mechanism donors with explicit KEEP / ADAPT / DEFER / REJECT boundaries.
- Added SFR-3 Field Integrity Shell A: steady primary confinement coils, 24 independent planar trim channels, 24 passive superconducting-loop research channels, confidence-aware sensing and fail-closed control.
- Added a deterministic 12-by-24 harmonic controllability screen with bounded commands, nominal, single-actuator-failure, low-confidence, passive-loop-quench and passive-only transient scenarios.
- Passed the declared synthetic thresholds while assigning exactly zero confinement, fusion-power, ignition or net-electric credit.
- Added a 52-row architecture BOM covering field sources, control, support-mode damping, magnet shielding, plasma-facing materials, blanket integration and rejected material/liquid concepts.
- Retained WC/B4C, HfH1.7 composites, tungsten-fiber composites, liquid-lithium edge modules and ferromagnetic blanket co-design only at their defensible authority levels.
- Added SFR3-G0 through SFR3-G9 promotion gates, a high-authority solver contract, source provenance, six regression tests and fail-closed v0.7 quality-gate checks.

## 0.6.0 — 2026-08-21 — Phase-Programmed Breathing and Tri-Lobe Falsification

- Preserved SFR-2 Rev A geometry, rigid vessel and steady primary HTS field unchanged.
- Added a 720-sample-per-cycle magnetic-breathing screen for synchronous, ABAB-opposed and traveling-quadrature patterns at 0% through 5% modulation depth.
- Used fixed-particle ideal adiabatic bookkeeping, Bosch-Hale D-T reactivity and instantaneous ISS04 comparison without inventing magnetic-pumping, RF, shock, flux-compression or actuator-power credit.
- Found no declared waveform that improves both cycle-average optimistic ignition ratio and cycle-average uniform fusion power. No cycle-average case crosses the proxy.
- Translated the user concept image into an area-preserving poloidal m=3 harmonic repeated within all four field periods. Rejected global three-toroidal-lobe substitution and three-body D-T credit.
- Added an explicit 24-row actuator-overlay architecture BOM built around eight normal-conducting triplet stations and 24 independent circuits; all electrical, magnetic, thermal and structural ratings remain solver or hardware dependent.
- Added separate promotion gates for dynamic equilibrium, electromagnetics, magnetic-pumping kinetics, particle and alpha orbits, transport/MHD, wall loads, integrated power and hardware.
- Added deterministic generated evidence, tests, provenance, CLI access and fail-closed v0.6 quality-gate checks.

## 0.5.0 — 2026-08-18 — SFR-2 Dynamic-Compression Assumption Breaker

- Preserved SFR-1 Rev A and all v0.4 evidence unchanged as the steady-state reference branch.
- Added SFR-2 Rev A, interpreting the user-specified 23/26/23/26 ft pattern as four consecutive sectors of one closed toroidal plasma system rather than four independent reactors connected by plasma ducts.
- Added deterministic geometry bookkeeping, Bosch-Hale D-T burn calculation, ideal radial-compression upper-bound thermodynamics, target-power matching, ISS04 rotational-transform sensitivity and explicit transient-confinement sensitivity.
- Assigned zero numerical credit to unmodeled traveling-wave/RF heating, magnetic pumping, ABAB staggering advantage, or magnetic-flux-compression field amplification.
- Added SFR2-G0 through SFR2-G9 promotion gates; only G0 specification is passed and every physics/engineering/hardware gate remains NOT_RUN.
- Added a reproducible negative result: with H_ISS04=1.0 and equal 1 GW target power, no declared SFR-2 point crosses the optimistic alpha-only ignition proxy; radial compression worsens the ISS04 proxy in the tested target-power-matched cases.
- Superseded earlier conversational percentage estimates with repository-generated equations/results rather than copying informal numbers into evidence.
- Added SFR-2 schema, technical-basis provenance, documentation, tests, CLI access, release-generation integration and v0.5 quality-gate checks.

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
