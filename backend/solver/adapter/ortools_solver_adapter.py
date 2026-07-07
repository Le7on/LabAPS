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
    def __init__(self, max_time_in_seconds: float = 10.0):
        self._max_time = max_time_in_seconds

    def solve(self, model: SchedulingModel) -> SchedulingSolution:
        if not model.tasks:
            return SchedulingSolution(status="optimal", feasible=True, makespan=0)

        cp = cp_model.CpModel()
        horizon = model.horizon

        starts: dict[str, cp_model.IntVar] = {}
        ends: dict[str, cp_model.IntVar] = {}

        for task in model.tasks:
            start = cp.new_int_var(0, horizon, f"start_{task.identifier}")
            end = cp.new_int_var(0, horizon, f"end_{task.identifier}")
            cp.add(end == start + task.duration)
            starts[task.identifier] = start
            ends[task.identifier] = end

        # Precedence: a task starts only after all its predecessors end.
        for task in model.tasks:
            for predecessor in task.predecessors:
                if predecessor in ends:
                    cp.add(starts[task.identifier] >= ends[predecessor])

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
