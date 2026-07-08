"""Staff API tests."""

from __future__ import annotations

import pytest

from backend.app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def test_create_and_list_staff(client):
    response = client.post(
        "/api/v1/staff",
        json={"staffCode": "ST-001", "name": "Alice", "skills": ["pcr", "elisa"]},
    )
    assert response.status_code == 201
    payload = response.get_json()["data"]
    assert payload["staffCode"] == "ST-001"
    assert payload["skills"] == ["elisa", "pcr"]
    assert payload["active"] is True

    listing = client.get("/api/v1/staff")
    assert listing.status_code == 200
    body = listing.get_json()
    assert body["meta"]["total"] == 1
    assert body["data"][0]["name"] == "Alice"


def test_create_staff_requires_code(client):
    response = client.post("/api/v1/staff", json={"name": "No code"})
    assert response.status_code == 422
    assert response.get_json()["error"]["code"] == "VALIDATION_FAILED"
