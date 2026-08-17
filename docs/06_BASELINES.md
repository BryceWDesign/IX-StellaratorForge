# Baselines and Controls

## Matched helical control

`configs/baselines/matched_helical_5fp.json` is the primary release-0.1 comparator.
It matches the candidate's major/minor radius, initial helical-axis amplitude, initial iota,
shear, mirror amplitude, required total helical strength, number of harmonic degrees of
freedom, and optimizer budget while using a five-field-period spectrum.

It is intentionally described as a **matched reduced-model control**, not a model of an
existing stellarator.

## Axisymmetric negative control

`axisymmetric_negative_control.json` exists to test code response to removal of helical
terms. It is not a fair stellarator baseline because the reduced field-line model can impose
rotational transform independently of a physical coil geometry.

## Why a named machine is not used as the internal baseline

A fair comparison to W7-X, HSX, or another optimized stellarator requires validated
equilibrium and coil data plus the same downstream particle/stability/transport pipeline.
Pretending that the reduced internal model represents those devices would make the
comparison less credible, not more.
