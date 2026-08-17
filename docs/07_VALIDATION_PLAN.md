# Validation Plan

## Release-0.1 gates

- configuration/schema integrity;
- deterministic optimizer behavior;
- field-period geometry regression;
- field-line integration determinism;
- bounce-action proxy tests;
- RF spatial-mode purity tests;
- engineering-proxy monotonicity tests;
- incomplete energy-ledger refusal;
- evidence-bundle validation;
- committed-result reproduction;
- release-manifest integrity.

## Promotion gates

### Geometry hypothesis → magnetic candidate

Requires a solved 3-D equilibrium, nested-surface evidence, rotational-transform profile,
coil or equivalent field realization, and normal-field-error report.

### Magnetic candidate → confinement candidate

Requires guiding-center/fast-particle analysis and matched-control comparison.

### Confinement candidate → plasma candidate

Requires finite-pressure equilibrium, MHD stability, transport, and edge/divertor analysis.

### Plasma candidate → fusion-performance candidate

Requires blanket/neutronics, fuel-cycle, complete recirculating-power accounting, and a
plant-level energy analysis.

A later-stage gate cannot be bypassed by a favorable earlier-stage proxy.
