import pytest

from backend.app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def test_create_and_list_plan(client):
    response = client.post(
        "/api/v1/plans",
        json={
            "planningHorizon": "2026-W32",
            "name": "Week 32 Production Plan",
            "description": "Routine production",
        },
    )

    assert response.status_code == 201
    payload = response.get_json()
    assert payload["success"] is True
    assert payload["data"]["name"] == "Week 32 Production Plan"
    assert payload["data"]["planningHorizon"] == "2026-W32"

    listing = client.get("/api/v1/plans")
    assert listing.status_code == 200
    body = listing.get_json()
    assert body["success"] is True
    assert body["meta"]["total"] == 1
    assert body["data"][0]["name"] == "Week 32 Production Plan"


def test_get_plan_returns_details(client):
    created = client.post(
        "/api/v1/plans",
        json={
            "planningHorizon": "2026-W33",
            "name": "Week 33 Production Plan",
            "description": "Routine production",
        },
    )
    plan_id = created.get_json()["data"]["id"]

    response = client.get(f"/api/v1/plans/{plan_id}")

    assert response.status_code == 200
    payload = response.get_json()["data"]
    assert payload["id"] == plan_id
    assert payload["planCode"] == "PLAN-2026-W33"
