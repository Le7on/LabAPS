"""Test doubles for the scheduling engine.

FakeSolverAdapter places tasks sequentially without importing OR-Tools, so engine
wiring can be tested in isolation from the optimizer.
"""

from __future__ import annotations

from backend.engines.scheduling.scheduling_model import (
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
            resource_id = None
            if model.resources:
                eligible = model.eligible_resources(task)
                if not eligible:
                    return SchedulingSolution(status="infeasible", feasible=False)
                resource_id = eligible[0].identifier

            scheduled.append(
                ScheduledTask(
                    identifier=task.identifier,
                    start=cursor,
                    end=cursor + task.duration,
                    resource_id=resource_id,
                )
            )
            cursor += task.duration

        return SchedulingSolution(
            scheduled_tasks=tuple(scheduled),
            makespan=cursor,
            status="fake",
            feasible=True,
        )
