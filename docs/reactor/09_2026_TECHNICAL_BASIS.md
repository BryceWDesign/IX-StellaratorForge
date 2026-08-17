
# 2026 Technical Basis

This file records the contemporary technical basis used to choose Rev A targets. These sources motivate targets and solver paths; they do not validate SFR-1.

## Integrated stellarator power-plant reference

**Swanson et al., “Overview of the Helios Design: A Practical Planar Coil Stellarator Fusion Power Plant,” arXiv:2512.08027 (2025/2026 revision).**

Relevant reference values include an 8 m major radius, 6 T on-axis field, 20 K HTS coils, 20 T maximum on-coil field, 1.2 m minimum plasma-to-coil distance, ~960 MW fusion power, 40% thermal conversion target, full plant integration, tritium breeding/blanket design, divertor, maintenance and control. IX-StellaratorForge uses these as a comparison point, not as copied performance evidence.

Source: https://arxiv.org/abs/2512.08027

## Reactor-relevant QI reference

**Sánchez et al., “CIEMAT-QI4X: a reactor-relevant quasi-isodynamic stellarator configuration compatible with an island divertor,” arXiv:2512.08825.**

Provides a four-field-period QI reference with low transport, good fast-ion confinement, small bootstrap current, a finite-beta edge island chain and a corresponding coil set. It motivates keeping a 4FP QI branch alive.

Source: https://arxiv.org/abs/2512.08825

## Direct trapped-orbit optimization

**Chen et al., “Direct Optimization of Stellarator Omnigenity from the Second Adiabatic Invariant,” arXiv:2608.02418.**

Demonstrates differentiable direct-J optimization in DESC and motivates replacing reduced bounce proxies with orbit-action authority.

Source: https://arxiv.org/abs/2608.02418

## QI + piecewise omnigenity

**Velasco et al., “Combination of quasi-isodynamic and piecewise omnigenous magnetic fields,” arXiv:2603.12377.**

Motivates relaxing high-field-side QI structure when that improves engineering freedom without automatically sacrificing the neoclassical advantages sought from QI.

Source: https://arxiv.org/abs/2603.12377

## Coil feasibility during plasma optimization

**Yu et al., “Quasi-single-stage optimization for advanced stellarators,” arXiv:2608.03122.**

Motivates preventing a plasma boundary from winning before coil feasibility is considered.

Source: https://arxiv.org/abs/2608.03122

## Coil/support co-optimization

**Fu & Kaptanoglu, “Towards joint optimization of stellarator coils and support structures,” arXiv:2607.05749.**

Motivates joint electromagnetic/structural design rather than post-hoc support engineering.

Source: https://arxiv.org/abs/2607.05749

## REBCO strain optimization

**Huslage et al., “Strain Optimization for ReBCO High-Temperature Superconducting Stellarator Coils in SIMSOPT,” arXiv:2409.01925.**

Motivates treating REBCO tape orientation, binormal curvature and torsion as optimization constraints.

Source: https://arxiv.org/abs/2409.01925

## Solver stack

- DESC — 3-D MHD equilibrium and differentiable optimization: https://github.com/PlasmaControl/DESC
- SIMSOPT — stellarator coil/field/optimization framework: https://github.com/hiddenSymmetries/simsopt
- VMEC++ — independent VMEC implementation and validation path: https://github.com/proximafusion/vmecpp
- Raytrax — JAX ECRH ray tracing: https://github.com/proximafusion/raytrax
- OpenMC — continuous-energy Monte Carlo particle transport: https://github.com/openmc-dev/openmc
- OpenMC ecosystem — DAGMC, ParaStell, Stellarmesh, fusion benchmarks and CAD tooling: https://github.com/openmc-dev/openmc-ecosystem

## Interpretation rule

Published feasibility of a method, material regime or reference reactor does not transfer its evidence to SFR-1. SFR-1 must produce its own solver inputs, outputs, convergence evidence, uncertainty campaign and matched comparison before promotion.
