"""Assignment Builder.

Reconstructs Assignments from a SchedulingSolution after solving. Assignments are
the planning-domain result of scheduling; they are rebuilt here rather than being
carried through the solver (Solver Model architecture).
"""

from __future__ import annotations

from dataclasses import dataclass

from backend.engines.scheduling.scheduling_model import (
    EQUIPMENT,
    STAFF,
    SchedulingModel,
    SchedulingSolution,
)


@dataclass(frozen=True, slots=True)
class Assignment:
    """A scheduled operation placement (framework-free result object).

    ``resource_id`` is the equipment (kept for backward compatibility);
    ``equipment_id`` and ``staff_id`` expose the per-kind assignments.
    """

    operation_id: str
    start: int
    end: int
    resource_id: str | None = None
    equipment_id: str | None = None
    staff_id: str | None = None


class AssignmentBuilder:
    def build(self, solution: SchedulingSolution, model: SchedulingModel) -> tuple[Assignment, ...]:
        if not solution.feasible:
            return ()

        known = model.task_map()
        assignments = []
        for scheduled in solution.scheduled_tasks:
            if scheduled.identifier not in known:
                continue
            equipment_id = scheduled.resource_of(EQUIPMENT)
            staff_id = scheduled.resource_of(STAFF)
            assignments.append(
                Assignment(
                    operation_id=scheduled.identifier,
                    start=scheduled.start,
                    end=scheduled.end,
                    resource_id=equipment_id or scheduled.resource_id,
                    equipment_id=equipment_id,
                    staff_id=staff_id,
                )
            )
        return tuple(assignments)
