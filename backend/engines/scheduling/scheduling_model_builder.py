"""Scheduling Model Builder.

Transforms a validated Planning Problem into a Scheduling Model. Stateless engine
(Dependency Injection Strategy, section 7). Introduces optimization concepts;
does not solve.
"""

from __future__ import annotations

from backend.engines.planning.planning_problem import PlanningProblem
from backend.engines.scheduling.scheduling_model import SchedulingModel, Task


class SchedulingModelBuilder:
    def build(self, problem: PlanningProblem) -> SchedulingModel:
        tasks = tuple(
            Task(
                identifier=op.identifier,
                duration=op.duration,
                predecessors=op.depends_on,
            )
            for op in problem.operations
        )
        return SchedulingModel(tasks=tasks, horizon=problem.policies.planning_horizon)
