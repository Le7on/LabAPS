# docs/11_Development/00_Project_Bootstrap_Plan.md

# Project Bootstrap Plan

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.1

**Status:** Approved

---

# 1. Purpose

This document defines the engineering execution plan for implementing Lab APS.

Architecture design is considered complete.

From this point onward, development shall follow incremental milestones.

Each milestone must produce:

- Runnable code
- Testable functionality
- Git commits
- Updated documentation (if required)

---

# 2. Engineering Principles

Development follows these principles.

1. Every milestone must compile and run.

2. Every milestone must be independently testable.

3. No milestone leaves the project in a broken state.

4. Architecture changes require an ADR.

5. Business rules evolve through Business Rule documents, not code comments.

---

# 3. Project Roadmap

```text id="bp001"
Phase 0

Architecture

✓ Complete

↓

Phase 1

Bootstrap

↓

Phase 2

Infrastructure

↓

Phase 3

Planning Domain

↓

Phase 4

Scheduling Engine

↓

Phase 5

Execution

↓

Phase 6

Reporting

↓

Phase 7

Release 1.0
```

---

# 4. Phase 1 - Bootstrap

Objective

Create a runnable project skeleton.

Deliverables

- Developer CLI
- Project Generator
- Backend Skeleton
- Frontend Skeleton
- Configuration
- Logging
- VS Code Workspace

Milestones

M1.1

Bootstrap CLI

M1.2

Template Engine

M1.3

Backend Skeleton

M1.4

Frontend Skeleton

M1.5

Development Environment

Exit Criteria

The application starts successfully.

---

# 5. Phase 2 - Infrastructure

Objective

Build the technical foundation.

Deliverables

- SQLAlchemy
- Alembic
- Database Session
- Repository Framework
- Query Framework
- Logging
- Exception Handling

Exit Criteria

Database migration executes successfully.

---

# 6. Phase 3 - Planning Domain

Objective

Implement business aggregates.

Deliverables

- Plan
- Plan Version
- Planning Context
- Workflow Instance
- Operation Instance

Exit Criteria

Planning objects pass all unit tests.

---

# 7. Phase 4 - Scheduling Engine

Objective

Implement planning and optimization.

Deliverables

- Planning Problem Builder
- Scheduling Model Builder
- Constraint Builder
- Objective Builder
- Solver Adapter
- Assignment Builder

Exit Criteria

Generate Schedule produces valid Assignments.

---

# 8. Phase 5 - Execution

Objective

Support execution tracking.

Deliverables

- Assignment Execution
- Execution Record
- Execution History

Exit Criteria

Assignments can be executed through the UI.

---

# 9. Phase 6 - Reporting

Objective

Provide operational visibility.

Deliverables

- Dashboard
- KPI
- Equipment Utilization
- Material Forecast
- Export

Exit Criteria

Planning reports are available.

---

# 10. Git Strategy

Every milestone consists of multiple Git commits.

Example

```text id="bp002"
Milestone 1.1

Commit 001

Developer CLI

Commit 002

Manifest

Commit 003

Template Engine

Commit 004

Bootstrap Engine
```

Every commit must leave the project runnable.

---

# 11. Branch Strategy

```text id="bp003"
main

↓

develop

↓

feature/<feature-name>
```

Only reviewed code may be merged into `main`.

---

# 12. Definition of Done

A milestone is complete only if:

- Code builds successfully.
- Unit tests pass.
- Documentation is updated.
- No architectural violations exist.
- Code review is completed.

---

# 13. Engineering Rules

1. Business architecture is frozen.

2. Implementation evolves incrementally.

3. Every milestone produces executable software.

4. Technical debt shall be addressed before entering the next phase.

5. Architecture documents remain synchronized with implementation.

---

# 14. Current Milestone

Current Phase

Phase 4 – Scheduling Engine (scaffold complete)

Completed Phases

- Phase 1 – Bootstrap (M1.1) + M1.2 Backend Framework
- Phase 2 – Infrastructure (SQLAlchemy, session, repository, Alembic)
- Phase 3 – Planning Domain (Plan aggregate vertical slice)
- Phase 4 – Scheduling Engine scaffold (PlanningProblem -> SchedulingModel ->
  OR-Tools CP-SAT SolverAdapter -> AssignmentBuilder)

Current Objective

Wire the SchedulingEngine into a generate-schedule use case against persisted
Plan Versions, then extend to the laboratory/execution/reporting modules.

See the session log: [../12_Development_Log/AUTONOMOUS_SESSION_2026-07-07.md](../12_Development_Log/AUTONOMOUS_SESSION_2026-07-07.md).

---

# 15. Next Immediate Tasks

Phases 1-4 core deliverables are implemented and tested (14 passing tests).

The next engineering tasks are:

1. PlanVersion API (create/approve/publish) on the Plan aggregate
2. GenerateSchedule use case wiring SchedulingEngine to a persisted Plan Version
3. Laboratory module (Equipment, Staff, Workflow Definition)
4. Frontend views consuming the REST API
5. Push local commits once GitHub is reachable

Business development begins only after the bootstrap framework is stable.
