"""Create Workflow Definition use case (one Unit of Work)."""

from __future__ import annotations

from backend.modules.laboratory.domain.aggregates.workflow_definition import (
    WorkflowDefinition,
)
from backend.modules.laboratory.dto.workflow_definition_dto import (
    CreateWorkflowDefinitionRequest,
    workflow_definition_to_dict,
)
from backend.shared.errors import NotFoundError, ValidationError


def _build_workflow(request, workflow_id=None):
    kwargs = {
        "workflow_code": request.workflow_code,
        "name": request.name,
        "project_id": request.project_id,
    }
    if workflow_id is not None:
        kwargs["id"] = workflow_id
    workflow = WorkflowDefinition(**kwargs)
    # Dependencies are expressed by method (operation) type within the workflow;
    # they are resolved to instance ids at generation time.
    for op in request.operations:
        workflow.add_operation(
            operation_type=op.operation_type,
            duration=op.duration,
            gelatin_type=op.gelatin_type,
            equipment_ids=op.equipment_ids,
            depends_on=op.depends_on,
        )
    return workflow


def _validate_refs(uow, request):
    if uow.projects.get(request.project_id) is None:
        raise ValidationError(f"Unknown project: {request.project_id}")
    for op in request.operations:
        for eid in op.equipment_ids:
            if uow.equipment.get(eid) is None:
                raise ValidationError(f"Unknown equipment: {eid}")


class CreateWorkflowDefinitionUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self, request: CreateWorkflowDefinitionRequest) -> dict:
        workflow = _build_workflow(request)
        with self._uow_factory() as uow:
            _validate_refs(uow, request)
            uow.workflow_definitions.add(workflow)
        return workflow_definition_to_dict(workflow)


class UpdateWorkflowDefinitionUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self, workflow_id: str, request: CreateWorkflowDefinitionRequest) -> dict:
        workflow = _build_workflow(request, workflow_id=workflow_id)
        with self._uow_factory() as uow:
            _validate_refs(uow, request)
            if not uow.workflow_definitions.update(workflow):
                raise NotFoundError(f"Workflow {workflow_id} not found")
            # Re-read so the response reflects persisted method ids (unchanged
            # methods keep their ids; the in-memory aggregate had fresh ones).
            saved = uow.workflow_definitions.get(workflow_id)
        return workflow_definition_to_dict(saved)
