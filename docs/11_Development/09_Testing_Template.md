# docs/11_Development/09_Testing_Template.md

# Development Guide

## Chapter 9 - Testing Template

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Status:** Development Baseline

---

# 1. Purpose

This document defines the testing strategy and implementation standard for Lab APS.

The objective is to ensure that business logic remains testable, deterministic and maintainable.

Testing shall verify business behaviour rather than implementation details.

---

# 2. Testing Philosophy

Testing follows the principle:

> Test business behaviour before testing framework integration.

Priority order:

1. Domain
2. Engine
3. Use Case
4. Repository
5. API
6. UI

---

# 3. Testing Pyramid

```text
                UI Test

          Integration Test

             Use Case Test

        Engine / Domain Test

             Unit Test
```

The majority of tests shall be Domain and Engine tests.

---

# 4. Test Categories

## Domain Tests

Purpose

Verify business rules.

Examples

* PlanVersion.publish()
* Assignment.start()
* Equipment.disable()

Requirements

* No Flask
* No SQLAlchemy
* No OR-Tools

---

## Engine Tests

Purpose

Verify deterministic algorithms.

Examples

* WorkflowGenerator
* PlanningProblemBuilder
* ConstraintBuilder

Requirements

* Pure in-memory execution

---

## Use Case Tests

Purpose

Verify business orchestration.

Dependencies

* Fake Repository
* Fake Solver
* Fake Clock (when required)

Verify

* Transaction flow
* Correct Aggregate interaction
* Correct response DTO

---

## Repository Tests

Purpose

Verify ORM mapping.

Dependencies

* SQLite Test Database

Verify

* CRUD
* Relationship Mapping
* Cascade Rules

Business rules are out of scope.

---

## API Tests

Purpose

Verify REST behaviour.

Verify

* HTTP Status
* Request Validation
* Response DTO
* Error Codes

---

## UI Tests

Purpose

Verify critical user workflows.

Version 1.0 focuses on:

* Planning workflow
* Generate Schedule
* Publish Plan

Pixel-perfect testing is not required.

---

# 5. Test Naming

Pattern

```text
test_<behavior>_<expected_result>()
```

Examples

```text
test_publish_reviewed_version_success()

test_publish_working_version_should_fail()

test_generate_schedule_returns_assignments()
```

---

# 6. Test Data

Avoid shared mutable fixtures.

Prefer explicit builders.

Example

```text
PlanBuilder

PlanVersionBuilder

AssignmentBuilder
```

Every test should clearly describe its setup.

---

# 7. Fake Objects

Preferred test doubles

* Fake Repository
* Fake Solver Adapter
* Fake Clock
* Fake Notification Service

Avoid mocking business behaviour whenever possible.

---

# 8. Coverage Requirements

Minimum expectations

| Layer      |      Coverage Goal |
| ---------- | -----------------: |
| Domain     |                95% |
| Engine     |                90% |
| Use Case   |                85% |
| Repository |                80% |
| API        | Critical endpoints |

Coverage percentage is a guide, not the primary objective.

Business-critical behaviour takes precedence.

---

# 9. Regression Tests

Every resolved production defect shall include a regression test.

A bug is not considered fixed until a test prevents its recurrence.

---

# 10. Architectural Rules

1. Tests verify behaviour.
2. Domain tests require no infrastructure.
3. Engine tests are deterministic.
4. Integration tests verify component interaction.
5. Production bugs require regression tests.
6. Tests shall be readable and business-oriented.
