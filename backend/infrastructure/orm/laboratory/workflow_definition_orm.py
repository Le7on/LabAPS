"""Workflow Definition ORM models.

Persistence mapping for the Workflow Definition aggregate and its owned Operation
Definitions. Conversion to/from domain objects happens in the repository. Cascade
stays within the aggregate boundary (SQLAlchemy Mapping Guide, section 7).
"""

from __future__ import annotations

from sqlalchemy import JSON, Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.infrastructure.orm.common.base import BaseEntity
from backend.infrastructure.orm.laboratory.associations import method_equipment


class WorkflowDefinitionORM(BaseEntity):
    __tablename__ = "workflow_definition"

    workflow_code: Mapped[str] = mapped_column(String(50), index=True)
    name: Mapped[str] = mapped_column(String(200))
    # A workflow is defined for exactly one project (ADR-015, SSOT section 6).
    project_id: Mapped[str] = mapped_column(ForeignKey("project.id"), index=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    operations: Mapped[list[OperationDefinitionORM]] = relationship(
        back_populates="workflow",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class OperationDefinitionORM(BaseEntity):
    """A Method (= Stage) within a workflow (ADR-015).

    ``duration`` is the number of shifts the method occupies (1 shift = 1
    scheduler time unit). ``gelatin_type`` is a method attribute; equipment is
    bound explicitly via ``method_equipment`` rather than matched by capability.
    """

    __tablename__ = "operation_definition"

    workflow_id: Mapped[str] = mapped_column(ForeignKey("workflow_definition.id"), index=True)
    operation_type: Mapped[str] = mapped_column(String(100))
    duration: Mapped[int] = mapped_column(Integer)
    gelatin_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    depends_on: Mapped[list] = mapped_column(JSON, default=list)

    workflow: Mapped[WorkflowDefinitionORM] = relationship(back_populates="operations")
    equipment: Mapped[list[EquipmentORM]] = relationship(  # noqa: F821
        "EquipmentORM",
        secondary=method_equipment,
        back_populates="methods",
        lazy="selectin",
    )
