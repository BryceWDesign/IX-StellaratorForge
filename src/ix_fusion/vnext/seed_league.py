"""Candidate-family definitions for the vNext search league."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SeedFamily:
    family_id: str
    field_periods: int | None
    physics_family: str
    role: str
    rationale: str
    privileged: bool


def load_seed_league(path: str | Path) -> tuple[SeedFamily, ...]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    seeds = tuple(SeedFamily(**item) for item in raw["families"])
    if any(seed.privileged for seed in seeds):
        raise ValueError("vNext forbids a privileged seed family before high-authority evidence exists")
    ids = [seed.family_id for seed in seeds]
    if len(ids) != len(set(ids)):
        raise ValueError("seed family IDs must be unique")
    return seeds
