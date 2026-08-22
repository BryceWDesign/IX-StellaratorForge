# SFR-2 Actuation Overlay A BOM

This is the architecture-level build inventory for testing phase-programmed magnetic breathing and a repeated poloidal tri-lobe actuator harmonic without changing the SFR-2 Rev A baseline.

## Locked architectural decisions

1. The vacuum vessel, blanket and primary HTS confinement magnets remain rigid.
2. The primary HTS magnet current remains steady DC.
3. Eight auxiliary normal-conducting saddle-coil triplet stations are screened, two per ABAB field period.
4. Twenty-four independently driven circuits permit synchronous, ABAB-opposed and traveling-quadrature waveforms.
5. No actuator current, field amplitude, voltage, stored energy, conductor size, cooling rate or support load is claimed before equilibrium and electromagnetic solves.
6. The actuator package cannot be promoted without full-cycle topology, kinetic, alpha-orbit, MHD, eddy-current, fatigue and integrated-power evidence.

## Meaning of “proper BOM” at this stage

The companion CSV is complete for the selected test architecture at system level. It is not a procurement or fabrication BOM. Ratings and dimensions that would require a solved magnetic field, conducting-structure response or hardware qualification are explicitly marked solver-dependent or hardware-dependent instead of being invented.

The main SFR-2 design is not replaced by this overlay. A rejected overlay leaves the v0.5.0 SFR-2 Rev A evidence unchanged.
