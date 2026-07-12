"""Plan demand-line API tests (ADR-020): PI requests workflow rounds on a date."""

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
    workflow = client.post(
        "/api/v1/workflow-definitions",
        json={
            "workflowCode": "SMDP",
            "name": "SMDP",
            "projectId": project_id,
            "operations": [{"operationType": "run", "duration": 1}],
        },
    ).get_json()["data"]
    workflow_id = workflow["id"]
    method_id = workflow["operations"][0]["id"]
    plan_id = client.post(
        "/api/v1/plans",
        json={
            "planningHorizon": "2026-W33",
            "name": "PI plan",
            "startDate": "2026-08-10",
            "endDate": "2026-08-20",
        },
    ).get_json()["data"]["id"]
    return workflow_id, method_id, plan_id


def test_add_and_list_demand_line(client):
    workflow_id, method_id, plan_id = _setup(client)
    created = client.post(
        f"/api/v1/plans/{plan_id}/demand-lines",
        json={
            "workflowDefinitionId": workflow_id,
            "operationDefinitionId": method_id,
            "rounds": 3,
            "targetDate": "2026-08-12",
        },
    )
    assert created.status_code == 201
    assert created.get_json()["data"]["rounds"] == 3

    plan = client.get(f"/api/v1/plans/{plan_id}").get_json()["data"]
    assert len(plan["demandLines"]) == 1
    assert plan["demandLines"][0]["targetDate"] == "2026-08-12"
    assert plan["demandLines"][0]["operationDefinitionId"] == method_id


def test_demand_line_date_must_be_in_plan_range(client):
    workflow_id, method_id, plan_id = _setup(client)
    resp = client.post(
        f"/api/v1/plans/{plan_id}/demand-lines",
        json={
            "workflowDefinitionId": workflow_id,
            "operationDefinitionId": method_id,
            "rounds": 1,
            "targetDate": "2026-09-01",
        },
    )
    assert resp.status_code == 422


def test_remove_demand_line(client):
    workflow_id, method_id, plan_id = _setup(client)
    line_id = client.post(
        f"/api/v1/plans/{plan_id}/demand-lines",
        json={
            "workflowDefinitionId": workflow_id,
            "operationDefinitionId": method_id,
            "rounds": 1,
            "targetDate": "2026-08-12",
        },
    ).get_json()["data"]["id"]

    assert client.delete(f"/api/v1/plans/{plan_id}/demand-lines/{line_id}").status_code == 200
    plan = client.get(f"/api/v1/plans/{plan_id}").get_json()["data"]
    assert plan["demandLines"] == []
