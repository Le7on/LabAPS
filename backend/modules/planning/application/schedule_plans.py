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
            # Overtime days (weekend/holiday any resource signed up for) become
            # extra working days in the calendar (ADR-022).
            staff_list = uow.staff.list()
            equipment_list = uow.equipment.list()
            all_overtime = sorted(
                {d for r in [*staff_list, *equipment_list] for d in r.overtime_dates}
            )
            slots = build_calendar(start, end, shift_mode, skipped, extra_workdays=all_overtime)
            if not slots:
                raise ValidationError("The combined calendar has no working days")

            # Which calendar days are "overtime-only" (weekend/holiday). A resource
            # may work such a day only if it is in that resource's overtime set.
            overtime_only_days = self._overtime_only_days(slots, skipped)

            workflows = {w.id: w for w in uow.workflow_definitions.list()}
            operations = self._build_operations(plans, slots, workflows)
            if not operations:
                raise ValidationError("Selected plans have no demand lines")

            resources = self._build_resources(
                staff_list, equipment_list, slots, overtime_only_days
            )
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
        """Materialize each demand line's selected Method into ``rounds`` pinned
        operations. A request targets one Method (SMDP/SAP/…), so each round is a
        single operation of that method, pinned to the target day (ADR-020)."""
        ops = []
        for plan in plans:
            for line in plan.demand_lines:
                wf = workflows.get(line.workflow_definition_id)
                if wf is None:
                    continue
                method = next(
                    (op for op in wf.operations if op.id == line.operation_definition_id), None
                )
                if method is None:
                    raise ValidationError(
                        f"Method {line.operation_definition_id} not in workflow {wf.id}"
                    )
                window = day_window(slots, line.target_date)
                if window is None:
                    raise ValidationError(f"Target date {line.target_date} is not a working day")
                for r in range(1, line.rounds + 1):
                    ops.append(
                        Operation(
                            identifier=f"{plan.id}:{line.id}:{method.id}#r{r}",
                            duration=method.duration,
                            required_capability=(f"m:{method.id}" if method.equipment_ids else None),
                            required_skill=(f"p:{wf.project_id}" if wf.project_id else None),
                            window=window,
                        )
                    )
        return ops

    @staticmethod
    def _overtime_only_days(slots, skipped) -> set[str]:
        """Calendar day strings that are only present because of overtime — i.e.
        weekends or holidays. A resource works them only if it signed up (ADR-022).
        """
        skip = set(skipped)
        out = set()
        for slot in slots:
            iso = slot.day.isoformat()
            if slot.day.weekday() >= 5 or iso in skip:
                out.add(iso)
        return out

    @staticmethod
    def _blocked_for(resource, overtime_only_days) -> list:
        """Dates the resource cannot work: its own unavailable days, plus every
        overtime-only day it did NOT sign up for."""
        overtime = set(resource.overtime_dates)
        blocked = set(resource.unavailable_dates)
        blocked |= {d for d in overtime_only_days if d not in overtime}
        return [[d, d] for d in sorted(blocked)]

    @classmethod
    def _build_resources(cls, staff_list, equipment_list, slots, overtime_only_days):
        """Active equipment (bound-method tokens) and staff (project tokens),
        masked by each resource's unavailable days and un-signed overtime days."""
        resources = []

        for e in equipment_list:
            if not e.active:
                continue
            windows = available_windows(slots, cls._blocked_for(e, overtime_only_days))
            if not windows:
                continue
            resources.append(
                Resource(
                    identifier=e.id,
                    kind=EQUIPMENT,
                    provides=frozenset(f"m:{mid}" for mid in e.method_ids),
                    windows=windows,
                    fv_duration=e.fv_duration,
                    fv_validity=e.fv_validity,
                )
            )

        for s in staff_list:
            if not s.active:
                continue
            windows = available_windows(slots, cls._blocked_for(s, overtime_only_days))
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
