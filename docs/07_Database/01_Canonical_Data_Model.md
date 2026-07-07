# docs/07_Database/01_Canonical_Data_Model.md

# Canonical Data Model (CDM)

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

The Canonical Data Model (CDM) defines the authoritative business data structures used throughout Lab APS.

The CDM is independent of:

* Database technology
* ORM implementation
* REST API
* JSON serialization
* Solver implementation

Every implementation shall derive its data structures from this document.

The CDM is the Single Source of Truth (SSOT) for all persistent and exchangeable business data.

---

# 2. Design Principles

The CDM follows the principles below.

### Principle 1

Business objects are defined before database tables.

---

### Principle 2

Every object has exactly one owner.

---

### Principle 3

Objects are stable.

Implementations may change.

---

### Principle 4

The same business concept shall have the same structure everywhere.

Examples

* Database
* DTO
* API
* Export
* Import

---

### Principle 5

Scheduling-specific objects are excluded.

Objects such as:

* Scheduling Model
* Constraint Model
* Variable Model

are runtime models and do not belong to the CDM.

---

# 3. Domain Overview

The CDM consists of three domains.

```text
Laboratory Definition

↓

Planning

↓

Execution
```

Planning is the Core Domain.

---

# 4. Laboratory Definition Domain

Laboratory Definition contains stable business objects.

```text
Laboratory

├── Staff

├── Equipment

├── Capability

├── Skill

├── Project

├── Workflow Definition

├── Operation Definition

├── Material

├── Shift

└── Calendar
```

These objects describe the laboratory.

They are not planning results.

---

# 5. Planning Domain

Planning contains operational planning objects.

```text
Plan

└── Plan Version

      ├── Planning Context

      ├── Demand

      ├── Workflow Instance

      │      └── Operation Instance

      ├── Assignment

      ├── Material Forecast

      └── KPI
```

Everything inside Planning belongs to exactly one Plan Version except the Plan itself.

---

# 6. Execution Domain

Execution records actual execution.

```text
Execution

├── Execution Record

└── Execution Log
```

Execution references Assignments but never modifies planning data.

---

# 7. Canonical Object Rules

Each canonical object shall define:

* Identity
* Ownership
* Lifecycle
* Business Attributes
* Relationships

Every object in the CDM follows this template.

---

# 8. Object Identity

Business identity and technical identity are separated.

Every object shall contain:

Technical Identity

* UUID

Business Identity

* Business Code (when applicable)

Example

Plan

Technical ID

```text
UUID
```

Business Code

```text
PLAN-2026-W32
```

Business Codes may change.

UUIDs never change.

---

# 9. Object Classification

The CDM classifies objects into four categories.

## Definition Objects

Stable laboratory knowledge.

Examples

* Workflow Definition
* Operation Definition
* Equipment
* Staff

---

## Planning Objects

Generated during planning.

Examples

* Plan Version
* Workflow Instance
* Operation Instance

---

## Result Objects

Generated after scheduling.

Examples

* Assignment
* Material Forecast
* KPI

---

## Execution Objects

Generated during execution.

Examples

* Execution Record
* Execution Log

---

# 10. Ownership Rules

Every object has one owner.

| Object               | Owner                 |
| -------------------- | --------------------- |
| Staff                | Laboratory Definition |
| Equipment            | Laboratory Definition |
| Workflow Definition  | Laboratory Definition |
| Operation Definition | Workflow Definition   |
| Plan                 | Planning              |
| Plan Version         | Plan                  |
| Planning Context     | Plan Version          |
| Demand               | Plan Version          |
| Workflow Instance    | Plan Version          |
| Operation Instance   | Workflow Instance     |
| Assignment           | Plan Version          |
| Material Forecast    | Plan Version          |
| KPI                  | Plan Version          |
| Execution Record     | Execution             |

Ownership is mandatory.

Shared ownership is prohibited.

---

# 11. Reference Rules

Objects may reference other domains.

Example

Assignment

references

Equipment

Assignment

references

Staff

Reference does not imply ownership.

Cross-domain references shall always use stable identifiers.

---

# 12. Lifecycle Rules

Definition Objects

Long-lived

↓

Planning Objects

Versioned

↓

Result Objects

Derived

↓

Execution Objects

Historical

Each category follows a different lifecycle.

---

# 13. Versioning Rules

Only Planning Objects are versioned.

Examples

Plan

↓

Plan Version

Definition Objects remain stable.

Execution Objects are append-only.

---

# 14. Runtime Objects

The following objects do NOT belong to the CDM.

* Planning Problem
* Scheduling Model
* Constraint Model
* Objective Model
* Variable Model
* Scheduling Solution

These are runtime representations.

They are regenerated whenever scheduling executes.

---

# 15. Canonical Data Flow

The CDM defines the business data flow.

```text
Laboratory Definition

↓

Plan

↓

Plan Version

↓

Workflow Instance

↓

Operation Instance

↓

Assignment

↓

Execution
```

Every implementation shall preserve this flow.

---

# 16. Implementation Mapping

The CDM serves as the source model for:

Database

↓

ORM

↓

Repository

↓

DTO

↓

OpenAPI

↓

Import / Export

↓

Reporting

↓

Analytics

No implementation shall redefine business objects independently.

---

# 17. Architectural Rules

1. The CDM is the authoritative business data model.

2. Database tables derive from the CDM.

3. API DTOs derive from the CDM.

4. ORM entities derive from the CDM.

5. Runtime scheduling objects are excluded from the CDM.

6. Every business object appears only once in the CDM.

7. Any modification to the CDM requires an Architecture Decision Record (ADR).

---

# 18. Next Phase

The next document,

**02_Physical_ERD.md**

maps every Canonical Business Object into physical relational tables.

The Physical ERD shall not introduce any business object that does not already exist in the Canonical Data Model.
