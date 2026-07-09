"""Schedule From Instances use case.

Schedules the persisted Operation Instances of a Plan Version against the
resources captured in its immutable Planning Context snapshot (ADR-008: planning
never depends on live configuration after scheduling begins). Persists the
resulting assignments and marks the version Scheduled.
"""

from __future__ import annotations

from backend.engines.planning.planning_problem import (
    EQUIPMENT,
    OBJECTIVE_MAKESPAN,
    OBJECTIVE_WEIGHTED_COMPLETION,
    STAFF,
    Operation,
    PlanningPolicies,
    PlanningProblem,
    Resource,
)
from backend.engines.scheduling.scheduling_engine import SchedulingEngine
from backend.shared.errors import NotFoundError, ValidationError


class ScheduleInstancesUseCase:
    def __init__(self, uow_factory, scheduling_engine: SchedulingEngine):
        self._uow_factory = uow_factory
        self._engine = scheduling_engine

    def execute(self, plan_id: str, version_id: str) -> dict:
        with self._uow_factory() as uow:
            plan = uow.plans.get(plan_id)
            if plan is None:
                raise NotFoundError(f"Plan {plan_id} not found")
            plan.get_version(version_id)  # raises NotFoundError if missing

            operations = uow.workflow_instances.list_operation_instances(version_id)
            if not operations:
                raise ValidationError("No operation instances to schedule; generate first")
            context = uow.workflow_instances.get_context(version_id) or {}
            demands = uow.demands.list_for_version(version_id)

            problem = self._build_problem(operations, context, demands)
            result = self._engine.schedule(problem)

            assignments = [
                {
                    "operationId": a.operation_id,
                    "start": a.start,
                    "end": a.end,
                    "resourceId": a.resource_id,
                    "equipmentId": a.equipment_id,
                    "staffId": a.staff_id,
                }
                for a in result.assignments
            ]

            if result.feasible:
                plan.mark_version_scheduled(version_id)
                uow.plans.save(plan)
                uow.assignments.replace_for_version(version_id, assignments)

        return {
            "planId": plan_id,
            "versionId": version_id,
            "status": result.status,
            "feasible": result.feasible,
            "makespan": result.makespan,
            "assignments": assignments,
        }

    @staticmethod
    def _build_problem(operations, context, demands) -> PlanningProblem:
        # Operation identity is the operation instance id; dependencies in the
        # instances reference operation definition ids, so map them.
        def_to_instance = {op["operationDefinitionId"]: op["id"] for op in operations}

        if demands:
            weight = sum(d.priority.weight * d.quantity for d in demands)
            objective = OBJECTIVE_WEIGHTED_COMPLETION
        else:
            weight = 1
            objective = OBJECTIVE_MAKESPAN

        built_ops = tuple(
            Operation(
                identifier=op["id"],
                duration=op["duration"],
                required_capability=op["requiredCapability"],
                required_skill=op["requiredSkill"],
                depends_on=tuple(
                    def_to_instance[d] for d in op["dependsOn"] if d in def_to_instance
                ),
                weight=weight,
            )
            for op in operations
        )
        resources = tuple(
            Resource(identifier=e["id"], kind=EQUIPMENT, provides=frozenset(e["capabilities"]))
            for e in context.get("equipment", [])
        ) + tuple(
            Resource(identifier=s["id"], kind=STAFF, provides=frozenset(s["skills"]))
            for s in context.get("staff", [])
        )
        return PlanningProblem(
            operations=built_ops,
            resources=resources,
            policies=PlanningPolicies(objective=objective),
        )
