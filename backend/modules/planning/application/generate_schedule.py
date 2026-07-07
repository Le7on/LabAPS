"""Generate Schedule use case.

Bridges the Planning domain and the Scheduling Engine: it verifies the target
Plan Version exists, builds a PlanningProblem from the supplied operations, runs
the injected SchedulingEngine, and returns the resulting assignments.

Scope note: operations are supplied in the request for this milestone. A later
milestone builds the PlanningProblem from persisted Workflow/Operation Instances
and the Planning Context snapshot.
"""

from __future__ import annotations

from backend.engines.planning.planning_problem import (
    Operation,
    PlanningPolicies,
    PlanningProblem,
)
from backend.engines.scheduling.scheduling_engine import SchedulingEngine
from backend.modules.planning.repository.plan_repository import PlanRepository
from backend.shared.errors import NotFoundError, ValidationError


class GenerateScheduleUseCase:
    def __init__(self, session_factory, scheduling_engine: SchedulingEngine):
        self._session_factory = session_factory
        self._engine = scheduling_engine

    def execute(self, plan_id: str, version_id: str, operations: list[dict]) -> dict:
        session = self._session_factory()
        try:
            repository = PlanRepository(session)
            plan = repository.get(plan_id)
        finally:
            session.close()

        if plan is None:
            raise NotFoundError(f"Plan {plan_id} not found")
        if not any(v.id == version_id for v in plan.versions):
            raise NotFoundError(f"Plan version {version_id} not found")

        problem = self._build_problem(operations)
        result = self._engine.schedule(problem)

        return {
            "planId": plan_id,
            "versionId": version_id,
            "status": result.status,
            "feasible": result.feasible,
            "makespan": result.makespan,
            "assignments": [
                {"operationId": a.operation_id, "start": a.start, "end": a.end}
                for a in result.assignments
            ],
        }

    @staticmethod
    def _build_problem(operations: list[dict]) -> PlanningProblem:
        if not operations:
            raise ValidationError("At least one operation is required")

        built = tuple(
            Operation(
                identifier=str(op.get("id")),
                duration=int(op.get("duration", 0)),
                depends_on=tuple(op.get("dependsOn", ())),
            )
            for op in operations
        )
        return PlanningProblem(operations=built, policies=PlanningPolicies())
