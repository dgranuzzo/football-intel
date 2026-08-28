"""Contrato de um provedor de dados. Novas ligas/APIs implementam esta interface."""

from __future__ import annotations

from abc import ABC, abstractmethod

from football_intel.models import Snapshot


class StatsClient(ABC):
    """Cliente de estatisticas de uma competicao."""

    @abstractmethod
    def fetch_snapshot(self, competition_code: str, season: str | None = None) -> Snapshot:
        """Retorna snapshot normalizado da competicao."""
