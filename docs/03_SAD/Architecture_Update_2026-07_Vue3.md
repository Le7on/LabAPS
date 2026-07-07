# docs/03_SAD/Architecture_Update_2026-07_Vue3.md

# Architecture Update

## Frontend Technology Upgrade

**Project:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.1

**Status:** Accepted

**Effective Date:** 2026-07-07

---

# 1. Purpose

This document records the implementation architecture upgrade from the original Flask Template rendering model to a modern Single Page Application (SPA) architecture.

This upgrade affects the implementation layer only.

The following architectural artifacts remain unchanged:

- Vision
- SRS
- Domain Model
- Aggregate Design
- State Model
- Constraint Framework
- Planning Model
- Solver Architecture

Business architecture is not affected.

---

# 2. Background

Version 1.0 originally adopted the following presentation architecture.

```text
PyWebView

↓

Flask

↓

HTML + Bootstrap
```

Although suitable for small desktop tools, this approach has several limitations.

- UI complexity increases rapidly.
- Client-side state management is weak.
- Dynamic planning views become difficult to maintain.
- Future Web deployment requires significant changes.

After architectural review, the frontend technology stack was upgraded.

---

# 3. Decision

Lab APS adopts a modern frontend/backend separation.

The new implementation architecture is:

```text
PyWebView

↓

Vue 3 Application

↓

Pinia

↓

Axios

↓

REST API

↓

Flask Backend

↓

Application Layer

↓

Domain Layer

↓

Planning Engine

↓

Scheduling Engine
```

PyWebView becomes a desktop container only.

Flask becomes a pure REST API server.

Vue becomes responsible for all user interface rendering.

---

# 4. New Technology Stack

## Desktop

- PyWebView

Purpose

Desktop application container.

PyWebView shall not contain business logic.

---

## Frontend

Framework

Vue 3

Build Tool

Vite

State Management

Pinia

HTTP Client

Axios

Routing

Vue Router

Responsibilities

- User interaction
- View rendering
- Client state
- API communication

Business rules remain in the backend.

---

## Backend

Framework

Flask

Responsibilities

- REST API
- Authentication (future)
- Use Case execution
- Domain orchestration

Flask shall not render HTML pages.

---

## Database

Version 1.0

SQLite

Future

PostgreSQL

No change.

---

## Optimization

Google OR-Tools CP-SAT

No change.

---

# 5. Updated Runtime Architecture

```text
+------------------------------------------------------+
|                  PyWebView Window                    |
|                                                      |
|  +----------------------------------------------+    |
|  |              Vue 3 Frontend                  |    |
|  |                                              |    |
|  |  Components                                 |    |
|  |  Views                                      |    |
|  |  Pinia Store                                |    |
|  +----------------------+-----------------------+    |
|                         |                            |
|                         | Axios                      |
|                         ▼                            |
|  +----------------------------------------------+    |
|  |               Flask REST API                 |    |
|  +----------------------------------------------+    |
|                         |                            |
|                         ▼                            |
|              Application / Domain                   |
|                         |                            |
|                         ▼                            |
|         Planning & Scheduling Engine                |
|                         |                            |
|                         ▼                            |
|                  SQLite Database                    |
+------------------------------------------------------+
```

---

# 6. Project Structure Changes

Previous structure

```text
src/

    api/

    ui/templates/

    ui/static/
```

Updated structure

```text
src/

    backend/

        api/

        application/

        domain/

        engines/

        infrastructure/

        solver/

    frontend/

        src/

            views/

            components/

            router/

            stores/

            api/

            assets/

        public/

        package.json

        vite.config.ts
```

Frontend and backend become independent projects.

---

# 7. API Changes

The REST API becomes the only communication mechanism between frontend and backend.

Flask templates are removed.

All business operations are executed through REST endpoints.

The previously defined API contracts remain valid.

---

# 8. UI Changes

The Information Architecture remains unchanged.

Navigation remains unchanged.

Plan Workspace remains unchanged.

Only the implementation technology changes.

Vue Components replace HTML templates.

---

# 9. State Management

Client-side application state shall be managed by Pinia.

Examples

- Current Plan
- Current Plan Version
- Selected Workspace Tab
- Authentication State (future)
- User Preferences (future)

Business state remains on the backend.

---

# 10. Build Process

Development

```text
Frontend

↓

npm run dev

Backend

↓

python src/backend/app.py
```

Production

```text
Frontend

↓

npm run build

↓

dist/

↓

PyWebView
```

---

# 11. Migration Impact

The following documents require implementation updates only.

- Project Structure
- Development Guide
- Bootstrap Tool

The following documents remain unchanged.

- Vision
- SRS
- SAD (Business Architecture)
- ADR-001 to ADR-010
- Constraint Framework
- State Model

---

# 12. Benefits

The new implementation provides:

- Clear frontend/backend separation
- Better component reuse
- Better state management
- Easier testing
- Easier future Web deployment
- Cleaner REST architecture

No business architecture changes are introduced.

---

# 13. Architecture Baseline

From Version 1.1 onward, Lab APS officially adopts:

- Vue 3
- Vite
- Pinia
- Axios
- Flask REST API
- PyWebView

This implementation architecture becomes the new development baseline for the project.
