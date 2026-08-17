from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE_NAMES = {"MANIFEST.sha256", "IX-Fusion.zip", "IX-StellaratorForge.zip"}
EXCLUDE_PARTS = {"__pycache__", ".git", ".venv", ".pytest_cache", "*.egg-info"}


def include(path: Path) -> bool:
    if path.name in EXCLUDE_NAMES:
        return False
    if any(part in {"__pycache__", ".git", ".venv", ".pytest_cache"} for part in path.parts):
        return False
    if any(part.endswith(".egg-info") for part in path.parts):
        return False
    return path.is_file()


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    files = sorted(p for p in ROOT.rglob("*") if include(p))
    lines = [f"{digest(path)}  {path.relative_to(ROOT).as_posix()}" for path in files]
    (ROOT / "MANIFEST.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote MANIFEST.sha256 for {len(files)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
