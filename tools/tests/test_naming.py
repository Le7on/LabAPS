"""Tests for the code-generation naming helpers."""

from __future__ import annotations

import pytest
from naming import naming_context, to_camel, to_pascal, to_snake, to_title


@pytest.mark.parametrize(
    ("value", "snake", "pascal", "camel", "title"),
    [
        ("plan version", "plan_version", "PlanVersion", "planVersion", "Plan Version"),
        ("PlanVersion", "plan_version", "PlanVersion", "planVersion", "Plan Version"),
        ("plan_version", "plan_version", "PlanVersion", "planVersion", "Plan Version"),
        ("equipment", "equipment", "Equipment", "equipment", "Equipment"),
        ("work-order", "work_order", "WorkOrder", "workOrder", "Work Order"),
    ],
)
def test_case_conversions(value, snake, pascal, camel, title):
    assert to_snake(value) == snake
    assert to_pascal(value) == pascal
    assert to_camel(value) == camel
    assert to_title(value) == title


def test_naming_context_keys():
    ctx = naming_context("plan version")
    assert ctx == {
        "NAME_SNAKE": "plan_version",
        "NAME_PASCAL": "PlanVersion",
        "NAME_CAMEL": "planVersion",
        "NAME_TITLE": "Plan Version",
    }
