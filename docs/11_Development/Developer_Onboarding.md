# Developer Onboarding Guide

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Status:** Draft

---

## 1. Purpose

This guide helps a new contributor understand how to start working on Lab APS, what the repository structure looks like, and where to look for architecture and implementation guidance.

---

## 2. Repository Overview

The repository is organized into the following top-level areas:

- backend/ — backend application, domain modules, scheduling engines, and solver integration.
- frontend/ — Vue 3 SPA frontend shell.
- docs/ — architecture, requirements, design, and workflow documentation.
- tests/ — integration and end-to-end tests.
- tools/ — project bootstrap and code generation tooling.
- deployment/ — deployment assets and environment configuration.
- resources/ — static assets and supporting files.

---

## 3. Recommended Reading Path

Before writing code, read the following documents in order:

1. [../PROJECT_CONTEXT.md](../PROJECT_CONTEXT.md)
2. [../01_Vision/01_Vision.md](../01_Vision/01_Vision.md)
3. [../02_SRS/01_Introduction.md](../02_SRS/01_Introduction.md)
4. [../03_SAD/02_System_Architecture.md](../03_SAD/02_System_Architecture.md)
5. [../11_Development/00_Engineering_Baseline.md](../11_Development/00_Engineering_Baseline.md)
6. [../07_Database/03_Physical_ERD.md](../07_Database/03_Physical_ERD.md)
7. [../08_API/02_Planning_API.md](../08_API/02_Planning_API.md)

---

## 4. Development Environment

## Python

The project is expected to use Python with the following core dependencies:

- Flask
- SQLAlchemy
- Flask-SQLAlchemy
- Alembic
- OR-Tools
- PyYAML
- python-dotenv

The project bootstrap templates reference these dependencies in the tooling templates under [../tools/templates/project](../tools/templates/project).

## Frontend

The current architecture targets a Vue 3 frontend with Vite, Pinia, and Axios.

## Testing

The expected toolchain includes:

- pytest
- pytest-cov
- ruff
- black
- isort
- mypy

---

## 5. Suggested Development Workflow

1. Start from the relevant requirement or ADR.
2. Confirm the affected domain module.
3. Update the related design document if the behavior or architecture changes.
4. Implement the change in the smallest possible unit.
5. Add or update tests.
6. Run validation checks before submitting.

---

## 6. Where to Start for Common Tasks

## Add or change a domain concept

Look at:

- [../03_SAD/03_Domain_Architecture.md](../03_SAD/03_Domain_Architecture.md)
- [../10_State_Model/01_State_Model_Overview.md](../10_State_Model/01_State_Model_Overview.md)
- [../07_Database/03_Physical_ERD.md](../07_Database/03_Physical_ERD.md)

## Add or change planning or scheduling logic

Look at:

- [../03_SAD/05_Scheduling_Architecture.md](../03_SAD/05_Scheduling_Architecture.md)
- [../06_Planning_Model/01_Planning_Model.md](../06_Planning_Model/01_Planning_Model.md)
- [../05_Constraint_Framework/01_Constraint_Framework.md](../05_Constraint_Framework/01_Constraint_Framework.md)

## Add or change API behavior

Look at:

- [../08_API/01_API_Resource_Model.md](../08_API/01_API_Resource_Model.md)
- [../08_API/02_Planning_API.md](../08_API/02_Planning_API.md)
- [../03_SAD/16_API_Architecture.md](../03_SAD/16_API_Architecture.md)

## Add or change UI behavior

Look at:

- [../09_UI/04_Plan_Workspace_Design.md](../09_UI/04_Plan_Workspace_Design.md)
- [../09_UI/06_Interaction_Specification.md](../09_UI/06_Interaction_Specification.md)
- [../03_SAD/Architecture_Update_2026-07_Vue3.md](../03_SAD/Architecture_Update_2026-07_Vue3.md)

---

## 7. Contribution Checklist

Before opening a pull request, confirm the following:

- the relevant requirement or ADR is identified
- the related documentation has been updated if needed
- tests have been added or updated
- the change follows the architecture boundaries
- no architectural rule has been bypassed

---

## 8. Next Step

For the first implementation milestone, focus on the bootstrap and infrastructure layer, then move to planning domain modules and scheduling workflows.
