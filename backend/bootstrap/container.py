"""Composition Root.

The only place where the application object graph is assembled. Dependencies are
constructed here and injected downward (Configuration -> Infrastructure ->
Repositories -> Engines -> Use Cases -> API). No other module assembles business
objects (see Development Guide chapter 3).
"""

from __future__ import annotations

from dataclasses import dataclass

from backend.config.settings import AppConfig


@dataclass(slots=True)
class Container:
    """Holds the assembled application dependencies.

    Later phases extend this with the database engine/session factory,
    repositories, engines and use cases. Kept intentionally small so the wiring
    stays explicit and each phase adds exactly what it needs.
    """

    config: AppConfig


def build_container(config: AppConfig) -> Container:
    """Assemble the application object graph from configuration."""

    return Container(config=config)
