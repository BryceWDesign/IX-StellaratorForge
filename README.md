# IX-StellaratorForge

**Evidence-driven stellarator fusion reactor design and computational co-design program.**

IX-StellaratorForge preserves the original `IX-Fusion` research lineage and builds a reactor-level evidence program above it. **SFR-1 Rev A** remains the steady-state reference architecture; **SFR-2 Rev A** remains a separate dynamic-compression assumption breaker; **SFR-3 Field Integrity Shell A** remains the synthetic magnetic-error-control branch; **Dual Boundary AHIS A** remains the independently monitored engineering boundary; **SFR-4 Integrated Physical-Promotion Campaign A** remains the integrated heat/magnetic campaign. Version 0.10.0 adds **SFR-5 Reality Gradient and Adaptive Inverse Design A**, which converts the SFR-4 magnetic rejection into a fail-closed architecture-search program instead of increasing brute-force sampling of the same family.

> **Release:** `0.10.0: Reality Gradient and Adaptive Inverse Design`
>
> **Repository verdict:** `GREEN` when all preserved evidence, the SFR-4 integrated campaign, and the SFR-5 adaptive inverse-design autopsy reproduce.
>
> **SFR-2 primary verdict:** `NO_PRIMARY_CASE_CROSSES_OPTIMISTIC_IGNITION_PROXY`
>
> **Actuation-overlay verdict:** `NO_DECLARED_BREATHING_CASE_IMPROVES_BOTH_CYCLE_AVERAGE_PROXY_AND_FUSION_POWER`
>
> **SFR-3 verdict:** `SYNTHETIC_HARMONIC_CONTROL_DEMONSTRATED__PHYSICAL_CONFINEMENT_UNPROVEN`
>
> **Dual-boundary verdict:** `DUAL_BOUNDARY_ARCHITECTURE_SCREEN_PASS__PHYSICAL_SURVIVABILITY_AND_CONFINEMENT_UNPROVEN`
>
> **SFR-4 verdict:** `INTEGRATED_REDUCED_CAMPAIGN_COMPLETE__NOMINAL_HEAT_ENVELOPE_SCREEN_PASS__PHYSICAL_COIL_EQUILIBRIUM_CONFINEMENT_AND_FUSION_UNPROVEN`
>
> **SFR-5 verdict:** `REALITY_GRADIENT_AUTOPSY_COMPLETE__CURRENT_MAGNETIC_FAMILY_REJECTED__ADAPTIVE_INVERSE_DESIGN_PATH_DEFINED__NO_PHYSICS_PROMOTION`
>
> No branch claims demonstrated confinement, ignition, net energy, tritium self-sufficiency, net electricity, buildable hardware, reactor safety, or reactor feasibility.

## What v0.10.0 adds

SFR-5 treats the `0 / 80` SFR-4 magnetic result as information about the search representation, not an invitation to sample the same family more densely. Its diagnosis is regenerated from the committed SFR-4 result and thresholds rather than hard-coded into a new narrative.

| SFR-5 diagnostic | Executed result |
|---|---:|
| SFR-4 direct-filament candidates | 80 |
| Combined topology passes | 0 |
| Mean-transform factor required to reach the minimum iota gate | 3.8265x |
| Remaining normalized excursion slack | 3.887% |
| Held-out richer-basis RMS normal-field error / declared limit | 12.9825x |
| Earned fusion-progress credit | 0 |

The two magnetic diagnostics remain separate evidence lanes because they are not the same physical coil representation. SFR-5 rejects continued brute-force search of the fixed helical plus fixed hybrid filament basis as the preferred next move, while explicitly **not** rejecting stellarators, quasi-isodynamic configurations, nonplanar modular coils or fusion.

The new inverse-design contract allows the plasma boundary, winding surface, nonplanar coil geometry, current groups, REBCO orientation and engineering keep-outs to move. Constraint failures become normalized pressure signals. A backward geometry gradient is only permitted when a real solver supplies analytic, automatic-differentiation or controlled finite-difference sensitivities; the base release deliberately records that step as `NOT_RUN`.

Primary v0.10 artifacts:

