"""Demand API tests."""

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
        "/api/v1/projects", json={"projectCode": "PRJ-1", "name": "Assay"}
    ).get_json()["data"]["id"]


def _new_version(client):
    plan_id = client.post(
        "/api/v1/plans", json={"planningHorizon": "2026-W33", "name": "P"}
    ).get_json()["data"]["id"]
    version_id = client.post(f"/api/v1/plans/{plan_id}/versions").get_json()["data"]["id"]
    return plan_id, version_id


def test_add_and_list_demand(client):
    project_id = _project(client)
    plan_id, version_id = _new_version(client)
    base = f"/api/v1/plans/{plan_id}/versions/{version_id}/demands"

    created = client.post(base, json={"projectId": project_id, "quantity": 10, "priority": "high"})
    assert created.status_code == 201
    assert created.get_json()["data"]["priority"] == "high"

    listing = client.get(base)
    assert listing.status_code == 200
    body = listing.get_json()
    assert body["meta"]["total"] == 1
    assert body["data"][0]["projectId"] == project_id
    assert body["data"][0]["quantity"] == 10


def test_demand_requires_positive_quantity(client):
    project_id = _project(client)
    plan_id, version_id = _new_version(client)
    response = client.post(
        f"/api/v1/plans/{plan_id}/versions/{version_id}/demands",
        json={"projectId": project_id, "quantity": 0},
    )
    assert response.status_code == 422


def test_demand_with_unknown_project_returns_404(client):
    plan_id, version_id = _new_version(client)
    response = client.post(
        f"/api/v1/plans/{plan_id}/versions/{version_id}/demands",
        json={"projectId": "no-such-project", "quantity": 1},
    )
    assert response.status_code == 404


def test_demand_on_unknown_plan_returns_404(client):
    response = client.post(
        "/api/v1/plans/nope/versions/nope/demands",
        json={"projectId": "PRJ-1", "quantity": 1},
    )
    assert response.status_code == 404
