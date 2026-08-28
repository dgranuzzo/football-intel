"""Configuracao via ambiente e YAML."""

from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Settings carregadas de .env e variaveis de ambiente."""

    model_config = SettingsConfigDict(
        env_file=str(ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    football_data_token: str = ""
    active_leagues: str = "BSA"
    google_sheets_spreadsheet_id: str = ""
    google_service_account_json: str = "credentials/service_account.json"
    app_timezone: str = "America/Sao_Paulo"
    season: str = ""
    leagues_config_path: Path = Field(default=ROOT / "config" / "leagues.yaml")
    data_dir: Path = Field(default=ROOT / "data")

    @property
    def league_codes(self) -> list[str]:
        return [code.strip().upper() for code in self.active_leagues.split(",") if code.strip()]

    @property
    def service_account_path(self) -> Path:
        path = Path(self.google_service_account_json)
        if not path.is_absolute():
            return ROOT / path
        return path
