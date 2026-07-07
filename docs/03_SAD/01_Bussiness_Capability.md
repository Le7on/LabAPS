# docs/03_SAD/01_Business_Capability.md

# Software Architecture Design

## Chapter 1 - Business Capability Architecture

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Draft

---

# 1. Purpose

This document defines the business capability architecture of Lab APS.

Business Capabilities represent what the platform is able to do.

Business Capabilities are independent of:

- User Interface
- Database
- Programming Language
- Framework
- OR-Tools

They represent stable business responsibilities.

The architecture of the entire software shall be organized around these capabilities.

---

# 2. Design Principle

Lab APS follows a **Capability-Oriented Architecture**.

Each module owns one business capability.

Business capabilities communicate through Application Services.

No capability shall directly manipulate another capability's internal data.

---

# 3. Capability Map

The complete business capability map is shown below.

```text
                         Lab APS

                                │
        ┌───────────────────────┼────────────────────────┐
        │                       │                        │
        ▼                       ▼                        ▼

 Master Data             Planning                 Execution

        │                       │                        │
        ▼                       ▼                        ▼

 Configuration          Scheduling              Material Forecast

                                │
                                ▼

                           Reporting
```

Planning is the central capability of the platform.

---

# 4. Core Capability

The platform revolves around one core capability.

```text
Planning
```

Everything else exists to support Planning.

Planning owns:

- Plan
- Demand
- Workflow Instance
- Assignment
- Material Forecast

Planning is therefore the Core Domain.

---

# 5. Supporting Capabilities

## 5.1 Master Data

Provides stable laboratory information.

Responsibilities

- Staff
- Equipment
- Workflow Template
- Capability
- Skill
- Material Definition

Master Data never performs scheduling.

---

## 5.2 Configuration

Defines operational parameters.

Responsibilities

- Shift
- Holiday
- Leave
- Maintenance
- Solver Profile

Configuration modifies planning behavior.

Configuration never owns business data.

---

## 5.3 Workflow

Responsible for converting laboratory Projects into executable Operations.

Responsibilities

- Workflow Template
- Workflow Instance Generation
- Dependency Generation
- Intermediate Resource Generation
- Material BOM Resolution

Workflow owns execution logic.

Workflow does not own scheduling.

---

## 5.4 Scheduling

Responsible for optimization.

Responsibilities

- Variable Builder
- Constraint Builder
- Objective Builder
- Solver Adapter
- Result Parser

Scheduling receives Operations.

Scheduling returns Assignments.

Scheduling never owns Workflow logic.

---

## 5.5 Execution

Responsible for execution tracking.

Responsibilities

- Assignment Status
- Workflow Progress
- Plan Progress

Execution never changes scheduling logic.

---

## 5.6 Material Forecast

Responsible for material estimation.

Responsibilities

- Material Consumption
- Daily Summary
- Weekly Summary
- Inventory Warning

Material Forecast is derived from the Schedule.

---

## 5.7 Reporting

Responsible for information presentation.

Responsibilities

- KPI
- Utilization
- Schedule Export
- Material Report

Reporting owns no business logic.

---

# 6. Capability Dependency

Business Capabilities communicate only through defined interfaces.

```text
Master Data
      │
      ▼
 Planning
      │
      ▼
 Workflow
      │
      ▼
 Scheduling
      │
      ▼
 Assignment
      │
      ├────────► Execution
      │
      ├────────► Material Forecast
      │
      └────────► Reporting
```

Execution never calls Scheduling.

Reporting never calls Workflow.

Material Forecast never modifies Planning.

---

# 7. Capability Responsibilities

| Capability        | Owns                   | Does NOT Own     |
| ----------------- | ---------------------- | ---------------- |
| Master Data       | Laboratory Definitions | Plans            |
| Configuration     | Planning Parameters    | Business Objects |
| Planning          | Plans                  | Equipment        |
| Workflow          | Operations             | Scheduling       |
| Scheduling        | Assignments            | Workflow Logic   |
| Execution         | Progress               | Planning         |
| Material Forecast | Forecast               | Inventory        |
| Reporting         | Reports                | Business Logic   |

---

# 8. Architectural Rules

The following rules shall always be respected.

### Rule 1

Planning is the Core Domain.

---

### Rule 2

Workflow is responsible for generating executable Operations.

---

### Rule 3

Scheduling is responsible only for optimization.

---

### Rule 4

Execution shall never modify Assignments created by Scheduling.

---

### Rule 5

Material Forecast shall never participate in scheduling optimization.

---

### Rule 6

Reporting shall consume business data only.

It shall never contain business logic.

---

### Rule 7

Business Capabilities shall remain stable even if the implementation technology changes.

---

# 9. Mapping to Source Code

Each capability shall map directly to one application module.

```text
src/

masterdata/

configuration/

planning/

workflow/

scheduling/

execution/

material/

reporting/
```

Each module owns:

```text
api/

service/

domain/

repository/

dto/
```

No module shall directly access another module's repository.

---

# 10. Future Extension

Future capabilities shall be added as independent modules.

Examples

- Scenario Planning
- Notification Center
- LIMS Connector
- Instrument Connector
- AI Recommendation
- Audit Center

Existing capabilities should not require redesign to support these extensions.

The capability architecture shall remain stable throughout the lifetime of the platform.
