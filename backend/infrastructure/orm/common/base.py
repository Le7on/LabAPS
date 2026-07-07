"""ORM base classes.

ORM models are persistence models only, never Domain Objects (SQLAlchemy Mapping
Guide, principles 1-2). The declarative base and shared columns live here.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Declarative base for all Lab APS ORM models."""


def _uuid() -> str:
    return str(uuid.uuid4())


class BaseEntity(Base):
    """Abstract base providing UUID identity and audit/timestamp columns.

    UUID is the technical identity and is never exposed to end users; business
    codes are separate columns on concrete tables.
    """

    __abstract__ = True

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    created_by: Mapped[str] = mapped_column(String(100), default="system")
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
    updated_by: Mapped[str] = mapped_column(String(100), default="system")
