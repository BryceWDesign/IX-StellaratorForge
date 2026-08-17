# SFR-1 Closure Campaign — v0.3.0

## Purpose

This campaign attacks the open reactor questions using the highest-authority computation that can be reproduced in the repository **without inventing external solver output**. It separates three things that are often blurred together in concept-reactor work:

1. **analytical/empirical screens** that can expose contradictions;
2. **intermediate numerical models** that can kill obviously poor engineering choices; and
3. **high-fidelity external solvers** that are required before a gate can actually be promoted.

A reduced model may reject a candidate. It may not declare a reactor solved.

## What is newly computed

The machine-readable result is `results/closure/sfr1_v030_closure_campaign.json`.

For the Rev A screening envelope (R=8.0 m, a=1.7 m, B0=6 T, beta=3%, Ti=Te=15 keV), the in-repo Bosch-Hale uniform 50/50 D-T calculation gives about **704.57 MW** fusion power in the deliberately uniform-pressure model. The same model would require beta about **3.574%** to reach 1,000 MW at fixed B/T/volume, or an effective fusion-power profile/physics enhancement of about **1.419x** relative to that uniform calculation. A fixed-pressure temperature scan peaks near **13.5 keV** at about **710.87 MW** in this simplified model.

These values are not a claim that SFR-1 will produce those powers. They are consistency boundaries. Real profiles, impurities, helium ash, radiation, alpha redistribution and transport must replace the uniform model.

For a 1,000 MW target, the Q=10 confinement screen requires approximately **0.984 s** energy confinement and an ISS04 screening enhancement **H≈1.63** using iota=0.55. The ignition-limit screen requires approximately **1.48 s** and **H≈1.91**. ISS04 is empirical; neither number replaces gyrokinetic or neoclassical calculation.

The simple 24-coil encircling-only Biot-Savart diagnostic reproduces the gross field but leaves percent-level normal-field error on the reduced non-axisymmetric boundaries. v0.3 also adds a richer 120-filament fixed basis and validates it on an unseen angularly offset surface grid. All tested 2FP/3FP/4FP/6FP cases still fail the 0.5% RMS screening threshold. These are useful failures: **no fixed-basis coil set is promoted. Solved-boundary shaping/single-stage optimization plus REBCO/structural evidence is mandatory.**

The 6 T electron-cyclotron fundamental is ~167.95 GHz, so the nominal 170 GHz ECRH choice passes only a resonance-scale sanity check. 3-D accessibility and deposition remain open.

The target 1,000 MW D-T source corresponds to ~801.14 MW neutron power and ~3.546e20 reactions/neutrons per second before detailed source-spectrum/profile treatment. At TBR=1.15, the blanket must breed at least the equivalent of ~0.1765 kg/day tritium at this continuous target burn rate. Full 3-D Monte Carlo TBR remains open.

The plant target ledger still closes algebraically at **340 MWe** for 1,000 MW fusion, blanket energy multiplier 1.15, 40% gross conversion and 120 MW recirculating load. If one substitutes the uniform 704.57 MW burn screen instead, the same plant assumptions yield only **~204.10 MWe**. This exposes the central coupling: the power plant does not close at the current crude uniform plasma point.

## Current verdict

`EXECUTABLE_SFR1_POC_AND_FULL_DESIGN_INVENTORY__HIGH_FIDELITY_G1_G2_G3_G4_G5_G7_NOT_CLOSED`

That verdict is intentionally not `FUSION_SOLVED`.

## External technical anchors

- DESC 0.17.3: https://pypi.org/project/desc-opt/
- VMEC++: https://github.com/proximafusion/vmecpp
- Helios preconceptual reference: https://arxiv.org/abs/2512.08027
- Bosch-Hale implementation cross-check: https://github.com/fusion-energy/fusion_neutron_utils
