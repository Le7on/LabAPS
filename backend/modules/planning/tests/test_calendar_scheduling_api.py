"""End-to-end test: equipment date availability honored by instance scheduling.

A plan always has a calendar; marking equipment unavailable on the early days of
the plan must push the operation to a later, available day.
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


def test_scheduling_honors_equipment_date_availability(client):
    project_id = client.post(
        "/api/v1/projects", json={"projectCode": "PRJ-1", "name": "Proj"}
    ).get_json()["data"]["id"]
    eq_id = client.post(
        "/api/v1/equipment",
        json={"equipmentCode": "EQ-1", "name": "M", "fvValidity": 0},
    ).get_json()["data"]["id"]
    workflow_id = client.post(
        "/api/v1/workflow-definitions",
        json={
            "workflowCode": "WF-1",
            "name": "PCR",
            "projectId": project_id,
            "operations": [{"operationType": "amplify", "duration": 1, "equipmentIds": [eq_id]}],
        },
    ).get_json()["data"]["id"]
    plan_id = client.post(
        "/api/v1/plans",
        json={
            "planningHorizon": "2026-W33",
            "name": "P",
            "startDate": "2026-08-10",
            "endDate": "2026-08-14",
            "shiftMode": "single",
        },
    ).get_json()["data"]["id"]
    # Machine down for the first three days; only 08-13/08-14 remain.
    client.post(
        f"/api/v1/plans/{plan_id}/availability",
        json={
            "kind": "equipment",
            "resourceId": eq_id,
            "available": True,
            "unavailableDates": [["2026-08-10", "2026-08-12"]],
        },
    )
    version_id = client.post(f"/api/v1/plans/{plan_id}/versions").get_json()["data"]["id"]
    base = f"/api/v1/plans/{plan_id}/versions/{version_id}"
    client.post(f"{base}/generate-instances", json={"workflowDefinitionId": workflow_id})
    scheduled = client.post(f"{base}/schedule-instances")

    assert scheduled.status_code == 200
    body = scheduled.get_json()
    assert body["meta"]["feasible"] is True
    assignment = body["data"]["assignments"][0]
    # Must land on an available day (08-13 or 08-14), not the down days.
    assert assignment["startAt"][:10] >= "2026-08-13"
