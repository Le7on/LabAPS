"""Per-plan date-based availability: leave / breakdown excludes specific days.

Uses a calendar plan so integer slots map to real dates; marking a resource
unavailable on a date must keep work off that date (or make it infeasible when
that resource is the only option and no other day is free).
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


def _setup(client, duration=1):
    project_id = client.post(
        "/api/v1/projects", json={"projectCode": "PRJ-1", "name": "Proj"}
    ).get_json()["data"]["id"]
    # FV off so the machine isn't consumed by validation in these tiny horizons.
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
            "operations": [{"operationType": "run", "duration": duration, "equipmentIds": [eq_id]}],
        },
    ).get_json()["data"]["id"]
    plan_id = client.post(
        "/api/v1/plans",
        json={
            "name": "P",
            "planningHorizon": "2026-W33",
            "startDate": "2026-08-10",
            "endDate": "2026-08-12",
            "shiftMode": "single",
        },
    ).get_json()["data"]["id"]
    return project_id, eq_id, workflow_id, plan_id


def _schedule(client, plan_id, workflow_id):
    version_id = client.post(f"/api/v1/plans/{plan_id}/versions").get_json()["data"]["id"]
    base = f"/api/v1/plans/{plan_id}/versions/{version_id}"
    client.post(f"{base}/generate-instances", json={"workflowDefinitionId": workflow_id})
    return client.post(f"{base}/schedule-instances").get_json()


def test_equipment_breakdown_keeps_work_off_that_day(client):
    _, eq_id, workflow_id, plan_id = _setup(client)
    # Machine down on the first day (2026-08-10).
    client.post(
        f"/api/v1/plans/{plan_id}/availability",
        json={
            "kind": "equipment",
            "resourceId": eq_id,
            "available": True,
            "unavailableDates": [["2026-08-10", "2026-08-10"]],
        },
    )
    body = _schedule(client, plan_id, workflow_id)
    assert body["meta"]["feasible"] is True
    a = body["data"]["assignments"][0]
    # The one operation must not land on the down day.
    assert not a["startAt"].startswith("2026-08-10")


def test_full_breakdown_makes_single_day_plan_infeasible(client):
    # One-day plan; the only machine is down that day -> nowhere to run.
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
            "startDate": "2026-08-10",
            "endDate": "2026-08-10",
            "shiftMode": "single",
        },
    ).get_json()["data"]["id"]
    client.post(
        f"/api/v1/plans/{plan_id}/availability",
        json={
            "kind": "equipment",
            "resourceId": eq_id,
            "available": True,
            "unavailableDates": [["2026-08-10", "2026-08-10"]],
        },
    )
    body = _schedule(client, plan_id, workflow_id)
    assert body["meta"]["feasible"] is False
