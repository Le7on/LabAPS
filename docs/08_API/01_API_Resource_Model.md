# docs/08_API/01_API_Resource_Model.md

# API Resource Model

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines the REST resource model of Lab APS.

It establishes the mapping between Domain Aggregates and REST Resources.

The objective is to ensure that APIs expose business concepts rather than database tables or internal implementation details.

---

# 2. Design Principles

The API follows the principles below.

### Principle 1

Resources represent business objects.

Not database tables.

---

### Principle 2

URLs represent nouns.

HTTP methods represent actions.

---

### Principle 3

Business actions that do not naturally fit CRUD are modeled as commands on resources.

---

### Principle 4

Aggregate boundaries shall be preserved.

One request modifies one Aggregate Root.

---

# 3. Resource Overview

Version 1.0 exposes the following top-level resources.

```text id="api001"
Laboratory

├── Staff

├── Equipment

├── Projects

└── Workflow Definitions

Planning

└── Plans

Execution

└── Executions

Reporting

└── Reports
```

No other top-level resources shall be introduced without architectural review.

---

# 4. Planning Resources

Planning is centered around the Plan Aggregate.

```text id="api002"
/plans

/plans/{planId}

/plans/{planId}/versions

/plans/{planId}/versions/{versionId}
```

The Plan remains the Aggregate Root.

Plan Version is always accessed through its parent Plan.

---

# 5. Version Resources

Plan Versions expose planning results.

Examples

```text id="api003"
/plans/{planId}/versions

/plans/{planId}/versions/{versionId}
```

Nested resources include:

```text id="api004"
/assignments

/workflow-instances

/material-forecast

/kpis
```

These are subordinate resources.

They are never top-level resources.

---

# 6. Command Resources

Some business actions cannot be represented using CRUD.

These actions are modeled as commands.

Examples

```text id="api005"
POST

/plans/{planId}/versions

Create Plan Version
```

```text id="api006"
POST

/plans/{planId}/versions/{versionId}:generate
```

Generate Schedule.

```text id="api007"
POST

/plans/{planId}/versions/{versionId}:publish
```

Publish Plan Version.

Commands always operate on an existing Aggregate.

---

# 7. Laboratory Resources

Laboratory Definition exposes the following resources.

```text id="api008"
/staff

/equipment

/projects

/workflow-definitions

/materials

/shifts

/calendars
```

These resources support standard CRUD operations.

---

# 8. Execution Resources

Execution resources expose execution progress.

```text id="api009"
/executions

/executions/{executionId}
```

Execution updates Assignment status.

Execution never modifies planning data.

---

# 9. Reporting Resources

Reporting resources are read-only.

Examples

```text id="api010"
/reports/equipment-utilization

/reports/material-forecast

/reports/planning-summary
```

Reports shall never modify business objects.

---

# 10. Resource Ownership

| Resource              | Aggregate Owner     |
| --------------------- | ------------------- |
| /plans                | Plan                |
| /staff                | Staff               |
| /equipment            | Equipment           |
| /projects             | Project             |
| /workflow-definitions | Workflow Definition |
| /executions           | Execution           |

Every resource maps to exactly one Aggregate Root.

---

# 11. Nested Resource Rules

Nested resources are read through their owning Aggregate.

Examples

Allowed

```text id="api011"
/plans/{planId}/versions/{versionId}/assignments
```

Not Allowed

```text id="api012"
/assignments/{assignmentId}
```

Assignment belongs to a Plan Version.

It is not an independent Aggregate.

The same principle applies to:

* Workflow Instance
* Operation Instance
* Material Forecast
* KPI

---

# 12. HTTP Method Policy

| Method | Meaning                                     |
| ------ | ------------------------------------------- |
| GET    | Read                                        |
| POST   | Create or execute business command          |
| PUT    | Replace editable state                      |
| PATCH  | Partial update                              |
| DELETE | Archive or logical delete (where supported) |

Published planning data shall never be physically deleted.

---

# 13. Response Model

Every successful response follows a consistent structure.

```text id="api013"
{
    "data": {},
    "meta": {},
    "links": {}
}
```

Every error response follows a consistent structure.

```text id="api014"
{
    "error": {
        "code": "...",
        "message": "...",
        "details": []
    }
}
```

Internal exception details shall never be exposed.

---

# 14. Architectural Rules

1. Resources represent business concepts.

2. Aggregate Roots define top-level resources.

3. Child entities are exposed only through their parent Aggregate.

4. Business commands use POST on existing resources.

5. REST resources shall remain stable even if internal implementation changes.

6. DTOs derive from the Canonical Data Model rather than ORM models.

---

# 15. Next Artifact

The next document,

**02_OpenAPI_Specification.md**

defines:

* Every endpoint
* Request DTO
* Response DTO
* HTTP status codes
* Validation rules
* Error codes

using the resource model established in this document.
