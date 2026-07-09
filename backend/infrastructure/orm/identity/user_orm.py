"""User and API token ORM models (ADR-013).

Only a hash of each token is stored, never the token itself. A user owns one or
more tokens and has a single role.
"""

from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.infrastructure.orm.common.base import BaseEntity


class UserORM(BaseEntity):
    __tablename__ = "app_user"

    username: Mapped[str] = mapped_column(String(100), index=True, unique=True)
    role: Mapped[str] = mapped_column(String(30))
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    tokens: Mapped[list[ApiTokenORM]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class ApiTokenORM(BaseEntity):
    __tablename__ = "api_token"

    user_id: Mapped[str] = mapped_column(ForeignKey("app_user.id"), index=True)
    token_hash: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    label: Mapped[str] = mapped_column(String(100), default="")

    user: Mapped[UserORM] = relationship(back_populates="tokens")
