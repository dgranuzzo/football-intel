"""Modelos normalizados — o schema nao muda ao adicionar uma liga."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Competition(BaseModel):
    competition_code: str
    competition_name: str
    short_name: str
    area: str
    type: str
    season: Optional[str] = None
    provider: str = "football_data"


class Team(BaseModel):
    team_id: int
    team_name: str
    short_name: Optional[str] = None
    tla: Optional[str] = None
    area: Optional[str] = None
    competition_code: str


class Match(BaseModel):
    match_id: int
    competition_code: str
    season: Optional[str] = None
    utc_date: datetime
    status: str
    matchday: Optional[int] = None
    stage: Optional[str] = None
    group_name: Optional[str] = None
    home_team_id: int
    home_team: str
    away_team_id: int
    away_team: str
    home_goals: Optional[int] = None
    away_goals: Optional[int] = None
    winner: Optional[str] = None
    venue: Optional[str] = None
    referee: Optional[str] = None


class StandingRow(BaseModel):
    competition_code: str
    season: Optional[str] = None
    matchday: Optional[int] = None
    position: int
    team_id: int
    team_name: str
    played: int
    won: int
    draw: int
    lost: int
    goals_for: int
    goals_against: int
    goal_diff: int
    points: int
    form: Optional[str] = None


class Scorer(BaseModel):
    competition_code: str
    season: Optional[str] = None
    player_id: int
    player_name: str
    team_id: int
    team_name: str
    goals: int
    assists: Optional[int] = None
    penalties: Optional[int] = None
    played: Optional[int] = None


class PipelineRun(BaseModel):
    run_at: datetime
    competition_code: str
    matches: int = 0
    standings: int = 0
    scorers: int = 0
    status: str = "ok"
    notes: str = ""


class Snapshot(BaseModel):
    competition: Competition
    teams: list[Team] = Field(default_factory=list)
    matches: list[Match] = Field(default_factory=list)
    standings: list[StandingRow] = Field(default_factory=list)
    scorers: list[Scorer] = Field(default_factory=list)
    run: Optional[PipelineRun] = None
