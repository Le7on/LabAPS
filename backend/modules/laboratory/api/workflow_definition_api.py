"""Laboratory REST API — Workflow Definitions.

Adapts HTTP requests to Workflow Definition use cases. No business logic.
Envelope responses (ADR-012).
"""

from __future__ import annotations

from flask import Blueprint, current_app, request

from backend.modules.laboratory.application.create_workflow_definition import (
    CreateWorkflowDefinitionUseCase,
    UpdateWorkflowDefinitionUseCase,
)
from backend.modules.laboratory.application.list_workflow_definitions import (
    DeleteWorkflowDefinitionUseCase,
    ListWorkflowDefinitionsUseCase,
)
from backend.modules.laboratory.dto.workflow_definition_dto import (
    CreateWorkflowDefinitionRequest,
)
from backend.shared import api_response
from backend.shared.errors import ValidationError

workflow_definition_bp = Blueprint("workflow_definition", __name__)


def _uow():
    return current_app.config["CONTAINER"].unit_of_work


@workflow_definition_bp.post("/workflow-definitions")
def create_workflow_definition():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValidationError("Request body must be a JSON object")

    use_case = CreateWorkflowDefinitionUseCase(_uow())
    result = use_case.execute(CreateWorkflowDefinitionRequest.from_json(data))
    return api_response.success(result, status=201)


@workflow_definition_bp.get("/workflow-definitions")
def list_workflow_definitions():
    use_case = ListWorkflowDefinitionsUseCase(_uow())
    result = use_case.execute()
    return api_response.collection(result["items"])


@workflow_definition_bp.put("/workflow-definitions/<workflow_id>")
def update_workflow_definition(workflow_id: str):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValidationError("Request body must be a JSON object")
    use_case = UpdateWorkflowDefinitionUseCase(_uow())
    return api_response.success(
        use_case.execute(workflow_id, CreateWorkflowDefinitionRequest.from_json(data))
    )


@workflow_definition_bp.delete("/workflow-definitions/<workflow_id>")
def delete_workflow_definition(workflow_id: str):
    use_case = DeleteWorkflowDefinitionUseCase(_uow())
    return api_response.success(use_case.execute(workflow_id))
