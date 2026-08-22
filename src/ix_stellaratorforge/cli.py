
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .readiness import build_readiness_report
from .closure import run_closure_campaign
from .computational_closure import run_computational_closure
from .poc import run_sfr1_poc
from .reactor import load_reactor_config, validate_reactor_config
from .sfr2 import run_sfr2_screen
from .sfr2_actuation import run_actuation_overlay_screen
from .sfr3_field_integrity import run_sfr3_field_integrity_screen
from .sfr3_dual_boundary import run_dual_boundary_screen
from .sfr4_integrated_campaign import run_integrated_campaign


def main() -> int:
    parser = argparse.ArgumentParser(prog="ix-stellaratorforge")
    parser.add_argument(
        "command",
        choices=(
            "validate",
            "report",
            "closure",
            "max-closure",
            "poc",
            "sfr2-screen",
            "sfr2-actuation-screen",
            "sfr3-field-integrity-screen",
            "sfr3-dual-boundary-screen",
            "sfr4-integrated-campaign",
        ),
    )
    parser.add_argument("--config", default="configs/reactor/sfr1_rev_a.json")
    args = parser.parse_args()
    if args.command == "sfr2-screen":
        raw = json.loads(Path(args.config if args.config != "configs/reactor/sfr1_rev_a.json" else "configs/reactor/sfr2_rev_a.json").read_text(encoding="utf-8"))
        print(json.dumps(run_sfr2_screen(raw), indent=2, sort_keys=True))
        return 0
    if args.command == "sfr2-actuation-screen":
        config_path = (
            args.config
            if args.config != "configs/reactor/sfr1_rev_a.json"
            else "configs/reactor/sfr2_actuation_overlay_a.json"
        )
        raw = json.loads(Path(config_path).read_text(encoding="utf-8"))
        print(json.dumps(run_actuation_overlay_screen(raw), indent=2, sort_keys=True))
        return 0
    if args.command == "sfr3-field-integrity-screen":
        config_path = (
            args.config
            if args.config != "configs/reactor/sfr1_rev_a.json"
            else "configs/reactor/sfr3_field_integrity_shell_a.json"
        )
        raw = json.loads(Path(config_path).read_text(encoding="utf-8"))
        print(json.dumps(run_sfr3_field_integrity_screen(raw), indent=2, sort_keys=True))
        return 0
    if args.command == "sfr3-dual-boundary-screen":
        config_path = (
            args.config
            if args.config != "configs/reactor/sfr1_rev_a.json"
            else "configs/reactor/sfr3_dual_boundary_ahis_a.json"
        )
        raw = json.loads(Path(config_path).read_text(encoding="utf-8"))
        sfr3_raw = json.loads(
            Path("configs/reactor/sfr3_field_integrity_shell_a.json").read_text(
                encoding="utf-8"
            )
        )
        print(json.dumps(run_dual_boundary_screen(raw, sfr3_raw), indent=2, sort_keys=True))
        return 0
    if args.command == "sfr4-integrated-campaign":
        config_path = (
            args.config
            if args.config != "configs/reactor/sfr1_rev_a.json"
            else "configs/reactor/sfr4_integrated_physical_promotion_a.json"
        )
        raw = json.loads(Path(config_path).read_text(encoding="utf-8"))
        print(json.dumps(run_integrated_campaign(raw), indent=2, sort_keys=True))
        return 0
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
