from __future__ import annotations
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from ix_stellaratorforge.closure import run_closure_campaign
from ix_stellaratorforge.reactor import load_reactor_config

cfg = load_reactor_config(ROOT / "configs/reactor/sfr1_rev_a.json")
result = run_closure_campaign(cfg)
out = ROOT / "results/closure/sfr1_v030_closure_campaign.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2, sort_keys=True))
print(f"\nWrote {out.relative_to(ROOT)}")
