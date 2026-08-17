from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ix_fusion.studies import run_secondary_studies


if __name__ == "__main__":
    run_secondary_studies(ROOT)
    print("secondary studies complete")
