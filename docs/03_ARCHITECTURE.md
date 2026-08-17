# Architecture

IX-Fusion is deliberately layered so low-fidelity internal models can later be replaced by
specialist solvers without rewriting the evidence and claim-control plane.

## Layer 1 — Geometry seed

C6 is the initial field-period hypothesis. C3 and C9 terms are ordinary optional Fourier/
helical corrections and are not privileged. An optimizer is free to eliminate them.

## Layer 2 — Magnetic screening

The internal release contains a dimensionless field-strength spectrum and a reduced
Hamiltonian-like field-line ODE. These are screening models only.

## Layer 3 — Omnigenity target

A reduced bounce-action variation proxy measures sensitivity to field-line label. It is
inspired by the second-adiabatic-invariant criterion but is explicitly not the invariant of
a solved equilibrium.

## Layer 4 — Active control

Six distributed phase-controlled actuators are represented as a spatial phased array. The
current model evaluates mode purity under phase, amplitude, and geometry errors and an
abstract feedback correction. Frequency is intentionally not hard-coded; a real frequency
must come from a plasma resonance/deposition model.

## Layer 5 — Magneto-structural integrity

Axis curvature/torsion and normalized support burden are screening terms. The intended
high-fidelity path is joint coil/support optimization with field-error feedback and
structural sensing, not post-hoc mechanical design.

## Layer 6 — Reactor-facing engineering penalties

Blanket-space, heat-spreading, shielding-penetration, and cryogenic burdens are intentionally
normalized. They prevent the optimizer from treating engineering as free but do not replace
neutronics, thermal-hydraulics, materials, or cryogenic design.

## Layer 7 — Evidence control plane

Every promoted claim must pass explicit gates. Results are versioned, hashed, reproducible,
and allowed to be negative. A loss ledger records what remains unknown.
