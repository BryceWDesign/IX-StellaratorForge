# SFR-1 Full System BOM — Design Inventory

## What "full BOM" means in this repository

This is the **complete system-category bill of materials for the SFR-1 reference reactor
architecture**. It is intended to ensure that no reactor subsystem disappears from the design
because it is inconvenient to model.

It is **not** a fabrication/procurement BOM. Quantities, final dimensions, conductor current,
material grades, nuclear-material composition/enrichment, tritium inventories, pressure
ratings, safety set-points, part numbers, vendors, and construction drawings remain gated by
high-fidelity physics, engineering review, regulation, and licensing. Those details must not
be inferred from this document.

Maturity labels:

- `DEFINED` — subsystem role and interfaces are defined.
- `CANDIDATE` — technology family selected for comparison, not frozen.
- `SOLVER_DEPENDENT` — final choice/size requires the named analysis gate.
- `HARDWARE_DEPENDENT` — cannot be qualified by repository computation alone.

| ID | System | Required component / technology family | Current SFR-1 basis | Maturity | Governing gate |
|---|---|---|---|---|---|
| C01 | Plasma core | 3-D magnetic equilibrium | 3FP/4FP/6FP QI-family + QA reference + direct-J branch | SOLVER_DEPENDENT | G1 |
| C02 | Plasma core | pressure/current/iota profiles | finite-beta profile family, no profile frozen | SOLVER_DEPENDENT | G1/G3/G4 |
| C03 | Plasma core | separatrix/LCFS definition | equilibrium-derived | SOLVER_DEPENDENT | G1/G5 |
| C04 | Plasma core | impurity/helium-ash model | transport-coupled | SOLVER_DEPENDENT | G3/G4/G5 |
| M01 | Magnets | primary stellarator field coils | modular/helical/planar candidates may compete | SOLVER_DEPENDENT | G2 |
| M02 | Magnets | shaping / trim coils | required if core/coil co-design selects them | SOLVER_DEPENDENT | G2 |
| M03 | Magnets | REBCO winding pack | coated-conductor family | CANDIDATE | G2 |
| M04 | Magnets | winding insulation / turn separation | cryogenic radiation-compatible system | CANDIDATE | G2/G7 |
| M05 | Magnets | coil cases | structural metallic/composite case family | SOLVER_DEPENDENT | G2 |
| M06 | Magnets | inter-coil support structure | jointly optimized support network | SOLVER_DEPENDENT | G2 |
| M07 | Magnets | current leads | HTS/resistive transition architecture | CANDIDATE | G2/G8 |
| M08 | Magnets | joints / demountable interfaces | candidate only where maintenance value justifies loss | CANDIDATE | G2/G8 |
| M09 | Magnets | quench detection | distributed voltage/temperature/field sensing | HARDWARE_DEPENDENT | G2/G9 |
| M10 | Magnets | energy extraction / dump | independent protection path | SOLVER_DEPENDENT | G2/G9 |
| CR01 | Cryogenic | magnet cryostat | common or segmented vacuum cryostat | CANDIDATE | G2/G8 |
| CR02 | Cryogenic | thermal shields | staged radiation/thermal intercepts | DEFINED | G2/G8 |
| CR03 | Cryogenic | cryocooler/refrigeration plant | 20 K-class magnet refrigeration architecture | SOLVER_DEPENDENT | G8 |
| CR04 | Cryogenic | cryogenic distribution | supply/return headers, isolation, instrumentation | SOLVER_DEPENDENT | G8/G9 |
| VV01 | Vacuum | plasma vacuum vessel | 3-D vessel conformal to selected core | SOLVER_DEPENDENT | G1/G5/G7 |
| VV02 | Vacuum | vessel support | gravity/EM/seismic/thermal support | SOLVER_DEPENDENT | G2/G7/G9 |
| VV03 | Vacuum | pumping | high-vacuum pumping train and roughing system | CANDIDATE | G5/G8 |
| VV04 | Vacuum | isolation valves | service/maintenance segmentation | CANDIDATE | G8/G9 |
| PFC01 | PFC | first-wall armour | tungsten-family plasma-facing surface | CANDIDATE | G5/G7 |
| PFC02 | PFC | first-wall heat sink | high-heat-flux substrate/cooling structure | SOLVER_DEPENDENT | G5/G8 |
| PFC03 | PFC | divertor targets | replaceable high-heat-flux targets | SOLVER_DEPENDENT | G5 |
| PFC04 | PFC | divertor pumping structure | neutral exhaust and pumping interface | SOLVER_DEPENDENT | G5 |
| PFC05 | PFC | erosion/deposition monitoring | spectroscopy + surface/thermal diagnostics | CANDIDATE | G5/G9 |
| BL01 | Blanket | breeding zone | lithium-bearing breeder/multiplier candidate; exact composition TBD | SOLVER_DEPENDENT | G7 |
| BL02 | Blanket | structural matrix | low-activation structural-material family | SOLVER_DEPENDENT | G7/G8 |
| BL03 | Blanket | coolant passages | geometry selected by thermal/neutronic optimization | SOLVER_DEPENDENT | G7/G8 |
| BL04 | Blanket | neutron/gamma shield | layered shield selected by transport optimization | SOLVER_DEPENDENT | G7 |
| BL05 | Blanket | reflector/multiplier regions | optional, neutronics-selected | SOLVER_DEPENDENT | G7 |
| BL06 | Blanket | replaceable blanket modules | remote-maintainable sector/module architecture | DEFINED | G7/G8/G9 |
| BL07 | Blanket | penetrations / port shielding | streaming-aware local shielding | SOLVER_DEPENDENT | G7 |
| FC01 | Fuel cycle | deuterium supply/conditioning | plant fuel-cycle subsystem | CANDIDATE | G8/G9 |
| FC02 | Fuel cycle | tritium processing | closed accountable processing architecture | SOLVER_DEPENDENT | G7/G8/G9 |
| FC03 | Fuel cycle | breeder extraction interface | blanket-specific extraction technology | SOLVER_DEPENDENT | G7/G8 |
| FC04 | Fuel cycle | isotope separation / cleanup | process-system candidate | SOLVER_DEPENDENT | G8/G9 |
| FC05 | Fuel cycle | pellet fueling | core D/T pellet injection architecture | CANDIDATE | G3/G4/G8 |
| FC06 | Fuel cycle | edge gas fueling | controlled edge fueling | CANDIDATE | G4/G5 |
| H01 | Heating | ECRH sources | 170-GHz-class gyrotron architecture at 6 T screening field | CANDIDATE | G6 |
| H02 | Heating | RF transmission | evacuated/quasi-optical transmission family | SOLVER_DEPENDENT | G6/G8 |
| H03 | Heating | launchers | equilibrium-selected launcher geometry | SOLVER_DEPENDENT | G6 |
| H04 | Heating | beam diagnostics/protection | arc/reflection/power monitoring | DEFINED | G6/G9 |
| D01 | Diagnostics | magnetic diagnostics | field, flux and coil-state measurements | DEFINED | G1/G2/G9 |
| D02 | Diagnostics | density diagnostics | interferometry / reflectometry candidates | CANDIDATE | G3/G4/G9 |
| D03 | Diagnostics | temperature diagnostics | Thomson/ECE/spectroscopic candidates | CANDIDATE | G3/G4/G9 |
| D04 | Diagnostics | neutron diagnostics | source-rate/profile monitoring | CANDIDATE | G7/G9 |
| D05 | Diagnostics | divertor/first-wall thermography | high-speed thermal monitoring | DEFINED | G5/G9 |
| D06 | Diagnostics | structural health monitoring | strain/temperature/vibration/displacement/leak sensing | DEFINED | G2/G9 |
| CT01 | Controls | plasma supervisory control | model-based supervisory layer | DEFINED | G6/G9 |
| CT02 | Controls | independent machine protection | independent fast protection/interlock layer | DEFINED | G9 |
| CT03 | Controls | timing/data acquisition | deterministic timing + synchronized acquisition | CANDIDATE | G9 |
| CT04 | Controls | evidence/provenance recorder | immutable/replayable run evidence | DEFINED | all |
| TH01 | Heat transport | primary blanket coolant loop | helium reference; alternatives remain open | CANDIDATE | G7/G8 |
| TH02 | Heat transport | primary pumps/compressors | coolant-specific | SOLVER_DEPENDENT | G8 |
| TH03 | Heat transport | intermediate heat exchanger | isolates nuclear primary from power block | CANDIDATE | G8 |
| TH04 | Heat transport | decay-heat removal | independent shutdown heat-removal path | DEFINED | G8/G9 |
| PC01 | Power conversion | turbine cycle | indirect sCO2 Brayton vs steam Rankine comparison | CANDIDATE | G8 |
| PC02 | Power conversion | generator | grid-scale synchronous/generator architecture | SOLVER_DEPENDENT | G8 |
| PC03 | Power conversion | condenser/heat rejection | site/cycle-dependent | SOLVER_DEPENDENT | G8 |
| EL01 | Electrical | magnet power supplies | controlled DC supplies | SOLVER_DEPENDENT | G2/G8 |
| EL02 | Electrical | RF electrical plant | gyrotron/modulator auxiliary power | SOLVER_DEPENDENT | G6/G8 |
| EL03 | Electrical | plant distribution | normal and safety-related distribution | SOLVER_DEPENDENT | G8/G9 |
| EL04 | Electrical | emergency/ride-through power | independent shutdown/protection power | DEFINED | G9 |
| RH01 | Maintenance | remote handling manipulators | activated-component remote handling | CANDIDATE | G8/G9 |
| RH02 | Maintenance | blanket/divertor transfer | shielded transfer / service tooling | SOLVER_DEPENDENT | G8/G9 |
| RH03 | Maintenance | inspection tooling | remote NDE/visual/metrology | CANDIDATE | G9 |
| SF01 | Safety | tritium confinement boundaries | multiple static/dynamic barriers | DEFINED | G8/G9 |
| SF02 | Safety | vacuum/pressure relief | analyzed relief/isolation architecture | SOLVER_DEPENDENT | G8/G9 |
| SF03 | Safety | fire detection/suppression | facility hazard-dependent | CANDIDATE | G9 |
| SF04 | Safety | radiation monitoring | area/process/personnel monitoring | DEFINED | G7/G9 |
| SF05 | Safety | confinement/ventilation | filtered pressure-zoned confinement | SOLVER_DEPENDENT | G9 |
| FAC01 | Facility | biological shielding | site and transport-calculation dependent | SOLVER_DEPENDENT | G7/G9 |
| FAC02 | Facility | reactor hall / foundations | seismic, EM and maintenance-load dependent | SOLVER_DEPENDENT | G9 |
| FAC03 | Facility | hot cell / activated maintenance | maintenance strategy dependent | SOLVER_DEPENDENT | G8/G9 |
| FAC04 | Facility | cooling-water / heat-rejection interface | site-specific | SOLVER_DEPENDENT | G8/G9 |
| SW01 | Software | MHD equilibrium | DESC + VMEC++ cross-check | CANDIDATE | G1 |
| SW02 | Software | coil optimization | SIMSOPT / DESC coil tools / independent checks | CANDIDATE | G2 |
| SW03 | Software | neoclassical transport | SFINCS/KNOSOS-class solver | CANDIDATE | G3 |
| SW04 | Software | energetic particles | guiding-center / alpha-orbit solver | CANDIDATE | G3 |
| SW05 | Software | gyrokinetic turbulence | GX/stella-class nonlinear solver | CANDIDATE | G4 |
| SW06 | Software | edge/divertor | 3-D edge/SOL/divertor toolchain | SOLVER_DEPENDENT | G5 |
| SW07 | Software | ECRH propagation/deposition | ray/full-wave toolchain | SOLVER_DEPENDENT | G6 |
| SW08 | Software | neutronics | OpenMC + CAD/DAGMC/ParaStell-class geometry workflow | CANDIDATE | G7 |
| SW09 | Software | structural FEA | nonlinear EM/structural/thermal model | SOLVER_DEPENDENT | G2/G8 |
| SW10 | Software | plant systems | thermal-hydraulic + process/power balance | SOLVER_DEPENDENT | G8 |

## BOM closure rule

A row being present means the reactor architecture accounts for the subsystem. It does **not**
mean the subsystem has been designed, procured, certified, or demonstrated. A procurement BOM
can only be generated after the corresponding physics/engineering gates close and a qualified
engineering organization accepts the design basis.
