# docs/11_Development/03_Dependency_Injection_Strategy.md

# Development Guide

## Chapter 3 - Dependency Injection Strategy

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Development Baseline

---

# 1. Purpose

This document defines how application components are created and connected at runtime.

Lab APS adopts a lightweight dependency injection strategy based on:

* Composition Root
* Constructor Injection

The objective is to keep the architecture explicit, testable and easy to understand.

---

# 2. Design Philosophy

Business components shall never create their own dependencies.

Instead:

* Dependencies are constructed once.
* Dependencies are injected.
* Dependencies are owned by the runtime composition.

Object creation belongs to the Application startup process.

Business logic never performs object construction.

---

# 3. Composition Root

The Composition Root is the only place where object graphs are assembled.

```text
Application Start

↓

Application Factory

↓

Build Infrastructure

↓

Build Repositories

↓

Build Engines

↓

Build Use Cases

↓

Register API

↓

Launch UI
```

No other module shall assemble business objects.

---

# 4. Dependency Flow

Dependencies always flow toward the business.

```text
Configuration

↓

Infrastructure

↓

Repository

↓

Engine

↓

Use Case

↓

API
```

Reverse dependencies are prohibited.

---

# 5. Constructor Injection

Every component receives its dependencies through its constructor.

Example

Use Case depends on

* Repository
* Planning Engine

Planning Engine depends on

* Scheduling Engine

Scheduling Engine depends on

* Solver Adapter

Components never instantiate these objects internally.

---

# 6. Repository Lifetime

Repositories are application-scoped.

One repository instance is reused during the lifetime of the application.

Repositories obtain database sessions through the persistence layer rather than owning them.

---

# 7. Engine Lifetime

All Engines are stateless.

Examples

* WorkflowGenerator
* PlanningProblemBuilder
* SchedulingModelBuilder
* ConstraintBuilder
* ObjectiveBuilder
* AssignmentBuilder
* MaterialCalculator

Because Engines contain no mutable state, they may be reused safely.

---

# 8. Solver Lifetime

The Solver Adapter is also stateless.

Each scheduling request creates a new optimization model.

The Solver Adapter never caches optimization state between scheduling executions.

---

# 9. Use Case Lifetime

Use Cases are lightweight coordinators.

Each execution follows:

```text
Receive Request

↓

Load Aggregate

↓

Invoke Domain

↓

Persist Changes

↓

Return DTO
```

Use Cases shall never retain internal state.

---

# 10. Session Management

Database sessions are managed by the Application Layer.

Rules

* One Use Case = One Unit of Work.
* Commit only after successful completion.
* Roll back on any exception.

Repositories shall never commit transactions.

---

# 11. Testability

Constructor Injection enables dependency replacement.

Examples

Production

```text
PlanRepository
```

Testing

```text
FakePlanRepository
```

Production

```text
ORToolsSolverAdapter
```

Testing

```text
FakeSolverAdapter
```

No code changes are required to switch implementations.

---

# 12. Dependency Rules

The following dependencies are allowed.

| Component         | Depends On            |
| ----------------- | --------------------- |
| API               | Use Cases             |
| Use Cases         | Repositories, Engines |
| Planning Engine   | Scheduling Engine     |
| Scheduling Engine | Solver Adapter        |
| Repository        | Persistence           |
| Persistence       | SQLAlchemy            |

No dependency may point upward.

---

# 13. Prohibited Patterns

The following patterns are prohibited.

Service Locator

Components shall not retrieve dependencies from a global registry.

---

Singleton Business Objects

Domain objects shall never be implemented as singletons.

---

Framework Injection

Domain objects shall never receive Flask Request, SQLAlchemy Session or OR-Tools objects.

---

Hidden Object Creation

Business components shall never instantiate repositories or engines internally.

---

# 14. Architectural Rules

1. The Composition Root is the only object assembly location.

2. Constructor Injection is mandatory.

3. Dependencies are explicit.

4. Engines remain stateless.

5. Repositories never manage transactions.

6. Domain objects remain framework-independent.

7. Test implementations shall be replaceable without changing production code.

---

# 15. Future Evolution

If the application evolves into:

* Multi-user Web deployment
* Distributed scheduling
* Background worker architecture

the Composition Root may later be replaced by a dedicated Dependency Injection container.

The business architecture shall remain unchanged.
