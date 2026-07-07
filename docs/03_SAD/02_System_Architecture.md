# docs/03_SAD/02_System_Architecture.md

# Software Architecture Design

## Chapter 2 - System Architecture

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Draft

---

# 1. Purpose

This document defines the overall software architecture of Lab APS.

It describes how software components collaborate to transform laboratory production demand into executable laboratory plans.

This chapter focuses on software architecture rather than business requirements.

---

# 2. Architectural Goals

The architecture is designed to satisfy the following objectives.

- High Maintainability
- Clear Separation of Responsibilities
- Configurable Laboratory Definition
- Replaceable Scheduling Engine
- Reproducible Planning
- Future Extensibility

---

# 3. Architectural Style

Lab APS adopts a layered architecture combined with Domain-Driven Design (DDD).

```text
Presentation Layer

↓

Application Layer

↓

Domain Layer

↓

Infrastructure Layer
```

Each layer has a clearly defined responsibility.

Dependencies shall always point downward.

---

# 4. High-Level Architecture

```text
                    Desktop UI
               (PyWebView + HTML)

                       │

                Flask REST API

                       │

              Application Services

                       │

        ┌──────────────┼──────────────┐
        │              │              │

        ▼              ▼              ▼

 Master Data      Planning        Reporting

        │              │

        │              ▼

        │        Scheduling Engine

        │              │

        │              ▼

        │        Solver Adapter

        │              │

        └──────────────▼

                Infrastructure

      SQLite / PostgreSQL / Files / Logs
```

Business modules never communicate directly with OR-Tools.

---

# 5. Layer Responsibilities

## 5.1 Presentation Layer

Responsibilities

- Desktop User Interface
- User Interaction
- Data Presentation
- Input Validation
- Gantt Chart
- Dashboard

Technology

- PyWebView
- HTML5
- Bootstrap
- JavaScript

The Presentation Layer shall not contain business logic.

---

## 5.2 Application Layer

The Application Layer coordinates use cases.

Typical responsibilities include:

- Create Plan
- Generate Schedule
- Publish Plan
- Export Report

Application Services coordinate multiple domain services.

Business rules do not belong here.

---

## 5.3 Domain Layer

The Domain Layer contains all business knowledge.

The Domain Layer owns:

- Plan
- Demand
- Planning Context
- Workflow Generator
- Scheduling Policies
- Material Calculator

The Domain Layer is independent of:

- Flask
- SQLAlchemy
- OR-Tools
- Database

---

## 5.4 Infrastructure Layer

Responsibilities

- Database
- ORM
- Logging
- File Export
- Solver Adapter

Infrastructure implements technical details only.

---

# 6. Business Modules

The system is divided into business modules.

```text
Master Data

Configuration

Planning

Scheduling

Execution

Material Forecast

Reporting
```

Planning is the Core Domain.

---

# 7. Planning Module

Planning is responsible for the complete planning lifecycle.

```text
Plan

│

├── Demand

├── Planning Context

├── Workflow Generator

├── Planner

├── Publisher

└── Version Manager
```

Planning owns all planning-related business objects.

Planning does not know OR-Tools.

---

# 8. Scheduling Module

Scheduling is an independent optimization module.

Responsibilities

- Build Variables
- Build Constraints
- Define Objectives
- Invoke Solver
- Parse Solver Results

Input

Operations

Output

Assignments

Scheduling owns optimization only.

---

# 9. Master Data Module

Master Data maintains stable laboratory definitions.

Objects include

- Staff
- Equipment
- Capability
- Skill
- Workflow Template
- Material Definition

Master Data never stores planning results.

---

# 10. Configuration Module

Configuration defines operational behavior.

Objects include

- Shift
- Holiday
- Leave
- Maintenance
- Solver Profile

Configuration data may change frequently.

Configuration never owns business objects.

---

# 11. Execution Module

Execution tracks plan execution.

Responsibilities

- Assignment Status
- Plan Progress
- Execution History

Execution shall never modify scheduling decisions.

Execution records reality.

Planning creates intention.

---

# 12. Material Forecast Module

Material Forecast calculates expected material usage.

Input

Published Schedule

Output

- Daily Consumption
- Weekly Consumption
- Material Warning

Material Forecast is deterministic.

It never affects scheduling.

---

# 13. Reporting Module

Reporting consumes information from other modules.

Responsibilities

- Dashboard
- Schedule Export
- KPI
- Utilization Report
- Material Report

Reporting contains no business rules.

---

# 14. Module Dependencies

The allowed dependency graph is shown below.

```text
Presentation

↓

Application

↓

Planning

├────────► Scheduling

├────────► Master Data

├────────► Configuration

├────────► Material Forecast

└────────► Reporting

Infrastructure
```

The following dependencies are prohibited.

- Reporting → Planning
- Execution → Scheduling
- Scheduling → Master Data Repository
- Scheduling → Database

---

# 15. Solver Isolation

The optimization engine shall always be isolated behind a Solver Adapter.

```text
Planning

↓

Scheduling

↓

Solver Adapter

↓

Google OR-Tools
```

No business module may directly reference OR-Tools classes.

This allows future replacement of the optimization engine.

---

# 16. Repository Rule

Each module owns its own repositories.

Example

```text
planning/

    repository/

masterdata/

    repository/

execution/

    repository/
```

Repositories shall not be shared across modules.

Cross-module communication shall occur through Application Services.

---

# 17. Error Handling

Business validation errors shall be detected before scheduling.

Examples

- Missing Workflow Template
- Missing Equipment Capability
- Missing Staff Skill
- Invalid Planning Calendar

Scheduling errors shall only represent optimization failures.

---

# 18. Architectural Constraints

The following rules are mandatory.

1. Planning is the Core Domain.

2. Scheduling is an Optimization Service.

3. OR-Tools is an Infrastructure dependency.

4. Workflow Generator belongs to Planning.

5. Material Forecast is generated after scheduling.

6. Configuration defines behavior.

7. Master Data defines laboratory resources.

8. Every published schedule shall be reproducible.

---

# 19. Future Evolution

The architecture is designed to support future extensions without changing the core domain.

Future modules may include:

- Scenario Planning
- Dynamic Rescheduling
- LIMS Connector
- Instrument Connector
- AI Recommendation
- Notification Center
- Audit Center

These modules shall integrate through Application Services without modifying existing domain responsibilities.
