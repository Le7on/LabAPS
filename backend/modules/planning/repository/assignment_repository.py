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
                    planned_start_at=a.get("startAt"),
                    planned_end_at=a.get("endAt"),
                    planned_shift=a.get("shift"),
                    status="pending",
                )
            )

    def mark_version_ready(self, plan_version_id: str) -> None:
        """Move all Pending assignments of a version to Ready (BR-AS-002)."""
        stmt = select(AssignmentORM).where(
            AssignmentORM.plan_version_id == plan_version_id,
            AssignmentORM.status == "pending",
        )
        for orm in self.session.scalars(stmt).all():
            orm.status = "ready"

    def list_for_version(self, plan_version_id: str) -> list[dict]:
        stmt = (
            select(AssignmentORM)
            .where(AssignmentORM.plan_version_id == plan_version_id)
            .order_by(AssignmentORM.planned_start)
        )
        return [self._to_dict(a) for a in self.session.scalars(stmt).all()]

    def get(self, assignment_id: str) -> AssignmentORM | None:
        return self.session.get(AssignmentORM, assignment_id)

    def to_dict(self, orm: AssignmentORM) -> dict:
        return self._to_dict(orm)

    @staticmethod
    def _to_dict(a: AssignmentORM) -> dict:
        return {
            "id": a.id,
            "operationId": a.operation_id,
            "equipmentId": a.equipment_id,
            "staffId": a.staff_id,
            "start": a.planned_start,
            "end": a.planned_end,
            "startAt": a.planned_start_at,
            "endAt": a.planned_end_at,
            "shift": a.planned_shift,
            "status": a.status,
            "reason": a.reason,
        }
