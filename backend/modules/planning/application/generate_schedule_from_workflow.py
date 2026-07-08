"""Generate Schedule From Workflow use case.

Builds a PlanningProblem from persisted Laboratory Definition data instead of
hand-fed input: operations come from a Workflow Definition, and resources come
from the active Equipment pool. Runs the injected Scheduling Engine and returns
the assignments.

This is the first real Laboratory -> Planning -> Scheduling integration. It
reads across modules at the application layer (allowed); the domain and engines
stay module-independent.
"""

from __future__ import annotations

from backend.engines.planning.planning_problem import (
    EQUIPMENT,
    STAFF,
    Operation,
    PlanningPolicies,
    PlanningProblem,
    Resource,
)
from backend.engines.scheduling.scheduling_engine import SchedulingEngine
from backend.shared.errors import NotFoundError, ValidationError


class GenerateScheduleFromWorkflowUseCase:
    def __init__(self, uow_factory, scheduling_engine: SchedulingEngine):
        self._uow_factory = uow_factory
        self._engine = scheduling_engine

    def execute(self, plan_id: str, version_id: str, workflow_definition_id: str) -> dict:
        with self._uow_factory() as uow:
            plan = uow.plans.get(plan_id)
            workflow = uow.workflow_definitions.get(workflow_definition_id)
            equipment = [e for e in uow.equipment.list() if e.active]
            staff = [s for s in uow.staff.list() if s.active]

            if plan is None:
                raise NotFoundError(f"Plan {plan_id} not found")
            plan.get_version(version_id)  # raises NotFoundError if missing
            if workflow is None:
                raise NotFoundError(f"Workflow definition {workflow_definition_id} not found")
            if not workflow.operations:
                raise ValidationError("Workflow definition has no operations")

            problem = self._build_problem(workflow, equipment, staff)
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

            # BR-PV-002: a feasible schedule moves the version to Scheduled and
            # persists the assignments onto the version (replacing any prior run).
            if result.feasible:
                plan.mark_version_scheduled(version_id)
                uow.plans.save(plan)
                uow.assignments.replace_for_version(version_id, assignments)

        return {
            "planId": plan_id,
            "versionId": version_id,
            "workflowDefinitionId": workflow_definition_id,
            "status": result.status,
            "feasible": result.feasible,
            "makespan": result.makespan,
            "assignments": assignments,
        }

    @staticmethod
    def _build_problem(workflow, equipment, staff) -> PlanningProblem:
        # Operation identity is the operation definition id; dependencies in the
        # definition reference the same ids.
        operations = tuple(
            Operation(
                identifier=op.id,
                duration=op.duration,
                required_capability=op.required_capability,
                required_skill=op.required_skill,
                depends_on=tuple(op.depends_on),
            )
            for op in workflow.operations
        )
        resources = tuple(
            Resource(identifier=e.id, kind=EQUIPMENT, provides=frozenset(e.capabilities))
            for e in equipment
        ) + tuple(
            Resource(identifier=s.id, kind=STAFF, provides=frozenset(s.skills)) for s in staff
        )
        return PlanningProblem(
            operations=operations,
            resources=resources,
            policies=PlanningPolicies(),
        )
