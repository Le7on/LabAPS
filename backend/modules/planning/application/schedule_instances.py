"""Schedule From Instances use case.

Schedules the persisted Operation Instances of a Plan Version against the
resources captured in its immutable Planning Context snapshot (ADR-008: planning
never depends on live configuration after scheduling begins). Persists the
resulting assignments and marks the version Scheduled.
"""

from __future__ import annotations

from backend.engines.planning.calendar import (
    available_windows,
    build_calendar,
    map_interval,
)
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

    def execute(self, plan_id: str, version_id: str, frozen_until: int = 0) -> dict:
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

            # Calendar (ADR-016): a plan always has a date range, so the horizon
            # is the number of shift slots and each assignment maps to real dates.
            slots = build_calendar(
                plan.start_date, plan.end_date, plan.shift_mode, plan.skipped_dates
            )
            if not slots:
                raise ValidationError("The plan calendar has no working days (all dates skipped)")
            horizon = len(slots)

            problem = self._build_problem(
                operations, context, demands, frozen_until, horizon, slots
            )
            result = self._engine.schedule(problem)

            assignments = []
            for a in result.assignments:
                assignment = {
                    "operationId": a.operation_id,
                    "start": a.start,
                    "end": a.end,
                    "resourceId": a.resource_id,
                    "equipmentId": a.equipment_id,
                    "staffId": a.staff_id,
                }
                mapped = map_interval(slots, a.start, a.end)
                if mapped:
                    assignment.update(mapped)
                assignments.append(assignment)

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
    def _build_problem(
        operations, context, demands, frozen_until, horizon, slots
    ) -> PlanningProblem:
        # Operation identity is the operation instance id; dependencies in the
        # instances already reference instance ids (run r -> run r of each
        # prerequisite), so they are used directly. Guard against dangling refs.
        instance_ids = {op["id"] for op in operations}

        if demands:
            weight = sum(d.priority.weight * d.quantity for d in demands)
            objective = OBJECTIVE_WEIGHTED_COMPLETION
        else:
            weight = 1
            objective = OBJECTIVE_MAKESPAN

        # Equipment binding (ADR-015): a method's equipment candidates are
        # exactly the equipment bound to it, not capability matches. We express
        # this with a synthetic per-method token: the method requires token
        # ``m:<instanceId>`` and each bound equipment provides that token. This
        # restricts the method to its bound equipment using the existing
        # attribute-matching solver, with no solver change.
        equipment_tokens: dict[str, set[str]] = {}
        method_token: dict[str, str | None] = {}
        for op in operations:
            bound = op.get("equipmentIds") or []
            token = f"m:{op['id']}" if bound else None
            method_token[op["id"]] = token
            if token:
                for eid in bound:
                    equipment_tokens.setdefault(eid, set()).add(token)

        # Staff eligibility (ADR-017): a method is performed by staff qualified
        # for the method's workflow project. Expressed as a project token: the
        # method requires ``p:<projectId>`` and each staff member provides a
        # token for every project it is qualified for.
        def project_token(project_id):
            return f"p:{project_id}" if project_id else None

        built_ops = tuple(
            Operation(
                identifier=op["id"],
                duration=op["duration"],
                required_capability=method_token[op["id"]],
                required_skill=project_token(op.get("requiredProjectId")),
                depends_on=tuple(d for d in op["dependsOn"] if d in instance_ids),
                weight=weight,
            )
            for op in operations
        )

        def windows_for(res):
            # A resource's global unavailable days (leave / maintenance) become
            # the complementary available shift-slot windows; the solver then
            # keeps work off those days. Single dates are treated as 1-day ranges.
            # A resource unavailable every day keeps a zero-length window so it
            # stays present but can host nothing (its requirement isn't silently
            # dropped — the task surfaces as a conflict instead).
            ranges = [[d, d] for d in res.get("unavailableDates", [])]
            return available_windows(slots, ranges) or ((0, 0),)

        resources = tuple(
            Resource(
                identifier=e["id"],
                kind=EQUIPMENT,
                provides=frozenset(equipment_tokens.get(e["id"], set())),
                windows=windows_for(e),
                fv_duration=int(e.get("fvDuration", 0) or 0),
                fv_validity=int(e.get("fvValidity", 0) or 0),
            )
            for e in context.get("equipment", [])
        ) + tuple(
            Resource(
                identifier=s["id"],
                kind=STAFF,
                provides=frozenset(f"p:{pid}" for pid in s.get("qualifiedProjectIds", [])),
                windows=windows_for(s),
            )
            for s in context.get("staff", [])
        )
        policies = PlanningPolicies(
            objective=objective, frozen_until=frozen_until, planning_horizon=horizon
        )
        return PlanningProblem(
            operations=built_ops,
            resources=resources,
            policies=policies,
        )
