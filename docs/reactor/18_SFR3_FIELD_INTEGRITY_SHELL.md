# SFR-3 Field Integrity Shell A

## Objective

Field Integrity Shell A attempts to preserve the intended nested magnetic surfaces in the presence of construction error, support motion, blanket magnetization, current error and time-varying perturbations. It does not replace the primary stellarator field.

## Architecture

1. **Steady primary field.** Copper-stabilized REBCO coils remain the only baseline confinement source. The rigid vacuum vessel and plasma-facing surfaces do not move.
2. **Distributed active trim.** Twenty-four independently driven planar correction channels target a declared set of low-order Fourier error harmonics. Commands are bounded and may be withheld.
3. **Passive transient response.** Twenty-four optimized superconducting loops are retained as a research branch. Induced currents may oppose changing flux; the screen assigns them no static-error or DC correction credit.
4. **Observability.** Magnetic pickup coils, flux loops, circuit-current metrology, quench detection, cryogenic strain and support-motion sensing feed a confidence-aware estimator.
5. **Guarded control.** Active trim is allowed only when sensor confidence, power, thermal margin, quench state and an independent watchdog all pass. Failure returns to the known steady baseline or passive-only safe hold.
6. **Mechanical field preservation.** All-metal tuned dampers, optional shunt damping and alignment metrology target measured support modes. They receive no plasma credit; their purpose is to reduce coil motion and field error.
7. **Protected magnets.** WC/B4C and solver-dependent HfH composite options are concentrated around REBCO, joints and streaming paths. Shielding protects the field source but does not confine plasma.

## What the v0.7 screen actually computes

The code builds a 12-by-24 deterministic response matrix for cosine/sine components of six `(m,n)` harmonics. A bounded ridge solution commands the active array. A separate attenuation coefficient applies only to a declared transient vector. Seven scenarios test nominal operation, one failed actuator, low sensing confidence, passive-loop quench, active-coil quench, exhausted thermal margin and passive-only transient response.

The synthetic screen passes its declared thresholds. This means the chosen mathematical actuator basis spans the chosen mathematical error basis with bounded commands. It does **not** show that physical coils fit, survive, generate the response, preserve flux surfaces, suppress islands or improve confinement.

## The grounded “Tesla” question

The defensible lesson from Nikola Tesla's engineering—not an invented quotation—is to control fields through resonance, phase, geometry, measurement and energy accounting. In this architecture that becomes:

- do not fight the plasma with mass; shape the electromagnetic boundary condition;
- identify harmful spatial and structural modes rather than driving everything;
- separate passive response from powered correction;
- measure phase and amplitude before applying feedback; and
- fail to a stable unactuated state when authority or evidence is insufficient.

The repo therefore tests a field-control network, not a mythical ultra-dense container.
