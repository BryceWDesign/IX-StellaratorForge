# External Solver Integration

IX-Fusion is structured so internal reduced models can be replaced by specialist tools.
Release 0.1 detects but does not bundle or impersonate them.

## DESC

Intended authority: 3-D MHD equilibrium and optimization.

Adapter boundary should provide equilibrium surfaces, rotational transform, magnetic-field
strength data, pressure/current profiles, and solver convergence evidence in a versioned
run bundle.

## SIMSOPT

Intended authority: coil/field optimization, Biot-Savart field realization, engineering
constraints, and related stellarator optimization workflows.

## VMEC-class equilibrium

An independent equilibrium route is valuable for cross-checking solver-dependent results.

## Required adapter behavior

An adapter must record software version, input files, hashes, command/API settings, solver
status, convergence information, and output hashes. A failed or unavailable solver must
return `UNKNOWN`/failure evidence rather than substitute an internal proxy while preserving
a high-authority label.
