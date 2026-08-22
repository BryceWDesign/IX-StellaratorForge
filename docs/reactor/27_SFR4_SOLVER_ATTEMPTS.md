# SFR-4 Production Solver Attempts

The build runtime was audited before reduced calculations were accepted.

| Tool or route | Attempt result | Repository behavior |
|---|---|---|
| DESC Python package | Not installed | DESC adapter exited 1 and produced no equilibrium claim |
| VMEC++ Python package | Not installed | VMEC++ adapter exited 1 and produced no equilibrium claim |
| SIMSOPT | Not installed | Production coil/plasma co-design remains not run |
| OpenMC | Not installed | OpenMC builder exited 1 when execution was requested and produced no TBR claim |
| FEniCS or DOLFINx | Not installed | Structural and conjugate thermal FEA remain not run |
| Gmsh and CADQuery | Not installed | Configuration-controlled CAD and mesh gates remain not run |
| Package installation route | Attempted | Runtime network policy prevented dependency retrieval |

The adapters behaved correctly: each stopped rather than substituting an in-repository surrogate. Generated seed inputs remain available for execution in a qualified external environment.
