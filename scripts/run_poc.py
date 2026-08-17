from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ix_fusion.poc import run_poc


if __name__ == "__main__":
    result = run_poc(ROOT)
    print(result["verdict"]["reduced_model_verdict"])
