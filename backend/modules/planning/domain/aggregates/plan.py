"""Plan aggregate root.

Plan is the Aggregate Root of the Planning domain (ADR-001). It owns its
PlanVersions and enforces invariants. Pure Python: no framework dependencies.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime

from backend.modules.planning.domain.entities.plan_version import PlanVersion
from backend.modules.planning.domain.enums.plan_enums import (
    PlanStatus,
    PlanVersionStatus,
    VersionType,
)
from backend.shared.errors import NotFoundError, ValidationError

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
    # Calendar configuration (ADR-016). A plan always runs over a real date range;
    # the scheduler maps integer shift-slot units to these dates + shift windows.
    start_date: str | None = None
    end_date: str | None = None
    shift_mode: str = "single"
    skipped_dates: list[str] = field(default_factory=list)
    # PI request lines: run a workflow N rounds on a target date (ADR-020).
    demand_lines: list = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.planning_horizon:
            raise ValidationError("planningHorizon is required")
        if not self.name:
            raise ValidationError("name is required")
        if not self.start_date or not self.end_date:
            raise ValidationError("startDate and endDate are required")
        if self.end_date < self.start_date:
            raise ValidationError("endDate must be on or after startDate")
        if not self.plan_code:
            self.plan_code = self.derive_plan_code(self.planning_horizon)
        if self.shift_mode not in ("single", "double"):
            raise ValidationError("shiftMode must be 'single' or 'double'")

    def has_calendar(self) -> bool:
        # A plan always has a calendar now; kept for call-site compatibility.
        return True

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

    # -- version lifecycle (aggregate coordinates its children) ----------

    def get_version(self, version_id: str) -> PlanVersion:
        for version in self.versions:
            if version.id == version_id:
                return version
        raise NotFoundError(f"Plan version {version_id} not found")

    def mark_version_scheduled(self, version_id: str) -> PlanVersion:
        version = self.get_version(version_id)
        version.mark_scheduled()
        return version

    def review_version(self, version_id: str) -> PlanVersion:
        version = self.get_version(version_id)
        version.mark_reviewed()
        return version

    def publish_version(self, version_id: str) -> PlanVersion:
        """Publish a version, enforcing one published version per plan (BR-PV-004)."""
        version = self.get_version(version_id)
        version.publish()
        # Any previously published version is superseded and archived.
        for other in self.versions:
            if other.id != version_id and other.status == PlanVersionStatus.PUBLISHED:
                other.status = PlanVersionStatus.ARCHIVED
        return version

    def archive_version(self, version_id: str) -> PlanVersion:
        version = self.get_version(version_id)
        version.archive()
        return version
