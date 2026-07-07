"""Create Plan Version use case.

Loads the Plan aggregate, creates a new version through the domain, and persists.
One transaction boundary.
"""

from __future__ import annotations

from backend.modules.planning.repository.plan_repository import PlanRepository
from backend.shared.errors import NotFoundError


class CreatePlanVersionUseCase:
    def __init__(self, session_factory):
        self._session_factory = session_factory

    def execute(self, plan_id: str) -> dict:
        session = self._session_factory()
        try:
            repository = PlanRepository(session)
            plan = repository.get(plan_id)
            if plan is None:
                raise NotFoundError(f"Plan {plan_id} not found")

            version = plan.create_version()
            repository.save(plan)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

        return {
            "id": version.id,
            "planId": plan_id,
            "versionNumber": version.version_number,
            "versionType": version.version_type.value,
            "status": version.status.value,
        }
