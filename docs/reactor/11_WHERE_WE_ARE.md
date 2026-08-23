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
- Version 0.6 adds an optional, separately gated magnetic-breathing and tri-lobe actuation overlay without modifying SFR-2 Rev A.
- The overlay tests synchronous, ABAB-opposed and traveling-quadrature cycles and rejects all declared cases as joint cycle-average improvements.
- The tri-lobe image is retained only as an area-preserving repeated poloidal m=3 actuator hypothesis; it receives no astrophysical, three-body or thermodynamic fusion credit.
- Version 0.7 adds SFR-3 Field Integrity Shell A after auditing seven donor repositories for transferable mechanisms.
- SFR-3 combines 24 synthetic active trim channels, passive superconducting transient loops, confidence-aware diagnostics, fail-closed control, support-mode damping and geometry-aware magnet shielding.
- Its deterministic low-authority screen passes nominal, one-channel-fault, passive-only and safe-hold requirements while assigning zero physical confinement or fusion credit.
- Version 0.8 adds Dual Boundary AHIS A to the complete repository as an inner first-wall/vessel-health lane and an independent outer shield/support/alignment lane.
- The selected reduced-screen stack uses segmented tungsten, a graded W-to-RAFM transition, helium-cooled ODS-Eurofer/RAFM, PbLi with electrical channel inserts, a monitored double-wall vessel, WC/B4C shielding and REBCO-adjacent monitoring.
- The dual-boundary campaign compares three stacks under identical assumptions, checks eleven deterministic states and explicitly preserves one undetectable sub-sensitivity armor-crack case.
- Walls, liquids and sensors receive zero direct plasma-confinement, ignition, fusion and safety credit.
- Version 0.9 adds SFR-4 Integrated Physical-Promotion Campaign A and attempts all seven requested workstreams.
- Eighty direct-filament coil cases produce zero combined topology passes. The scanned classical helical family is rejected.
- The selected separated first-wall, blanket and divertor architecture passes its nominal and declared steady reduced heat envelope.
- Production equilibrium, transport, stable detachment, transient heat, qualified magnets, full 3-D TBR and hardware remain unrun.
- Version 0.10 adds SFR-5 Reality Gradient and Adaptive Inverse Design A.
- SFR-5 regenerates the v0.9 magnetic autopsy from committed evidence instead of copying diagnostic numbers into a new claim.
- The fixed helical plus fixed hybrid filament-basis family is stored as rejected for the preferred next search, with explicit evidence required before reopening.
- Plasma-boundary, winding-surface, nonplanar-coil and current degrees of freedom are opened for the next search; no geometry sensitivity or replacement coil result is fabricated in the base release.

## What v0.10.0 actually found

The SFR-4 failure contains a representation-level diagnosis. The best helical topology lane would need about 3.8265 times its present mean transform merely to reach the minimum iota gate while retaining only about 3.887% normalized radial-excursion slack. A separate held-out richer basis remains about 12.9825 times above its normal-field RMS limit.

Because those diagnostics come from different reduced representations, SFR-5 keeps them in independent evidence lanes. Their joint meaning is not that stellarators fail. Their joint meaning is that more brute-force sampling of the same fixed family is a poor next allocation of compute.

SFR-5 therefore opens the plasma boundary, winding surface, nonplanar coil geometry, current groups and engineering keep-outs as coupled design variables. The base release computes constraint pressure but records geometry sensitivities and the backward Reality Gradient as `NOT_RUN` until a real movable-geometry solver is connected.

## What v0.9.0 actually found

The magnet result is negative. The best scoring six-field-period filament case reaches approximately 0.0653 mean iota, well below the 0.25 minimum, although its radial-excursion screen passes. The richer held-out reconstruction remains approximately 6.49% RMS normal field against a 0.5% screen.

The heat result is conditionally positive. At the declared 1 GW, Q=20 target ledger, 60% controlled radiation and 24 m2 effective divertor wetted area produce approximately 0.294 MW/m2 first-wall peak and 5.724 MW/m2 divertor peak. One-dimensional temperature and hydraulic screens pass for the selected separated helium/PbLi/water architecture.

This does not move the earned fusion result because the heat solution has no passing physical magnetic configuration to protect.

## What v0.8.0 actually found

The balanced scoring model selects the helium-cooled tungsten/RAFM/PbLi DCLL stack. Its deliberately simple 1-D thermal result is 420.7 °C at the declared nominal heat flux and 632.9 °C at the steady-upset upper bound. The raw coefficient-of-thermal-expansion mismatch proxy is about 0.212%; this is not a stress calculation or structural qualification.

