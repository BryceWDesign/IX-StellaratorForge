# IX-StellaratorForge

**Evidence-driven stellarator fusion reactor design and computational co-design program.**

IX-StellaratorForge preserves the original `IX-Fusion` research lineage and builds a reactor-level evidence program above it. **SFR-1 Rev A** remains the steady-state reference architecture; **SFR-2 Rev A** is a separate dynamic-compression assumption breaker introduced in v0.5.0.

> **Release:** `0.5.0 — SFR-2 Dynamic-Compression Assumption Breaker`
>
> **Repository verdict:** `GREEN` when the preserved SFR-1 v0.4 evidence and the SFR-2 v0.5 low-authority screen both reproduce.
>
> **SFR-2 primary verdict:** `NO_PRIMARY_CASE_CROSSES_OPTIMISTIC_IGNITION_PROXY`
>
> Neither SFR-1 nor SFR-2 claims demonstrated ignition, net energy, tritium self-sufficiency, net electricity, buildable hardware, or reactor feasibility.


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
- current best simple classical-helical vacuum architecture: **4FP, alternating helices, 0.40 helical/TF current ratio**; it retains the nestedness screen but produces only **~0.0389 mean iota**, so it fails the transform requirement;
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

“Full” means complete at the system-architecture inventory level. It is **not** falsely labeled a procurement/fabrication BOM: final quantities, nuclear compositions/enrichment, conductor sizing/current, pressure ratings, safety setpoints, vendors, part numbers and drawings remain solver/hardware dependent.

## Evidence gates after v0.5

1. **G1 equilibrium — production execution open.** Inputs are complete; real finite-beta DESC and VMEC++ convergence/cross-code evidence has not been executed in this build runtime.
2. **G2 coils — new architectures executed, no promoted set.** Low/intermediate tests reject current fixed boundary/coil combinations; true plasma/coil co-optimization, REBCO Ic/strain over winding packs, loads/support FEA, tolerances and quench remain open.
3. **G3/G4 confinement — requirements and vacuum topology quantified, kinetic transport open.**
4. **G5 edge/divertor — open.**
5. **G6 RF — resonance-scale screen retained; 3-D deposition/wall-plug closure open.**
6. **G7 neutronics — source/coverage bounds complete; full 3-D OpenMC/DAGMC transport open.**
7. **G8 system — conditional algebra closed; coupled prediction waits on G1–G7.**
8. **G9 hardware — open by definition.**

SFR-2 has its own independent gates. Only `SFR2_G0_SPEC` is `PASS_SPEC_ONLY`; dynamic equilibrium, coils/field, particle and alpha orbits, transport/MHD, transient edge heat flux, RF/phase control, neutronics/TBR, integrated burn/plant, and hardware are all `NOT_RUN`. SFR-1 evidence cannot silently promote SFR-2.

## Quality gate

```bash
python check_stellarforge.py
```

`IX-STELLARATORFORGE: GREEN` means release integrity, tests, preserved SFR-1 evidence, the SFR-2 deterministic screen, license, tracked computations and solver contracts reproduce. **It never means fusion was achieved.**

## License and permission contact

This repository is **source-available for research/evaluation only** under `LicenseRef-IX-StellaratorForge-Eval-Only-1.1`; it is not OSI open source. Physical construction, manufacturing, deployment, reactor/lab-plasma operation, commercial use, power generation, or use outside the grant requires a separate written license from the project owner.

Licensing/permission inquiries: **https://www.linkedin.com/in/brycewdesign/**

A LinkedIn connection, message, discussion, download, citation or repository access does not itself grant additional rights. See `LICENSE`, `LICENSING.md`, and `NOTICE`.

## Start here

- `FINAL_STATUS.md`
- `PROOF_OF_CONCEPT.md`
- `docs/reactor/12_SFR2_DYNAMIC_COMPRESSION.md`
- `docs/reactor/13_SFR2_PROMOTION_GATES.md`
- `results/sfr2/SFR2_REVA_SCREEN_RESULT.md`
- `docs/closure/06_MAXIMUM_COMPUTATIONAL_CLOSURE.md`
- `results/computational_closure/SFR1_V040_RESULT.md`
- `BOM/SFR1_FULL_SYSTEM_BOM.md`
- `external_solvers/README.md`

The inherited IX-Fusion documentation/results remain in place as foundation evidence and are not rewritten into a success claim.
