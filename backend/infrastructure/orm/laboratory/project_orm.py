"""Project ORM model.

Persistence for laboratory projects. Conversion to/from the domain object happens
in the repository.
"""

from __future__ import annotations

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.infrastructure.orm.common.base import BaseEntity


class ProjectORM(BaseEntity):
    __tablename__ = "project"

    project_code: Mapped[str] = mapped_column(String(50), index=True)
    name: Mapped[str] = mapped_column(String(200))
    active: Mapped[bool] = mapped_column(Boolean, default=True)
