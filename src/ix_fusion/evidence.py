from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "1.0"


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return {k: _jsonable(v) for k, v in asdict(value).items()}
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    if hasattr(value, "item"):
        return value.item()
    return value


def write_json(path: str | Path, data: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(_jsonable(data), handle, indent=2, sort_keys=True)
        handle.write("\n")


def load_json(path: str | Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def evidence_bundle(
    run_id: str,
    model: str,
    seed: int,
    config_paths: list[Path],
    outputs: dict[str, Any],
    assumptions: list[str],
    limitations: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "created_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "model": model,
        "seed": seed,
        "input_hashes": {str(p): sha256_file(p) for p in config_paths},
        "outputs": _jsonable(outputs),
        "assumptions": assumptions,
        "limitations": limitations,
        "claim_level": "reduced-order computational screening only",
    }


def validate_bundle(bundle: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = {
        "schema_version",
        "run_id",
        "created_utc",
        "model",
        "seed",
        "input_hashes",
        "outputs",
        "assumptions",
        "limitations",
        "claim_level",
    }
    missing = required - set(bundle)
    if missing:
        errors.append("missing keys: " + ", ".join(sorted(missing)))
    if bundle.get("schema_version") != SCHEMA_VERSION:
        errors.append("unsupported schema_version")
    if not bundle.get("assumptions"):
        errors.append("assumptions must be explicit")
    if not bundle.get("limitations"):
        errors.append("limitations must be explicit")
    if bundle.get("claim_level") != "reduced-order computational screening only":
        errors.append("claim_level exceeds current model authority")
    return errors
