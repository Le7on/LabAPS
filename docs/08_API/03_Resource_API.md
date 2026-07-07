# docs/08_API/03_Resource_API.md

# OpenAPI Specification

## Resource API

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Draft

---

# 1. Purpose

This document defines REST resources used to maintain laboratory configuration.

These resources represent stable laboratory definitions.

Unlike Planning APIs, Resource APIs primarily support Create, Read, Update and Disable operations.

Resource APIs never generate schedules.

---

# 2. Resource Overview

Version 1.0 exposes the following resources.

```text
/staff

/equipment

/projects

/workflows

/materials

/shifts

/calendars
```

Each resource corresponds to one Aggregate Root.

---

# 3. Staff API

## List Staff

```http
GET /api/v1/staff
```

Returns all active staff.

Supports filtering by:

* Status
* Skill
* Keyword

---

## Get Staff

```http
GET /api/v1/staff/{staffId}
```

Returns one Staff together with:

* Skills
* Current Status

Planning information is excluded.

---

## Create Staff

```http
POST /api/v1/staff
```

Creates a new laboratory operator.

---

## Update Staff

```http
PUT /api/v1/staff/{staffId}
```

Updates editable information.

Immutable fields include:

* Technical Identifier

---

## Disable Staff

```http
POST /api/v1/staff/{staffId}:disable
```

The Staff record remains in the database.

Historical Plans remain unaffected.

---

# 4. Equipment API

## List Equipment

```http
GET /api/v1/equipment
```

Supports filtering by:

* Status
* Capability
* Keyword

---

## Get Equipment

```http
GET /api/v1/equipment/{equipmentId}
```

Returns:

* Equipment Information
* Capability Set
* Qualification Status

Execution history is not included.

---

## Create Equipment

```http
POST /api/v1/equipment
```

---

## Update Equipment

```http
PUT /api/v1/equipment/{equipmentId}
```

---

## Disable Equipment

```http
POST /api/v1/equipment/{equipmentId}:disable
```

Disabled equipment is excluded from future planning.

Historical Plans remain unchanged.

---

# 5. Project API

## List Projects

```http
GET /api/v1/projects
```

Returns all supported laboratory services.

Examples

* FV
* 96 OPA
* 384 PNG
* AZ RSV

---

## Get Project

```http
GET /api/v1/projects/{projectId}
```

Returns:

* Project Information
* Active Workflow Definition

---

## Create Project

```http
POST /api/v1/projects
```

Projects are stable business services.

---

# 6. Workflow API

## List Workflow Definitions

```http
GET /api/v1/workflows
```

Returns available Workflow Definitions.

Supports filtering by:

* Project
* Version
* Active

---

## Get Workflow Definition

```http
GET /api/v1/workflows/{workflowId}
```

Returns:

* Operation Definitions
* Dependencies
* Material BOM

---

## Create Workflow Definition

```http
POST /api/v1/workflows
```

Creates a new workflow definition.

Existing definitions remain unchanged.

---

## Activate Workflow Definition

```http
POST /api/v1/workflows/{workflowId}:activate
```

Only one Workflow Definition may be active for one Project.

Historical Plans continue referencing previous Workflow Definitions.

---

# 7. Material API

## List Materials

```http
GET /api/v1/materials
```

Returns all supported consumables and reagents.

Inventory quantities are intentionally excluded.

---

## Create Material

```http
POST /api/v1/materials
```

Adds a new material definition.

---

# 8. Calendar API

Calendar resources include:

* Shift
* Holiday
* Maintenance
* Staff Leave

Examples

```http
GET /api/v1/shifts

GET /api/v1/calendars

POST /api/v1/calendars

POST /api/v1/shifts
```

Planning snapshots are generated from these resources.

---

# 9. Validation Rules

All Resource APIs perform:

* Input validation
* Duplicate checking
* Referential integrity validation

Business validation remains inside the Domain.

---

# 10. Delete Strategy

Physical deletion is discouraged.

Resources support:

```http
POST :disable
```

instead of

```http
DELETE
```

Historical planning data must remain valid.

---

# 11. Error Codes

Typical errors include:

400

Invalid Request

404

Resource Not Found

409

Duplicate Business Code

422

Business Validation Failed

---

# 12. Architectural Rules

1. Resource APIs expose laboratory definitions only.

2. Resource APIs never modify planning data.

3. Resource APIs never regenerate existing Plan Versions.

4. Workflow activation affects future planning only.

5. Historical planning data remains immutable.

6. Commands follow the Resource + Command convention established by the Planning API.
