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
    # 2-shift method in single mode: day0 09-17 .. day1 09-17.
    assert a["startAt"] == "2026-08-10T09:00:00"
    assert a["endAt"] == "2026-08-11T17:00:00"
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
    # 2-shift method in double mode fits within a single day (06-14, 14-22).
    assert a["startAt"] == "2026-08-10T06:00:00"
    assert a["endAt"] == "2026-08-10T22:00:00"


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
    # Slot 0 = 08-10, slot 1 skips 08-11 -> 08-12. A 2-slot method spans both.
    assert a["startAt"] == "2026-08-10T09:00:00"
    assert a["endAt"] == "2026-08-12T17:00:00"


def test_calendar_too_small_is_infeasible(client):
    workflow_id = _setup_workflow(client)
    # Single mode, one day = one slot, but the method needs two slots.
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
    assert response.get_json()["meta"]["feasible"] is False
