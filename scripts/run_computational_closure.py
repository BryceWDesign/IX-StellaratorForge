#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from ix_stellaratorforge.computational_closure import run_computational_closure
from ix_stellaratorforge.reactor import load_reactor_config

def main()->int:
 cfg=load_reactor_config(ROOT/'configs/reactor/sfr1_rev_a.json')
 result=run_computational_closure(cfg,seed_output_dir=ROOT/'external_solvers/inputs')
 # Make paths repository-relative in persisted evidence.
 result['G1_equilibrium']['written_input_paths']=[str(Path(p).relative_to(ROOT)) for p in result['G1_equilibrium']['written_input_paths']]
 out=ROOT/'results/computational_closure/sfr1_v040.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(out.relative_to(ROOT));print(result['top_level_verdict']);return 0
if __name__=='__main__':raise SystemExit(main())
