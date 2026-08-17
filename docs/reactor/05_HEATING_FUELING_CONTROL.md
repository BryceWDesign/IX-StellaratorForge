
# Heating, Fueling and Control

## ECRH

For the 6 T reference field, the first-harmonic electron cyclotron frequency is approximately 167.95 GHz from `f_ce = eB/(2πm_e)`. Rev A therefore reserves a nominal 170 GHz ECRH architecture.

The 20 MW installed startup envelope is a design allocation, not a prediction of required startup power. POPCON/scenario calculations and 3-D ray/deposition analysis must determine:

- startup heating power;
- launch locations and polarizations;
- resonance access over the startup trajectory;
- absorption and shine-through;
- deposition profile and steering range;
- wall-plug efficiency and recirculating load;
- redundancy and failed-source behavior.

The old IX-Fusion/IX-TunerCore phase-coherence work survives only as actuator/control technology. Spatial RF mode purity cannot promote plasma heating performance.

## Fueling

Rev A uses deep D/T pellet fueling for the core plus edge gas puffing for edge/divertor control. Pellet size, velocity, repetition rate and isotope scheduling remain profile/transport dependent.

## Control architecture

The control system is layered:

1. fast hardware protection for magnets, vacuum and coolant;
2. plasma-state estimation and actuator control;
3. slower supervisory optimization;
4. assurance layer that records provenance and prevents a low-authority model from authorizing a high-consequence state change;
5. human authority for safety-critical mode transitions.

Distributed structural-health sensing inherited conceptually from AHIS/IX-AeroIntegrity is applied to coil cases, supports, vacuum boundaries, coolant manifolds and replaceable in-vessel modules.
