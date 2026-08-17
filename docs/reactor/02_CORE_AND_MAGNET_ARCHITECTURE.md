
# Core and Magnet Architecture

## Core optimization

The magnetic core is deliberately unresolved at Rev A. The 3FP, 4FP, 6FP, QA reference and direct-J search branches must be optimized against the **same reactor envelope** and the same penalty structure.

The primary physics path is:

1. finite-beta fixed-boundary DESC search;
2. direct-J / omnigenity and neoclassical objectives where available;
3. free-boundary coil realization;
4. VMEC++ independent equilibrium cross-check for promoted finalists;
5. direct guiding-center alpha calculations;
6. stability and nonlinear transport;
7. edge/divertor compatibility.

## Why direct-J matters

The inherited IX-Fusion bounce-action quantity was only a reduced proxy. Current 2026 work demonstrates differentiable optimization of the second adiabatic invariant directly inside DESC, including compact four-field-period examples with strong fast-ion performance and coil compatibility. SFR-1 therefore treats direct trapped-orbit action as a promotion metric rather than continuing to optimize the old proxy.

## QI-pwO branch

Strict QI can demand strong shaping and difficult coils. The 4FP branch allows piecewise-omnigenous relaxation on the high-field side so the optimization can trade a limited relaxation of geometric QI structure for better coil, blanket, port and maintenance feasibility while still demanding acceptable neoclassical/orbit performance.

## Magnet target

Rev A assumes a REBCO-class HTS winding technology target:

- nominal operating temperature: 20 K;
- on-conductor field ceiling: 20 T;
- winding strain target ≤0.35%;
- hard screening ceiling ≤0.40%;
- plasma-to-primary-coil target ≥1.35 m;
- support geometry optimized jointly with the winding rather than added after field optimization.

These are design constraints. No SFR-1 coil has yet demonstrated them.

## Coil selection objective

A coil set is unacceptable if it cannot simultaneously achieve:

- required boundary normal-field accuracy;
- adequate coil-coil and coil-vessel clearance;
- acceptable REBCO tape strain over the full winding pack;
- acceptable support stresses and deflection;
- quench detection/protection strategy;
- manufacturing and alignment-error robustness;
- maintenance windows for replaceable in-vessel sectors;
- neutron lifetime consistent with the plant architecture.

This is intentionally stricter than a magnetic-only coil optimization.
