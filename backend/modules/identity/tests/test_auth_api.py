"""Authentication and authorization API tests (ADR-013, auth enabled)."""

from __future__ import annotations

import pytest

from backend.app import create_app
from backend.modules.identity.domain.role import Role


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(TESTING=True)
    return app


@pytest.fixture()
def admin_token(app):
    # Seed an administrator directly through the container's auth service.
    result = app.config["CONTAINER"].auth_service.create_user("admin", Role.ADMINISTRATOR)
    return result["token"]


def _auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_unauthenticated_request_is_rejected(app):
    client = app.test_client()
    response = client.get("/api/v1/plans")
    assert response.status_code == 401
    assert response.get_json()["error"]["code"] == "UNAUTHORIZED"


def test_health_is_public(app):
    client = app.test_client()
    assert client.get("/api/v1/health").status_code == 200


def test_authenticated_request_succeeds(app, admin_token):
    client = app.test_client()
    response = client.get("/api/v1/plans", headers=_auth(admin_token))
    assert response.status_code == 200


def test_whoami_returns_current_user(app, admin_token):
    client = app.test_client()
    response = client.get("/api/v1/auth/whoami", headers=_auth(admin_token))
    assert response.status_code == 200
    assert response.get_json()["data"]["role"] == "administrator"


def test_admin_can_create_user_and_new_user_can_authenticate(app, admin_token):
    client = app.test_client()
    created = client.post(
        "/api/v1/users",
        json={"username": "planner", "role": "production_lm"},
        headers=_auth(admin_token),
    )
    assert created.status_code == 201
    planner_token = created.get_json()["data"]["token"]

    whoami = client.get("/api/v1/auth/whoami", headers=_auth(planner_token))
    assert whoami.get_json()["data"]["role"] == "production_lm"


def test_non_admin_cannot_create_user(app, admin_token):
    client = app.test_client()
    planner_token = client.post(
        "/api/v1/users",
        json={"username": "planner", "role": "production_lm"},
        headers=_auth(admin_token),
    ).get_json()["data"]["token"]

    forbidden = client.post(
        "/api/v1/users",
        json={"username": "x", "role": "production_lm"},
        headers=_auth(planner_token),
    )
    assert forbidden.status_code == 403
    assert forbidden.get_json()["error"]["code"] == "FORBIDDEN"


def test_invalid_token_is_rejected(app):
    client = app.test_client()
    response = client.get("/api/v1/plans", headers=_auth("not-a-real-token"))
    assert response.status_code == 401


def test_issue_token_bootstraps_admin_and_authenticates(app):
    # issue_token is the seed_admin entry point: it must work with no prior user.
    auth_service = app.config["CONTAINER"].auth_service
    result = auth_service.issue_token("admin", Role.ADMINISTRATOR)
    assert result["created"] is True

    client = app.test_client()
    whoami = client.get("/api/v1/auth/whoami", headers=_auth(result["token"]))
    assert whoami.status_code == 200
    assert whoami.get_json()["data"]["role"] == "administrator"


def test_issue_token_is_idempotent_for_existing_user(app):
    auth_service = app.config["CONTAINER"].auth_service
    first = auth_service.issue_token("admin", Role.ADMINISTRATOR)
    second = auth_service.issue_token("admin", Role.ADMINISTRATOR)

    assert second["created"] is False
    assert second["id"] == first["id"]
    # Both tokens are distinct and both authenticate as the same user.
    assert first["token"] != second["token"]
    client = app.test_client()
    for token in (first["token"], second["token"]):
        assert client.get("/api/v1/auth/whoami", headers=_auth(token)).status_code == 200
