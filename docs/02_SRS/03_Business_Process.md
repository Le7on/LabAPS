# docs/02_SRS/03_Business_Process.md

# Software Requirements Specification

## Chapter 3 - Business Process

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Draft

---

# 1. Purpose

This chapter defines the end-to-end business process of Lab APS.

It describes how a production plan is created, reviewed, published and executed.

The business process described here serves as the foundation for:

- Planning Engine
- Workflow Engine
- Scheduling Engine
- User Interface
- Database Design
- REST API

---

# 2. Planning Lifecycle

Lab APS manages production through a complete planning lifecycle.

```text
Planning Demand
        │
        ▼
Create Plan
        │
        ▼
Configure Inputs
        │
        ▼
Generate Workflow
        │
        ▼
Generate Schedule
        │
        ▼
Review Plan
        │
        ▼
Publish Plan
        │
        ▼
Execute
        │
        ▼
Close Plan
```

A Plan is the central business object throughout the entire lifecycle.

---

# 3. Business Workflow

## Step 1 – Receive Production Demand

Actor

Principal Investigator

Input

- Planning Horizon
- Required Projects
- Required Run Quantity
- Priority (Optional)

Output

Production Demand

Example

| Project | Quantity |
| ------- | -------: |
| FV      |        6 |
| 96 OPA  |       12 |
| 384 PNG |       18 |
| AZ RSV  |        8 |

---

## Step 2 – Create Plan

Actor

Production Laboratory Manager

Action

Create a new production plan.

Input

- Planning Horizon
- Demand
- Planning Calendar

Output

Plan

Example

```text
Plan

Week 32

Status

Draft
```

A newly created Plan contains no schedule.

---

## Step 3 – Verify Planning Environment

Before scheduling begins, the system validates planning inputs.

Validation includes

### Calendar

- Working Days
- Holidays
- Shift Definitions

### Staff

- Active Staff
- Leave
- Skills

### Equipment

- Equipment Status
- Maintenance
- Capability
- FV Qualification

Validation failures must be reported before scheduling.

---

## Step 4 – Generate Workflow Instances

Each Demand item is expanded into Workflow Instances.

Example

Demand

```text
384 PNG

3 Runs
```

System generates

```text
PNG-001

PNG-002

PNG-003
```

Each Workflow Instance is independent.

---

## Step 5 – Generate Operations

Workflow Engine converts every Workflow Instance into executable Operations.

Example

Workflow

```text
384 PNG
```

Generated Operations

```text
PNG-001

SMDP

↓

SAP
```

AZ RSV

```text
AZ001

CP

↓

SP
```

Operations become scheduling objects.

---

## Step 6 – Build Scheduling Model

Planning Engine converts Operations into a scheduling model.

The Scheduling Engine generates:

- Scheduling Variables
- Resource Constraints
- Dependency Constraints
- Calendar Constraints
- Optimization Objectives

The Scheduling Engine remains independent of laboratory business logic.

---

## Step 7 – Compute Schedule

Scheduling Engine invokes the Solver.

Inputs

- Operations
- Resources
- Constraints

Outputs

Assignments

Each Assignment contains

- Operation
- Equipment
- Staff
- Shift

---

## Step 8 – Material Forecast

After scheduling completes,

Material Calculator estimates material consumption.

Outputs

- Daily Consumption
- Weekly Consumption
- Material Summary

Inventory is not modified.

If available inventory data exists,

the system compares:

Forecast

↓

Inventory

↓

Warning

Example

```text
384 Tips

Need

2400

Current Stock

1800

Warning

Shortage

600
```

---

## Step 9 – Review Plan

Production Laboratory Manager reviews:

- Schedule
- Equipment Utilization
- Staff Allocation
- Material Forecast
- Planning Warnings

If necessary,

the Plan may be recalculated.

---

## Step 10 – Publish Plan

After approval,

the Plan is published.

Only Published Plans may be executed.

Publishing freezes the planning result.

---

## Step 11 – Execute Plan

Operators execute published Assignments.

Execution status is recorded.

Examples

- Not Started
- Running
- Completed
- Failed

Version 1.0 records execution status only.

Automatic rescheduling is outside current scope.

---

## Step 12 – Close Plan

When all Operations complete,

the Plan is closed.

Closed Plans become read-only historical records.

---

# 4. Plan State Machine

A Plan moves through several lifecycle states.

```text
Draft

↓

Ready

↓

Scheduled

↓

Reviewed

↓

Published

↓

Executing

↓

Completed

↓

Archived
```

State transitions must follow the defined order.

---

## State Description

| State     | Description                  |
| --------- | ---------------------------- |
| Draft     | Plan created                 |
| Ready     | Planning inputs validated    |
| Scheduled | Solver completed             |
| Reviewed  | Schedule reviewed            |
| Published | Released to laboratory       |
| Executing | Laboratory execution started |
| Completed | All operations completed     |
| Archived  | Historical record            |

---

# 5. Replanning

Production changes may require replanning.

Examples

- PI changes production demand
- Equipment failure
- Staff leave
- Equipment maintenance

Lab APS supports recalculating Draft or Reviewed Plans.

Published Plans cannot be recalculated directly.

Instead,

a new Plan Version shall be created.

---

# 6. Plan Version

Each planning cycle supports multiple versions.

Example

```text
Week 32

V1 Initial Plan

↓

V2 Equipment Maintenance

↓

V3 Demand Update
```

Only one version may be Published.

Historical versions remain available.

---

# 7. Responsibilities

## Principal Investigator

Responsible for

- Production Demand

Not responsible for

- Scheduling

---

## Production Laboratory Manager

Responsible for

- Planning
- Scheduling
- Review
- Publish

---

## Laboratory Engineer

Responsible for

- Configuration
- Workflow Templates
- Equipment
- Capability
- Skills

---

## Operator

Responsible for

- Execution

---

## System

Responsible for

- Workflow Generation
- Schedule Optimization
- Material Forecast
- Validation

---

# 8. Business Rules Reference

The following business rule groups apply during the planning process.

| Rule Group      | Description                             |
| --------------- | --------------------------------------- |
| Equipment Rules | Capability and qualification validation |
| Staff Rules     | Skill and availability validation       |
| Workflow Rules  | Operation dependency validation         |
| Calendar Rules  | Shift and holiday validation            |
| Material Rules  | Forecast calculation after scheduling   |

Detailed business rules are defined in **Chapter 5 – Business Rules**.

---

# 9. Future Extensions

The business process is designed to support future capabilities without changing the overall lifecycle.

Examples include

- Scenario Planning
- Multi-week Planning
- Dynamic Rescheduling
- AI-assisted Planning
- Automatic Instrument Integration

These capabilities extend existing business steps rather than replacing them.
