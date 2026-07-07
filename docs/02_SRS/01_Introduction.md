# docs/02_SRS/01_Introduction.md

# Software Requirements Specification

## Chapter 1 - Introduction

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Draft

---

# 1. Purpose

This Software Requirements Specification (SRS) defines the functional and non-functional requirements for the Laboratory Advanced Planning & Scheduling Platform (Lab APS).

The purpose of this document is to establish a common understanding between stakeholders, architects, developers and testers before implementation begins.

The SRS serves as the primary reference for:

* Software Architecture Design (SAD)
* Database Design
* API Design
* User Interface Design
* Test Case Design
* Future System Maintenance

---

# 2. Product Overview

Lab APS is a planning platform designed for laboratory production scheduling.

The system transforms production demand into executable laboratory schedules while considering:

* Equipment capability
* Operator skill
* Workflow dependencies
* Equipment qualification
* Shift calendar
* Resource availability

The platform provides optimized schedules together with operational analysis and material consumption forecasts.

---

# 3. Business Problem

Current laboratory planning is primarily performed manually.

Production Laboratory Managers typically use spreadsheets and personal experience to assign operators and equipment.

As laboratory complexity increases, manual planning introduces several challenges.

## BP-001 Manual Scheduling

Planning depends heavily on human experience.

Different planners may produce different schedules.

---

## BP-002 Equipment Capability Matching

Different instruments support different laboratory projects.

Example

* SU-HM-09 supports 384 Head workflows.
* SU-HM-01 supports 96 Head workflows.

Manual verification is time-consuming.

---

## BP-003 Operator Qualification

Not every operator can execute every laboratory project.

Manual assignment increases the risk of scheduling errors.

---

## BP-004 Workflow Dependency

Many laboratory workflows contain sequential operations.

Example

```text
SMDP
   │
   ▼
Output Plate
   │
   ▼
SAP
```

Dependencies must always be respected.

---

## BP-005 Equipment Qualification

Every instrument must periodically pass an FV qualification before performing production work.

Qualification status directly affects equipment availability.

---

## BP-006 Planning Efficiency

As weekly production demand increases, manual planning becomes increasingly difficult.

Generating a reliable schedule may require multiple revisions.

---

# 4. Product Objectives

The objectives of Lab APS are divided into business objectives and technical objectives.

---

## 4.1 Business Objectives

### BO-001

Reduce manual scheduling effort.

---

### BO-002

Generate executable production schedules automatically.

---

### BO-003

Improve laboratory resource utilization.

---

### BO-004

Reduce scheduling conflicts.

---

### BO-005

Support future laboratory expansion without redesigning the system.

---

## 4.2 Technical Objectives

### TO-001

Separate business logic from optimization algorithms.

---

### TO-002

Support configurable laboratory definitions.

---

### TO-003

Maintain reproducible scheduling results.

---

### TO-004

Provide maintainable software architecture.

---

# 5. Product Scope

Version 1.0 includes the following functional scope.

## In Scope

### Master Data

* Staff Management
* Equipment Management
* Workflow Template Management
* Capability Management
* Skill Management
* Material BOM Definition

---

### Planning

* Weekly Planning
* Demand Management
* Workflow Generation
* Automatic Scheduling
* Plan Publishing

---

### Scheduling

* Equipment Allocation
* Staff Allocation
* Shift Allocation
* Workflow Dependency Scheduling
* Equipment Qualification Validation

---

### Analysis

* Equipment Utilization
* Staff Utilization
* Material Consumption Forecast

---

### Reporting

* Schedule Export
* Material Forecast Export
* Planning Summary

---

# 6. Out of Scope

The following functions are intentionally excluded from Version 1.0.

* Inventory Management
* Purchasing
* Instrument Control
* Sample Tracking
* Laboratory Result Management
* Financial Management
* ERP Functions
* LIMS Functions

These functions may integrate with Lab APS in future versions.

---

# 7. Stakeholders

| Role                          | Responsibility                                  |
| ----------------------------- | ----------------------------------------------- |
| Principal Investigator (PI)   | Defines weekly production demand                |
| Production Laboratory Manager | Creates and publishes production plans          |
| Laboratory Engineer           | Maintains equipment, workflows and capabilities |
| Operator                      | Executes published schedules                    |
| System Administrator          | Maintains users and system configuration        |

---

# 8. Assumptions

The following assumptions apply to Version 1.0.

### AS-001

Production demand is provided before scheduling begins.

---

### AS-002

Workflow Templates have already been configured.

---

### AS-003

Staff information is maintained in the system.

---

### AS-004

Equipment capability is correctly configured.

---

### AS-005

Equipment qualification status is available.

---

### AS-006

Shift definitions are configured.

---

### AS-007

Holiday calendars are configured.

---

### AS-008

Material BOM definitions are configured.

---

# 9. Constraints

The following constraints apply to Version 1.0.

### C-001

Scheduling optimization shall use Google OR-Tools CP-SAT.

---

### C-002

The desktop application shall be implemented using Python, Flask and PyWebView.

---

### C-003

SQLite shall be used as the default development database.

PostgreSQL shall be supported for future production deployment.

---

### C-004

Business logic shall not directly depend on OR-Tools.

All optimization shall be accessed through the Solver Adapter.

---

### C-005

Configuration shall define laboratory behavior whenever practical.

Hardcoded laboratory configuration shall be avoided.

---

# 10. Success Criteria

Version 1.0 will be considered successful when the following conditions are met.

### SC-001

A complete weekly production plan can be generated automatically.

---

### SC-002

All workflow dependencies are satisfied.

---

### SC-003

No equipment conflicts exist.

---

### SC-004

No operator conflicts exist.

---

### SC-005

Equipment capability requirements are satisfied.

---

### SC-006

Operator skill requirements are satisfied.

---

### SC-007

Equipment qualification requirements are satisfied.

---

### SC-008

Material consumption forecasts are generated automatically.

---

### SC-009

Planning results can be exported for laboratory execution.

---

# 11. Document Relationship

This document serves as the entry point for all subsequent requirements.

The remaining SRS documents define:

* Business Process
* Functional Requirements
* Business Rules
* Use Cases
* User Interface Requirements
* Non-functional Requirements

Each requirement defined in later chapters shall trace back to the objectives established in this document.
