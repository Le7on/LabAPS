"""Overtime scheduling (ADR-022): a weekend day is schedulable only for resources
that signed up for overtime that day."""

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
    method_id = workflow["operations"][0]["id"]
    st_id = client.post(
        "/api/v1/staff",
        json={"staffCode": "ST-1", "name": "Alice", "qualifiedProjectIds": [project_id]},
    ).get_json()["data"]["id"]
    # A plan whose only working option is a Saturday (2026-08-15 is a Saturday).
    plan_id = client.post(
        "/api/v1/plans",
        json={
            "name": "P",
            "planningHorizon": "2026-W33",
            "startDate": "2026-08-15",
            "endDate": "2026-08-15",
            "shiftMode": "single",
        },
    ).get_json()["data"]["id"]
    client.post(
        f"/api/v1/plans/{plan_id}/demand-lines",
        json={
            "workflowDefinitionId": workflow["id"],
            "operationDefinitionId": method_id,
            "rounds": 1,
            "targetDate": "2026-08-15",
        },
    )
    return eq_id, st_id, plan_id


def test_weekend_is_not_workable_without_overtime(client):
    _eq, _st, plan_id = _setup(client)
    resp = client.post("/api/v1/schedule", json={"planIds": [plan_id]})
    # A Saturday-only plan with no overtime has no working days at all.
    assert resp.status_code == 422
    assert "no working days" in resp.get_json()["error"]["message"].lower()


def test_weekend_works_when_both_resources_sign_up_overtime(client):
    eq_id, st_id, plan_id = _setup(client)
    for kind, rid in (("equipment", eq_id), ("staff", st_id)):
        client.post(
            f"/api/v1/{kind}/{rid}/unavailable-dates",
            json={"unavailableDates": [], "overtimeDates": ["2026-08-15"]},
        )
    resp = client.post("/api/v1/schedule", json={"planIds": [plan_id]})
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["meta"]["feasible"] is True
    assert body["data"]["assignments"][0]["startAt"][:10] == "2026-08-15"
