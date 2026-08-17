
# Parameter Authority and Anti-Fiction Rule

IX-StellaratorForge separates **choosing a number** from **proving a number**.

## Authority classes

### Physical constant

An accepted physical constant or reaction energy. These can support exact arithmetic within the stated model.

### Derived screening

A transparent calculation from declared inputs, such as the 14.1/17.6 D-T neutron-power fraction or the electron cyclotron frequency at 6 T. Screening equations may check consistency but cannot promote reactor feasibility.

### Reference-informed target

A design target selected because contemporary stellarator/reactor work demonstrates that the regime is worth investigating. It is not evidence that SFR-1 achieves the value.

### Design target

A program requirement chosen by IX-StellaratorForge. Examples include 1 GW fusion-power class, full-3D TBR target ≥1.15 and net-electric floor ≥300 MW.

### Solver-dependent

A number that must emerge from high-authority computation: equilibrium, alpha loss, turbulent transport, local wall loading, coil stresses, TBR, nuclear heating, ECRH deposition, pumping, thermal-hydraulics and full-system power balance.

### Experiment-dependent

A property that software cannot certify: conductor performance in the actual winding pack, joints, quench behavior, irradiation endurance, component lifetime, tritium-system behavior, plasma performance and integrated hardware operation.

## Promotion rule

A lower-authority value may kill a design but may not crown one. If an optimistic reduced model says a candidate is excellent while a higher-authority solver says it fails, the higher-authority result controls.

## Exact ledger

The machine-readable parameter classification is `configs/reactor/parameter_ledger.json`.
