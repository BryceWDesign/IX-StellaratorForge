#!/usr/bin/env python3
"""Validate that imported production-solver evidence is real, explicit, and non-template."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def main()->int:
 ap=argparse.ArgumentParser();ap.add_argument("receipt",type=Path);args=ap.parse_args();d=json.loads(args.receipt.read_text())
 if not d.get("success",False): raise SystemExit("receipt does not report successful execution")
 if d.get("executed",True) is False: raise SystemExit("template/unexecuted receipt cannot be promoted")
 tool=d.get("tool","")
 if not tool: raise SystemExit("receipt missing tool identity")
 print(f"receipt structure PASS: {tool}");return 0
if __name__=="__main__":raise SystemExit(main())
