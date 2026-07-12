"""Workflow Definition API tests."""

from __future__ import annotations

import pytest

from backend.app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def _project_id(client):
    return client.post(
        "/api/v1/projects", json={"projectCode": "PRJ-1", "name": "Proj"}
    ).get_json()["data"]["id"]


def test_create_workflow_with_operations(client):
    response = client.post(
        "/api/v1/workflow-definitions",
        json={
            "workflowCode": "WF-001",
            "name": "Sample Prep",
            "projectId": _project_id(client),
            "operations": [
                {"operationType": "extract", "duration": 3, "gelatinType": "A"},
                {
                    "operationType": "amplify",
                    "duration": 2,
                    "dependsOn": ["extract"],
                },
            ],
        },
    )

    assert response.status_code == 201
    data = response.get_json()["data"]
    assert data["workflowCode"] == "WF-001"
    assert len(data["operations"]) == 2
    assert data["operations"][0]["operationType"] == "extract"
    assert data["operations"][0]["gelatinType"] == "A"
    assert data["operations"][1]["dependsOn"] == ["extract"]


def test_list_workflow_definitions(client):
    client.post(
        "/api/v1/workflow-definitions",
        json={"workflowCode": "WF-002", "name": "Assay", "projectId": _project_id(client)},
    )

    listing = client.get("/api/v1/workflow-definitions")
    assert listing.status_code == 200
    body = listing.get_json()
    assert body["meta"]["total"] == 1
    assert body["data"][0]["name"] == "Assay"


def test_create_workflow_requires_code(client):
    response = client.post("/api/v1/workflow-definitions", json={"name": "No code"})
    assert response.status_code == 422
    assert response.get_json()["error"]["code"] == "VALIDATION_FAILED"


def test_update_workflow_edits_name_and_methods_preserving_ids(client):
    pid = _project_id(client)
    created = client.post(
        "/api/v1/workflow-definitions",
        json={
            "workflowCode": "WF-1",
            "name": "Old",
            "projectId": pid,
            "operations": [
                {"operationType": "SMDP", "duration": 2},
                {"operationType": "SAP", "duration": 3},
            ],
        },
    ).get_json()["data"]
    wid = created["id"]
    smdp_id = next(o["id"] for o in created["operations"] if o["operationType"] == "SMDP")

    updated = client.put(
        f"/api/v1/workflow-definitions/{wid}",
        json={
            "workflowCode": "WF-1",
            "name": "New",
            "projectId": pid,
            "operations": [
                {"operationType": "SMDP", "duration": 5},  # edited, same type
                {"operationType": "CMDP", "duration": 1},  # new method
            ],  # SAP removed
        },
    )
    assert updated.status_code == 200
    data = updated.get_json()["data"]
    assert data["name"] == "New"
    types = {o["operationType"] for o in data["operations"]}
    assert types == {"SMDP", "CMDP"}
    # SMDP kept its id (so equipment bindings / demand lines survive) and new duration.
    smdp = next(o for o in data["operations"] if o["operationType"] == "SMDP")
    assert smdp["id"] == smdp_id
    assert smdp["duration"] == 5


def test_update_missing_workflow_is_404(client):
    pid = _project_id(client)
    resp = client.put(
        "/api/v1/workflow-definitions/nope",
        json={"workflowCode": "X", "name": "Y", "projectId": pid, "operations": []},
    )
    assert resp.status_code == 404
