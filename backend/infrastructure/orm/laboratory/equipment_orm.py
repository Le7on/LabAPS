"""Equipment ORM model.

Persistence mapping for laboratory equipment. Conversion to/from the domain
object happens in the repository.

Scope note: capabilities are stored as a JSON list for this slice. The fuller
design uses an equipment_capability mapping table once the Capability aggregate
exists (SQLAlchemy Mapping Guide, section 6).
"""

from __future__ import annotations

from sqlalchemy import JSON, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.infrastructure.orm.common.base import BaseEntity


class EquipmentORM(BaseEntity):
    __tablename__ = "equipment"

    equipment_code: Mapped[str] = mapped_column(String(50), index=True)
    name: Mapped[str] = mapped_column(String(200))
    capabilities: Mapped[list] = mapped_column(JSON, default=list)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
