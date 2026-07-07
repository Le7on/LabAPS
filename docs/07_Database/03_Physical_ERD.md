# docs/07_Database/03_Physical_ERD.md

# Physical Entity Relationship Design

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines the physical persistence model of Lab APS.

Unlike a traditional ERD that starts from tables, this design starts from Aggregate boundaries.

The objective is to preserve Domain integrity while implementing a relational database.

This document is the bridge between:

* Canonical Data Model
* SQLAlchemy ORM
* Relational Database

---

# 2. Design Principles

The physical database follows these principles.

### Principle 1

Aggregates determine transaction boundaries.

Tables do not.

---

### Principle 2

Relationships follow Aggregate ownership.

---

### Principle 3

Database normalization shall not violate Domain ownership.

---

### Principle 4

Historical planning data is append-only.

Updates to published planning data are prohibited.

---

# 3. Aggregate Mapping

The database contains four primary aggregates.

```text id="erd001"
Laboratory Aggregate

Planning Aggregate

Execution Aggregate

Reference Aggregate
```

Each aggregate owns its own persistence model.

---

# 4. Laboratory Aggregate

The Laboratory Aggregate stores reusable laboratory definitions.

```text id="erd002"
equipment
│
├── equipment_capability

staff
│
├── staff_skill

project
│
└── workflow_definition
        │
        ├── operation_definition
        ├── workflow_dependency
        └── material_bom

material

shift

calendar
```

These tables are shared by all planning activities.

---

# 5. Planning Aggregate

Planning is the Core Aggregate.

```text id="erd003"
plan
│
└── plan_version
      │
      ├── planning_context
      ├── demand
      ├── workflow_instance
      │       │
      │       └── operation_instance
      │
      ├── assignment
      ├── material_forecast
      └── plan_kpi
```

Every planning object belongs to exactly one Plan Version.

---

# 6. Execution Aggregate

Execution stores runtime execution history.

```text id="erd004"
execution_record
│
└── execution_log
```

Execution references Assignments.

Execution never owns planning data.

---

# 7. Reference Aggregate

Reference objects are reused throughout the system.

```text id="erd005"
capability

skill

material

shift

calendar
```

Reference aggregates contain no planning state.

---

# 8. Table Relationships

## Plan

```text id="erd006"
plan

1

↓

N

plan_version
```

---

## Plan Version

```text id="erd007"
plan_version

1

↓

1

planning_context
```

```text id="erd008"
plan_version

1

↓

N

demand
```

```text id="erd009"
plan_version

1

↓

N

workflow_instance
```

```text id="erd010"
plan_version

1

↓

N

assignment
```

```text id="erd011"
plan_version

1

↓

N

material_forecast
```

```text id="erd012"
plan_version

1

↓

1

plan_kpi
```

---

## Workflow

```text id="erd013"
workflow_definition

1

↓

N

operation_definition
```

```text id="erd014"
workflow_instance

1

↓

N

operation_instance
```

---

## Assignment

Assignments reference resources.

```text id="erd015"
assignment

↓

operation_instance

↓

equipment

↓

staff

↓

shift
```

Assignments own none of these objects.

---

# 9. Identity Strategy

Every table shall contain two identifiers.

Technical Identity

```text id="erd016"
id

UUID
```

Business Identity

Examples

```text id="erd017"
PLAN-2026-W32

PNG001

HM09
```

Technical identifiers are used internally.

Business identifiers are used by users.

---

# 10. Foreign Key Strategy

Foreign Keys always point toward Aggregate ownership.

Example

```text id="erd018"
plan_version

↓

plan
```

Allowed cross-aggregate references include:

* Assignment → Equipment
* Assignment → Staff
* Demand → Project
* WorkflowInstance → WorkflowDefinition

Cross-aggregate ownership is prohibited.

---

# 11. Cascade Rules

Cascade operations are allowed only within the same Aggregate.

Examples

Allowed

```text id="erd019"
Plan

↓

PlanVersion

↓

WorkflowInstance

↓

OperationInstance
```

Forbidden

```text id="erd020"
Assignment

↓

Equipment
```

Deleting or updating an Assignment shall never affect Equipment.

---

# 12. Versioning Strategy

Planning history is append-only.

Example

```text id="erd021"
Plan

↓

Version 1

↓

Version 2

↓

Version 3
```

No historical Plan Version shall be overwritten.

---

# 13. Snapshot Strategy

Planning Context stores immutable snapshots.

Snapshot data includes:

* Calendar
* Equipment Availability
* Staff Availability
* Solver Profile

Snapshots are stored together with the owning Plan Version.

---

# 14. Persistence Rules

The following rules are mandatory.

1. Every Aggregate Root owns one repository.

2. Child entities are persisted through the Aggregate Root.

3. Runtime scheduling objects are never persisted.

4. Published Plan Versions are immutable.

5. Historical records are append-only.

6. Cross-domain ownership is prohibited.

---

# 15. Mapping to SQLAlchemy

Each Aggregate Root maps to one Repository.

```text id="erd022"
PlanRepository

EquipmentRepository

StaffRepository

WorkflowDefinitionRepository
```

Child entities are managed through ORM relationships inside their owning Aggregate.

Repositories shall never exist for:

* Assignment
* OperationInstance
* MaterialForecast
* KPI

These objects are accessed through the Plan Aggregate.

---

# 16. Next Step

The next design artifact is:

**04_Table_Dictionary.md**

This document will define every physical table in detail, including:

* Columns
* Data Types
* Nullability
* Default Values
* Constraints
* Indexes

The Table Dictionary becomes the direct specification for SQLAlchemy model implementation.