- `results/sfr5/SFR5_REALITY_GRADIENT_A_RESULT.md`
- `results/sfr5/sfr5_reality_gradient_a_v0100.json`
- `configs/reactor/sfr5_reality_gradient_a.json`
- `docs/reactor/30_SFR5_REALITY_GRADIENT.md`
- `docs/reactor/31_SFR5_PROMOTION_GATES.md`
- `external_solvers/sfr5_inverse_design_evidence_contract.json`
- `provenance/SFR5_REALITY_GRADIENT_TECHNICAL_BASIS_2026.json`

## What v0.9.0 adds

All seven requested computational workstreams were attempted. The result is deliberately split: the heat architecture passes its declared nominal and steady reduced envelope, while the scanned physical coil family fails.

| Workstream | Executed result | Promotion decision |
|---|---|---|
| Physical coil field | 80 direct-filament Biot-Savart and field-line cases | 0 combined topology passes; current family rejected |
| Finite-beta equilibrium | DESC and VMEC++ adapters explicitly attempted | Dependencies unavailable; no equilibrium result fabricated |
| Coil/plasma co-design | Expanded geometry/current scan and held-out normal-field reconstruction | Production SIMSOPT co-design not run |
| Particle confinement | 3.5 MeV alpha gyroradius scope, approximately 0.0449 m at 6 T | No guiding-center or transport credit |
| Burn | Q=20 target requirement with declared alpha deposition and bremsstrahlung | Approximately H_ISS04 2.00 at design iota; not linked to a passing coil |
| Magnet engineering | Centerline strain, magnetic pressure and stored-energy scopes | Winding-pack FEA, peak conductor field and quench qualification open |
| Reactor systems | D-T source, breeding coverage, heat and conditional power ledgers | Full 3-D TBR and net-electric prediction open |

### Heat-exhaust result

The heat problem is separated into first-wall radiation, divertor exhaust and blanket neutron heating. At the declared 1 GW fusion target and Q=20 ledger, the selected requirement sends 60% of 228.98 MW plasma exhaust into controlled radiation and 40% to a 24 m2 effective island-divertor wetted area.

| Quantity | v0.9 reduced result |
|---|---:|
| First-wall peak heat flux | 0.294 MW/m2 |
| Divertor peak heat flux | 5.724 MW/m2 |
| Nominal first-wall tungsten surface | 401.2 C |
| First wall at declared 1 MW/m2 steady upper bound | 523.8 C |
| Divertor tungsten surface | 678.3 C |
| Divertor water mass flow | 426.0 kg/s through 960 parallel channels |
| Mean channel velocity | 7.56 m/s |
| Hydraulic pumping screen | 0.122 MW |

The retained architecture uses a helium-cooled segmented-tungsten/graded-W-RAFM/ODS-RAFM first wall, an isolated PbLi DCLL blanket, and an independently bounded water-cooled W/OFHC-Cu/CuCrZr divertor. Water and PbLi may not share a boundary, penetration or heat exchanger.

“Heat resolved” is restricted to requirement authority for nominal and declared steady conditions. Stable detachment, the three-dimensional island footprint, critical heat flux, erosion, cyclic fatigue, irradiation, transient events, accidents and hardware qualification remain open.

### Magnetic result

The best scoring direct-filament case reaches approximately 0.0653 mean iota against a minimum 0.25 gate. Its radial-excursion screen passes, but the transform screen fails. The held-out richer basis remains approximately 6.49% RMS normal field against a 0.5% screen. Raising current in this classical helical family is rejected as the next design move; a fundamentally different optimized nonplanar modular-coil family is required.

Primary v0.9 artifacts:

- `results/sfr4_integrated/SFR4_INTEGRATED_PHYSICAL_PROMOTION_A_RESULT.md`
- `BOM/SFR4_INTEGRATED_PROMOTION_BOM.md`
- `docs/reactor/25_SFR4_INTEGRATED_PHYSICAL_CAMPAIGN.md`
- `docs/reactor/26_SFR4_HEAT_EXHAUST_RESOLUTION.md`
- `docs/reactor/27_SFR4_SOLVER_ATTEMPTS.md`
- `docs/reactor/28_SFR4_PROMOTION_GATES.md`
- `docs/reactor/29_SFR4_DECISION.md`

