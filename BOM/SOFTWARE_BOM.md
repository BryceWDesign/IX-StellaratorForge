# IX-StellaratorForge Software BOM

Release: **0.3.0**  
As-of date: **2026-08-16**

## In-repository runtime

| Component | Supported range | Purpose |
|---|---|---|
| Python | >=3.11 | runtime, evidence generation and validation tooling |
| NumPy | >=2.0,<3 | numerical arrays, quadrature and linear algebra |
| Matplotlib | >=3.8,<4 | reproducible review figures inherited from IX-Fusion |

The SFR-1 PoC does not require a cloud service, database, GPU, or network API.

## External high-authority toolchain

These tools are **not bundled** and were **not executable in the v0.3 build runtime**. The versions below are reference versions verified from their primary project release channels as of the release date; every future evidence bundle must record the exact version/build/hash actually used.

| Tool | 2026 reference version | SFR-1 gate / role | Bundled? |
|---|---:|---|---|
| DESC | 0.17.3 | G1 3-D MHD equilibrium/optimization; possible G2 coil objectives | no |
| VMEC++ | 0.7.1 | G1 independent ideal-MHD equilibrium cross-check | no |
| SIMSOPT | 1.10.6 | G2 stellarator coil/field optimization integration | no |
| OpenMC | 0.16.0 | G7 3-D neutron/photon transport, TBR/heating/dose workflows | no |
| SFINCS/KNOSOS-class | pin on execution | G3 neoclassical transport/bootstrap consistency | no |
| guiding-center/direct-J solver | pin on execution | G3 alpha/fast-ion confinement | no |
| GX/stella-class | pin on execution | G4 nonlinear gyrokinetic transport | no |
| 3-D edge/SOL/divertor stack | pin on execution | G5 exhaust/topology/heat flux | no |
| ECRH ray/full-wave stack | pin on execution | G6 propagation/absorption/deposition | no |
| structural FEA stack | pin on execution | G2/G8 coil supports, loads and thermal/structural closure | no |

Primary project references are recorded in `provenance/EXTERNAL_TECHNICAL_BASIS_2026.json`.

## License note

IX-StellaratorForge is distributed under `LicenseRef-IX-StellaratorForge-Eval-Only-1.1`. Third-party software retains its own license and is not redistributed by this repository. This software BOM is descriptive and does not grant rights to third-party tools.
