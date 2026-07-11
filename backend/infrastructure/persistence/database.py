"""Database engine and session management.

Owns the SQLAlchemy engine and session factory. Sessions are handed to the
Application Layer, which defines transaction boundaries; repositories never
commit (SQLAlchemy Mapping Guide, section 13).
"""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from backend.infrastructure.orm.common.base import Base

# Import ORM models so they register on Base.metadata before create_all.
from backend.infrastructure.orm.execution import (
    execution_record_orm,  # noqa: F401
)
from backend.infrastructure.orm.identity import (
    user_orm,  # noqa: F401
)
from backend.infrastructure.orm.laboratory import (
    associations,  # noqa: F401
    equipment_orm,  # noqa: F401
    project_orm,  # noqa: F401
    staff_orm,  # noqa: F401
    workflow_definition_orm,  # noqa: F401
)
from backend.infrastructure.orm.planning import (
    assignment_orm,  # noqa: F401
    demand_orm,  # noqa: F401
    plan_orm,  # noqa: F401
    planning_context_orm,  # noqa: F401
    workflow_instance_orm,  # noqa: F401
)


class Database:
    """Holds the engine and session factory for one application instance."""

    def __init__(self, url: str):
        # check_same_thread=False lets the SQLite connection be shared across
        # Flask's request handling; safe for the single-process dev server.
        connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
        self.engine = create_engine(url, future=True, connect_args=connect_args)
        self.session_factory = sessionmaker(
            bind=self.engine, expire_on_commit=False, class_=Session
        )

    def create_all(self) -> None:
        """Create tables from ORM metadata (development bootstrap).

        Production schema changes go through Alembic migrations; this is a
        convenience for local development and tests.
        """

        Base.metadata.create_all(self.engine)

    def session(self) -> Session:
        return self.session_factory()
