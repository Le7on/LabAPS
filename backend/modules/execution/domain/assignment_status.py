"""Assignment execution status and transition rules (State Model, chapter 4).

Lifecycle: Pending -> Ready -> Running -> Completed | Failed | Cancelled.
Backward transitions are prohibited; Completed/Failed/Cancelled are terminal.
"""

from __future__ import annotations

from enum import StrEnum

from backend.shared.errors import ConflictError, ValidationError


class AssignmentStatus(StrEnum):
    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


# Allowed transitions: current -> {actions}. Encodes the transition table.
_TRANSITIONS: dict[AssignmentStatus, dict[str, AssignmentStatus]] = {
    AssignmentStatus.PENDING: {"mark_ready": AssignmentStatus.READY},
    AssignmentStatus.READY: {
        "start": AssignmentStatus.RUNNING,
        "cancel": AssignmentStatus.CANCELLED,
    },
    AssignmentStatus.RUNNING: {
        "complete": AssignmentStatus.COMPLETED,
        "fail": AssignmentStatus.FAILED,
    },
}


def next_status(current: AssignmentStatus, action: str) -> AssignmentStatus:
    """Return the target status for an action, or raise on an invalid transition."""
    allowed = _TRANSITIONS.get(current, {})
    if action not in allowed:
        raise ConflictError(
            f"Cannot {action} an assignment in state {current.value}",
            details=[{"code": "INVALID_ASSIGNMENT_STATE"}],
        )
    return allowed[action]


def require_reason(action: str, reason: str | None) -> str:
    """Fail and cancel require a reason (BR-AS-005 / BR-AS-006)."""
    if not reason:
        raise ValidationError(f"A reason is required to {action} an assignment")
    return reason
