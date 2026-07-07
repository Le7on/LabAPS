# docs/03_SAD/16_API_Architecture.md

# Software Architecture Design

## Chapter 16 - API & Use Case Architecture

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines the API architecture of Lab APS.

Unlike traditional CRUD systems, Lab APS is designed around business use cases.

Each API shall invoke exactly one Use Case.

Each Use Case represents one complete business action.

---

# 2. Architectural Principle

The API Layer shall expose business capabilities instead of database operations.

Correct

```text
Create Plan

Generate Schedule

Publish Plan

Complete Assignment
```

Incorrect

```text
Insert Plan

Update Plan

Delete Assignment
```

The API reflects business language rather than persistence operations.

---

# 3. Request Flow

Every request follows the same processing pipeline.

```text
Presentation

↓

REST API

↓

Use Case

↓

Domain

↓

Repository

↓

Database
```

The Presentation Layer never communicates directly with the Domain.

---

# 4. Use Case Layer

The Use Case Layer coordinates business activities.

Each Use Case:

- validates the request
- loads required aggregates
- invokes domain behavior
- persists changes
- returns a response

Business rules remain inside the Domain.

---

# 5. Core Use Cases

## Planning

```text
CreatePlan

ClonePlan

CreatePlanVersion

GenerateSchedule

PublishPlan

ArchivePlan
```

---

## Laboratory Definition

```text
CreateStaff

UpdateStaff

CreateEquipment

UpdateEquipment

CreateWorkflowDefinition

UpdateWorkflowDefinition
```

---

## Execution

```text
StartAssignment

CompleteAssignment

UpdateAssignmentStatus
```

---

## Reporting

```text
GetPlanningDashboard

GetEquipmentUtilization

GetMaterialForecast

ExportSchedule
```

---

# 6. API Resource Design

REST resources represent Aggregate Roots only.

Recommended resources

```text
/plans

/equipment

/staff

/projects

/workflow-definitions
```

Child entities are accessed through their parent.

Example

```text
/plans/{planId}/versions

/plans/{planId}/versions/{versionId}

/plans/{planId}/versions/{versionId}/assignments
```

There is no top-level Assignment API.

Assignments belong to a Plan Version.

---

# 7. API Design Rules

Rule 1

One request invokes one Use Case.

---

Rule 2

One Use Case owns one transaction.

---

Rule 3

One Aggregate Root is modified per request.

---

Rule 4

The API never returns Domain Entities.

DTOs are always returned.

---

# 8. DTO Strategy

The Presentation Layer exchanges DTOs only.

Example

```text
CreatePlanRequest

CreatePlanResponse

GenerateScheduleResponse

AssignmentSummary

PlanSummary
```

Domain objects remain internal.

---

# 9. Validation Strategy

Validation occurs in three stages.

## API Validation

Examples

- required fields
- invalid format
- missing parameters

---

## Use Case Validation

Examples

- Plan exists
- Version exists
- User authorization

---

## Domain Validation

Examples

- Plan lifecycle
- Publish rules
- Business invariants

Each layer validates only its own responsibility.

---

# 10. Long Running Operations

Schedule generation may require several seconds.

The API shall support asynchronous execution in future versions.

Version 1.0 may execute synchronously.

The Use Case interface shall remain unchanged.

---

# 11. Error Response

Errors are categorized as:

Business Error

```text
Cannot publish Draft Plan.
```

Validation Error

```text
Workflow Definition not found.
```

Scheduling Error

```text
No feasible schedule exists.
```

Infrastructure Error

```text
Database unavailable.
```

Responses shall never expose internal exception details.

---

# 12. API Versioning

API versioning is independent of Plan Version.

Recommended format

```text
/api/v1/...
```

Business versioning belongs to PlanVersion.

API versioning belongs to the interface.

These concepts shall never be mixed.

---

# 13. Architectural Rules

1. APIs expose business actions.

2. Every API invokes one Use Case.

3. Use Cases coordinate Domains.

4. Domain owns business rules.

5. Repositories remain private.

6. DTOs isolate Presentation from Domain.

7. API versioning and Plan Versioning are independent.

8. Future interfaces (CLI, Web, Scheduler, Integration) shall reuse the same Use Cases.
