# SFR-4 Integrated Physical-Promotion Campaign A

## Purpose

SFR-4 attempts the seven computational workstreams requested after Dual Boundary AHIS A:

1. physical coil fields;
2. finite-beta equilibrium;
3. coil and plasma co-design;
4. particle confinement;
5. self-consistent burn requirements;
6. magnet and heat engineering; and
7. reactor systems.

The campaign executes every method available in the build runtime and explicitly attempts the production adapters. DESC, VMEC++, SIMSOPT, OpenMC, kinetic transport, CAD, CFD and structural FEA are unavailable. Their gates therefore remain `NOT_RUN` or fail closed.

## Executed magnetic campaign

Eighty physical filament configurations are evaluated with direct Biot-Savart fields and field-line integration. Four field-period counts, two current-sign patterns and ten helical-to-toroidal-field current ratios are compared under identical geometry and acceptance rules.

No configuration passes both the radial-excursion and rotational-transform screens. The best declared scoring point uses six field periods, four alternating helices and a 1.0 helical-to-TF current ratio. It gives approximately 0.0653 mean iota and 0.1922 normalized maximum excursion. The excursion screen passes; the minimum 0.25 transform gate fails.

The held-out richer filament reconstruction also fails its 0.5% RMS normal-field criterion. SFR-4 therefore rejects this coil family rather than attaching its design-iota burn target to a nonpassing field.

## Particle and burn scope

The maximum-pitch 3.5 MeV alpha gyroradius at 6 T is approximately 0.0449 m, or 2.64% of the 1.7 m screening minor radius. Passing that scale test does not establish alpha retention. Guiding-center, neoclassical and gyrokinetic evidence remain absent, and the magnetic-topology prerequisite fails.

The Q=20 design-iota burn requirement includes Bosch-Hale D-T reactivity, a declared 90% alpha-deposition assumption and a hydrogenic bremsstrahlung screen. It requires approximately H_ISS04 2.00 at iota 0.55 under the declared assumptions. The value is a requirement, not a prediction, and cannot be credited to the failed physical coil family.

## Verdict

SFR-4 completes an integrated reduced campaign and produces a useful heat architecture. It does not promote a physical confinement candidate or move the earned fusion result above zero.