The architecture provides 192 paired monitoring locations distributed over 24 toroidal control sectors and eight poloidal stations, with 1,736 declared elements across independent inner and outer lanes. All eleven expected deterministic states reproduce. The silent-crack negative control remains undetected, correctly preventing a perfect-detection claim.

This improves the engineering hypothesis by making fault isolation, coolant isolation, safe hold, inspection and magnetic-alignment response testable. It does not improve the earned ignition proxy or establish plasma confinement.

## What v0.7.0 actually found

The declared 12-by-24 synthetic response matrix is full row rank. Bounded active commands reduce the declared combined challenge by about 65.46% nominally and 66.36% with one unavailable channel. A pure transient challenge is reduced by the declared 55% passive coefficient. Low sensor confidence prevents active correction, and a passive-loop quench removes passive credit.

Those results show only that the proposed control decomposition is internally testable. The response matrix is analytic rather than CAD/Biot-Savart-derived, so v0.7.0 does not move the earned confinement, ignition or fusion result.

## What v0.6.0 actually found

No declared breathing waveform improves both the cycle-average optimistic ignition ratio and cycle-average uniform fusion power. The closest ratio is 0.961559491 at 5% traveling quadrature, but uniform fusion power falls to 997.233 MW before actuator losses. The 5% synchronous case has an instantaneous 0.998114154 peak during expansion, when uniform fusion power falls to about 802.542 MW. Its cycle-average ratio is worse than baseline, so it is not credited as ignition capture or sustained burn.

The concept image helps define a balanced auxiliary actuation experiment. It does not itself move the design closer to fusion.

## What v0.5.0 actually found

The primary SFR-2 screen uses `H_ISS04=1.0` and compares all declared cases at the same 1 GW uniform D-T fusion-power target.

No primary case crosses the deliberately optimistic alpha-only ignition proxy. The strongest point is the uncompressed 15 T, `iota(2/3)=0.9` case with a confinement ratio of about 0.961 and a required `H_ISS04` of about 1.0405.

That is not a statement that the design is “4% from fusion.” It is only the gap inside one low-authority empirical/analytical screen.

An important correction also emerged: ideal radial compression does not automatically improve this target-power-matched ISS04 proxy. At the strongest declared field/transform point, 5% and 10% squeeze reduce the ratio rather than increase it. The repository retains that negative result rather than forcing the dynamic-compression hypothesis to pass.

## What this means

The project now contains **four reactor-level research branches plus two integrated design/engineering layers with different roles**:

- **SFR-1:** steady-state reference architecture and production-solver path.
- **SFR-2:** dynamic/high-field assumption breaker designed to test whether a staggered, strongly transformed, phase-actuated concept earns survival through progressively higher-authority physics.
- **SFR-3:** field-integrity overlay designed to preserve a steady stellarator field against error, motion and faults without changing the vessel or inventing material confinement.
- **Dual Boundary AHIS A:** engineering-health overlay designed to detect inner-wall, vessel, shield and support problems and coordinate protective actions without touching the plasma or replacing magnetic confinement.
- **SFR-4:** integrated promotion and heat-exhaust campaign that rejects the present coil family while retaining a testable steady heat-removal requirement.
- **SFR-5:** adaptive inverse-design layer that converts failed constraints into a governed family-switch/search program and opens coupled plasma/winding-surface/coil degrees of freedom without granting unearned physics credit.

No branch or layer has demonstrated ignition, reactor safety or reactor feasibility.

## The single most important next action

For SFR-3, the decisive next action is **SFR3-G2 physical coil response**: replace the analytic matrix with CAD-linked Biot-Savart responses including primary coils, trim coils, passive loops, blanket steel, shielding, ports and as-built errors. The following SFR3-G3 equilibrium/island campaign must then determine whether correction preserves nested surfaces.

For Dual Boundary AHIS A, the decisive next action is a coupled CAD-based thermal, electromagnetic and structural model of the selected geometry, followed by W/RAFM joint coupons, PbLi/coolant compatibility loops, calibrated interspace leak tests and sensor irradiation. The low-authority pass cannot substitute for any of those experiments.

For SFR-4/SFR-5, the decisive next action is to execute SFR5-G1 through G4: connect a real movable-geometry sensitivity path, run constrained winding-surface feasibility, realize discrete nonplanar modular coils, then perform single-stage coil/plasma optimization against finite-beta equilibrium with independent/cross-code confirmation. More current in the rejected classical helices is not a defensible next step.

For SFR-2, the decisive next action remains **SFR2-G1 dynamic equilibrium**: construct a real finite-beta ABAB 3-D equilibrium and determine whether the requested transform survives the proposed actuation/compression cycle without destructive islands, stochastic regions or MHD failure.

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
