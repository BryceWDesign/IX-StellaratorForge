# Execution Sequence

## Phase A — Seed league, no winners

1. Import 3FP, 4FP, 6FP and QA reference families plus unconstrained direct-J seeds.
2. Apply only cheap rejection filters: self-intersection, extreme curvature, obvious spectral/engineering pathologies.
3. Keep the original C6 seed and its matched controls as lineage tests.

## Phase B — Equilibrium truth

4. Solve each survivor with DESC at vacuum and finite pressure.
5. Cross-check selected survivors with VMEC++/VMEC-class equilibrium.
6. Reject candidates that require prescribed transform behavior not produced self-consistently.
7. Use multistart/deflation rather than trusting one local minimum.

## Phase C — Direct orbit + coil co-design

8. Replace the reduced bounce proxy with direct trapped-particle action / second-adiabatic-invariant objectives.
9. Build explicit coil sets and optimize boundary+coils in a single/quasi-single-stage loop.
10. Include stochastic coil perturbations, minimum clearances, curvature, REBCO strain, support stress, and vessel access.
11. Run FIRM3D/SIMSOPT-class fast-particle loss campaigns.

## Phase D — turbulence, fueling, finite-beta stability

12. Evaluate nonlinear turbulent heat **and particle** flux with GX; cross-check finalists with stella/GENE-class tools when feasible.
13. Optimize mirror-ratio / max-J / particle-pinch trade space rather than assuming lower heat flux is enough.
14. Evaluate profile evolution and finite-beta stability; candidates must survive realistic pressure/current variations.

## Phase E — edge, RF, neutronics

15. Co-design divertor topology and vessel while preserving coil access/maintenance clearance.
16. Replace RF purity with 3-D deposition/absorption/steering control and recirculating-power metrics.
17. Instantiate CAD-neutronics geometry and optimize blanket/shield radial build, penetrations, and coil nuclear heating.

## Phase F — system verdict

18. Run uncertainty campaigns across manufacturing errors, equilibrium/profile uncertainty, actuator faults, material properties, and model discrepancy.
19. Compare every survivor against matched conventional baselines using hard gates plus a Pareto front; do not collapse all physics into one weighted scalar.
20. Promote only if the high-authority evidence bundle demonstrates an advantage that persists after engineering and uncertainty penalties.
