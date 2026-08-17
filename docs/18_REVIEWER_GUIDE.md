# Reviewer Guide

A technically skeptical review is the intended use case.

Recommended order:

1. `README.md`
2. `docs/02_CLAIM_BOUNDARY.md`
3. `docs/05_PROOF_OF_CONCEPT.md`
4. `results/poc/POC_RESULT.md`
5. `docs/12_MODEL_LIMITATIONS.md`
6. `src/ix_fusion/field.py` and `src/ix_fusion/omnigenity.py`
7. `src/ix_fusion/optimizer.py`
8. `results/ablations/c6_ablations.json`
9. `results/evidence/loss_ledger.json`
10. `docs/15_EXTERNAL_SOLVERS.md`
11. `python check_green.py`

Questions the repository invites:

- Is the reduced field model useful enough to justify the next solver gate?
- Is the matched baseline fair?
- Are the objective terms weighted defensibly?
- Which internal proxy should be deleted once a high-fidelity solver is integrated?
- Does C6 offer any advantage after genuine equilibrium/coil optimization?
- Does the radial-excursion improvement survive guiding-center analysis?
- Is active phased control worth its complexity when actual deposition physics is included?

A reviewer does not need to accept the hypothesis to find the repository useful.
