# docs/06_Planning_Model/03_Planning_Problem.md

# Planning Model

## Chapter 3 - Planning Problem

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines the Planning Problem.

The Planning Problem is the canonical representation of one scheduling problem.

It is generated from one Plan Version and Planning Context.

It becomes the input to the Scheduling Engine.

The Planning Problem is independent of:

- Database
- ORM
- Flask
- OR-Tools
- User Interface

---

# 2. Position in Architecture

```text
PlanVersion
        │
        ▼
Planning Context
        │
        ▼
Planning Problem Builder
        │
        ▼
Planning Problem
        │
        ▼
Scheduling Model Builder
        │
        ▼
Scheduling Model
        │
        ▼
Solver
```

Planning Problem separates business modelling from optimization modelling.

---

# 3. Responsibilities

The Planning Problem represents **what must be scheduled**.

It does not describe **how to optimize**.

Responsibilities include:

- Collect planning resources.
- Collect executable operations.
- Collect planning calendar.
- Collect planning policies.
- Provide a deterministic scheduling problem.

The Planning Problem never contains solver variables or mathematical constraints.

---

# 4. Planning Problem Composition

The Planning Problem consists of four logical sections.

```text
Planning Problem

├── Resources
├── Operations
├── Calendars
└── Planning Policies
```

Each section represents facts rather than optimization concepts.

---

# 5. Resources

Resources describe available scheduling capacity.

Version 1.0 resources include:

Equipment

- Identifier
- Capability Set
- Availability

Staff

- Identifier
- Skill Set
- Availability

Shift

- Shift Window
- Working Calendar

Resources contain no scheduling assignments.

---

# 6. Operations

Operations represent executable work.

Each operation contains:

- Identifier
- Duration
- Required Capability
- Required Skill
- Dependency Reference
- Metadata

Operations are independent of optimization variables.

---

# 7. Calendars

Calendars describe temporal availability.

Sources include:

- Shift Definition
- Holiday Calendar
- Staff Leave
- Equipment Maintenance

Calendars define available scheduling windows only.

---

# 8. Planning Policies

Planning Policies describe planning behaviour.

Examples

- Planning Horizon
- Frozen Window
- Solver Profile
- Objective Profile

Policies influence scheduling but are not business entities.

---

# 9. Builder Responsibilities

Planning Problem Builder performs the following tasks.

1. Read one Plan Version.

2. Read one Planning Context.

3. Resolve all references.

4. Build normalized Resources.

5. Build normalized Operations.

6. Build normalized Calendars.

7. Build Planning Policies.

The builder performs no optimization.

---

# 10. Relationship to Scheduling Model

Planning Problem represents planning semantics.

Scheduling Model represents optimization semantics.

Transformation pipeline

```text
Planning Problem

↓

Scheduling Model Builder

↓

Scheduling Model
```

Scheduling Model introduces:

- Variables
- Constraint Model
- Objective Model

These concepts do not exist in the Planning Problem.

---

# 11. Validation

The Planning Problem shall be validated before Scheduling Model construction.

Validation includes:

- Missing resources
- Missing operation definitions
- Invalid dependencies
- Invalid planning calendar
- Inconsistent planning policies

Only valid Planning Problems proceed to scheduling.

---

# 12. Architectural Rules

1. Planning Problem is immutable.

2. Planning Problem contains no optimization variables.

3. Planning Problem contains no mathematical constraints.

4. Planning Problem contains no persistence objects.

5. Planning Problem is the only input accepted by the Scheduling Model Builder.

6. Every scheduling execution creates exactly one Planning Problem.

---

# 13. Design Philosophy

Planning and Scheduling represent two different problem spaces.

Planning describes the business problem.

Scheduling transforms that business problem into an optimization model.

Keeping these concerns separate allows the Planning Domain and the Scheduling Engine to evolve independently while preserving a stable architecture.
