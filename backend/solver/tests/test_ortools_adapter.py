"""OR-Tools solver adapter tests.

Verifies the real CP-SAT adapter honors durations and precedence and minimizes
makespan. Skipped automatically if OR-Tools is not installed.
"""

from __future__ import annotations

import pytest

pytest.importorskip("ortools")

from backend.engines.scheduling.scheduling_model import SchedulingModel, Task
from backend.solver.adapter.ortools_solver_adapter import ORToolsSolverAdapter


def test_solver_respects_precedence_and_minimizes_makespan():
    model = SchedulingModel(
        tasks=(
            Task(identifier="a", duration=3),
            Task(identifier="b", duration=2, predecessors=("a",)),
        ),
        horizon=50,
    )

    solution = ORToolsSolverAdapter(max_time_in_seconds=5).solve(model)

    assert solution.feasible
    placements = {t.identifier: t for t in solution.scheduled_tasks}
    # b must start only after a finishes.
    assert placements["b"].start >= placements["a"].end
    # Optimal makespan for a(3) -> b(2) in sequence is 5.
    assert solution.makespan == 5


def test_solver_handles_empty_model():
    solution = ORToolsSolverAdapter().solve(SchedulingModel())
    assert solution.feasible
    assert solution.makespan == 0
