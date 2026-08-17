# IX-Fusion vNext Scientific Thesis

## Decision

IX-Fusion v0.1.0 should not be extended by adding more weight terms to its reduced C6 objective. Its principal scientific weakness is upstream: the candidate boundary, rotational-transform profile, bounce-action proxy, engineering penalty, and RF purity layer are not yet self-consistent outputs of reactor-relevant plasma, coil, edge, and wave physics.

vNext therefore changes the problem from **"optimize C6"** to **"run an evidence-gated tournament among magnetic/engineering families and allow C6 to survive or die."**

## Five architectural corrections

1. **Field-period count becomes a discrete design variable.** 3FP, 4FP, 6FP, a 2FP QA engineering reference, and an unconstrained direct-orbit branch enter the same promotion system.
2. **Direct orbit physics replaces the bounce proxy at the first serious confinement gate.** The second adiabatic invariant / trapped-particle action is the governing quantity; reduced surrogates may only reject cheaply, never promote.
3. **Coils and supports enter before a magnetic configuration may win.** Coil-plasma distance, normal-field error, REBCO strain, structural stress, stochastic manufacturing errors, vessel access, and maintenance geometry are co-objectives or hard constraints.
4. **Turbulent particle transport is a first-class objective.** Heat flux alone is insufficient. Mirror ratio, inward/outward particle flux, density peaking, impurity behavior, and profile evolution must be evaluated.
5. **The RF layer is rewritten around deposition controllability.** Source phase/frequency synchronization remains legitimate controls infrastructure, but a spatial-array purity number is not accepted as plasma-coupling evidence. ECRH heating/control must be evaluated with 3-D ray/full-wave deposition models and recirculating-power accounting.

## Leading design hypothesis

The leading *research direction*, not a winner, is a **QI / QI-pwO stellarator family with direct-J optimization, coil-aware boundary optimization, stochastic HTS coil/support co-design, particle-transport-aware turbulence optimization, and edge/vessel co-design**. Pure QI is retained as a control because QI-pwO's value must be demonstrated rather than assumed.

## Current scientific verdict

**NOT YET A FUSION-PERFORMANCE CANDIDATE.**

The vNext package is an architecture and falsification upgrade. High-authority equilibrium, coil, orbit, turbulence, edge, RF, neutronics, and system results are not present in this runtime and are never fabricated.
