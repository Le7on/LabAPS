# docs/07_Database/04_Table_Dictionary.md

# Table Dictionary

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Draft

---

# 1. Purpose

This document defines every physical table used by Lab APS.

For each table, the following information is specified:

* Purpose
* Aggregate Owner
* Primary Key
* Columns
* Relationships
* Index Strategy
* Business Constraints

This document is the implementation specification for SQLAlchemy models and Alembic migrations.

---

# 2. Naming Convention

## Table Names

All table names use lowercase snake_case.

Examples

```text id="td001"
plan

plan_version

workflow_definition

operation_instance
```

---

## Primary Keys

Every table shall contain:

```text id="td002"
id UUID
```

UUID is the technical identity.

---

## Business Code

Business identifiers shall be stored separately.

Examples

```text id="td003"
plan_code

equipment_code

project_code

workflow_code
```

Business codes are user-facing identifiers.

---

## Audit Columns

Every table shall contain the following audit fields.

```text id="td004"
created_at

created_by

updated_at

updated_by
```

Future versions may add:

```text id="td005"
is_deleted
```

for soft delete.

---

# 3. Planning Aggregate

## Table: plan

### Purpose

Represents the business identity of a production plan.

### Aggregate

Planning

### Primary Key

```text id="td006"
id
```

### Columns

| Column             | Type         | Required | Description                 |
| ------------------ | ------------ | -------- | --------------------------- |
| id                 | UUID         | Yes      | Technical identifier        |
| plan_code          | VARCHAR(50)  | Yes      | Business identifier         |
| name               | VARCHAR(200) | Yes      | Display name                |
| planning_horizon   | VARCHAR(50)  | Yes      | Example: 2026-W32           |
| description        | TEXT         | No       | Planner notes               |
| current_version_id | UUID         | No       | Currently published version |
| created_at         | DATETIME     | Yes      | Audit                       |
| created_by         | VARCHAR(100) | Yes      | Audit                       |
| updated_at         | DATETIME     | Yes      | Audit                       |
| updated_by         | VARCHAR(100) | Yes      | Audit                       |

### Relationships

```text id="td007"
Plan

1

↓

N

PlanVersion
```

---

## Table: plan_version

### Purpose

Represents one scheduling result.

### Aggregate

Plan

### Primary Key

```text id="td008"
id
```

### Columns

| Column            | Type         | Required | Description                      |
| ----------------- | ------------ | -------- | -------------------------------- |
| id                | UUID         | Yes      | Technical identifier             |
| plan_id           | UUID         | Yes      | Parent Plan                      |
| version_no        | INTEGER      | Yes      | Version sequence                 |
| version_type      | ENUM         | Yes      | Working / Published / Simulation |
| status            | ENUM         | Yes      | Current lifecycle state          |
| objective_score   | DECIMAL      | No       | Optimization score               |
| solver_runtime_ms | INTEGER      | No       | Runtime in milliseconds          |
| created_at        | DATETIME     | Yes      | Audit                            |
| created_by        | VARCHAR(100) | Yes      | Audit                            |

### Relationships

Owns

* PlanningContext
* Demand
* WorkflowInstance
* Assignment
* MaterialForecast
* PlanKPI

---

## Table: planning_context

### Purpose

Stores immutable planning snapshots.

### Aggregate

PlanVersion

### Columns

| Column             | Type | Required | Description            |
| ------------------ | ---- | -------- | ---------------------- |
| id                 | UUID | Yes      | Technical identifier   |
| plan_version_id    | UUID | Yes      | Owner                  |
| calendar_snapshot  | JSON | Yes      | Calendar snapshot      |
| equipment_snapshot | JSON | Yes      | Equipment availability |
| staff_snapshot     | JSON | Yes      | Staff availability     |
| shift_snapshot     | JSON | Yes      | Shift configuration    |
| solver_profile     | JSON | Yes      | Solver configuration   |

### Notes

Snapshots are immutable.

No live references are stored.

---

## Table: demand

### Purpose

Stores requested production quantities.

### Aggregate

PlanVersion

### Columns

