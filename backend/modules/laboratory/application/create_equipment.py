"""Create Equipment use case."""

from __future__ import annotations

from backend.modules.laboratory.domain.entities.equipment import Equipment
from backend.modules.laboratory.dto.equipment_dto import (
    CreateEquipmentRequest,
    equipment_to_dict,
)
from backend.modules.laboratory.repository.equipment_repository import (
    EquipmentRepository,
)


class CreateEquipmentUseCase:
    def __init__(self, session_factory):
        self._session_factory = session_factory

    def execute(self, request: CreateEquipmentRequest) -> dict:
        equipment = Equipment(
            equipment_code=request.equipment_code,
            name=request.name,
            capabilities=request.capabilities,
        )

        session = self._session_factory()
        try:
            EquipmentRepository(session).add(equipment)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

        return equipment_to_dict(equipment)
