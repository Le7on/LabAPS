"""Get Dashboard use case (read-only).

Returns aggregate counts for the dashboard. Read-only, so it uses a session
directly through the Query Service rather than a write-oriented Unit of Work.
"""

from __future__ import annotations

from backend.modules.reporting.query.dashboard_query import DashboardQueryService


class GetDashboardUseCase:
    def __init__(self, session_factory):
        self._session_factory = session_factory

    def execute(self) -> dict:
        session = self._session_factory()
        try:
            return DashboardQueryService(session).summary()
        finally:
            session.close()
