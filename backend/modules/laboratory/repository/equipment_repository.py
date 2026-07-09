"""Equipment repository.

Converts between the Equipment ORM model and the domain object. Does not manage
transactions.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.infrastructure.orm.laboratory.equipment_orm import EquipmentORM
from backend.modules.laboratory.domain.entities.equipment import Equipment


class EquipmentRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, equipment: Equipment) -> None:
        self.session.add(self._to_orm(equipment))

    def get(self, equipment_id: str) -> Equipment | None:
        orm = self.session.get(EquipmentORM, equipment_id)
        return self._to_domain(orm) if orm else None

    def list(self) -> list[Equipment]:
        stmt = select(EquipmentORM).order_by(EquipmentORM.created_at)
        return [self._to_domain(o) for o in self.session.scalars(stmt).all()]

    @staticmethod
    def _to_orm(equipment: Equipment) -> EquipmentORM:
        return EquipmentORM(
            id=equipment.id,
            equipment_code=equipment.equipment_code,
            name=equipment.name,
            capabilities=sorted(equipment.capabilities),
            availability=[list(w) for w in equipment.availability],
            active=equipment.active,
        )

    @staticmethod
    def _to_domain(orm: EquipmentORM) -> Equipment:
        return Equipment(
            id=orm.id,
            equipment_code=orm.equipment_code,
            name=orm.name,
            capabilities=set(orm.capabilities or []),
            availability=[tuple(w) for w in (orm.availability or [])],
            active=orm.active,
        )
