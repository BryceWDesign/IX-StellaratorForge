from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def verify() -> list[str]:
    manifest = ROOT / "MANIFEST.sha256"
    if not manifest.exists():
        return ["MANIFEST.sha256 is missing"]
    errors: list[str] = []
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, rel = line.split("  ", 1)
        path = ROOT / rel
        if not path.exists():
            errors.append(f"missing: {rel}")
            continue
        actual = sha256(path)
        if actual != expected:
            errors.append(f"hash mismatch: {rel}")
    return errors


def main() -> int:
    errors = verify()
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("manifest integrity: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
