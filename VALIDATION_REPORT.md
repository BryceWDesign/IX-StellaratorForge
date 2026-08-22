# IX-StellaratorForge Validation Report

Release: **0.9.0**
Date: **2026-08-22**
Authority: **software integrity plus mixed low/intermediate analytical and direct-filament screening**

## v0.9 validation scope

The SFR-4 focused suite adds eleven tests covering the seven-workstream specification, 80-case physical coil rejection, production-solver fail-closed behavior, alpha gyroradius boundaries, burn-loss bookkeeping, heat partition, first-wall and divertor temperatures, hydraulic requirements, heat sensitivity, magnet nonqualification, conditional reactor bookkeeping and exact persisted-result reproduction.

One additional release-contract test checks the 64-row SFR-4 BOM. The complete suite contains **114 deterministic tests** when combined with the preserved 102-test v0.8 release.

## Executed evidence

* 80 direct-filament Biot-Savart and vacuum field-line cases;
* one held-out 120-filament normal-field reconstruction at the selected field-period count;
* 3.5 MeV alpha gyroradius scope;
* Bosch-Hale D-T burn and ISS04 Q=20 requirement with bremsstrahlung;
* 16-point radiation-fraction and divertor-area heat sensitivity matrix;
* multilayer first-wall and divertor 1-D conduction;
* distributed-water-loop mass flow, velocity, pressure drop and pump power;
* REBCO centerline geometry, magnetic-pressure and stored-energy scopes;
* exact D-T neutron and tritium source ledger;
* breeding-coverage constraint; and
* conditional plant arithmetic.

## Negative and open evidence

No physical coil passes. DESC, VMEC++, SIMSOPT and OpenMC are unavailable. Particle confinement, finite-beta equilibrium, transport, stable detachment, thermal transients, structural survival, full 3-D TBR, sustained burn, net electricity, safety and hardware remain unpromoted.

## GREEN meaning

GREEN means the repository, configuration, persisted reduced result, tests, BOMs, manifests and fail-closed boundaries reproduce. It does not mean the heat solution is physically qualified or that fusion performance improved.
