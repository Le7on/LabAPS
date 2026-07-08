"""List Execution History use case (read-only audit trail for an assignment)."""

from __future__ import annotations


class ListExecutionHistoryUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self, assignment_id: str) -> dict:
        with self._uow_factory() as uow:
            items = uow.execution_records.list_for_assignment(assignment_id)

        return {"count": len(items), "items": items}
