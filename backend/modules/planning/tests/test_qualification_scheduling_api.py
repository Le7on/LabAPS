"""End-to-end test: qualification constraint in instance scheduling.

An operation requiring a qualification is only assignable to staff holding a
currently-valid qualification (in addition to any required skill). An expired
qualification makes the operation infeasible.
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


def _workflow_with_qualification(client):
    return client.post(
        "/api/v1/workflow-definitions",
        json={
            "workflowCode": "WF-1",
            "name": "GMP run",
            "operations": [
                {
                    "operationType": "run",
                    "duration": 2,
                    "requiredSkill": "pcr",
                    "requiredQualification": "gmp",
                }
            ],
        },
    ).get_json()["data"]["id"]


def _schedule(client, workflow_id):
    plan_id = client.post(
        "/api/v1/plans", json={"planningHorizon": "2026-W33", "name": "P"}
    ).get_json()["data"]["id"]
    version_id = client.post(f"/api/v1/plans/{plan_id}/versions").get_json()["data"]["id"]
    base = f"/api/v1/plans/{plan_id}/versions/{version_id}"
    client.post(f"{base}/generate-instances", json={"workflowDefinitionId": workflow_id})
    return client.post(f"{base}/schedule-instances")


def test_qualified_staff_is_assigned(client):
    client.post(
        "/api/v1/staff",
        json={
            "staffCode": "ST-1",
            "name": "Alice",
            "skills": ["pcr"],
            "qualifications": {"gmp": "2099-12-31"},
        },
    )
    staff_id = client.get("/api/v1/staff").get_json()["data"][0]["id"]

    response = _schedule(client, _workflow_with_qualification(client))
    assert response.status_code == 200
    body = response.get_json()
    assert body["meta"]["feasible"] is True
    assert body["data"]["assignments"][0]["staffId"] == staff_id


def test_expired_qualification_makes_it_infeasible(client):
    # Has the skill, but the qualification expired in the past.
    client.post(
        "/api/v1/staff",
        json={
            "staffCode": "ST-1",
            "name": "Bob",
            "skills": ["pcr"],
            "qualifications": {"gmp": "2000-01-01"},
        },
    )

    response = _schedule(client, _workflow_with_qualification(client))
    assert response.status_code == 200
    assert response.get_json()["meta"]["feasible"] is False
