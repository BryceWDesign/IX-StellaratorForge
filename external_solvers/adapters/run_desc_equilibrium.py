#!/usr/bin/env python3
"""Run a real DESC equilibrium from an SFR-1 VMEC-format seed and write a receipt.

This script intentionally does not fall back to a surrogate if DESC is absent.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--receipt", type=Path, required=True)
    args=ap.parse_args()
    if importlib.util.find_spec("desc") is None:
        raise SystemExit("DESC is not installed. Install the pinned high-fidelity environment; no surrogate will be substituted.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    cmd=[sys.executable,"-m","desc","-vv",str(args.input),"-o",str(args.output)]
    proc=subprocess.run(cmd,text=True,capture_output=True)
    receipt={
        "tool":"DESC","command":cmd,"returncode":proc.returncode,
        "input":str(args.input),"input_sha256":sha256(args.input),
        "output":str(args.output),"executed_at_utc":datetime.now(timezone.utc).isoformat(),
        "stdout_tail":proc.stdout[-12000:],"stderr_tail":proc.stderr[-12000:],
        "success":bool(proc.returncode==0 and args.output.exists()),
        "authority":"production_solver_execution_receipt_not_automatic_scientific_promotion",
    }
    if args.output.exists(): receipt["output_sha256"]=sha256(args.output)
    args.receipt.parent.mkdir(parents=True,exist_ok=True)
    args.receipt.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
    return 0 if receipt["success"] else 2
if __name__=="__main__": raise SystemExit(main())
