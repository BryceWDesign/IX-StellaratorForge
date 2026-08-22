# SFR-4 Integrated Physical-Promotion Campaign A

Verdict: `INTEGRATED_REDUCED_CAMPAIGN_COMPLETE__NOMINAL_HEAT_ENVELOPE_SCREEN_PASS__PHYSICAL_COIL_EQUILIBRIUM_CONFINEMENT_AND_FUSION_UNPROVEN`

## Seven-workstream result

1. Physical coil field: 80 direct-filament candidates executed; 0 passes. Best reduced candidate has mean iota 0.065333 and normalized maximum radial excursion 0.192225. No coil is promoted.
2. Finite-beta equilibrium: not run. Available production tools: none. Unavailable: desc, vmecpp, simsopt, openmc, dolfinx, fenics, gmsh, cadquery.
3. Coil/plasma co-design: reduced geometry/current scan executed; production single-stage co-design not run.
4. Particle confinement: 3.5 MeV alpha gyroradius scope is 0.044900 m, but no guiding-center retention is credited because the topology prerequisite fails.
5. Burn: design-iota Q=20 screen requires H_ISS04 1.999672 after the declared bremsstrahlung and alpha-deposition assumptions. It is not linked to a passing physical coil.
6. Magnet engineering: magnetic-pressure, stored-energy and centerline geometry scopes executed; peak conductor field, winding-pack FEA and quench qualification remain open.
7. Reactor systems: exact D-T source and breeding-coverage constraints plus conditional plant ledger executed. Conditional net electric algebra is 339.878 MWe, with no prediction credit.

## Heat result

Plasma exhaust in the declared Q=20 target ledger: **228.977 MW**.
Controlled radiation requirement: **137.386 MW**, producing a first-wall peak screen of **0.294 MW/m2**.
Divertor power: **91.591 MW**, producing a selected peak screen of **5.724 MW/m2** over 24 m2 effective wetted area.
Divertor tungsten surface screen: **678.3 C**.
First-wall surface screen: **401.2 C nominal**, **523.8 C at the declared 1 MW/m2 steady upper bound**.
Water-loop screen: **426.0 kg/s**, **7.56 m/s**, **0.122 MW** across 960 parallel channels.
Selected heat-flux envelope pass: **True**.

The heat result is a requirement-level resolution for nominal and declared steady conditions. Stable detachment, 3-D island footprints, critical heat flux, erosion, cyclic fatigue, disruptions, coolant accidents and component qualification remain unproven.

## Scientific boundary

Earned fusion-progress credit remains exactly **0.0** because no physical coil passes, no finite-beta equilibrium is solved, and no particle/transport or sustained-burn calculation is promoted.
