# Results Ledger

## Release 0.9 status

| Question | Status | Evidence |
|---|---|---|
| Were all seven computational workstreams attempted? | YES | `results/sfr4_integrated/sfr4_integrated_physical_promotion_a_v090.json` |
| Does the expanded physical coil family pass? | NO | 0 of 80 candidates pass combined topology requirements |
| Did production equilibrium run? | NO | DESC and VMEC++ adapters stop because dependencies are unavailable |
| Is alpha confinement established? | NO | gyroradius scale passes, topology prerequisite and guiding-center evidence do not |
| Does the Q=20 design-iota requirement close at H_ISS04=1? | NO | required H is approximately 2.00 after declared bremsstrahlung and alpha deposition |
| Does the selected nominal and steady heat envelope pass? | YES at low authority | 0.294 MW/m2 first wall and 5.724 MW/m2 divertor peak screens |
| Are heat transients, fatigue and component life resolved? | NO | production edge, CFD, FEA and hardware gates remain unrun |
| Does the conditional plant ledger remain positive? | YES conditionally | approximately 339.88 MWe, with no prediction credit |
| Did v0.9 earn fusion progress? | NO | earned credit remains exactly zero |

## Release 0.8 status

| Question | Status | Evidence |
|---|---|---|
| Is the proposed inward/outer AHIS represented as two independent boundaries? | YES at architecture authority | `results/sfr3_dual_boundary/sfr3_dual_boundary_ahis_a_v080.json` |
| Which wall stack wins the declared balanced screen? | DB-A: W/RAFM/PbLi DCLL | score 9 versus 7 and 8 for the comparison stacks |
| Does the selected stack stay under declared temperature ceilings in the 1-D screen? | YES at low authority | 420.7 °C nominal; 632.9 °C steady-upset surface |
| Are inner and outer conditions observable in the declared model? | YES, incompletely | 192 paired locations and 1,736 sensing elements; irradiation/calibration unqualified |
| Do the eleven declared fault scenarios fail as expected? | YES deterministically | expected states exactly reproduce |
| Can every crack be detected? | NO | the silent armor crack remains below sensor sensitivity and requires periodic NDE |
| Do walls or sensors mechanically confine plasma? | NO | magnetic confinement is unchanged; direct credit is zero |
| Did v0.8 move the earned ignition or fusion result? | NO | fusion and ignition improvements remain exactly zero |

## Release 0.7 status

| Question | Status | Evidence |
|---|---|---|
| Does the declared 24-channel basis span the 12-component synthetic challenge? | YES at low authority | `results/sfr3_field_integrity/sfr3_field_integrity_shell_a_v070.json` |
| Does nominal bounded control meet the 60% RMS reduction threshold? | YES: about 65.46% | same result artifact |
| Does one unavailable channel meet the 55% threshold? | YES: about 66.36% | same result artifact |
| Do passive loops receive static/DC correction credit? | NO | passive attenuation is applied only to the declared transient vector |
| Does low sensor confidence suppress active commands? | YES | `PASSIVE_ONLY_SAFE_HOLD` fault scenario |
| Does this establish physical coils or improved confinement? | NO | SFR3-G2 through G9 are `NOT_RUN` |
| Did v0.7 move the earned ignition or fusion result? | NO | fusion and ignition credits are exactly zero |

## Release 0.6 status

| Question | Status | Evidence |
|---|---|---|
| Does phase-programmed magnetic breathing improve both cycle-average proxy and fusion power? | NO in the low-authority screen | `results/sfr2_actuation/sfr2_actuation_overlay_a_v060.json` |
| Does any declared breathing case cross the cycle-average optimistic ignition proxy? | NO | same result artifact |
| Does the 5% synchronous instantaneous peak establish ignition capture? | NO | peak occurs during expansion with about 802.542 MW uniform fusion power; cycle-average proxy is worse |
| Does the 5% traveling-quadrature case improve the ratio? | NOMINALLY, but fusion power falls | ratio 0.961559491; uniform power 997.233 MW before actuator debit |
| Does a global three-toroidal-lobe pattern preserve the 4FP baseline? | NO | `docs/reactor/15_TRILOBE_CONCEPT_TRANSLATION.md` |
| Does an area-preserving repeated poloidal m=3 harmonic earn fusion credit? | NO | zero-dimensional thermodynamic credit is exactly zero |
| Is magnetic-pumping heating demonstrated? | UNKNOWN | requires SFR2A-G3 kinetic evidence |
| Are the auxiliary coils realizable? | UNKNOWN | requires SFR2A-G1/G2 equilibrium and electromagnetic evidence |
| Is sustained burn or net energy demonstrated? | NO | all higher-authority gates remain open |

## Release 0.1 status

| Question | Status | Evidence |
|---|---|---|
| Does the internal POC run reproducibly? | PASS | `results/evidence/IXFUSION-POC-001.json` |
| Does C6 beat the matched control on mean radial-excursion proxy? | YES in reduced model | candidate/baseline JSON |
| Does C6 clear the full predeclared advantage gate? | NO | `results/poc/verdict.json` |
| Does abstract RF feedback improve target spatial-mode purity? | YES in signal model | `results/monte_carlo/rf_robustness.json` |
| Is C6 proven omnigenous? | UNKNOWN | requires solved equilibrium/orbit action |
| Are nested flux surfaces proven? | UNKNOWN | requires high-fidelity equilibrium/field analysis |
| Is fast-particle confinement improved? | UNKNOWN | requires guiding-center analysis |
| Is MHD stability acceptable? | UNKNOWN | requires finite-pressure stability analysis |
| Is turbulent transport improved? | UNKNOWN | requires transport/gyrokinetic analysis |
| Does RF improve a plasma? | UNKNOWN | requires full-wave/deposition/plasma response |
| Is blanket/tritium performance adequate? | UNKNOWN | requires neutronics/fuel-cycle model |
| Is net electricity positive? | UNKNOWN | incomplete plant energy ledger |

This ledger is intentionally less impressive than an unsupported claim.
