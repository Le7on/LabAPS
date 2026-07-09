"""Demand ORM model.

Persistence for requested production quantities, owned by the Plan Version
aggregate (Table Dictionary: demand). Conversion happens in the repository.
"""

from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.infrastructure.orm.common.base import BaseEntity


class DemandORM(BaseEntity):
    __tablename__ = "demand"

    plan_version_id: Mapped[str] = mapped_column(String(36), index=True)
    project_id: Mapped[str] = mapped_column(String(100))
    quantity: Mapped[int] = mapped_column(Integer)
    priority: Mapped[str] = mapped_column(String(20), default="normal")
