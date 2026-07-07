"""Scheduling Model.

Optimization representation of a Planning Problem. Introduces the concepts the
Planning Problem deliberately omits: schedulable tasks with durations and
precedence, and a horizon. Still framework-free: the Solver Adapter translates
this into OR-Tools variables, not this module.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Task:
    """A schedulable unit derived from a planning Operation."""

    identifier: str
    duration: int
    predecessors: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class SchedulingModel:
    """Optimization model: tasks, precedence and the scheduling horizon."""

    tasks: tuple[Task, ...] = ()
    horizon: int = 100

    def task_map(self) -> dict[str, Task]:
        return {task.identifier: task for task in self.tasks}


@dataclass(frozen=True, slots=True)
class ScheduledTask:
    """A task placed on the timeline by the solver."""

    identifier: str
    start: int
    end: int


@dataclass(frozen=True, slots=True)
class SchedulingSolution:
    """Solver output: task placements and status."""

    scheduled_tasks: tuple[ScheduledTask, ...] = ()
    makespan: int = 0
    status: str = "unknown"
    feasible: bool = False
    diagnostics: dict = field(default_factory=dict)
