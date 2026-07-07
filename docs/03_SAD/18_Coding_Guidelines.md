# docs/03_SAD/18_Coding_Guidelines.md

# Software Architecture Design

## Chapter 18 - Coding Guidelines

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines the coding principles for Lab APS.

The objective is to ensure that all source code follows the architectural decisions defined in the previous chapters.

Coding Guidelines focus on architecture rather than programming style.

PEP8 remains the default Python style guide.

---

# 2. Core Principles

Every implementation shall follow these principles.

1. Business first.
2. Domain before database.
3. Explicit is better than implicit.
4. Small classes.
5. Single responsibility.
6. Immutable scheduling input.
7. No hidden business logic.

---

# 3. Directory Responsibility

Each directory owns one responsibility.

```text id="cg001"
application/

laboratory/

planning/

execution/

reporting/

engines/

solver/

infrastructure/

common/
```

No directory shall become a "miscellaneous" folder.

Avoid directories such as:

```text id="cg002"
utils/

helpers/

misc/

common_services/
```

If a component cannot be classified, its responsibility should be reconsidered.

---

# 4. Domain Objects

Domain Objects represent business concepts.

Examples

- Plan
- PlanVersion
- WorkflowInstance
- OperationInstance
- Assignment

Domain Objects shall:

- contain business behaviour
- protect invariants
- expose meaningful methods

Domain Objects shall NOT:

- execute SQL
- call Flask
- call OR-Tools
- serialize JSON

---

# 5. Entity Design

Entities shall expose business methods.

Correct

```text id="cg003"
plan.publish()

plan.create_new_version()

assignment.complete()
```

Avoid

```text id="cg004"
plan.status = "Published"

assignment.status = "Completed"
```

Business state transitions shall be expressed through methods.

---

# 6. Value Objects

Immutable concepts shall be implemented as Value Objects.

Examples

- PlanningHorizon
- ShiftWindow
- CapabilitySet
- SkillSet
- MaterialQuantity

Value Objects shall:

- be immutable
- support equality by value
- contain validation

---

# 7. Repository Rules

Repositories persist Aggregate Roots only.

Allowed

```text id="cg005"
PlanRepository

EquipmentRepository

StaffRepository

WorkflowDefinitionRepository
```

Repositories shall never contain business rules.

Repositories shall never call the Solver.

---

# 8. Use Case Rules

Each Use Case represents one business action.

Examples

```text id="cg006"
CreatePlan

GenerateSchedule

PublishPlan

CompleteAssignment
```

Each Use Case shall:

- perform orchestration
- start one transaction
- invoke domain behaviour
- persist changes

Each Use Case shall NOT:

- implement scheduling
- calculate KPIs
- perform SQL directly

---

# 9. Engine Rules

Engines implement reusable business algorithms.

Current Engines

```text id="cg007"
Workflow Generator

Scheduling Model Builder

Constraint Builder

Objective Builder

Assignment Builder

Material Calculator
```

Engines are stateless.

Engines receive input.

Engines return output.

They never persist data.

---

# 10. Solver Rules

The Solver layer owns optimization only.

Allowed

- build variables
- build constraints
- invoke OR-Tools
- parse solution

Forbidden

- query repositories
- load Plans
- calculate materials
- publish Plans

---

# 11. DTO Rules

DTOs exist only at application boundaries.

DTOs shall:

- carry data
- contain no business behaviour

DTOs shall never be reused as Domain Objects.

---

# 12. Exception Rules

Business errors shall use domain-specific exceptions.

Examples

```text id="cg008"
InvalidPlanStateError

WorkflowDefinitionMissingError

SchedulingFailedError
```

Avoid generic exceptions for business logic.

---

# 13. Enumeration Rules

Business states shall be implemented using Enumerations.

Examples

```text id="cg009"
PlanStatus

AssignmentStatus

VersionType

EquipmentStatus
```

Avoid string literals in business logic.

---

# 14. Dependency Rules

Allowed

```text id="cg010"
Presentation

↓

Application

↓

Domain

↓

Infrastructure
```

Forbidden

- Domain → Flask
- Domain → SQLAlchemy
- Domain → OR-Tools
- Solver → Repository
- Reporting → Database

---

# 15. Testing Rules

Every business rule shall be testable without:

- Flask
- Database
- OR-Tools

Domain tests shall execute entirely in memory.

---

# 16. Naming Rules

Classes

```text id="cg011"
Plan

PlanVersion

WorkflowDefinition

SchedulingModel
```

Methods

```text id="cg012"
publish()

generate_schedule()

complete()

calculate_forecast()
```

Avoid ambiguous names.

Examples

```text id="cg013"
process()

execute()

handle()

do_work()
```

Method names shall express business intent.

---

# 17. Logging Rules

Log business events.

Examples

- Plan Created
- Schedule Generated
- Plan Published
- Assignment Completed

Do not log internal implementation details unless diagnosing failures.

---

# 18. Code Review Checklist

Every Pull Request shall answer:

- Does this preserve Aggregate boundaries?
- Does this introduce business logic into Infrastructure?
- Is this behaviour located in the correct Engine?
- Does this duplicate an existing Domain concept?
- Can this be unit tested without Flask?
- Can this be unit tested without a database?
- Does this violate any Architecture Constraint?

Changes failing this review shall be refactored before merge.

---

# 19. Architecture Philosophy

The codebase shall always reflect the business architecture.

Reading the source code should make the business process obvious.

Frameworks, databases and optimization libraries are implementation details.

Business concepts remain the permanent center of the system.
