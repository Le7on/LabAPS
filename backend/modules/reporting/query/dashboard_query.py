"""Dashboard query service.

Reporting is read-only (Engineering Baseline). Read models query the ORM directly
rather than loading aggregates through repositories, avoiding the domain-mapping
cost where no business behaviour is needed (lightweight CQRS: Repository for
writes, Query Service for reads).
"""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.infrastructure.orm.laboratory.equipment_orm import EquipmentORM
from backend.infrastructure.orm.laboratory.staff_orm import StaffORM
from backend.infrastructure.orm.laboratory.workflow_definition_orm import (
    WorkflowDefinitionORM,
)
from backend.infrastructure.orm.planning.plan_orm import PlanORM, PlanVersionORM


class DashboardQueryService:
    def __init__(self, session: Session):
        self.session = session

    def _count(self, model, *where) -> int:
        stmt = select(func.count()).select_from(model)
        for clause in where:
            stmt = stmt.where(clause)
        return int(self.session.scalar(stmt) or 0)

    def summary(self) -> dict:
        return {
            "plans": self._count(PlanORM),
            "planVersions": self._count(PlanVersionORM),
            "publishedVersions": self._count(PlanVersionORM, PlanVersionORM.status == "published"),
            "equipment": self._count(EquipmentORM),
            "activeEquipment": self._count(EquipmentORM, EquipmentORM.active.is_(True)),
            "staff": self._count(StaffORM),
            "workflowDefinitions": self._count(WorkflowDefinitionORM),
        }
