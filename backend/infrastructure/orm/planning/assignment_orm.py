"""Assignment ORM model.

Persistence for scheduling results. Belongs to the Plan Version aggregate
(Table Dictionary: assignment). Conversion happens in the repository.

Scope note: this slice references the scheduling operation id directly and stores
planned start/end as integer time units (the scheduler's horizon units). When
Operation Instances and a calendar are modelled, operation_id becomes
operation_instance_id and the times become datetimes.
"""

from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.infrastructure.orm.common.base import BaseEntity


class AssignmentORM(BaseEntity):
    __tablename__ = "assignment"

    plan_version_id: Mapped[str] = mapped_column(String(36), index=True)
    operation_id: Mapped[str] = mapped_column(String(100))
    equipment_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    staff_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    planned_start: Mapped[int] = mapped_column(Integer)
    planned_end: Mapped[int] = mapped_column(Integer)
    # Real calendar times (ADR-016): set when the plan has a calendar; the
    # integer units above map to these via the shift calendar. Null otherwise.
    planned_start_at: Mapped[str | None] = mapped_column(String(25), nullable=True)
    planned_end_at: Mapped[str | None] = mapped_column(String(25), nullable=True)
    planned_shift: Mapped[str | None] = mapped_column(String(20), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    reason: Mapped[str | None] = mapped_column(String(500), nullable=True)
