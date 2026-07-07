# docs/PROJECT_CONTEXT.md

# Lab APS Project Context

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Current Phase:** Implementation — Phase 1 (Bootstrap)

**Architecture Status:** Frozen (Baseline v1)

**Document Version:** 1.1

**Last Updated:** 2026-07-07

---

# Project Goal

Lab APS is a laboratory Advanced Planning & Scheduling (APS) platform designed for automated laboratory production planning.

The system transforms production demand into executable laboratory schedules while considering:

- Equipment capability
- Operator skill
- Workflow dependency
- Qualification requirements
- Calendar availability
- Optimization objectives

The platform focuses on planning rather than laboratory execution.

---

# Current Development Phase

The Architecture Design Phase is complete and the architecture baseline is frozen.

Implementation has progressed through Phases 1-4 (core scaffolds):

- Phase 1 – Bootstrap (M1.1) + M1.2 Backend Framework (Flask app factory,
  config, logging, Composition Root)
- Phase 2 – Infrastructure (SQLAlchemy, session, repository, Alembic)
- Phase 3 – Planning Domain (Plan aggregate vertical slice: domain, repository,
  use cases, REST API)
- Phase 4 – Scheduling Engine scaffold (PlanningProblem -> SchedulingModel ->
  OR-Tools CP-SAT SolverAdapter -> AssignmentBuilder)

See the session log: [12_Development_Log/AUTONOMOUS_SESSION_2026-07-07.md](12_Development_Log/AUTONOMOUS_SESSION_2026-07-07.md).

Current focus:

- Wire GenerateSchedule use case to persisted Plan Versions; extend to
  laboratory/execution/reporting modules and the frontend.

---

# Architecture Freeze

The following architectural decisions are considered frozen.

## Core Domain

Planning is the Core Domain.

Laboratory Definition and Planning are separate domains.

Execution is a supporting domain.

---

## Aggregate Root

Plan is the Aggregate Root.

Plan owns one or more Plan Versions.

---

## Versioning

Every scheduling execution creates a new Plan Version.

Published Plan Versions are immutable.

---

## Workflow

Workflow Definition belongs to Laboratory Definition.

Workflow Instance belongs to Plan Version.

Operation Definition belongs to Workflow Definition.

Operation Instance belongs to Workflow Instance.

Assignments always reference Operation Instances.

---

## Planning Context

Each Plan Version owns one immutable Planning Context.

Planning Context stores scheduling snapshots.

Planning never depends on live configuration after scheduling begins.

---

## Scheduling

Scheduling is an internal service of the Planning Domain.

OR-Tools is isolated through the Solver Adapter.

Business objects never enter the Solver directly.

---

## Solver Architecture

Planning Domain

↓

Planning Problem

↓

Scheduling Model

↓

Solver Adapter

↓

Scheduling Solution

↓

Assignment Builder

---

## Constraint Framework

Business Rules

↓

Constraint Specification

↓

Constraint Model

↓

Solver Adapter

Constraint categories are stable.

Business Rules evolve independently.

---

# Technology Stack

Backend

- Python
- Flask
- SQLAlchemy
- Alembic

Desktop

- PyWebView
- HTML
- Bootstrap
- JavaScript

Optimization

- Google OR-Tools (CP-SAT)

Database

- SQLite (Development)
- PostgreSQL (Future)

---

# Current Document Status

Completed

- Vision
- Terminology
- SRS
- SAD
- ADR
- Constraint Framework

Pending

- Physical ERD
- OpenAPI Specification
- UI Wireframe
- Solver Design Specification

Future

- Development
- Testing
- Deployment

---

# Working Rules

1. Architecture changes require an ADR.

2. Business objects must remain stable.

3. The Planning Domain owns scheduling.

4. Business Rules are expected to evolve.

5. The Constraint Framework should remain stable.

6. The Domain Model shall always drive the database, APIs and implementation.

---

# Next Task

Continue with Milestone **M1.2 – Backend Framework**:

- Flask Application Factory (`backend/app.py`)
- Configuration loading (`backend/config`)
- Logging initialization
- Dependency Composition Root

See [11_Development/00_Project_Bootstrap_Plan.md](11_Development/00_Project_Bootstrap_Plan.md) section 14.
