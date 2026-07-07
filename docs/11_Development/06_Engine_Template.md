# docs/11_Development/06_Engine_Template.md

# Development Guide

## Chapter 6 - Engine Implementation Template

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Development Baseline

---

# 1. Purpose

This document defines the implementation standard for all Engine components used by Lab APS.

Engines encapsulate reusable business algorithms.

They transform inputs into outputs.

They do not own business state.

They do not persist data.

---

# 2. What is an Engine?

An Engine is a stateless component responsible for performing one reusable business process.

Examples include:

* Workflow Generator
* Planning Problem Builder
* Scheduling Model Builder
* Constraint Builder
* Objective Builder
* Assignment Builder
* Material Calculator

Engines are reusable by multiple Use Cases.

---

# 3. Engine Responsibilities

An Engine may:

* Transform data
* Build runtime models
* Calculate derived results
* Execute deterministic algorithms

An Engine shall not:

* Access HTTP requests
* Execute SQL
* Commit transactions
* Load repositories
* Store business state

---

# 4. Standard Engine Pipeline

Every Engine follows the same execution pattern.

```text id="eng001"
Input

↓

Validate

↓

Transform

↓

Generate Result

↓

Return
```

Engines never modify their input objects.

---

# 5. Standard Class Structure

Each Engine shall expose one primary public method.

Example

```text id="eng002"
build()

generate()

calculate()

transform()

solve()
```

Method names shall express business intent.

Avoid generic names such as:

```text id="eng003"
execute()

process()

run()
```

---

# 6. Input Rules

Engine input shall consist of:

* Domain Objects
  or
* Runtime Models

Examples

Planning Engine

Input

```text id="eng004"
PlanVersion
```

Scheduling Engine

Input

```text id="eng005"
PlanningProblem
```

Constraint Builder

Input

```text id="eng006"
SchedulingModel
```

Input parameters shall be immutable.

---

# 7. Output Rules

Every Engine returns one well-defined result.

Examples

Workflow Generator

↓

WorkflowInstance Collection

Planning Problem Builder

↓

PlanningProblem

Scheduling Model Builder

↓

SchedulingModel

Assignment Builder

↓

Assignment Collection

Outputs shall not modify caller-owned objects.

---

# 8. Error Handling

Engines throw business exceptions when processing cannot continue.

Examples

```text id="eng007"
WorkflowDefinitionMissingError

InvalidPlanningContextError

ConstraintBuildError
```

Engines shall never swallow exceptions silently.

---

# 9. Logging

Each Engine logs only major execution milestones.

Recommended

* Start
* Finish
* Duration
* Result Summary

Avoid excessive per-item logging.

Example

```text id="eng008"
PlanningProblemBuilder

Operations: 128

Resources: 14

Duration: 28 ms
```

---

# 10. Stateless Design

Engines must remain stateless.

The following is prohibited:

* Cached planning data
* Mutable member variables
* Shared runtime context

All execution state shall be passed through method parameters.

---

# 11. Dependency Rules

Engine dependencies shall be minimal.

Allowed

* Other Engines (when architecturally approved)
* Configuration objects
* Value Objects

Forbidden

* Repository
* ORM Model
* Flask Request
* SQLAlchemy Session
* REST DTO

---

# 12. Engine Categories

Lab APS defines three Engine categories.

## Planning Engines

Examples

* PlanningContextBuilder
* WorkflowGenerator
* PlanningProblemBuilder

Responsibility

Transform business data into planning data.

---

## Scheduling Engines

Examples

* SchedulingModelBuilder
* ConstraintBuilder
* ObjectiveBuilder
* AssignmentBuilder

Responsibility

Transform planning data into scheduling results.

---

## Analysis Engines

Examples

* MaterialCalculator
* KPIBuilder

Responsibility

Generate analytical outputs from scheduling results.

---

# 13. Testing Requirements

Every Engine shall have dedicated unit tests.

Tests shall verify:

* Valid input
* Invalid input
* Empty input
* Boundary conditions
* Deterministic output

Engines shall be testable without:

* Database
* Flask
* OR-Tools

except for the Solver Adapter.

---

# 14. Performance Guidelines

Engine implementations should:

* Avoid repeated traversal of the same collection.
* Prefer immutable intermediate models.
* Minimize object allocation inside loops.
* Separate validation from transformation.

Optimization should not reduce readability.

---

# 15. Code Review Checklist

Before merging an Engine implementation, verify:

* Is the Engine stateless?
* Does it perform exactly one responsibility?
* Does it avoid persistence?
* Does it avoid framework dependencies?
* Does it return a deterministic result?
* Can it be tested independently?

---

# 16. Engine Template Summary

Every Engine in Lab APS follows the same architecture.

```text id="eng009"
Input

↓

Validation

↓

Transformation

↓

Result

↓

Return
```

Business orchestration belongs to Use Cases.

Business rules belong to the Domain.

Reusable algorithms belong to Engines.

This separation shall remain consistent across the entire codebase.
