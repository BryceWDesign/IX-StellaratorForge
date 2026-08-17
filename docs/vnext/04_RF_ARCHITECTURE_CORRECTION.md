# RF Architecture Correction

## What survives from IX-Fusion / IX-TunerCore

- deterministic source timing;
- PLL/DDS-style frequency and phase stabilization;
- amplitude/phase error injection;
- calibration and feedback abstractions;
- actuator-health telemetry.

## What is removed as a scientific claim

The six-source spatial-mode purity metric is **not** accepted as evidence that a plasma will absorb power at the desired location, suppress an instability, drive current, or improve confinement.

## Replacement objective

For each promoted equilibrium, RF/ECRH evaluation must model:

1. launch geometry and polarization;
2. frequency and magnetic-resonance location;
3. 3-D ray/full-wave propagation;
4. absorbed-power profile and localization;
5. steering/frequency robustness to equilibrium variation;
6. density/accessibility constraints;
7. total source/transmission/recirculating-power burden;
8. actuator fault tolerance.

Source synchronization is therefore a **control implementation variable**, while deposition/absorption and system power are the physics objectives.