## What v0.8.0 adds

The user's "AHIS flipped inside out" idea is implemented as two independent, instrumented engineering boundaries around the unchanged magnetic-confinement concept. The inner lane looks inward from protected positions behind the plasma-facing armor and first wall. The outer lane monitors the double-wall vessel, shielding, cryostat and magnet-support alignment. Neither lane enters the plasma volume, presses on plasma, or receives direct confinement credit.

| Item | Selected v0.8 configuration | Reduced-screen result |
|---|---|---|
| Plasma-facing stack | Segmented tungsten, graded W-to-RAFM transition, helium-cooled ODS-Eurofer/RAFM first wall | 420.7 °C nominal surface; 632.9 °C declared steady-upset upper bound |
| Breeding and shielding | Enriched PbLi DCLL blanket, electrically insulating SiC/alumina channel inserts, WC/B4C shield, local HfH only after 3-D neutronics | Architecture selected; no TBR, corrosion, MHD-pressure-drop or lifetime credit |
| Double boundary | Monitored 316LN-class double-wall vessel and interspace, followed by thermal shield, cryostat and monitored support shell | 192 paired locations across 24 toroidal sectors and eight poloidal stations |
| Instrumentation | Two independent inner/outer lanes, hard vacuum/interspace channels and sector-level references | 1,736 declared sensing elements; radiation survivability and calibration remain unqualified |
| Fault campaign | Eleven nominal and fault scenarios | All expected deterministic states reproduced; a sub-sensitivity armor crack is intentionally not detected and requires periodic NDE |
| Fusion effect | None credited | Earned confinement, fusion, ignition and net-electric improvement remain exactly zero |

The 1-D temperature and coefficient-of-thermal-expansion calculations are sizing screens, not thermal FEA, fracture mechanics or lifetime predictions. The reported raw mismatch proxy for the selected stack is approximately **0.212%** and is deliberately not converted into stress or pass/fail structural credit. The cooler W/Cu/CuCrZr comparison is deferred because a water-cooled first wall beside PbLi creates a more severe integration and accident problem. The SiCf/SiC comparison remains attractive at high temperature but is deferred by joining, code-qualification and maturity gaps.

The architecture can trigger magnetic trim, power rundown, coolant isolation, safe hold and inspection. It cannot squeeze plasma with wall pressure. Its purpose is to detect damage, preserve geometry and prevent an engineering fault from silently degrading the magnetic cage.

Primary v0.8 artifacts:

- `results/sfr3_dual_boundary/SFR3_DUAL_BOUNDARY_AHIS_A_RESULT.md`
- `BOM/SFR3_DUAL_BOUNDARY_AHIS_BOM.md`
- `docs/reactor/21_SFR3_DUAL_BOUNDARY_ARCHITECTURE.md`
- `docs/reactor/22_SFR3_DUAL_BOUNDARY_MATERIAL_SELECTION.md`
- `docs/reactor/23_SFR3_DUAL_BOUNDARY_FAULT_CAMPAIGN.md`
- `docs/reactor/24_SFR3_DUAL_BOUNDARY_PROMOTION_GATES.md`

## What v0.7.0 adds

Seven uploaded repositories—AHIS, PressureX, IX-Vibe, IX-Breath, IX-GCR-SPE, IX-Shield and IX-HfTaZen-Shield—were audited as mechanism donors. No hidden material or liquid confinement mechanism was found. Their defensible patterns were translated into a magnetic field-integrity architecture:

