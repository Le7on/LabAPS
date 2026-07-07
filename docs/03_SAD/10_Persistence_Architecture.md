# docs/03_SAD/10_Persistence_Architecture.md

# Software Architecture Design

## Chapter 10 - Persistence Architecture

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines how business objects are persisted.

The persistence architecture shall preserve:

- Domain boundaries
- Aggregate consistency
- Historical traceability
- Version isolation

Persistence is an implementation of the Domain Model.

It shall never redefine business concepts.

---

# 2. Design Principles

The persistence layer follows these principles.

## Principle 1

Database entities originate from Domain Objects.

Never the opposite.

---

## Principle 2

Each Aggregate owns its own persistence model.

---

## Principle 3

Repositories exist only for Aggregate Roots.

Child entities are persisted through their Aggregate.

---

## Principle 4

Historical planning data must never be overwritten.

New planning results create new Plan Versions.

---

## Principle 5

Infrastructure owns persistence.

Domain owns business rules.

---

# 3. Aggregate Mapping

The following Aggregate Roots exist.

```text id="5kr5pn"
Laboratory Definition

├── Staff
├── Equipment
├── Workflow Template
└── Material


Planning

└── Plan
```

Repositories are created only for these Aggregate Roots.

---

# 4. Repository Design

Each Aggregate Root owns one Repository.

```text id="gnywga"
StaffRepository

EquipmentRepository

WorkflowTemplateRepository

PlanRepository
```

Repositories never exist for:

- Assignment
- OperationInstance
- Demand
- KPI
- MaterialForecast

These objects belong to PlanVersion.

---

# 5. Plan Aggregate Persistence

The persistence hierarchy is shown below.

```text id="t6ukfu"
Plan
│
├── PlanVersion
│      │
│      ├── PlanningContext
│      ├── Demand
│      ├── WorkflowInstance
│      │      │
│      │      └── OperationInstance
│      │
│      ├── Assignment
│      ├── MaterialForecast
│      └── KPI
```

Saving a Plan persists the complete aggregate.

---

# 6. Ownership Rules

Each entity has exactly one owner.

| Entity            | Owner            |
| ----------------- | ---------------- |
| PlanVersion       | Plan             |
| PlanningContext   | PlanVersion      |
| Demand            | PlanVersion      |
| WorkflowInstance  | PlanVersion      |
| OperationInstance | WorkflowInstance |
| Assignment        | PlanVersion      |
| MaterialForecast  | PlanVersion      |
| KPI               | PlanVersion      |

Ownership is mandatory.

Shared ownership is prohibited.

---

# 7. Reference Rules

Entities may reference external objects.

Example

```text id="hfsz1h"
Assignment

↓

Equipment
```

The Assignment stores:

- EquipmentId
- StaffId

It does not own Equipment or Staff.

---

WorkflowInstance stores:

WorkflowTemplateId

OperationInstance stores:

OperationTemplateId

Reference does not imply ownership.

---

# 8. Snapshot Strategy

PlanningContext stores snapshots rather than live references.

Snapshot examples

```text id="ckjlwm"
Equipment Availability

Staff Availability

Holiday Calendar

Shift Profile

Solver Profile
```

Snapshots guarantee that historical plans remain reproducible.

---

# 9. Version Strategy

Every scheduling calculation creates one PlanVersion.

Example

```text id="ez0dyo"
Plan

Week 32

│

├── Version 1

├── Version 2

└── Version 3
```

Versions are append-only.

Deletion is not supported.

---

# 10. Loading Strategy

The Application Layer shall avoid loading the complete aggregate unless necessary.

Recommended loading patterns

## Planning List

Load

Plan

Only

---

## Planning Detail

Load

Plan

Current PlanVersion

---

## Solver

Load

PlanVersion

Complete Aggregate

---

## Reporting

Load

Published PlanVersion

Only

---

# 11. Persistence Transactions

Transactions follow Aggregate boundaries.

Example

```text id="jlwm1u"
Generate Schedule

↓

Load Plan

↓

Create PlanVersion

↓

Generate Assignments

↓

Generate Forecast

↓

Save Plan

↓

Commit
```

No partial persistence is allowed.

---

# 12. Cascade Rules

Cascade persistence is allowed only inside the Aggregate.

Example

```text id="ovdbzv"
Plan

↓

PlanVersion

↓

WorkflowInstance

↓

OperationInstance
```

Cascade shall never cross Aggregate boundaries.

---

# 13. Delete Rules

Physical deletion is discouraged.

Recommended approach

Soft Delete

or

Archive

Historical planning data shall remain available.

---

# 14. Database Independence

Persistence architecture is independent of database technology.

Supported databases

- SQLite
- PostgreSQL

Future support

- SQL Server
- Oracle

Domain logic shall remain unchanged.

---

# 15. Architectural Rules

The following rules are mandatory.

1. Every Aggregate Root owns one Repository.

2. Child entities are never loaded independently for business operations.

3. PlanVersion is immutable after publication.

4. Historical data is append-only.

5. PlanningContext always stores snapshots.

6. Database entities shall not contain business logic.

7. ORM models are persistence models, not domain models.

8. Domain objects shall not inherit from SQLAlchemy models.

---

# 16. Persistence Flow

The persistence flow for schedule generation is:

```text id="8f7gcm"
PlanRepository

↓

Load Plan

↓

Create New PlanVersion

↓

Scheduling Engine

↓

Assignments

↓

Forecast

↓

PlanRepository.Save()

↓

Database
```

The Scheduling Engine never performs persistence directly.
