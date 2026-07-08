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
