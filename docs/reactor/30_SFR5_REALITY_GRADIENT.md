# SFR-5 Reality Gradient and Adaptive Inverse Design

## Why SFR-5 exists

SFR-4 did more than reject one magnetic scan. It exposed a representation bottleneck.

The best direct-filament helical topology case has mean iota `0.06533346157` against the declared minimum `0.25`, while its normalized maximum radial excursion is already `0.1922252737` against a `0.20` ceiling. Reaching the minimum transform would require about `3.8265x` the present mean transform while only about `3.887%` normalized excursion slack remains.

A separate held-out richer filament reconstruction has validation RMS `Bn/B = 0.06491274876` against a `0.005` screen, about `12.9825x` the limit.

Those values belong to different reduced-model lanes. SFR-5 keeps them separate and does not invent a single physical coilset that satisfies or violates all of them simultaneously.

## The missing control loop

Earlier releases largely push information forward:

`plasma target -> magnet family -> reduced physics -> engineering screen -> pass/fail`

SFR-5 adds the reverse information path:

`failed constraint -> normalized residual -> constraint pressure -> real sensitivity -> upstream geometry change`

For a canonical inequality `c_i(x) <= 0`, SFR-5 can maintain non-negative augmented-Lagrangian-style pressure. If a real solver supplies the Jacobian `J = dc/dx`, that pressure can be mapped onto upstream variables through a transpose-Jacobian operation. The base release intentionally stops before this step because no production movable-geometry evaluator is installed.

No geometry derivative is fabricated from the v0.9 numbers.

## What is now allowed to move

The next magnetic search is no longer restricted to current ratios and a fixed helical basis. The SFR-5 contract explicitly opens:

- plasma-boundary Fourier coefficients and field-period choice;
- winding-surface shape and clearance distribution;
- nonplanar modular-coil Fourier geometry;
- coil count, placement, symmetry class and independent current groups;
- REBCO orientation constraints;
- coil-to-coil and coil-to-plasma spacing;
- support, access and maintenance exclusion zones.

The primary replacement family is a single-stage nonplanar modular-coil search with a movable plasma boundary. A constrained differentiable winding-surface/global proxy is intended to reject coil-hostile plasma shapes before expensive discrete-coil and equilibrium work.

## Family rejection memory

The current `fixed_helical_plus_fixed_hybrid_filament_basis` family is stored as rejected evidence. It may not silently return because a later optimizer prefers it. Reopening requires explicit new evidence such as a different plasma-boundary family, winding-surface parameterization, nonplanar-coil parameterization, or higher-authority evidence that changes the identity of the failure.

## Claim boundary

SFR-5 G0 is a reduced architecture autopsy and research-control result. It does not establish a replacement coilset, finite-beta equilibrium, physical confinement, TBR, ignition, net electricity, qualified magnets, safety or hardware operation. Earned fusion-progress credit remains zero.
