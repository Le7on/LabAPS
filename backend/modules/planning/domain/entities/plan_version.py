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


@dataclass(slots=True)
class PlanVersion:
    version_number: int
    version_type: VersionType = VersionType.WORKING
    status: PlanVersionStatus = PlanVersionStatus.DRAFT
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @property
    def is_published(self) -> bool:
        return self.status == PlanVersionStatus.PUBLISHED
