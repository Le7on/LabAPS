# docs/ARCHITECTURE_INDEX.md

## Lab APS Architecture Index

**Architecture Baseline:** Version 1.0

---

### Documentation Structure

```text
docs/

README.md
PROJECT_CONTEXT.md
ARCHITECTURE_INDEX.md
ARCHITECTURE_LOG.md

01_Vision/
02_SRS/
03_SAD/
04_ADR/
05_Constraint_Framework/
06_Planning_Model/
07_Database/
08_API/
09_UI/
10_State_Model/
11_Development/
12_Development_Log/
```

### Quick Start

- Start here: [README.md](README.md)
- Project context: [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md)
- Developer onboarding: [11_Development/Developer_Onboarding.md](11_Development/Developer_Onboarding.md)
- Testing guide: [11_Development/Testing_and_Validation_Guide.md](11_Development/Testing_and_Validation_Guide.md)
- Deployment guide: [11_Development/Deployment_and_Operations_Guide.md](11_Development/Deployment_and_Operations_Guide.md)

---

## Vision

| Document    | Status   |
| ----------- | -------- |
| Vision      | Complete |
| Terminology | Complete |

---

## SRS

| ID     | Document                | Status   |
| ------ | ----------------------- | -------- |
| SRS-01 | Introduction            | Complete |
| SRS-02 | Business Background     | Complete |
| SRS-03 | Business Process        | Complete |
| SRS-04 | Functional Requirements | Complete |
| SRS-05 | Business Object Model   | Complete |

---

## SAD

| ID     | Document                  | Status   |
| ------ | ------------------------- | -------- |
| SAD-01 | Business Capability       | Complete |
| SAD-02 | System Architecture       | Complete |
| SAD-03 | Domain Architecture       | Complete |
| SAD-04 | Plan Aggregate            | Complete |
| SAD-05 | Scheduling Architecture   | Complete |
| SAD-06 | Application Architecture  | Complete |
| SAD-07 | Conceptual Database Model | Complete |
| SAD-08 | Plan Lifecycle            | Complete |
| SAD-09 | Plan Version Architecture | Complete |
| SAD-10 | Persistence Architecture  | Complete |
| SAD-11 | Conceptual ERD            | Complete |
| SAD-12 | Physical Database Design  | Complete |
| SAD-13 | Architecture Constraints  | Complete |
| SAD-14 | Solver Model              | Complete |
| SAD-15 | Module Interaction        | Complete |
| SAD-16 | API Architecture          | Complete |
| SAD-17 | Deployment Architecture   | Complete |
| SAD-18 | Coding Guidelines         | Complete |
| SAD-19 | Project Structure         | Complete |
| SAD-20 | Development Workflow      | Complete |

---

## ADR

| ID      | Decision                                    | Status   |
| ------- | ------------------------------------------- | -------- |
| ADR-001 | Plan as Aggregate Root                      | Accepted |
| ADR-002 | Plan + Plan Version                         | Accepted |
| ADR-003 | Workflow Definition vs Workflow Instance    | Accepted |
| ADR-004 | Operation Definition vs Operation Instance  | Accepted |
| ADR-005 | Scheduling Model as Anti-Corruption Layer   | Accepted |
| ADR-006 | Constraint Model                            | Accepted |
| ADR-007 | Constraint Model vs Objective Model         | Accepted |
| ADR-008 | Planning Context Snapshots                  | Accepted |
| ADR-009 | Reject Direct Database-Driven Scheduling    | Accepted |
| ADR-010 | Separate Laboratory Definition and Planning | Accepted |

---

## Constraint Framework

| Document                 | Status   |
| ------------------------ | -------- |
| Constraint Framework     | Complete |
| Constraint Mapping       | Complete |
| Constraint Specification | Complete |

---

## Architecture Baseline

## Core Domain

Planning

## Aggregate Root

Plan

## Version Model

Plan → Plan Version

## Workflow Model

Project

↓

Workflow Definition

↓

Operation Definition

↓

Workflow Instance

↓

Operation Instance

↓

Assignment

## Scheduling Pipeline

Planning Problem

↓

Scheduling Model

↓

Scheduling Solution

## Solver

Planning Problem

↓

Scheduling Model

↓

Constraint Model

↓

Objective Model

↓

Solver Adapter

↓

OR-Tools

---

## Remaining Design Artifacts

Priority 1

- Physical ERD
- Data Dictionary
- OpenAPI Specification
- UI Wireframe
- Solver Design Specification

Priority 2

- Developer Guide
- Test Specification

### Documentation Delivery Status

The following documentation artifacts are now available as implementation support material:

- Documentation entry page: [README.md](README.md)
- Developer onboarding: [11_Development/Developer_Onboarding.md](11_Development/Developer_Onboarding.md)
- Testing and validation guide: [11_Development/Testing_and_Validation_Guide.md](11_Development/Testing_and_Validation_Guide.md)

---

## Session Resume Prompt

To continue this project in a new conversation, provide this file together with [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) and state the next target artifact.

Example:

> Continue Lab APS architecture. Current baseline is frozen. Start from [README.md](README.md), then review [11_Development/Developer_Onboarding.md](11_Development/Developer_Onboarding.md) and [11_Development/Testing_and_Validation_Guide.md](11_Development/Testing_and_Validation_Guide.md).
