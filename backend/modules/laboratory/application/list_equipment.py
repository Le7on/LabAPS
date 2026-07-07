"""List Equipment use case (read operation)."""

from __future__ import annotations

from backend.modules.laboratory.dto.equipment_dto import equipment_to_dict


class ListEquipmentUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self) -> dict:
        with self._uow_factory() as uow:
            items = [equipment_to_dict(e) for e in uow.equipment.list()]

        return {"count": len(items), "items": items}
