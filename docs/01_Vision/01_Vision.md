# docs/01_Vision/Vision.md

# Lab APS Vision

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Draft

---

# 1. Purpose

Lab APS is designed to provide an intelligent planning and scheduling platform for automated laboratories.

The system focuses on transforming laboratory production requirements into executable schedules through configurable workflows, resource allocation and constraint-based optimization.

Lab APS is intended to reduce manual planning effort, improve laboratory resource utilization and provide a maintainable scheduling framework that can evolve with laboratory operations.

---

# 2. Vision Statement

To build a lightweight, configurable and extensible Laboratory Advanced Planning & Scheduling Platform that enables laboratory managers to efficiently generate production plans while remaining independent of specific laboratory equipment, workflows or testing projects.

---

# 3. Product Position

Lab APS is an **Advanced Planning & Scheduling Platform**.

It is **not** intended to replace:

- Laboratory Information Management System (LIMS)
- Inventory Management System
- Enterprise Resource Planning (ERP)
- Instrument Control Software

Instead, Lab APS acts as the planning center between laboratory demand and laboratory execution.

```text
                 PI Demand
                     │
                     ▼
              Planning & Scheduling
                     │
                     ▼
            Laboratory Execution
                     │
                     ▼
          Result / Material Forecast
```

---

# 4. Business Background

Current laboratory planning relies heavily on manual scheduling using spreadsheets and individual experience.

As laboratory complexity increases, planning becomes difficult because of:

- Different equipment capabilities
- Different operator skills
- Workflow dependencies
- Instrument qualification requirements
- Multiple working shifts
- Increasing production demand

Manual scheduling becomes difficult to maintain and difficult to optimize.

Lab APS aims to standardize and automate this planning process.

---

# 5. Product Goals

The primary goals of Lab APS are:

### Goal 1

Automatically generate executable laboratory schedules.

---

### Goal 2

Reduce manual planning effort.

---

### Goal 3

Increase equipment utilization.

---

### Goal 4

Balance operator workload.

---

### Goal 5

Provide material consumption forecasting.

---

### Goal 6

Support future laboratory expansion without changing core architecture.

---

# 6. Core Principles

The following principles guide all future design and development.

## Principle 1

Configuration defines the laboratory.

Laboratory configuration must be data-driven rather than hardcoded.

Examples include:

- Staff
- Equipment
- Skills
- Shifts
- Holidays
- Workflow Templates

---

## Principle 2

Workflow defines the process.

Each laboratory project shall be represented by a Workflow Template.

Workflow Templates describe:

- Operations
- Dependencies
- Intermediate outputs
- Material requirements

Workflow Templates are reusable.

---

## Principle 3

Planning defines the demand.

Laboratory managers specify production demand.

The system determines how the demand should be executed.

---

## Principle 4

Scheduling computes the optimal allocation.

Scheduling is responsible only for optimization.

Business knowledge shall remain outside the solver.

---

## Principle 5

The Solver is an implementation detail.

Business modules shall never directly depend on OR-Tools.

The solver may be replaced in the future without affecting business modules.

---

## Principle 6

Material consumption is derived from the schedule.

Consumables and reagents do not participate in scheduling optimization.

Instead, material consumption is calculated after scheduling and used for forecasting and inventory verification.

---

# 7. Scope

## Included in Version 1

- Master Data Management
- Workflow Template Management
- Weekly Planning
- Automatic Scheduling
- Material Consumption Forecast
- Gantt Schedule Visualization
- Excel Export

---

## Planned for Future Versions

- Scenario Comparison
- Dynamic Rescheduling
- Multi-week Planning
- KPI Dashboard
- LIMS Integration
- Instrument Integration
- REST API
- AI-assisted Planning

---

# 8. Target Users

The initial users of Lab APS are:

### Principal Investigator (PI)

Defines weekly production demand.

---

### Production Laboratory Manager

Creates production plans.

Runs scheduling.

Publishes plans.

---

### Laboratory Engineer

Maintains equipment, workflows and laboratory configuration.

---

### Operator

Executes assigned laboratory operations.

---

### System Administrator

Maintains user accounts and system configuration.

---

# 9. Product Philosophy

Lab APS follows a workflow-driven planning philosophy.

The system plans laboratory work based on Workflow Templates rather than individual experiments.

Every production plan is generated using the following lifecycle:

```text
Production Demand
        │
        ▼
Workflow Generation
        │
        ▼
Operation Generation
        │
        ▼
Constraint Construction
        │
        ▼
Scheduling
        │
        ▼
Material Forecast
        │
        ▼
Published Plan
```

---

# 10. Success Criteria

The first release of Lab APS will be considered successful if it can:

- Generate a complete weekly laboratory schedule automatically.
- Allocate operators and equipment correctly.
- Respect workflow dependencies.
- Respect equipment capabilities.
- Respect operator qualifications.
- Support multiple working shifts.
- Produce material consumption forecasts.
- Export the final schedule for laboratory execution.

---

# 11. Long-term Vision

Lab APS is designed as a long-term laboratory planning platform rather than a standalone scheduling application.

Future development should continue following the same architectural principles while allowing new laboratory workflows, equipment types and optimization strategies to be incorporated without redesigning the core system.

The ultimate objective is to establish Lab APS as the central planning platform for laboratory production management.
