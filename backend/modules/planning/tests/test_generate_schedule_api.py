"""Integration test: create plan -> create version -> generate schedule.

Exercises the full slice through the real OR-Tools solver adapter wired in the
container.
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


def test_full_planning_to_schedule_flow(client):
    created = client.post(
        "/api/v1/plans",
        json={
            "startDate": "2026-08-10",
            "endDate": "2026-08-20",
            "planningHorizon": "2026-W34",
            "name": "Schedule Test",
        },
    )
    assert created.status_code == 201
    plan_id = created.get_json()["data"]["id"]

    version = client.post(f"/api/v1/plans/{plan_id}/versions")
    assert version.status_code == 201
    version_id = version.get_json()["data"]["id"]
    assert version.get_json()["data"]["versionNumber"] == 1

    schedule = client.post(
        f"/api/v1/plans/{plan_id}/versions/{version_id}/schedule",
        json={
            "operations": [
                {"id": "op1", "duration": 3},
                {"id": "op2", "duration": 2, "dependsOn": ["op1"]},
            ]
        },
    )

    assert schedule.status_code == 200
    body = schedule.get_json()
    assert body["success"] is True
    assert body["meta"]["feasible"] is True
    assert body["meta"]["makespan"] == 5
    assignments = {a["operationId"]: a for a in body["data"]["assignments"]}
    assert assignments["op2"]["start"] >= assignments["op1"]["end"]


def test_schedule_unknown_plan_returns_404(client):
    response = client.post(
        "/api/v1/plans/does-not-exist/versions/x/schedule",
        json={"operations": [{"id": "op1", "duration": 1}]},
    )
    assert response.status_code == 404
