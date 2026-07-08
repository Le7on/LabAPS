"""Test doubles for the scheduling engine.

FakeSolverAdapter places tasks sequentially without importing OR-Tools, so engine
wiring can be tested in isolation from the optimizer.
"""

from __future__ import annotations

from backend.engines.scheduling.scheduling_model import (
    ResourceAssignment,
    ScheduledTask,
    SchedulingModel,
    SchedulingSolution,
)
from backend.solver.adapter.solver_adapter import SolverAdapter


class FakeSolverAdapter(SolverAdapter):
    """Schedules tasks back-to-back in declaration order (ignores precedence).

    When resources are present, assigns each task to its first eligible resource
    and reports infeasible if any task has no eligible resource.
    """

    def solve(self, model: SchedulingModel) -> SchedulingSolution:
        cursor = 0
        scheduled: list[ScheduledTask] = []
        for task in model.tasks:
            assignments: list[ResourceAssignment] = []
            for kind in model.kinds():
                if task.requirement_for(kind) is None:
                    continue
                eligible = model.eligible_resources(task, kind)
                if not eligible:
                    return SchedulingSolution(status="infeasible", feasible=False)
                assignments.append(
                    ResourceAssignment(kind=kind, resource_id=eligible[0].identifier)
                )

            scheduled.append(
                ScheduledTask(
                    identifier=task.identifier,
                    start=cursor,
                    end=cursor + task.duration,
                    assignments=tuple(assignments),
                )
            )
            cursor += task.duration

        return SchedulingSolution(
            scheduled_tasks=tuple(scheduled),
            makespan=cursor,
            status="fake",
            feasible=True,
        )
