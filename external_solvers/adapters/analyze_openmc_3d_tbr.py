#!/usr/bin/env python3
"""Extract TBR from a real 3-D OpenMC statepoint containing a named tritium tally."""
from __future__ import annotations
import argparse, importlib.util, json
from pathlib import Path

def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument("statepoint",type=Path);ap.add_argument("--tally",default="TBR");ap.add_argument("--output",type=Path,required=True);args=ap.parse_args()
    if importlib.util.find_spec("openmc") is None: raise SystemExit("OpenMC is not installed")
    import openmc  # type: ignore
    with openmc.StatePoint(args.statepoint) as sp:
        tally=sp.get_tally(name=args.tally); mean=float(tally.mean.sum()); std=float((tally.std_dev**2).sum()**0.5)
    payload={"statepoint":str(args.statepoint),"tally":args.tally,"TBR_mean_per_source":mean,"TBR_combined_std_dev":std,"passes_1p10_floor":bool(mean-2*std>=1.10),"passes_1p15_target":bool(mean-2*std>=1.15),"authority":"OpenMC_statepoint_analysis; promotion additionally requires validated 3D geometry/materials/source/nuclear_data"}
    args.output.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n");print(json.dumps(payload,indent=2));return 0
if __name__=="__main__":raise SystemExit(main())
