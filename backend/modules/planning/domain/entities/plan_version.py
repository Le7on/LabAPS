"""PlanVersion entity.

A version of a Plan. Belongs to the Plan aggregate. Pure Python: no Flask,
SQLAlchemy or OR-Tools (Engineering Baseline, dependency rules).
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime

from backend.modules.planning.domain.enums.plan_enums import (
    PlanVersionStatus,
    VersionType,
)
from backend.shared.errors import ConflictError


@dataclass(slots=True)
class PlanVersion:
    version_number: int
    version_type: VersionType = VersionType.WORKING
    status: PlanVersionStatus = PlanVersionStatus.WORKING
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @property
    def is_published(self) -> bool:
        return self.status == PlanVersionStatus.PUBLISHED

    # -- lifecycle behaviour (State Model, chapter 3) --------------------
    # Transitions occur only through these methods; the status is never set
    # directly by callers.

    def mark_scheduled(self) -> None:
        """A feasible schedule was produced (Working/Scheduled/Reviewed -> Scheduled)."""
        self._reject_if_published()
        if self.status == PlanVersionStatus.ARCHIVED:
            raise ConflictError(
                "Archived plan version cannot be scheduled",
                details=[{"code": "INVALID_PLAN_VERSION_STATE"}],
            )
        self.status = PlanVersionStatus.SCHEDULED

    def mark_reviewed(self) -> None:
        """Approve the schedule for publication (Scheduled -> Reviewed)."""
        if self.status != PlanVersionStatus.SCHEDULED:
            raise ConflictError(
                "Only a scheduled plan version can be reviewed",
                details=[{"code": "INVALID_PLAN_VERSION_STATE"}],
            )
        self.status = PlanVersionStatus.REVIEWED

    def publish(self) -> None:
        """Publish the reviewed version (Reviewed -> Published)."""
        if self.status != PlanVersionStatus.REVIEWED:
            raise ConflictError(
                "Only a reviewed plan version can be published",
                details=[{"code": "INVALID_PLAN_VERSION_STATE"}],
            )
        self.status = PlanVersionStatus.PUBLISHED

    def archive(self) -> None:
        """Archive the version (any non-archived state -> Archived)."""
        if self.status == PlanVersionStatus.ARCHIVED:
            raise ConflictError(
                "Plan version is already archived",
                details=[{"code": "INVALID_PLAN_VERSION_STATE"}],
            )
        self.status = PlanVersionStatus.ARCHIVED

    def _reject_if_published(self) -> None:
        if self.status == PlanVersionStatus.PUBLISHED:
            raise ConflictError(
                "Published plan versions are immutable",
                details=[{"code": "PLAN_VERSION_PUBLISHED"}],
            )
