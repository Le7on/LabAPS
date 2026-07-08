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

Implementation has progressed through Phases 1-6 (first working slices across the
stack):

- Phase 1 – Bootstrap: developer CLI + code generators, backend framework.
- Phase 2 – Infrastructure: SQLAlchemy, Unit of Work, Alembic.
- Phase 3 – Planning Domain: Plan aggregate + Plan Version lifecycle
  (Working -> Scheduled -> Reviewed -> Published -> Archived, immutability
  enforced).
- Phase 4 – Scheduling Engine: OR-Tools CP-SAT with resource assignment
  (equipment by capability, staff by skill), scheduling from persisted Workflow
  Definitions, persisted Assignments.
- Phase 5 – Execution: assignment lifecycle (start/complete/fail/cancel) with an
  append-only audit trail.
- Phase 6 – Reporting: dashboard counts + KPI/equipment utilization (read-only
  query services).
- Frontend SPA: dashboard, plans, equipment, staff, workflow definitions and an
  end-to-end scheduling view.

For the full build state and traceability, see
[IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md). Per-milestone delivery docs
and the session index are under
[12_Development_Log/](12_Development_Log/AUTONOMOUS_SESSION_2026-07-07.md).

Current focus:

- Operation Instances, calendar/qualification constraints, a real objective
  model (once Demand is modelled), and authentication.

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

Phases 1-6 have working slices end to end. Candidate next milestones:

- Model Operation Instances so Assignments reference persisted instances.
- Calendar / availability and qualification constraints in the scheduler.
- A real objective model once Demand is modelled (replacing interim makespan).
- Authentication / authorization at the Composition Root.

See [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) for the current build
state and known gaps.
