"""Unit tests for laboratory domain objects (pure, no framework)."""

from __future__ import annotations

import pytest

from backend.modules.laboratory.domain.aggregates.workflow_definition import (
    WorkflowDefinition,
)
from backend.modules.laboratory.domain.entities.staff import Staff
from backend.shared.errors import ValidationError


def test_staff_skill_query_and_deactivate():
    staff = Staff(staff_code="ST-1", name="Alice", skills={"pcr"})
    assert staff.has_skill("pcr")
    assert not staff.has_skill("elisa")
    staff.deactivate()
    assert staff.active is False


def test_workflow_add_operation_is_owned_by_aggregate():
    workflow = WorkflowDefinition(workflow_code="WF-1", name="Prep")
    op = workflow.add_operation(operation_type="extract", duration=3, required_capability="spin")

    assert len(workflow.operations) == 1
    assert workflow.operations[0] is op
    assert op.required_capability == "spin"


def test_operation_requires_positive_duration():
    workflow = WorkflowDefinition(workflow_code="WF-1", name="Prep")
    with pytest.raises(ValidationError):
        workflow.add_operation(operation_type="extract", duration=0)
