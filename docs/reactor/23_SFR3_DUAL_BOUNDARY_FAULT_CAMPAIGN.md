# Dual-boundary fault campaign

Eleven deterministic scenarios are executed under versioned signal, channel-failure and expected-state definitions.

| Scenario | Result |
|---|---|
| Nominal | `NOMINAL` |
| Inner hotspot with lane A temperature failure | Detected by lane B; controlled power rundown |
| Coolant leak with one interspace channel failed | Detected by surviving coolant/interspace channels; isolate and safe hold |
| Outer support shift plus flux error | Request bounded SFR-3 trim, then inspect |
| Complete inner lane A loss | Degraded monitoring with lane B retained |
| Complete outer lane A loss | Degraded monitoring with lane B retained |
| Both sector buses lost | Safe hold due to lost observability |
| Vacuum breach | Isolate and safe hold |
| Total control-power loss | Passive hard safe hold |
| Silent armor crack below online sensitivity | No automatic detection; periodic NDE required |
| Support shift with trim unavailable | Safe hold; no uncorrected operation |

The silent-crack case is essential. A monitoring system cannot be allowed to claim total coverage merely because every simulated signal was detected. Real probability of detection requires seeded flaws, irradiated materials, calibrated inspection hardware and blind tests.

The campaign validates deterministic control routing only. It does not establish detection probability, safe shutdown time, allowable leak size, structural margin or licensing classification.
