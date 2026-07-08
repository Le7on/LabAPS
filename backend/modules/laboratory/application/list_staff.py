"""List Staff use case (read operation)."""

from __future__ import annotations

from backend.modules.laboratory.dto.staff_dto import staff_to_dict


class ListStaffUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self) -> dict:
        with self._uow_factory() as uow:
            items = [staff_to_dict(s) for s in uow.staff.list()]

        return {"count": len(items), "items": items}
