# docs/11_Development/07_Solver_Template.md

# Development Guide

## Chapter 7 - Solver Implementation Template

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Development Baseline

---

# 1. Purpose

This document defines the implementation standard for the Scheduling Engine and Solver components.

The objective is to ensure that every optimization feature follows a consistent architecture.

The Solver is treated as an implementation detail.

Business logic remains outside the Solver.

---

# 2. Solver Architecture

The Solver Pipeline is fixed.

```text id="sv001"
Planning Problem

↓

Scheduling Model Builder

↓

Scheduling Model

↓

Variable Builder

↓

Constraint Builder

↓

Objective Builder

↓

Solver Adapter

↓

Scheduling Solution

↓

Assignment Builder
```

Every scheduling request follows this sequence.

No stage may be skipped.

---

# 3. Responsibilities

| Component                | Responsibility                            |
| ------------------------ | ----------------------------------------- |
| Planning Problem Builder | Normalize business data                   |
| Scheduling Model Builder | Build runtime scheduling model            |
| Variable Builder         | Create optimization variables             |
| Constraint Builder       | Build solver-independent constraints      |
| Objective Builder        | Build optimization objectives             |
| Solver Adapter           | Translate to OR-Tools and execute         |
| Assignment Builder       | Convert solution back to business objects |

Each component owns one responsibility.

---

# 4. Variable Builder

Variable Builder creates optimization variables only.

Typical variables include:

- Assignment Variable
- Start Time Variable
- End Time Variable

Variable Builder shall not:

- evaluate business rules
- access repositories
- calculate objectives

---

# 5. Constraint Builder

Constraint Builder converts normalized scheduling facts into constraint objects.

Constraint Builder shall:

- consume Scheduling Model
- produce Constraint Model

Constraint Builder shall not:

- call OR-Tools APIs
- access the database
- evaluate user permissions

---

# 6. Objective Builder

Objective Builder creates optimization goals.

Examples

- Maximize completed demand
- Balance staff workload
- Maximize equipment utilization

Objective Builder never creates hard constraints.

---

# 7. Solver Adapter

Solver Adapter is the only component allowed to use OR-Tools.

Responsibilities

- Create CP-SAT model
- Register variables
- Register constraints
- Register objective
- Execute solver
- Parse solution

The Solver Adapter shall never:

- load Domain objects
- perform SQL
- modify business entities

---

# 8. Assignment Builder

Assignment Builder reconstructs business objects from the Scheduling Solution.

Input

- Scheduling Solution
- Scheduling Model

Output

- Assignment collection

Business reconstruction occurs only here.

---

# 9. Error Handling

Errors are classified into three groups.

Validation Errors

Examples

- Missing Capability
- Invalid Planning Context

Optimization Errors

Examples

- No feasible solution
- Solver timeout

Infrastructure Errors

Examples

- OR-Tools exception
- Unexpected runtime failure

Each category shall produce a different business exception.

---

# 10. Performance Guidelines

Implementations should:

- Build lookup dictionaries before iteration.
- Avoid repeated graph traversal.
- Minimize object allocation.
- Separate preprocessing from optimization.

The Scheduling Model should be constructed once and reused throughout one scheduling execution.

---

# 11. Logging

Every Solver execution records:

- Plan Version ID
- Number of Operations
- Number of Resources
- Number of Constraints
- Runtime
- Solver Status
- Objective Score

Detailed variable logging shall be enabled only in debug mode.

---

# 12. Testing Strategy

Each pipeline component shall be tested independently.

| Component                | Test Type        |
| ------------------------ | ---------------- |
| Planning Problem Builder | Unit Test        |
| Scheduling Model Builder | Unit Test        |
| Variable Builder         | Unit Test        |
| Constraint Builder       | Unit Test        |
| Objective Builder        | Unit Test        |
| Solver Adapter           | Integration Test |
| Assignment Builder       | Unit Test        |

The majority of tests should not require OR-Tools.

---

# 13. Architectural Rules

1. Business objects never enter the Solver Adapter.
2. The Scheduling Model is immutable.
3. Constraint Builder is solver-independent.
4. Objective Builder is solver-independent.
5. OR-Tools is isolated behind the Solver Adapter.
6. Assignment Builder is the only component allowed to reconstruct Assignments.
7. Every scheduling execution is deterministic for identical inputs and solver settings.

---

# 14. Extension Strategy

Future optimization features shall extend the pipeline rather than replacing it.

Examples

- Additional Constraint Builders
- Alternative Objective Builders
- Multiple Solver Adapters
- AI-assisted objective generation

The Planning Domain shall remain unchanged.

---

# 15. Implementation Baseline

Every Solver implementation in Lab APS shall follow the architecture defined in this document.

Business evolution shall occur in the Planning Domain.

Optimization evolution shall occur inside the Scheduling Engine.

The boundary between these two layers shall remain stable throughout the lifetime of the platform.
