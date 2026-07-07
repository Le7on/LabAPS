"""Create Plan use case.

One business action, one transaction boundary. Loads no aggregate (creation),
invokes the domain, persists, returns a DTO.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from backend.modules.planning.domain.aggregates.plan import Plan
from backend.modules.planning.dto.plan_dto import CreatePlanRequest, plan_to_dict
from backend.modules.planning.repository.plan_repository import PlanRepository


class CreatePlanUseCase:
    def __init__(self, session_factory):
        self._session_factory = session_factory

    def execute(self, request: CreatePlanRequest) -> dict:
        plan = Plan(
            planning_horizon=request.planning_horizon,
            name=request.name,
            description=request.description,
        )

        session: Session = self._session_factory()
        try:
            repository = PlanRepository(session)
            repository.add(plan)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

        return plan_to_dict(plan)
