# docs/03_SAD/09_Plan_Version_Architecture.md

# Software Architecture Design

## Chapter 9 - Plan & Plan Version Architecture

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Approved (Architecture Baseline)

---

# 1. Purpose

This document defines the relationship between **Plan** and **Plan Version**.

The objective is to separate:

- Business Identity
- Planning Results

This design supports:

- Multiple schedule generations
- Version history
- Published plans
- Future scenario planning

without introducing additional business objects.

This document supersedes previous discussions regarding Planning Session and ParentPlanID.

---

# 2. Design Decision

The Planning Domain consists of two primary planning entities.

```text
Plan
    │
    └──────► Plan Version
```

Plan represents the business identity.

Plan Version represents one complete planning result.

---

# 3. Why Two Objects?

A laboratory manager usually thinks in terms of:

> "Week 32 Production Plan"

This identity never changes.

However, the schedule may be recalculated many times.

Example

```text
Week 32 Production Plan

Version 1

↓

Version 2

↓

Version 3

↓

Published
```

The business identity remains constant.

Only the planning result changes.

---

# 4. Plan

## Description

Plan represents one production planning period.

Examples

- Week 32 Production Plan
- Week 33 Production Plan
- August Production Plan

A Plan does not contain scheduling data.

Instead, it manages multiple Plan Versions.

---

## Responsibilities

Plan owns:

- Planning Horizon
- Name
- Description
- Current Published Version
- Version Collection

Plan does NOT own:

- Assignments
- Workflow Instances
- Material Forecast
- KPI

These belong to Plan Version.

---

# 5. Plan Version

## Description

Plan Version represents one scheduling result.

Every execution of the Scheduling Engine produces a new Plan Version.

Example

```text
Week 32

Version 1

↓

Schedule Generated

↓

Assignments

↓

Forecast

↓

KPI
```

Recalculating creates another version.

Existing versions remain unchanged.

---

# 6. Plan Structure

```text
Plan

├── Plan ID
├── Name
├── Planning Horizon
├── Description
├── Current Published Version
└── Version Collection
```

Plan contains only metadata.

---

# 7. Plan Version Structure

Each Plan Version owns a complete planning snapshot.

```text
Plan Version

├── Planning Context
├── Demand Snapshot
├── Workflow Instances
├── Operation Instances
├── Assignments
├── Material Forecast
├── KPI
└── Solver Information
```

Plan Version is self-contained.

---

# 8. Planning Context

Planning Context belongs to Plan Version.

It captures the environment used during scheduling.

Planning Context contains snapshots of:

- Calendar
- Shift Profile
- Equipment Availability
- Staff Availability
- Solver Profile

Planning Context is immutable.

---

# 9. Demand Snapshot

Demand belongs to Plan Version.

Reason:

Planning may be regenerated after the PI changes demand.

Example

```text
Version 1

PNG = 20

↓

PI changes requirement

↓

Version 2

PNG = 24
```

Historical demand must remain available.

---

# 10. Schedule Ownership

Assignments belong to Plan Version.

```text
Plan

↓

Plan Version

↓

Assignments
```

Assignments never belong directly to Plan.

---

# 11. Material Forecast Ownership

Material Forecast belongs to Plan Version.

Every version generates its own forecast.

Different versions may produce different material requirements.

---

# 12. KPI Ownership

KPIs belong to Plan Version.

Examples

- Equipment Utilization
- Staff Utilization
- Completion Rate
- Solver Runtime

KPIs are generated automatically after scheduling.

---

# 13. Version Lifecycle

```text
Created

↓

Generated

↓

Reviewed

↓

Published

↓

Archived
```

Each Plan Version has its own lifecycle.

Publishing one version does not modify historical versions.

---

# 14. Publish Strategy

Publishing follows these rules.

Rule 1

Only one Plan Version may have Published status.

Rule 2

Publishing a new version automatically retires the previous published version.

Rule 3

Historical versions remain read-only.

---

# 15. Version Types

Version Type classifies the purpose of a version.

Version 1.0 supports:

| Version Type | Description                            |
| ------------ | -------------------------------------- |
| Working      | Planner is still modifying the version |
| Published    | Official execution version             |
| Simulation   | Used for what-if analysis              |
| Emergency    | Generated for unexpected situations    |

Additional types may be introduced in future versions.

---

# 16. Version Creation

New Plan Versions may be created by:

- Initial planning
- Demand change
- Manual recalculation
- Equipment maintenance
- Staff leave
- Emergency request

Every new version copies the previous Planning Context before applying modifications.

---

# 17. Aggregate Design

Planning Aggregate

```text
Plan
    │
    ├── Plan Version
    │
    ├── Plan Version
    │
    └── Plan Version
```

Each Plan Version owns:

```text
Planning Context

Demand

Workflow Instance

Operation Instance

Assignment

Material Forecast

KPI
```

The Aggregate Root remains Plan.

---

# 18. Architectural Rules

The following rules are mandatory.

1. Plan is the Aggregate Root.

2. Plan Version is the planning result.

3. Workflow Instances belong to Plan Version.

4. Operation Instances belong to Workflow Instances.

5. Assignments belong to Plan Version.

6. Material Forecast belongs to Plan Version.

7. KPI belongs to Plan Version.

8. Planning Context belongs to Plan Version.

9. Published versions are immutable.

10. The Scheduling Engine always receives one Plan Version as input.

---

# 19. Implications for Database Design

The conceptual persistence model becomes:

```text
Plan
    │
    ├── PlanVersion
    │      │
    │      ├── PlanningContext
    │      ├── Demand
    │      ├── WorkflowInstance
    │      ├── OperationInstance
    │      ├── Assignment
    │      ├── MaterialForecast
    │      └── KPI
```

This structure preserves:

- Historical traceability
- Auditability
- Reproducibility
- Future extensibility

while keeping the Planning Domain simple.

---

# 20. Architecture Baseline

This document establishes the planning baseline for Lab APS.

Future modules, including:

- Database Design
- Repository Design
- REST API
- Scheduling Engine
- UI
- Reporting

shall adopt the Plan + Plan Version architecture defined here.

No alternative planning model shall be introduced without an Architecture Decision Record (ADR).
