# SFR-5 Reality Gradient and Adaptive Inverse Design A

## Executed result

Top-level verdict: `REALITY_GRADIENT_AUTOPSY_COMPLETE__CURRENT_MAGNETIC_FAMILY_REJECTED__ADAPTIVE_INVERSE_DESIGN_PATH_DEFINED__NO_PHYSICS_PROMOTION`

SFR-5 derives its diagnosis from the committed v0.9 SFR-4 magnetic result and its declared thresholds. It does not merge the direct-filament topology lane with the independent held-out reconstruction lane.

- SFR-4 direct-filament cases: **80**.
- Combined topology passes: **0**.
- Transform factor required merely to reach the minimum iota gate: **3.8265x**.
- Remaining normalized excursion slack: **3.887%** of the declared limit.
- Held-out RMS normal-field error relative to its limit: **12.9825x**.

## Decision

The present fixed helical plus fixed hybrid filament-basis family is rejected as the preferred next search family. The next program must allow the plasma boundary, winding surface, nonplanar coil geometry, and currents to move together under explicit engineering constraints.

The primary next family is `single_stage_nonplanar_modular_fourier_coils_with_movable_plasma_boundary`. Winding-surface proxy/global optimization, discrete filament realization, finite-beta equilibrium, particle/transport checks, 3-D neutronics, magnet engineering, and hardware remain promotion gates rather than assumed capabilities.

## Reality Gradient status

SFR-5 computes normalized constraint pressure from the existing evidence but deliberately does **not** fabricate a geometry gradient. A backward gradient is only valid after a real movable-geometry evaluator supplies analytic, automatic-differentiation, or controlled finite-difference sensitivities.

## Claim boundary

This release does not demonstrate a viable replacement coil set, finite-beta equilibrium, kinetic confinement, TBR, ignition, net-electric power, magnet qualification, safety qualification, or hardware operation. Earned fusion-progress credit remains exactly zero.
