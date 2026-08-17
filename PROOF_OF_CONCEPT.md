# IX-StellaratorForge — SFR-1 Proof of Concept and Computational Closure

Release: **0.4.0**

PoC verdict: **`PIPELINE_POC_PASS__REACTOR_PHYSICS_NOT_CLOSED`**

Maximum in-repo closure verdict: **`MAXIMUM_IN_REPO_COMPUTATIONAL_CLOSURE_COMPLETE__PRODUCTION_SOLVER_AND_HARDWARE_GATES_REMAIN`**

## Two different things are tested

The lightweight SFR-1 PoC verifies that architecture validation, D-T burn, confinement requirements, target-vs-screened power accounting, RF resonance, source-term accounting and held-out magnetic reconstruction execute reproducibly.

The v0.4 maximum closure campaign goes further: it generates production MHD inputs, executes new vacuum magnet architectures, traces field lines, calculates HTS geometry strain proxies, solves TBR coverage constraints and closes conditional plant thresholds.

Neither is allowed to impersonate DESC/VMEC++, gyrokinetics/neoclassical transport, structural FEA, OpenMC 3-D transport or hardware.

## Run

```bash
python scripts/run_sfr1_poc.py
python scripts/run_computational_closure.py
python scripts/generate_v040_evidence.py
```

Tracked outputs:

- `results/sfr1_poc/sfr1_poc_v040.json`
- `results/computational_closure/sfr1_v040.json`
- `results/computational_closure/SFR1_V040_RESULT.md`
- `results/reactor/sfr1_rev_a_readiness.json`

## What fails today

The current lower-authority plasma point does not reach the design fusion-power target; the new simple helical architecture cannot simultaneously reach the rotational-transform target and preserve its nestedness screen; the independent surface-current reconstruction does not meet the 0.5% held-out normal-field target.

Those failures are retained because they constrain what the production co-design must improve.

## Promotion boundary

A G1/G2/G3/G4/G7 green status can only be issued from imported production evidence that satisfies the machine-readable contracts. `external_solvers/adapters/validate_production_receipt.py` explicitly rejects unexecuted/template receipts.

Actual net-electric fusion remains outside software authority.
