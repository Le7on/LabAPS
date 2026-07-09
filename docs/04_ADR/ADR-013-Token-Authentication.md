# ADR-013 — Token Authentication and Role Authorization

**Status:** Accepted

**Date:** 2026-07-08

---

# Context

The Planning API doc requires authenticated users and role-based authorization
(Production LM, Administrator), but listed authentication as "future". The REST
API has been built without any authentication. Bringing authentication in now —
before more endpoints harden — is cheaper than retrofitting, and the earlier
design review flagged the Composition Root as the natural injection point.

The current deployment target is a single-user PyWebView desktop app, with future
web/multi-user deployment on the roadmap (ADR-011).

---

# Decision

Adopt **token-based authentication with role authorization**, wired through the
Composition Root.

- A `User` has a role (`administrator` or `production_lm`) and owns one or more
  API tokens. Tokens are opaque random strings; only a hash is stored.
- Clients send `Authorization: Bearer <token>`. A single `before_request` guard
  resolves the token to the current user and attaches it to the request context.
- Endpoints declare required roles via a small decorator; the guard enforces
  authentication, the decorator enforces authorization.
- Health and authentication bootstrap endpoints are public; all business
  endpoints require authentication.

This is the simplest mechanism that satisfies the requirement for the desktop
stage and upgrades cleanly to JWT for web deployment (the token-verification seam
stays the same).

---

# Rationale

- Token headers need no login page or session store, fitting the PyWebView
  desktop model while still gating the API.
- Storing only token hashes avoids leaking credentials from the database.
- Centralizing verification in one guard keeps auth out of business code
  (use cases and the domain never see tokens or Flask request state).
- The role check is declarative and lives at the API boundary, consistent with
  "role enforcement belongs to the Application/API layer" (Planning API doc).

---

# Alternatives Considered

## Option A — Username/password + server sessions

Rejected for now. A full login flow (password hashing, session store, login page)
is more than the desktop stage needs; it can be layered on top of the same user
model later.

## Option B — Stateless JWT

Rejected as the starting point. JWT suits multi-user web deployment but is
heavier than needed for a single-user desktop app. The chosen design keeps the
verification seam so JWT can replace opaque tokens without touching endpoints.

## Option C — Opaque bearer token + role (chosen)

Accepted. Minimal, satisfies the requirement, and upgrade-friendly.

---

# Consequences

Positive

- All business endpoints are authenticated; roles gate sensitive actions.
- Auth is centralized; business layers remain framework- and auth-agnostic.
- A clear upgrade path to JWT/web sessions.

Negative

- Token issuance/management is minimal (no rotation UI yet).
- Tests and any API clients must send a token; a test fixture provides one.

---

# Architectural Impact

- New `identity` concern: `User` + `ApiToken` (infrastructure ORM + a domain
  role enum), an `AuthService` (verify token -> user), and a Flask guard +
  role decorator in `shared`.
- The Composition Root builds the `AuthService` and registers the guard.
- Domain, engines and solver are unaffected.

---

# Related Documents

- Planning API (security section)
- ADR-011 (Vue 3 SPA — future web deployment)
- ADR-012 (API response envelope — auth errors use the same envelope)
