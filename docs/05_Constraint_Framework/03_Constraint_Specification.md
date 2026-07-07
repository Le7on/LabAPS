# docs/05_Constraint_Framework/03_Constraint_Specification.md

# Constraint Framework

## Chapter 3 - Constraint Specification

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines the Constraint Specification used by the Scheduling Engine.

Constraint Specification is the normalized scheduling language of Lab APS.

It is derived from Planning Facts rather than handwritten business rules.

Constraint Specification is solver-independent.

It forms the stable contract between the Planning Domain and the Scheduling Engine.

---

# 2. Design Philosophy

Lab APS does not compile business rules.

Instead, it derives scheduling constraints from planning facts.

The scheduling pipeline becomes:

```text
Laboratory Definition
        │
        ▼
Planning Context
        │
        ▼
Planning Facts
        │
        ▼
Constraint Specification
        │
        ▼
Constraint Model
        │
        ▼
Solver Adapter
```

Facts describe reality.

Constraints describe scheduling restrictions.

---

# 3. What is a Planning Fact?

A Planning Fact is a normalized business fact that may influence scheduling.

Examples include:

Operation Facts

* Operation Duration
* Required Capability
* Required Skill
* Dependency

Equipment Facts

* Capability Set
* Availability
* Qualification

Staff Facts

* Skill Set
* Availability

Calendar Facts

* Shift
* Holiday
* Maintenance

Planning Facts are immutable during one scheduling execution.

---

# 4. What is a Constraint Specification?

A Constraint Specification describes one scheduling restriction.

It does not describe business meaning.

It does not describe solver implementation.

Instead, it expresses scheduling semantics.

Example

```text
Constraint Type

Capability

Subject

OperationInstance

Target

Equipment

Requirement

384 Head
```

---

# 5. Constraint Structure

Every Constraint Specification contains the following attributes.

Mandatory

* Constraint Category
* Source
* Target
* Parameters

Optional

* Severity
* Priority
* Description
* Metadata

The structure is intentionally generic.

---

# 6. Constraint Categories

Version 1.0 supports:

```text
Resource

Capability

Qualification

Dependency

Calendar

Policy
```

Each specification belongs to exactly one category.

Composite business behaviour is represented by multiple specifications.

---

# 7. Generation Principles

Constraint Specifications are generated automatically.

They originate from:

* Workflow Definitions
* Operation Definitions
* Planning Context
* Laboratory Definition

Users never create Constraint Specifications directly.

---

# 8. Resolution

Constraint Specifications reference business identities.

Before scheduling they are resolved into scheduling identities.

Example

Before Resolution

```text
Operation

Needs

PNG Skill
```

After Resolution

```text
Operation 143

Needs

Skill 008
```

Normalization removes business ambiguity.

---

# 9. Validation

Every Constraint Specification shall pass validation.

Validation checks include:

* Missing source
* Missing target
* Unsupported category
* Invalid parameter
* Circular dependency

Only validated specifications may enter the Constraint Model.

---

# 10. Relationship to Constraint Model

Constraint Specification represents scheduling intent.

Constraint Model represents optimization data.

Example

```text
Constraint Specification

↓

Capability Constraint

↓

Constraint Model

↓

CP-SAT Constraint
```

Constraint Specifications remain independent of mathematical formulation.

---

# 11. Architectural Rules

1. Constraint Specifications are immutable.

2. Constraint Specifications are generated automatically.

3. Constraint Specifications never reference ORM entities.

4. Constraint Specifications never contain OR-Tools objects.

5. Constraint Specifications are deterministic.

6. One Planning Fact may generate multiple Constraint Specifications.

7. Constraint Specifications are implementation-independent.

---

# 12. Future Evolution

Future versions may introduce additional specification types without changing existing Scheduling Engines.

The Scheduling Engine shall evolve by supporting new specifications rather than introducing solver-specific business logic.

Constraint Specification is expected to remain one of the most stable interfaces within the Lab APS architecture.
