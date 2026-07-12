"""Equipment ORM model.

Persistence mapping for laboratory equipment. Conversion to/from the domain
object happens in the repository. Equipment is applicable to a set of Projects
(equipment_project) and bound to Methods (method_equipment) (ADR-018).
"""

from __future__ import annotations

from sqlalchemy import JSON, Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.infrastructure.orm.common.base import BaseEntity
from backend.infrastructure.orm.laboratory.associations import (
    equipment_project,
    method_equipment,
)
from backend.infrastructure.orm.laboratory.project_orm import ProjectORM  # noqa: F401


class EquipmentORM(BaseEntity):
    __tablename__ = "equipment"

    equipment_code: Mapped[str] = mapped_column(String(50), index=True)
    name: Mapped[str] = mapped_column(String(200))
    unavailable_dates: Mapped[list] = mapped_column(JSON, default=list)
    overtime_dates: Mapped[list] = mapped_column(JSON, default=list)
    fv_duration: Mapped[int] = mapped_column(Integer, default=1)
    fv_validity: Mapped[int] = mapped_column(Integer, default=14)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Projects this equipment is applicable to (ADR-018).
    projects: Mapped[list[ProjectORM]] = relationship(
        "ProjectORM",
        secondary=equipment_project,
        lazy="selectin",
    )
    # Methods this equipment is bound to (reverse of method_equipment).
    methods: Mapped[list[OperationDefinitionORM]] = relationship(  # noqa: F821
        "OperationDefinitionORM",
        secondary=method_equipment,
        back_populates="equipment",
        lazy="selectin",
    )