| SFR-3 layer | Decision | v0.7 evidence state |
|---|---|---|
| Primary confinement | Keep the steady copper-stabilized REBCO field and rigid vessel | Architecture reference only |
| Active correction | Add 24 individually driven planar trim channels | 12-by-24 synthetic response is full row rank; physical response not solved |
| Passive correction | Study 24 flux-conserving superconducting loops | Transient response only; exactly zero DC-error credit |
| Observability and FDIR | Add magnetic/current/quench/strain/motion sensing, confidence gates and independent safe hold | Fault-state logic executes deterministically |
| Structural control | Target measured support modes with warm-side damping and alignment monitoring | Architecture only; no unmeasured damping credit |
| Magnet protection | Concentrate WC/B4C and solver-dependent HfH shielding around REBCO and streaming paths | No transferred tokamak performance; 3-D OpenMC required |
| Plasma-facing/edge | Segmented tungsten family; boron or local liquid lithium only as guarded experiments | Zero direct confinement credit |

The declared synthetic commissioning challenge produces approximately **65.46% nominal RMS reduction**, **66.36% with one unavailable trim channel**, and **55% passive attenuation of a pure transient challenge**. Low sensor confidence disables active correction. Those numbers validate the mathematical control decomposition only; the repo assigns them **zero confinement, fusion-power, ignition and net-electric gain**.

The 52-row architecture inventory is `BOM/SFR3_FIELD_INTEGRITY_SHELL_BOM.csv`. The result is `results/sfr3_field_integrity/sfr3_field_integrity_shell_a_v070.json`. Physical promotion begins by replacing the analytic response matrix with CAD-linked Biot-Savart fields and then testing finite-beta equilibria and islands.

## What v0.6.0 adds

The baseline 23 / 26 / 23 / 26 ft ABAB geometry, rigid vessel and steady primary HTS field remain unchanged. The new overlay tests three auxiliary magnetic-field patterns over 720 samples per cycle at depths from 0% through 5%.

| Actuation question | v0.6 result |
|---|---|
| Does synchronous squeeze and expansion sustain an advantage? | **No.** The 5% case produces an instantaneous proxy peak near 0.9981 during expansion, when uniform fusion power has fallen to about 802.5 MW. Its cycle-average proxy is worse than the unchanged baseline. The peak is not ignition capture. |
| Does an ABAB-opposed wave improve both principal metrics? | **No.** No declared case improves both cycle-average optimistic ignition ratio and cycle-average uniform fusion power. |
| Does the traveling-quadrature wave move closer? | **Only nominally in one proxy and not jointly.** At 5% depth the cycle-average ratio changes from about 0.961077 to 0.961559 while cycle-average uniform fusion power falls from 1000.000 to about 997.233 MW, before actuator losses. |
| Does any cycle-average case cross the proxy? | **No.** |
| Does the Gemini tri-lobe image supply a fusion mechanism? | **No earned gain.** Astrophysical accretion and three-body collision claims are rejected. An area-preserving poloidal `m=3` harmonic repeated inside all four field periods is retained only as a testable actuator symmetry. |
| Is the actuator hardware specified? | **At architecture level only.** The 24-row overlay BOM selects eight normal-conducting triplet stations and 24 independent circuits. Currents, turns, voltage, cooling, forces and placement remain solver or hardware dependent. |

The machine-readable result is `results/sfr2_actuation/sfr2_actuation_overlay_a_v060.json`. The concise interpretation is in `results/sfr2_actuation/SFR2_ACTUATION_OVERLAY_A_RESULT.md`.


## What v0.5.0 adds

v0.5.0 does **not** rewrite SFR-1. It adds SFR-2 Rev A as a separately gated assumption-breaker study built from the 23 / 26 / 23 / 26 ft concept.

| SFR-2 question | v0.5 result |
|---|---|
| Four machines or one plasma system? | **One continuous closed toroidal plasma system.** The four dimensions are consecutive ABAB sector arc lengths, not independent plasmas connected by ducts. |
| Does the 23/26 staggering itself earn confinement credit? | **No.** v0.5 assigns zero benefit to staggering until a real 3-D equilibrium/transport calculation demonstrates one. |
| Does “magnetic rifling” help in the empirical screen? | **Yes, monotonically inside ISS04.** At the highest declared 15 T field with no compression, the target-power-matched ratio rises from ~0.814 at `iota=0.6` to ~0.961 at `iota=0.9`. This is not proof that such a field is realizable. |
| Does radial compression automatically improve the ignition screen? | **No.** At the same 1 GW target and `H_ISS04=1`, 0%, 5%, and 10% squeeze give approximately 0.961, 0.889, and 0.816 respectively at the most favorable declared field/transform point. The smaller minor radius penalizes ISS04 confinement. |
| Is phase-controlled traveling-wave/RF heating credited? | **No.** Numerical credit is exactly zero until a self-consistent wave/plasma calculation exists. |
| Is magnetic-flux compression credited? | **No.** Axis field is held fixed in the compression screen. |
| Did any primary SFR-2 point cross the optimistic ignition proxy? | **No.** The best primary case requires `H_ISS04 ≈ 1.0405` in an already optimistic alpha-only balance. That is not “4% away from fusion.” |

