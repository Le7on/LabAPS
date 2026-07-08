# docs/ARCHITECTURE_LOG.md

# Lab APS Architecture Log

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

---

## Current Phase

Implementation — Phases 1-6 have working slices (backend + frontend)

Status

🟢 In Progress (Bootstrap, Infrastructure, Planning + lifecycle, Scheduling with
resource assignment + persistence, Execution + audit, Reporting, and the SPA all
have first working slices)

Architecture Baseline

Version 1.0 (Frozen)

See [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) for the detailed build
state and traceability.

---

# Completed Artifacts

## Vision

- Vision
- Terminology

Status

✅ Complete

---

## Software Requirement Specification (SRS)

- Introduction
- Business Background
- Business Process
- Functional Requirements
- Business Object Model

Status

✅ Complete

---

## Software Architecture Design (SAD)

Completed

- Business Capability
- System Architecture
- Domain Architecture
- Plan Aggregate
- Scheduling Architecture
- Application Architecture
- Conceptual Database Model
- Plan Lifecycle
- Plan Version Architecture
- Persistence Architecture
- Conceptual ERD
- Physical Database Design
- Architecture Constraints
- Solver Model
- Module Interaction
- API Architecture
- Deployment Architecture
- Coding Guidelines
- Project Structure
- Development Workflow

Status

✅ Complete

---

## Architecture Decision Records (ADR)

Completed

- ADR-001
- ADR-002
- ADR-003
- ADR-004
- ADR-005
- ADR-006
- ADR-007
- ADR-008
- ADR-009
- ADR-010

Status

✅ Complete

---

## Constraint Framework

Completed

- Constraint Framework
- Constraint Mapping
- Constraint Specification

Status

✅ Complete

---

# Frozen Architectural Decisions

The following architectural decisions are considered stable.

## Domain

Planning is the Core Domain.

Laboratory Definition and Planning are separate domains.

Execution is a supporting domain.

---

## Aggregate

Plan is the Aggregate Root.

Plan owns multiple Plan Versions.

---

## Planning

Planning Context uses immutable snapshots.

Workflow Definition is separated from Workflow Instance.

Operation Definition is separated from Operation Instance.

---

## Scheduling

Scheduling receives a Planning Problem.

Scheduling builds a Scheduling Model.

Solver receives only the Scheduling Model.

Assignments are reconstructed after solving.

---

## Optimization

Constraint Model and Objective Model are independent.

OR-Tools is isolated behind the Solver Adapter.

Business Rules never generate OR-Tools constraints directly.

---

## Persistence

Planning data is versioned.

Published Plan Versions are immutable.

Repositories exist only for Aggregate Roots.

---

# Current Project Status

Architecture

██████████████████████████████ 100%

Requirements

██████████████████████████████ 100%

Domain Design

██████████████████████████████ 100%

Database Design

██████████████████████████░░░░ 80%

API Design

░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0%

UI Prototype

░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0%

Implementation

██░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 5%

Testing

░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0%

---

# Current Milestone

Phase 1 – Bootstrap

Completed

M1.1 – Developer CLI and project skeleton generation

Current Target

M1.2 – Backend Framework

Deliverables

- Flask Application Factory
- Configuration loading
- Logging initialization
- Dependency Composition Root

---

# Next Artifact

```text
backend/app.py
```

Goal

Introduce the Flask Application Factory and runtime composition on top of the generated skeleton, per Development Guide chapters 1–3.

---

# Development Readiness Checklist

| Item                        | Status |
| --------------------------- | ------ |
| Vision                      | ✅     |
| Terminology                 | ✅     |
| SRS                         | ✅     |
| SAD                         | ✅     |
| ADR                         | ✅     |
| Constraint Framework        | ✅     |
| Physical ERD                | ✅     |
| Data Dictionary             | ✅     |
| OpenAPI                     | ⏳     |
| UI Wireframe                | ⏳     |
| Solver Design Specification | ⏳     |

Implementation shall begin only after all items above are complete.

---

# Resume Instruction

To resume the project in a new conversation:

1. Provide `PROJECT_CONTEXT.md`.
2. Provide `ARCHITECTURE_INDEX.md`.
3. Provide this Architecture Log.
4. State the next artifact to produce.

Example

> Continue Lab APS. Architecture Baseline v1.0 is frozen. Implementation Phase 1 – Bootstrap is underway; M1.1 is complete. Next milestone: M1.2 – Backend Framework (`backend/app.py`).

No previous conversation history is required.
