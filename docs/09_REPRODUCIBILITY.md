# Reproducibility

The release uses deterministic inputs and explicit random seeds.

Primary reproducible artifacts:

- `results/poc/c6_candidate.json`
- `results/baselines/matched_helical_5fp.json`
- `results/poc/verdict.json`
- `results/ablations/c6_ablations.json`
- `results/monte_carlo/rf_robustness.json`
- `results/monte_carlo/geometry_error_robustness.json`
- `results/evidence/loss_ledger.json`
- `results/evidence/IXFUSION-POC-001.json`

`python scripts/reproduce_release.py --verify` regenerates the deterministic machine results
in a temporary directory and compares them to the committed release. Runtime timestamps are
excluded from semantic equality. JSON structure, integers, booleans, strings, and non-JSON text
remain exact. Floating-point values are compared with a deliberately tight cross-platform
tolerance (`rtol=1e-10`, `atol=1e-12`) so last-bit differences from operating-system, CPU math
library, Python patch release, or NumPy build do not create false RED results. Differences larger
than those tolerances remain failures and are reported with their JSON paths and values.

Figures are regenerated from the same machine results but are not byte-compared because
rendering metadata may vary across Matplotlib versions.
