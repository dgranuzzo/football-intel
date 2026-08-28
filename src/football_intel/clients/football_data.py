"""Cliente football-data.org v4."""

from __future__ import annotations

from datetime import datetime, timezone

import httpx

from football_intel.clients.base import StatsClient
from football_intel.models import (
    Competition,
    Match,
    PipelineRun,
    Scorer,
    Snapshot,
    StandingRow,
    Team,
)

BASE_URL = "https://api.football-data.org/v4"


class FootballDataError(RuntimeError):
    """Erro HTTP ou de payload da API."""


class FootballDataClient(StatsClient):
    def __init__(self, token: str, timeout: float = 30.0) -> None:
        if not token:
            raise FootballDataError(
                "FOOTBALL_DATA_TOKEN vazio. Crie em https://www.football-data.org/client/register"
            )
        self._client = httpx.Client(
            base_url=BASE_URL,
            headers={"X-Auth-Token": token},
            timeout=timeout,
        )

    def close(self) -> None:
        self._client.close()

    def _get(self, path: str, params: dict | None = None) -> dict:
        response = self._client.get(path, params=params)
        if response.status_code == 403:
            raise FootballDataError(
                f"Acesso negado em {path}. Token invalido ou liga fora do plano. "
                f"Detalhe: {response.text[:300]}"
            )
        if response.status_code == 429:
            raise FootballDataError("Rate limit (10 req/min no plano free). Tente de novo.")
        if response.status_code >= 400:
            raise FootballDataError(f"HTTP {response.status_code} em {path}: {response.text[:300]}")
        return response.json()

    def fetch_snapshot(self, competition_code: str, season: str | None = None) -> Snapshot:
        params = {"season": season} if season else None
        competition = self._get(f"/competitions/{competition_code}")
        matches_payload = self._get(f"/competitions/{competition_code}/matches", params=params)
        standings_payload = self._get(f"/competitions/{competition_code}/standings", params=params)
        scorers_payload = self._get(
            f"/competitions/{competition_code}/scorers",
            params={**(params or {}), "limit": 20},
        )
        return self._normalize(
            competition_code,
            competition,
            matches_payload,
            standings_payload,
            scorers_payload,
        )

    def _normalize(
        self,
        code: str,
        competition: dict,
        matches_payload: dict,
        standings_payload: dict,
        scorers_payload: dict,
    ) -> Snapshot:
        season = _season_label(competition)
        comp = Competition(
            competition_code=code,
            competition_name=competition.get("name") or code,
            short_name=competition.get("code") or code,
            area=(competition.get("area") or {}).get("name") or "",
            type=competition.get("type") or "LEAGUE",
            season=season,
            provider="football_data",
        )
        matches = [_to_match(code, season, item) for item in matches_payload.get("matches", [])]
        standings = _to_standings(code, season, standings_payload)
        scorers = [_to_scorer(code, season, item) for item in scorers_payload.get("scorers", [])]
        teams = _teams_from(code, matches, standings)
        run = PipelineRun(
            run_at=datetime.now(timezone.utc),
            competition_code=code,
            matches=len(matches),
            standings=len(standings),
            scorers=len(scorers),
            status="ok",
        )
        return Snapshot(
            competition=comp,
            teams=teams,
            matches=matches,
            standings=standings,
            scorers=scorers,
            run=run,
        )


def _season_label(competition: dict) -> str | None:
    current = competition.get("currentSeason") or {}
    start = (current.get("startDate") or "")[:4]
    end = (current.get("endDate") or "")[:4]
    if start and end and start != end:
        return f"{start}/{end}"
    return start or None


def _to_match(code: str, season: str | None, item: dict) -> Match:
    score = item.get("score") or {}
    full_time = score.get("fullTime") or {}
    home = item.get("homeTeam") or {}
    away = item.get("awayTeam") or {}
    refs = item.get("referees") or []
    referee = refs[0].get("name") if refs else None
    utc = item.get("utcDate")
    return Match(
        match_id=item["id"],
        competition_code=code,
        season=season,
        utc_date=datetime.fromisoformat(utc.replace("Z", "+00:00")),
        status=item.get("status") or "UNKNOWN",
        matchday=item.get("matchday"),
        stage=item.get("stage"),
        group_name=item.get("group"),
        home_team_id=home.get("id") or 0,
        home_team=home.get("name") or "",
        away_team_id=away.get("id") or 0,
        away_team=away.get("name") or "",
        home_goals=full_time.get("home"),
        away_goals=full_time.get("away"),
        winner=score.get("winner"),
        venue=item.get("venue"),
        referee=referee,
    )


def _to_standings(code: str, season: str | None, payload: dict) -> list[StandingRow]:
    rows: list[StandingRow] = []
    for table in payload.get("standings") or []:
        if table.get("type") and table.get("type") != "TOTAL":
            continue
        for item in table.get("table") or []:
            team = item.get("team") or {}
            rows.append(
                StandingRow(
                    competition_code=code,
                    season=season,
                    matchday=payload.get("season", {}).get("currentMatchday"),
                    position=item.get("position") or 0,
                    team_id=team.get("id") or 0,
                    team_name=team.get("name") or "",
                    played=item.get("playedGames") or 0,
                    won=item.get("won") or 0,
                    draw=item.get("draw") or 0,
                    lost=item.get("lost") or 0,
                    goals_for=item.get("goalsFor") or 0,
                    goals_against=item.get("goalsAgainst") or 0,
                    goal_diff=item.get("goalDifference") or 0,
                    points=item.get("points") or 0,
                    form=item.get("form"),
                )
            )
    return rows


def _to_scorer(code: str, season: str | None, item: dict) -> Scorer:
    player = item.get("player") or {}
    team = item.get("team") or {}
    return Scorer(
        competition_code=code,
        season=season,
        player_id=player.get("id") or 0,
        player_name=player.get("name") or "",
        team_id=team.get("id") or 0,
        team_name=team.get("name") or "",
        goals=item.get("goals") or 0,
        assists=item.get("assists"),
        penalties=item.get("penalties"),
        played=item.get("playedMatches"),
    )


def _teams_from(code: str, matches: list[Match], standings: list[StandingRow]) -> list[Team]:
    seen: dict[int, Team] = {}
    for row in standings:
        seen[row.team_id] = Team(
            team_id=row.team_id,
            team_name=row.team_name,
            competition_code=code,
        )
    for match in matches:
        if match.home_team_id not in seen:
            seen[match.home_team_id] = Team(
                team_id=match.home_team_id,
                team_name=match.home_team,
                competition_code=code,
            )
        if match.away_team_id not in seen:
            seen[match.away_team_id] = Team(
                team_id=match.away_team_id,
                team_name=match.away_team,
                competition_code=code,
            )
    return list(seen.values())
