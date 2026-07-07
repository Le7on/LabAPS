# docs/11_Development/01_Project_Architecture.md

# Development Guide

## Chapter 1 - Project Architecture

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Development Baseline

---

# 1. Purpose

This document defines the runtime architecture of the Lab APS application.

Unlike the Software Architecture Design (SAD), which describes business architecture, this document describes how the application is assembled at runtime.

It serves as the implementation blueprint for the Python project.

---

# 2. Design Goals

The runtime architecture shall satisfy the following goals.

* Clear startup sequence
* Dependency isolation
* Testability
* Replaceable infrastructure
* Simple deployment
* Minimal framework coupling

---

# 3. Runtime Architecture

The application starts from a single entry point.

```text
app.py

↓

Application Factory

↓

Infrastructure Initialization

↓

Repository Registration

↓

Domain Service Registration

↓

Planning Engine Initialization

↓

Scheduling Engine Initialization

↓

REST API Registration

↓

PyWebView Startup
```

Every initialization step has one responsibility.

---

# 4. Application Factory

The Application Factory creates the runtime environment.

Responsibilities include:

* Load configuration
* Initialize Flask
* Initialize SQLAlchemy
* Register Blueprints
* Register global error handlers
* Register dependency container

Business logic shall never exist inside the Application Factory.

---

# 5. Dependency Structure

Dependencies are initialized in the following order.

```text
Configuration

↓

Infrastructure

↓

Repositories

↓

Application Use Cases

↓

Planning Engine

↓

Scheduling Engine

↓

Presentation
```

Lower layers shall never depend on higher layers.

---

# 6. Runtime Components

The runtime consists of six major components.

| Component         | Responsibility            |
| ----------------- | ------------------------- |
| Configuration     | Runtime configuration     |
| Infrastructure    | Database, logging, export |
| Application       | Use Cases                 |
| Domain            | Business behaviour        |
| Planning Engine   | Planning pipeline         |
| Scheduling Engine | Optimization pipeline     |

---

# 7. Configuration Loading

Configuration is loaded only once during startup.

Suggested configuration files:

```text
config.yaml

logging.yaml

solver.yaml
```

Configuration shall be injected rather than accessed globally.

---

# 8. Repository Registration

Repositories are created during application startup.

Examples

* PlanRepository
* StaffRepository
* EquipmentRepository
* WorkflowDefinitionRepository

Repositories are shared by Application Use Cases through dependency injection.

---

# 9. Engine Registration

Planning Engine components.

```text
PlanningContextBuilder

PlanningProblemBuilder

WorkflowGenerator
```

Scheduling Engine components.

```text
SchedulingModelBuilder

ConstraintBuilder

ObjectiveBuilder

SolverAdapter

AssignmentBuilder
```

Engines are stateless and reusable.

---

# 10. Presentation Startup

After initialization completes:

* Flask REST API starts.
* PyWebView loads the local web application.
* The user enters through the Dashboard.

The Presentation Layer never initializes business services directly.

---

# 11. Architectural Rules

1. Runtime initialization is centralized.

2. Dependencies flow inward.

3. Engines remain stateless.

4. Business logic is never executed during startup.

5. Runtime configuration remains external.

6. Every component is replaceable without affecting the Domain Model.

---

# 12. Next Artifact

The next document,

**02_Project_Structure_Implementation.md**

defines the actual Python package layout, naming conventions and implementation templates used by the development team.