The implementation intentionally supersedes earlier conversational percentages. Only repository-generated results count as SFR-2 evidence. See `docs/reactor/12_SFR2_DYNAMIC_COMPRESSION.md` and `results/sfr2/SFR2_REVA_SCREEN_RESULT.md`.

## What v0.4.0 resolves

v0.4 turns the remaining red-X list into explicit executed calculations or production-solver jobs. It does not rename a surrogate as high fidelity.

| Problem | v0.4 result |
|---|---|
| Failed fixed coil basis | **Resolved as rejected.** Two new architecture classes are executed: classical helical TF+helix co-design scans and a continuous winding-surface current-potential reconstruction. Neither earns promotion. |
| G1 equilibrium | **Input-generation problem closed; production solve open.** Four finite-pressure VMEC-family seed files are generated from the exact analytic SFR-1 screening boundary for DESC/VMEC++ execution and cross-check. |
| G3/G4 confinement | **Requirements/topology quantified; kinetic validation open.** Q=10 confinement requirement and vacuum field-line transform/nestedness are executable; alpha-orbit, neoclassical and gyrokinetic production evidence remains required. |
| G2 HTS magnets | **Geometry screen executable; magnet qualification open.** Curve length, bend radius and conservative REBCO hard-way strain proxy are calculated; field-performance failure prevents promotion and winding-pack Ic/FEA/quench/manufacturing qualification remains mandatory. |
| G7 neutronics/TBR | **Source and geometric breeding bounds closed; full 3-D transport open.** Exact D-T source/tritium ledgers and blanket-coverage constraints are calculated; an OpenMC CSG torus proxy builder and 3-D statepoint analyzer are included. |
| G8 net electric | **Conditional plant equations closed.** The current ~704.57 MW uniform screen gives ~204.10 MWe under the declared plant assumptions; the 300 MWe floor requires ~913.04 MW fusion; the 1 GW target ledger gives 340 MWe. |
| Actual net-electric fusion | **Not computationally resolvable.** It requires physical hardware and calibrated measurements. |

## Current numerical snapshot

At the current 8.0 m major radius, 1.7 m minor-radius screening geometry, 6 T axis field, 3% beta and 15 keV uniform D-T screen:

- screened fusion power: **704.57 MW**;
- fusion power required to clear the 300 MWe plant floor under the existing plant assumptions: **913.04 MW**;
- corresponding fixed-temperature uniform-beta screen for that net floor: **~3.415% beta**;
- beta screen for the 1 GW target: **~3.574%**;
- current screened net-electric algebra: **~204.10 MWe**;
- 1 GW target net-electric algebra: **340 MWe**;
- expanded v0.9 best-scoring classical-helical vacuum architecture: **6FP, four alternating helices, 1.0 helical/TF current ratio**; it retains the radial-excursion screen but produces only **~0.0653 mean iota**, so it fails the transform requirement;
- continuous winding-surface current-potential held-out RMS `Bn/B0`: **~1.64% (2FP), 2.32% (3FP), 3.05% (4FP), 4.57% (6FP)** — all fail the 0.5% screen;
- the geometry-only REBCO strain proxy is below the 0.4% ceiling for the screened TF/helical centerlines, but that is **not** winding-pack qualification.

These numbers are evidence at their stated authority only. A failed reduced/intermediate screen can reject an architecture; a passing reduced screen cannot prove a reactor.

## High-fidelity execution pack

