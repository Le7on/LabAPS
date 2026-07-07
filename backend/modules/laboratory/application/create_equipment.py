"""Create Equipment use case (one Unit of Work)."""

from __future__ import annotations

from backend.modules.laboratory.domain.entities.equipment import Equipment
from backend.modules.laboratory.dto.equipment_dto import (
    CreateEquipmentRequest,
    equipment_to_dict,
)


class CreateEquipmentUseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self, request: CreateEquipmentRequest) -> dict:
        equipment = Equipment(
            equipment_code=request.equipment_code,
            name=request.name,
            capabilities=request.capabilities,
        )

        with self._uow_factory() as uow:
            uow.equipment.add(equipment)

        return equipment_to_dict(equipment)
