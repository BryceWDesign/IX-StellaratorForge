# SFR-1 v0.4 Computational Closure Result

Verdict: `MAXIMUM_IN_REPO_COMPUTATIONAL_CLOSURE_COMPLETE__PRODUCTION_SOLVER_AND_HARDWARE_GATES_REMAIN`

## Magnet search

- 40 classical-helical architecture points executed across 2/3/4/6 field periods, two current-sign patterns and five helical/TF current ratios.
- best screened case: 4FP alternating helices, ratio 0.40;
- mean |iota|: ~0.03885;
- maximum traced radial excursion: ~0.2865 m (~16.85% of minor radius);
- nestedness screen: PASS;
- transform screen: FAIL;
- combined screen: FAIL.

Independent continuous current-potential held-out RMS `Bn/B0`:

- 2FP: ~0.01643;
- 3FP: ~0.02319;
- 4FP: ~0.03052;
- 6FP: ~0.04570.

All exceed the 0.005 screening limit.

The geometry-only REBCO strain proxy is below the 0.004 ceiling for the reference TF loop and the best screened helix, but field-performance failure blocks magnet promotion.

## Equilibrium

Four VMEC-format fixed-boundary finite-pressure seed inputs are generated and boundary reconstruction is unit-tested against the analytic SFR-1 screening surface. Production MHD execution remains open.

## Confinement

The existing Q=10 requirement is retained and the new vacuum field-line result provides topology evidence. Kinetic confinement is not promoted.

## Neutronics

At 1 GW fusion and global TBR target 1.15, required local TBR under the zero-breeding-uncovered-area bound is:

- 100% blanket coverage: 1.150;
- 95%: 1.211;
- 90%: 1.278;
- 85%: 1.353;
- 80%: 1.4375;
- 75%: 1.533.

Full 3-D OpenMC remains open.

## Net electric

- current uniform fusion screen: ~704.57 MW;
- current conditional net: ~204.10 MWe;
- fusion power required for 300 MWe floor: ~913.04 MW;
- beta required for the 300 MWe floor under fixed-T uniform scaling: ~3.415%;
- beta required for the 1 GW fusion target under the same scaling: ~3.574%;
- target 1 GW conditional net: 340 MWe.
