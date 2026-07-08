"""Assignment execution use cases.

Transition an assignment's execution status (start/complete/fail/cancel). The
domain transition rules (State Model chapter 4) are enforced by
``assignment_status.next_status``; each action is one transaction.
"""

from __future__ import annotations

from backend.modules.execution.domain.assignment_status import (
    AssignmentStatus,
    next_status,
    require_reason,
)
from backend.shared.errors import NotFoundError


class _AssignmentActionUseCase:
    _action = ""
    _needs_reason = False

    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self, assignment_id: str, reason: str | None = None) -> dict:
        with self._uow_factory() as uow:
            orm = uow.assignments.get(assignment_id)
            if orm is None:
                raise NotFoundError(f"Assignment {assignment_id} not found")

            target = next_status(AssignmentStatus(orm.status), self._action)
            orm.status = target.value
            if self._needs_reason:
                orm.reason = require_reason(self._action, reason)

            result = uow.assignments.to_dict(orm)

        return result


class StartAssignmentUseCase(_AssignmentActionUseCase):
    _action = "start"


class CompleteAssignmentUseCase(_AssignmentActionUseCase):
    _action = "complete"


class FailAssignmentUseCase(_AssignmentActionUseCase):
    _action = "fail"
    _needs_reason = True


class CancelAssignmentUseCase(_AssignmentActionUseCase):
    _action = "cancel"
    _needs_reason = True
