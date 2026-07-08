"""Plan Version lifecycle use cases.

Review, publish and archive a Plan Version. Each is one business action / one
transaction; the domain enforces the transition rules (State Model, chapter 3).
"""

from __future__ import annotations

from backend.shared.errors import NotFoundError


def _version_dict(plan_id: str, version) -> dict:
    return {
        "id": version.id,
        "planId": plan_id,
        "versionNumber": version.version_number,
        "versionType": version.version_type.value,
        "status": version.status.value,
    }


class _PlanVersionTransitionUseCase:
    """Shared load -> transition -> persist flow for version lifecycle actions."""

    _action = ""  # Plan aggregate method name

    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self, plan_id: str, version_id: str) -> dict:
        with self._uow_factory() as uow:
            plan = uow.plans.get(plan_id)
            if plan is None:
                raise NotFoundError(f"Plan {plan_id} not found")

            version = getattr(plan, self._action)(version_id)
            uow.plans.save(plan)
            result = _version_dict(plan_id, version)

        return result


class ReviewPlanVersionUseCase(_PlanVersionTransitionUseCase):
    _action = "review_version"


class PublishPlanVersionUseCase(_PlanVersionTransitionUseCase):
    _action = "publish_version"


class ArchivePlanVersionUseCase(_PlanVersionTransitionUseCase):
    _action = "archive_version"
