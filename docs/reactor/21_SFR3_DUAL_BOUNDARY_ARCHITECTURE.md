# SFR-3 Dual Boundary Integrity Network

## Translation of the user's proposal

“AHIS flipped inside out” is interpreted as an inward-facing health-monitoring network behind the plasma-facing wall. It observes temperature, strain, coolant state and magnetic disturbance. It does not exert mechanical pressure on plasma.

The second AHIS layer faces outward. It observes the vacuum-vessel interspace, shield, supports, vibration and magnet alignment. The two networks share no single sensing lane or power dependency that is intentionally credited as independent.

## Why a double wall helps

A double wall provides an interspace that can be evacuated, pressure-monitored and helium-leak tested. It adds defense in depth for vacuum and radioactive inventory, provides space for shielding and cooling, and makes some leak paths observable before the outer boundary is lost.

It does not add a second magnetic surface. If plasma reaches the material wall, magnetic confinement has already degraded. The permitted response is to correct a measured field error, reduce plasma power, isolate coolant, enter safe hold and inspect or replace the affected sector.

## Spatial architecture

The 24 toroidal sectors align with the 24 SFR-3 trim channels. Each sector contains eight poloidal monitoring locations, producing 192 paired inner and outer locations. Two sensing lanes provide nominal single-channel tolerance. Hard vacuum channels are independent of the model-based estimator.

This layout is deliberately dense because a localized first-wall event cannot be safely inferred from a single global sensor. Final placement must be optimized against neutron dose, feedthrough count, maintenance access and observability rank.

## Integration with magnetic correction

An outer support displacement becomes actionable only when it correlates with a magnetic flux error and SFR-3 trim resources remain healthy. The v0.8 screen reuses the SFR-3 synthetic 65.46% correction result solely to verify control routing. It does not convert structural monitoring into physical confinement evidence.
