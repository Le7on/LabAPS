"""Integration test: plan calendar maps scheduling to real dates + shifts (ADR-016)."""

from __future__ import annotations

import pytest

from backend.app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def _setup_workflow(client):
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
            "operations": [{"operationType": "run", "duration": 2, "equipmentIds": [eq_id]}],
        },
    ).get_json()["data"]["id"]
    return workflow_id


def _schedule(client, plan_payload, workflow_id):
    plan_id = client.post("/api/v1/plans", json=plan_payload).get_json()["data"]["id"]
    version_id = client.post(f"/api/v1/plans/{plan_id}/versions").get_json()["data"]["id"]
    base = f"/api/v1/plans/{plan_id}/versions/{version_id}"
    client.post(f"{base}/generate-instances", json={"workflowDefinitionId": workflow_id})
    return client.post(f"{base}/schedule-instances"), base


def test_single_shift_calendar_maps_dates(client):
    workflow_id = _setup_workflow(client)
    response, _ = _schedule(
        client,
        {
            "planningHorizon": "2026-W33",
            "name": "P",
            "startDate": "2026-08-10",
            "endDate": "2026-08-20",
            "shiftMode": "single",
        },
        workflow_id,
    )
    assert response.status_code == 200
    assert response.get_json()["meta"]["feasible"] is True
    a = response.get_json()["data"]["assignments"][0]
    # 2-hour method (single shift starts 09:00) -> 09:00–11:00 on day 0.
    assert a["startAt"] == "2026-08-10T09:00:00"
    assert a["endAt"] == "2026-08-10T11:00:00"
    assert a["shift"] == "Shift1"


def test_double_shift_calendar_two_slots_per_day(client):
    workflow_id = _setup_workflow(client)
    response, _ = _schedule(
        client,
        {
            "planningHorizon": "2026-W33",
            "name": "P",
            "startDate": "2026-08-10",
            "endDate": "2026-08-20",
            "shiftMode": "double",
        },
        workflow_id,
    )
    a = response.get_json()["data"]["assignments"][0]
    # 2-hour method in double mode starts at the first shift's 06:00 -> 06:00–08:00.
    assert a["startAt"] == "2026-08-10T06:00:00"
    assert a["endAt"] == "2026-08-10T08:00:00"


def test_skipped_dates_are_excluded(client):
    workflow_id = _setup_workflow(client)
    response, _ = _schedule(
        client,
        {
            "planningHorizon": "2026-W33",
            "name": "P",
            "startDate": "2026-08-10",
            "endDate": "2026-08-20",
            "shiftMode": "single",
            "skippedDates": ["2026-08-11"],
        },
        workflow_id,
    )
    a = response.get_json()["data"]["assignments"][0]
    # 08-11 is skipped (no hours). The 2-hour method fits on 08-10; nothing lands
    # on the skipped day.
    assert a["startAt"].startswith("2026-08-10")
    assert not a["startAt"].startswith("2026-08-11")
    assert not a["endAt"].startswith("2026-08-11")


def test_method_longer_than_available_hours_is_unscheduled(client):
    # A method needing more hours than the single day offers (8h) can't be placed.
    project_id = client.post(
        "/api/v1/projects", json={"projectCode": "PRJ-2", "name": "Proj2"}
    ).get_json()["data"]["id"]
    eq_id = client.post(
        "/api/v1/equipment",
        json={"equipmentCode": "EQ-2", "name": "M2", "fvValidity": 0},
    ).get_json()["data"]["id"]
    workflow_id = client.post(
        "/api/v1/workflow-definitions",
        json={
            "workflowCode": "WF-2",
            "name": "W2",
            "projectId": project_id,
            "operations": [{"operationType": "long", "duration": 20, "equipmentIds": [eq_id]}],
        },
    ).get_json()["data"]["id"]
    response, _ = _schedule(
        client,
        {
            "planningHorizon": "2026-W33",
            "name": "P",
            "startDate": "2026-08-10",
            "endDate": "2026-08-10",
            "shiftMode": "single",
        },
        workflow_id,
    )
    assert response.status_code == 200
    # Partial scheduling (ADR-023): unplaceable -> feasible run, zero assignments.
    assert response.get_json()["meta"]["feasible"] is True
    assert response.get_json()["data"]["assignments"] == []
