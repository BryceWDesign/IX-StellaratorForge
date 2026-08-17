# High-fidelity execution plan

The current runtime contains NumPy/SciPy/JAX but not DESC, VMEC++, SIMSOPT or OpenMC, and its Python package manager cannot reach the public package index. The repository therefore records exact solver promotion contracts instead of substituting homemade output for those codes.

When the solver environment is available, execute in this order:

1. **G1:** Generate finite-beta equilibria for the 2FP QA reference, 3FP QI, 4FP QI/pwO, 6FP C6/QI and direct-J search families with DESC. Archive convergence/force-balance metrics and input profiles. Cross-check promoted finalists with VMEC++.
2. **G2:** Co-optimize coils with the solved plasma boundary using DESC/SIMSOPT-class tooling. Add REBCO field/strain constraints, Lorentz loads, structural FEA, clearance and stochastic manufacturing errors.
3. **G3:** Compute alpha/guiding-center loss and direct-J metrics, plus neoclassical heat/particle transport and bootstrap current.
4. **G4:** Run nonlinear gyrokinetics and iterate plasma profiles until heat/particle sources and transport close.
5. **G5:** Optimize the edge/divertor/vessel together; reject candidates without a credible exhaust solution.
6. **G6:** Run 3-D ECRH propagation/deposition on the surviving equilibrium and include wall-plug power in recirculating load.
7. **G7:** Build full stellarator CAD/DAGMC neutronics geometry and run Monte Carlo TBR/heating/dose/streaming calculations.
8. **G8:** Recompute the plant from the solver-derived fusion power, blanket multiplication, thermal limits, gross efficiency and itemized recirculating loads. Propagate uncertainty.
9. **G9:** Hardware only. No software result may promote it.

The machine-readable contract is `configs/closure/high_fidelity_solver_contract.json`.
