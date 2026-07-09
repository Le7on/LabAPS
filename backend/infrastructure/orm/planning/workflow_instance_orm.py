"""Workflow Instance and Operation Instance ORM models.

Generated from a Workflow Definition into a Plan Version (ADR-003, ADR-004).
WorkflowInstance belongs to the Plan Version aggregate; OperationInstance belongs
to the WorkflowInstance. OperationInstance is the smallest schedulable business
object. Conversion happens in the repository.
"""

from __future__ import annotations

from sqlalchemy import JSON, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.infrastructure.orm.common.base import BaseEntity


class WorkflowInstanceORM(BaseEntity):
    __tablename__ = "workflow_instance"

    plan_version_id: Mapped[str] = mapped_column(String(36), index=True)
    workflow_definition_id: Mapped[str] = mapped_column(String(36))
    workflow_code: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(20), default="generated")

    operations: Mapped[list[OperationInstanceORM]] = relationship(
        back_populates="workflow",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class OperationInstanceORM(BaseEntity):
    __tablename__ = "operation_instance"

    workflow_instance_id: Mapped[str] = mapped_column(
        ForeignKey("workflow_instance.id"), index=True
    )
    operation_definition_id: Mapped[str] = mapped_column(String(36))
    operation_code: Mapped[str] = mapped_column(String(100))
    sequence_no: Mapped[int] = mapped_column(Integer)
    duration_shift: Mapped[int] = mapped_column(Integer)
    required_capability: Mapped[str | None] = mapped_column(String(100), nullable=True)
    required_skill: Mapped[str | None] = mapped_column(String(100), nullable=True)
    required_qualification: Mapped[str | None] = mapped_column(String(100), nullable=True)
    depends_on: Mapped[list] = mapped_column(JSON, default=list)
    status: Mapped[str] = mapped_column(String(20), default="pending")

    workflow: Mapped[WorkflowInstanceORM] = relationship(back_populates="operations")
