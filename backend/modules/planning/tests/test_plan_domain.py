"""Unit tests for the Plan aggregate (pure domain, no framework)."""

from __future__ import annotations

import pytest

from backend.modules.planning.domain.aggregates.plan import Plan
from backend.modules.planning.domain.enums.plan_enums import (
    PlanStatus,
    PlanVersionStatus,
    VersionType,
)
from backend.shared.errors import ValidationError


def test_plan_code_derived_from_horizon():
    plan = Plan(planning_horizon="2026-W33", name="Week 33")
    assert plan.plan_code == "PLAN-2026-W33"
    assert plan.status == PlanStatus.DRAFT


def test_plan_requires_horizon():
    with pytest.raises(ValidationError):
        Plan(planning_horizon="", name="No horizon")


def test_plan_requires_name():
    with pytest.raises(ValidationError):
        Plan(planning_horizon="2026-W33", name="")


def test_create_version_appends_incrementing_versions():
    plan = Plan(planning_horizon="2026-W33", name="Week 33")

    first = plan.create_version()
    second = plan.create_version(VersionType.SIMULATION)

    assert first.version_number == 1
    assert second.version_number == 2
    assert second.version_type == VersionType.SIMULATION
    assert len(plan.versions) == 2
    assert first.status == PlanVersionStatus.DRAFT
    assert not first.is_published
