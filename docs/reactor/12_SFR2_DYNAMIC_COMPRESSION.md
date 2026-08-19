# SFR-2 Rev A — staggered high-field dynamic-compression assumption breaker

## Purpose

SFR-2 is **not a replacement for SFR-1** and is not a declared reactor solution. It is a deliberately separate assumption-breaker candidate added in v0.5.0 to test whether the compact/high-field/dynamic ideas developed during design exploration survive transparent first-order physics screens.

The defining user-specified geometry is **23 / 26 / 23 / 26 ft**. In the repository this is interpreted as four consecutive arc-length sectors of **one closed toroidal plasma system**. It is **not** modeled as four independent stellarators connected by plasma ducts.

## Locked Rev A interpretation

- Sector pattern: `ABAB`.
- A sectors: candidate confinement-dominant regions.
- B sectors: candidate actuation/compression/heating-access regions.
- Primary confinement field: steady; it is never numerically reversed back and forth.
- Traveling actuation sequence: `A1 → B1 → A2 → B2` with 0/90/180/270 degree phase labels.
- Numerical phase/RF heating credit: **zero** until a real wave/plasma calculation exists.
- Numerical magnetic-flux-compression field credit: **zero**.
- “Magnetic rifling” is represented only by the ISS04 rotational-transform input `iota(2/3)` and does not assert that a realizable 3-D field with that transform exists.

## Geometry proxy

The sector lengths sum to 98 ft. v0.5.0 converts that centerline path to an equivalent circular major radius and uses a declared screening aspect ratio of 4.5 to obtain a circular-torus minor radius and volume. This is bookkeeping, not a solved stellarator boundary.

No benefit is awarded simply because the sectors alternate 23/26/23/26 rather than 24.5/24.5/24.5/24.5. Any actual ABAB advantage must be earned later by finite-beta equilibrium, orbit and transport calculations.

## Compression model

The radial-compression screen is intentionally simple and explicit:

1. Major radius is held fixed.
2. Both cross-sectional dimensions shrink by `(1-s)` where `s` is radial squeeze fraction.
3. Particle number is conserved, so density scales as `C²`, where `C = 1/(1-s)`.
4. An ideal monatomic adiabatic law gives `T ∝ C^(4/3)`.
5. Axis magnetic field is held fixed. No flux-compression field amplification is credited.
6. Uniform 50/50 D-T, `Te = Ti`, no impurities, ash, profile peaking or radiation.
7. D-T reactivity is Bosch-Hale.

This thermodynamic treatment is optimistic. Real dynamic compression can lose particles and energy, excite instabilities, generate asymmetry, alter the magnetic topology, and interact strongly with the wall.

## Confinement / ignition proxy

The screen compares:

- an optimistic alpha-only confinement requirement, `tau_required = W_thermal / P_alpha`, and
- ISS04 empirical stellarator energy-confinement scaling.

Radiation and other loss channels are not included in the alpha-only balance, so a ratio of one is **not ignition evidence**. ISS04 is itself an empirical global scaling and is extrapolated outside the data space when used for this candidate.

The primary result uses `H_ISS04 = 1.0`. Values 1.2 and 1.4 exist only as sensitivity variables and may not be presented as earned SFR-2 performance.

## v0.5.0 result

The repository-generated result is in `results/sfr2/SFR2_REVA_SCREEN_RESULT.md` and `results/sfr2/sfr2_rev_a_screen_v050.json`.

The most important outcome is a **negative correction** to the earlier informal exploration: when each case is normalized to the same 1 GW uniform-fusion target, ideal radial compression does not automatically improve the ISS04 ignition proxy. The density/temperature benefit is offset by the smaller minor radius and altered empirical confinement. This is precisely why the design is now encoded rather than relying on conversational percentages.

At `H_ISS04 = 1.0`, no declared SFR-2 Rev A case crosses the optimistic ignition proxy. The strongest primary point occurs at the high end of the declared field and transform sweep and remains below unity. Favorable `H > 1` sensitivity cases can cross the proxy, but those values are not earned by SFR-2 evidence.

## What would actually decide SFR-2

The next authority jump is not another algebraic percentage. It is a dynamic 3-D physics problem:

- construct and converge a finite-beta ABAB equilibrium;
- establish that the requested transform profile exists without destructive islands/stochastic regions;
- perturb that equilibrium through the full four-phase actuation cycle;
- test ideal/resistive MHD stability;
- calculate neoclassical, bootstrap, gyrokinetic/profile transport and alpha orbits;
- model RF/wave deposition instead of assigning phase-heating credit;
- design coils and structures that can produce the field while surviving stress, strain, quench and neutron exposure;
- solve transient edge/divertor/first-wall heat loads;
- run full 3-D neutronics/TBR and integrated plant closure.

Until those steps exist, SFR-2 remains a **computational hypothesis with a reproducible low-authority screen**.
