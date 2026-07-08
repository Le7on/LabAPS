"""OR-Tools CP-SAT Solver Adapter.

The only module permitted to import OR-Tools. Translates a SchedulingModel into
CP-SAT variables and constraints, solves for minimum makespan, and parses the
result back into a framework-free SchedulingSolution.
"""

from __future__ import annotations

from ortools.sat.python import cp_model

from backend.engines.scheduling.scheduling_model import (
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

    Objective: minimize makespan. Note: makespan is an interim objective — the
    Objective Model doc lists demand/utilization goals that require entities not
    yet modelled (see ADR-007, session log).
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
        intervals: dict[str, cp_model.IntervalVar] = {}

        for task in model.tasks:
            start = cp.new_int_var(0, horizon, f"start_{task.identifier}")
            end = cp.new_int_var(0, horizon, f"end_{task.identifier}")
            interval = cp.new_interval_var(start, task.duration, end, f"interval_{task.identifier}")
            starts[task.identifier] = start
            ends[task.identifier] = end
            intervals[task.identifier] = interval

        # Dependency: a task starts only after all its predecessors end.
        for task in model.tasks:
            for predecessor in task.predecessors:
                if predecessor in ends:
                    cp.add(starts[task.identifier] >= ends[predecessor])

        assignment = self._add_resource_assignment(cp, model, starts, ends)
        if assignment is None:
            # An operation has no eligible resource for a required kind: infeasible.
            return SchedulingSolution(status="infeasible", feasible=False)

        makespan = cp.new_int_var(0, horizon, "makespan")
        cp.add_max_equality(makespan, list(ends.values()))
        cp.minimize(makespan)

        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = self._max_time
        status = solver.solve(cp)

        feasible = status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
        if not feasible:
            return SchedulingSolution(status=_STATUS_NAMES.get(status, "unknown"), feasible=False)

        scheduled = tuple(
            ScheduledTask(
                identifier=task.identifier,
                start=solver.value(starts[task.identifier]),
                end=solver.value(ends[task.identifier]),
                assignments=self._resolve_assignments(solver, assignment, task.identifier),
            )
            for task in model.tasks
        )

        return SchedulingSolution(
            scheduled_tasks=scheduled,
            makespan=solver.value(makespan),
            status=_STATUS_NAMES.get(status, "unknown"),
            feasible=True,
            diagnostics={"wall_time": solver.wall_time},
        )

    def _add_resource_assignment(self, cp, model, starts, ends):
        """Add per-kind assignment literals, capability/skill matching and
        resource no-overlap.

        For each resource kind present (equipment, staff), a task that requires
        that kind is assigned exactly one eligible resource, and no resource does
        two tasks at once. A kind a task does not require is skipped for it.

        Returns a nested map ``{task_id: {kind: {resource_id: literal}}}``, an
        empty dict when the model has no resources, or ``None`` when a task has a
        requirement for a kind but no eligible resource (infeasible).
        """

        if not model.resources:
            return {}

        assignment: dict[str, dict[str, dict[str, cp_model.IntVar]]] = {}
        per_resource: dict[str, list] = {r.identifier: [] for r in model.resources}

        for task in model.tasks:
            task_literals: dict[str, dict[str, cp_model.IntVar]] = {}

            for kind in model.kinds():
                requirement = task.requirement_for(kind)
                eligible = model.eligible_resources(task, kind)

                # Only enforce a kind when the task requires it. If required but
                # nothing is eligible, the problem is infeasible.
                if requirement is None and not eligible:
                    continue
                if requirement is not None and not eligible:
                    return None
                if requirement is None:
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

                cp.add_exactly_one(literals.values())
                task_literals[kind] = literals

            assignment[task.identifier] = task_literals

        # Resource: each resource does one task at a time.
        for optional_intervals in per_resource.values():
            if optional_intervals:
                cp.add_no_overlap(optional_intervals)

        return assignment

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
