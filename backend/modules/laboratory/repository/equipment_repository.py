"""Equipment repository.

Converts between the Equipment ORM model and the domain object. Does not manage
transactions.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.infrastructure.orm.laboratory.equipment_orm import EquipmentORM
from backend.infrastructure.orm.laboratory.project_orm import ProjectORM
from backend.infrastructure.orm.laboratory.workflow_definition_orm import (
    OperationDefinitionORM,
)
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

    def set_active(self, equipment_id: str, active: bool) -> bool:
        orm = self.session.get(EquipmentORM, equipment_id)
        if orm is None:
            return False
        orm.active = active
        return True

    def update(self, equipment: Equipment) -> bool:
        orm = self.session.get(EquipmentORM, equipment.id)
        if orm is None:
            return False
        orm.equipment_code = equipment.equipment_code
        orm.name = equipment.name
        orm.unavailable_dates = list(equipment.unavailable_dates)
        orm.fv_duration = equipment.fv_duration
        orm.fv_validity = equipment.fv_validity
        orm.projects = self._resolve_projects(equipment.applicable_project_ids)
        orm.methods = self._resolve_methods(equipment.method_ids)
        return True

    def delete(self, equipment_id: str) -> bool:
        orm = self.session.get(EquipmentORM, equipment_id)
        if orm is None:
            return False
        self.session.delete(orm)
        return True

    def set_unavailable_dates(self, equipment_id: str, dates: list) -> bool:
        orm = self.session.get(EquipmentORM, equipment_id)
        if orm is None:
            return False
        orm.unavailable_dates = list(dates)
        return True

    def _resolve_projects(self, ids):
        if not ids:
            return []
        return list(self.session.scalars(select(ProjectORM).where(ProjectORM.id.in_(ids))).all())

    def _resolve_methods(self, ids):
        if not ids:
            return []
        return list(
            self.session.scalars(
                select(OperationDefinitionORM).where(OperationDefinitionORM.id.in_(ids))
            ).all()
        )

    def _to_orm(self, equipment: Equipment) -> EquipmentORM:
        projects = []
        if equipment.applicable_project_ids:
            projects = list(
                self.session.scalars(
                    select(ProjectORM).where(ProjectORM.id.in_(equipment.applicable_project_ids))
                ).all()
            )
        methods = []
        if equipment.method_ids:
            methods = list(
                self.session.scalars(
                    select(OperationDefinitionORM).where(
                        OperationDefinitionORM.id.in_(equipment.method_ids)
                    )
                ).all()
            )
        return EquipmentORM(
            id=equipment.id,
            equipment_code=equipment.equipment_code,
            name=equipment.name,
            unavailable_dates=list(equipment.unavailable_dates),
            fv_duration=equipment.fv_duration,
            fv_validity=equipment.fv_validity,
            projects=projects,
            methods=methods,
            active=equipment.active,
        )

    @staticmethod
    def _to_domain(orm: EquipmentORM) -> Equipment:
        return Equipment(
            id=orm.id,
            equipment_code=orm.equipment_code,
            name=orm.name,
            unavailable_dates=list(orm.unavailable_dates or []),
            fv_duration=orm.fv_duration if orm.fv_duration is not None else 1,
            fv_validity=orm.fv_validity if orm.fv_validity is not None else 14,
            applicable_project_ids={p.id for p in orm.projects},
            method_ids={m.id for m in orm.methods},
            active=orm.active,
        )
