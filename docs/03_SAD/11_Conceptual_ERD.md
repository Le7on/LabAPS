# docs/03_SAD/11_Conceptual_ERD.md

# Software Architecture Design

## Chapter 11 - Conceptual Entity Relationship Model

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines the conceptual entity relationship model for Lab APS.

The purpose of the conceptual model is to describe:

* Business entities
* Ownership
* Relationships
* Aggregate boundaries

This document intentionally ignores:

* Primary Keys
* Foreign Keys
* SQL Data Types
* Indexes
* ORM Implementation

Those belong to the Physical Database Design.

---

# 2. Domain Overview

The Lab APS conceptual model consists of three domains.

```text
Laboratory Definition

Planning

Execution
```

Planning is the Core Domain.

---

# 3. Laboratory Definition Domain

Laboratory Definition describes **what the laboratory is**.

It does not contain operational data.

## Entities

```text
Laboratory
│
├── Staff
│     └── Skill
│
├── Equipment
│     └── Capability
│
├── Project
│
├── Workflow Definition
│     └── Operation Definition
│
├── Material
│
├── Shift
│
├── Holiday
│
└── Maintenance
```

---

## Responsibilities

### Staff

Defines laboratory personnel.

Owns:

* Skills

Does not own:

* Assignments
* Plans

---

### Equipment

Defines laboratory instruments.

Owns:

* Capability

Does not own:

* Schedule
* Assignment

---

### Project

Represents a laboratory testing service.

Examples

* FV
* 96 OPA
* 384 PNG
* AZ RSV
* DiLA

A Project references one active Workflow Definition.

---

### Workflow Definition

Defines how a Project is executed.

Contains

* Operation Definitions
* Dependency Definitions
* Material BOM
* Intermediate Resource Definitions

Workflow Definition is reusable.

---

### Operation Definition

Defines one logical laboratory step.

Examples

* FV
* SMDP
* SAP
* CP
* SP

Operation Definition is never scheduled directly.

---

# 4. Planning Domain

Planning owns all generated planning data.

```text
Plan
│
└── Plan Version
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

---

## Plan

Represents one business planning identity.

Example

Week 32 Production Plan

---

## Plan Version

Represents one planning result.

Each scheduling execution creates a new Plan Version.

---

## Planning Context

Captures immutable snapshots used during scheduling.

Contains:

* Calendar Snapshot
* Staff Snapshot
* Equipment Snapshot
* Solver Profile
* Shift Profile

---

## Demand

Represents production requirements.

Demand belongs to one Plan Version.

Demand references one Project.

---

## Workflow Instance

Generated from:

Project

↓

Workflow Definition

↓

Workflow Instance

Workflow Instance groups multiple Operation Instances.

---

## Operation Instance

Generated automatically.

Contains:

* Status
* Duration
* Dependency
* Required Capability
* Required Skill

Operation Instance is the smallest schedulable business entity.

---

## Assignment

Represents scheduling results.

Assignment references:

* Operation Instance
* Staff
* Equipment
* Shift

Assignment belongs to one Plan Version.

---

## Material Forecast

Generated after scheduling.

References:

* Material
* Operation Instance

Contains:

* Planned Consumption
* Warning

---

## KPI

Represents calculated planning metrics.

Examples

* Equipment Utilization
* Staff Utilization
* Solver Runtime
* Completion Rate

---

# 5. Execution Domain

Execution records actual laboratory progress.

```text
Assignment

↓

Execution Record

↓

Execution Log
```

Execution does not modify planning data.

Execution records actual events.

---

# 6. Cross-Domain Relationships

The conceptual relationships are shown below.

```text
Project
        │
        ▼
Workflow Definition
        │
        ▼
Operation Definition
        │
        ▼
Workflow Instance
        │
        ▼
Operation Instance
        │
        ▼
Assignment
```

Resource references

```text
Assignment

├── Staff

├── Equipment

└── Shift
```

Demand relationship

```text
Plan Version

↓

Demand

↓

Project
```

---

# 7. Aggregate Boundaries

Planning Aggregate

```text
Plan
│
└── Plan Version
      │
      ├── Planning Context
      ├── Demand
      ├── Workflow Instance
      ├── Assignment
      ├── Material Forecast
      └── KPI
```

Workflow Aggregate

```text
Workflow Definition

└── Operation Definition
```

Staff Aggregate

```text
Staff

└── Skill
```

Equipment Aggregate

```text
Equipment

└── Capability
```

---

# 8. Cardinality

| Relationship                               | Cardinality                                    |
| ------------------------------------------ | ---------------------------------------------- |
| Plan → Plan Version                        | 1 : N                                          |
| Plan Version → Demand                      | 1 : N                                          |
| Project → Workflow Definition              | 1 : N (versioned definitions, only one active) |
| Workflow Definition → Operation Definition | 1 : N                                          |
| Plan Version → Workflow Instance           | 1 : N                                          |
| Workflow Instance → Operation Instance     | 1 : N                                          |
| Operation Instance → Assignment            | 1 : 0..1                                       |
| Equipment → Assignment                     | 1 : N                                          |
| Staff → Assignment                         | 1 : N                                          |
| Material → Material Forecast               | 1 : N                                          |

---

# 9. Design Decisions

## DD-001

Project and Workflow Definition are independent.

Business services remain stable even if execution workflows evolve.

---

## DD-002

Workflow Definition and Workflow Instance are independent.

Definitions are reusable.

Instances are generated.

---

## DD-003

Operation Definition and Operation Instance are independent.

Definitions describe the process.

Instances describe one execution.

---

## DD-004

Assignments are generated only after scheduling.

They never exist independently.

---

## DD-005

Material Forecast is a derived entity.

It is regenerated whenever a new Plan Version is generated.

---

# 10. Next Stage

This conceptual model serves as the source for the Physical Database Design.

The next design phase will define:

* Physical Tables
* Primary Keys
* Foreign Keys
* Indexes
* Naming Conventions
* SQLAlchemy Mapping

No physical database implementation shall contradict this conceptual model.
