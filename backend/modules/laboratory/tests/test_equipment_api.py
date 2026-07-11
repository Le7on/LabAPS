"""Equipment API tests."""

from __future__ import annotations

import pytest

from backend.app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def test_create_and_list_equipment(client):
    response = client.post(
        "/api/v1/equipment",
        json={"equipmentCode": "EQ-001", "name": "Centrifuge"},
    )
    assert response.status_code == 201
    payload = response.get_json()["data"]
    assert payload["equipmentCode"] == "EQ-001"
    assert payload["applicableProjectIds"] == []
    assert payload["methodIds"] == []
    assert payload["active"] is True

    listing = client.get("/api/v1/equipment")
    assert listing.status_code == 200
    body = listing.get_json()
    assert body["meta"]["total"] == 1
    assert body["data"][0]["name"] == "Centrifuge"


def test_create_equipment_requires_code(client):
    response = client.post("/api/v1/equipment", json={"name": "No code"})
    assert response.status_code == 422
    assert response.get_json()["error"]["code"] == "VALIDATION_FAILED"
