"""Orquestra extract -> transform -> load para uma ou mais ligas."""

from __future__ import annotations

from pathlib import Path

import yaml

from football_intel.clients.football_data import FootballDataClient
from football_intel.exporters.csv import write_csvs
from football_intel.exporters.sheets import publish_snapshot
from football_intel.models import Snapshot
from football_intel.settings import Settings


def load_catalog(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def resolve_leagues(settings: Settings) -> list[dict]:
    catalog = load_catalog(settings.leagues_config_path)
    wanted = set(settings.league_codes)
    selected = []
    for code, meta in catalog["competitions"].items():
        if code in wanted:
            selected.append({"code": code, **meta})
    missing = wanted - {item["code"] for item in selected}
    if missing:
        raise ValueError(f"Ligas desconhecidas em ACTIVE_LEAGUES: {sorted(missing)}")
    return selected


def run(settings: Settings | None = None, publish_sheets: bool = True) -> list[Snapshot]:
    settings = settings or Settings()
    leagues = resolve_leagues(settings)
    client = FootballDataClient(settings.football_data_token)
    snapshots: list[Snapshot] = []
    try:
        for league in leagues:
            snapshot = client.fetch_snapshot(league["code"], settings.season or None)
            csv_dir = settings.data_dir / "warehouse"
            write_csvs(snapshot, csv_dir)
            if publish_sheets and settings.google_sheets_spreadsheet_id:
                publish_snapshot(
                    snapshot,
                    settings.google_sheets_spreadsheet_id,
                    settings.service_account_path,
                )
            snapshots.append(snapshot)
    finally:
        client.close()
    return snapshots
