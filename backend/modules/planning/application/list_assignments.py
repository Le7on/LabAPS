"""List Assignments use case (read operation).

Returns the persisted scheduling assignments for a Plan Version.
"""

from __future__ import annotations

from backend.shared.errors import NotFoundError


class ListAssignmentsUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self, plan_id: str, version_id: str) -> dict:
        with self._uow_factory() as uow:
            plan = uow.plans.get(plan_id)
            if plan is None:
                raise NotFoundError(f"Plan {plan_id} not found")
            plan.get_version(version_id)  # raises NotFoundError if missing
            items = uow.assignments.list_for_version(version_id)

        return {"count": len(items), "items": items}
