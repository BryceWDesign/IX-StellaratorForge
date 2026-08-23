# IX-StellaratorForge v0.10.0: Reality Gradient and Adaptive Inverse Design

## Bottom line

The v0.9 SFR-4 integrated campaign remains preserved: its declared nominal and steady heat envelope passes the reduced screen, while its scanned physical coil family fails with zero combined topology passes across 80 direct-filament cases.

Version 0.10.0 adds SFR-5 Reality Gradient and converts that failure into a governed architecture-search decision rather than increasing brute-force sampling of the same magnetic representation.

Top-level SFR-5 verdict:

`REALITY_GRADIENT_AUTOPSY_COMPLETE__CURRENT_MAGNETIC_FAMILY_REJECTED__ADAPTIVE_INVERSE_DESIGN_PATH_DEFINED__NO_PHYSICS_PROMOTION`

## Executed SFR-5 diagnosis

SFR-5 regenerates its values from the committed SFR-4 result and configuration:

* SFR-4 direct-filament candidates: 80;
* combined topology passes: 0;
* transform factor required merely to reach the minimum iota gate: approximately 3.8265x;
* remaining normalized radial-excursion slack in that same topology lane: approximately 3.887%; and
* separate held-out richer-basis RMS normal-field error: approximately 12.9825x its declared limit.

The direct-filament topology and held-out reconstruction are preserved as separate evidence lanes. They are not combined into a fictitious physical coilset.

## What changed

The fixed helical plus fixed hybrid filament-basis family is rejected as the preferred target for more brute-force sampling. SFR-5 opens plasma-boundary, winding-surface, nonplanar-coil, current-group and engineering keep-out degrees of freedom for the replacement search.

The base release computes normalized constraint pressure but deliberately does not fabricate a geometry gradient. Real geometry sensitivities, constrained winding-surface optimization, discrete nonplanar coils, single-stage finite-beta co-design, particle/transport evidence, 3-D neutronics, magnet qualification, integrated plant analysis and hardware remain `NOT_RUN`.

## Preserved v0.9 heat result

The selected separated first-wall/blanket/divertor architecture still passes its declared nominal and steady reduced heat envelope. That remains requirement-level evidence only; stable detachment, 3-D island footprints, transient heat, lifetime, critical heat flux, irradiation, structural qualification and accidents remain open.

## Scientific boundary

Earned improvement toward demonstrated equilibrium, confinement, ignition, TBR, net-electric power, qualified magnets, safety or hardware remains exactly **0.00%**.

The useful v0.10 advance is a stronger research-control result: failed magnetic evidence now determines which representation must change next, while the software is prohibited from promoting that decision into a physical fusion claim.
