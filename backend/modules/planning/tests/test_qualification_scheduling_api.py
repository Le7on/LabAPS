"""End-to-end test: staff eligibility by project qualification (ADR-017).

A method is performed only by staff qualified for the method's workflow project.
Staff not qualified for that project cannot be assigned, making an
otherwise-schedulable method infeasible.
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


def _project(client, code="PRJ-1"):
    return client.post("/api/v1/projects", json={"projectCode": code, "name": code}).get_json()[
        "data"
    ]["id"]


def _staff_only_workflow(client, project_id):
    # A method with no bound equipment: only staff eligibility gates it.
    return client.post(
        "/api/v1/workflow-definitions",
        json={
            "workflowCode": "WF-1",
            "name": "Run",
            "projectId": project_id,
            "operations": [{"operationType": "run", "duration": 2}],
        },
    ).get_json()["data"]["id"]


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


def test_qualified_staff_is_assigned(client):
    project_id = _project(client)
    client.post(
        "/api/v1/staff",
        json={"staffCode": "ST-1", "name": "Alice", "qualifiedProjectIds": [project_id]},
    )
    staff_id = client.get("/api/v1/staff").get_json()["data"][0]["id"]

    response = _schedule(client, _staff_only_workflow(client, project_id))
    assert response.status_code == 200
    body = response.get_json()
    assert body["meta"]["feasible"] is True
    assert body["data"]["assignments"][0]["staffId"] == staff_id


def test_staff_not_qualified_for_project_is_infeasible(client):
    project_id = _project(client, "PRJ-1")
    other_project = _project(client, "PRJ-2")
    # Staff qualified only for a different project.
    client.post(
        "/api/v1/staff",
        json={"staffCode": "ST-1", "name": "Bob", "qualifiedProjectIds": [other_project]},
    )

    response = _schedule(client, _staff_only_workflow(client, project_id))
    assert response.status_code == 200
    assert response.get_json()["meta"]["feasible"] is False
