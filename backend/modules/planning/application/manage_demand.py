"""Demand use cases for a Plan Version (add, list)."""

from __future__ import annotations

from backend.modules.planning.domain.entities.demand import Demand, DemandPriority
from backend.shared.errors import NotFoundError, ValidationError


def _demand_dict(demand: Demand) -> dict:
    return {
        "id": demand.id,
        "projectId": demand.project_id,
        "quantity": demand.quantity,
        "priority": demand.priority.value,
    }


class AddDemandUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self, plan_id: str, version_id: str, data: dict) -> dict:
        try:
            priority = DemandPriority(data.get("priority", "normal"))
        except ValueError as exc:
            raise ValidationError(f"Unknown priority: {data.get('priority')}") from exc

        demand = Demand(
            project_id=data.get("projectId", ""),
            quantity=int(data.get("quantity", 0)),
            priority=priority,
        )

        with self._uow_factory() as uow:
            plan = uow.plans.get(plan_id)
            if plan is None:
                raise NotFoundError(f"Plan {plan_id} not found")
            plan.get_version(version_id)  # raises NotFoundError if missing
            uow.demands.add(version_id, demand)

        return _demand_dict(demand)


class ListDemandUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self, plan_id: str, version_id: str) -> dict:
        with self._uow_factory() as uow:
            plan = uow.plans.get(plan_id)
            if plan is None:
                raise NotFoundError(f"Plan {plan_id} not found")
            plan.get_version(version_id)
            items = [_demand_dict(d) for d in uow.demands.list_for_version(version_id)]

        return {"count": len(items), "items": items}
