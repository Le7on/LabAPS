"""Global resource date availability (ADR-021): maintenance/leave excludes days.

A machine's global unavailable dates keep work off those days (or make it
infeasible when that machine is the only option and no other day is free).
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


def _setup(client, start="2026-08-10", end="2026-08-12"):
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
            "name": "W",
            "projectId": project_id,
            "operations": [{"operationType": "run", "duration": 1, "equipmentIds": [eq_id]}],
        },
    ).get_json()["data"]["id"]
    plan_id = client.post(
        "/api/v1/plans",
        json={
            "name": "P",
            "planningHorizon": "2026-W33",
            "startDate": start,
            "endDate": end,
            "shiftMode": "single",
        },
    ).get_json()["data"]["id"]
    return eq_id, workflow_id, plan_id


def _schedule(client, plan_id, workflow_id):
    version_id = client.post(f"/api/v1/plans/{plan_id}/versions").get_json()["data"]["id"]
    base = f"/api/v1/plans/{plan_id}/versions/{version_id}"
    client.post(f"{base}/generate-instances", json={"workflowDefinitionId": workflow_id})
    return client.post(f"{base}/schedule-instances").get_json()


def test_equipment_maintenance_keeps_work_off_that_day(client):
    eq_id, workflow_id, plan_id = _setup(client)
    # Machine under maintenance on the first day (2026-08-10).
    client.post(
        f"/api/v1/equipment/{eq_id}/unavailable-dates",
        json={"unavailableDates": ["2026-08-10"]},
    )
    body = _schedule(client, plan_id, workflow_id)
    assert body["meta"]["feasible"] is True
    a = body["data"]["assignments"][0]
    assert not a["startAt"].startswith("2026-08-10")


def test_full_maintenance_leaves_single_day_plan_unscheduled(client):
    eq_id, workflow_id, plan_id = _setup(client, start="2026-08-10", end="2026-08-10")
    client.post(
        f"/api/v1/equipment/{eq_id}/unavailable-dates",
        json={"unavailableDates": ["2026-08-10"]},
    )
    body = _schedule(client, plan_id, workflow_id)
    # The only machine is down and it's a single day: nothing can be placed, so
    # the run succeeds with zero assignments (the op is a conflict).
    assert body["meta"]["feasible"] is True
    assert body["data"]["assignments"] == []
