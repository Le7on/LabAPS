"""Deactivate / activate API tests for laboratory resources."""

from __future__ import annotations

import pytest

from backend.app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def test_deactivate_and_reactivate_equipment(client):
    created = client.post(
        "/api/v1/equipment",
        json={"equipmentCode": "EQ-1", "name": "M", "capabilities": ["pcr"]},
    )
    eq_id = created.get_json()["data"]["id"]

    deactivated = client.post(f"/api/v1/equipment/{eq_id}/deactivate")
    assert deactivated.status_code == 200
    assert deactivated.get_json()["data"]["active"] is False

    listed = client.get("/api/v1/equipment").get_json()["data"][0]
    assert listed["active"] is False

    reactivated = client.post(f"/api/v1/equipment/{eq_id}/activate")
    assert reactivated.status_code == 200
    assert reactivated.get_json()["data"]["active"] is True


def test_deactivate_staff(client):
    staff_id = client.post("/api/v1/staff", json={"staffCode": "ST-1", "name": "Alice"}).get_json()[
        "data"
    ]["id"]
    response = client.post(f"/api/v1/staff/{staff_id}/deactivate")
    assert response.status_code == 200
    assert response.get_json()["data"]["active"] is False


def test_deactivate_project(client):
    project_id = client.post(
        "/api/v1/projects", json={"projectCode": "PRJ-1", "name": "Assay"}
    ).get_json()["data"]["id"]
    response = client.post(f"/api/v1/projects/{project_id}/deactivate")
    assert response.status_code == 200
    assert response.get_json()["data"]["active"] is False


def test_deactivate_unknown_returns_404(client):
    response = client.post("/api/v1/equipment/nope/deactivate")
    assert response.status_code == 404
