
# Safety and Assurance Architecture

IX-StellaratorForge does not treat stellarator disruption avoidance as a complete reactor safety case.

## Principal hazard families

- superconducting magnet stored energy and quench;
- tritium inventory and permeation;
- activated structures and shutdown dose;
- decay heat;
- vacuum-boundary failure;
- coolant loss/flow transients;
- plasma-wall off-normal loading;
- cryogenic oxygen-deficiency and pressure hazards;
- high-power RF and electrical systems.

## Defense-in-depth principles

- independent protection does not depend on the research optimizer;
- loss of software optimization cannot defeat magnet, vacuum, tritium or decay-heat protection;
- shutdown removes auxiliary heating and fueling and moves plant systems to bounded safe states;
- quench protection has dedicated sensors and energy-disposal paths;
- tritium uses multiple confinement boundaries and inventory accounting;
- decay-heat removal remains available after plasma termination;
- every high-consequence control decision is logged with state, evidence and authority.

## Assurance inheritance

Concepts from IX-Autonomy-Assurance-Case-Runtime, IX-BlackFox and IX-Sally are retained as **control/evidence architecture only**. They do not substitute for nuclear licensing, certified safety systems or validated hardware.
