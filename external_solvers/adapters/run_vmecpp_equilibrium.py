#!/usr/bin/env python3
"""Run a real VMEC++ fixed-boundary equilibrium and write wout + execution receipt."""
from __future__ import annotations
import argparse, hashlib, importlib.util, json
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("input",type=Path); ap.add_argument("--wout",type=Path,required=True); ap.add_argument("--receipt",type=Path,required=True); args=ap.parse_args()
    if importlib.util.find_spec("vmecpp") is None:
        raise SystemExit("VMEC++ is not installed. No surrogate will be substituted.")
    import vmecpp  # type: ignore
    inp=vmecpp.VmecInput.from_file(str(args.input))
    out=vmecpp.run(inp)
    args.wout.parent.mkdir(parents=True,exist_ok=True); out.wout.save(str(args.wout))
    iota=[]
    try: iota=[float(x) for x in out.mercier.iota]
    except Exception: pass
    receipt={"tool":"VMEC++","input":str(args.input),"input_sha256":sha256(args.input),"wout":str(args.wout),"wout_sha256":sha256(args.wout),"iota":iota,"executed_at_utc":datetime.now(timezone.utc).isoformat(),"success":True,"authority":"production_solver_execution_receipt_not_automatic_scientific_promotion"}
    args.receipt.parent.mkdir(parents=True,exist_ok=True);args.receipt.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
    return 0
if __name__=="__main__": raise SystemExit(main())
