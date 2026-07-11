"""Per-plan resource availability: get/set and effect on scheduling."""

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
    project_id = client.post(
        "/api/v1/projects", json={"projectCode": "PRJ-1", "name": "Proj"}
    ).get_json()["data"]["id"]
    eq_id = client.post(
        "/api/v1/equipment", json={"equipmentCode": "EQ-1", "name": "M"}
    ).get_json()["data"]["id"]
    workflow_id = client.post(
        "/api/v1/workflow-definitions",
        json={
            "workflowCode": "WF-1",
            "name": "PCR",
            "projectId": project_id,
            "operations": [{"operationType": "amplify", "duration": 2, "equipmentIds": [eq_id]}],
        },
    ).get_json()["data"]["id"]
    plan_id = client.post(
        "/api/v1/plans", json={"planningHorizon": "2026-W33", "name": "P"}
    ).get_json()["data"]["id"]
    return project_id, eq_id, workflow_id, plan_id


def test_availability_defaults_to_available(client):
    _, eq_id, _, plan_id = _setup(client)
    data = client.get(f"/api/v1/plans/{plan_id}/availability").get_json()["data"]
    eq = next(e for e in data["equipment"] if e["id"] == eq_id)
    assert eq["available"] is True


def test_set_and_read_back_unavailable(client):
    _, eq_id, _, plan_id = _setup(client)
    resp = client.post(
        f"/api/v1/plans/{plan_id}/availability",
        json={"kind": "equipment", "resourceId": eq_id, "available": False},
    )
    assert resp.status_code == 200

    data = client.get(f"/api/v1/plans/{plan_id}/availability").get_json()["data"]
    eq = next(e for e in data["equipment"] if e["id"] == eq_id)
    assert eq["available"] is False


def test_unavailable_equipment_is_excluded_and_makes_infeasible(client):
    _, eq_id, workflow_id, plan_id = _setup(client)
    # The only equipment that can run the method is marked unavailable for the plan.
    client.post(
        f"/api/v1/plans/{plan_id}/availability",
        json={"kind": "equipment", "resourceId": eq_id, "available": False},
    )
    version_id = client.post(f"/api/v1/plans/{plan_id}/versions").get_json()["data"]["id"]
    base = f"/api/v1/plans/{plan_id}/versions/{version_id}"
    client.post(f"{base}/generate-instances", json={"workflowDefinitionId": workflow_id})
    scheduled = client.post(f"{base}/schedule-instances")
    assert scheduled.status_code == 200
    assert scheduled.get_json()["meta"]["feasible"] is False


def test_available_equipment_schedules_fine(client):
    _, eq_id, workflow_id, plan_id = _setup(client)
    version_id = client.post(f"/api/v1/plans/{plan_id}/versions").get_json()["data"]["id"]
    base = f"/api/v1/plans/{plan_id}/versions/{version_id}"
    client.post(f"{base}/generate-instances", json={"workflowDefinitionId": workflow_id})
    scheduled = client.post(f"{base}/schedule-instances")
    assert scheduled.get_json()["meta"]["feasible"] is True
