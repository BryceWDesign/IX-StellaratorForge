
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .readiness import build_readiness_report
from .closure import run_closure_campaign
from .computational_closure import run_computational_closure
from .poc import run_sfr1_poc
from .reactor import load_reactor_config, validate_reactor_config


def main() -> int:
    parser = argparse.ArgumentParser(prog="ix-stellaratorforge")
    parser.add_argument("command", choices=("validate", "report", "closure", "max-closure", "poc"))
    parser.add_argument("--config", default="configs/reactor/sfr1_rev_a.json")
    args = parser.parse_args()
    config = load_reactor_config(Path(args.config))
    if args.command == "validate":
        verdict = validate_reactor_config(config)
        print(json.dumps({"passed": verdict.passed, "errors": verdict.errors, "warnings": verdict.warnings}, indent=2))
        return 0 if verdict.passed else 1
    if args.command == "closure":
        print(json.dumps(run_closure_campaign(config), indent=2, sort_keys=True))
        return 0
    if args.command == "max-closure":
        print(json.dumps(run_computational_closure(config), indent=2, sort_keys=True))
        return 0
    if args.command == "poc":
        print(json.dumps(run_sfr1_poc(config), indent=2, sort_keys=True))
        return 0
    print(json.dumps(build_readiness_report(config), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
