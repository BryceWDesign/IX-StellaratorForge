#!/usr/bin/env python3
"""Check completeness of a production G3/G4 evidence JSON against the SFR-1 contract.

This validates provenance/completeness only; it does not invent universal transport thresholds.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path

REQUIRED={
 "identity":["candidate_id","equilibrium_solver","equilibrium_output_sha256","transport_tool_versions","input_hashes","execution_environment"],
 "energetic_particles":["alpha_birth_distribution_definition","loss_fraction_vs_time","loss_energy_and_wall_location_distribution","orbit_or_direct_J_metric","numerical_convergence_or_step_sensitivity"],
 "neoclassical":["particle_flux_vs_radius","ion_and_electron_heat_flux_vs_radius","bootstrap_current_profile","collisionality_and_Er_scan","numerical_convergence"],
 "gyrokinetic":["linear_growth_rate_scan","nonlinear_ion_heat_flux","nonlinear_electron_heat_flux_or_documented_model_boundary","particle_flux","gradient_and_resolution_sensitivity"],
 "profile_closure":["heating_and_alpha_source_profiles","transport_iteration_convergence","density_and_temperature_profiles","fusion_power_from_profiles","required_auxiliary_power"]
}

def main()->int:
 ap=argparse.ArgumentParser();ap.add_argument('evidence',type=Path);args=ap.parse_args();d=json.loads(args.evidence.read_text())
 missing=[]
 for section,keys in REQUIRED.items():
  obj=d if section=='identity' else d.get(section,{})
  for key in keys:
   if key not in obj or obj[key] in (None,"",[],{}): missing.append(f'{section}.{key}')
 if d.get('executed') is not True: missing.append('executed=true')
 if missing:
  print(json.dumps({'complete':False,'missing':missing},indent=2));return 2
 print(json.dumps({'complete':True,'note':'Evidence fields are present; scientific acceptance still requires threshold/reference analysis.'},indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
