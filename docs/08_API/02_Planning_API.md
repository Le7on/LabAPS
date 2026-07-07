# docs/08_API/02_Planning_API.md

# OpenAPI Specification

## Planning API

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Draft

---

# 1. Purpose

This document defines the REST API contract for the Planning Domain.

The Planning API is responsible for the lifecycle of:

- Plan
- Plan Version
- Scheduling
- Publication

The API follows the Resource + Command architecture defined in:

`01_API_Resource_Model.md`

---

# 2. Resource Overview

```text id="planapi001"
/plans

/plans/{planId}

/plans/{planId}/versions

/plans/{planId}/versions/{versionId}
```

Business actions are implemented as Commands.

---

# 3. Create Plan

## Endpoint

```http id="planapi002"
POST /api/v1/plans
```

## Purpose

Create a new planning identity.

No schedule is generated.

No Plan Version is created.

---

## Request

```json id="planapi003"
{
  "planningHorizon": "2026-W32",
  "name": "Week 32 Production Plan",
  "description": "Routine production"
}
```

---

## Response

HTTP

```text id="planapi004"
201 Created
```

```json id="planapi005"
{
  "id": "PLAN-UUID",
  "planCode": "PLAN-2026-W32",
  "name": "Week 32 Production Plan",
  "planningHorizon": "2026-W32"
}
```

---

# 4. List Plans

## Endpoint

```http id="planapi006"
GET /api/v1/plans
```

## Query Parameters

| Parameter       | Description                         |
| --------------- | ----------------------------------- |
| planningHorizon | Filter by planning horizon          |
| status          | Filter by current published version |
| keyword         | Search by name                      |

---

## Response

HTTP

```text id="planapi007"
200 OK
```

Returns a collection of Plan summaries.

---

# 5. Get Plan

## Endpoint

```http id="planapi008"
GET /api/v1/plans/{planId}
```

Returns:

- Plan
- Current Published Version
- Version Summary

The API does not return complete Assignments.

Large collections are retrieved separately.

---

# 6. Create Plan Version

## Endpoint

```http id="planapi009"
POST /api/v1/plans/{planId}/versions
```

## Purpose

Create a new working Plan Version.

The new version copies:

- Planning Context
- Demand

No schedule is generated yet.

---

## Request

```json id="planapi010"
{
  "versionType": "Working",
  "comment": "Replan after equipment maintenance"
}
```

---

## Response

HTTP

```text id="planapi011"
201 Created
```

Returns the new Plan Version.

---

# 7. Get Plan Version

## Endpoint

```http id="planapi012"
GET /api/v1/plans/{planId}/versions/{versionId}
```

Returns

- Planning Context
- Demand
- Schedule Summary
- Forecast Summary

Large collections are paged where appropriate.

---

# 8. Generate Schedule

## Endpoint

```http id="planapi013"
POST /api/v1/plans/{planId}/versions/{versionId}:generate
```

## Purpose

Execute the complete planning pipeline.

Pipeline

```text id="planapi014"
Validate

↓

Build Planning Problem

↓

Build Scheduling Model

↓

Solve

↓

Build Assignments

↓

Calculate Forecast

↓

Calculate KPI
```

---

## Request

```json id="planapi015"
{
  "solverProfile": "Default"
}
```

---

## Response

HTTP

```text id="planapi016"
200 OK
```

```json
{
  "status": "Scheduled",
  "objectiveScore": 98.7,
  "runtimeMs": 5234,
  "warnings": []
}
```

---

# 9. Publish Plan Version

## Endpoint

```http id="planapi017"
POST /api/v1/plans/{planId}/versions/{versionId}:publish
```

## Preconditions

- Version Status = Reviewed
- Validation Passed

---

## Response

HTTP

```text id="planapi018"
200 OK
```

Returns the published Plan Version.

Only one version may be published.

---

# 10. Archive Plan

## Endpoint

```http id="planapi019"
POST /api/v1/plans/{planId}:archive
```

Archived Plans become read-only.

No physical deletion occurs.

---

# 11. Validation Errors

HTTP

```text id="planapi020"
400 Bad Request
```

Examples

- Invalid Planning Horizon
- Missing Demand
- Missing Planning Context

---

# 12. Business Errors

HTTP

```text id="planapi021"
409 Conflict
```

Examples

- Published Version already exists.
- Version cannot be published.
- Plan already archived.

---

# 13. Scheduling Errors

HTTP

```text id="planapi022"
422 Unprocessable Entity
```

Examples

- No feasible schedule.
- Missing qualified resources.
- Unsatisfied workflow dependencies.

---

# 14. Security

Planning operations require authenticated users.

Recommended authorization.

| Operation         | Role                          |
| ----------------- | ----------------------------- |
| Create Plan       | Production LM                 |
| Create Version    | Production LM                 |
| Generate Schedule | Production LM                 |
| Publish           | Production LM                 |
| Archive           | Administrator / Production LM |

Role enforcement belongs to the Application Layer.

---

# 15. Design Rules

1. Plans are Aggregate Roots.

2. Plan Versions are always accessed through Plans.

3. Commands use POST with `:action`.

4. Scheduling is triggered only through the Generate command.

5. Publish never modifies historical versions.

6. APIs exchange DTOs only.

7. Runtime scheduling models are never exposed.

---

# 16. Future Extension

Future commands may include:

```text id="planapi023"
:simulate

:compare

:clone

:export

:recalculate
```

These commands shall extend the existing resource model without changing resource ownership.
