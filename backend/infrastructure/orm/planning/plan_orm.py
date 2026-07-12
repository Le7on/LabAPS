"""Plan aggregate ORM models.

Persistence mapping only. Conversion to/from Domain Objects happens in the
repository (SQLAlchemy Mapping Guide, section 12).
"""

from __future__ import annotations

from sqlalchemy import JSON, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.infrastructure.orm.common.base import BaseEntity


class PlanORM(BaseEntity):
    __tablename__ = "plan"

    plan_code: Mapped[str] = mapped_column(String(50), index=True)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(String(500), default="")
    planning_horizon: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(20), default="draft")
    # Calendar configuration (ADR-016). When start/end are set, scheduling maps
    # integer time units to real dates + shift windows. shift_mode is
    # "single" or "double"; skipped_dates are "YYYY-MM-DD" strings excluded
    # from the calendar.
    start_date: Mapped[str | None] = mapped_column(String(10), nullable=True)
    end_date: Mapped[str | None] = mapped_column(String(10), nullable=True)
    shift_mode: Mapped[str] = mapped_column(String(10), default="single")
    skipped_dates: Mapped[list] = mapped_column(JSON, default=list)

    versions: Mapped[list[PlanVersionORM]] = relationship(
        back_populates="plan",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    demand_lines: Mapped[list[PlanDemandLineORM]] = relationship(
        back_populates="plan",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class PlanDemandLineORM(BaseEntity):
    """A PI request line: run a workflow N rounds on a target date (ADR-020)."""

    __tablename__ = "plan_demand_line"

    plan_id: Mapped[str] = mapped_column(ForeignKey("plan.id"), index=True)
    workflow_definition_id: Mapped[str] = mapped_column(String(36))
    operation_definition_id: Mapped[str] = mapped_column(String(36), default="")
    rounds: Mapped[int] = mapped_column(Integer)
    target_date: Mapped[str] = mapped_column(String(10))

    plan: Mapped[PlanORM] = relationship(back_populates="demand_lines")


class PlanVersionORM(BaseEntity):
    __tablename__ = "plan_version"

    plan_id: Mapped[str] = mapped_column(ForeignKey("plan.id"), index=True)
    version_number: Mapped[int] = mapped_column(Integer)
    version_type: Mapped[str] = mapped_column(String(20), default="working")
    status: Mapped[str] = mapped_column(String(20), default="draft")

    plan: Mapped[PlanORM] = relationship(back_populates="versions")
