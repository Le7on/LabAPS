"""Assignment Builder.

Reconstructs Assignments from a SchedulingSolution after solving. Assignments are
the planning-domain result of scheduling; they are rebuilt here rather than being
carried through the solver (Solver Model architecture).
"""

from __future__ import annotations

from dataclasses import dataclass

from backend.engines.scheduling.scheduling_model import SchedulingModel, SchedulingSolution


@dataclass(frozen=True, slots=True)
class Assignment:
    """A scheduled operation placement (framework-free result object)."""

    operation_id: str
    start: int
    end: int
    resource_id: str | None = None


class AssignmentBuilder:
    def build(self, solution: SchedulingSolution, model: SchedulingModel) -> tuple[Assignment, ...]:
        if not solution.feasible:
            return ()

        known = model.task_map()
        return tuple(
            Assignment(
                operation_id=scheduled.identifier,
                start=scheduled.start,
                end=scheduled.end,
                resource_id=scheduled.resource_id,
            )
            for scheduled in solution.scheduled_tasks
            if scheduled.identifier in known
        )
