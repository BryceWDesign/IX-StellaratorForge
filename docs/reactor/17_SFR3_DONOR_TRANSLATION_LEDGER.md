# SFR-3 donor translation ledger

The seven donor repositories were treated as mechanism libraries, not as transferable physics validation. Their code, materials and claims were screened against the fusion environment before reuse.

| Donor | Keep or adapt | Reject in SFR-3 | Fusion-specific use |
|---|---|---|---|
| AHIS | Distributed sensing, state estimation, watchdogs, fault latching, actuator-authority accounting | Self-healing-hull implications and unqualified PVDF near cryogenic or neutron-hot zones | Magnetic diagnostics, strain/alignment health, quench-aware control |
| PressureX | Passive rate-dependent load shaping and sealed-fluid discipline | Its dimensionally incomplete impact model and any fluid placed in the plasma volume | Warm support impulse damping only |
| IX-Vibe | Measured-FRF targeting, tuned/shunt damping, distributed modal sensing | A generic broadband damping layer as a magnetic solution | Suppress coil-support modes that can create field error |
| IX-Breath | Resource gates, confidence bands, bounded states, independent hard protection | Flexible-vessel breathing or unbudgeted active correction | Active trim is allowed only when sensing, power, thermal and quench margins close |
| IX-GCR-SPE | Protect the smallest high-value zone, graded shielding, penetration monitoring | Direct transfer of space-radiation material performance | Local shield optimization around REBCO, joints, ports and penetrations |
| IX-Shield | Areal-density ledger, weak-direction analysis and geometric coverage | Low-temperature hydrogen-rich materials next to the fusion core | Port-resolved neutron streaming and shield accounting |
| IX-HfTaZen-Shield | Segmentation, compliant interfaces, thermal paths, seam-first design, hotspot monitoring | Routine Hf/Ta plasma-facing armor and re-entry oxidation assumptions | Segmented tungsten armor, graded joints and monitored interfaces |

## Rule used throughout

A pattern survives only if its physical function survives translation. For example, a tuned damper can help preserve coil alignment, but it cannot be relabeled as plasma confinement. A hydride shield can protect a magnet only after 3-D neutronics validates it, and it cannot be credited as an inward force on the plasma.

No donor repository supplied a hidden confinement material. Their real contribution is a more observable, fault-tolerant and mechanically stable magnetic system.
