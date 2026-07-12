"""OR-Tools Policy constraint tests (frozen planning window).

Skipped automatically if OR-Tools is not installed.
"""

from __future__ import annotations

import pytest

pytest.importorskip("ortools")

from backend.engines.scheduling.scheduling_model import SchedulingModel, Task
from backend.solver.adapter.ortools_solver_adapter import ORToolsSolverAdapter


def _solve(frozen_until):
    model = SchedulingModel(
        tasks=(Task(identifier="t1", duration=3),),
        horizon=100,
        frozen_until=frozen_until,
    )
    return ORToolsSolverAdapter(max_time_in_seconds=5).solve(model)


def test_no_frozen_window_starts_at_zero():
    solution = _solve(0)
    assert solution.feasible
    assert solution.scheduled_tasks[0].start == 0


def test_frozen_window_pushes_start_past_boundary():
    solution = _solve(15)
    assert solution.feasible
    assert solution.scheduled_tasks[0].start >= 15


def test_frozen_window_exceeding_horizon_leaves_task_unscheduled():
    # Frozen boundary leaves no room for the 3-unit task before the horizon: the
    # run stays feasible and the task is unscheduled (a conflict), per ADR-023.
    model = SchedulingModel(
        tasks=(Task(identifier="t1", duration=3),),
        horizon=10,
        frozen_until=9,
    )
    solution = ORToolsSolverAdapter(max_time_in_seconds=5).solve(model)
    assert solution.feasible
    assert solution.scheduled_tasks == ()
    assert solution.unscheduled == ("t1",)
