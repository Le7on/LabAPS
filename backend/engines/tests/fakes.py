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
    """Schedules tasks back-to-back in declaration order (ignores precedence)."""

    def solve(self, model: SchedulingModel) -> SchedulingSolution:
        cursor = 0
        scheduled: list[ScheduledTask] = []
        for task in model.tasks:
            scheduled.append(
                ScheduledTask(identifier=task.identifier, start=cursor, end=cursor + task.duration)
            )
            cursor += task.duration

        return SchedulingSolution(
            scheduled_tasks=tuple(scheduled),
            makespan=cursor,
            status="fake",
            feasible=True,
        )
