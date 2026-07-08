"""Staff ORM model.

Persistence mapping for laboratory staff. Conversion to/from the domain object
happens in the repository.

Scope note: skills are stored as a JSON list for this slice. The fuller design
uses a staff_skill mapping table once the Skill aggregate exists (SQLAlchemy
Mapping Guide, section 6).
"""

from __future__ import annotations

from sqlalchemy import JSON, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.infrastructure.orm.common.base import BaseEntity


class StaffORM(BaseEntity):
    __tablename__ = "staff"

    staff_code: Mapped[str] = mapped_column(String(50), index=True)
    name: Mapped[str] = mapped_column(String(200))
    skills: Mapped[list] = mapped_column(JSON, default=list)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
