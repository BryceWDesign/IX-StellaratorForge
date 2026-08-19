# SFR-2 Rev A — v0.5.0 low-authority screening result

## Verdict

`NO_PRIMARY_CASE_CROSSES_OPTIMISTIC_IGNITION_PROXY`

This result is **not evidence of ignition or achieved fusion hardware**. It is an analytical/empirical screening artifact.

## Geometry bookkeeping

- Sector sequence: `SFR-2-RevA` uses 23 / 26 / 23 / 26 ft as four consecutive sectors of **one closed toroidal plasma system**.
- Total axis-path proxy: 29.870400 m.
- Equivalent circular major radius: 4.754022 m.
- Screening aspect ratio: 4.500.
- Screening minor radius: 1.056449 m.
- The ABAB staggering receives **zero confinement credit** in this model.

## Primary screen — H_ISS04 = 1.0, no assumed transient confinement penalty

- Best primary case: B_axis=15.0 T, iota(2/3)=0.90, radial squeeze=0.00%.
- Optimistic ignition-proxy tau ratio: **0.961077**.
- Required H_ISS04 at unit retention: **1.040499**.
- Uniform target-power-matched fusion screen: 1000.000 MW.
- Circular neutron wall-load proxy: 4.041 MW/m².

## Dynamic-compression check

- Best H=1 dynamic case: B_axis=15.0 T, iota(2/3)=0.90, squeeze=5.00%.
- Optimistic ignition-proxy tau ratio: **0.888505**.
- In the target-power-matched ISS04 screen, compression does **not** automatically improve the ignition proxy; shrinking the minor radius penalizes empirical confinement. This is a useful negative result, not a failed repository run.
- No RF resonance, magnetic pumping, traveling-wave phase gain, or flux-compression field amplification is numerically credited.

## Favorable sensitivity only — not earned performance

- Best declared sensitivity case: H_ISS04=1.4, B_axis=15.0 T, iota(2/3)=0.90, squeeze=0.00%, retention=1.00.
- Tau ratio: 1.345508.
- H>1 and retention values are scenario variables. SFR-2 has not earned them from equilibrium/transport evidence.

## What changed relative to the conversational exploration

Earlier chat percentages were heuristic and are **not retained as repository evidence**. The v0.5.0 implementation recalculates the candidate from explicit equations and exposes an important correction: once fusion power is normalized to the same 1 GW target, ideal radial compression can worsen the ISS04 ignition proxy even while increasing density and temperature. The repository result supersedes those exploratory percentages.

## Authority boundary

A low-authority pass may justify more computation; it may not declare ignition. A low-authority failure may reject a candidate. Dynamic finite-beta equilibrium, islands/stochasticity, MHD, kinetic transport, alpha orbits, RF deposition, real coils, transient heat flux, neutronics and hardware remain open.
