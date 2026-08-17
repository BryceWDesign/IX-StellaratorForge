# Production solver handoff

v0.4 makes the next work executable without pretending it was run in the release build environment.

## Order

1. Run DESC on each fixed-NFP seed.
2. Discard non-converged/poor-force-balance configurations.
3. Cross-check finalists in VMEC++.
4. Replace fixed-boundary coil fitting with equilibrium/coil co-design in DESC/SIMSOPT-class tooling, then REBCO winding-pack and structural FEA.
5. Run energetic-particle/direct-J and neoclassical evidence, followed by nonlinear gyrokinetics/profile iteration.
6. Solve edge/divertor and RF deposition.
7. Generate full 3-D reactor CAD/DAGMC geometry and run OpenMC TBR/heating/dose/DPA/streaming.
8. Import all production outputs into the plant ledger and close uncertainty-aware net electric power.
9. Hardware remains a separate authority.

## Fail-closed rule

Every supplied adapter exits with an error if its real dependency is absent. The project does not have a compatibility mode that relabels the in-repo reduced physics as DESC, VMEC++, OpenMC, gyrokinetics or FEA.

## Windows host

The repository itself is cross-platform Python. The high-fidelity science stack should be run in a supported Linux environment (for a Windows workstation, WSL2 or a Linux container/VM is the intended route) because production fusion tools do not all provide native Windows support.
