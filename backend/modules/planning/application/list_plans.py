"""List Plans use case (read operation)."""

from __future__ import annotations

from backend.modules.planning.dto.plan_dto import plan_to_dict
from backend.modules.planning.repository.plan_repository import PlanRepository


class ListPlansUseCase:
    def __init__(self, session_factory):
        self._session_factory = session_factory

    def execute(self) -> dict:
        session = self._session_factory()
        try:
            repository = PlanRepository(session)
            plans = repository.list()
            items = [plan_to_dict(p) for p in plans]
        finally:
            session.close()

        return {"count": len(items), "items": items}
