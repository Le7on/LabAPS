# docs/09_UI/01_Information_Architecture.md

# User Interface Design

## Chapter 1 - Information Architecture

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Architecture Baseline

---

# 1. Purpose

This document defines the Information Architecture (IA) of Lab APS.

Information Architecture describes:

* What information the system manages
* How information is organized
* How users navigate between business capabilities

This document intentionally does not define visual layout.

Wireframes are defined in later documents.

---

# 2. Design Principles

The Information Architecture follows these principles.

### Principle 1

Organize by business activities.

Not by database tables.

---

### Principle 2

Users navigate by business tasks.

Not by system implementation.

---

### Principle 3

Planning is the center of the application.

Everything else supports Planning.

---

### Principle 4

Frequently used functions shall require the fewest navigation steps.

---

# 3. Primary Navigation

Version 1.0 contains six primary modules.

```text
Dashboard

Planning

Laboratory

Execution

Reports

Administration
```

These modules remain stable throughout the lifetime of the platform.

---

# 4. Dashboard

Dashboard answers:

> What is happening today?

Primary information includes:

* Current Planning Horizon
* Published Plans
* Equipment Status
* Planning Alerts
* Material Warnings
* Recent Activity

Dashboard is read-oriented.

No business editing occurs here.

---

# 5. Planning

Planning is the primary working area.

Planning answers:

> What should be executed?

Planning contains:

```text
Plans

Plan Versions

Planning Context

Demand

Schedule

Material Forecast

KPI
```

Typical user:

Production Laboratory Manager

Planning is expected to be the most frequently used module.

---

# 6. Laboratory

Laboratory maintains stable laboratory definitions.

Contents

```text
Staff

Equipment

Projects

Workflow Definitions

Materials

Capabilities

Skills

Shift

Calendar
```

Typical user

Laboratory Engineer

Changes made here affect future planning only.

Historical plans remain unchanged.

---

# 7. Execution

Execution answers:

> What is currently being executed?

Execution contains:

* Assignment Status
* Execution Records
* Execution History

Execution never changes planning decisions.

---

# 8. Reports

Reports answer:

> How did planning perform?

Examples

* Equipment Utilization
* Staff Utilization
* Material Forecast
* Planning KPI
* Historical Plans

Reports are read-only.

---

# 9. Administration

Administration manages application behaviour.

Contents

* Users
* Roles
* System Settings
* Solver Profiles
* Audit Logs

Administration does not contain laboratory business data.

---

# 10. Navigation Hierarchy

```text
Dashboard

Planning
    ├── Plans
    │      └── Plan Versions
    ├── Demand
    ├── Schedule
    ├── Forecast
    └── KPI

Laboratory
    ├── Staff
    ├── Equipment
    ├── Projects
    ├── Workflow Definitions
    ├── Materials
    ├── Calendars
    └── Shift

Execution
    ├── Assignments
    ├── Execution Records
    └── History

Reports
    ├── Planning
    ├── Equipment
    ├── Staff
    ├── Materials
    └── KPI

Administration
    ├── Users
    ├── Roles
    ├── Solver Profiles
    └── Audit
```

---

# 11. Ownership

Each module owns one business responsibility.

| Module         | Responsibility         |
| -------------- | ---------------------- |
| Dashboard      | Overview               |
| Planning       | Production planning    |
| Laboratory     | Laboratory definitions |
| Execution      | Runtime execution      |
| Reports        | Analysis               |
| Administration | System management      |

Responsibilities shall not overlap.

---

# 12. User Roles

Primary users

| Role                | Primary Module     |
| ------------------- | ------------------ |
| PI                  | Dashboard, Reports |
| Production LM       | Planning           |
| Laboratory Engineer | Laboratory         |
| Operator            | Execution          |
| Administrator       | Administration     |

The navigation is optimized for these primary responsibilities.

---

# 13. Information Flow

The information flow through the application follows the business lifecycle.

```text
Laboratory

↓

Planning

↓

Execution

↓

Reports
```

Dashboard summarizes all stages.

Administration supports all stages.

---

# 14. Navigation Rules

1. Every business object has exactly one primary location.

2. Users should never edit the same information from multiple modules.

3. Planning remains the central navigation hub.

4. Dashboard provides entry points rather than editing functionality.

5. Reports never modify business data.

---

# 15. Future Expansion

Future modules may include:

* Simulation
* Scenario Planning
* AI Assistant
* Notifications
* Integrations

New modules shall integrate into the existing navigation hierarchy rather than replacing it.

The Information Architecture shall remain stable as the platform evolves.
