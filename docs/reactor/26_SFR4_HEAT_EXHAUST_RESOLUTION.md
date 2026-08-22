# SFR-4 Heat-Exhaust Resolution

## Problem split

The heat problem is split into three independent domains:

1. Distributed plasma radiation reaches the first wall.
2. Parallel exhaust power reaches the divertor targets.
3. Neutron power heats the breeding blanket and shield.

Treating all three as one wall heat flux would hide the dominant physics and coolant incompatibilities.

## Selected reduced-screen architecture

The declared Q=20 target ledger supplies 228.98 MW of plasma exhaust after the 90% alpha-deposition assumption. A controlled-radiation requirement sends 60% to approximately 536.9 m2 of first-wall area. The remaining 40% reaches a 24-sector long-leg island-divertor requirement with 24 m2 effective wetted area and a 1.5 peak factor.

The selected first wall is:

* 3 mm segmented tungsten;
* 1 mm graded W-to-RAFM transition;
* 3 mm helium-cooled ODS-RAFM structure; and
* a physically separate PbLi DCLL blanket.

The selected divertor target is:

* 6 mm segmented tungsten;
* 1 mm OFHC copper compliant interlayer;
* 2 mm CuCrZr heat sink; and
* an independent pressurized-water circuit.

Water never shares a boundary, penetration or heat exchanger with PbLi. A double coolant boundary, guard vacuum and independent leak detection are mandatory.

## Executed result

| Quantity | Reduced-screen result | Declared gate |
|---|---:|---:|
| First-wall peak heat flux | 0.294 MW/m2 | at most 0.5 MW/m2 nominal |
| Divertor peak heat flux | 5.724 MW/m2 | at most 10 MW/m2 steady |
| First-wall surface temperature | 401.2 C nominal | layer-specific service ceilings |
| First-wall surface at 1 MW/m2 | 523.8 C | layer-specific service ceilings |
| Divertor tungsten surface | 678.3 C | 1200 C screen |
| Divertor water mass flow | 426.0 kg/s | requirement output |
| Mean flow velocity | 7.56 m/s | at most 10 m/s |
| Hydraulic pumping power | 0.122 MW | at most 5 MW |

At the selected 24 m2 wetted area, at least approximately 30.12% controlled radiation is required to remain below the 10 MW/m2 divertor limit. At 60% radiation, at least approximately 13.74 m2 effective wetted area is required. The selected point therefore has reduced-screen margin.

## Meaning of resolved

The nominal and declared steady heat-allocation problem is resolved at requirement authority: a feasible partition, wetted area, material stack, coolant separation and hydraulic target have been identified in the model.

The physical heat problem is not qualified. The result assumes stable impurity-seeded detachment and the requested island-divertor footprint. It does not solve three-dimensional edge plasma and neutrals, critical heat flux, boiling stability, erosion, redeposition, W/Cu fatigue, neutron degradation, disruptions or accidents. Failure in any of those gates reopens the architecture.
