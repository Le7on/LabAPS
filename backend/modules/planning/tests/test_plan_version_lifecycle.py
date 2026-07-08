"""Unit tests for the Plan Version lifecycle (State Model, chapter 3)."""

from __future__ import annotations

import pytest

from backend.modules.planning.domain.aggregates.plan import Plan
from backend.modules.planning.domain.enums.plan_enums import PlanVersionStatus
from backend.shared.errors import ConflictError


def _plan_with_version() -> tuple[Plan, str]:
    plan = Plan(planning_horizon="2026-W33", name="P")
    version = plan.create_version()
    return plan, version.id


def test_happy_path_working_to_published():
    plan, vid = _plan_with_version()

    plan.mark_version_scheduled(vid)
    assert plan.get_version(vid).status == PlanVersionStatus.SCHEDULED

    plan.review_version(vid)
    assert plan.get_version(vid).status == PlanVersionStatus.REVIEWED

    plan.publish_version(vid)
    assert plan.get_version(vid).status == PlanVersionStatus.PUBLISHED


def test_cannot_publish_working_version():
    plan, vid = _plan_with_version()
    with pytest.raises(ConflictError):
        plan.publish_version(vid)


def test_cannot_review_working_version():
    plan, vid = _plan_with_version()
    with pytest.raises(ConflictError):
        plan.review_version(vid)


def test_published_version_is_immutable_for_scheduling():
    plan, vid = _plan_with_version()
    plan.mark_version_scheduled(vid)
    plan.review_version(vid)
    plan.publish_version(vid)

    with pytest.raises(ConflictError):
        plan.mark_version_scheduled(vid)


def test_publishing_supersedes_previous_published_version():
    plan = Plan(planning_horizon="2026-W33", name="P")
    v1 = plan.create_version()
    v2 = plan.create_version()

    for v in (v1, v2):
        plan.mark_version_scheduled(v.id)
        plan.review_version(v.id)

    plan.publish_version(v1.id)
    plan.publish_version(v2.id)

    assert plan.get_version(v1.id).status == PlanVersionStatus.ARCHIVED
    assert plan.get_version(v2.id).status == PlanVersionStatus.PUBLISHED
    published = [v for v in plan.versions if v.status == PlanVersionStatus.PUBLISHED]
    assert len(published) == 1
