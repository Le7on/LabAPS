# ADR-012 — Adopt a Unified API Response Envelope

**Status:** Accepted

**Date:** 2026-07-07

---

# Context

Two API documents disagreed on the response format, and the first implemented
endpoints followed neither consistently:

- `08_API/04_API_Response_Standard.md` specifies an envelope:
  `{ "success": bool, "data": ..., "meta": ... }` with a structured
  `error` object and stable SCREAMING_SNAKE error codes.
- `08_API/02_Planning_API.md` shows bare resource objects
  (e.g. `{ "id": ..., "planCode": ... }`).
- The committed test `test_plans_api.py` expected bare objects and a
  `{ "count", "items" }` list shape.
- The first implementation (planning + laboratory) returned bare objects,
  used HTTP 400 for validation, and lowercase error codes (`not_found`).

This is a contract ambiguity: the frontend, tests, and backend could each read a
different "authoritative" source. It must be resolved before more endpoints
harden the wrong shape.

---

# Problem Statement

The API needs one predictable response contract that:

- distinguishes business errors from transport status,
- carries command metadata (scheduling runtime, objective score, warnings),
- carries pagination metadata for collections,
- remains stable as endpoints and future async APIs are added.

---

# Decision

Lab APS adopts the response envelope defined in
`08_API/04_API_Response_Standard.md` as the single authoritative contract for
every REST endpoint.

## Success

```json
{ "success": true, "data": <object|array>, "meta": { ... } }
```

- Single resources: `data` is an object.
- Collections: `data` is an array; pagination lives in `meta`
  (`page`, `pageSize`, `total`).
- Commands (generate schedule, publish): `data` is the updated resource;
  execution info (`runtimeMs`, `objectiveScore`, `warnings`) lives in `meta`.

## Error

```json
{
  "success": false,
  "error": { "code": "PLAN_NOT_FOUND", "message": "...", "details": [] },
  "meta": {}
}
```

- Error `code` is a stable SCREAMING_SNAKE identifier, independent of UI wording.
- Validation failures return HTTP 422 with `code: "VALIDATION_FAILED"` and
  per-field `details`.
- Business conflicts return HTTP 409; not-found returns 404; unexpected
  failures return 500 and never expose stack traces, SQL, or exception types.

HTTP status conveys transport semantics; the error `code` conveys business
meaning.

---

# Consequences

Positive

- One contract for frontend, tests, and backend; the two API docs stop
  disagreeing (doc 02 examples are updated to show envelopes).
- Command and pagination metadata have a defined home.
- Future async APIs preserve the same outer structure.

Negative

- The committed `test_plans_api.py` and the first endpoints must be updated to
  the envelope. This is a one-time migration done together with this ADR.
- Slightly more verbose responses; the frontend unwraps `data`/`meta` centrally
  in its API layer.

---

# Alternatives Considered

## Option A — Bare resource objects (status quo of doc 02 / first impl)

Rejected. No place for command/pagination metadata; forces ad-hoc shapes like
`{count, items}`; diverges from the more complete doc 04.

## Option B — Envelope only for collections/commands, bare for single GET

Rejected. Mixed contract; the frontend must branch per endpoint; violates the
"success and failure share the same outer structure" principle.

## Option C — Unified envelope for every endpoint (doc 04)

Accepted. Predictable, extensible, already fully specified in doc 04.

---

# Architectural Impact

- Presentation layer only. Domain, application, engines, solver and persistence
  are unaffected.
- A shared response helper (`backend/shared/api_response.py`) builds envelopes;
  error handlers emit the error envelope. `AppError` subclasses carry the stable
  code and HTTP status.

---

# Related Documents

- `08_API/04_API_Response_Standard.md` (authoritative response contract)
- `08_API/02_Planning_API.md` (examples updated to envelopes)
- SAD-16 API Architecture
