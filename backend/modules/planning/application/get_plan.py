"""Get Plan use case (read operation)."""

from __future__ import annotations

from backend.modules.planning.dto.plan_dto import plan_to_dict
from backend.modules.planning.repository.plan_repository import PlanRepository
from backend.shared.errors import NotFoundError


class GetPlanUseCase:
    def __init__(self, session_factory):
        self._session_factory = session_factory

    def execute(self, plan_id: str) -> dict:
        session = self._session_factory()
        try:
            repository = PlanRepository(session)
            plan = repository.get(plan_id)
        finally:
            session.close()

        if plan is None:
            raise NotFoundError(f"Plan {plan_id} not found")

        return plan_to_dict(plan)
