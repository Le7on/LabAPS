"""Schedule Selected Plans use case (ADR-020/021).

Merges the demand lines of several selected plans into ONE scheduling run over a
shared calendar and a shared pool of active resources. Each demand line
(workflow x rounds on a target date) is materialized into ``rounds`` workflow
instances whose operations are pinned to the target day. Global per-resource
unavailable dates (ADR-021) mask the calendar. Returns dated assignments.
"""

from __future__ import annotations

from backend.engines.planning.calendar import (
    available_windows,
    build_calendar,
    day_window,
    map_interval,
)
from backend.engines.planning.planning_problem import (
    EQUIPMENT,
    OBJECTIVE_MAKESPAN,
    STAFF,
    Operation,
    PlanningPolicies,
    PlanningProblem,
    Resource,
)
from backend.engines.scheduling.scheduling_engine import SchedulingEngine
from backend.shared.errors import NotFoundError, ValidationError


class SchedulePlansUseCase:
    def __init__(self, uow_factory, scheduling_engine: SchedulingEngine):
        self._uow_factory = uow_factory
        self._engine = scheduling_engine

    def execute(self, plan_ids: list[str], shift_mode: str = "single") -> dict:
        if not plan_ids:
            raise ValidationError("Select at least one plan to schedule")

        with self._uow_factory() as uow:
            plans = []
            for pid in plan_ids:
                plan = uow.plans.get(pid)
                if plan is None:
                    raise NotFoundError(f"Plan {pid} not found")
                plans.append(plan)

            # Unified calendar spans the earliest start to the latest end across
            # all selected plans; holidays are the union of skipped dates.
            start = min(p.start_date for p in plans)
            end = max(p.end_date for p in plans)
            skipped = sorted({d for p in plans for d in p.skipped_dates})
            slots = build_calendar(start, end, shift_mode, skipped)
            if not slots:
                raise ValidationError("The combined calendar has no working days")

            workflows = {w.id: w for w in uow.workflow_definitions.list()}
            operations = self._build_operations(plans, slots, workflows)
            if not operations:
                raise ValidationError("Selected plans have no demand lines")

            resources = self._build_resources(uow, slots)
            problem = PlanningProblem(
                operations=tuple(operations),
                resources=tuple(resources),
                policies=PlanningPolicies(
                    objective=OBJECTIVE_MAKESPAN, planning_horizon=len(slots)
                ),
            )
            result = self._engine.schedule(problem)

            assignments = []
            for a in result.assignments:
                item = {
                    "operationId": a.operation_id,
                    "start": a.start,
                    "end": a.end,
                    "equipmentId": a.equipment_id,
                    "staffId": a.staff_id,
                }
                mapped = map_interval(slots, a.start, a.end)
                if mapped:
                    item.update(mapped)
                assignments.append(item)

        return {
            "planIds": plan_ids,
            "startDate": start,
            "endDate": end,
            "status": result.status,
            "feasible": result.feasible,
            "assignments": assignments,
        }

    # -- problem building -------------------------------------------------

    @staticmethod
    def _build_operations(plans, slots, workflows):
        """Materialize every demand line into pinned workflow-instance operations."""
        ops = []
        for plan in plans:
            for line in plan.demand_lines:
                wf = workflows.get(line.workflow_definition_id)
                if wf is None or not wf.operations:
                    continue
                window = day_window(slots, line.target_date)
                if window is None:
                    raise ValidationError(f"Target date {line.target_date} is not a working day")
                for r in range(1, line.rounds + 1):
                    id_by_type = {}
                    for op in wf.operations:
                        inst_id = f"{plan.id}:{line.id}:{op.id}#r{r}"
                        id_by_type[op.operation_type] = inst_id
                    for op in wf.operations:
                        ops.append(
                            Operation(
                                identifier=id_by_type[op.operation_type],
                                duration=op.duration,
                                required_capability=(f"m:{op.id}" if op.equipment_ids else None),
                                required_skill=(f"p:{wf.project_id}" if wf.project_id else None),
                                depends_on=tuple(
                                    id_by_type[dep] for dep in op.depends_on if dep in id_by_type
                                ),
                                window=window,
                            )
                        )
        return ops

    @staticmethod
    def _build_resources(uow, slots):
        """Active equipment (bound-method tokens) and staff (project tokens),
        masked by each resource's global unavailable dates."""
        resources = []

        # Which methods each equipment can run -> synthetic per-method token.
        for e in uow.equipment.list():
            if not e.active:
                continue
            windows = available_windows(slots, [[d, d] for d in e.unavailable_dates])
            if not windows:
                continue
            provides = {f"m:{mid}" for mid in e.method_ids}
            resources.append(
                Resource(
                    identifier=e.id,
                    kind=EQUIPMENT,
                    provides=frozenset(provides),
                    windows=windows,
                    fv_duration=e.fv_duration,
                    fv_validity=e.fv_validity,
                )
            )

        for s in uow.staff.list():
            if not s.active:
                continue
            windows = available_windows(slots, [[d, d] for d in s.unavailable_dates])
            if not windows:
                continue
            resources.append(
                Resource(
                    identifier=s.id,
                    kind=STAFF,
                    provides=frozenset(f"p:{pid}" for pid in s.qualified_project_ids),
                    windows=windows,
                )
            )
        return resources
