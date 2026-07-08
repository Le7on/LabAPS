"""Engine-level resource assignment tests (via FakeSolverAdapter)."""

from __future__ import annotations

from backend.engines.planning.planning_problem import (
    EQUIPMENT,
    STAFF,
    Operation,
    PlanningProblem,
    Resource,
)
from backend.engines.scheduling.scheduling_engine import SchedulingEngine
from backend.engines.tests.fakes import FakeSolverAdapter


def test_engine_assigns_capable_equipment():
    engine = SchedulingEngine(solver_adapter=FakeSolverAdapter())
    problem = PlanningProblem(
        operations=(Operation(identifier="op1", duration=2, required_capability="pcr"),),
        resources=(
            Resource(identifier="eqA", kind=EQUIPMENT, provides=frozenset({"spin"})),
            Resource(identifier="eqB", kind=EQUIPMENT, provides=frozenset({"pcr"})),
        ),
    )

    result = engine.schedule(problem)

    assert result.feasible
    assert result.assignments[0].equipment_id == "eqB"


def test_engine_assigns_equipment_and_staff():
    engine = SchedulingEngine(solver_adapter=FakeSolverAdapter())
    problem = PlanningProblem(
        operations=(
            Operation(
                identifier="op1",
                duration=2,
                required_capability="pcr",
                required_skill="pcr-operator",
            ),
        ),
        resources=(
            Resource(identifier="eqB", kind=EQUIPMENT, provides=frozenset({"pcr"})),
            Resource(identifier="stA", kind=STAFF, provides=frozenset({"pcr-operator"})),
        ),
    )

    result = engine.schedule(problem)

    assert result.feasible
    assignment = result.assignments[0]
    assert assignment.equipment_id == "eqB"
    assert assignment.staff_id == "stA"


def test_engine_infeasible_when_no_capable_resource():
    engine = SchedulingEngine(solver_adapter=FakeSolverAdapter())
    problem = PlanningProblem(
        operations=(Operation(identifier="op1", duration=2, required_capability="mass-spec"),),
        resources=(Resource(identifier="eqA", kind=EQUIPMENT, provides=frozenset({"spin"})),),
    )

    result = engine.schedule(problem)

    assert not result.feasible
    assert result.assignments == ()
