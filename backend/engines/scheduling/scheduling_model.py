"""Scheduling Model.

Optimization representation of a Planning Problem (Scheduling Model doc, ch.2).
Holds the Resource Graph, the Operation Graph (tasks + precedence) and the
horizon. Still framework-free: the Solver Adapter translates this into OR-Tools
Assignment/Start/End variables, not this module.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class SchedulingResource:
    """A schedulable resource in the Resource Graph (equipment or staff).

    Holds scheduling attributes only; business information has been removed.
    """

    identifier: str
    capabilities: frozenset[str] = frozenset()

    def can_perform(self, required_capability: str | None) -> bool:
        return required_capability is None or required_capability in self.capabilities


@dataclass(frozen=True, slots=True)
class Task:
    """A schedulable unit derived from a planning Operation."""

    identifier: str
    duration: int
    predecessors: tuple[str, ...] = ()
    required_capability: str | None = None


@dataclass(frozen=True, slots=True)
class SchedulingModel:
    """Optimization model: resources, tasks, precedence and the horizon."""

    tasks: tuple[Task, ...] = ()
    resources: tuple[SchedulingResource, ...] = ()
    horizon: int = 100

    def task_map(self) -> dict[str, Task]:
        return {task.identifier: task for task in self.tasks}

    def eligible_resources(self, task: Task) -> tuple[SchedulingResource, ...]:
        """Resources whose capability set satisfies the task (Capability Constraint)."""
        return tuple(r for r in self.resources if r.can_perform(task.required_capability))


@dataclass(frozen=True, slots=True)
class ScheduledTask:
    """A task placed on the timeline and assigned to a resource by the solver."""

    identifier: str
    start: int
    end: int
    resource_id: str | None = None


@dataclass(frozen=True, slots=True)
class SchedulingSolution:
    """Solver output: task placements and status (no Domain Objects)."""

    scheduled_tasks: tuple[ScheduledTask, ...] = ()
    makespan: int = 0
    status: str = "unknown"
    feasible: bool = False
    diagnostics: dict = field(default_factory=dict)
