# docs/05_Constraint_Framework/01_Constraint_Framework.md

# Constraint Framework

## Chapter 1 - Constraint Framework

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

The Constraint Framework defines the scheduling constraint architecture used by Lab APS.

Unlike Business Rules, which evolve continuously with laboratory operations, the Constraint Framework defines the stable categories of constraints supported by the Scheduling Engine.

Business Rules are mapped onto one or more Constraint Types.

The Constraint Framework is expected to remain stable over the lifetime of the platform.

---

# 2. Relationship with Business Rules

Business Rules describe laboratory policies.

Constraint Types describe how those policies affect scheduling.

Example

```text
Business Rule

384 PNG requires 384 Head

↓

Constraint Type

Capability Constraint

↓

Constraint Builder

↓

Solver Constraint
```

Business Rules may change.

Constraint Types should remain stable.

---

# 3. Constraint Processing Pipeline

```text
Business Rule

↓

Constraint Mapping

↓

Constraint Specification

↓

Constraint Builder

↓

Constraint Model

↓

Solver Adapter

↓

OR-Tools
```

Every scheduling rule shall pass through this pipeline.

Business Rules shall never generate OR-Tools constraints directly.

---

# 4. Constraint Categories

Version 1.0 defines the following categories.

```text
Constraint Framework

├── Resource Constraint
├── Capability Constraint
├── Qualification Constraint
├── Dependency Constraint
├── Calendar Constraint
├── Policy Constraint
└── Objective Constraint
```

Each category has a clearly defined responsibility.

---

# 5. Resource Constraint

Resource Constraints control exclusive use of schedulable resources.

Typical examples

- One Equipment executes one Operation at a time.
- One Staff executes one Operation at a time.
- One Operation occupies one Shift.

Typical properties

- Resource Type
- Capacity
- Occupation Window

Resource Constraints do not describe laboratory policies.

They describe physical resource limits.

---

# 6. Capability Constraint

Capability Constraints determine whether a resource is technically able to perform an operation.

Typical examples

- 384 Head required.
- iSWAP required.
- 16 Channel required.

Capability Constraints compare:

```text
Operation Requirement

↓

Equipment Capability
```

Capability Constraints never involve scheduling sequence.

---

# 7. Qualification Constraint

Qualification Constraints validate certification or qualification requirements.

Examples

- FV qualification must be valid.
- Operator qualification must be active.

Qualification Constraints differ from Capability Constraints.

Capability describes **can perform**.

Qualification describes **currently allowed to perform**.

---

# 8. Dependency Constraint

Dependency Constraints describe execution order.

Examples

```text
SMDP

↓

SAP
```

```text
CP

↓

SP
```

Dependency Constraints may also describe:

- Earliest Start
- Latest Finish
- Minimum Delay
- Maximum Delay

Future versions may support more dependency types.

---

# 9. Calendar Constraint

Calendar Constraints define temporal availability.

Examples

- Working Day
- Shift
- Holiday
- Staff Leave
- Equipment Maintenance

Calendar Constraints define **when** scheduling is allowed.

They do not define **who** performs the work.

---

# 10. Policy Constraint

Policy Constraints represent laboratory operating policies.

Examples

- FV required every 14 days.
- Published Plans are immutable.
- Frozen planning window.
- Planning horizon limitations.

Policy Constraints typically originate from laboratory SOPs.

---

# 11. Objective Constraint

Objective Constraints represent optimization preferences rather than feasibility.

Examples

- Maximize completed demand.
- Balance staff workload.
- Maximize equipment utilization.
- Reduce equipment switching.

Objective Constraints are implemented through the Objective Model rather than the Constraint Model.

---

# 12. Constraint Ownership

Each Constraint Category has one owner.

| Constraint    | Owner                                  |
| ------------- | -------------------------------------- |
| Resource      | Scheduling Engine                      |
| Capability    | Scheduling Engine                      |
| Qualification | Scheduling Engine                      |
| Dependency    | Workflow Generator + Scheduling Engine |
| Calendar      | Planning Context Builder               |
| Policy        | Planning Domain                        |
| Objective     | Objective Builder                      |

Business Rules do not own constraints.

They classify into existing constraint categories.

---

# 13. Constraint Specification

Every Business Rule is converted into one or more Constraint Specifications.

Each Constraint Specification contains:

- Constraint Category
- Source Entity
- Target Entity
- Parameters
- Severity
- Description

Constraint Specifications are solver-independent.

---

# 14. Hard and Soft Constraints

Constraint categories may produce either:

## Hard Constraints

Must always be satisfied.

Examples

- Resource Capacity
- Workflow Dependency
- Required Capability

Violation results in an infeasible schedule.

---

## Soft Constraints

May be violated with a penalty.

Examples

- Staff workload balance
- Equipment preference
- Preferred shift

Soft Constraints contribute to optimization objectives.

---

# 15. Extensibility

New Business Rules shall never create new solver logic directly.

Instead:

```text
New Business Rule

↓

Existing Constraint Category

↓

Constraint Specification

↓

Constraint Builder
```

A new Constraint Category shall be introduced only when an existing category cannot accurately represent the business semantics.

Creating a new category requires an Architecture Decision Record (ADR).

---

# 16. Design Rules

1. Constraint Categories are stable architectural concepts.

2. Business Rules are mapped to Constraint Categories.

3. Constraint Specifications are immutable.

4. Constraint Builders consume only Constraint Specifications.

5. Solver Adapters consume only Constraint Models.

6. Solver-specific APIs shall never appear outside the Solver Adapter.

7. New laboratory requirements should extend Business Rules before extending the Constraint Framework.

---

# 17. Version Strategy

Constraint Framework versions evolve independently from Business Rules.

Version 1.0 defines seven stable constraint categories.

Future releases may introduce additional categories only after architectural review.

Business Rules may evolve freely without changing the framework.
