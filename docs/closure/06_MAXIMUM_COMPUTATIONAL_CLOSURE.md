# SFR-1 v0.4 Maximum Computational Closure

## Objective

Push every unresolved reactor item as far as reproducibly possible without replacing production science tools by lower-authority surrogates.

## G1 — equilibrium

The reduced SFR-1 boundary is converted exactly into VMEC Fourier coefficients and four finite-pressure fixed-boundary namelists. The generator derives the seed pressure from beta and magnetic pressure and derives a toroidal-flux screen from `B*pi*a^2`. These are solver **inputs**, not equilibrium outputs.

DESC and VMEC++ execution adapters are included. A G1 pass requires convergence, force-residual evidence, finite-beta metrics and cross-code agreement. This runtime did not contain either production solver, so G1 remains open at production authority.

## G2 — magnet architecture

Three successive architecture classes now exist in the evidence history:

1. planar encircling loops — rejected;
2. richer fixed filament basis — rejected on held-out points;
3. v0.4 new work:
   - TF + classical helical winding scan with direct Biot-Savart field-line integration;
   - continuous Fourier current-potential winding-surface reconstruction with separate fitting and validation nodes.

The best classical-helical case preserves the excursion screen but yields insufficient transform. The current-potential family retains percent-level held-out normal-field error. Therefore the boundary and coil geometry must become a single-stage/quasi-single-stage optimization variable set rather than a fixed boundary followed by coil fitting.

The HTS module calculates only geometric bend/strain proxies. It never converts a geometric pass into winding-pack qualification.

## G3/G4 — confinement

The repository closes the required `tau_E`/ISS04 screening target and quantifies vacuum field-line iota/nestedness for the executed magnet architectures. It does not claim kinetic confinement. Production promotion requires energetic-particle guiding-center evidence, neoclassical transport/bootstrap current, nonlinear gyrokinetics and profile iteration.

## G7 — neutronics/TBR

Exact source and fuel-cycle requirements are calculated from D-T reaction kinematics. For blanket coverage fraction `f`, if uncovered area breeds zero tritium, the necessary local breeder-region average satisfies

`TBR_local >= TBR_global / f`.

For the 1.15 SFR-1 target this becomes 1.278 at 90% breeding coverage, 1.353 at 85%, and 1.438 at 80%. These are exact bounds under the stated assumption, not neutron-transport predictions.

An executable OpenMC axisymmetric CSG torus proxy builder is included for material/nuclear-data sensitivity when OpenMC is installed. It is explicitly barred from G7 final promotion. Final G7 requires the solved 3-D stellarator geometry, ports, divertor and penetrations through OpenMC/DAGMC/ParaStell-class transport.

## G8 — net electric

With the current uniform burn screen of 704.57 MW, 1.15 blanket energy multiplier, 40% gross efficiency and 120 MW recirculating load, the algebraic screen is 204.10 MWe. The 300 MWe floor requires 913.04 MW fusion. The target 1 GW point yields 340 MWe conditional net.

The plant equation is closed; the reactor prediction is not. Real blanket multiplication, heat transport, conversion efficiency, cryogenics, RF/heating, pumps and tritium processing must replace targets after G1–G7.

## G9 — hardware

No computational method can demonstrate actual net-electric fusion. Hardware is a separate evidence authority.
