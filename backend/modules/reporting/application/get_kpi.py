"""Get KPI use case (read-only)."""

from __future__ import annotations

from backend.modules.reporting.query.kpi_query import KpiQueryService


class GetKpiUseCase:
    def __init__(self, session_factory):
        self._session_factory = session_factory

    def execute(self) -> dict:
        session = self._session_factory()
        try:
            return KpiQueryService(session).summary()
        finally:
            session.close()
