# docs/03_SAD/15_Module_Interaction.md

# Software Architecture Design

## Chapter 15 - Module Interaction

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines how modules interact within Lab APS.

It establishes communication rules, dependency rules and ownership boundaries.

Its primary objective is to prevent architectural erosion as the project evolves.

---

# 2. Interaction Principles

All module interactions shall follow these principles.

1. Communication shall be use-case driven.
2. Modules shall expose services, not repositories.
3. Business logic shall remain inside the owning domain.
4. Dependencies shall be one-way.
5. Cross-module database access is prohibited.

---

# 3. Module Overview

```text
Presentation
        │
        ▼
Application
        │
        ▼
+---------------------------+
|  Laboratory Definition    |
|  Planning                 |
|  Execution                |
|  Reporting                |
+---------------------------+
        │
        ▼
Infrastructure
```

The Application Layer is the only coordinator.

---

# 4. Module Responsibilities

| Module                | Primary Responsibility             |
| --------------------- | ---------------------------------- |
| Presentation          | User interaction                   |
| Application           | Coordinate use cases               |
| Laboratory Definition | Laboratory definitions             |
| Planning              | Plan lifecycle and scheduling      |
| Execution             | Execution tracking                 |
| Reporting             | Reporting and dashboards           |
| Infrastructure        | Persistence and external libraries |

---

# 5. Allowed Dependencies

The following dependencies are allowed.

```text
Presentation
    │
    ▼
Application
    │
    ├────────► Laboratory Definition
    ├────────► Planning
    ├────────► Execution
    └────────► Reporting
```

Planning may depend on:

- Scheduling Engine
- Solver Adapter

through internal Domain Services only.

---

# 6. Forbidden Dependencies

The following dependencies are prohibited.

```text
Presentation
        │
        ├────► Repository

Presentation
        │
        ├────► OR-Tools

Reporting
        │
        ├────► Planning Repository

Execution
        │
        ├────► Scheduling Engine

Scheduling
        │
        ├────► SQLAlchemy

Scheduling
        │
        ├────► Flask
```

These rules shall be enforced during code review.

---

# 7. Repository Access Rules

Repositories are private to the owning module.

Correct

```text
Application Service

↓

PlanRepository
```

Incorrect

```text
Reporting

↓

PlanRepository
```

Reporting shall request data through Application Services.

---

# 8. Typical Interaction

## Create Plan

```text
Presentation

↓

PlanApplicationService

↓

Plan Aggregate

↓

PlanRepository

↓

Database
```

---

## Generate Schedule

```text
Presentation

↓

PlanningApplicationService

↓

PlanRepository

↓

SchedulingModelBuilder

↓

Scheduling Engine

↓

AssignmentBuilder

↓

PlanRepository

↓

Database
```

---

## Publish Plan

```text
Presentation

↓

PlanningApplicationService

↓

Plan Aggregate

↓

Publish()

↓

PlanRepository

↓

Database
```

---

## Update Execution

```text
Presentation

↓

ExecutionApplicationService

↓

Execution Domain

↓

ExecutionRepository

↓

Database
```

Planning data remains unchanged.

---

# 9. Read vs Write Model

Version 1.0 uses a logical separation between write operations and read operations.

Write Operations

- Create Plan
- Generate Schedule
- Publish Plan
- Update Execution

Read Operations

- Dashboard
- Reports
- Planning List
- Material Forecast

Read operations shall not modify domain objects.

---

# 10. Data Flow

Planning follows the sequence below.

```text
Laboratory Definition
            │
            ▼
Planning Context
            │
            ▼
PlanVersion
            │
            ▼
SchedulingModel
            │
            ▼
SchedulingSolution
            │
            ▼
Assignments
            │
            ▼
Material Forecast
            │
            ▼
Reports
```

Each transformation has a single owner.

---

# 11. Service Granularity

Application Services shall represent business use cases.

Examples

Correct

- CreatePlan()
- GenerateSchedule()
- PublishPlan()
- CompleteAssignment()

Avoid generic services such as

- Save()
- Update()
- Process()

Business-oriented interfaces improve readability.

---

# 12. Error Propagation

Errors propagate upward only.

```text
Infrastructure

↓

Domain

↓

Application

↓

Presentation
```

Each layer converts errors into representations suitable for the next layer.

Infrastructure exceptions shall never be exposed directly to the UI.

---

# 13. External Integration

External systems communicate only with the Application Layer.

Examples

- LIMS
- Inventory System
- Authentication Provider

No external system may invoke Domain objects directly.

---

# 14. Future Module Integration

Future modules shall integrate through Application Services.

Examples

- Scenario Planning
- Notification Center
- AI Recommendation
- Audit Center

Existing module boundaries shall remain unchanged.

---

# 15. Architecture Rules

1. Every module owns its business logic.

2. Every Aggregate owns its data.

3. Repositories are private to the owning module.

4. Cross-module database access is prohibited.

5. The Application Layer coordinates all business use cases.

6. Scheduling is an internal service of the Planning Domain.

7. External systems communicate only through Application Services.

8. Module boundaries shall not be bypassed for convenience.

---

# 16. Code Review Checklist

Every architectural change shall be reviewed against the following questions.

- Is ownership preserved?
- Is the dependency direction correct?
- Does this introduce a circular dependency?
- Does this bypass an Application Service?
- Does this expose internal domain objects?
- Does this violate Aggregate boundaries?

If any answer indicates a violation, the implementation shall be redesigned before merging.
