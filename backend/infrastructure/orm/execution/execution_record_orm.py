"""Execution Record ORM model.

Append-only audit trail of assignment execution transitions (State Model rule:
every transition shall be auditable). One row per transition.
"""

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from backend.infrastructure.orm.common.base import BaseEntity


class ExecutionRecordORM(BaseEntity):
    __tablename__ = "execution_record"

    assignment_id: Mapped[str] = mapped_column(String(36), index=True)
    from_status: Mapped[str] = mapped_column(String(20))
    to_status: Mapped[str] = mapped_column(String(20))
    action: Mapped[str] = mapped_column(String(20))
    reason: Mapped[str | None] = mapped_column(String(500), nullable=True)
