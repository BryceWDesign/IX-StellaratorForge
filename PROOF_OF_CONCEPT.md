# IX-StellaratorForge — executable evidence overview

Release: **0.10.0**

## SFR-5 Reality Gradient and adaptive inverse design

v0.10.0 converts the preserved SFR-4 magnetic rejection into a deterministic architecture-search decision. It derives the diagnostic values from the committed SFR-4 JSON and config, preserves the topology and held-out reconstruction as separate evidence lanes, and stores the rejected family in fail-closed memory.

Result: `REALITY_GRADIENT_AUTOPSY_COMPLETE__CURRENT_MAGNETIC_FAMILY_REJECTED__ADAPTIVE_INVERSE_DESIGN_PATH_DEFINED__NO_PHYSICS_PROMOTION`.

The result means the fixed helical plus fixed hybrid filament-basis family is no longer the preferred target for more brute-force sampling. It does not prove a replacement coilset. Geometry sensitivities, winding-surface optimization, discrete nonplanar coils, finite-beta co-design, transport, TBR, magnet qualification, plant closure and hardware all remain unrun.

## SFR-4 integrated campaign

v0.9.0 attempts all seven requested computational workstreams. Its executable result is deliberately split:

> The declared nominal and steady heat envelope can be satisfied in a reduced requirement model by controlled radiation, at least 24 m2 effective island-divertor wetted area, a helium-cooled tungsten/RAFM first wall and an independently bounded water-cooled W/Cu/CuCrZr divertor. The scanned 80-case classical helical coil family cannot supply the required transform and is rejected.

Result: `INTEGRATED_REDUCED_CAMPAIGN_COMPLETE__NOMINAL_HEAT_ENVELOPE_SCREEN_PASS__PHYSICAL_COIL_EQUILIBRIUM_CONFINEMENT_AND_FUSION_UNPROVEN`.

This proves only executable bookkeeping, falsification and requirements. It does not prove equilibrium, confinement, detachment, thermal lifetime, safety or fusion.

## Dual Boundary AHIS A

v0.8.0 adds the proposed inward-facing and outer AHIS layers to the full repository as a separately gated engineering branch. Its executable proof is intentionally narrow:

> Three declared wall stacks can be compared with the same low-authority 1-D thermal model; the selected tungsten/RAFM/PbLi stack can be instrumented at 192 paired inner/outer locations; eleven deterministic fault states can fail closed; and all walls and sensors receive exactly zero plasma-confinement and fusion credit.

Result: `DUAL_BOUNDARY_ARCHITECTURE_SCREEN_PASS__PHYSICAL_SURVIVABILITY_AND_CONFINEMENT_UNPROVEN`.

This is a material-stack, observability and fault-response architecture result. It is not pressure confinement, equilibrium, transport, thermal FEA, structural survival, sensor qualification, blanket performance, a safety case or fusion.

## SFR-3

v0.7.0 adds Field Integrity Shell A as a separate confinement-support branch. Its executable proof is intentionally narrow:

> A 24-channel synthetic trim-coil basis spans the declared 12-component harmonic challenge, meets bounded nominal and single-channel-fault reduction thresholds, applies passive-loop credit only to transients, and fails closed when the control state is not trustworthy.

Result: `SYNTHETIC_HARMONIC_CONTROL_DEMONSTRATED__PHYSICAL_CONFINEMENT_UNPROVEN`.

This is an architecture and controllability result. It is not a coil field, equilibrium, island, orbit, transport, MHD, neutron, burn, plant or hardware result.

## SFR-1

SFR-1 Rev A remains the steady-state reference architecture. Its v0.4 proof-of-concept and maximum in-repository computational closure artifacts are preserved unchanged:

- PoC verdict: `PIPELINE_POC_PASS__REACTOR_PHYSICS_NOT_CLOSED`
- maximum closure verdict: `MAXIMUM_IN_REPO_COMPUTATIONAL_CLOSURE_COMPLETE__PRODUCTION_SOLVER_AND_HARDWARE_GATES_REMAIN`

The SFR-1 PoC verifies executable architecture validation, D-T burn arithmetic, confinement requirements, target-vs-screened power accounting, RF resonance, source-term accounting and held-out magnetic reconstruction. The v0.4 maximum closure layer adds production MHD seed generation, alternative vacuum magnet architecture screens, field-line tracing, geometry-only HTS strain proxies, TBR coverage constraints and conditional plant thresholds.

None of those artifacts impersonates DESC/VMEC++, kinetic transport, structural FEA, full 3-D OpenMC transport or hardware.

## SFR-2

v0.5.0 added SFR-2 Rev A as a separate assumption-breaker, not as a promotion of SFR-1. v0.6.0 adds a separately gated magnetic-breathing and tri-lobe actuation overlay while keeping both SFR-1 and SFR-2 Rev A unchanged.

