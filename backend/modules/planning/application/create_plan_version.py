"""Create Plan Version use case.

Loads the Plan aggregate, creates a new version through the domain, and persists.
One transaction boundary (the Unit of Work).
"""

from __future__ import annotations

from backend.shared.errors import NotFoundError


class CreatePlanVersionUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self, plan_id: str) -> dict:
        with self._uow_factory() as uow:
            plan = uow.plans.get(plan_id)
            if plan is None:
                raise NotFoundError(f"Plan {plan_id} not found")

            version = plan.create_version()
            uow.plans.save(plan)

        return {
            "id": version.id,
            "planId": plan_id,
            "versionNumber": version.version_number,
            "versionType": version.version_type.value,
            "status": version.status.value,
        }
