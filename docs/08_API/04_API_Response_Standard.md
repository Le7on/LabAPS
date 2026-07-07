# docs/08_API/04_API_Response_Standard.md

# API Response & Error Specification

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.1

**Status:** Implemented

**Decision:** [ADR-012](../04_ADR/ADR-012-API-Response-Envelope.md)

---

# 1. Purpose

This document defines the standard response format used by every REST API in Lab APS.

This envelope is the single authoritative response contract (ADR-012). It is
implemented by `backend/shared/api_response.py` and enforced for errors by
`backend/shared/error_handlers.py`.

A unified response model simplifies:

- Frontend implementation
- Error handling
- Logging
- Integration
- Future API evolution

Every endpoint shall follow this specification.

---

# 2. Design Principles

The API shall satisfy the following principles.

1. Responses are predictable.

2. Success and failure share the same outer structure.

3. Business errors are distinguishable from system errors.

4. HTTP status codes and business error codes are independent.

---

# 3. Success Response

Every successful response follows the structure below.

```json
{
  "success": true,
  "data": {},
  "meta": {}
}
```

---

## success

Boolean.

Always

```text
true
```

for successful requests.

---

## data

Contains the requested business object.

Examples

- Plan
- Plan Version
- Staff
- Equipment

Collections are returned as arrays.

---

## meta

Contains metadata.

Typical fields

```json
{
  "timestamp": "...",
  "requestId": "...",
  "durationMs": 35
}
```

---

# 4. Error Response

Every failed request follows the structure below.

```json
{
  "success": false,
  "error": {
    "code": "PLAN_VERSION_NOT_FOUND",
    "message": "Plan Version does not exist.",
    "details": []
  },
  "meta": {}
}
```

---

# 5. HTTP Status Mapping

| HTTP Status | Meaning                    |
| ----------- | -------------------------- |
| 200         | Success                    |
| 201         | Created                    |
| 400         | Invalid Request            |
| 401         | Authentication Required    |
| 403         | Permission Denied          |
| 404         | Resource Not Found         |
| 409         | Business Conflict          |
| 422         | Business Validation Failed |
| 500         | Internal Server Error      |

HTTP status communicates transport status.

Business meaning is represented by error codes.

---

# 6. Business Error Codes

Business errors shall use stable identifiers.

Examples

```text
PLAN_NOT_FOUND

PLAN_ALREADY_ARCHIVED

PLAN_VERSION_NOT_FOUND

WORKFLOW_NOT_FOUND

INVALID_PLAN_STATE

NO_FEASIBLE_SCHEDULE

INVALID_PLANNING_CONTEXT

STAFF_SKILL_MISSING

EQUIPMENT_CAPABILITY_MISSING

FV_QUALIFICATION_EXPIRED
```

Error codes shall never depend on user interface wording.

---

# 7. Validation Errors

Validation failures shall return

```text
422 Unprocessable Entity
```

Example

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Validation failed.",
    "details": [
      {
        "field": "planningHorizon",
        "message": "Planning horizon is required."
      }
    ]
  }
}
```

---

# 8. Business Conflicts

Business conflicts occur when the request is valid but violates business rules.

Examples

- Publishing an already published version.
- Editing an archived Plan.
- Creating duplicate business codes.

HTTP

```text
409 Conflict
```

---

# 9. Internal Errors

Unexpected failures return

```text
500 Internal Server Error
```

The response shall never expose:

- Stack traces
- SQL
- Internal exception types

Detailed information shall be written to the application log.

---

# 10. Pagination

Collection endpoints shall support pagination.

Response example

```json
{
  "success": true,
  "data": [],
  "meta": {
    "page": 1,
    "pageSize": 20,
    "total": 135
  }
}
```

---

# 11. Command Responses

Business commands such as:

- Generate Schedule
- Publish Plan
- Archive Plan

shall return the updated resource together with execution metadata.

Example

```json
{
  "success": true,
  "data": {
    "status": "Published"
  },
  "meta": {
    "runtimeMs": 5321
  }
}
```

---

# 12. Architectural Rules

1. Every API follows the same response structure.

2. Business errors use stable error codes.

3. HTTP status codes represent transport semantics only.

4. Internal exceptions are never exposed.

5. Response DTOs derive from the Canonical Data Model.

6. Future asynchronous APIs shall preserve the same response contract.
