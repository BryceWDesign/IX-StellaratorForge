# IX-Fusion Proof of Concept Result

> **Authority boundary:** reduced-order computational screening only. This document is not
> an MHD equilibrium result, a reactor design, or evidence of net-positive fusion energy.

**Candidate:** `c6_flower_derived_seed`  
**Matched baseline:** `matched_helical_5fp_control`  
**Reduced-model verdict:** **FAIL_OR_INCONCLUSIVE**  
**Scientific stage:** `geometry_hypothesis`

## Predeclared gates

| Gate | Status | Candidate/value | Threshold/reference |
|---|---:|---:|---:|
| composite_improvement | **FAIL** | -0.04873197 | >= 0.02 |
| bounce_action_proxy | **FAIL** | 0.00025810989 | 0.00025767287 |
| field_line_escape | **PASS** | 0 | 0 |
| engineering_burden | **FAIL** | 0.87056575 | 0.86688184 |

## Reduced-order metrics

| Metric | C6 seed | Matched baseline |
|---|---:|---:|
| Composite screening objective (lower better) | 0.03188204 | 0.03040056 |
| Bounce-action variation proxy | 0.0258% | 0.0258% |
| Field-strength coefficient of variation | 6.2718% | 6.2800% |
| Mean radial excursion proxy | 0.00930135 | 0.01303682 |
| Field-line escape fraction | 0.0000% | 0.0000% |
| Engineering burden proxy | 0.87056575 | 0.78807440 |

## Active-control robustness screen

Six-source target-mode purity, median open loop: **99.2097%**  
Six-source target-mode purity, median with abstract feedback: **99.9285%**  
Median unwanted-mode power reduction factor: **11.051x**

This signal-processing result does not demonstrate plasma heating, current drive, mode suppression,
or full-wave coupling. It only verifies that a distributed phased-actuator abstraction can be tested
under deterministic geometry/phase/amplitude error and feedback assumptions.

## Verdict

The C6 seed does not clear every predeclared reduced-order advantage gate. The hypothesis remains a geometry experiment and must not be described as a confinement improvement.

## Required next authority gates

1. Solved 3-D equilibrium from DESC/VMEC-class tooling.
2. Coil realization and normal-field error from SIMSOPT-class tooling.
3. Guiding-center / fast-particle confinement against matched controls.
4. Finite-pressure MHD stability.
5. Turbulent transport and edge/divertor analysis.
6. RF full-wave / deposition modeling.
7. Blanket, neutronics, cryogenic and recirculating-power accounting.

Until those gates are passed, IX-Fusion remains a **geometry hypothesis and evaluation framework**.
