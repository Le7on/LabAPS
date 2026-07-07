"""Planning Problem.

Canonical representation of one scheduling problem, generated from a Plan Version
and its Planning Context. Independent of Database, ORM, Flask, OR-Tools and UI
(Planning Model, chapter 3). Immutable and free of optimization concepts.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Resource:
    """Available scheduling capacity (equipment or staff)."""

    identifier: str
    capabilities: frozenset[str] = frozenset()


@dataclass(frozen=True, slots=True)
class Operation:
    """Executable work to be scheduled."""

    identifier: str
    duration: int
    required_capability: str | None = None
    depends_on: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class PlanningPolicies:
    """Planning behaviour (not a business entity)."""

    planning_horizon: int = 100


@dataclass(frozen=True, slots=True)
class PlanningProblem:
    """What must be scheduled. Never how to optimize.

    Contains facts only: resources, operations and planning policies. Contains no
    solver variables or mathematical constraints.
    """

    resources: tuple[Resource, ...] = ()
    operations: tuple[Operation, ...] = ()
    policies: PlanningPolicies = field(default_factory=PlanningPolicies)
