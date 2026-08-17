from __future__ import annotations

import argparse
import json
from pathlib import Path

from .external import detect_external_solvers
from .poc import run_poc


def _root_from_here() -> Path:
    return Path(__file__).resolve().parents[2]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ix-fusion")
    sub = parser.add_subparsers(dest="command", required=True)
    poc = sub.add_parser("poc", help="run the reduced-order proof of concept")
    poc.add_argument("--repo-root", type=Path, default=_root_from_here())
    poc.add_argument("--output", type=Path)
    poc.add_argument("--no-figures", action="store_true")
    sub.add_parser("solvers", help="report optional high-fidelity solver availability")
    args = parser.parse_args(argv)
    if args.command == "poc":
        result = run_poc(args.repo_root, args.output, generate_figures=not args.no_figures)
        print(json.dumps(result["verdict"], indent=2, sort_keys=True))
        return 0
    if args.command == "solvers":
        print(json.dumps([s.__dict__ for s in detect_external_solvers()], indent=2))
        return 0
    return 2
