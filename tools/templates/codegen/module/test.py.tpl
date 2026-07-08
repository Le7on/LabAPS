"""Tests for the {{NAME_TITLE}} module."""

from __future__ import annotations

import pytest

from backend.modules.{{NAME_SNAKE}}.domain.entities.{{NAME_SNAKE}} import {{NAME_PASCAL}}
from backend.shared.errors import ValidationError


def test_{{NAME_SNAKE}}_creation():
    entity = {{NAME_PASCAL}}(name="example")
    assert entity.name == "example"
    assert entity.id


def test_{{NAME_SNAKE}}_requires_name():
    with pytest.raises(ValidationError):
        {{NAME_PASCAL}}(name="")
