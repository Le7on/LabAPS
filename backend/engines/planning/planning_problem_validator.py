"""Planning Problem validation.

A valid Planning Problem is required before Scheduling Model construction
(Planning Model, chapter 3, section 11). Stateless.
"""

from __future__ import annotations

from backend.engines.planning.planning_problem import PlanningProblem
from backend.shared.errors import ValidationError


class PlanningProblemValidator:
    def validate(self, problem: PlanningProblem) -> None:
        if not problem.operations:
            raise ValidationError("Planning problem has no operations to schedule")

        operation_ids = {op.identifier for op in problem.operations}

        for op in problem.operations:
            if op.duration <= 0:
                raise ValidationError(f"Operation {op.identifier} has non-positive duration")
            for dependency in op.depends_on:
                if dependency not in operation_ids:
                    raise ValidationError(
                        f"Operation {op.identifier} depends on unknown operation {dependency}"
                    )
