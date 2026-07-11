"""KPI reporting API tests."""

from __future__ import annotations

import pytest

from backend.app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def test_empty_kpi(client):
    response = client.get("/api/v1/reports/kpi")
    assert response.status_code == 200
    data = response.get_json()["data"]
    assert data["assignmentStatus"] == {}
    assert data["equipmentUtilization"] == []


def test_kpi_reflects_scheduling(client):
    project_id = client.post(
        "/api/v1/projects", json={"projectCode": "PRJ-1", "name": "Proj"}
    ).get_json()["data"]["id"]
    eq_id = client.post(
        "/api/v1/equipment",
        json={"equipmentCode": "EQ-1", "name": "M", "capabilities": ["pcr"]},
    ).get_json()["data"]["id"]
    workflow_id = client.post(
        "/api/v1/workflow-definitions",
        json={
            "workflowCode": "WF-1",
            "name": "PCR",
            "projectId": project_id,
            "operations": [{"operationType": "amplify", "duration": 3, "equipmentIds": [eq_id]}],
        },
    ).get_json()["data"]["id"]
    plan_id = client.post(
        "/api/v1/plans", json={"planningHorizon": "2026-W33", "name": "P"}
    ).get_json()["data"]["id"]
    version_id = client.post(f"/api/v1/plans/{plan_id}/versions").get_json()["data"]["id"]
    base = f"/api/v1/plans/{plan_id}/versions/{version_id}"
    client.post(f"{base}/generate-instances", json={"workflowDefinitionId": workflow_id})
    client.post(f"{base}/schedule-instances")

    data = client.get("/api/v1/reports/kpi").get_json()["data"]
    assert data["assignmentStatus"].get("pending") == 1
    util = data["equipmentUtilization"]
    assert len(util) == 1
    assert util[0]["assignmentCount"] == 1
    assert util[0]["busyTime"] == 3
