"""Scheduling Model Builder.

Transforms a validated Planning Problem into a Scheduling Model. Stateless engine
(Dependency Injection Strategy, section 7). Introduces optimization concepts;
does not solve.
"""

from __future__ import annotations

from backend.engines.planning.planning_problem import (
    EQUIPMENT,
    OBJECTIVE_WEIGHTED_COMPLETION,
    STAFF,
    PlanningProblem,
)
from backend.engines.scheduling.scheduling_model import (
    Objective,
    SchedulingModel,
    SchedulingResource,
    Task,
)


class SchedulingModelBuilder:
    def build(self, problem: PlanningProblem) -> SchedulingModel:
        tasks = tuple(
            Task(
                identifier=op.identifier,
                duration=op.duration,
                predecessors=op.depends_on,
                requirements=self._requirements(op),
                weight=op.weight,
            )
            for op in problem.operations
        )
        resources = tuple(
            SchedulingResource(
                identifier=r.identifier,
                kind=r.kind,
                provides=frozenset(r.provides),
                windows=tuple(r.windows),
                fv_duration=r.fv_duration,
                fv_validity=r.fv_validity,
            )
            for r in problem.resources
        )
        objective = (
            Objective.WEIGHTED_COMPLETION
            if problem.policies.objective == OBJECTIVE_WEIGHTED_COMPLETION
            else Objective.MAKESPAN
        )
        return SchedulingModel(
            tasks=tasks,
            resources=resources,
            horizon=problem.policies.planning_horizon,
            objective=objective,
            frozen_until=problem.policies.frozen_until,
        )

    @staticmethod
    def _requirements(op) -> frozenset[tuple[str, str]]:
        reqs: set[tuple[str, str]] = set()
        if op.required_capability is not None:
            reqs.add((EQUIPMENT, op.required_capability))
        if op.required_skill is not None:
            reqs.add((STAFF, op.required_skill))
        # A required qualification is another STAFF-kind requirement: the assigned
        # staff member must provide it (and it must be currently valid, resolved
        # when the resource's provided set is built).
        if op.required_qualification is not None:
            reqs.add((STAFF, op.required_qualification))
        return frozenset(reqs)
