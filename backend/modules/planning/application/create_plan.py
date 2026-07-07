"""Create Plan use case.

One business action, one transaction boundary (the Unit of Work). Invokes the
domain, persists, returns a DTO.
"""

from __future__ import annotations

from backend.modules.planning.domain.aggregates.plan import Plan
from backend.modules.planning.dto.plan_dto import CreatePlanRequest, plan_to_dict


class CreatePlanUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self, request: CreatePlanRequest) -> dict:
        plan = Plan(
            planning_horizon=request.planning_horizon,
            name=request.name,
            description=request.description,
        )

        with self._uow_factory() as uow:
            uow.plans.add(plan)

        return plan_to_dict(plan)
