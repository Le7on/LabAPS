"""OR-Tools CP-SAT Solver Adapter.

The only module permitted to import OR-Tools. Translates a SchedulingModel into
CP-SAT variables and constraints, solves for minimum makespan, and parses the
result back into a framework-free SchedulingSolution.
"""

from __future__ import annotations

from ortools.sat.python import cp_model

from backend.engines.scheduling.scheduling_model import (
    EQUIPMENT,
    Objective,
    ResourceAssignment,
    ScheduledTask,
    SchedulingModel,
    SchedulingSolution,
)
from backend.solver.adapter.solver_adapter import SolverAdapter

_STATUS_NAMES = {
    cp_model.OPTIMAL: "optimal",
    cp_model.FEASIBLE: "feasible",
    cp_model.INFEASIBLE: "infeasible",
    cp_model.MODEL_INVALID: "model_invalid",
    cp_model.UNKNOWN: "unknown",
}


class ORToolsSolverAdapter(SolverAdapter):
    """Translates a SchedulingModel into CP-SAT and minimizes makespan.

    Constraint categories implemented (Constraint Framework):

    - Dependency: a task starts only after its predecessors end (FS, lag 0).
    - Capability: a task is assigned only to a resource whose capability set
      satisfies its requirement (enforced by only creating assignment literals
      for eligible resources).
    - Resource: a resource performs one task at a time (no-overlap on the
      resource's optional intervals). Cardinality: each task is assigned to
      exactly one resource when resources are present.

    Objective (ADR-007): either minimize makespan, or minimize demand-weighted
    completion time (sum of weight * end), selected by ``model.objective``. The
    weighted objective pulls higher-priority demand earlier; makespan is always
    computed and reported.
    """

    def __init__(self, max_time_in_seconds: float = 10.0):
        self._max_time = max_time_in_seconds

    def solve(self, model: SchedulingModel) -> SchedulingSolution:
        if not model.tasks:
            return SchedulingSolution(status="optimal", feasible=True, makespan=0)

        cp = cp_model.CpModel()
        horizon = model.horizon

        starts: dict[str, cp_model.IntVar] = {}
        ends: dict[str, cp_model.IntVar] = {}

        # Policy Constraint (frozen window): no task starts before frozen_until.
        earliest = max(0, model.frozen_until)

        # Each task is optionally scheduled: work that can't be placed (no
        # eligible resource, or no room) is left unscheduled and surfaced as a
        # conflict, rather than making the whole run infeasible.
        scheduled: dict[str, cp_model.IntVar] = {}

        for task in model.tasks:
            sched = cp.new_bool_var(f"sched_{task.identifier}")
            scheduled[task.identifier] = sched

            # Variables span the whole horizon so the model is always satisfiable
            # (an unplaced task just sits anywhere with scheduled=0). The end domain
            # is widened by the duration so ``end == start + duration`` always has a
            # solution even for a task too long to fit — such a task is simply left
            # unscheduled (window/horizon bounds below apply only WHEN scheduled).
            start = cp.new_int_var(earliest, horizon, f"start_{task.identifier}")
            end = cp.new_int_var(earliest, horizon + task.duration, f"end_{task.identifier}")
            cp.add(end == start + task.duration)
            starts[task.identifier] = start
            ends[task.identifier] = end

            # A task longer than the whole horizon can never be placed.
            if task.duration > horizon - earliest:
                cp.add(sched == 0)
            else:
                cp.add(end <= horizon).only_enforce_if(sched)

            lo = max(earliest, task.window[0]) if task.window else earliest
            hi = min(horizon, task.window[1]) if task.window else horizon
            if hi < lo:
                cp.add(sched == 0)
            else:
                cp.add(start >= lo).only_enforce_if(sched)
                cp.add(end <= hi).only_enforce_if(sched)

        # Dependency: a task runs only after its predecessors; a task can only be
        # scheduled if all its predecessors are (can't do step 2 without step 1).
        for task in model.tasks:
            for predecessor in task.predecessors:
                if predecessor in ends:
                    cp.add(starts[task.identifier] >= ends[predecessor]).only_enforce_if(
                        scheduled[task.identifier]
                    )
                    cp.add(scheduled[task.identifier] <= scheduled[predecessor])

        assignment = self._add_resource_assignment(cp, model, starts, ends, scheduled)

        # Upper bound allows an unscheduled over-long task's end to exceed the
        # horizon without making the max-equality infeasible.
        max_end = horizon + sum(t.duration for t in model.tasks)
        makespan = cp.new_int_var(0, max_end, "makespan")
        cp.add_max_equality(makespan, list(ends.values()))

        # Objective: schedule as much as possible first (each scheduled task is
        # worth far more than any timing cost), then optimize timing. ``big`` must
        # strictly exceed the largest possible ``timing`` so one more scheduled
        # task always dominates any timing improvement.
        placed = sum(scheduled.values())
        if model.objective == Objective.WEIGHTED_COMPLETION:
            task_map = model.task_map()
            timing = sum(task_map[tid].weight * end for tid, end in ends.items())
            max_timing = sum(task_map[tid].weight for tid in ends) * max_end
        else:
            timing = makespan
            max_timing = max_end
        big = max_timing + 1
        cp.maximize(big * placed - timing)

        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = self._max_time
        status = solver.solve(cp)

        feasible = status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
        if not feasible:
            return SchedulingSolution(status=_STATUS_NAMES.get(status, "unknown"), feasible=False)

        scheduled_tasks = []
        unscheduled = []
        for task in model.tasks:
            if solver.value(scheduled[task.identifier]) == 1:
                scheduled_tasks.append(
                    ScheduledTask(
                        identifier=task.identifier,
                        start=solver.value(starts[task.identifier]),
                        end=solver.value(ends[task.identifier]),
                        assignments=self._resolve_assignments(
                            solver, assignment, task.identifier
                        ),
                    )
                )
            else:
                unscheduled.append(task.identifier)

        # Surface FV occupancy as tasks so they appear in the timeline (ADR-019).
        for resource in model.resources:
            for i, (s, e) in enumerate(resource.fv_intervals(model.horizon)):
                if e <= s:
                    continue
                scheduled_tasks.append(
                    ScheduledTask(
                        identifier=f"FV-{resource.identifier}-{i + 1}",
                        start=s,
                        end=e,
                        assignments=(ResourceAssignment(EQUIPMENT, resource.identifier),),
                        is_fv=True,
                    )
                )

        return SchedulingSolution(
            scheduled_tasks=tuple(scheduled_tasks),
            makespan=solver.value(makespan),
            status=_STATUS_NAMES.get(status, "unknown"),
            feasible=True,
            unscheduled=tuple(unscheduled),
            diagnostics={"wall_time": solver.wall_time},
        )

    def _add_resource_assignment(self, cp, model, starts, ends, scheduled):
        """Add per-kind assignment literals, capability/skill matching and
        resource no-overlap.

        For each resource kind a task requires, the task — *if scheduled* — is
        assigned exactly one eligible resource, and no resource does two tasks at
        once. A task with no eligible resource for a required kind cannot be
        scheduled (``scheduled == 0``), so it surfaces as a conflict.

        Returns ``{task_id: {kind: {resource_id: literal}}}``.
        """

        assignment: dict[str, dict[str, dict[str, cp_model.IntVar]]] = {}
        per_resource: dict[str, list] = {r.identifier: [] for r in model.resources}

        present_kinds = set(model.kinds())
        for task in model.tasks:
            task_literals: dict[str, dict[str, cp_model.IntVar]] = {}

            for kind in present_kinds:
                required = task.requires(kind)
                eligible = model.eligible_resources(task, kind)

                if not required:
                    continue
                if not eligible:
                    # A kind is present but no resource is eligible for this task
                    # -> it cannot be scheduled (surfaced as a conflict).
                    cp.add(scheduled[task.identifier] == 0)
                    continue

                literals: dict[str, cp_model.IntVar] = {}
                for resource in eligible:
                    present = cp.new_bool_var(
                        f"assign_{task.identifier}_{kind}_{resource.identifier}"
                    )
                    literals[resource.identifier] = present
                    optional = cp.new_optional_interval_var(
                        starts[task.identifier],
                        task.duration,
                        ends[task.identifier],
                        present,
                        f"opt_{task.identifier}_{kind}_{resource.identifier}",
                    )
                    per_resource[resource.identifier].append(optional)
                    self._add_calendar_constraint(cp, task, resource, present, starts, ends)

                # Assigned exactly one eligible resource iff the task is scheduled.
                cp.add(sum(literals.values()) == scheduled[task.identifier])
                task_literals[kind] = literals

            assignment[task.identifier] = task_literals

        # FV validity (ADR-019): pre-place fixed FV occupancy intervals on each
        # equipment. They join the machine's no-overlap set, so normal work is
        # pushed into the tiled gaps — which are exactly the in-validity windows.
        for resource in model.resources:
            for i, (s, e) in enumerate(resource.fv_intervals(model.horizon)):
                if e <= s:
                    continue
                fv_interval = cp.new_interval_var(s, e - s, e, f"fv_{resource.identifier}_{i}")
                per_resource[resource.identifier].append(fv_interval)

        # Resource: each resource does one task at a time.
        for optional_intervals in per_resource.values():
            if optional_intervals:
                cp.add_no_overlap(optional_intervals)

        return assignment

    @staticmethod
    def _add_calendar_constraint(cp, task, resource, present, starts, ends):
        """Calendar Constraint: if assigned to a windowed resource, the task must
        fit entirely within one of the resource's availability windows.
        """
        if not resource.windows:
            return

        start = starts[task.identifier]
        end = ends[task.identifier]
        fits = []
        for w_index, (w_start, w_end) in enumerate(resource.windows):
            in_window = cp.new_bool_var(f"win_{task.identifier}_{resource.identifier}_{w_index}")
            cp.add(start >= w_start).only_enforce_if(in_window)
            cp.add(end <= w_end).only_enforce_if(in_window)
            fits.append(in_window)
        # When assigned to this resource, exactly one window must hold.
        cp.add_exactly_one(fits).only_enforce_if(present)

    @staticmethod
    def _resolve_assignments(solver, assignment, task_id):
        from backend.engines.scheduling.scheduling_model import ResourceAssignment

        by_kind = assignment.get(task_id) if assignment else None
        if not by_kind:
            return ()

        result = []
        for kind, literals in by_kind.items():
            for resource_id, present in literals.items():
                if solver.value(present) == 1:
                    result.append(ResourceAssignment(kind=kind, resource_id=resource_id))
                    break
        return tuple(result)
