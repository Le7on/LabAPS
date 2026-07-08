"""KPI query service.

Read-only reporting metrics: assignment status breakdown and per-equipment
assignment load (a simple utilization proxy). Queries the ORM directly
(lightweight CQRS read model).
"""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.infrastructure.orm.laboratory.equipment_orm import EquipmentORM
from backend.infrastructure.orm.planning.assignment_orm import AssignmentORM


class KpiQueryService:
    def __init__(self, session: Session):
        self.session = session

    def assignment_status_breakdown(self) -> dict[str, int]:
        stmt = select(AssignmentORM.status, func.count()).group_by(AssignmentORM.status)
        return {status: int(count) for status, count in self.session.execute(stmt).all()}

    def equipment_utilization(self) -> list[dict]:
        """Per-equipment assignment count and total planned busy time.

        Busy time is the sum of (planned_end - planned_start) across the
        equipment's assignments; a coarse utilization proxy until a calendar
        model provides capacity.
        """
        duration = AssignmentORM.planned_end - AssignmentORM.planned_start
        stmt = (
            select(
                EquipmentORM.id,
                EquipmentORM.equipment_code,
                EquipmentORM.name,
                func.count(AssignmentORM.id),
                func.coalesce(func.sum(duration), 0),
            )
            .outerjoin(AssignmentORM, AssignmentORM.equipment_id == EquipmentORM.id)
            .group_by(EquipmentORM.id, EquipmentORM.equipment_code, EquipmentORM.name)
            .order_by(EquipmentORM.equipment_code)
        )
        return [
            {
                "equipmentId": eid,
                "equipmentCode": code,
                "name": name,
                "assignmentCount": int(count),
                "busyTime": int(busy),
            }
            for eid, code, name, count, busy in self.session.execute(stmt).all()
        ]

    def summary(self) -> dict:
        return {
            "assignmentStatus": self.assignment_status_breakdown(),
            "equipmentUtilization": self.equipment_utilization(),
        }
