# docs/03_SAD/13_Architecture_Constraints.md

# Software Architecture Design

## Chapter 13 - Architecture Constraints

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines the architectural constraints that every implementation must follow.

Unlike functional requirements, these constraints protect the long-term maintainability of the system.

Violating these constraints is considered an architectural defect.

---

# 2. Core Principles

Lab APS is based on four principles.

```text
Configuration

↓

Planning

↓

Scheduling

↓

Execution
```

Business knowledge flows downward.

Dependencies never flow upward.

---

# 3. Domain Ownership

Every business object has exactly one owner.

Example

| Business Object    | Owner                 |
| ------------------ | --------------------- |
| Plan               | Planning              |
| PlanVersion        | Planning              |
| WorkflowDefinition | Laboratory Definition |
| Equipment          | Laboratory Definition |
| Staff              | Laboratory Definition |
| Assignment         | Planning              |
| ExecutionRecord    | Execution             |

No object may have multiple owners.

---

# 4. Aggregate Rule

Aggregate boundaries shall never be crossed directly.

Correct

```text
Application Service

↓

PlanRepository

↓

Plan Aggregate
```

Incorrect

```text
AssignmentRepository

↓

Update Assignment

↓

Skip Plan
```

Assignments shall always be modified through the Plan Aggregate.

---

# 5. Repository Rules

Only Aggregate Roots own repositories.

Allowed

```text
PlanRepository

EquipmentRepository

StaffRepository

WorkflowDefinitionRepository
```

Forbidden

```text
AssignmentRepository

DemandRepository

OperationInstanceRepository

MaterialForecastRepository
```

Child entities are managed through Aggregate Roots.

---

# 6. Database Rules

Business logic shall never exist inside:

* SQL
* Trigger
* Stored Procedure
* ORM Model

The database is responsible only for persistence.

---

# 7. Domain Rules

Domain objects shall not depend on:

* Flask
* SQLAlchemy
* OR-Tools
* PyWebView

Domain objects must be pure Python.

---

# 8. Application Rules

Application Services coordinate business use cases.

Application Services shall not:

* implement optimization
* implement workflow generation
* implement business calculations

They orchestrate Domain Services.

---

# 9. Scheduling Rules

Scheduling receives only:

* PlanVersion
* PlanningContext

Scheduling never queries:

* Database
* Flask
* Repository

Scheduling returns Assignments only.

---

# 10. Material Rules

Material Forecast is generated after scheduling.

Material Forecast shall never:

* modify inventory
* influence optimization
* update external systems

Material Forecast is analytical only.

---

# 11. UI Rules

Presentation shall never:

* contain business rules
* access repositories
* access OR-Tools

Presentation communicates only through Application Services.

---

# 12. Configuration Rules

Configuration defines behavior.

Configuration shall never contain executable business logic.

Example

Allowed

```text
Shift

Holiday

Maintenance

Solver Profile
```

Forbidden

```text
IF Project == PNG

THEN ...

ELSE ...
```

Business rules belong in the Domain Layer.

---

# 13. Workflow Rules

Workflow Definition describes execution.

Workflow Definition shall never:

* contain schedule
* contain staff
* contain equipment

Workflow Definition is reusable.

---

# 14. Version Rules

Every scheduling execution creates a new PlanVersion.

Historical PlanVersions are immutable.

Published PlanVersions cannot be modified.

---

# 15. Extension Rules

Future extensions shall be implemented by adding new modules.

Existing Core Domain behavior shall not be modified unless an Architecture Decision Record (ADR) is approved.

---

# 16. Architecture Review Checklist

Every Pull Request affecting architecture shall answer:

* Does this violate Aggregate boundaries?
* Does this introduce business logic into Infrastructure?
* Does this bypass the Application Layer?
* Does this couple business logic to OR-Tools?
* Does this modify historical planning data?
* Does this preserve PlanVersion immutability?

If any answer is "Yes", the change requires architectural review.
