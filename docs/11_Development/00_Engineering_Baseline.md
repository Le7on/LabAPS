# docs/11_Development/00_Engineering_Baseline.md

# Engineering Baseline

## Lab APS Engineering Architecture v2.0

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Status:** Frozen

**Version:** 2.0

**Date:** 2026-07-07

---

# 1. Purpose

This document defines the final engineering architecture for Lab APS.

Unlike the Software Architecture Design (SAD), which describes business architecture, this document defines how the source code is organized for long-term development.

This document is the implementation baseline for Version 1.0.

No structural changes shall be introduced without an Architecture Decision Record (ADR).

---

# 2. Engineering Philosophy

The engineering architecture follows four principles.

## Business First

Business Domains determine module boundaries.

---

## Module First

Developers work inside business modules rather than technical layers.

---

## Shared Engines

Reusable planning algorithms remain independent from business modules.

---

## Framework Isolation

Frameworks remain outside the Domain Model.

---

# 3. Project Structure

```text
LAB APS/

├── docs/
│
├── backend/
│
│   ├── app.py
│
│   ├── bootstrap/
│
│   ├── config/
│
│   ├── modules/
│   │
│   │   ├── planning/
│   │   │
│   │   │   ├── api/
│   │   │   ├── application/
│   │   │   ├── domain/
│   │   │   ├── repository/
│   │   │   ├── dto/
│   │   │   └── tests/
│   │   │
│   │   ├── laboratory/
│   │   │
│   │   ├── execution/
│   │   │
│   │   └── reporting/
│   │
│   ├── engines/
│   │
│   │   ├── planning/
│   │   ├── scheduling/
│   │   └── analysis/
│   │
│   ├── solver/
│   │
│   ├── infrastructure/
│   │
│   └── shared/
│
├── frontend/
│
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
│
├── tools/
│
├── deployment/
│
├── tests/
│
└── resources/
```

---

# 4. Backend Architecture

The backend follows a Module First architecture.

Each business module contains everything required for that domain.

Example

```text
planning/

    api/

    application/

    domain/

    repository/

    dto/

    tests/
```

Developers working on Planning rarely need to leave the Planning module.

---

# 5. Module Responsibilities

## Planning

Owns:

* Plan
* Plan Version
* Planning Context
* Workflow Instance
* Operation Instance
* Assignment

Planning is the Core Domain.

---

## Laboratory

Owns:

* Staff
* Equipment
* Workflow Definition
* Project
* Material
* Capability
* Skill

Laboratory Definition provides configuration for future planning.

---

## Execution

Owns:

* Execution Record
* Execution Log

Execution records actual laboratory activities.

---

## Reporting

Owns:

* Dashboard Queries
* KPI Queries
* Forecast Queries
* Export

Reporting is read-only.

---

# 6. Shared Engines

Business algorithms are implemented once and shared across modules.

Planning Engines

* PlanningContextBuilder
* WorkflowGenerator
* PlanningProblemBuilder

Scheduling Engines

* SchedulingModelBuilder
* ConstraintBuilder
* ObjectiveBuilder
* AssignmentBuilder

Analysis Engines

* MaterialCalculator
* KPIBuilder

Engines remain stateless.

---

# 7. Solver

The Solver remains completely isolated.

Responsibilities

* Variable generation
* Constraint translation
* Objective translation
* Optimization
* Solution parsing

Only the Solver package may import OR-Tools.

---

# 8. Infrastructure

Infrastructure contains technical implementation only.

Examples

* SQLAlchemy
* Alembic
* Logging
* Export
* Persistence

Infrastructure owns no business behaviour.

---

# 9. Frontend

Frontend is an independent Vue 3 application.

Technology stack

* Vue 3
* Vite
* Pinia
* Vue Router
* Axios

Communication with the backend occurs exclusively through REST APIs.

PyWebView acts only as the desktop host.

---

# 10. Developer Toolkit

The `tools` directory contains the Lab APS Developer CLI.

Responsibilities

* Initialize project
* Generate modules
* Generate Use Cases
* Generate Domain Entities
* Generate API skeletons
* Verify project health

The CLI is the only supported project generation mechanism.

Manual scaffolding is discouraged.

---

# 11. Dependency Rules

Allowed dependencies

```text
Frontend

↓

REST API

↓

Application

↓

Domain

↓

Engines

↓

Solver

↓

Infrastructure
```

Forbidden

* Domain → Infrastructure
* Domain → Flask
* Domain → SQLAlchemy
* Solver → Repository
* Frontend → Database

---

# 12. Development Workflow

Development proceeds by Module.

Example

Planning Feature

↓

Planning Module

↓

Planning Engine (if required)

↓

Shared Infrastructure

↓

Frontend

Developers should avoid modifying multiple unrelated modules within the same feature.

---

# 13. Git Strategy

Development is organized into:

Phase

↓

Milestone

↓

Git Commit

Every commit shall:

* compile successfully
* pass existing tests
* preserve architectural integrity

---

# 14. Frozen Engineering Decisions

The following engineering decisions are frozen.

* Module First architecture
* Vue 3 + Vite frontend
* Flask REST backend
* Shared Planning/Scheduling Engines
* Isolated Solver
* Lightweight CQRS (Repository + Query Service)
* Composition Root with Constructor Injection
* Domain-driven implementation

Future enhancements shall extend this baseline rather than replacing it.

---

# 15. Engineering Baseline

This document becomes the official engineering baseline for Lab APS Version 1.0.

Future development shall conform to this structure.

Changes to module boundaries, dependency rules or project organization require an Architecture Decision Record (ADR) before implementation.
