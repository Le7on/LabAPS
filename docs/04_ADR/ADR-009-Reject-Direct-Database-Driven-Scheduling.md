# docs/04_ADR/ADR-009-Reject-Direct-Database-Driven-Scheduling.md

# ADR-009 — Reject Direct Database-Driven Scheduling

**Status:** Accepted

**Date:** 2026-07-06

---

# Context

During implementation planning, one possible architecture was considered.

Instead of constructing a Planning Domain and Scheduling Model, the Solver could query the database directly.

The execution flow would become:

```text
Database

↓

OR-Tools

↓

Schedule

↓

Database
```

This approach appears attractive because it removes several transformation steps.

However, it fundamentally changes the responsibility of the optimization engine.

---

# Decision

Lab APS explicitly rejects direct database-driven scheduling.

The Solver shall never:

* query the database
* execute SQL
* access repositories
* understand ORM entities
* understand database relationships

The Solver shall receive only one Scheduling Model.

---

# Rejected Architecture

The following architecture shall not be implemented.

```text
Database

↓

Repository

↓

OR-Tools

↓

Database
```

Business objects are bypassed.

The Planning Domain loses control of scheduling.

---

# Accepted Architecture

The accepted architecture is:

```text
Laboratory Definition

↓

Planning Domain

↓

PlanVersion

↓

SchedulingModelBuilder

↓

Scheduling Model

↓

Solver Adapter

↓

Scheduling Solution

↓

AssignmentBuilder

↓

PlanVersion
```

The Solver remains isolated from persistence.

---

# Rationale

## Domain Ownership

Scheduling is part of the Planning Domain.

The database is only a persistence mechanism.

Allowing the Solver to query the database would move business ownership into Infrastructure.

This violates the architectural principles established by Lab APS.

---

## Testability

A Solver depending on a database cannot be tested independently.

Unit testing would require:

* ORM
* migrations
* database setup
* seed data

By introducing the Scheduling Model, the Solver can be tested entirely in memory.

---

## Replaceability

Future versions may replace:

* SQLite
* PostgreSQL
* SQLAlchemy

without changing scheduling behaviour.

Likewise, the optimization engine may change without modifying the persistence layer.

---

## Deterministic Input

The Scheduling Model represents one immutable planning snapshot.

The database represents continuously changing business data.

Optimization requires deterministic input.

Direct database access cannot guarantee this.

---

# Alternatives Considered

## Option A — Direct SQL Queries

Rejected.

Business rules become distributed between SQL and Solver code.

Maintenance becomes difficult.

---

## Option B — Repository Access Inside Solver

Rejected.

The Solver becomes dependent on Application and Infrastructure layers.

Layer boundaries are violated.

---

## Option C — ORM Entity Input

Rejected.

ORM entities contain persistence concerns.

Scheduling requires optimization concerns.

Mixing the two increases coupling.

---

## Option D — Scheduling Model

Accepted.

Scheduling receives a normalized, immutable optimization model.

Persistence and optimization remain independent.

---

# Consequences

Positive

* Clean architectural boundaries.
* Independent testing.
* Easier debugging.
* Replaceable persistence layer.
* Replaceable optimization engine.

Negative

* Additional transformation step.
* Slight increase in implementation complexity.

The additional complexity is intentional because it significantly improves long-term maintainability.

---

# Architectural Rules

1. The Solver never imports SQLAlchemy.

2. The Solver never imports Repository classes.

3. The Solver never queries the database.

4. The Solver never understands ORM entities.

5. The Scheduling Model is the only accepted optimization input.

6. AssignmentBuilder is the only component allowed to reconstruct business entities from solver output.

---

# Code Review Checklist

Reject any implementation that:

* executes SQL inside the Solver
* loads repositories inside the Solver
* passes ORM entities into the Solver
* bypasses the Scheduling Model

Such implementations violate the Lab APS architecture.

---

# Related Documents

* SAD Chapter 9 — Persistence Architecture
* SAD Chapter 14 — Solver Model
* ADR-005 — Scheduling Model as an Anti-Corruption Layer
* ADR-006 — Constraint Model
* ADR-008 — Planning Context Uses Snapshots

---

# Long-Term Impact

This decision establishes a permanent architectural boundary.

The database persists business data.

The Planning Domain owns business behaviour.

The Scheduling Model represents optimization input.

The Solver performs optimization only.

These responsibilities shall remain independent throughout the lifetime of Lab APS.
