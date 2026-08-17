# 2026 External Evidence Map

Access date for this research pass: 2026-08-16/17.

## Magnetic optimization

- Chen et al., *Direct Optimization of Stellarator Omnigenity from the Second Adiabatic Invariant*, arXiv:2608.02418. Direct differentiable optimization of trapped-particle action; used here to justify replacing IX-Fusion's reduced bounce proxy at the serious orbit gate.
- Velasco et al., *Combination of quasi-isodynamic and piecewise omnigenity*, arXiv:2603.12377. Used to define a QI-pwO branch rather than assuming strict QI is always the best engineering compromise.
- Yu et al., *Quasi-single-stage optimization for advanced stellarators*, arXiv:2608.03122. Used to require coil feasibility during boundary optimization.
- Gil et al., *Stochastic single-stage stellarator optimization using fixed-boundary equilibria*, arXiv:2603.11699. Used to place manufacturing/error robustness inside optimization rather than after it.
- Fu & Kaptanoglu, *Towards joint optimization of stellarator coils and support structures*, arXiv:2607.05749. Used to elevate support stress to a co-design variable.

## Transport and fast particles

- Bañón Navarro et al., *Optimizing Particle Transport for Enhanced Confinement in Quasi-Isodynamic Stellarators*, arXiv:2507.21003. Used to require particle transport and mirror-ratio sensitivity, not only heat transport.
- Plunk et al., *Enhanced performance in quasi-isodynamic max-J stellarators with a turbulent particle pinch*, arXiv:2507.19319 (2026 revision). Used to motivate a self-fueling / inward-pinch branch and profile-evolution checks.
- Paul et al., *FIRM3D: Fast ion reduced models in 3D*, arXiv:2605.16734. Used as an open energetic-particle transport route.
- Kim et al., *Optimization of Nonlinear Turbulence in Stellarators*, arXiv:2310.18842 / JPP. Establishes the DESC+GX nonlinear turbulence-in-loop pattern used by the vNext protocol.

## Edge and exhaust

- Veksler et al., *Stellarator island divertor shape optimization for reduced peak heat fluxes*, arXiv:2602.24049. Used to make divertor geometry an optimization problem with uncertainty/robustness rather than a late drawing exercise.
- Giuliani et al., *Divertor topology and vacuum vessel design for stellarators*, arXiv:2607.27127. Used to require joint edge-topology/vessel/coil-clearance design.

## RF / heating

- Max Planck Institute for Plasma Physics, HiPMiB announcement, 2026-07-27. W7-X program is developing 2 MW gyrotrons and 2 MW transmission as a reactor-relevant ECRH technology step.
- Proxima Fusion `raytrax`: JAX-based ECRH ray tracing. Used as a model-based deposition-control path.

## Open solver stack

- DESC v0.17.3 (2026-07-31): differentiable 3-D MHD equilibrium/optimization.
- SIMSOPT v1.10.6 (2026-02-10): stellarator coil/field/optimization framework.
- Proxima Fusion VMEC++: current open C++/Python VMEC reimplementation.
- OpenMC ecosystem: DAGMC/CAD conversion, Paramak, ParaStell, Stellarmesh, plasma-source and fusion benchmark tooling for neutronics/CAD workflows.

## Interpretation rule

These sources establish available methods and research directions. They do **not** validate an IX-Fusion design. A vNext candidate becomes evidence only after the corresponding solver run, provenance bundle, uncertainty campaign, and matched comparison exist.