The repository contains exact fixed-boundary finite-pressure seed inputs:

- `external_solvers/inputs/input.SFR1_QA_2FP_REF`
- `external_solvers/inputs/input.SFR1_QI_3FP`
- `external_solvers/inputs/input.SFR1_QI_PWO_4FP`
- `external_solvers/inputs/input.SFR1_C6_QI_6FP`

and executable adapters:

- `external_solvers/adapters/run_desc_equilibrium.py`
- `external_solvers/adapters/run_vmecpp_equilibrium.py`
- `external_solvers/adapters/build_openmc_axisymmetric_proxy.py`
- `external_solvers/adapters/analyze_openmc_3d_tbr.py`
- `external_solvers/adapters/validate_production_receipt.py`

The adapters **stop** if the real dependency is unavailable. They never silently replace DESC, VMEC++ or OpenMC with in-repo surrogate physics.

## Run the in-repo campaign

```bash
python scripts/run_computational_closure.py
python scripts/generate_v040_evidence.py
python scripts/run_sfr2_screen.py
python scripts/run_sfr2_actuation_overlay.py
python scripts/run_sfr3_field_integrity.py
python scripts/run_sfr3_dual_boundary.py
python scripts/run_sfr4_integrated_campaign.py
python scripts/run_sfr5_reality_gradient.py
python check_stellarforge.py
```

The first command is the expensive deterministic architecture campaign. The release gate validates its tracked evidence rather than repeatedly recomputing the same field scan in several subprocesses.

## Reactor envelope

| Item | Rev A value | Authority |
|---|---:|---|
| Major radius | 8.0 m | reference-informed target |
| Minor radius | 1.7 m | design target |
| On-axis field | 6.0 T | reference-informed target |
| Volume-average beta | 3.0% | screening/design point |
| Fusion-power class | 1,000 MW | design target |
| HTS operating temperature | 20 K | reference-informed target |
| Maximum field on conductor | ≤20 T | design ceiling |
| Plasma-to-coil distance | 1.35 m target; 1.20 m hard floor | design constraint |
| Full-3D TBR | ≥1.15 target; 1.10 hard floor | production-solver objective |
| Thermal conversion efficiency | 40% target | plant target |
| Recirculating-power ceiling | 120 MW | design target |
| Net-electric floor | 300 MW | design requirement, not prediction |

No core is privileged: 2FP QA reference, 3FP QI, 4FP QI/piecewise-omnigenous, 6FP C6 lineage and a direct-J assumption-breaker remain competitors.

## BOM / design inventory

`BOM/SFR1_FULL_SYSTEM_BOM.csv` and `.md` contain **87 unique system-level rows** spanning plasma, magnets, cryogenics, vacuum, PFCs, blanket/shield, tritium/fueling, RF, diagnostics, controls, heat transport, power conversion, electrical, maintenance, safety, facility and solver infrastructure.

`BOM/SFR3_FIELD_INTEGRITY_SHELL_BOM.csv` contains **52 rows** covering direct field sources, trim and passive correction, diagnostics, guarded control, support-mode damping, magnet shielding, plasma-facing and blanket integration, maintenance and explicit rejected/separate concepts. Diamond, glitter, passive dense liquids and flexible-vessel compression are not hidden as active components.

`BOM/SFR3_DUAL_BOUNDARY_AHIS_BOM.csv` contains **64 rows** covering the selected tungsten/RAFM/PbLi stack, two comparison stacks, independent inner and outer sensing, interspace leak monitoring, support/alignment surveillance, protection actions, evidence jobs and explicit rejection/defer decisions. PVDF and unqualified electronics are not placed at the plasma-facing surface.

`BOM/SFR4_INTEGRATED_PROMOTION_BOM.csv` contains **64 rows** covering all seven workstreams, the separated helium/PbLi/water heat architecture, production solver requirements, particle and burn tools, magnet qualification, neutron transport, fuel cycle, remote maintenance and high-heat-flux testing.

“Full” means complete at the system-architecture inventory level. It is **not** falsely labeled a procurement/fabrication BOM: final quantities, nuclear compositions/enrichment, conductor sizing/current, pressure ratings, safety setpoints, vendors, part numbers and drawings remain solver/hardware dependent.

