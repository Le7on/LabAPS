# docs/03_SAD/03_Domain_Architecture.md

# Software Architecture Design

## Chapter 3 - Domain Architecture

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Draft

---

# 1. Purpose

This document defines the Domain Architecture of Lab APS.

The purpose of Domain Architecture is to divide the system into clear business domains with explicit ownership and boundaries.

A domain owns its own business logic, business objects and data.

Domains communicate through Application Services only.

This document serves as the foundation for:

* Project Structure
* Package Organization
* Repository Design
* Database Design
* API Design

---

# 2. Domain Design Principles

The Domain Architecture follows Domain-Driven Design (DDD).

The following principles shall always be respected.

* Business owns technology.
* Domains own data.
* Domains communicate through services.
* Infrastructure supports domains.
* The Solver is not a domain.

---

# 3. Domain Overview

Lab APS is divided into three business domains.

```text id="84r1tl"
                    Lab APS

        ┌────────────────────────────┐
        │     Foundation Domain      │
        └─────────────┬──────────────┘
                      │
                      ▼
        ┌────────────────────────────┐
        │      Planning Domain       │
        └─────────────┬──────────────┘
                      │
                      ▼
        ┌────────────────────────────┐
        │     Supporting Domain      │
        └────────────────────────────┘
```

Planning Domain is the Core Domain.

Foundation Domain provides laboratory definitions.

Supporting Domain consumes planning results.

---

# 4. Foundation Domain

Foundation Domain defines the laboratory.

It contains stable business information.

Foundation Domain does not participate directly in scheduling.

---

## Responsibilities

* Staff
* Equipment
* Capability
* Skill
* Workflow Template
* Material Definition
* Shift Definition
* Holiday Calendar
* Leave
* Maintenance
* Solver Profile

---

## Business Objects

```text id="phl4oq"
Staff

Equipment

Capability

Skill

Workflow Template

Material

Shift

Holiday

Leave

Maintenance
```

---

## Rules

Foundation Domain never owns:

* Plans
* Schedule
* Assignment
* Material Forecast

Foundation Domain provides reference information only.

---

# 5. Planning Domain

Planning Domain is the Core Domain of Lab APS.

Planning transforms laboratory demand into executable plans.

Every business process revolves around Planning.

---

## Responsibilities

* Plan Management
* Demand Management
* Planning Context
* Workflow Generation
* Scheduling Coordination
* Material Forecast
* Plan Version
* Publish

---

## Business Objects

```text id="mdj3sk"
Plan

Planning Context

Demand

Workflow Instance

Operation

Assignment

Material Forecast

KPI
```

---

## Internal Services

Planning Domain owns the following Domain Services.

```text id="6x9i8k"
Workflow Generator

Planner

Publisher

Material Calculator

Plan Validator

Version Manager
```

---

## Planning Context

Planning Context is part of the Planning Domain.

It captures the planning environment at scheduling time.

Planning Context contains snapshots of:

* Calendar
* Equipment Availability
* Staff Availability
* Shift Configuration
* Solver Profile

Planning Context guarantees reproducible planning.

---

# 6. Scheduling

Scheduling belongs to the Planning Domain.

Scheduling is **not** an independent business domain.

Scheduling is an Optimization Service.

---

Scheduling consists of

```text id="ihc7x8"
Variable Builder

Constraint Builder

Objective Builder

Solver Adapter

Result Parser
```

Scheduling receives Operations.

Scheduling returns Assignments.

Scheduling owns no business data.

---

# 7. Supporting Domain

Supporting Domain consumes planning information.

Supporting Domain never changes planning decisions.

---

## Responsibilities

* Execution Tracking
* Dashboard
* Reporting
* KPI Visualization

---

## Business Objects

```text id="mtyfpi"
Execution

Execution Log

Dashboard

Reports
```

---

## Rules

Supporting Domain shall never

* Generate Plans
* Modify Plans
* Execute Scheduling

Supporting Domain is read-oriented.

---

# 8. Domain Communication

Only Application Services may coordinate multiple domains.

The communication model is shown below.

```text id="5g0m0x"
Presentation

↓

Application Services

↓

Foundation Domain

↓

Planning Domain

↓

Supporting Domain
```

Direct domain-to-domain repository access is prohibited.

---

# 9. Aggregate Ownership

Every Aggregate belongs to exactly one Domain.

| Aggregate         | Domain     |
| ----------------- | ---------- |
| Staff             | Foundation |
| Equipment         | Foundation |
| Workflow Template | Foundation |
| Material          | Foundation |
| Plan              | Planning   |
| Planning Context  | Planning   |
| Demand            | Planning   |
| Workflow Instance | Planning   |
| Operation         | Planning   |
| Assignment        | Planning   |
| Material Forecast | Planning   |
| Execution         | Supporting |
| Dashboard         | Supporting |
| Report            | Supporting |

No Aggregate may belong to multiple Domains.

---

# 10. Dependency Rules

Allowed dependencies

```text id="hzc5ol"
Foundation

↓

Planning

↓

Supporting
```

Forbidden dependencies

* Supporting → Foundation Repository
* Supporting → Scheduling
* Scheduling → Database
* Foundation → Planning

Dependencies shall always point toward the Core Domain through Application Services.

---

# 11. Package Mapping

Each Domain maps directly to a source package.

```text id="vmkq6r"
src/

foundation/

planning/

supporting/

application/

infrastructure/

common/
```

The package structure mirrors the Domain Architecture.

---

# 12. Database Ownership

Each Domain owns its own persistence model.

Examples

Foundation

* Staff
* Equipment
* Workflow Template

Planning

* Plan
* Demand
* Assignment

Supporting

* Execution Log
* Report Cache

Cross-domain table updates are prohibited.

---

# 13. Domain Events (Reserved)

Future versions may introduce Domain Events.

Examples

* PlanCreated
* ScheduleGenerated
* PlanPublished
* AssignmentCompleted

Domain Events shall be used for asynchronous communication.

Version 1.0 does not require event-driven implementation.

---

# 14. Domain Evolution

The architecture supports future extensions without changing the Core Domain.

Examples

Foundation Domain

* Equipment Categories
* Laboratory Sites

Planning Domain

* Scenario Planning
* Dynamic Rescheduling
* Multi-week Planning

Supporting Domain

* Notification Center
* Audit Center
* AI Recommendation

Future functionality shall extend existing domains rather than introducing unnecessary new domains.

---

# 15. Architecture Summary

The Domain Architecture establishes the following rules.

1. Planning is the Core Domain.

2. Scheduling is a Domain Service within Planning.

3. Foundation defines laboratory knowledge.

4. Supporting consumes planning outputs.

5. Domains own their own business objects.

6. Domains communicate through Application Services.

7. Infrastructure never contains business logic.

This architecture shall remain stable throughout the lifetime of the Lab APS platform.
