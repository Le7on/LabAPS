"""Scheduling Model.

Optimization representation of a Planning Problem (Scheduling Model doc, ch.2).
Holds the Resource Graph, the Operation Graph (tasks + precedence) and the
horizon. Still framework-free: the Solver Adapter translates this into OR-Tools
Assignment/Start/End variables, not this module.

Resources have a ``kind`` (e.g. "equipment", "staff"). A task may require one
resource of each kind, matched by that kind's attribute set (equipment by
capability, staff by skill). When a task requires a kind, exactly one resource of
that kind is assigned and no two tasks share a resource in time.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

EQUIPMENT = "equipment"
STAFF = "staff"


class Objective(StrEnum):
    """Optimization goal (Objective Model, ADR-007).

    MAKESPAN: minimize the latest end time.
    WEIGHTED_COMPLETION: minimize sum(weight * end); higher-weight (higher demand
    priority) work is pulled earlier. Falls back to makespan behaviour when all
    weights are equal.
    """

    MAKESPAN = "makespan"
    WEIGHTED_COMPLETION = "weighted_completion"


@dataclass(frozen=True, slots=True)
class SchedulingResource:
    """A schedulable resource in the Resource Graph.

    ``provides`` is the resource's attribute set: capabilities for equipment,
    skills for staff. Holds scheduling attributes only.
    """

    identifier: str
    kind: str = EQUIPMENT
    provides: frozenset[str] = frozenset()

    def satisfies(self, requirement: str | None) -> bool:
        return requirement is None or requirement in self.provides


@dataclass(frozen=True, slots=True)
class Task:
    """A schedulable unit derived from a planning Operation.

    ``requirements`` maps a resource kind to the attribute it needs, e.g.
    ``{"equipment": "pcr", "staff": "pcr-operator"}``. A kind absent from the map
    is not required.
    """

    identifier: str
    duration: int
    predecessors: tuple[str, ...] = ()
    requirements: frozenset[tuple[str, str]] = frozenset()
    weight: int = 1

    def requirement_for(self, kind: str) -> str | None:
        for req_kind, value in self.requirements:
            if req_kind == kind:
                return value
        return None


@dataclass(frozen=True, slots=True)
class SchedulingModel:
    """Optimization model: resources, tasks, precedence and the horizon."""

    tasks: tuple[Task, ...] = ()
    resources: tuple[SchedulingResource, ...] = ()
    horizon: int = 100
    objective: Objective = Objective.MAKESPAN

    def task_map(self) -> dict[str, Task]:
        return {task.identifier: task for task in self.tasks}

    def kinds(self) -> tuple[str, ...]:
        """Distinct resource kinds present in the model, in stable order."""
        seen: list[str] = []
        for r in self.resources:
            if r.kind not in seen:
                seen.append(r.kind)
        return tuple(seen)

    def eligible_resources(self, task: Task, kind: str) -> tuple[SchedulingResource, ...]:
        """Resources of ``kind`` that satisfy the task's requirement for it."""
        requirement = task.requirement_for(kind)
        return tuple(r for r in self.resources if r.kind == kind and r.satisfies(requirement))


@dataclass(frozen=True, slots=True)
class ResourceAssignment:
    """A single resource assigned to a task, by kind."""

    kind: str
    resource_id: str


@dataclass(frozen=True, slots=True)
class ScheduledTask:
    """A task placed on the timeline and its resource assignments by the solver."""

    identifier: str
    start: int
    end: int
    assignments: tuple[ResourceAssignment, ...] = ()

    def resource_of(self, kind: str) -> str | None:
        for a in self.assignments:
            if a.kind == kind:
                return a.resource_id
        return None

    @property
    def resource_id(self) -> str | None:
        """Backward-compatible accessor: the equipment resource, if any."""
        return self.resource_of(EQUIPMENT) or (
            self.assignments[0].resource_id if self.assignments else None
        )


@dataclass(frozen=True, slots=True)
class SchedulingSolution:
    """Solver output: task placements and status (no Domain Objects)."""

    scheduled_tasks: tuple[ScheduledTask, ...] = ()
    makespan: int = 0
    status: str = "unknown"
    feasible: bool = False
    diagnostics: dict = field(default_factory=dict)
