#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from ix_stellaratorforge.poc import run_sfr1_poc
from ix_stellaratorforge.reactor import load_reactor_config
from ix_stellaratorforge.readiness import build_readiness_report

def main()->int:
 cfg=load_reactor_config(ROOT/'configs/reactor/sfr1_rev_a.json')
 poc=run_sfr1_poc(cfg);p=ROOT/'results/sfr1_poc/sfr1_poc_v040.json';p.write_text(json.dumps(poc,indent=2,sort_keys=True)+'\n')
 comp_path=ROOT/'results/computational_closure/sfr1_v040.json'
 if not comp_path.exists(): raise SystemExit('run scripts/run_computational_closure.py first')
 comp=json.loads(comp_path.read_text())
 ready=build_readiness_report(cfg)
 ready['maximum_computational_closure_v0_4']={
   'verdict':comp['top_level_verdict'],
   'G1':comp['G1_equilibrium']['status'],
   'G2':comp['G2_magnets']['status'],
   'G3_G4':comp['G3_G4_confinement']['status'],
   'G7':comp['G7_neutronics']['status'],
   'G8':comp['G8_net_electric']['status'],
   'G9':comp['G9_hardware']['status'],
   'authority_note':'Supplemental in-repo closure layer; formal G1-G9 promotion_status remains unchanged until production evidence is committed.',
 }
 (ROOT/'results/reactor/sfr1_rev_a_readiness.json').write_text(json.dumps(ready,indent=2,sort_keys=True)+'\n')
 print(p.relative_to(ROOT));print('results/reactor/sfr1_rev_a_readiness.json');return 0
if __name__=='__main__':raise SystemExit(main())