| Column          | Type    |
| --------------- | ------- |
| id              | UUID    |
| plan_version_id | UUID    |
| project_id      | UUID    |
| quantity        | INTEGER |
| priority        | ENUM    |

---

## Table: workflow_instance

### Purpose

Represents one generated workflow.

### Aggregate

PlanVersion

### Columns

| Column                 | Type         |
| ---------------------- | ------------ |
| id                     | UUID         |
| plan_version_id        | UUID         |
| workflow_definition_id | UUID         |
| workflow_code          | VARCHAR(100) |
| status                 | ENUM         |

### Notes

WorkflowInstance is intentionally lightweight.

Business execution occurs on OperationInstance.

---

## Table: operation_instance

### Purpose

Represents one executable operation.

### Aggregate

WorkflowInstance

### Columns

| Column                  | Type         |
| ----------------------- | ------------ |
| id                      | UUID         |
| workflow_instance_id    | UUID         |
| operation_definition_id | UUID         |
| operation_code          | VARCHAR(100) |
| sequence_no             | INTEGER      |
| duration_shift          | INTEGER      |
| status                  | ENUM         |

### Notes

OperationInstance is the smallest schedulable business object.

---

## Table: assignment

### Purpose

Stores scheduling results.

### Aggregate

PlanVersion

### Columns

| Column                | Type     |
| --------------------- | -------- |
| id                    | UUID     |
| plan_version_id       | UUID     |
| operation_instance_id | UUID     |
| equipment_id          | UUID     |
| staff_id              | UUID     |
| shift_id              | UUID     |
| planned_start         | DATETIME |
| planned_end           | DATETIME |
| status                | ENUM     |

### Business Rule

One OperationInstance has at most one Assignment.

---

## Table: material_forecast

### Purpose

Stores predicted material consumption.

### Aggregate

PlanVersion

### Columns

| Column          | Type    |
| --------------- | ------- |
| id              | UUID    |
| plan_version_id | UUID    |
| material_id     | UUID    |
| quantity        | DECIMAL |
| warning_level   | ENUM    |

---

## Table: plan_kpi

### Purpose

Stores planning KPIs.

### Aggregate

PlanVersion

### Columns

| Column                | Type    |
| --------------------- | ------- |
| id                    | UUID    |
| plan_version_id       | UUID    |
| equipment_utilization | DECIMAL |
| staff_utilization     | DECIMAL |
| completion_rate       | DECIMAL |
| solver_runtime_ms     | INTEGER |

---

# 4. Laboratory Definition Aggregate

Version 1.0 defines the following master tables.

| Table                | Purpose                            |
| -------------------- | ---------------------------------- |
| staff                | Laboratory operators               |
| staff_skill          | Staff skill mapping                |
| equipment            | Laboratory equipment               |
| equipment_capability | Equipment capability mapping       |
| capability           | Capability definitions             |
| skill                | Skill definitions                  |
| project              | Laboratory services                |
| workflow_definition  | Workflow definition                |
| operation_definition | Operation definition               |
| workflow_dependency  | Workflow dependency definition     |
| material             | Consumable and reagent definitions |
| material_bom         | Material requirements              |
| shift                | Shift definitions                  |
| calendar             | Holiday and working calendar       |

Detailed field definitions for these tables are provided in separate documents to keep this dictionary maintainable.

---

# 5. Execution Aggregate

| Table            | Purpose                     |
| ---------------- | --------------------------- |
| execution_record | Execution status            |
| execution_log    | Historical execution events |

Execution tables reference Assignments but never modify planning data.

---

# 6. General Constraints

The following constraints apply to all tables.

* Every table has a UUID primary key.
* Foreign keys reference Aggregate ownership.
* Business codes are unique where applicable.
* Published planning data is immutable.
* Historical records are append-only.

---

# 7. Next Artifact

The next document is:

**05_SQLAlchemy_Mapping_Guide.md**

It defines:

* ORM class organization
* Relationship mapping
* Cascade strategy
* Lazy loading strategy
* Repository implementation guidelines

This document bridges the gap between the physical schema and the Python implementation.
