"""Per-plan resource availability ORM.

Records, for one Plan, whether a specific resource (staff or equipment) is
available during that plan's period. Availability is per-plan (the same resource
can be available in one plan and not another). Only explicit settings are stored;
a resource with no row defaults to available.
"""

from __future__ import annotations

from sqlalchemy import JSON, Boolean, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from backend.infrastructure.orm.common.base import BaseEntity


class PlanResourceAvailabilityORM(BaseEntity):
    __tablename__ = "plan_resource_availability"
    __table_args__ = (
        UniqueConstraint("plan_id", "resource_kind", "resource_id", name="uq_plan_resource"),
    )

    plan_id: Mapped[str] = mapped_column(String(36), index=True)
    resource_kind: Mapped[str] = mapped_column(String(20))  # "staff" | "equipment"
    resource_id: Mapped[str] = mapped_column(String(36))
    # False = unavailable for the whole plan period. True (default) = available,
    # except on any date ranges in ``unavailable_dates`` (leave / breakdown /
    # downtime), each ["YYYY-MM-DD", "YYYY-MM-DD"] inclusive.
    available: Mapped[bool] = mapped_column(Boolean, default=True)
    unavailable_dates: Mapped[list] = mapped_column(JSON, default=list)
