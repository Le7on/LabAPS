"""Unit tests for assignment execution transitions (State Model, chapter 4)."""

from __future__ import annotations

import pytest

from backend.modules.execution.domain.assignment_status import (
    AssignmentStatus,
    next_status,
    require_reason,
)
from backend.shared.errors import ConflictError, ValidationError


def test_forward_transitions():
    assert next_status(AssignmentStatus.PENDING, "mark_ready") == AssignmentStatus.READY
    assert next_status(AssignmentStatus.READY, "start") == AssignmentStatus.RUNNING
    assert next_status(AssignmentStatus.RUNNING, "complete") == AssignmentStatus.COMPLETED
    assert next_status(AssignmentStatus.RUNNING, "fail") == AssignmentStatus.FAILED
    assert next_status(AssignmentStatus.READY, "cancel") == AssignmentStatus.CANCELLED


def test_cannot_start_pending():
    with pytest.raises(ConflictError):
        next_status(AssignmentStatus.PENDING, "start")


def test_cannot_complete_ready():
    with pytest.raises(ConflictError):
        next_status(AssignmentStatus.READY, "complete")


def test_terminal_states_reject_actions():
    for terminal in (
        AssignmentStatus.COMPLETED,
        AssignmentStatus.FAILED,
        AssignmentStatus.CANCELLED,
    ):
        with pytest.raises(ConflictError):
            next_status(terminal, "start")


def test_reason_required_for_fail_and_cancel():
    assert require_reason("fail", "instrument error") == "instrument error"
    with pytest.raises(ValidationError):
        require_reason("cancel", None)
