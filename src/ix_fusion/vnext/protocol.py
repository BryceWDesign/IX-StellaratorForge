"""The vNext scientific-promotion protocol."""
from __future__ import annotations

from .authority import Authority
from .gates import GateSpec


GATES: tuple[GateSpec, ...] = (
    GateSpec("G0_SEED", Authority.REDUCED_MODEL, ("reduced_screen", "negative_control")),
    GateSpec("G1_EQUILIBRIUM", Authority.EQUILIBRIUM_SOLVER, ("nested_surfaces", "self_consistent_iota", "finite_beta_scan")),
    GateSpec("G2_COILS", Authority.COIL_REALIZATION, ("normal_field_error", "coil_clearance", "coil_strain", "support_stress", "coil_error_robustness")),
    GateSpec("G3_ORBITS", Authority.ORBIT_TRANSPORT, ("direct_J", "fast_alpha_loss", "neoclassical_transport")),
    GateSpec("G4_TURBULENCE", Authority.MULTIPHYSICS, ("nonlinear_heat_flux", "particle_flux", "profile_transport")),
    GateSpec("G5_EDGE", Authority.MULTIPHYSICS, ("divertor_topology", "peak_heat_flux", "edge_robustness", "vessel_clearance")),
    GateSpec("G6_RF", Authority.MULTIPHYSICS, ("ecrh_deposition", "absorption", "steering_robustness", "recirculating_power")),
    GateSpec("G7_NEUTRONICS", Authority.MULTIPHYSICS, ("coil_nuclear_heating", "shielding_margin", "blanket_radial_build", "penetration_weak_zones")),
    GateSpec("G8_SYSTEM", Authority.MULTIPHYSICS, ("net_power_balance", "maintenance_access", "uncertainty_campaign", "matched_baseline_advantage")),
)
