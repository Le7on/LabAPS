"""Composition Root.

The only place where the application object graph is assembled. Dependencies are
constructed here and injected downward (Configuration -> Infrastructure ->
Repositories -> Engines -> Use Cases -> API). No other module assembles business
objects (see Development Guide chapter 3).
"""

from __future__ import annotations

from dataclasses import dataclass

from backend.config.settings import AppConfig
from backend.infrastructure.persistence.database import Database


@dataclass(slots=True)
class Container:
    """Holds the assembled application dependencies.

    Later phases extend this with engines and additional repositories/use cases.
    The database and its session factory are constructed once and shared.
    """

    config: AppConfig
    database: Database

    @property
    def session_factory(self):
        return self.database.session_factory


def build_container(config: AppConfig) -> Container:
    """Assemble the application object graph from configuration."""

    database = Database(config.database.url)

    return Container(config=config, database=database)
