"""Integration test: schedule from a persisted Workflow Definition + Equipment.

Exercises the Laboratory -> Planning -> Scheduling path through the real
OR-Tools solver: operations come from a workflow definition, resources from the
active equipment pool.
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


def _capture_op_ids(workflow_data):
    return {op["operationType"]: op["id"] for op in workflow_data["operations"]}


def test_schedule_from_workflow_uses_persisted_data(client):
    # Equipment pool: only eqB can do "pcr".
    client.post(
        "/api/v1/equipment",
        json={"equipmentCode": "EQ-A", "name": "Shaker", "capabilities": ["spin"]},
    )
    client.post(
        "/api/v1/equipment",
        json={"equipmentCode": "EQ-B", "name": "Thermocycler", "capabilities": ["pcr"]},
    )
    eq_b_id = client.get("/api/v1/equipment").get_json()["data"][1]["id"]

    # Workflow with one pcr operation.
    wf = client.post(
        "/api/v1/workflow-definitions",
        json={
            "workflowCode": "WF-1",
            "name": "PCR Prep",
            "operations": [
                {"operationType": "amplify", "duration": 4, "requiredCapability": "pcr"}
            ],
        },
    ).get_json()["data"]
    workflow_id = wf["id"]

    plan_id = client.post(
        "/api/v1/plans", json={"planningHorizon": "2026-W50", "name": "Lab Plan"}
    ).get_json()["data"]["id"]
    version_id = client.post(f"/api/v1/plans/{plan_id}/versions").get_json()["data"]["id"]

    response = client.post(
        f"/api/v1/plans/{plan_id}/versions/{version_id}/schedule-from-workflow",
        json={"workflowDefinitionId": workflow_id},
    )

    assert response.status_code == 200
    body = response.get_json()
    assert body["meta"]["feasible"] is True
    assignment = body["data"]["assignments"][0]
    # The pcr operation must be assigned to the only pcr-capable equipment.
    assert assignment["resourceId"] == eq_b_id


def test_schedule_assigns_equipment_and_staff(client):
    client.post(
        "/api/v1/equipment",
        json={"equipmentCode": "EQ-B", "name": "Thermocycler", "capabilities": ["pcr"]},
    )
    client.post(
        "/api/v1/staff",
        json={"staffCode": "ST-1", "name": "Alice", "skills": ["pcr-operator"]},
    )
    eq_id = client.get("/api/v1/equipment").get_json()["data"][0]["id"]
    st_id = client.get("/api/v1/staff").get_json()["data"][0]["id"]

    workflow_id = client.post(
        "/api/v1/workflow-definitions",
        json={
            "workflowCode": "WF-2",
            "name": "PCR",
            "operations": [
                {
                    "operationType": "amplify",
                    "duration": 3,
                    "requiredCapability": "pcr",
                    "requiredSkill": "pcr-operator",
                }
            ],
        },
    ).get_json()["data"]["id"]

    plan_id = client.post(
        "/api/v1/plans", json={"planningHorizon": "2026-W52", "name": "P"}
    ).get_json()["data"]["id"]
    version_id = client.post(f"/api/v1/plans/{plan_id}/versions").get_json()["data"]["id"]

    response = client.post(
        f"/api/v1/plans/{plan_id}/versions/{version_id}/schedule-from-workflow",
        json={"workflowDefinitionId": workflow_id},
    )

    assert response.status_code == 200
    assignment = response.get_json()["data"]["assignments"][0]
    assert assignment["equipmentId"] == eq_id
    assert assignment["staffId"] == st_id


def test_schedule_from_unknown_workflow_returns_404(client):
    plan_id = client.post(
        "/api/v1/plans", json={"planningHorizon": "2026-W51", "name": "P"}
    ).get_json()["data"]["id"]
    version_id = client.post(f"/api/v1/plans/{plan_id}/versions").get_json()["data"]["id"]

    response = client.post(
        f"/api/v1/plans/{plan_id}/versions/{version_id}/schedule-from-workflow",
        json={"workflowDefinitionId": "does-not-exist"},
    )
    assert response.status_code == 404