## Evidence gates after v0.10

1. **G1 equilibrium — production execution open.** Inputs are complete; real finite-beta DESC and VMEC++ convergence/cross-code evidence has not been executed in this build runtime.
2. **G2 coils — new architectures executed, no promoted set.** Low/intermediate tests reject current fixed boundary/coil combinations; true plasma/coil co-optimization, REBCO Ic/strain over winding packs, loads/support FEA, tolerances and quench remain open.
3. **G3/G4 confinement — requirements and vacuum topology quantified, kinetic transport open.**
4. **G5 edge/divertor — open.**
5. **G6 RF — resonance-scale screen retained; 3-D deposition/wall-plug closure open.**
6. **G7 neutronics — source/coverage bounds complete; full 3-D OpenMC/DAGMC transport open.**
7. **G8 system — conditional algebra closed; coupled prediction waits on G1–G7.**
8. **G9 hardware — open by definition.**

SFR-2 has its own independent gates. Only `SFR2_G0_SPEC` is `PASS_SPEC_ONLY`; dynamic equilibrium, coils/field, particle and alpha orbits, transport/MHD, transient edge heat flux, RF/phase control, neutronics/TBR, integrated burn/plant, and hardware are all `NOT_RUN`. SFR-1 evidence cannot silently promote SFR-2.

The actuation overlay is independently gated. Only `SFR2A_G0_OVERLAY_SPEC` is `PASS_SPEC_ONLY`. Time-dependent equilibrium, coils/electromagnetics, magnetic-pumping kinetics, particle and alpha orbits, transport/MHD, wall loads, integrated power and hardware all remain `NOT_RUN`.

SFR-3 is independently gated. `SFR3_G0_ARCHITECTURE_SPEC` is `PASS_SPEC_ONLY` and `SFR3_G1_SYNTHETIC_CONTROLLABILITY` is `PASS_LOW_AUTHORITY_SYNTHETIC_ONLY`. Physical Biot-Savart response, free-boundary equilibrium/islands, particle and alpha orbits, transport/MHD, magnet engineering, 3-D neutronics/TBR, integrated burn/plant and hardware are all `NOT_RUN`. The synthetic pass cannot promote any of them.

Dual Boundary AHIS A is also independently gated. Only its configuration and reduced thermal/fault-logic screens pass. Conjugate thermal FEA, disruption/EM structural FEA, W/RAFM joint qualification, coolant and PbLi MHD/corrosion loops, sensor irradiation/calibration, 3-D neutronics, remote maintenance and integrated hardware tests remain `NOT_RUN`. No passing reduced screen can promote those gates.

SFR-4 is independently gated. Its specification passes; its scanned coil family fails; its nominal and declared steady reduced heat screen passes. CAD-linked nonplanar coil optimization, DESC/VMEC++ equilibrium, islands/stability, alpha and thermal transport, 3-D edge/divertor physics, CFD/FEA/fatigue/irradiation, OpenMC TBR, integrated burn/plant analysis and hardware remain `NOT_RUN`.

SFR-5 is independently gated. Only `SFR5_G0_SPEC_AND_AUTOPSY` is `PASS_REDUCED`: the v0.9 magnetic evidence is reinterpreted as an architecture-family rejection and a declared inverse-design search direction. Movable-geometry sensitivities, winding-surface feasibility, discrete nonplanar-coil realization, single-stage finite-beta plasma/coil co-design, transport, 3-D heat/magnet/neutronics closure, integrated plant analysis and hardware remain `NOT_RUN`. Constraint pressure is diagnostic until a real movable-geometry evaluator supplies sensitivities; SFR-5 assigns zero unearned physics or fusion credit.

## Quality gate

```bash
python check_stellarforge.py
```

`IX-STELLARATORFORGE: GREEN` means release integrity, the complete deterministic test suite, preserved SFR-1/SFR-2/SFR-3 evidence, the dual-boundary reduced screen, the SFR-4 integrated campaign, the SFR-5 Reality Gradient autopsy, BOM contracts, license, tracked computations and solver contracts reproduce. **It never means fusion was achieved.**

