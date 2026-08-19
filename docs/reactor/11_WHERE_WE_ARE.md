# Where IX-StellaratorForge Is Now

## Completed

- The original IX-Fusion reduced-order result is preserved rather than rewritten.
- SFR-1 Rev A remains a parameterized steady-state reference architecture with explicit reactor subsystem targets and authority labels.
- SFR-1 v0.4 maximum in-repository computational closure is preserved, including its negative magnet results and open production-solver/hardware gates.
- SFR-2 Rev A now exists as a separately gated assumption-breaker candidate based on the 23/26/23/26 ft ABAB concept.
- SFR-2 is encoded as one continuous closed toroidal plasma system, not four independent plasmas connected by ducts.
- The SFR-2 screen reproduces geometry bookkeeping, Bosch-Hale burn physics, ideal radial-compression thermodynamics, target-power matching and ISS04 transform sensitivity.
- SFR-2 assigns zero numerical benefit to ABAB staggering, unmodeled traveling-wave/RF heating, magnetic pumping or magnetic-flux amplification.
- Every high-authority SFR-2 physics/engineering gate remains `NOT_RUN`.

## What v0.5.0 actually found

The primary SFR-2 screen uses `H_ISS04=1.0` and compares all declared cases at the same 1 GW uniform D-T fusion-power target.

No primary case crosses the deliberately optimistic alpha-only ignition proxy. The strongest point is the uncompressed 15 T, `iota(2/3)=0.9` case with a confinement ratio of about 0.961 and a required `H_ISS04` of about 1.0405.

That is not a statement that the design is “4% from fusion.” It is only the gap inside one low-authority empirical/analytical screen.

An important correction also emerged: ideal radial compression does not automatically improve this target-power-matched ISS04 proxy. At the strongest declared field/transform point, 5% and 10% squeeze reduce the ratio rather than increase it. The repository retains that negative result rather than forcing the dynamic-compression hypothesis to pass.

## What this means

The project now contains **two reactor-level research branches with different roles**:

- **SFR-1:** steady-state reference architecture and production-solver path.
- **SFR-2:** dynamic/high-field assumption breaker designed to test whether a staggered, strongly transformed, phase-actuated concept earns survival through progressively higher-authority physics.

Neither branch has demonstrated ignition or reactor feasibility.

## The single most important next action

For SFR-2, the decisive next action is **SFR2-G1 dynamic equilibrium**: construct a real finite-beta ABAB 3-D equilibrium and determine whether the requested transform survives the proposed actuation/compression cycle without destructive islands, stochastic regions or MHD failure.

For SFR-1, the corresponding next action remains the G1 DESC/VMEC++ finite-beta equilibrium tournament already defined in v0.4.

## What would materially change confidence in SFR-2

The first major confidence jump requires one SFR-2 candidate to demonstrate, on the same geometry:

1. converged finite-beta equilibrium throughout the actuation cycle;
2. acceptable magnetic surfaces/island behavior and MHD stability;
3. strong thermal and alpha-particle confinement;
4. neoclassical and turbulent transport compatible with the burn target;
5. physically realizable coils/current systems at the demanded field and bandwidth;
6. RF/phase-control deposition that provides actual useful energy transfer rather than an assumed benefit.

Only after that would transient heat flux, 3-D neutronics/TBR and integrated plant closure become meaningful promotion evidence.
