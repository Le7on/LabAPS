"""Planning Context ORM model.

Stores one immutable planning snapshot per Plan Version (ADR-008; Table
Dictionary: planning_context). Snapshots are JSON and hold no live references, so
planning never depends on live configuration after scheduling begins.
"""

from __future__ import annotations

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.infrastructure.orm.common.base import BaseEntity


class PlanningContextORM(BaseEntity):
    __tablename__ = "planning_context"

    plan_version_id: Mapped[str] = mapped_column(String(36), index=True, unique=True)
    equipment_snapshot: Mapped[list] = mapped_column(JSON, default=list)
    staff_snapshot: Mapped[list] = mapped_column(JSON, default=list)
    solver_profile: Mapped[dict] = mapped_column(JSON, default=dict)