## License and permission contact

This repository is **source-available for research/evaluation only** under `LicenseRef-IX-StellaratorForge-Eval-Only-1.1`; it is not OSI open source. Physical construction, manufacturing, deployment, reactor/lab-plasma operation, commercial use, power generation, or use outside the grant requires a separate written license from the project owner.

Licensing/permission inquiries: **https://www.linkedin.com/in/brycewdesign/**

A LinkedIn connection, message, discussion, download, citation or repository access does not itself grant additional rights. See `LICENSE`, `LICENSING.md`, and `NOTICE`.

## Start here

- `FINAL_STATUS.md`
- `PROOF_OF_CONCEPT.md`
- `docs/reactor/30_SFR5_REALITY_GRADIENT.md`
- `docs/reactor/31_SFR5_PROMOTION_GATES.md`
- `results/sfr5/SFR5_REALITY_GRADIENT_A_RESULT.md`
- `results/sfr5/sfr5_reality_gradient_a_v0100.json`
- `docs/reactor/25_SFR4_INTEGRATED_PHYSICAL_CAMPAIGN.md`
- `docs/reactor/26_SFR4_HEAT_EXHAUST_RESOLUTION.md`
- `docs/reactor/27_SFR4_SOLVER_ATTEMPTS.md`
- `docs/reactor/28_SFR4_PROMOTION_GATES.md`
- `docs/reactor/29_SFR4_DECISION.md`
- `results/sfr4_integrated/SFR4_INTEGRATED_PHYSICAL_PROMOTION_A_RESULT.md`
- `BOM/SFR4_INTEGRATED_PROMOTION_BOM.md`
- `docs/reactor/21_SFR3_DUAL_BOUNDARY_ARCHITECTURE.md`
- `docs/reactor/22_SFR3_DUAL_BOUNDARY_MATERIAL_SELECTION.md`
- `docs/reactor/23_SFR3_DUAL_BOUNDARY_FAULT_CAMPAIGN.md`
- `docs/reactor/24_SFR3_DUAL_BOUNDARY_PROMOTION_GATES.md`
- `results/sfr3_dual_boundary/SFR3_DUAL_BOUNDARY_AHIS_A_RESULT.md`
- `BOM/SFR3_DUAL_BOUNDARY_AHIS_BOM.md`
- `docs/reactor/17_SFR3_DONOR_TRANSLATION_LEDGER.md`
- `docs/reactor/18_SFR3_FIELD_INTEGRITY_SHELL.md`
- `docs/reactor/19_SFR3_MATERIAL_AND_LIQUID_BRANCHES.md`
- `docs/reactor/20_SFR3_PROMOTION_GATES.md`
- `results/sfr3_field_integrity/SFR3_FIELD_INTEGRITY_SHELL_A_RESULT.md`
- `BOM/SFR3_FIELD_INTEGRITY_SHELL_BOM.md`
- `docs/reactor/12_SFR2_DYNAMIC_COMPRESSION.md`
- `docs/reactor/13_SFR2_PROMOTION_GATES.md`
- `results/sfr2/SFR2_REVA_SCREEN_RESULT.md`
- `docs/reactor/14_SFR2_PHASE_PROGRAMMED_BREATHING.md`
- `docs/reactor/15_TRILOBE_CONCEPT_TRANSLATION.md`
- `docs/reactor/16_SFR2_ACTUATION_AND_TRILOBE_GATES.md`
- `results/sfr2_actuation/SFR2_ACTUATION_OVERLAY_A_RESULT.md`
- `BOM/SFR2_ACTUATION_OVERLAY_BOM.md`
- `docs/closure/06_MAXIMUM_COMPUTATIONAL_CLOSURE.md`
- `results/computational_closure/SFR1_V040_RESULT.md`
- `BOM/SFR1_FULL_SYSTEM_BOM.md`
- `external_solvers/README.md`

The inherited IX-Fusion documentation/results remain in place as foundation evidence and are not rewritten into a success claim.
