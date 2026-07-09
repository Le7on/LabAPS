"""Create Workflow Definition use case (one Unit of Work)."""

from __future__ import annotations

from backend.modules.laboratory.domain.aggregates.workflow_definition import (
    WorkflowDefinition,
)
from backend.modules.laboratory.dto.workflow_definition_dto import (
    CreateWorkflowDefinitionRequest,
    workflow_definition_to_dict,
)


class CreateWorkflowDefinitionUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self, request: CreateWorkflowDefinitionRequest) -> dict:
        workflow = WorkflowDefinition(
            workflow_code=request.workflow_code,
            name=request.name,
        )
        for op in request.operations:
            workflow.add_operation(
                operation_type=op.operation_type,
                duration=op.duration,
                required_capability=op.required_capability,
                required_skill=op.required_skill,
                required_qualification=op.required_qualification,
                depends_on=op.depends_on,
            )

        with self._uow_factory() as uow:
            uow.workflow_definitions.add(workflow)

        return workflow_definition_to_dict(workflow)
