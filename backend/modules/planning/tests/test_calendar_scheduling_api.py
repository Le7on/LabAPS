"""End-to-end test: equipment availability windows honored by instance scheduling.

Verifies calendar data flows: Equipment.availability -> Planning Context snapshot
-> schedule-instances resource windows -> solver placement.
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


def test_scheduling_honors_equipment_availability_window(client):
    project_id = client.post(
        "/api/v1/projects", json={"projectCode": "PRJ-1", "name": "Proj"}
    ).get_json()["data"]["id"]
    # Equipment available only in [10, 20).
    eq_id = client.post(
        "/api/v1/equipment",
        json={
            "equipmentCode": "EQ-1",
            "name": "Windowed",
            "capabilities": ["pcr"],
            "availability": [[10, 20]],
        },
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
    scheduled = client.post(f"{base}/schedule-instances")

    assert scheduled.status_code == 200
    body = scheduled.get_json()
    assert body["meta"]["feasible"] is True
    assignment = body["data"]["assignments"][0]
    # The operation must be placed inside the [10, 20) window.
    assert assignment["start"] >= 10
    assert assignment["end"] <= 20
