# Proof of Concept

## Predeclared test

Candidate: `c6_flower_derived_seed`  
Matched control: `matched_helical_5fp_control`

Both receive the same optimizer algorithm, passes, amplitude steps, phase steps, iota steps,
and mirror steps. The matched control is not presented as W7-X, HSX, or any named device.
It is a reduced-model comparator with a different field-period seed.

## Gates

1. Composite screening objective must improve by at least 2%.
2. Bounce-action variation proxy may not worsen.
3. Field-line escape fraction may not worsen.
4. Engineering burden may be at most 10% above the matched control.

## Current result

The C6 candidate fails the overall gate. The committed machine-readable verdict is:

`FAIL_OR_INCONCLUSIVE`

Notable tension in the result:

- C6 mean radial excursion proxy is lower than the matched control.
- C6 bounce-action variation is marginally worse.
- C6 engineering burden is higher than the allowed ratio.
- C6 composite objective is worse, so the predeclared advantage threshold is not reached.

This is precisely why the repository does not optimize a single attractive metric.

See `results/poc/POC_RESULT.md` and `results/poc/verdict.json` for exact regenerated values.
