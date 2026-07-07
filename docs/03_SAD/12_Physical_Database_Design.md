# docs/03_SAD/12_Physical_Database_Design.md

# Software Architecture Design

## Chapter 12 - Physical Database Design

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines the physical database model for Lab APS.

It specifies:

- Physical tables
- Primary keys
- Foreign key relationships
- Naming conventions
- Audit columns

This design is derived directly from the Domain Model and Conceptual ERD.

---

# 2. Design Principles

The database shall follow these principles.

## DB-001

Tables represent persistent business entities.

---

## DB-002

Primary Keys use UUID.

Business Codes are stored separately.

Example

```text id="db1q1"
id

(UUID)

plan_code

PLAN-2026-W32
```

---

## DB-003

Every table includes audit columns.

```text id="db2q2"
created_at

created_by

updated_at

updated_by
```

---

## DB-004

Soft Delete is preferred.

```text id="db3q3"
is_deleted
```

Historical planning data shall never be physically removed.

---

# 3. Laboratory Definition Tables

The following tables define the laboratory.

```text id="tbl1"
staff

staff_skill

equipment

equipment_capability

project

workflow_definition

operation_definition

workflow_dependency

material

material_bom

shift

holiday

maintenance

staff_leave
```

---

## 3.1 staff

Purpose

Maintain laboratory operators.

Suggested columns

```text id="st1"
id

staff_code

name

status

remarks
```

---

## 3.2 staff_skill

Purpose

Map Staff to Skills.

Relationship

```text id="st2"
Staff

1

↓

N

StaffSkill
```

---

## 3.3 equipment

Purpose

Maintain laboratory equipment.

Suggested columns

```text id="eq1"
id

equipment_code

name

status

location
```

---

## 3.4 equipment_capability

Purpose

Store equipment capabilities.

Examples

- 384 Head
- 96 Head
- 16 Channel
- iSWAP

Many-to-many relationship between Equipment and Capability.

---

## 3.5 project

Purpose

Represent laboratory services.

Example

```text id="pj1"
FV

96 OPA

384 PNG

AZ RSV

DiLA
```

Projects are stable business objects.

---

## 3.6 workflow_definition

Purpose

Define execution flow.

Important fields

```text id="wf1"
id

workflow_code

project_id

version

is_active
```

A Project may own multiple Workflow Definitions.

Only one is active.

---

## 3.7 operation_definition

Purpose

Define logical workflow steps.

Suggested columns

```text id="op1"
id

workflow_definition_id

operation_code

name

duration_shift

required_skill

required_capability
```

---

## 3.8 workflow_dependency

Purpose

Represent operation precedence.

Example

```text id="dep1"
SMDP

↓

SAP
```

---

## 3.9 material

Purpose

Maintain material definitions.

Examples

- Tips
- Plate
- Deepwell Block
- FV Kit

No inventory quantities are stored.

---

## 3.10 material_bom

Purpose

Define expected material usage.

Relationship

```text id="bom1"
Operation Definition

↓

Material

↓

Quantity
```

---

# 4. Planning Tables

Planning data is versioned.

```text id="plan1"
plan

plan_version

planning_context

demand

workflow_instance

operation_instance

assignment

material_forecast

plan_kpi
```

---

## 4.1 plan

Purpose

Business identity.

Suggested columns

```text id="plan2"
id

plan_code

planning_horizon

name

current_version_id
```

---

## 4.2 plan_version

Purpose

Planning result.

Suggested columns

```text id="pv1"
id

plan_id

version_no

version_type

status

solver_runtime

objective_score
```

---

## 4.3 planning_context

Purpose

Planning snapshot.

Suggested columns

```text id="ctx1"
id

plan_version_id

calendar_snapshot

staff_snapshot

equipment_snapshot

solver_profile
```

Large snapshot fields may be stored as JSON.

---

## 4.4 demand

Purpose

Store production requirements.

Suggested columns

```text id="dm1"
id

plan_version_id

project_id

quantity

priority
```

---

## 4.5 workflow_instance

Purpose

Represent one generated workflow.

Suggested columns

```text id="wi1"
id

plan_version_id

workflow_definition_id

workflow_code
```

Workflow Instance remains lightweight.

---

## 4.6 operation_instance

Purpose

Represent executable operations.

Suggested columns

```text id="oi1"
id

workflow_instance_id

operation_definition_id

sequence_no

status
```

Scheduling is performed on Operation Instances.

---

## 4.7 assignment

Purpose

Scheduling result.

Suggested columns

```text id="as1"
id

plan_version_id

operation_instance_id

equipment_id

staff_id

shift_id

planned_start

planned_end

status
```

---

## 4.8 material_forecast

Purpose

Store predicted material usage.

Suggested columns

```text id="mf1"
id

plan_version_id

material_id

quantity

warning_level
```

---

## 4.9 plan_kpi

Purpose

Store calculated KPIs.

Suggested columns

```text id="kpi1"
id

plan_version_id

equipment_utilization

staff_utilization

completion_rate

solver_runtime
```

---

# 5. Execution Tables

```text id="exe1"
execution_record

execution_log
```

Execution references Assignment only.

Planning data is never modified.

---

# 6. Naming Convention

Tables

```text id="nm1"
snake_case
```

Columns

```text id="nm2"
snake_case
```

Primary Key

```text id="nm3"
id
```

Foreign Keys

```text id="nm4"
plan_id

project_id

equipment_id
```

No abbreviated column names.

---

# 7. Index Strategy

Recommended indexes

## plan

- plan_code
- planning_horizon

---

## plan_version

- plan_id
- status
- version_no

---

## assignment

- equipment_id
- staff_id
- shift_id
- operation_instance_id

---

## operation_instance

- workflow_instance_id
- status

---

# 8. JSON Usage

The following information may be stored as JSON snapshots.

- Planning Context
- Solver Parameters
- Snapshot Metadata

Business entities shall not be stored entirely as JSON.

Only immutable snapshots are allowed.

---

# 9. Database Responsibilities

The database is responsible for:

- Persistence
- Referential Integrity
- Historical Data

The database is NOT responsible for:

- Business Rules
- Scheduling Logic
- Workflow Generation
- Material Calculation

These responsibilities belong to the Domain Layer.

---

# 10. Evolution Strategy

Future schema evolution shall follow these rules.

- Add new tables instead of changing historical semantics.
- Preserve backward compatibility whenever possible.
- Never change the meaning of an existing column.
- Introduce new versions through migration scripts.

The physical database shall evolve without changing the core Domain Model.
