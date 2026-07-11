"""Tests for Staff <-> Project qualification (ADR-014, ADR-017).

A staff member's Skill is the set of projects it is qualified for. Being
qualified means the staff member may perform that project's work. Creating staff
with unknown project ids is rejected.
"""

from __future__ import annotations

import pytest

from backend.app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def _project(client, code="PRJ-1"):
    return client.post("/api/v1/projects", json={"projectCode": code, "name": code}).get_json()[
        "data"
    ]["id"]


def test_staff_qualified_for_projects(client):
    p1 = _project(client, "PRJ-1")
    p2 = _project(client, "PRJ-2")
    created = client.post(
        "/api/v1/staff",
        json={"staffCode": "ST-1", "name": "Alice", "qualifiedProjectIds": [p1, p2]},
    )
    assert created.status_code == 201
    assert sorted(created.get_json()["data"]["qualifiedProjectIds"]) == sorted([p1, p2])

    # Round-trips through listing.
    listed = client.get("/api/v1/staff").get_json()["data"][0]
    assert sorted(listed["qualifiedProjectIds"]) == sorted([p1, p2])


def test_staff_without_projects_defaults_empty(client):
    created = client.post("/api/v1/staff", json={"staffCode": "ST-2", "name": "Bob"})
    assert created.status_code == 201
    assert created.get_json()["data"]["qualifiedProjectIds"] == []


def test_staff_rejects_unknown_project(client):
    response = client.post(
        "/api/v1/staff",
        json={"staffCode": "ST-3", "name": "Carol", "qualifiedProjectIds": ["does-not-exist"]},
    )
    assert response.status_code == 422
    assert response.get_json()["error"]["code"] == "VALIDATION_FAILED"
