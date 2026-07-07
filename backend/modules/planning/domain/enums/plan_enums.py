"""Planning domain enumerations.

Business enumerations are Python Enums; magic strings are prohibited
(SQLAlchemy Mapping Guide, section 10).
"""

from __future__ import annotations

from enum import StrEnum


class PlanStatus(StrEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"


class VersionType(StrEnum):
    WORKING = "working"
    PUBLISHED = "published"
    SIMULATION = "simulation"


class PlanVersionStatus(StrEnum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    APPROVED = "approved"
    PUBLISHED = "published"
