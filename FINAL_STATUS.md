# IX-StellaratorForge v0.5.0 — SFR-2 assumption-breaker integration

## Current repository verdict

`GREEN` means the preserved SFR-1 v0.4 evidence and the new SFR-2 Rev A low-authority study reproduce from committed inputs and code.

It does **not** mean fusion, ignition, net energy, net electricity, dynamic MHD stability, a buildable high-field magnet, tritium self-sufficiency, or hardware operation has been demonstrated.

## What v0.5.0 adds

v0.5.0 preserves SFR-1 Rev A unchanged as the steady-state reference program and adds **SFR-2 Rev A** as a separate assumption-breaker candidate.

SFR-2 encodes the user-specified `23 / 26 / 23 / 26 ft` pattern as four consecutive sectors of **one closed toroidal plasma system**. It does not model four independent plasma machines connected by ducts.

The new implementation includes:

- deterministic 23/26/23/26 geometry bookkeeping;
- an explicit 4.5 aspect-ratio circular-torus screening proxy;
- Bosch-Hale D-T reactivity;
- an ideal monatomic radial-compression upper-bound with no magnetic-field amplification credit;
- ISS04 confinement sensitivity to axis field and rotational transform;
- a target-power-matched 1 GW comparison so compression cases are not rewarded merely for producing more fusion power in an unconstrained uniform model;
- zero numerical credit for unmodeled RF resonance, magnetic pumping, traveling-wave phase heating, or flux-compression field gain;
- SFR2-G0 through SFR2-G9 promotion gates;
- reproducibility tests and tracked JSON/Markdown results.

## Primary SFR-2 result

The primary screen is defined as:

- `H_ISS04 = 1.0`;
- no assumed transient confinement penalty;
- axis-field sweep: 6, 8, 10, 12, 15 T;
- `iota(2/3)` sweep: 0.6, 0.7, 0.8, 0.9;
- radial squeeze: 0%, 5%, 10%;
- each case solved for the base beta that makes the uniform compressed state equal the same 1,000 MW fusion-power target.

**Result:** `NO_PRIMARY_CASE_CROSSES_OPTIMISTIC_IGNITION_PROXY`.

The strongest primary point is the **uncompressed** 15 T / `iota=0.9` case. Its ISS04-to-alpha-only required confinement ratio is approximately **0.9611**, corresponding to an `H_ISS04` requirement of approximately **1.0405** in this optimistic screen.

That is **not “3.9% away from fusion”**. It means only that the empirical confinement estimate is about 3.9% below the deliberately optimistic alpha-only balance for that low-authority point.

## Important negative result: compression is not automatically beneficial

The updated implementation corrects the earlier conversational exploration.

At fixed 1 GW target power and `H_ISS04=1`, radial compression increases density and temperature but shrinks the minor radius. In ISS04 this confinement-size penalty dominates the first-order benefit for the declared SFR-2 scan:

- 0% squeeze, 15 T, `iota=0.9`: ratio ~0.9611;
- 5% squeeze: ratio ~0.8885;
- 10% squeeze: ratio ~0.8164.

Therefore v0.5.0 does **not** claim the traveling-compression idea improves ignition likelihood. Dynamic compression remains scientifically open because ISS04 is not a dynamic-MHD model and the repository gives phase-controlled heating zero numerical credit.

## Magnetic-rifling sensitivity

Within ISS04 only, increasing `iota(2/3)` improves the confinement proxy. At 15 T and no compression, the target-power-matched ratios rise monotonically from about 0.814 at `iota=0.6` to about 0.961 at `iota=0.9`.

This does not prove that an ABAB 3-D equilibrium with `iota=0.9` exists or is stable. Magnetic islands, stochasticity, coil feasibility and transport remain unresolved.

## Favorable sensitivity is not earned performance

The repository also evaluates `H_ISS04 = 1.2` and `1.4` as sensitivity variables. Some favorable cases cross the low-authority proxy. Those are **scenario studies only** and cannot be quoted as achieved SFR-2 confinement.

## SFR-1 status is preserved

All v0.4 SFR-1 evidence remains intact:

- 87-row system design inventory;
- finite-pressure DESC/VMEC++ seed pack;
- rejected low/intermediate coil architectures retained as negative evidence;
- HTS geometry-only screens;
- TBR coverage bounds and OpenMC execution path;
- conditional plant thresholds;
- all high-authority production-solver and hardware gates still open where evidence is absent.

v0.5.0 does not rewrite SFR-1 history to make SFR-2 look successful.

## SFR-2 authority jumps still required

1. Dynamic finite-beta ABAB equilibrium.
2. Coil/current solution and high-field structural/strain/quench feasibility.
3. Thermal and alpha-particle orbit confinement through the actuation cycle.
4. Neoclassical/bootstrap, gyrokinetic/profile transport, island/stochastic and ideal/resistive MHD assessment.
5. 3-D edge/divertor transient heat-flux closure.
6. Real RF/wave deposition and phase-control calculation.
7. Full 3-D neutronics/TBR/shielding.
8. Integrated burn/thermal/plant calculation using G1–G7 outputs.
9. Physical hardware evidence.

The repository explicitly keeps SFR2-G1 through SFR2-G9 at `NOT_RUN`.
