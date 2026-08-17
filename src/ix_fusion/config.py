from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path
from typing import Any

from .models import CandidateConfig, Harmonic


def _harmonic_from_dict(data: dict[str, Any]) -> Harmonic:
    return Harmonic(
        m=int(data["m"]),
        n=int(data["n"]),
        amplitude=float(data["amplitude"]),
        phase=float(data.get("phase", 0.0)),
    )


def candidate_from_dict(data: dict[str, Any]) -> CandidateConfig:
    config = CandidateConfig(
        name=str(data["name"]),
        role=str(data["role"]),
        description=str(data["description"]),
        nfp=int(data["nfp"]),
        major_radius=float(data["major_radius"]),
        minor_radius=float(data["minor_radius"]),
        axis_helical_amplitude=float(data["axis_helical_amplitude"]),
        iota0=float(data["iota0"]),
        shear=float(data["shear"]),
        mirror_amplitude=float(data["mirror_amplitude"]),
        required_helical_strength=float(data["required_helical_strength"]),
        harmonics=tuple(_harmonic_from_dict(item) for item in data.get("harmonics", [])),
        metadata=dict(data.get("metadata", {})),
    )
    config.validate()
    return config


def load_candidate(path: str | Path) -> CandidateConfig:
    path = Path(path)
    with path.open("r", encoding="utf-8") as handle:
        return candidate_from_dict(json.load(handle))


def load_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"expected JSON object in {path}")
    return data


def with_harmonics(config: CandidateConfig, harmonics: tuple[Harmonic, ...]) -> CandidateConfig:
    updated = replace(config, harmonics=harmonics)
    updated.validate()
    return updated
