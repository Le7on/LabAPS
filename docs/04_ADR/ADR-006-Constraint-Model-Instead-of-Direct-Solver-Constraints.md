# docs/04_ADR/ADR-006-Constraint-Model-Instead-of-Direct-Solver-Constraints.md

# ADR-006 — Introduce a Constraint Model Instead of Building OR-Tools Constraints Directly

**Status:** Accepted

**Date:** 2026-07-06

---

# Context

Lab APS uses Google OR-Tools CP-SAT as the optimization engine.

Business rules originating from laboratory operations must ultimately become mathematical constraints.

The straightforward implementation would be:

```text
Business Rule

↓

Constraint Builder

↓

OR-Tools Constraint
```

However, this tightly couples laboratory business rules with a specific optimization engine.

As the number of business rules grows, the Constraint Builder would become increasingly complex and difficult to maintain.

---

# Decision

Lab APS introduces a dedicated **Constraint Model**.

The scheduling pipeline becomes:

```text
Business Rule

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

The Constraint Model becomes the stable contract between business rules and the optimization engine.

---

# Rationale

## Separate Business Semantics from Solver Implementation

Business rules describe laboratory behaviour.

Examples include:

* Equipment capacity
* Staff availability
* Workflow dependency
* FV qualification
* Shift availability

These concepts should exist independently of any optimization library.

The optimization engine only receives normalized constraint definitions.

---

## Stable Business Layer

Business rules change according to laboratory requirements.

Optimization implementations change according to solver technology.

Keeping these concerns separate reduces long-term coupling.

---

## Replaceable Optimization Engine

Future versions may replace OR-Tools with another optimization engine.

Examples:

* Gurobi
* CPLEX
* Timefold
* OptaPlanner

Only the Solver Adapter requires modification.

The Constraint Model remains unchanged.

---

## Better Testing

Constraint Specifications and Constraint Models can be verified without executing the Solver.

Examples include:

* Number of generated constraints
* Constraint categories
* Resource mappings
* Dependency mappings

This allows deterministic unit testing.

---

# Constraint Categories

Version 1.0 defines the following constraint categories.

## Resource Constraints

Examples

* Equipment Capacity
* Staff Capacity

---

## Requirement Constraints

Examples

* Required Capability
* Required Skill

---

## Dependency Constraints

Examples

* Finish-to-Start
* Intermediate Resource Availability

---

## Calendar Constraints

Examples

* Working Days
* Holidays
* Leave
* Maintenance

---

## Qualification Constraints

Examples

* FV Qualification

---

## Policy Constraints

Examples

* Maximum Planning Horizon
* Frozen Plan Rules
* Published Version Protection

---

# Constraint Specification

A Constraint Specification describes one business rule in a normalized form.

Typical attributes include:

* Constraint Type
* Source Object
* Target Object
* Parameters
* Severity

Constraint Specifications are independent of OR-Tools.

---

# Constraint Builder

Constraint Builder converts Constraint Specifications into the Constraint Model.

Responsibilities include:

* Resolve references
* Normalize values
* Validate completeness
* Group related constraints

Constraint Builder does not invoke OR-Tools.

---

# Constraint Model

The Constraint Model contains only solver-independent constraint objects.

Typical contents include:

```text
Constraint Model

├── Resource Constraints
├── Dependency Constraints
├── Calendar Constraints
├── Requirement Constraints
└── Policy Constraints
```

The Constraint Model is immutable.

It exists only during scheduling.

---

# Solver Adapter

The Solver Adapter converts the Constraint Model into solver-specific constraints.

Responsibilities include:

* Create OR-Tools variables
* Translate Constraint Model
* Register constraints
* Execute optimization

Business rules are never interpreted inside the Solver Adapter.

---

# Alternatives Considered

## Option A — Direct OR-Tools Constraint Generation

Rejected.

Business rules become tightly coupled with OR-Tools APIs.

Changing the optimization engine would require widespread code changes.

---

## Option B — Constraint Model

Accepted.

Business semantics remain stable while solver implementation remains replaceable.

The architecture becomes easier to understand and easier to test.

---

# Consequences

Positive

* Clear separation between business rules and optimization implementation.
* Easier maintenance.
* Easier testing.
* Cleaner architecture.
* Solver independence.

Negative

* Additional transformation layer.
* Slight increase in implementation complexity.

The benefits significantly outweigh the additional implementation effort.

---

# Architectural Rules

1. Business Rules never generate OR-Tools constraints directly.

2. Constraint Specifications are solver-independent.

3. Constraint Models are immutable.

4. Solver Adapter consumes only the Constraint Model.

5. Constraint Builder contains no optimization logic.

6. Solver-specific APIs shall never appear outside the Solver Adapter.

---

# Related Documents

* SAD Chapter 5 — Scheduling Architecture
* SAD Chapter 14 — Solver Model
* ADR-005 — Scheduling Model as an Anti-Corruption Layer

---

# Future Considerations

Future versions may introduce configurable optimization policies.

The Constraint Model provides a stable foundation for these enhancements without changing business rules or the Planning Domain.
