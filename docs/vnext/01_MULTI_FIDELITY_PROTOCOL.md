# Multi-Fidelity Promotion Protocol

The rule is asymmetric:

> **Cheap models may kill a candidate. Cheap models may not crown a candidate.**

## Promotion ladder

| Gate | Minimum authority | Required question |
|---|---|---|
| G0 Seed | reduced model | Is the hypothesis internally coherent enough to spend solver time? |
| G1 Equilibrium | solved 3-D MHD equilibrium | Are surfaces, transform, finite-beta behavior, and equilibrium self-consistent? |
| G2 Coils | explicit coil/support realization | Can magnets reproduce the field with usable clearance, strain, stress, and error tolerance? |
| G3 Orbits | guiding-center / direct-J transport | Are trapped and fusion-born energetic particles acceptably confined? |
| G4 Turbulence | nonlinear gyrokinetic + profile transport | Are heat and particle transport acceptable together? |
| G5 Edge | edge/divertor/vessel model | Can exhaust be routed without unacceptable peak loads or fragile topology? |
| G6 RF | 3-D deposition/wave model | Can heating/control be delivered robustly with acceptable recirculating power? |
| G7 Neutronics | 3-D transport model | Are coil heating, shielding, blanket radial build, and penetrations credible? |
| G8 System | coupled uncertainty/system model | Does the design still beat matched baselines after all penalties and uncertainties? |

A result cannot be promoted beyond the authority of the solver that produced it. Cross-code disagreement is evidence, not noise to be averaged away.
