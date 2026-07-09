"""Integration test: generate instances + planning context, then schedule them.

Exercises the deepened core chain: Workflow Definition -> Operation Instances +
Planning Context snapshot -> scheduling against the snapshot (ADR-008).
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


def _setup(client):
    client.post(
        "/api/v1/equipment",
        json={"equipmentCode": "EQ-B", "name": "Thermocycler", "capabilities": ["pcr"]},
    )
    eq_id = client.get("/api/v1/equipment").get_json()["data"][0]["id"]
    workflow_id = client.post(
        "/api/v1/workflow-definitions",
        json={
            "workflowCode": "WF-1",
            "name": "PCR",
            "operations": [
                {"operationType": "amplify", "duration": 3, "requiredCapability": "pcr"}
            ],
        },
    ).get_json()["data"]["id"]
    plan_id = client.post(
        "/api/v1/plans", json={"planningHorizon": "2026-W33", "name": "P"}
    ).get_json()["data"]["id"]
    version_id = client.post(f"/api/v1/plans/{plan_id}/versions").get_json()["data"]["id"]
    return eq_id, workflow_id, plan_id, version_id


def test_generate_then_schedule_instances(client):
    eq_id, workflow_id, plan_id, version_id = _setup(client)
    base = f"/api/v1/plans/{plan_id}/versions/{version_id}"

    generated = client.post(
        f"{base}/generate-instances", json={"workflowDefinitionId": workflow_id}
    )
    assert generated.status_code == 201
    assert generated.get_json()["data"]["operationCount"] == 1

    scheduled = client.post(f"{base}/schedule-instances")
    assert scheduled.status_code == 200
    body = scheduled.get_json()
    assert body["meta"]["feasible"] is True
    assignment = body["data"]["assignments"][0]
    # Scheduled against the snapshot equipment; assigned to the pcr machine.
    assert assignment["equipmentId"] == eq_id

    # Assignments were persisted on the version.
    listing = client.get(f"{base}/assignments").get_json()
    assert listing["meta"]["total"] == 1


def test_schedule_instances_without_generation_is_422(client):
    _, _, plan_id, version_id = _setup(client)
    response = client.post(f"/api/v1/plans/{plan_id}/versions/{version_id}/schedule-instances")
    assert response.status_code == 422
