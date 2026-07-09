"""Planning Problem.

Canonical representation of one scheduling problem, generated from a Plan Version
and its Planning Context. Independent of Database, ORM, Flask, OR-Tools and UI
(Planning Model, chapter 3). Immutable and free of optimization concepts.
"""

from __future__ import annotations

from dataclasses import dataclass, field

EQUIPMENT = "equipment"
STAFF = "staff"


@dataclass(frozen=True, slots=True)
class Resource:
    """Available scheduling capacity.

    ``kind`` is "equipment" or "staff"; ``provides`` is the resource's capability
    set (equipment) or skill set (staff).
    """

    identifier: str
    kind: str = EQUIPMENT
    provides: frozenset[str] = frozenset()


@dataclass(frozen=True, slots=True)
class Operation:
    """Executable work to be scheduled.

    An operation may require a capability (equipment) and/or a skill (staff).
    """

    identifier: str
    duration: int
    required_capability: str | None = None
    required_skill: str | None = None
    depends_on: tuple[str, ...] = ()
    weight: int = 1


# Objective selectors mirrored from the scheduling model (kept as plain strings
# here so the Planning Problem stays free of optimization types).
OBJECTIVE_MAKESPAN = "makespan"
OBJECTIVE_WEIGHTED_COMPLETION = "weighted_completion"


@dataclass(frozen=True, slots=True)
class PlanningPolicies:
    """Planning behaviour (not a business entity)."""

    planning_horizon: int = 100
    objective: str = OBJECTIVE_MAKESPAN


@dataclass(frozen=True, slots=True)
class PlanningProblem:
    """What must be scheduled. Never how to optimize.

    Contains facts only: resources, operations and planning policies. Contains no
    solver variables or mathematical constraints.
    """

    resources: tuple[Resource, ...] = ()
    operations: tuple[Operation, ...] = ()
    policies: PlanningPolicies = field(default_factory=PlanningPolicies)
