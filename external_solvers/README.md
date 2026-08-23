# IX-StellaratorForge production-solver execution pack

This directory is an **execution bridge**, not prefilled evidence.

## SFR-4 integrated campaign

`sfr4_integrated_evidence_contract.json` defines nine fail-closed promotion gates spanning physical coils, cross-code equilibrium, stability, particle transport, three-dimensional island-divertor exhaust, thermal/structural qualification, OpenMC neutronics, integrated burn/plant analysis and hardware. v0.9 explicitly attempted the DESC, VMEC++ and OpenMC adapters; all stopped because the production dependencies are absent.

## Dual Boundary AHIS

`sfr3_dual_boundary_evidence_contract.json` defines the evidence needed to replace the v0.8 1-D thermal and deterministic fault screen: coupled CAD thermal/EM/structural analysis, W/RAFM joint and fatigue qualification, PbLi/coolant MHD and corrosion loops, sensor irradiation/calibration, quantified interspace leak testing, full 3-D neutronics and integrated representative hardware. No reduced-screen pass may be promoted into survivability, safety or confinement evidence.

## SFR-3 field integrity

`sfr3_field_integrity_evidence_contract.json` defines the high-authority path that must replace the v0.7 analytic response matrix: CAD-linked magnetic response, free-boundary equilibrium and islands, particle/alpha orbits, coupled magnet engineering and full 3-D neutronics. No missing output may be replaced by the synthetic controllability pass.

## G1 equilibrium

Inputs in `inputs/` are generated from the exact analytic SFR-1 reduced boundary and contain finite-pressure/flux/iota design seeds.

Example once the real tools are installed:

```bash
python external_solvers/adapters/run_desc_equilibrium.py \
  external_solvers/inputs/input.SFR1_QI_3FP \
  --output external_results/desc/SFR1_QI_3FP.h5 \
  --receipt external_results/desc/SFR1_QI_3FP.receipt.json

python external_solvers/adapters/run_vmecpp_equilibrium.py \
  external_solvers/inputs/input.SFR1_QI_3FP \
  --wout external_results/vmecpp/wout_SFR1_QI_3FP.nc \
  --receipt external_results/vmecpp/SFR1_QI_3FP.receipt.json
```

A receipt is not an automatic pass. Force balance, geometry, beta/iota, stability and cross-code acceptance criteria still apply.

## G7 OpenMC

`build_openmc_axisymmetric_proxy.py` constructs an **axisymmetric CSG torus proxy** and can optionally run it. Its TBR result is useful for material/nuclear-data sensitivity only and cannot close G7.

The final 3-D workflow must import solved stellarator/vessel/blanket/divertor/port geometry through a validated CAD/DAGMC/ParaStell-class path and tally tritium production plus heating/damage/streaming. `analyze_openmc_3d_tbr.py` analyzes a named `(n,Xt)` tally from a real statepoint and applies conservative `mean - 2 sigma` floor/target checks.

## Dependencies

`requirements-high-fidelity.txt` records the current pinned MHD/coil Python tools used by this release contract. OpenMC and kinetic/gyrokinetic tools require their own supported Linux/WSL/container environments.

**No adapter substitutes an in-repo surrogate when its production dependency is missing.**
