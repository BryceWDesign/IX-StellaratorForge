from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run(label: str, command: list[str]) -> None:
    proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if proc.returncode:
        print(f"{label:.<34} FAIL")
        print(proc.stdout)
        print(proc.stderr)
        raise SystemExit(proc.returncode)
    print(f"{label:.<34} PASS")


def validate_json() -> None:
    for path in (ROOT / "configs" / "vnext").glob("*.json"):
        json.loads(path.read_text(encoding="utf-8"))
    json.loads((ROOT / "results" / "vnext" / "robust_nfp_sweep.json").read_text(encoding="utf-8"))
    print(f"{'vNext JSON integrity':.<34} PASS")


print("IX-STELLARATORFORGE INHERITED vNEXT QUALITY GATE\n")
validate_json()
run("Inherited IX-Fusion foundation gate", [sys.executable, "check_green.py"])
run("vNext tests", [sys.executable, "-m", "pytest", "-q", "tests/vnext"])
run("vNext readiness report", [sys.executable, "scripts/report_vnext_readiness.py"])
print("\nIX-STELLARATORFORGE INHERITED vNEXT: GREEN (architecture/research-contract level)")
print("This does NOT mean a plasma, magnet, reactor, Q>1 system, or net-electric plant has been demonstrated.")
