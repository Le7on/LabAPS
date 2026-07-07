"""Get Plan use case (read operation)."""

from __future__ import annotations

from backend.modules.planning.dto.plan_dto import plan_to_dict
from backend.shared.errors import NotFoundError


class GetPlanUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self, plan_id: str) -> dict:
        with self._uow_factory() as uow:
            plan = uow.plans.get(plan_id)

        if plan is None:
            raise NotFoundError(f"Plan {plan_id} not found")

        return plan_to_dict(plan)
