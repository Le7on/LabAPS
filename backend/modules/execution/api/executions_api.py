"""Execution REST API — Assignment execution.

Transitions an assignment's execution status. Envelope responses (ADR-012);
invalid transitions surface as 409 from the domain.
"""

from __future__ import annotations

from flask import Blueprint, current_app, request

from backend.modules.execution.application.execute_assignment import (
    CancelAssignmentUseCase,
    CompleteAssignmentUseCase,
    FailAssignmentUseCase,
    StartAssignmentUseCase,
)
from backend.modules.execution.application.list_execution_history import (
    ListExecutionHistoryUseCase,
)
from backend.shared import api_response

executions_bp = Blueprint("executions", __name__)


def _uow():
    return current_app.config["CONTAINER"].unit_of_work


def _reason() -> str | None:
    data = request.get_json(silent=True)
    return data.get("reason") if isinstance(data, dict) else None


@executions_bp.post("/executions/<assignment_id>/start")
def start_assignment(assignment_id: str):
    return api_response.success(StartAssignmentUseCase(_uow()).execute(assignment_id))


@executions_bp.post("/executions/<assignment_id>/complete")
def complete_assignment(assignment_id: str):
    return api_response.success(CompleteAssignmentUseCase(_uow()).execute(assignment_id))


@executions_bp.post("/executions/<assignment_id>/fail")
def fail_assignment(assignment_id: str):
    return api_response.success(FailAssignmentUseCase(_uow()).execute(assignment_id, _reason()))


@executions_bp.post("/executions/<assignment_id>/cancel")
def cancel_assignment(assignment_id: str):
    return api_response.success(CancelAssignmentUseCase(_uow()).execute(assignment_id, _reason()))


@executions_bp.get("/executions/<assignment_id>/history")
def execution_history(assignment_id: str):
    result = ListExecutionHistoryUseCase(_uow()).execute(assignment_id)
    return api_response.collection(result["items"])
