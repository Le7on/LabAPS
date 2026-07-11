"""Update / delete CRUD tests for laboratory resources."""

from __future__ import annotations

import pytest

from backend.app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def test_project_update_and_delete(client):
    pid = client.post("/api/v1/projects", json={"projectCode": "PRJ-1", "name": "Old"}).get_json()[
        "data"
    ]["id"]

    updated = client.put(f"/api/v1/projects/{pid}", json={"projectCode": "PRJ-1", "name": "New"})
    assert updated.status_code == 200
    assert updated.get_json()["data"]["name"] == "New"

    deleted = client.delete(f"/api/v1/projects/{pid}")
    assert deleted.status_code == 200
    assert client.get("/api/v1/projects").get_json()["meta"]["total"] == 0


def test_delete_project_with_workflow_is_conflict(client):
    pid = client.post("/api/v1/projects", json={"projectCode": "PRJ-1", "name": "P"}).get_json()[
        "data"
    ]["id"]
    client.post(
        "/api/v1/workflow-definitions",
        json={
            "workflowCode": "WF-1",
            "name": "W",
            "projectId": pid,
            "operations": [{"operationType": "run", "duration": 1}],
        },
    )
    resp = client.delete(f"/api/v1/projects/{pid}")
    assert resp.status_code == 409


def test_equipment_update_and_delete(client):
    eid = client.post(
        "/api/v1/equipment", json={"equipmentCode": "EQ-1", "name": "Old"}
    ).get_json()["data"]["id"]

    updated = client.put(f"/api/v1/equipment/{eid}", json={"equipmentCode": "EQ-1", "name": "New"})
    assert updated.status_code == 200
    assert updated.get_json()["data"]["name"] == "New"

    assert client.delete(f"/api/v1/equipment/{eid}").status_code == 200
    assert client.get("/api/v1/equipment").get_json()["meta"]["total"] == 0


def test_staff_update_and_delete(client):
    sid = client.post("/api/v1/staff", json={"staffCode": "ST-1", "name": "Old"}).get_json()[
        "data"
    ]["id"]

    updated = client.put(f"/api/v1/staff/{sid}", json={"staffCode": "ST-1", "name": "New"})
    assert updated.status_code == 200
    assert updated.get_json()["data"]["name"] == "New"

    assert client.delete(f"/api/v1/staff/{sid}").status_code == 200
    assert client.get("/api/v1/staff").get_json()["meta"]["total"] == 0


def test_workflow_delete(client):
    pid = client.post("/api/v1/projects", json={"projectCode": "PRJ-1", "name": "P"}).get_json()[
        "data"
    ]["id"]
    wid = client.post(
        "/api/v1/workflow-definitions",
        json={
            "workflowCode": "WF-1",
            "name": "W",
            "projectId": pid,
            "operations": [{"operationType": "run", "duration": 1}],
        },
    ).get_json()["data"]["id"]

    assert client.delete(f"/api/v1/workflow-definitions/{wid}").status_code == 200
    assert client.get("/api/v1/workflow-definitions").get_json()["meta"]["total"] == 0


def test_update_missing_returns_404(client):
    assert client.put("/api/v1/staff/nope", json={"staffCode": "X", "name": "Y"}).status_code == 404
