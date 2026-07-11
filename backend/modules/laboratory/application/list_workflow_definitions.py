"""List Workflow Definitions use case (read operation)."""

from __future__ import annotations

from backend.modules.laboratory.dto.workflow_definition_dto import (
    workflow_definition_to_dict,
)


class ListWorkflowDefinitionsUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self) -> dict:
        with self._uow_factory() as uow:
            items = [workflow_definition_to_dict(w) for w in uow.workflow_definitions.list()]

        return {"count": len(items), "items": items}


class DeleteWorkflowDefinitionUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self, workflow_id: str) -> dict:
        from backend.shared.errors import NotFoundError

        with self._uow_factory() as uow:
            if not uow.workflow_definitions.delete(workflow_id):
                raise NotFoundError(f"Workflow {workflow_id} not found")
        return {"id": workflow_id, "deleted": True}
