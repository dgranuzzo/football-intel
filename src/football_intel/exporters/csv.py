"""Exporta snapshot para CSV versionavel (bom para Git e Tableau)."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from football_intel.models import Snapshot


def write_csvs(snapshot: Snapshot, out_dir: Path) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    frames = {
        "matches": pd.DataFrame([item.model_dump() for item in snapshot.matches]),
        "standings": pd.DataFrame([item.model_dump() for item in snapshot.standings]),
        "scorers": pd.DataFrame([item.model_dump() for item in snapshot.scorers]),
        "teams": pd.DataFrame([item.model_dump() for item in snapshot.teams]),
        "competitions": pd.DataFrame([snapshot.competition.model_dump()]),
    }
    paths: dict[str, Path] = {}
    prefix = snapshot.competition.competition_code.lower()
    for name, frame in frames.items():
        path = out_dir / f"{prefix}_{name}.csv"
        frame.to_csv(path, index=False)
        paths[name] = path
    return paths
