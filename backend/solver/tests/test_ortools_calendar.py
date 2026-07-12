"""OR-Tools calendar constraint tests (resource availability windows).

Skipped automatically if OR-Tools is not installed.
"""

from __future__ import annotations

import pytest

pytest.importorskip("ortools")

from backend.engines.scheduling.scheduling_model import (
    EQUIPMENT,
    SchedulingModel,
    SchedulingResource,
    Task,
)
from backend.solver.adapter.ortools_solver_adapter import ORToolsSolverAdapter


def _solve(resource):
    model = SchedulingModel(
        tasks=(Task(identifier="t1", duration=3, requirements=frozenset({(EQUIPMENT, "cap")})),),
        resources=(resource,),
        horizon=100,
    )
    return ORToolsSolverAdapter(max_time_in_seconds=5).solve(model)


def test_task_scheduled_within_availability_window():
    # Resource only available in [10, 20): the task must start at or after 10.
    resource = SchedulingResource(
        identifier="eq", kind=EQUIPMENT, provides=frozenset({"cap"}), windows=((10, 20),)
    )
    solution = _solve(resource)
    assert solution.feasible
    placed = solution.scheduled_tasks[0]
    assert placed.start >= 10
    assert placed.end <= 20


def test_task_unscheduled_when_no_window_fits():
    # Only a 2-unit window, but the task needs 3 units: it can't be placed, so it
    # is left unscheduled (a conflict) while the run itself succeeds.
    resource = SchedulingResource(
        identifier="eq", kind=EQUIPMENT, provides=frozenset({"cap"}), windows=((0, 2),)
    )
    solution = _solve(resource)
    assert solution.feasible
    assert solution.scheduled_tasks == ()
    assert len(solution.unscheduled) == 1


def test_task_uses_a_later_window_when_needed():
    # Two windows; only the second is long enough for a 3-unit task.
    resource = SchedulingResource(
        identifier="eq",
        kind=EQUIPMENT,
        provides=frozenset({"cap"}),
        windows=((0, 2), (30, 40)),
    )
    solution = _solve(resource)
    assert solution.feasible
    placed = solution.scheduled_tasks[0]
    assert placed.start >= 30
    assert placed.end <= 40
