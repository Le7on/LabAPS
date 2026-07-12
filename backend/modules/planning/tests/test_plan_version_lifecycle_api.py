"""API tests for the Plan Version lifecycle transitions."""

from __future__ import annotations

import pytest

from backend.app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def _new_plan_version(client):
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
    return plan_id, version_id


def test_full_lifecycle_via_api(client):
    plan_id, version_id = _new_plan_version(client)
    base = f"/api/v1/plans/{plan_id}/versions/{version_id}"

    # Schedule -> Scheduled.
    sched = client.post(f"{base}/schedule", json={"operations": [{"id": "op1", "duration": 2}]})
    assert sched.status_code == 200

    review = client.post(f"{base}/review")
    assert review.status_code == 200
    assert review.get_json()["data"]["status"] == "reviewed"

    publish = client.post(f"{base}/publish")
    assert publish.status_code == 200
    assert publish.get_json()["data"]["status"] == "published"

    # Published version is immutable: re-scheduling is a 409 conflict.
    conflict = client.post(f"{base}/schedule", json={"operations": [{"id": "op1", "duration": 2}]})
    assert conflict.status_code == 409
    assert conflict.get_json()["error"]["code"] == "CONFLICT"


def test_publish_before_review_is_conflict(client):
    plan_id, version_id = _new_plan_version(client)
    response = client.post(f"/api/v1/plans/{plan_id}/versions/{version_id}/publish")
    assert response.status_code == 409
