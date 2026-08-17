# Model Limitations

The strongest internal limitation is that rotational transform is not generated from the
3-D coil/field geometry. This is visible in the `no_axis_helical_shaping` ablation: removing
axis shaping can improve the reduced composite objective because the internal model can
retain its parameterized transform anyway. That behavior is a **model warning**, not an
argument for an axisymmetric stellarator.

Consequences:

- internal optimization must not be interpreted as coil optimization;
- the C6 seed cannot be promoted based on this model alone;
- an equilibrium/coil solver is a mandatory next gate;
- ablations that exploit absent physics are diagnostic of model authority, not physical
  design recommendations.

The current model also lacks finite pressure, self-consistent currents, particle collisions,
turbulence, plasma-wall interaction, neutronics, fuel cycle, and actual plant power.
