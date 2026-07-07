"""List Equipment use case (read operation)."""

from __future__ import annotations

from backend.modules.laboratory.dto.equipment_dto import equipment_to_dict
from backend.modules.laboratory.repository.equipment_repository import (
    EquipmentRepository,
)


class ListEquipmentUseCase:
    def __init__(self, session_factory):
        self._session_factory = session_factory

    def execute(self) -> dict:
        session = self._session_factory()
        try:
            items = [equipment_to_dict(e) for e in EquipmentRepository(session).list()]
        finally:
            session.close()

        return {"count": len(items), "items": items}
