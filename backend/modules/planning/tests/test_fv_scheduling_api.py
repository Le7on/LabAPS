"""FV validity constraint in scheduling (ADR-019).

Every machine must be validated periodically; an FV occupies the machine and a
normal operation cannot run in the FV slot. With FV on, work is pushed past the
FV occupancy; with FV off, work starts at 0.
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


def _run(client, fv_validity):
    project_id = client.post(
        "/api/v1/projects", json={"projectCode": "PRJ-1", "name": "Proj"}
    ).get_json()["data"]["id"]
    eq_id = client.post(
        "/api/v1/equipment",
        json={"equipmentCode": "EQ-1", "name": "M", "fvDuration": 1, "fvValidity": fv_validity},
    ).get_json()["data"]["id"]
    workflow_id = client.post(
        "/api/v1/workflow-definitions",
        json={
            "workflowCode": "WF-1",
            "name": "W",
            "projectId": project_id,
            "operations": [{"operationType": "run", "duration": 2, "equipmentIds": [eq_id]}],
        },
    ).get_json()["data"]["id"]
    plan_id = client.post(
        "/api/v1/plans", json={"planningHorizon": "2026-W33", "name": "P"}
    ).get_json()["data"]["id"]
    version_id = client.post(f"/api/v1/plans/{plan_id}/versions").get_json()["data"]["id"]
    base = f"/api/v1/plans/{plan_id}/versions/{version_id}"
    client.post(f"{base}/generate-instances", json={"workflowDefinitionId": workflow_id})
    return client.post(f"{base}/schedule-instances").get_json()


def test_without_fv_operation_starts_at_zero(client):
    body = _run(client, fv_validity=0)
    assert body["meta"]["feasible"] is True
    assert body["data"]["assignments"][0]["start"] == 0


def test_with_fv_operation_is_pushed_past_the_fv_slot(client):
    # FV occupies slot [0,1); the operation cannot overlap it, so it starts >= 1.
    body = _run(client, fv_validity=10)
    assert body["meta"]["feasible"] is True
    assert body["data"]["assignments"][0]["start"] >= 1
