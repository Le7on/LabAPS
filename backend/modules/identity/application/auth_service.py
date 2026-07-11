"""Authentication service (ADR-013).

Verifies bearer tokens against stored token hashes and creates users with tokens.
Tokens are opaque random strings; only their SHA-256 hash is persisted.
"""

from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass

from sqlalchemy import select

from backend.infrastructure.orm.identity.user_orm import ApiTokenORM, UserORM
from backend.modules.identity.domain.role import Role


@dataclass(frozen=True, slots=True)
class CurrentUser:
    id: str
    username: str
    role: Role


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


class AuthService:
    """Stateless auth operations, backed by a session factory."""

    def __init__(self, session_factory):
        self._session_factory = session_factory

    def create_user(self, username: str, role: Role, label: str = "default") -> dict:
        """Create a user with one API token. Returns the plaintext token once."""
        token = secrets.token_urlsafe(32)
        session = self._session_factory()
        try:
            user = UserORM(username=username, role=role.value)
            user.tokens.append(ApiTokenORM(token_hash=hash_token(token), label=label))
            session.add(user)
            session.commit()
            user_id = user.id
        finally:
            session.close()

        return {"id": user_id, "username": username, "role": role.value, "token": token}

    def issue_token(self, username: str, role: Role, label: str = "seed") -> dict:
        """Issue a new API token for a user, creating the user if absent.

        Idempotent bootstrap entry point: if the user already exists its role is
        left unchanged and a fresh token is appended; otherwise the user is
        created with ``role``. Returns the plaintext token once (only its hash is
        persisted) plus a ``created`` flag indicating whether the user was new.
        """
        token = secrets.token_urlsafe(32)
        session = self._session_factory()
        try:
            user = session.scalar(select(UserORM).where(UserORM.username == username))
            created = user is None
            if user is None:
                user = UserORM(username=username, role=role.value)
                session.add(user)
            user.tokens.append(ApiTokenORM(token_hash=hash_token(token), label=label))
            session.commit()
            result = {
                "id": user.id,
                "username": user.username,
                "role": user.role,
                "token": token,
                "created": created,
            }
        finally:
            session.close()

        return result

    def resolve(self, token: str) -> CurrentUser | None:
        """Resolve a plaintext bearer token to the current user, or None."""
        if not token:
            return None
        session = self._session_factory()
        try:
            stmt = select(ApiTokenORM).where(ApiTokenORM.token_hash == hash_token(token))
            row = session.scalar(stmt)
            if row is None or not row.user.active:
                return None
            return CurrentUser(id=row.user.id, username=row.user.username, role=Role(row.user.role))
        finally:
            session.close()
