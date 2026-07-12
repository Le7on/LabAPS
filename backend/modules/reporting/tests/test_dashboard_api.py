"""Dashboard reporting API tests."""

from __future__ import annotations

import pytest

from backend.app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def test_empty_dashboard(client):
    response = client.get("/api/v1/reports/dashboard")
    assert response.status_code == 200
    data = response.get_json()["data"]
    assert data["plans"] == 0
    assert data["equipment"] == 0
    assert data["publishedVersions"] == 0


def test_dashboard_reflects_created_entities(client):
    client.post(
        "/api/v1/plans",
        json={
            "startDate": "2026-08-10",
            "endDate": "2026-08-20",
            "planningHorizon": "2026-W33",
            "name": "P",
        },
    )
    client.post(
        "/api/v1/equipment",
        json={"equipmentCode": "EQ-1", "name": "Machine", "capabilities": ["pcr"]},
    )
    client.post("/api/v1/staff", json={"staffCode": "ST-1", "name": "Alice"})
    project_id = client.post(
        "/api/v1/projects", json={"projectCode": "PRJ-1", "name": "Proj"}
    ).get_json()["data"]["id"]
    client.post(
        "/api/v1/workflow-definitions",
        json={"workflowCode": "WF-1", "name": "Prep", "projectId": project_id},
    )

    data = client.get("/api/v1/reports/dashboard").get_json()["data"]
    assert data["plans"] == 1
    assert data["equipment"] == 1
    assert data["activeEquipment"] == 1
    assert data["staff"] == 1
    assert data["workflowDefinitions"] == 1
