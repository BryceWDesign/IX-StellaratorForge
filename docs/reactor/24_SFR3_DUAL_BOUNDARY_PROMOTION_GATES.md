# SFR-3 dual-boundary promotion gates

| Gate | Evidence required | v0.8 status |
|---|---|---|
| SFR3D-G0 | Versioned architecture, layer stack, monitoring count, fault states and claim boundary | `PASS_SPEC_ONLY` |
| SFR3D-G1 | Three-stack 1-D comparison and eleven-scenario deterministic fault campaign | `PASS_LOW_AUTHORITY_SYNTHETIC_ONLY` |
| SFR3D-G2 | Coupled 3-D thermal, coolant CFD, electromagnetic load and nonlinear structural FEA | `NOT_RUN` |
| SFR3D-G3 | Fracture, creep, fatigue, erosion, joining and irradiation lifetime | `NOT_RUN` |
| SFR3D-G4 | Sensor radiation, temperature, drift, calibration, latency and feedthrough qualification | `NOT_RUN` |
| SFR3D-G5 | CAD-linked vessel, blanket, shield and sensor magnetic perturbation plus trim response | `NOT_RUN` |
| SFR3D-G6 | Full 3-D neutronics, TBR, nuclear heating, damage, gas production, dose and streaming | `NOT_RUN` |
| SFR3D-G7 | Integrated helium, PbLi, tritium, chemical, fire, leak and decay-heat safety analysis | `NOT_RUN` |
| SFR3D-G8 | Remote maintenance, alignment recovery, availability and activated waste | `NOT_RUN` |
| SFR3D-G9 | Instrumented coupon, sector prototype and representative fault-injection hardware | `NOT_RUN` |

## Kill criteria

The branch is demoted if the selected stack exceeds structural temperature or strain limits in coupled analysis, coolant isolation cannot prevent escalation, sensor survivability or probability of detection is inadequate, common-cause failure defeats both lanes, vessel or shield materials create unacceptable magnetic error, TBR or REBCO protection fails, or remote replacement cannot restore alignment.

Neither a G0 specification nor G1 reduced-screen pass may be quoted as physical wall survival, safety qualification or improved plasma confinement.
