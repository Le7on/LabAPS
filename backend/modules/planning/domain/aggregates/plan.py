"""Plan aggregate root.

Plan is the Aggregate Root of the Planning domain (ADR-001). It owns its
PlanVersions and enforces invariants. Pure Python: no framework dependencies.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime

from backend.modules.planning.domain.entities.plan_version import PlanVersion
from backend.modules.planning.domain.enums.plan_enums import PlanStatus, VersionType
from backend.shared.errors import ValidationError

PLAN_CODE_PREFIX = "PLAN-"


@dataclass(slots=True)
class Plan:
    """A production plan identified by a planning horizon.

    ``plan_code`` is derived from the planning horizon (e.g. horizon
    ``2026-W33`` -> code ``PLAN-2026-W33``).
    """

    planning_horizon: str
    name: str
    description: str = ""
    status: PlanStatus = PlanStatus.DRAFT
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    plan_code: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    versions: list[PlanVersion] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.planning_horizon:
            raise ValidationError("planningHorizon is required")
        if not self.name:
            raise ValidationError("name is required")
        if not self.plan_code:
            self.plan_code = self.derive_plan_code(self.planning_horizon)

    @staticmethod
    def derive_plan_code(planning_horizon: str) -> str:
        return f"{PLAN_CODE_PREFIX}{planning_horizon}"

    def create_version(self, version_type: VersionType = VersionType.WORKING) -> PlanVersion:
        """Create and append a new PlanVersion, returning it."""

        version = PlanVersion(
            version_number=len(self.versions) + 1,
            version_type=version_type,
        )
        self.versions.append(version)
        return version
