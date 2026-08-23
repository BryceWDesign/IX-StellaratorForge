# SFR-5 Promotion Gates

SFR-5 is deliberately structured so that a software search decision cannot promote itself into a physics result.

| Gate | Required evidence | Base v0.10 status |
|---|---|---|
| SFR5-G0 | Reproduce SFR-4 magnetic autopsy, preserve independent evidence lanes, reject brute-force continuation | PASS_REDUCED |
| SFR5-G1 | Movable plasma, winding-surface and coil geometry plus real sensitivities | NOT_RUN |
| SFR5-G2 | Constrained winding-surface/global coil feasibility with normal-field, complexity and force/support limits | NOT_RUN |
| SFR5-G3 | Discrete nonplanar coil curves/currents with spacing, curvature, finite-build follow-up and reproducible receipt | NOT_RUN |
| SFR5-G4 | Single-stage coil/plasma co-design plus finite-beta equilibrium and independent/cross-code confirmation | NOT_RUN |
| SFR5-G5 | Guiding-center/alpha confinement, neoclassical transport and turbulent-transport evidence | NOT_RUN |
| SFR5-G6 | 3-D heat exhaust, magnet forces/strain/quench and full 3-D neutronics/TBR | NOT_RUN |
| SFR5-G7 | Coupled burn, fuel cycle, recirculating power and net-electric plant ledger | NOT_RUN |
| SFR5-G8 | Representative hardware, metrology, electromagnetic/thermal testing, fault and safety evidence | NOT_RUN |

## Preferred method ladder

The base release names methods, not results:

1. QUADCOIL or an equivalent differentiable constrained winding-surface/global proxy;
2. SIMSOPT or an equivalent constrained discrete-filament optimizer;
3. simultaneous plasma-boundary and coil co-design coupled to VMEC/DESC-class equilibrium;
4. particle, neoclassical and turbulent-transport evaluation;
5. 3-D edge/divertor, OpenMC/DAGMC-class neutronics, structural/thermal analysis and HTS qualification;
6. integrated plant and hardware evidence.

An unavailable tool remains unavailable. A proxy may eliminate a family but may not inherit the authority of a production solver.
