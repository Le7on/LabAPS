"""OR-Tools resource-assignment tests (real CP-SAT).

Covers the Capability, Resource (no-overlap) and cardinality constraints added to
the solver. Skipped automatically if OR-Tools is not installed.
"""

from __future__ import annotations

import pytest

pytest.importorskip("ortools")

from backend.engines.scheduling.scheduling_model import (
    SchedulingModel,
    SchedulingResource,
    Task,
)
from backend.solver.adapter.ortools_solver_adapter import ORToolsSolverAdapter


def _solve(model):
    return ORToolsSolverAdapter(max_time_in_seconds=5).solve(model)


def test_task_assigned_only_to_capable_resource():
    model = SchedulingModel(
        tasks=(Task(identifier="t1", duration=2, required_capability="pcr"),),
        resources=(
            SchedulingResource(identifier="eqA", capabilities=frozenset({"spin"})),
            SchedulingResource(identifier="eqB", capabilities=frozenset({"pcr"})),
        ),
        horizon=50,
    )

    solution = _solve(model)

    assert solution.feasible
    placement = solution.scheduled_tasks[0]
    assert placement.resource_id == "eqB"  # only eqB has the required capability


def test_single_resource_serializes_two_tasks():
    # Both tasks need the same sole capable resource -> they cannot overlap.
    model = SchedulingModel(
        tasks=(
            Task(identifier="t1", duration=3, required_capability="pcr"),
            Task(identifier="t2", duration=4, required_capability="pcr"),
        ),
        resources=(SchedulingResource(identifier="eqB", capabilities=frozenset({"pcr"})),),
        horizon=50,
    )

    solution = _solve(model)

    assert solution.feasible
    assert solution.makespan == 7  # 3 + 4 forced sequential on one resource
    for t in solution.scheduled_tasks:
        assert t.resource_id == "eqB"


def test_two_resources_run_tasks_in_parallel():
    model = SchedulingModel(
        tasks=(
            Task(identifier="t1", duration=3, required_capability="pcr"),
            Task(identifier="t2", duration=4, required_capability="pcr"),
        ),
        resources=(
            SchedulingResource(identifier="eq1", capabilities=frozenset({"pcr"})),
            SchedulingResource(identifier="eq2", capabilities=frozenset({"pcr"})),
        ),
        horizon=50,
    )

    solution = _solve(model)

    assert solution.feasible
    # With two capable resources the tasks run in parallel: makespan = max(3, 4).
    assert solution.makespan == 4
    assigned = {t.resource_id for t in solution.scheduled_tasks}
    assert assigned == {"eq1", "eq2"}


def test_no_capable_resource_is_infeasible():
    model = SchedulingModel(
        tasks=(Task(identifier="t1", duration=2, required_capability="mass-spec"),),
        resources=(SchedulingResource(identifier="eqA", capabilities=frozenset({"spin"})),),
        horizon=50,
    )

    solution = _solve(model)

    assert not solution.feasible
    assert solution.status == "infeasible"
