# IX-StellaratorForge v0.9.0: Integrated Physical Promotion and Heat Exhaust

## Bottom line

All seven requested computational workstreams were attempted. The executable reduced campaign completed, but the result is not a fusion promotion.

The heat architecture passes its declared nominal and steady screening envelope. The scanned physical coil family fails.

Top-level verdict:

`INTEGRATED_REDUCED_CAMPAIGN_COMPLETE__NOMINAL_HEAT_ENVELOPE_SCREEN_PASS__PHYSICAL_COIL_EQUILIBRIUM_CONFINEMENT_AND_FUSION_UNPROVEN`

## What passed

The selected heat architecture separates distributed first-wall heat, concentrated divertor exhaust and blanket neutron heat. At the declared 1 GW fusion target and Q=20 ledger:

* first-wall peak heat flux: approximately 0.294 MW/m2;
* divertor peak heat flux: approximately 5.724 MW/m2;
* nominal first-wall tungsten surface: approximately 401.2 C;
* first-wall surface at the declared 1 MW/m2 steady upper bound: approximately 523.8 C;
* divertor tungsten surface: approximately 678.3 C;
* divertor water flow: approximately 426.0 kg/s through 960 parallel channels;
* mean channel velocity: approximately 7.56 m/s; and
* hydraulic pumping screen: approximately 0.122 MW.

The selected requirements are a helium-cooled segmented-W/graded-W-RAFM/ODS-RAFM first wall, isolated PbLi DCLL blanket, and a separately bounded water-cooled W/OFHC-Cu/CuCrZr divertor. The water and PbLi systems never share a boundary, penetration or heat exchanger.

This resolves the nominal and declared steady heat allocation only at reduced-model authority. Stable detachment, the 3-D island footprint, critical heat flux, boiling stability, erosion, cyclic fatigue, irradiation, disruptions, accidents and hardware qualification remain unproven.

## What failed

Eighty direct-filament Biot-Savart coil configurations were executed. Zero pass both the transform and radial-excursion gates. The best declared scoring case reaches approximately 0.0653 mean iota against a minimum 0.25 requirement. The richer held-out normal-field reconstruction is approximately 6.49% RMS against a 0.5% screen.

The classical scanned helical family is rejected. Increasing its current did not solve the missing transform without violating other field-quality requirements.

## What could not run

DESC, VMEC++, SIMSOPT, OpenMC, kinetic transport, CAD, CFD and structural FEA are unavailable in this runtime. The DESC, VMEC++ and OpenMC adapters were explicitly invoked and stopped with exit code 1. The dependency-installation route was attempted and blocked by runtime network policy. No surrogate output was relabeled as production evidence.

## Remaining scientific result

The 3.5 MeV alpha gyroradius scale is approximately 0.0449 m at 6 T, but no alpha retention is credited. The Q=20 design-iota burn requirement, including the declared alpha-deposition and bremsstrahlung assumptions, requires approximately H_ISS04 2.00. That target cannot be assigned to the failed physical coil family.

Earned improvement toward demonstrated confinement, ignition or fusion remains exactly **0.00%**.

The useful advance is narrower and real: the repository now has an executable heat-exhaust requirement and a stronger rejection of an inadequate magnet family. The next design action is a fundamentally different nonplanar modular-coil optimization, not another increase in current through the rejected helices.
