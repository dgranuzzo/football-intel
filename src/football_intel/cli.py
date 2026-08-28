"""CLI: python -m football_intel sync."""

from __future__ import annotations

import sys
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from football_intel.pipeline import run
from football_intel.settings import Settings

app = typer.Typer(add_completion=False, no_args_is_help=True)
console = Console()


@app.command()
def sync(
    leagues: Optional[str] = typer.Option(
        None,
        "--leagues",
        "-l",
        help="Codigos separados por virgula. Default: ACTIVE_LEAGUES no .env",
    ),
    no_sheets: bool = typer.Option(False, "--no-sheets", help="Nao publica no Google Sheets"),
) -> None:
    """Coleta estatisticas e atualiza CSV + Google Sheets."""
    settings = Settings()
    if leagues:
        settings.active_leagues = leagues
    try:
        snapshots = run(settings, publish_sheets=not no_sheets)
    except Exception as exc:  # noqa: BLE001 — CLI deve mostrar o erro amigavel
        console.print(f"[red]Falha no pipeline:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    table = Table(title="Football Intel — sync")
    table.add_column("Liga")
    table.add_column("Temporada")
    table.add_column("Jogos", justify="right")
    table.add_column("Tabela", justify="right")
    table.add_column("Artilheiros", justify="right")
    for snapshot in snapshots:
        table.add_row(
            snapshot.competition.competition_code,
            snapshot.competition.season or "-",
            str(len(snapshot.matches)),
            str(len(snapshot.standings)),
            str(len(snapshot.scorers)),
        )
    console.print(table)
    console.print("[green]CSV atualizado em data/warehouse/[/green]")


def main() -> None:
    app()


if __name__ == "__main__":
    sys.exit(main())
