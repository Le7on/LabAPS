# docs/11_Development/08_Domain_Entity_Template.md

# Development Guide

## Chapter 8 - Domain Entity Implementation Template

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Development Baseline

---

# 1. Purpose

This document defines the implementation standard for Domain Entities in Lab APS.

Domain Entities represent business concepts.

They are responsible for protecting business invariants and exposing business behaviour.

They are **not** persistence models.

They are **not** DTOs.

They are **not** ORM entities.

---

# 2. Design Philosophy

A Domain Entity answers the question:

> "What can this business object do?"

It does **not** answer:

> "What fields does this object have?"

Business behaviour is always more important than data structure.

---

# 3. Responsibilities

A Domain Entity shall:

* protect business invariants
* expose business behaviour
* validate state transitions
* generate domain events

A Domain Entity shall not:

* execute SQL
* call repositories
* call REST APIs
* know about Flask
* know about SQLAlchemy
* know about OR-Tools

---

# 4. Entity Structure

Every Domain Entity consists of:

```text id="de001"
Identity

↓

Business Attributes

↓

Business Behaviour

↓

Business Invariants

↓

Domain Events
```

Business behaviour is the primary interface.

---

# 5. Behaviour First

Business behaviour shall always be expressed through methods.

Correct

```python id="de002"
plan.create_version()

plan_version.approve()

plan_version.publish()

assignment.start()

assignment.complete()
```

Incorrect

```python id="de003"
plan_version.status = PlanVersionStatus.APPROVED

assignment.status = AssignmentStatus.RUNNING
```

Business state is the result of behaviour.

It is never the input.

---

# 6. State Protection

Entities are responsible for validating their own lifecycle.

Example

```python id="de004"
plan_version.publish()
```

The entity validates:

* Current state
* Business invariants
* Transition rules

The caller does not manipulate status directly.

---

# 7. Aggregate Consistency

Only the Aggregate Root may modify child entities.

Example

Correct

```text id="de005"
Plan

↓

create_version()

↓

PlanVersion
```

Incorrect

```text id="de006"
Repository

↓

Update PlanVersion
```

Child entities shall never be modified independently during business operations.

---

# 8. Identity

Every Entity has an immutable identity.

Identity consists of:

* Technical Identifier (UUID)
* Business Identifier (where applicable)

Identity never changes during the lifetime of the entity.

---

# 9. Equality

Entities compare by identity.

Example

```text id="de007"
PlanVersion

ID

↓

Equal
```

Business attributes shall not determine entity equality.

---

# 10. Value Objects

Immutable concepts shall be represented as Value Objects.

Examples

* PlanningHorizon
* ShiftWindow
* MaterialQuantity
* CapabilitySet
* SkillSet

Entities own Value Objects.

Entities do not inherit from them.

---

# 11. Business Invariants

Every Entity protects its own invariants.

Examples

PlanVersion

* Published versions are immutable.

Assignment

* Only Ready assignments may start.

Execution

* Completed executions cannot restart.

Business invariants shall never be duplicated in Use Cases.

---

# 12. Domain Events

Entities generate events when meaningful business behaviour occurs.

Examples

```text id="de008"
PlanVersionPublished

AssignmentStarted

ExecutionCompleted

EquipmentDisabled
```

Entities publish intent.

Infrastructure determines how events are handled.

---

# 13. Constructor Rules

Constructors create valid business objects only.

Invalid objects shall never exist.

Optional data may be initialized through explicit business methods.

---

# 14. Mutation Rules

Public setters are discouraged.

Business modifications shall occur through behaviour.

Example

Correct

```python id="de009"
equipment.disable()

staff.deactivate()

assignment.assign(...)
```

Incorrect

```python id="de010"
equipment.status = ...

staff.status = ...

assignment.staff = ...
```

---

# 15. Collaboration Rules

Entities collaborate only through:

* Aggregate Root
* Domain Services
* Value Objects

Entities shall not communicate through repositories or infrastructure components.

---

# 16. Testing Requirements

Each Entity shall have dedicated unit tests covering:

* Object creation
* Valid behaviour
* Invalid behaviour
* State transitions
* Business invariants
* Generated Domain Events

Entities shall be testable entirely in memory.

---

# 17. Code Review Checklist

Before approving a Domain Entity implementation, verify:

* Does the Entity expose behaviour instead of setters?
* Does it protect its own invariants?
* Does it avoid framework dependencies?
* Does it avoid persistence concerns?
* Does it generate Domain Events where appropriate?
* Does it preserve Aggregate consistency?

---

# 18. Implementation Baseline

Every Domain Entity in Lab APS shall follow this template.

The Domain Model is the center of the application.

Frameworks, databases and optimization libraries are implementation details.

Business behaviour shall always remain inside the Domain Entity.
