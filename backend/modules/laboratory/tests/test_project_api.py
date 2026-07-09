"""Project API tests."""

from __future__ import annotations

import pytest

from backend.app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def test_create_and_list_project(client):
    response = client.post("/api/v1/projects", json={"projectCode": "PRJ-1", "name": "Assay Dev"})
    assert response.status_code == 201
    assert response.get_json()["data"]["projectCode"] == "PRJ-1"

    listing = client.get("/api/v1/projects")
    assert listing.status_code == 200
    body = listing.get_json()
    assert body["meta"]["total"] == 1
    assert body["data"][0]["name"] == "Assay Dev"


def test_create_project_requires_code(client):
    response = client.post("/api/v1/projects", json={"name": "No code"})
    assert response.status_code == 422
