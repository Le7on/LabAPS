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
    # Availability windows [start, end); empty means always available (Calendar
    # Constraint). A task assigned to this resource must fit within one window.
    windows: tuple[tuple[int, int], ...] = ()
    # FV validity (ADR-019): fv_validity > 0 means this equipment must be
    # validated periodically. An FV occupies the machine for fv_duration and is
    # placed every fv_validity units; normal work can only occupy the tiled gaps,
    # which keeps every operation within a valid FV window. 0 = no FV needed.
    fv_duration: int = 0
    fv_validity: int = 0

    def satisfies(self, requirement: str | None) -> bool:
        return requirement is None or requirement in self.provides

    def satisfies_all(self, requirements: frozenset[str]) -> bool:
        return requirements.issubset(self.provides)

    def fv_intervals(self, horizon: int) -> tuple[tuple[int, int], ...]:
        """Fixed FV occupancy intervals [start, end) tiling the horizon (ADR-019).

        An FV runs at the start of each validity period. Placing an FV of length
        ``fv_duration`` at the start of every ``fv_validity`` window means the
        machine's usable (non-FV) time always sits within a valid window, so a
        normal task that avoids these intervals is necessarily in validity.
        """
        if self.fv_validity <= 0 or self.fv_duration <= 0:
            return ()
        intervals = []
        start = 0
        while start < horizon:
            intervals.append((start, min(start + self.fv_duration, horizon)))
            start += self.fv_validity
        return tuple(intervals)


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
    # Optional hard time window [start, end) the task must fit within (in slot
    # units). Used to pin a PI demand line's rounds to their target day (ADR-020).
    window: tuple[int, int] | None = None

    def requirement_for(self, kind: str) -> str | None:
        for req_kind, value in self.requirements:
            if req_kind == kind:
                return value
        return None

    def requirements_for(self, kind: str) -> frozenset[str]:
        """All attribute values a resource of ``kind`` must provide for this task."""
        return frozenset(value for req_kind, value in self.requirements if req_kind == kind)

    def requires(self, kind: str) -> bool:
        return any(req_kind == kind for req_kind, _ in self.requirements)


@dataclass(frozen=True, slots=True)
class SchedulingModel:
    """Optimization model: resources, tasks, precedence and the horizon."""

    tasks: tuple[Task, ...] = ()
    resources: tuple[SchedulingResource, ...] = ()
    horizon: int = 100
    objective: Objective = Objective.MAKESPAN
    # Policy Constraint: no task may start before this frozen boundary (the
    # frozen planning window is locked). 0 means no frozen window.
    frozen_until: int = 0

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
        """Resources of ``kind`` that satisfy all of the task's requirements for it.

        A staff task may require both a skill and a qualification; a resource is
        eligible only if it provides every required value.
        """
        required = task.requirements_for(kind)
        return tuple(r for r in self.resources if r.kind == kind and r.satisfies_all(required))


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
    is_fv: bool = False

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
