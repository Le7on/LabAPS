"""Engine-level resource assignment tests (via FakeSolverAdapter)."""

from __future__ import annotations

from backend.engines.planning.planning_problem import (
    Operation,
    PlanningProblem,
    Resource,
)
from backend.engines.scheduling.scheduling_engine import SchedulingEngine
from backend.engines.tests.fakes import FakeSolverAdapter


def test_engine_assigns_capable_resource():
    engine = SchedulingEngine(solver_adapter=FakeSolverAdapter())
    problem = PlanningProblem(
        operations=(Operation(identifier="op1", duration=2, required_capability="pcr"),),
        resources=(
            Resource(identifier="eqA", capabilities=frozenset({"spin"})),
            Resource(identifier="eqB", capabilities=frozenset({"pcr"})),
        ),
    )

    result = engine.schedule(problem)

    assert result.feasible
    assert result.assignments[0].resource_id == "eqB"


def test_engine_infeasible_when_no_capable_resource():
    engine = SchedulingEngine(solver_adapter=FakeSolverAdapter())
    problem = PlanningProblem(
        operations=(Operation(identifier="op1", duration=2, required_capability="mass-spec"),),
        resources=(Resource(identifier="eqA", capabilities=frozenset({"spin"})),),
    )

    result = engine.schedule(problem)

    assert not result.feasible
    assert result.assignments == ()
