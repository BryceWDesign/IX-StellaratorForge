
# SFR-1 Rev A Reference Reactor Design

## Purpose

SFR-1 Rev A is the first reactor-level architecture of IX-StellaratorForge. Its job is to make the design concrete enough that every major plasma, magnet, blanket, exhaust, thermal, fuel-cycle, maintenance and control decision has an explicit interface and an evidence requirement.

It is intentionally **preconceptual**. Rev A fixes a plant-scale reference envelope and engineering constraints while refusing to fabricate the high-fidelity plasma solution that must occupy that envelope.

## Mission

Design a steady-state D-T stellarator in the ~1 GW fusion-power class that can plausibly progress toward net electric production while preserving the principal stellarator advantage: externally generated steady-state confinement without relying on a large transformer-driven plasma current.

The reactor-level program succeeds only if one core family closes all of the following simultaneously:

- solved finite-beta equilibrium and nested-surface quality;
- trapped-particle and alpha confinement;
- nonlinear heat and particle transport;
- manufacturable HTS coils and supports;
- sufficient blanket/shield space;
- full-3D tritium breeding margin including ports;
- credible steady-state heat and particle exhaust;
- ECRH startup/control with acceptable wall-plug power;
- remote maintainability without routine primary-coil removal;
- cryogenic and thermal conversion closure;
- positive complete-plant power balance;
- robust performance under manufacturing, alignment and operational uncertainty.

## Rev A envelope

The declared numerical envelope is stored in `configs/reactor/sfr1_rev_a.json` and the authority of every number is stored separately in `configs/reactor/parameter_ledger.json`.

The nominal machine scale is `R=8.0 m`, `a=1.7 m`, `B0=6 T`, `β=3%`, and a `1 GW` D-T fusion-power target. These are optimization anchors, not predictions. If high-authority analysis requires a larger machine, lower field, different beta, or a different radial build, the architecture is designed to move rather than to protect the numbers.

## Core family strategy

Rev A deliberately creates a reactor **family** instead of hiding magnetic uncertainty behind one geometry:

- `SFR1_QI_3FP`: 3FP QI/omnigenous candidate motivated by the inherited IX-Fusion low-authority multistart screen.
- `SFR1_QI_PWO_4FP`: 4FP QI-pwO candidate motivated by current reactor-relevant QI work and new direct-orbit optimization.
- `SFR1_C6_QI_6FP`: the historical C6 lineage, retained as a real competitor rather than protected symbolism.
- `SFR1_QA_2FP_REF`: engineering reference forcing QI complexity to earn its place.
- `SFR1_DIRECT_J_SEARCH`: no preselected field-period count; orbit physics may discover a better family.

The first reactor geometry to be called **SFR-1B** must have earned selection by the comparative gate sequence. Rev A will not predeclare it.

## Radial build reservation

Rev A reserves 1.35 m from the plasma reference boundary to the primary coil envelope:

- 0.05 m first-wall/PFC reservation;
- 0.55 m breeding-blanket reservation;
- 0.45 m neutron/gamma shielding reservation;
- 0.10 m vacuum-vessel structural reservation;
- 0.20 m thermal-shield/clearance reservation.

This is a geometric budget, **not** a shielding solution. G7 can expand or redistribute it. A core shape that cannot preserve sufficient local blanket/shield thickness around high-field-side constrictions or ports fails reactor integration even if its plasma metrics are excellent.

## System stack

From plasma outward:

1. D-T plasma and scrape-off/edge region.
2. Divertor/first-wall plasma-facing surfaces.
3. Replaceable breeder/heat-extraction modules.
4. Dedicated neutron/gamma shield where breeder cannot provide sufficient attenuation.
5. Vacuum vessel and structural boundary.
6. Thermal shield and cryogenic clearance.
7. REBCO winding pack and coil case/support network.
8. Cryostat and external plant systems.

The coil topology is not frozen. Modular non-planar coils, mixed encircling/shaping concepts, and other buildable current systems may compete if they respect the IP and evidence ledgers.

## Power target versus power claim

`1,000 MW fusion` is a design target. At that target, D-T reaction kinematics alone imply ~801 MW neutron power and ~199 MW alpha power. A provisional blanket multiplier of 1.15 and 40% gross conversion efficiency produce a screening gross-electric value of 460 MW. If recirculating power reaches the Rev A ceiling of 120 MW, screening net power would be 340 MW.

That arithmetic only says the **plant target is internally worth pursuing**. It does not prove the plasma can produce 1 GW, the blanket multiplier is achievable, 40% conversion is achievable, or that recirculating power can be held below 120 MW.

## Rev A completion definition

Rev A is complete when the architecture is internally consistent, the design ledger is machine-readable, all high-authority unknowns are explicit, and no target is represented as an achieved result. That is the state of this release.
