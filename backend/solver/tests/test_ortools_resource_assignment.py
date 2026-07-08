"""OR-Tools resource-assignment tests (real CP-SAT).

Covers the Capability, Skill, Resource (no-overlap) and cardinality constraints.
Skipped automatically if OR-Tools is not installed.
"""

from __future__ import annotations

import pytest

pytest.importorskip("ortools")

from backend.engines.scheduling.scheduling_model import (
    EQUIPMENT,
    STAFF,
    SchedulingModel,
    SchedulingResource,
    Task,
)
from backend.solver.adapter.ortools_solver_adapter import ORToolsSolverAdapter


def _solve(model):
    return ORToolsSolverAdapter(max_time_in_seconds=5).solve(model)


def _equip(id_, *caps):
    return SchedulingResource(identifier=id_, kind=EQUIPMENT, provides=frozenset(caps))


def _staff(id_, *skills):
    return SchedulingResource(identifier=id_, kind=STAFF, provides=frozenset(skills))


def test_task_assigned_only_to_capable_equipment():
    model = SchedulingModel(
        tasks=(Task(identifier="t1", duration=2, requirements=frozenset({(EQUIPMENT, "pcr")})),),
        resources=(_equip("eqA", "spin"), _equip("eqB", "pcr")),
        horizon=50,
    )

    solution = _solve(model)

    assert solution.feasible
    assert solution.scheduled_tasks[0].resource_of(EQUIPMENT) == "eqB"


def test_task_requires_equipment_and_staff():
    model = SchedulingModel(
        tasks=(
            Task(
                identifier="t1",
                duration=2,
                requirements=frozenset({(EQUIPMENT, "pcr"), (STAFF, "pcr-op")}),
            ),
        ),
        resources=(_equip("eqB", "pcr"), _staff("stA", "pcr-op"), _staff("stB", "spin-op")),
        horizon=50,
    )

    solution = _solve(model)

    assert solution.feasible
    placed = solution.scheduled_tasks[0]
    assert placed.resource_of(EQUIPMENT) == "eqB"
    assert placed.resource_of(STAFF) == "stA"


def test_single_resource_serializes_two_tasks():
    model = SchedulingModel(
        tasks=(
            Task(identifier="t1", duration=3, requirements=frozenset({(EQUIPMENT, "pcr")})),
            Task(identifier="t2", duration=4, requirements=frozenset({(EQUIPMENT, "pcr")})),
        ),
        resources=(_equip("eqB", "pcr"),),
        horizon=50,
    )

    solution = _solve(model)

    assert solution.feasible
    assert solution.makespan == 7  # forced sequential on one resource


def test_two_resources_run_tasks_in_parallel():
    model = SchedulingModel(
        tasks=(
            Task(identifier="t1", duration=3, requirements=frozenset({(EQUIPMENT, "pcr")})),
            Task(identifier="t2", duration=4, requirements=frozenset({(EQUIPMENT, "pcr")})),
        ),
        resources=(_equip("eq1", "pcr"), _equip("eq2", "pcr")),
        horizon=50,
    )

    solution = _solve(model)

    assert solution.feasible
    assert solution.makespan == 4  # parallel: max(3, 4)


def test_no_capable_resource_is_infeasible():
    model = SchedulingModel(
        tasks=(
            Task(identifier="t1", duration=2, requirements=frozenset({(EQUIPMENT, "mass-spec")})),
        ),
        resources=(_equip("eqA", "spin"),),
        horizon=50,
    )

    solution = _solve(model)

    assert not solution.feasible
    assert solution.status == "infeasible"
