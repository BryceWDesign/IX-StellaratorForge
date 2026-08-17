
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ix_stellaratorforge.readiness import build_readiness_report
from ix_stellaratorforge.reactor import load_reactor_config

config = load_reactor_config(ROOT / "configs" / "reactor" / "sfr1_rev_a.json")
report = build_readiness_report(config)
(ROOT / "results" / "reactor" / "sfr1_rev_a_readiness.json").write_text(
    json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps(report, indent=2, sort_keys=True))
raise SystemExit(0 if report["architecture_validation"]["passed"] else 1)
