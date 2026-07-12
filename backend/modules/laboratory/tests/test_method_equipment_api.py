"""Tests for Method (=Stage) equipment binding (ADR-015).

A workflow's methods bind equipment directly (replacing capability matching);
the scheduler then restricts each method to its bound equipment.
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


def _project(client):
    return client.post(
        "/api/v1/projects", json={"projectCode": "PRJ-1", "name": "Proj"}
    ).get_json()["data"]["id"]


def _equipment(client, code="EQ-1"):
    return client.post("/api/v1/equipment", json={"equipmentCode": code, "name": code}).get_json()[
        "data"
    ]["id"]


def test_workflow_method_binds_equipment(client):
    project_id = _project(client)
    eq_id = _equipment(client)
    created = client.post(
        "/api/v1/workflow-definitions",
        json={
            "workflowCode": "WF-1",
            "name": "W",
            "projectId": project_id,
            "operations": [
                {
                    "operationType": "run",
                    "duration": 2,
                    "gelatinType": "TypeA",
                    "equipmentIds": [eq_id],
                }
            ],
        },
    )
    assert created.status_code == 201
    method = created.get_json()["data"]["operations"][0]
    assert method["gelatinType"] == "TypeA"
    assert method["equipmentIds"] == [eq_id]


def test_workflow_rejects_unknown_equipment(client):
    project_id = _project(client)
    response = client.post(
        "/api/v1/workflow-definitions",
        json={
            "workflowCode": "WF-1",
            "name": "W",
            "projectId": project_id,
            "operations": [{"operationType": "run", "duration": 1, "equipmentIds": ["nope"]}],
        },
    )
    assert response.status_code == 422


def _schedule(client, workflow_id):
    plan_id = client.post(
        "/api/v1/plans",
        json={
            "startDate": "2026-08-10",
            "endDate": "2026-08-20",
            "planningHorizon": "2026-W33",
            "name": "P",
        },
    ).get_json()["data"]["id"]
    version_id = client.post(f"/api/v1/plans/{plan_id}/versions").get_json()["data"]["id"]
    base = f"/api/v1/plans/{plan_id}/versions/{version_id}"
    client.post(f"{base}/generate-instances", json={"workflowDefinitionId": workflow_id})
    return client.post(f"{base}/schedule-instances")


def test_scheduling_assigns_only_bound_equipment(client):
    project_id = _project(client)
    bound = _equipment(client, "EQ-BOUND")
    _equipment(client, "EQ-OTHER")  # exists but not bound
    workflow_id = client.post(
        "/api/v1/workflow-definitions",
        json={
            "workflowCode": "WF-1",
            "name": "W",
            "projectId": project_id,
            "operations": [{"operationType": "run", "duration": 2, "equipmentIds": [bound]}],
        },
    ).get_json()["data"]["id"]

    response = _schedule(client, workflow_id)
    assert response.status_code == 200
    body = response.get_json()
    assert body["meta"]["feasible"] is True
    # The method is assigned exactly its bound equipment, never the other one.
    assert body["data"]["assignments"][0]["equipmentId"] == bound


def test_duration_is_number_of_shifts(client):
    # 1 shift = 1 scheduler time unit: a 3-shift method spans 3 units.
    project_id = _project(client)
    eq_id = _equipment(client)
    workflow_id = client.post(
        "/api/v1/workflow-definitions",
        json={
            "workflowCode": "WF-1",
            "name": "W",
            "projectId": project_id,
            "operations": [{"operationType": "run", "duration": 3, "equipmentIds": [eq_id]}],
        },
    ).get_json()["data"]["id"]

    body = _schedule(client, workflow_id).get_json()
    assignment = body["data"]["assignments"][0]
    assert assignment["end"] - assignment["start"] == 3


# --- Equipment side: applicable projects + method binding (ADR-018) ---------


def _workflow_with_method(client, project_id):
    wf = client.post(
        "/api/v1/workflow-definitions",
        json={
            "workflowCode": "WF-1",
            "name": "W",
            "projectId": project_id,
            "operations": [{"operationType": "run", "duration": 1}],
        },
    ).get_json()["data"]
    return wf["operations"][0]["id"]


def test_equipment_applicable_projects_and_methods(client):
    project_id = _project(client)
    method_id = _workflow_with_method(client, project_id)
    created = client.post(
        "/api/v1/equipment",
        json={
            "equipmentCode": "EQ-1",
            "name": "Cycler",
            "applicableProjectIds": [project_id],
            "methodIds": [method_id],
        },
    )
    assert created.status_code == 201
    data = created.get_json()["data"]
    assert data["applicableProjectIds"] == [project_id]
    assert data["methodIds"] == [method_id]

    listed = client.get("/api/v1/equipment").get_json()["data"][0]
    assert listed["applicableProjectIds"] == [project_id]
    assert listed["methodIds"] == [method_id]


def test_equipment_rejects_unknown_project(client):
    response = client.post(
        "/api/v1/equipment",
        json={"equipmentCode": "EQ-1", "name": "X", "applicableProjectIds": ["nope"]},
    )
    assert response.status_code == 422


def test_equipment_rejects_unknown_method(client):
    project_id = _project(client)
    response = client.post(
        "/api/v1/equipment",
        json={
            "equipmentCode": "EQ-1",
            "name": "X",
            "applicableProjectIds": [project_id],
            "methodIds": ["nope"],
        },
    )
    assert response.status_code == 422
