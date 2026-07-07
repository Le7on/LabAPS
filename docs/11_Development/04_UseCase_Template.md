# docs/11_Development/04_UseCase_Template.md

# Development Guide

## Chapter 4 - Use Case Implementation Template

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Development Baseline

---

# 1. Purpose

This document defines the implementation template for Application Use Cases.

A Use Case represents one complete business action.

Examples include:

* Create Plan
* Create Plan Version
* Generate Schedule
* Approve Plan Version
* Publish Plan Version
* Start Execution

Every business action shall be implemented as one independent Use Case.

---

# 2. Design Philosophy

A Use Case coordinates business behaviour.

It is responsible for orchestration.

It is **not** responsible for business rules.

Business rules remain inside the Domain.

---

# 3. Responsibilities

A Use Case is responsible for:

* Validate request
* Load Aggregate
* Invoke Domain behaviour
* Invoke Engines (if required)
* Persist Aggregate
* Return DTO

A Use Case shall **not**:

* Execute SQL
* Build scheduling models
* Calculate business rules
* Manipulate ORM objects directly

---

# 4. Standard Execution Flow

Every Use Case follows the same sequence.

```text id="uct001"
Receive Request

↓

Validate Input

↓

Load Aggregate

↓

Invoke Domain

↓

Invoke Engine (Optional)

↓

Persist Aggregate

↓

Build Response DTO

↓

Return Response
```

Every step has one responsibility.

---

# 5. Standard Structure

Each Use Case consists of:

```text id="uct002"
Request DTO

↓

Use Case

↓

Response DTO
```

Dependencies are injected through the constructor.

---

# 6. Constructor Dependencies

Typical dependencies include:

* Repository
* Planning Engine
* Scheduling Engine
* Material Calculator

Only required dependencies shall be injected.

Avoid injecting unused services.

---

# 7. Request Validation

Input validation occurs before loading business objects.

Examples

* Required fields
* Invalid identifiers
* Invalid formats

Business validation is **not** performed here.

---

# 8. Aggregate Loading

The Use Case loads exactly one Aggregate Root.

Examples

```text id="uct003"
Plan
```

or

```text id="uct004"
Equipment
```

Child entities are accessed through the Aggregate.

Repositories shall never load child entities independently for business operations.

---

# 9. Domain Invocation

Business behaviour is executed through explicit domain methods.

Correct examples

```text id="uct005"
plan.create_version()

plan_version.approve()

plan_version.publish()

assignment.start()
```

Avoid direct property modification.

---

# 10. Engine Invocation

When required, Engines are invoked after Domain validation.

Example

```text id="uct006"
Generate Schedule

↓

Planning Problem Builder

↓

Scheduling Model Builder

↓

Scheduling Engine

↓

Assignment Builder

↓

Material Calculator
```

The Use Case coordinates these steps.

The Use Case does not implement them.

---

# 11. Persistence

Only Aggregate Roots are persisted.

Example

```text id="uct007"
PlanRepository.save(plan)
```

The Repository persists child entities through Aggregate ownership.

The Use Case never saves child entities individually.

---

# 12. Response DTO

The Response DTO contains only information required by the caller.

Response DTOs shall:

* be immutable
* contain no business behaviour
* contain no ORM models

---

# 13. Error Handling

Use Cases distinguish three categories of errors.

Validation Error

Input is invalid.

Business Error

Business rule violated.

Infrastructure Error

Unexpected technical failure.

Errors are propagated to the API layer using business exceptions.

---

# 14. Transaction Boundary

One Use Case equals one transaction.

```text id="uct008"
Begin Transaction

↓

Business Action

↓

Save Aggregate

↓

Commit
```

Any exception triggers rollback.

---

# 15. Naming Convention

Use Cases are named using business actions.

Correct

```text id="uct009"
CreatePlanUseCase

GenerateScheduleUseCase

ApprovePlanVersionUseCase

PublishPlanVersionUseCase
```

Avoid generic names such as:

```text id="uct010"
PlanService

BusinessService

CommonService
```

Names shall describe the business action.

---

# 16. Unit Testing

Each Use Case shall have dedicated tests covering:

* Successful execution
* Validation failures
* Business rule violations
* Infrastructure failures

Repositories and Solver Adapter shall be replaceable with test doubles.

---

# 17. Implementation Checklist

Before completing a Use Case, verify:

* One business action only.
* One Aggregate Root modified.
* Domain behaviour invoked through methods.
* No ORM logic.
* No SQL.
* No business rules implemented in the Use Case.
* One transaction.
* DTO returned.

---

# 18. Reference Implementation Pattern

Every new Use Case in Lab APS shall follow this document.

Consistency across all Use Cases is more important than implementation style.

A developer familiar with one Use Case should immediately understand every other Use Case in the project.
