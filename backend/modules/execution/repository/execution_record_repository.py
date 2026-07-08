"""Execution Record repository (append-only audit trail)."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.infrastructure.orm.execution.execution_record_orm import ExecutionRecordORM


class ExecutionRecordRepository:
    def __init__(self, session: Session):
        self.session = session

    def record(
        self,
        assignment_id: str,
        from_status: str,
        to_status: str,
        action: str,
        reason: str | None = None,
    ) -> None:
        self.session.add(
            ExecutionRecordORM(
                assignment_id=assignment_id,
                from_status=from_status,
                to_status=to_status,
                action=action,
                reason=reason,
            )
        )

    def list_for_assignment(self, assignment_id: str) -> list[dict]:
        stmt = (
            select(ExecutionRecordORM)
            .where(ExecutionRecordORM.assignment_id == assignment_id)
            .order_by(ExecutionRecordORM.created_at)
        )
        return [
            {
                "fromStatus": r.from_status,
                "toStatus": r.to_status,
                "action": r.action,
                "reason": r.reason,
                "recordedAt": r.created_at.isoformat(),
            }
            for r in self.session.scalars(stmt).all()
        ]
