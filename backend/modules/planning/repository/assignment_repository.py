"""Assignment repository.

Persists scheduling results for a Plan Version. Replacing a version's
assignments (delete-then-insert) reflects a fresh scheduling run. Does not manage
transactions.
"""

from __future__ import annotations

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from backend.infrastructure.orm.planning.assignment_orm import AssignmentORM


class AssignmentRepository:
    def __init__(self, session: Session):
        self.session = session

    def replace_for_version(self, plan_version_id: str, assignments: list[dict]) -> None:
        """Replace all assignments for a plan version with a new set."""
        self.session.execute(
            delete(AssignmentORM).where(AssignmentORM.plan_version_id == plan_version_id)
        )
        for a in assignments:
            self.session.add(
                AssignmentORM(
                    plan_version_id=plan_version_id,
                    operation_id=a["operationId"],
                    equipment_id=a.get("equipmentId"),
                    staff_id=a.get("staffId"),
                    planned_start=a["start"],
                    planned_end=a["end"],
                    status="planned",
                )
            )

    def list_for_version(self, plan_version_id: str) -> list[dict]:
        stmt = (
            select(AssignmentORM)
            .where(AssignmentORM.plan_version_id == plan_version_id)
            .order_by(AssignmentORM.planned_start)
        )
        return [
            {
                "operationId": a.operation_id,
                "equipmentId": a.equipment_id,
                "staffId": a.staff_id,
                "start": a.planned_start,
                "end": a.planned_end,
                "status": a.status,
            }
            for a in self.session.scalars(stmt).all()
        ]
