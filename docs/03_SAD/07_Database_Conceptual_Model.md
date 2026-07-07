# docs/03_SAD/07_Database_Conceptual_Model.md

# Software Architecture Design

## Chapter 7 - Conceptual Database Model

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Draft

---

# 1. Purpose

This document defines the conceptual data model of Lab APS.

The purpose of the conceptual model is to establish a stable mapping between the business domain and the persistence layer.

This document is independent of:

- SQL dialect
- ORM implementation
- Database engine

It defines business entities and their relationships only.

---

# 2. Design Principles

The conceptual database follows these principles.

1. Database entities originate from Domain Objects.

2. Database design shall not redefine business concepts.

3. Every entity has a single owner.

4. Relationships shall reflect business ownership.

5. Aggregate boundaries shall be preserved.

---

# 3. Domain Areas

The conceptual model is divided into three domains.

```text
Laboratory Definition

Planning

Execution
```

Each domain owns its own entities.

---

# 4. Laboratory Definition Domain

This domain defines the laboratory itself.

Entities

```text
Staff

Skill

Equipment

Capability

Project

Workflow Template

Operation Template

Material

Shift

Holiday

Maintenance

Leave
```

These entities are relatively stable.

They are shared by multiple Plans.

---

# 5. Planning Domain

Planning owns all planning data.

Entities

```text
Plan

Planning Context

Demand

Workflow Instance

Operation Instance

Assignment

Material Forecast

Plan KPI

Plan Version
```

All planning entities belong to exactly one Plan.

---

# 6. Execution Domain

Execution records actual execution status.

Entities

```text
Execution Record

Execution Log
```

Execution references Assignments.

Execution never changes planning data.

---

# 7. Entity Relationships

The overall relationship is shown below.

```text
Plan
│
├── Planning Context
│
├── Demand
│
├── Workflow Instance
│      │
│      └── Operation Instance
│
├── Assignment
│
├── Material Forecast
│
└── KPI
```

Outside references

```text
Workflow Template
        │
        ▼
Workflow Instance

Operation Template
        │
        ▼
Operation Instance

Equipment
        │
        ▼
Assignment

Staff
        │
        ▼
Assignment
```

---

# 8. Aggregate Ownership

Plan owns

- Planning Context
- Demand
- Workflow Instance
- Operation Instance
- Assignment
- Material Forecast
- KPI

Workflow Template owns

- Operation Template

Equipment owns

- Capability

Staff owns

- Skill

---

# 9. Reference Rules

Planning entities reference Laboratory Definition entities.

Examples

Workflow Instance

→ Workflow Template

Operation Instance

→ Operation Template

Assignment

→ Staff

Assignment

→ Equipment

Planning entities shall never duplicate laboratory definitions.

---

# 10. Snapshot Strategy

Planning Context stores planning snapshots.

Snapshots include

- Equipment Availability
- Staff Availability
- Calendar
- Shift Profile
- Solver Profile

Snapshots preserve reproducibility.

Historical Plans are unaffected by later configuration changes.

---

# 11. Version Strategy

A Plan may contain multiple versions.

Each version owns

- Assignments
- Material Forecast
- KPI

Only one version may have Published status.

---

# 12. Material Forecast

Material Forecast is derived data.

It references:

- Operation Instance
- Material Definition

Material Forecast never modifies inventory.

---

# 13. Execution Mapping

Execution references Assignments.

Relationship

```text
Assignment

↓

Execution Record

↓

Execution Log
```

Execution information is append-only.

Planning data remains unchanged.

---

# 14. Entity Lifecycle

Laboratory Definition

Long-lived

↓

Planning

Weekly

↓

Execution

Daily

↓

Archive

Historical

Entity lifecycle determines retention strategy.

---

# 15. Persistence Rules

The persistence layer shall follow these rules.

- No circular ownership.
- No cross-domain updates.
- No persistence logic inside Domain Objects.
- Repositories operate on Aggregate Roots only.
- Child entities are persisted through their Aggregate Root.

These rules ensure consistency between the Domain Model and the database model.
