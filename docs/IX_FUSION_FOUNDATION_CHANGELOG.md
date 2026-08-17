# Changelog

## 0.1.0 — 2026-08-15

Initial evaluation release.

- Locked the C6-seeded stellarator hypothesis and matched-control protocol.
- Added reduced field-strength, field-line, bounce-action, engineering, and robustness screens.
- Added deterministic equal-budget seed optimization.
- Added distributed phase-control Monte Carlo and structural/geometry-error Monte Carlo.
- Added ablations for axis shaping, mirror term, harmonic phase, C3 correction, and C9 correction.
- Added evidence bundles, loss ledger, claim gates, validation gate, release manifest, and reproducibility tooling.
- Hardened release reproduction for Windows/Linux portability: exact structure and text are preserved while floating-point outputs use tight `rtol=1e-10` / `atol=1e-12` comparison with mismatch-path diagnostics.
- Current C6 hypothesis result is `FAIL_OR_INCONCLUSIVE` at the reduced-model gate; scientific stage remains `geometry_hypothesis`.
