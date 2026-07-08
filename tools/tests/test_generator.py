"""Tests for the code generator.

Generates into a temporary project root (via the generator's context) and checks
that files are created and the name substitutions are applied.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from generator import Generator


@pytest.fixture()
def generator(tmp_path: Path) -> Generator:
    gen = Generator()
    # Redirect output to a temporary project root; keep the real template root.
    gen.context.project_root = tmp_path
    return gen


def test_new_module_creates_layered_skeleton(generator, tmp_path):
    generator.new_module("work order")

    module = tmp_path / "backend" / "modules" / "work_order"
    for layer in ("api", "application", "domain", "repository", "dto", "tests"):
        assert (module / layer / "__init__.py").is_file()

    entity = (module / "domain" / "entities" / "work_order.py").read_text(encoding="utf-8")
    assert "class WorkOrder:" in entity

    api = (module / "api" / "work_order_api.py").read_text(encoding="utf-8")
    assert 'Blueprint("work_order"' in api


def test_new_entity_renders_name(generator, tmp_path):
    generator.new_entity("planning", "material batch")

    path = (
        tmp_path / "backend" / "modules" / "planning" / "domain" / "entities" / "material_batch.py"
    )
    text = path.read_text(encoding="utf-8")
    assert "class MaterialBatch:" in text


def test_new_usecase_renders_name(generator, tmp_path):
    generator.new_usecase("planning", "approve plan version")

    path = tmp_path / "backend" / "modules" / "planning" / "application" / "approve_plan_version.py"
    text = path.read_text(encoding="utf-8")
    assert "class ApprovePlanVersionUseCase:" in text
