"""Multi-plan unified schedule run (ADR-020/021)."""

from __future__ import annotations

import pytest

from backend.app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def _lab(client):
    project_id = client.post(
        "/api/v1/projects", json={"projectCode": "PRJ-1", "name": "Proj"}
    ).get_json()["data"]["id"]
    eq_id = client.post(
        "/api/v1/equipment",
        json={"equipmentCode": "EQ-1", "name": "M", "fvValidity": 0},
    ).get_json()["data"]["id"]
    workflow = client.post(
        "/api/v1/workflow-definitions",
        json={
            "workflowCode": "SMDP",
            "name": "SMDP",
            "projectId": project_id,
            "operations": [{"operationType": "run", "duration": 1, "equipmentIds": [eq_id]}],
        },
    ).get_json()["data"]
    # A qualified operator.
    client.post(
        "/api/v1/staff",
        json={"staffCode": "ST-1", "name": "Alice", "qualifiedProjectIds": [project_id]},
    )
    return workflow["id"], workflow["operations"][0]["id"]


def _plan(client, name, start, end, shift_mode="double"):
    return client.post(
        "/api/v1/plans",
        json={
            "name": name,
            "planningHorizon": "2026-W33",
            "startDate": start,
            "endDate": end,
            "shiftMode": shift_mode,
        },
    ).get_json()["data"]["id"]


def _line(client, plan_id, workflow_id, method_id, rounds, date):
    client.post(
        f"/api/v1/plans/{plan_id}/demand-lines",
        json={
            "workflowDefinitionId": workflow_id,
            "operationDefinitionId": method_id,
            "rounds": rounds,
            "targetDate": date,
        },
    )


def test_two_plans_scheduled_together_on_target_days(client):
    workflow_id, method_id = _lab(client)
    p1 = _plan(client, "PI-A", "2026-08-10", "2026-08-15")
    p2 = _plan(client, "PI-B", "2026-08-10", "2026-08-15")
    _line(client, p1, workflow_id, method_id, 2, "2026-08-11")
    _line(client, p2, workflow_id, method_id, 1, "2026-08-13")

    resp = client.post("/api/v1/schedule", json={"planIds": [p1, p2], "shiftMode": "double"})
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["meta"]["feasible"] is True
    days = sorted(a["startAt"][:10] for a in body["data"]["assignments"])
    # 2 rounds on the 11th + 1 round on the 13th = 3 operations on those days.
    assert days == ["2026-08-11", "2026-08-11", "2026-08-13"]


def test_schedule_requires_plan_ids(client):
    resp = client.post("/api/v1/schedule", json={"planIds": []})
    assert resp.status_code == 422


def test_overbooked_day_schedules_what_it_can_and_reports_conflicts(client):
    # One machine, single shift (1 slot/day), but 3 rounds demanded on one day:
    # one round schedules, the other two surface as conflicts (ADR-023).
    workflow_id, method_id = _lab(client)
    plan_id = _plan(client, "PI", "2026-08-11", "2026-08-11", shift_mode="single")
    _line(client, plan_id, workflow_id, method_id, 3, "2026-08-11")

    resp = client.post("/api/v1/schedule", json={"planIds": [plan_id], "shiftMode": "single"})
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["meta"]["feasible"] is True
    assert len(body["data"]["assignments"]) == 1
    conflicts = body["data"]["conflicts"]
    assert len(conflicts) == 1
    assert conflicts[0]["unscheduledRounds"] == 2
    assert conflicts[0]["targetDate"] == "2026-08-11"
