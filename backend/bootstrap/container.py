"""Composition Root.

The only place where the application object graph is assembled. Dependencies are
constructed here and injected downward (Configuration -> Infrastructure ->
Repositories -> Engines -> Use Cases -> API). No other module assembles business
objects (see Development Guide chapter 3).
"""

from __future__ import annotations

from dataclasses import dataclass

from backend.config.settings import AppConfig
from backend.engines.scheduling.scheduling_engine import SchedulingEngine
from backend.infrastructure.persistence.database import Database
from backend.solver.adapter.ortools_solver_adapter import ORToolsSolverAdapter


@dataclass(slots=True)
class Container:
    """Holds the assembled application dependencies.

    The database/session factory and the (stateless) scheduling engine are
    constructed once and shared. Later phases extend this with additional
    repositories and use cases.
    """

    config: AppConfig
    database: Database
    scheduling_engine: SchedulingEngine

    @property
    def session_factory(self):
        return self.database.session_factory


def build_container(config: AppConfig) -> Container:
    """Assemble the application object graph from configuration."""

    database = Database(config.database.url)

    # Stateless scheduling engine with the OR-Tools solver adapter injected.
    scheduling_engine = SchedulingEngine(solver_adapter=ORToolsSolverAdapter())

    return Container(
        config=config,
        database=database,
        scheduling_engine=scheduling_engine,
    )
