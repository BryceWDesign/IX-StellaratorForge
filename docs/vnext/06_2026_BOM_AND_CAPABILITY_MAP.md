# 2026 BOM and Capability Map

This is a **research/development capability BOM**, not an operational fusion-reactor construction procedure.

## Computational layer — obtainable now

| Capability | Current route | vNext use |
|---|---|---|
| 3-D MHD equilibrium / differentiable optimization | DESC 0.17.3 | primary equilibrium/optimization branch |
| Independent equilibrium cross-check | VMEC++ / VMEC-class | cross-code equilibrium validation |
| Coil/field optimization | SIMSOPT 1.10.6 | explicit coils, fields, errors, geometry |
| Direct energetic-particle transport | FIRM3D | fusion-born fast-ion loss / orbit diagnostics |
| Nonlinear gyrokinetics | GX; stella cross-check | heat + particle turbulent flux |
| ECRH ray/deposition | Raytrax plus independent ray/full-wave tools | deposition controllability, steering robustness |
| 3-D neutronics | OpenMC + DAGMC/ParaStell/Stellarmesh ecosystem | coil heating, shielding, radial build, penetrations |
| Structural optimization | coil-fem / conventional FEA cross-check | coil/support stress and displacement |

## Magnet materials — commercially real research inputs

REBCO/2G-HTS tape is commercially available from multiple suppliers. SuperPower's published current specifications include widths from 2 to 12 mm, typical piece lengths of 200–500 m with longer pieces possible depending on specification, multiple copper-stabilizer options, and published mechanical/critical-current data. Fujikura also markets rare-earth HTS tape specifically toward fusion-magnet applications and announced an additional production-capacity expansion in February 2026.

These facts justify REBCO as a **real material branch**, not a claim that any particular stellarator coil is already qualified. Final conductor selection must be made from measured Ic(B,T,angle), strain, joint, irradiation, quench/protection, manufacturability, and cost data for the actual coil geometry.

## Subscale validation instrumentation inherited from the repo set

- magnetic-field mapping / Hall-probe arrays;
- fiber-optic or conventional strain/temperature sensing;
- electrical/thermal telemetry and calibrated energy accounting;
- structural-health / impedance / guided-wave channels where physically applicable;
- deterministic DAQ, run manifests, hashes, fault injection, and replay.

## Deliberately not frozen yet

- blanket breeding material and coolant;
- first-wall/divertor material stack;
- reactor-scale cryoplant;
- gyrotron count/frequency/power;
- plasma dimensions / field strength;
- coil current / winding pack;
- tritium plant;
- net-electric conversion cycle.

Freezing those before G1–G5 would create false precision. They become BOM items only when a promoted equilibrium/coil/edge geometry supplies the loads and spatial constraints they must satisfy.
