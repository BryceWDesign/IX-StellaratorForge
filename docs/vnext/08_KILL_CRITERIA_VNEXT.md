# vNext Kill Criteria

A branch is killed or demoted when any of the following survives reasonable solver-resolution and model-cross-check tests:

- no robust nested equilibrium / unacceptable islands at the required pressure range;
- direct-J or guiding-center confinement is materially worse than matched references;
- fast-alpha losses are unacceptable or hypersensitive to small field errors;
- required coils violate clearance, curvature, HTS strain, support-stress, or stochastic-error tolerances;
- turbulent heat or particle transport forces implausible fueling/heating requirements;
- edge topology cannot spread exhaust within chosen material/engineering limits without compromising core confinement;
- RF deposition/control advantage disappears in 3-D propagation or is outweighed by recirculating/complexity burden;
- blanket/shield radial build or penetrations make the magnetic design infeasible;
- whole-system power/maintenance/uncertainty accounting loses to a matched baseline;
- the optimizer consistently removes the C6-specific structure, in which case C6 is retired even if descendants remain viable.

A candidate may be scientifically interesting and still fail the reactor-candidate gate.
