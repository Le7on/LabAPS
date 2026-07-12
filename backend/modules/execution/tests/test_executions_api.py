"""API tests for the assignment execution lifecycle."""

from __future__ import annotations

import pytest

from backend.app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def _scheduled_published_assignment(client):
    """Set up a published plan version with one ready assignment; return its id."""
    project_id = client.post(
        "/api/v1/projects", json={"projectCode": "PRJ-1", "name": "Proj"}
    ).get_json()["data"]["id"]
    eq_id = client.post(
        "/api/v1/equipment",
        json={"equipmentCode": "EQ-1", "name": "M", "capabilities": ["pcr"]},
    ).get_json()["data"]["id"]
    workflow_id = client.post(
        "/api/v1/workflow-definitions",
        json={
            "workflowCode": "WF-1",
            "name": "PCR",
            "projectId": project_id,
            "operations": [{"operationType": "amplify", "duration": 3, "equipmentIds": [eq_id]}],
        },
    ).get_json()["data"]["id"]
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
    client.post(f"{base}/schedule-instances")
    client.post(f"{base}/review")
    client.post(f"{base}/publish")

    assignment = client.get(f"{base}/assignments").get_json()["data"][0]
    return assignment


def test_publish_marks_assignments_ready(client):
    assignment = _scheduled_published_assignment(client)
    assert assignment["status"] == "ready"


def test_start_then_complete(client):
    assignment = _scheduled_published_assignment(client)
    aid = assignment["id"]

    started = client.post(f"/api/v1/executions/{aid}/start")
    assert started.status_code == 200
    assert started.get_json()["data"]["status"] == "running"

    completed = client.post(f"/api/v1/executions/{aid}/complete")
    assert completed.status_code == 200
    assert completed.get_json()["data"]["status"] == "completed"


def test_cannot_complete_before_start(client):
    assignment = _scheduled_published_assignment(client)
    response = client.post(f"/api/v1/executions/{assignment['id']}/complete")
    assert response.status_code == 409
    assert response.get_json()["error"]["code"] == "CONFLICT"


def test_fail_requires_reason(client):
    assignment = _scheduled_published_assignment(client)
    aid = assignment["id"]
    client.post(f"/api/v1/executions/{aid}/start")

    no_reason = client.post(f"/api/v1/executions/{aid}/fail", json={})
    assert no_reason.status_code == 422

    with_reason = client.post(f"/api/v1/executions/{aid}/fail", json={"reason": "instrument error"})
    assert with_reason.status_code == 200
    assert with_reason.get_json()["data"]["status"] == "failed"
    assert with_reason.get_json()["data"]["reason"] == "instrument error"


def test_execution_history_records_transitions(client):
    assignment = _scheduled_published_assignment(client)
    aid = assignment["id"]
    client.post(f"/api/v1/executions/{aid}/start")
    client.post(f"/api/v1/executions/{aid}/complete")

    history = client.get(f"/api/v1/executions/{aid}/history")
    assert history.status_code == 200
    body = history.get_json()
    # Two transitions recorded: ready->running (start), running->completed (complete).
    assert body["meta"]["total"] == 2
    actions = [r["action"] for r in body["data"]]
    assert actions == ["start", "complete"]
    assert body["data"][0]["fromStatus"] == "ready"
    assert body["data"][1]["toStatus"] == "completed"
