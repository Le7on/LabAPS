"""Create Plan use case.

One business action, one transaction boundary (the Unit of Work). Invokes the
domain, persists, returns a DTO.
"""

from __future__ import annotations

from backend.modules.planning.domain.aggregates.plan import Plan
from backend.modules.planning.domain.enums.plan_enums import PlanStatus
from backend.modules.planning.dto.plan_dto import CreatePlanRequest, plan_to_dict
from backend.shared.errors import ConflictError, NotFoundError


class CreatePlanUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self, request: CreatePlanRequest) -> dict:
        plan = Plan(
            planning_horizon=request.planning_horizon,
            name=request.name,
            description=request.description,
            start_date=request.start_date,
            end_date=request.end_date,
            shift_mode=request.shift_mode,
            skipped_dates=request.skipped_dates,
        )

        with self._uow_factory() as uow:
            uow.plans.add(plan)

        return plan_to_dict(plan)


class DeletePlanUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self, plan_id: str) -> dict:
        with self._uow_factory() as uow:
            plan = uow.plans.get(plan_id)
            if plan is None:
                raise NotFoundError(f"Plan {plan_id} not found")
            # Only draft plans can be deleted; active/archived plans are kept.
            if plan.status != PlanStatus.DRAFT:
                raise ConflictError("Only draft plans can be deleted")
            uow.plans.delete(plan_id)
        return {"id": plan_id, "deleted": True}
