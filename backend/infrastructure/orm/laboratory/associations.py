"""Laboratory many-to-many association tables.

Kept in a neutral module so ORM models can reference the same Table objects
without importing each other (avoids circular imports). ADR-014/015/017/018.
"""

from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Table

from backend.infrastructure.orm.common.base import Base

# Staff <-> Project: which projects a staff member is qualified for (ADR-014/017).
staff_project = Table(
    "staff_project",
    Base.metadata,
    Column("staff_id", ForeignKey("staff.id"), primary_key=True),
    Column("project_id", ForeignKey("project.id"), primary_key=True),
)

# Method (operation definition) <-> Equipment: methods bound to equipment
# (ADR-015).
method_equipment = Table(
    "method_equipment",
    Base.metadata,
    Column("operation_definition_id", ForeignKey("operation_definition.id"), primary_key=True),
    Column("equipment_id", ForeignKey("equipment.id"), primary_key=True),
)

# Equipment <-> Project: projects an equipment is applicable to (ADR-018).
equipment_project = Table(
    "equipment_project",
    Base.metadata,
    Column("equipment_id", ForeignKey("equipment.id"), primary_key=True),
    Column("project_id", ForeignKey("project.id"), primary_key=True),
)
