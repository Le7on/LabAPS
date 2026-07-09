"""OR-Tools objective tests: makespan vs weighted completion.

Skipped automatically if OR-Tools is not installed.
"""

from __future__ import annotations

import pytest

pytest.importorskip("ortools")

from backend.engines.scheduling.scheduling_model import (
    EQUIPMENT,
    Objective,
    SchedulingModel,
    SchedulingResource,
    Task,
)
from backend.solver.adapter.ortools_solver_adapter import ORToolsSolverAdapter


def _model(objective, weights):
    # Two tasks competing for one resource (so their order matters).
    return SchedulingModel(
        tasks=(
            Task(
                identifier="light",
                duration=2,
                requirements=frozenset({(EQUIPMENT, "cap")}),
                weight=weights[0],
            ),
            Task(
                identifier="heavy",
                duration=5,
                requirements=frozenset({(EQUIPMENT, "cap")}),
                weight=weights[1],
            ),
        ),
        resources=(
            SchedulingResource(identifier="eq", kind=EQUIPMENT, provides=frozenset({"cap"})),
        ),
        horizon=50,
        objective=objective,
    )


def test_weighted_completion_schedules_high_weight_task_first():
    solution = ORToolsSolverAdapter(max_time_in_seconds=5).solve(
        _model(Objective.WEIGHTED_COMPLETION, weights=(1, 10))
    )
    assert solution.feasible
    placements = {t.identifier: t for t in solution.scheduled_tasks}
    # The heavier-weight task should run first (start at 0).
    assert placements["heavy"].start == 0
    assert placements["light"].start >= placements["heavy"].end


def test_makespan_objective_is_unaffected_by_weights():
    solution = ORToolsSolverAdapter(max_time_in_seconds=5).solve(
        _model(Objective.MAKESPAN, weights=(1, 10))
    )
    assert solution.feasible
    # Both objectives serialize on one resource, so makespan is 2 + 5 = 7.
    assert solution.makespan == 7
