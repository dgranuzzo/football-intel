"""Publica o snapshot em Google Sheets (fonte do Looker Studio / Tableau)."""

from __future__ import annotations

from pathlib import Path

import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

from football_intel.models import Snapshot

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

TAB_ORDER = ["matches", "standings", "scorers", "teams", "competitions", "pipeline_runs"]


def publish_snapshot(
    snapshot: Snapshot,
    spreadsheet_id: str,
    service_account_path: Path,
) -> str:
    if not spreadsheet_id:
        raise ValueError("GOOGLE_SHEETS_SPREADSHEET_ID nao configurado.")
    if not service_account_path.exists():
        raise FileNotFoundError(
            f"Service account nao encontrada em {service_account_path}. "
            "Veja docs/GOOGLE_SHEETS.md."
        )
    creds = Credentials.from_service_account_file(str(service_account_path), scopes=SCOPES)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(spreadsheet_id)

    frames = {
        "matches": pd.DataFrame([item.model_dump(mode="json") for item in snapshot.matches]),
        "standings": pd.DataFrame([item.model_dump(mode="json") for item in snapshot.standings]),
        "scorers": pd.DataFrame([item.model_dump(mode="json") for item in snapshot.scorers]),
        "teams": pd.DataFrame([item.model_dump(mode="json") for item in snapshot.teams]),
        "competitions": pd.DataFrame([snapshot.competition.model_dump(mode="json")]),
        "pipeline_runs": pd.DataFrame(
            [snapshot.run.model_dump(mode="json")] if snapshot.run else []
        ),
    }
    for tab_name in TAB_ORDER:
        _upsert_tab(spreadsheet, tab_name, frames[tab_name])
    return spreadsheet.url


def _upsert_tab(spreadsheet: gspread.Spreadsheet, title: str, frame: pd.DataFrame) -> None:
    try:
        worksheet = spreadsheet.worksheet(title)
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title=title, rows=2, cols=20)

    if frame.empty:
        worksheet.clear()
        worksheet.update("A1", [[title, "sem dados nesta execucao"]])
        return

    values = [list(frame.columns)] + frame.fillna("").astype(str).values.tolist()
    worksheet.clear()
    worksheet.update("A1", values)
    worksheet.freeze(rows=1)
