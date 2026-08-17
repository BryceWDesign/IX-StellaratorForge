# Model Hierarchy

IX-Fusion uses an authority ladder. A result may not be interpreted above the level of the
model that produced it.

| Level | Model | Allowed interpretation |
|---|---|---|
| L0 | geometry/configuration | seed definition only |
| L1 | reduced field strength + field-line ODE | comparative screening |
| L2 | reduced bounce-action proxy | trapped-particle hypothesis screening |
| L3 | solved MHD equilibrium | magnetic-candidate evidence |
| L4 | coil realization + error fields | buildability/field-realization evidence |
| L5 | guiding-center/fast-particle + stability | confinement-candidate evidence |
| L6 | turbulence + edge/divertor + RF full-wave | plasma-candidate evidence |
| L7 | neutronics + fuel cycle + full plant power | fusion-performance-candidate evidence |

Release 0.1 ends at **L2** internally. Optional external-solver adapters are detection and
interface points; they do not fabricate L3+ evidence when those tools are absent.
