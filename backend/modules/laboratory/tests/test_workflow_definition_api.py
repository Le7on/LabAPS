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


def test_create_workflow_with_operations(client):
    response = client.post(
        "/api/v1/workflow-definitions",
        json={
            "workflowCode": "WF-001",
            "name": "Sample Prep",
            "operations": [
                {"operationType": "extract", "duration": 3, "requiredCapability": "spin"},
                {
                    "operationType": "amplify",
                    "duration": 2,
                    "requiredSkill": "pcr",
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
    assert data["operations"][1]["requiredSkill"] == "pcr"
    assert data["operations"][1]["dependsOn"] == ["extract"]


def test_list_workflow_definitions(client):
    client.post(
        "/api/v1/workflow-definitions",
        json={"workflowCode": "WF-002", "name": "Assay"},
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
