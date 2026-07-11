"""Unit tests for laboratory domain objects (pure, no framework)."""

from __future__ import annotations

import pytest

from backend.modules.laboratory.domain.aggregates.workflow_definition import (
    WorkflowDefinition,
)
from backend.modules.laboratory.domain.entities.staff import Staff
from backend.shared.errors import ValidationError


def test_staff_qualification_query_and_deactivate():
    staff = Staff(staff_code="ST-1", name="Alice", qualified_project_ids={"P-1"})
    assert staff.is_qualified_for("P-1")
    assert not staff.is_qualified_for("P-2")
    staff.deactivate()
    assert staff.active is False


def test_workflow_add_operation_is_owned_by_aggregate():
    workflow = WorkflowDefinition(workflow_code="WF-1", name="Prep", project_id="P-1")
    op = workflow.add_operation(
        operation_type="extract", duration=3, gelatin_type="A", equipment_ids=("EQ-1",)
    )

    assert len(workflow.operations) == 1
    assert workflow.operations[0] is op
    assert op.gelatin_type == "A"
    assert op.equipment_ids == ("EQ-1",)


def test_operation_requires_positive_duration():
    workflow = WorkflowDefinition(workflow_code="WF-1", name="Prep", project_id="P-1")
    with pytest.raises(ValidationError):
        workflow.add_operation(operation_type="extract", duration=0)


def test_workflow_requires_project():
    with pytest.raises(ValidationError):
        WorkflowDefinition(workflow_code="WF-1", name="Prep")