Its proof-of-concept claim is intentionally narrower:

> The 23/26/23/26 ABAB concept can be represented as a deterministic computational hypothesis with explicit geometry, compression assumptions, target-power matching, ISS04 sensitivity, promotion gates, and zero numerical credit for unmodeled phase/RF or flux-compression effects.

Primary SFR-2 verdict:

`NO_PRIMARY_CASE_CROSSES_OPTIMISTIC_IGNITION_PROXY`

That negative result is retained. It prevents the repository from turning earlier exploratory percentages into evidence.

## Run

```bash
python scripts/run_sfr1_poc.py
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

Tracked SFR-2 outputs:

- `configs/reactor/sfr2_rev_a.json`
- `results/sfr2/sfr2_rev_a_screen_v050.json`
- `results/sfr2/SFR2_REVA_SCREEN_RESULT.md`
- `results/sfr2_actuation/sfr2_actuation_overlay_a_v060.json`
- `results/sfr2_actuation/SFR2_ACTUATION_OVERLAY_A_RESULT.md`
- `docs/reactor/12_SFR2_DYNAMIC_COMPRESSION.md`
- `docs/reactor/13_SFR2_PROMOTION_GATES.md`

Tracked SFR-3 outputs:

- `configs/reactor/sfr3_field_integrity_shell_a.json`
- `results/sfr3_field_integrity/sfr3_field_integrity_shell_a_v070.json`
- `results/sfr3_field_integrity/SFR3_FIELD_INTEGRITY_SHELL_A_RESULT.md`
- `BOM/SFR3_FIELD_INTEGRITY_SHELL_BOM.csv`
- `docs/reactor/17_SFR3_DONOR_TRANSLATION_LEDGER.md`
- `docs/reactor/18_SFR3_FIELD_INTEGRITY_SHELL.md`
- `docs/reactor/20_SFR3_PROMOTION_GATES.md`

Tracked dual-boundary outputs:

- `configs/reactor/sfr3_dual_boundary_ahis_a.json`
- `results/sfr3_dual_boundary/sfr3_dual_boundary_ahis_a_v080.json`
- `results/sfr3_dual_boundary/SFR3_DUAL_BOUNDARY_AHIS_A_RESULT.md`
- `BOM/SFR3_DUAL_BOUNDARY_AHIS_BOM.csv`
- `docs/reactor/21_SFR3_DUAL_BOUNDARY_ARCHITECTURE.md`
- `docs/reactor/22_SFR3_DUAL_BOUNDARY_MATERIAL_SELECTION.md`
- `docs/reactor/23_SFR3_DUAL_BOUNDARY_FAULT_CAMPAIGN.md`
- `docs/reactor/24_SFR3_DUAL_BOUNDARY_PROMOTION_GATES.md`

Tracked SFR-4 outputs:

- `configs/reactor/sfr4_integrated_physical_promotion_a.json`
- `results/sfr4_integrated/sfr4_integrated_physical_promotion_a_v090.json`
- `results/sfr4_integrated/SFR4_INTEGRATED_PHYSICAL_PROMOTION_A_RESULT.md`
- `BOM/SFR4_INTEGRATED_PROMOTION_BOM.csv`
- `docs/reactor/25_SFR4_INTEGRATED_PHYSICAL_CAMPAIGN.md`
- `docs/reactor/26_SFR4_HEAT_EXHAUST_RESOLUTION.md`
- `docs/reactor/27_SFR4_SOLVER_ATTEMPTS.md`
- `docs/reactor/28_SFR4_PROMOTION_GATES.md`
- `docs/reactor/29_SFR4_DECISION.md`

Tracked SFR-5 outputs:

- `configs/reactor/sfr5_reality_gradient_a.json`
- `results/sfr5/sfr5_reality_gradient_a_v0100.json`
- `results/sfr5/SFR5_REALITY_GRADIENT_A_RESULT.md`
- `schemas/reactor/sfr5_reality_gradient.schema.json`
- `provenance/SFR5_REALITY_GRADIENT_TECHNICAL_BASIS_2026.json`
- `external_solvers/sfr5_inverse_design_evidence_contract.json`
- `docs/reactor/30_SFR5_REALITY_GRADIENT.md`
- `docs/reactor/31_SFR5_PROMOTION_GATES.md`

## Promotion boundary

A low-authority model may reject a candidate. It may not declare one successful.

SFR-2 G1–G9 and SFR-3 G2–G9 remain unrun until candidate-specific high-authority evidence exists. Dual-boundary high-authority thermal, structural, irradiation, leak, blanket and integrated hardware gates are also unrun. Actual fusion and net-electric operation remain outside software authority.
