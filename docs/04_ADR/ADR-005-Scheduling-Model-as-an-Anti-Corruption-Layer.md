# docs/04_ADR/ADR-005-Scheduling-Model-as-an-Anti-Corruption-Layer.md

# ADR-005 — Scheduling Model as an Anti-Corruption Layer

**Status:** Accepted

**Date:** 2026-07-06

---

# Context

The Planning Domain contains rich business objects.

Examples include:

* Plan
* PlanVersion
* WorkflowInstance
* OperationInstance
* Assignment
* PlanningContext

These objects represent business concepts.

However, the optimization engine (Google OR-Tools CP-SAT) requires a normalized mathematical model rather than business entities.

Two implementation approaches were considered.

Option A

```text id="adr5-001"
PlanVersion

↓

OR-Tools
```

Option B

```text id="adr5-002"
PlanVersion

↓

Scheduling Model

↓

OR-Tools
```

---

# Decision

Lab APS introduces an intermediate **Scheduling Model** between the Planning Domain and the optimization engine.

The Scheduling Model is an in-memory representation of the optimization problem.

It is created immediately before solving and discarded immediately afterwards.

The Scheduling Model is **not** a Domain Object.

The Scheduling Model is **not** persisted.

---

# Rationale

## Separation of Concerns

The Planning Domain answers:

> What needs to be done?

The Scheduling Model answers:

> What optimization problem should be solved?

The Solver answers:

> What is the optimal solution?

Each layer has one responsibility.

---

## Stable Domain Model

Business objects evolve according to laboratory requirements.

Optimization models evolve according to scheduling algorithms.

Keeping these concerns separate prevents unnecessary coupling.

---

## Replaceable Solver

The Scheduling Model does not depend on OR-Tools.

Future versions may replace OR-Tools with another optimization engine without modifying:

* Plan
* PlanVersion
* WorkflowInstance
* OperationInstance

Only the Solver Adapter changes.

---

## Testability

The Scheduling Model can be verified independently.

Examples:

* Operation count
* Resource availability
* Dependency graph
* Constraint generation

without executing the optimizer.

This significantly simplifies testing.

---

# Alternatives Considered

## Option A — Direct Domain Access

```text id="adr5-003"
PlanVersion

↓

OR-Tools
```

Rejected.

The Solver would become tightly coupled to:

* Domain objects
* Repository structure
* Business terminology

Any business change would directly affect optimization code.

---

## Option B — Database-driven Solver

```text id="adr5-004"
Database

↓

OR-Tools
```

Rejected.

The optimization engine would need to understand database schema.

Business logic would become distributed between SQL and optimization code.

Testing would become significantly more difficult.

---

## Option C — JSON-based Solver Input

Rejected.

Although serialization becomes simpler, the Scheduling Model would lose strong typing and validation.

A dedicated object model is preferred.

---

# Consequences

Positive

* Strong separation between business and optimization.
* Easier testing.
* Easier debugging.
* Solver independence.
* Cleaner architecture.

Negative

* One additional transformation step.
* Additional in-memory objects during scheduling.

These costs are acceptable because scheduling is performed periodically rather than continuously.

---

# Scheduling Model Responsibilities

The Scheduling Model shall contain only optimization concepts.

Examples

```text id="adr5-005"
Resource Set

Operation Set

Dependency Set

Calendar Set

Constraint Set

Objective Set
```

The Scheduling Model shall not contain:

* ORM entities
* Flask objects
* Repository references
* SQL
* UI concepts

---

# Architectural Rules

1. The Scheduling Model is immutable.

2. The Scheduling Model is built from one PlanVersion.

3. The Scheduling Model is never persisted.

4. OR-Tools receives only the Scheduling Model.

5. OR-Tools returns only a Scheduling Solution.

6. Business entities are reconstructed after solving.

7. The Scheduling Model is the only contract between the Planning Domain and the optimization engine.

---

# Implementation Notes

The scheduling pipeline shall always follow this sequence.

```text id="adr5-006"
PlanVersion

↓

SchedulingModelBuilder

↓

SchedulingModel

↓

ConstraintBuilder

↓

ObjectiveBuilder

↓

SolverAdapter

↓

SchedulingSolution

↓

AssignmentBuilder

↓

PlanVersion
```

No implementation shall bypass the Scheduling Model.

---

# Related Documents

* SAD Chapter 5 — Scheduling Architecture
* SAD Chapter 14 — Solver Model
* ADR-001 — Plan as the Aggregate Root
* ADR-002 — Plan + PlanVersion
* ADR-004 — Operation Definition and Operation Instance

---

# Future Considerations

The Scheduling Model is intentionally generic.

Future extensions may include:

* Batch scheduling
* Resource groups
* Alternative objective strategies
* Parallel solving
* Distributed optimization

These enhancements shall extend the Scheduling Model without changing the Planning Domain.
