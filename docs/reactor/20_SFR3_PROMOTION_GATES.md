# SFR-3 promotion gates

| Gate | Required evidence | v0.7 status |
|---|---|---|
| SFR3-G0 architecture | Explicit components, donor dispositions, claim boundary and BOM | `PASS_SPEC_ONLY` |
| SFR3-G1 synthetic controllability | Full-row-rank deterministic response, bounded nominal case, single-channel fault, passive-only and safe-hold cases | `PASS_LOW_AUTHORITY_SYNTHETIC_ONLY` |
| SFR3-G2 coil response | CAD-linked Biot-Savart or equivalent response matrix including ports, shields and blanket steel | `NOT_RUN` |
| SFR3-G3 equilibrium and islands | Free-boundary finite-beta equilibria; island widths, effective ripple and strike-point motion with faults | `NOT_RUN` |
| SFR3-G4 orbits | Thermal-ion and alpha guiding-center/full-orbit losses over credible error distributions | `NOT_RUN` |
| SFR3-G5 transport and MHD | Neoclassical and turbulent transport plus stability over the controlled envelope | `NOT_RUN` |
| SFR3-G6 magnet engineering | Integrated electromagnetic stress, support modes, REBCO margin, quench and cryogenic budget | `NOT_RUN` |
| SFR3-G7 neutronics and TBR | Port-resolved 3-D OpenMC or equivalent; TBR, heating, damage, dose and lifetime | `NOT_RUN` |
| SFR3-G8 burn and plant | Self-consistent heating, fueling, exhaust, recirculating power and net-electric balance | `NOT_RUN` |
| SFR3-G9 hardware | Calibrated coil/sensor coupon, fault-injection bench and then plasma experiment | `NOT_RUN` |

## Kill criteria

The branch is demoted if physical coil responses are ill-conditioned, required commands exceed engineering limits, passive loops cannot quench safely, correction worsens islands or fast-particle loss, structural motion defeats field tolerance, shielding eliminates maintainability or TBR, or active recirculating power negates plant closure.

No lower gate may substitute for a higher gate. In particular, SFR3-G1 cannot be described as improved confinement.
