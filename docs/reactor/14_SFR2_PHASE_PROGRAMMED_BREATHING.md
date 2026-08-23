# SFR-2 phase-programmed magnetic breathing

## Question

Can timed contraction and expansion of the magnetic flux-surface envelope move the unchanged SFR-2 Rev A design closer to its optimistic ignition proxy while supporting, rather than merely spiking, cycle-averaged fusion output?

## Preserved design

The 23 / 26 / 23 / 26 ft ABAB axis-path bookkeeping, four field periods, rigid vacuum vessel and steady primary HTS confinement field remain unchanged. The study adds an optional auxiliary magnetic-field overlay. It does not mechanically flex the reactor.

## Three declared phase patterns

| Pattern | Sector phases | Purpose |
|---|---|---|
| Synchronous | 0 / 0 / 0 / 0 degrees | Global contraction and expansion upper-bound |
| ABAB opposed | 0 / 180 / 0 / 180 degrees | Alternating squeeze and expansion between A and B sectors |
| Traveling quadrature | 0 / 90 / 180 / 270 degrees | A phase-stepped perturbation moving around the closed path |

Depths of 0, 0.25%, 0.5%, 1%, 2% and 5% are sampled at 720 points per cycle.

## Model

For sector `j`, the minor-radius scale is

`s_j(t) = 1 - epsilon sin(omega t + phi_j)`.

The global volume ratio is the axis-length-weighted sum of `s_j(t)^2`. Particle inventory is fixed. Density and temperature follow ideal monatomic adiabatic bookkeeping. Bosch-Hale D-T reactivity produces an instantaneous uniform-plasma fusion-power screen. Each time sample is compared with the ISS04 alpha-only optimistic ignition proxy at `H_ISS04 = 1`.

This is a zero-dimensional global-volume screen. It cannot resolve local pressure redistribution, field-line topology, islands, stochasticity, MHD, kinetic absorption, alpha orbits, edge loads or realizable coil currents.

## No hidden credits

Numerical credit is zero for magnetic-pumping absorption, RF phase heating, shocks, flux-field amplification, actuator efficiency, astrophysical gravity, accretion and three-body fusion. Actuator, cooling and cryogenic power are not yet known, so no net-power claim is permitted.

## Result

The closest cycle-average case is 5% traveling-quadrature actuation:

| Quantity | Baseline | 5% traveling quadrature |
|---|---:|---:|
| Cycle-average optimistic ignition ratio | 0.961077249 | 0.961559491 |
| Cycle-average uniform fusion power | 1000.000 MW | 997.233 MW |
| Joint improvement | n/a | No |

The ratio improvement is only about 0.000482 absolute while uniform fusion power falls by about 2.767 MW, before actuator losses. No declared case crosses the cycle-average proxy or improves both primary metrics.

The synchronous 5% case briefly reaches 0.998114154, but this occurs during the 5% expansion half-cycle, not during compression, while the uniform fusion-power screen falls to about 802.542 MW. Its cycle-average proxy is worse than baseline. It is not ignition capture or sustained burn.

## Decision

The breathing overlay is rejected as an earned closer-to-fusion result at this authority. It remains a testable actuator hypothesis only. Promotion requires the evidence in `15_SFR2_ACTUATION_AND_TRILOBE_GATES.md`.
