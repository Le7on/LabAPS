"""Seed an administrator and print a one-time API token (ADR-013).

Bootstrap entry point for a fresh database, which starts empty. Because every
API path except health requires a valid bearer token and tokens can only be
issued by an existing administrator, the first administrator must be seeded out
of band. Run once after creating the database:

    python -m backend.seed_admin

The plaintext token is printed once and never stored (only its SHA-256 hash is
persisted). Paste it into the frontend login page. Re-running appends a fresh
token to the existing user rather than creating a duplicate.
"""

from __future__ import annotations

import argparse

from backend.app import create_app
from backend.modules.identity.domain.role import Role


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Seed an administrator API token.")
    parser.add_argument(
        "--username", default="admin", help="Administrator username (default: admin)."
    )
    parser.add_argument(
        "--role",
        default=Role.ADMINISTRATOR.value,
        choices=[r.value for r in Role],
        help="Role to assign to a newly created user (default: administrator).",
    )
    args = parser.parse_args(argv)

    app = create_app()
    auth_service = app.config["CONTAINER"].auth_service
    result = auth_service.issue_token(args.username, Role(args.role), label="seed")

    action = "Created" if result["created"] else "Issued new token for existing"
    print(f"{action} user '{result['username']}' (role: {result['role']}).")
    print()
    print("API token (shown once - copy it now):")
    print(f"    {result['token']}")
    print()
    print("Paste this token into the frontend login page.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
