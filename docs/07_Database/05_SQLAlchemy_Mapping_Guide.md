# docs/07_Database/05_SQLAlchemy_Mapping_Guide.md

# SQLAlchemy Mapping Guide

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines how the Canonical Data Model is mapped into SQLAlchemy ORM models.

Its objectives are:

- Maintain consistency across the codebase
- Preserve Aggregate boundaries
- Prevent ORM models from becoming Domain models
- Standardize relationship mapping

This guide applies to every SQLAlchemy model in Lab APS.

---

# 2. Design Principles

## Principle 1

ORM Models are persistence models.

They are **not** Domain Objects.

---

## Principle 2

Business behaviour belongs to Domain Objects.

ORM Models contain only persistence mapping.

---

## Principle 3

Repositories convert between ORM Models and Domain Objects.

Neither layer depends directly on the other.

---

# 3. Package Structure

Suggested package organization.

```text id="orm001"
infrastructure/

    orm/

        planning/

        laboratory/

        execution/

        common/
```

Each Aggregate has its own ORM package.

---

# 4. Base Entity

Every ORM model shall inherit from a common base class.

The base class provides:

- UUID primary key
- Audit fields
- Timestamp fields

Business fields shall not be defined in the base class.

---

# 5. UUID Strategy

Every table uses UUID as the primary key.

Example

```python id="orm002"
id = mapped_column(UUID, primary_key=True)
```

Business codes remain separate columns.

UUID is never exposed to end users.

---

# 6. Relationship Strategy

Relationships follow Aggregate ownership.

### One-to-Many

Example

```text id="orm003"
Plan

↓

PlanVersion
```

Use ORM relationships.

Parent owns child.

---

### Many-to-One

Child references parent through Foreign Key.

The child never owns the parent.

---

### Many-to-Many

Only mapping tables are allowed.

Examples

- staff_skill
- equipment_capability

Business logic shall not be stored in mapping tables.

---

# 7. Cascade Strategy

Cascade is allowed only inside the same Aggregate.

Recommended

```text id="orm004"
Plan

↓

PlanVersion

↓

WorkflowInstance

↓

OperationInstance
```

Recommended SQLAlchemy option

```python id="orm005"
cascade="all, delete-orphan"
```

Cross-Aggregate cascade is prohibited.

---

# 8. Loading Strategy

Default loading strategy

```text id="orm006"
selectinload
```

Reasons

- Good performance
- Avoids N+1 queries
- Predictable behaviour

Avoid default eager loading.

Load related objects only when required.

---

# 9. Lazy Loading Policy

Inside the Application Layer

Explicit loading is preferred.

Inside the Domain Layer

Lazy loading is prohibited.

Domain Objects shall not trigger database queries.

---

# 10. Enum Strategy

Business Enumerations shall be implemented using Python Enum classes.

Examples

```text id="orm007"
PlanStatus

AssignmentStatus

VersionType

EquipmentStatus
```

Database stores enum values using SQLAlchemy Enum mapping.

Magic strings are prohibited.

---

# 11. JSON Strategy

JSON columns are permitted only for immutable snapshots.

Examples

- Planning Context
- Solver Profile

JSON shall not replace relational business entities.

---

# 12. Repository Mapping

Repositories perform conversion.

```text id="orm008"
ORM Model

↓

Repository

↓

Domain Object
```

The reverse mapping follows the same path.

The Presentation Layer never accesses ORM models.

---

# 13. Transaction Strategy

Transactions are managed by the Application Layer.

Repositories shall not start or commit transactions.

Each Use Case defines one transaction boundary.

---

# 14. Query Strategy

Read operations may use optimized ORM queries.

Write operations shall always load Aggregate Roots.

Never update child entities directly.

Example

Correct

```text id="orm009"
Load Plan

↓

Modify PlanVersion

↓

Save Plan
```

Incorrect

```text id="orm010"
Update Assignment Table Directly
```

---

# 15. Index Guidelines

Indexes shall be added for:

- Foreign Keys
- Business Codes
- Frequently filtered status columns

Indexes shall not be added speculatively.

Measure before optimization.

---

# 16. Migration Strategy

Alembic is the only supported migration mechanism.

Rules

- Every schema change requires a migration.
- Migrations are additive whenever possible.
- Historical data must remain compatible.

Direct database modification is prohibited.

---

# 17. Mapping Rules Summary

1. ORM Models are not Domain Objects.

2. Repositories isolate persistence.

3. Cascade stays within Aggregate boundaries.

4. Domain Objects never depend on SQLAlchemy.

5. UUID is the technical identity.

6. JSON is used only for snapshots.

7. Transactions belong to Use Cases.

8. Every schema change is managed through Alembic.

---

# 18. Implementation Checklist

Before adding a new ORM model, verify:

- Does it correspond to a Canonical Object?
- Does it belong to an existing Aggregate?
- Is ownership correctly represented?
- Are cascade rules correct?
- Are loading strategies appropriate?
- Does it preserve the Domain Model?

Only after these questions are satisfied should the ORM model be implemented.
