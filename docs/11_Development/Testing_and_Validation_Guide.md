# Testing and Validation Guide

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Status:** Draft

---

## 1. Purpose

This guide defines a lightweight validation strategy for the Lab APS project while the implementation is still evolving.

The purpose is to ensure that changes are verifiable, regressions are discoverable, and new features can be introduced safely.

---

## 2. Validation Layers

The project should validate work at three levels:

## 2.1 Unit Tests

Focus on domain behavior, value objects, state transitions, and business rules.

Examples:

- plan state transitions
- assignment validation
- constraint mapping logic
- scheduling model builders

## 2.2 Integration Tests

Focus on flows that cross module boundaries:

- planning service to repository
- API to application use case
- solver adapter to scheduling model

## 2.3 End-to-End Tests

Focus on high-level user journeys:

- create a plan
- generate a schedule
- publish a version
- inspect forecast and KPI output

---

## 3. Suggested Test Categories

## Domain Tests

These should be the highest priority for business logic.

They should:

- run without Flask
- run without database access
- run without OR-Tools

## API Tests

API tests should validate:

- request validation
- success and error responses
- status codes
- response schema

## Solver Tests

Solver-related tests should verify:

- constraint generation
- objective generation
- solution parsing
- fallback behavior on scheduling failure

---

## 4. Suggested Tooling

The project bootstrap templates already indicate the expected test stack:

- pytest
- pytest-cov
- black
- ruff
- isort
- mypy

Recommended usage:

- pytest for tests
- pytest-cov for coverage reports
- ruff for linting
- mypy for static typing checks

---

## 5. Validation Checklist

Before considering a change complete, verify the following:

- the affected requirement or ADR is identified
- the change has a test case or validation scenario
- the relevant documentation is updated
- domain rules remain isolated from infrastructure code
- the change does not introduce architectural violations

---

## 6. Example Validation Commands

The following commands are expected to be used during development:

```bash
pytest
```

```bash
pytest --cov
```

```bash
ruff check .
```

```bash
mypy .
```

---

## 7. Definition of Done for a Feature

A feature is not complete until:

- the core behavior works
- relevant tests pass
- documentation is updated
- the change is consistent with the architecture baseline

---

## 8. Recommended Next Step

When implementation begins in earnest, create a minimal test suite for the planning domain first, then expand to API and integration layers.
