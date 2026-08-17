# IX-Fusion Validation Report

Release: **0.1.0**  
Date: **2026-08-15**  
Authority: **software integrity + reduced-order computational screening only**

## Validation summary

The release was generated from versioned configurations and validated locally with the same
quality gate committed for GitHub Actions.

Current test suite: **41 deterministic unit/regression tests**, covering configuration
validation, C6 periodicity, field-strength bounds, field-line integration, bounce-action
proxy behavior, optimizer determinism, RF mode purity and feedback, structural/engineering
screens, energy-ledger claim refusal, evidence validation, Monte Carlo reproducibility,
external-solver detection, and release-result claim boundaries.

Release reproduction: **PASS**. `scripts/reproduce_release.py --verify` regenerates the
machine-readable proof-of-concept, matched baseline, ablations, RF Monte Carlo, geometry-
error Monte Carlo, loss ledger, and POC report in a temporary directory and compares them
against the committed release.

## Current scientific verdict

The release's C6 hypothesis verdict is **`FAIL_OR_INCONCLUSIVE`** at the reduced-model gate.
The scientific stage remains **`geometry_hypothesis`**.

This is a validation success, not a fusion success: the repository is allowed to reject its
own hypothesis and still be GREEN if the rejection is reproducible and internally
consistent.

## What GREEN means

`python check_green.py` verifies:

- required release-contract files;
- parseable JSON/configuration/evidence artifacts;
- absence of common scaffolding markers;
- evaluation-license contract markers;
- conservative claim-boundary state;
- Python compilation;
- full unit/regression suite;
- deterministic scientific reproduction;
- SHA-256 release manifest integrity.

A GREEN result means the repository's **internal evidence chain** is intact.

## What GREEN does not mean

GREEN is not evidence of a solved equilibrium, real nested flux surfaces, particle
confinement, MHD stability, low turbulent transport, RF plasma coupling, blanket
performance, tritium self-sufficiency, ignition, net energy, net electricity, or reactor
safety/buildability.

Those remain later authority gates and are explicitly recorded as `UNKNOWN` where
applicable.
