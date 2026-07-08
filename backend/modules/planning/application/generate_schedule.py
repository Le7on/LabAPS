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
    Resource,
)
from backend.engines.scheduling.scheduling_engine import SchedulingEngine
from backend.shared.errors import NotFoundError, ValidationError


class GenerateScheduleUseCase:
    def __init__(self, uow_factory, scheduling_engine: SchedulingEngine):
        self._uow_factory = uow_factory
        self._engine = scheduling_engine

    def execute(
        self,
        plan_id: str,
        version_id: str,
        operations: list[dict],
        resources: list[dict] | None = None,
    ) -> dict:
        with self._uow_factory() as uow:
            plan = uow.plans.get(plan_id)

        if plan is None:
            raise NotFoundError(f"Plan {plan_id} not found")
        if not any(v.id == version_id for v in plan.versions):
            raise NotFoundError(f"Plan version {version_id} not found")

        problem = self._build_problem(operations, resources or [])
        result = self._engine.schedule(problem)

        return {
            "planId": plan_id,
            "versionId": version_id,
            "status": result.status,
            "feasible": result.feasible,
            "makespan": result.makespan,
            "assignments": [
                {
                    "operationId": a.operation_id,
                    "start": a.start,
                    "end": a.end,
                    "resourceId": a.resource_id,
                }
                for a in result.assignments
            ],
        }

    @staticmethod
    def _build_problem(operations: list[dict], resources: list[dict]) -> PlanningProblem:
        if not operations:
            raise ValidationError("At least one operation is required")

        built_ops = tuple(
            Operation(
                identifier=str(op.get("id")),
                duration=int(op.get("duration", 0)),
                depends_on=tuple(op.get("dependsOn", ())),
                required_capability=op.get("requiredCapability"),
            )
            for op in operations
        )
        built_resources = tuple(
            Resource(
                identifier=str(r.get("id")),
                capabilities=frozenset(r.get("capabilities", [])),
            )
            for r in resources
        )
        return PlanningProblem(
            operations=built_ops,
            resources=built_resources,
            policies=PlanningPolicies(),
        )
