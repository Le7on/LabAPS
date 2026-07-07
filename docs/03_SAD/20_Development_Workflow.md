# docs/03_SAD/20_Development_Workflow.md

# Software Architecture Design

## Chapter 20 - Development Workflow

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines the engineering workflow for developing Lab APS.

Its objectives are:

- Preserve architectural consistency
- Ensure traceability
- Reduce regression risk
- Support long-term maintenance

Every change to the system shall follow this workflow.

---

# 2. Development Lifecycle

Every feature follows the same lifecycle.

```text id="dw001"
Requirement

↓

Architecture Review

↓

Domain Design

↓

Database Design (if required)

↓

Implementation

↓

Unit Test

↓

Integration Test

↓

Code Review

↓

Merge

↓

Release
```

Implementation shall never begin before the domain design is approved.

---

# 3. Requirement Traceability

Every implementation shall originate from a documented requirement.

Example

```text id="dw002"
FR-PLAN-006

↓

Use Case

↓

Implementation

↓

Unit Test
```

Every Pull Request shall reference:

- Requirement ID
- Use Case
- Related ADR (if applicable)

---

# 4. Architecture Change Process

Normal feature development shall not modify the architecture.

If a change affects:

- Domain Model
- Aggregate
- Module Boundary
- Persistence Model
- Scheduling Model

an Architecture Decision Record (ADR) is required.

No architectural change shall bypass the ADR process.

---

# 5. Feature Development Workflow

Each feature shall be developed in the following order.

### Step 1

Define the business requirement.

---

### Step 2

Identify the owning Domain.

---

### Step 3

Determine the affected Use Case.

---

### Step 4

Update the Domain Model if required.

---

### Step 5

Implement Domain behaviour.

---

### Step 6

Implement Application Use Case.

---

### Step 7

Implement Infrastructure.

---

### Step 8

Implement UI.

UI is always the last step.

---

# 6. Solver Development Workflow

Solver-related features follow a dedicated workflow.

```text id="dw003"
Business Rule

↓

Scheduling Model

↓

Constraint Builder

↓

Objective Builder

↓

Solver Adapter

↓

Assignment Builder

↓

Unit Test
```

Business rules shall never be implemented directly inside OR-Tools code.

---

# 7. Database Change Workflow

Schema changes follow the process below.

```text id="dw004"
Domain Model

↓

Conceptual ERD

↓

Physical Database Design

↓

Migration Script

↓

Repository Update

↓

Integration Test
```

The database schema shall never evolve independently of the Domain Model.

---

# 8. Testing Strategy

Testing follows the testing pyramid.

```text id="dw005"
Integration Test

▲

Engine Test

▲

Domain Test

▲

Unit Test
```

Priority shall always be given to Domain Tests.

---

# 9. Code Review Checklist

Every Pull Request shall answer the following questions.

### Domain

- Is the Aggregate respected?
- Are business rules located in the Domain?

### Application

- Does one Use Case represent one business action?

### Engine

- Is logic reusable?
- Is the Engine stateless?

### Solver

- Is OR-Tools isolated?

### Infrastructure

- Is persistence free of business logic?

---

# 10. Documentation Workflow

Architecture documentation evolves with the software.

Whenever one of the following changes:

- Domain
- Database
- API
- Scheduling Model

the corresponding document shall be updated in the same Pull Request.

Documentation and code shall remain synchronized.

---

# 11. Versioning

The project follows Semantic Versioning.

Examples

```text id="dw006"
v1.0.0

Major Release

v1.1.0

New Feature

v1.0.1

Bug Fix
```

Database migrations shall be versioned together with application releases.

---

# 12. Branch Strategy

Suggested Git branches.

```text id="dw007"
main

develop

feature/*

bugfix/*

release/*
```

Only reviewed code may be merged into `main`.

---

# 13. Release Checklist

Before a release:

- All unit tests pass.
- Integration tests pass.
- Database migrations validated.
- Documentation updated.
- Version number updated.
- Changelog updated.

No release shall bypass the checklist.

---

# 14. Definition of Done

A feature is considered complete only if:

- Requirement implemented.
- Unit tests written.
- Integration tests pass.
- Documentation updated.
- Code reviewed.
- No architectural violations remain.

Code alone does not constitute completion.

---

# 15. Engineering Principles

The following principles guide all development.

1. Business before technology.
2. Domain before database.
3. Use Cases before UI.
4. Engines before frameworks.
5. Simplicity before cleverness.
6. Traceability before speed.
7. Maintainability before optimization.

---

# 16. Long-term Evolution

Lab APS is expected to evolve over many years.

Future enhancements—including:

- Scenario Planning
- Dynamic Rescheduling
- LIMS Integration
- AI-assisted Scheduling
- Multi-site Planning

shall extend the existing architecture rather than replacing it.

The objective is evolutionary architecture rather than periodic redesign.
