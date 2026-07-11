"""Staff ORM model.

Persistence mapping for laboratory staff. Conversion to/from the domain object
happens in the repository. A staff member's competency is the set of Projects it
is qualified for (ADR-017), via the staff_project join.
"""

from __future__ import annotations

from sqlalchemy import JSON, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.infrastructure.orm.common.base import BaseEntity
from backend.infrastructure.orm.laboratory.associations import staff_project
from backend.infrastructure.orm.laboratory.project_orm import ProjectORM  # noqa: F401


class StaffORM(BaseEntity):
    __tablename__ = "staff"

    staff_code: Mapped[str] = mapped_column(String(50), index=True)
    name: Mapped[str] = mapped_column(String(200))
    availability: Mapped[list] = mapped_column(JSON, default=list)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Projects this staff member is qualified for (ADR-017) — its "Skill".
    projects: Mapped[list[ProjectORM]] = relationship(
        "ProjectORM",
        secondary=staff_project,
        lazy="selectin",
    )
