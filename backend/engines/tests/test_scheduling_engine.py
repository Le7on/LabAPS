"""Scheduling engine pipeline tests (using the fake solver)."""

from __future__ import annotations

import pytest

from backend.engines.planning.planning_problem import (
    Operation,
    PlanningPolicies,
    PlanningProblem,
)
from backend.engines.scheduling.scheduling_engine import SchedulingEngine
from backend.engines.tests.fakes import FakeSolverAdapter
from backend.shared.errors import ValidationError


def _problem() -> PlanningProblem:
    return PlanningProblem(
        operations=(
            Operation(identifier="op1", duration=3),
            Operation(identifier="op2", duration=2, depends_on=("op1",)),
        ),
        policies=PlanningPolicies(planning_horizon=50),
    )


def test_engine_produces_assignments_for_each_operation():
    engine = SchedulingEngine(solver_adapter=FakeSolverAdapter())

    result = engine.schedule(_problem())

    assert result.feasible
    assert len(result.assignments) == 2
    assert result.makespan == 5
    ids = {a.operation_id for a in result.assignments}
    assert ids == {"op1", "op2"}


def test_engine_rejects_empty_problem():
    engine = SchedulingEngine(solver_adapter=FakeSolverAdapter())

    with pytest.raises(ValidationError):
        engine.schedule(PlanningProblem())


def test_engine_rejects_unknown_dependency():
    engine = SchedulingEngine(solver_adapter=FakeSolverAdapter())
    problem = PlanningProblem(
        operations=(Operation(identifier="op1", duration=1, depends_on=("ghost",)),)
    )

    with pytest.raises(ValidationError):
        engine.schedule(problem)
