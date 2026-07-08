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

        assignment = self._add_resource_assignment(cp, model, starts, ends, horizon)
        if assignment is None:
            # An operation has no capable resource: the problem is infeasible.
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
                resource_id=self._resolve_resource(solver, assignment, task.identifier),
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

    def _add_resource_assignment(self, cp, model, starts, ends, horizon):
        """Add assignment literals + capability + resource no-overlap.

        Returns a map ``{task_id: {resource_id: literal}}``, an empty dict when
        the model has no resources (timing-only scheduling), or ``None`` when a
        task has no eligible resource (infeasible).
        """

        if not model.resources:
            return {}

        assignment: dict[str, dict[str, cp_model.IntVar]] = {}
        # Collect optional intervals per resource for the no-overlap constraint.
        per_resource: dict[str, list] = {r.identifier: [] for r in model.resources}

        for task in model.tasks:
            eligible = model.eligible_resources(task)
            if not eligible:
                return None

            literals: dict[str, cp_model.IntVar] = {}
            for resource in eligible:
                present = cp.new_bool_var(f"assign_{task.identifier}_{resource.identifier}")
                literals[resource.identifier] = present
                optional = cp.new_optional_interval_var(
                    starts[task.identifier],
                    task.duration,
                    ends[task.identifier],
                    present,
                    f"opt_{task.identifier}_{resource.identifier}",
                )
                per_resource[resource.identifier].append(optional)

            # Cardinality: exactly one resource performs the task.
            cp.add_exactly_one(literals.values())
            assignment[task.identifier] = literals

        # Resource: each resource does one task at a time.
        for optional_intervals in per_resource.values():
            if optional_intervals:
                cp.add_no_overlap(optional_intervals)

        return assignment

    @staticmethod
    def _resolve_resource(solver, assignment, task_id):
        literals = assignment.get(task_id) if assignment else None
        if not literals:
            return None
        for resource_id, present in literals.items():
            if solver.value(present) == 1:
                return resource_id
        return None
