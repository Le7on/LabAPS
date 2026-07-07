# docs/04_ADR/ADR-011-Adopt-Vue3-SPA-Frontend.md

# ADR-011 — Adopt Vue 3 SPA Frontend

**Status:** Accepted

**Date:** 2026-07-07

---

# Context

Version 1.0 originally proposed a presentation architecture based on:

```text
PyWebView

↓

Flask

↓

Jinja2 Templates

↓

Bootstrap
```

This approach is common for small CRUD-oriented systems.

However, Lab APS is an interactive planning application rather than a traditional CRUD application.

Typical user activities include:

* Planning Workspace
* Version Comparison
* Gantt Timeline
* Material Forecast
* KPI Dashboard
* Interactive Planning Review

These features require rich client-side state management and dynamic UI interaction.

---

# Problem Statement

The original architecture introduced several limitations.

## Limited Client-side State

The application maintains a large amount of transient UI state.

Examples include:

* Current Plan
* Current Plan Version
* Selected Workspace
* Current Filters
* Current Timeline View
* Warning Panel

Managing these using server-rendered templates would significantly increase complexity.

---

## Tight Coupling

Rendering HTML inside Flask couples:

* UI
* API
* Backend

This reduces maintainability and future deployment flexibility.

---

## Future Scalability

Future roadmap items include:

* Scenario Planning
* AI Recommendation
* Interactive Gantt
* Drag-and-Drop Planning
* Side-by-side Version Comparison

These features are naturally implemented as SPA interactions.

---

# Decision

Lab APS adopts a Single Page Application (SPA) frontend.

Technology stack:

```text
Vue 3

↓

Vue Router

↓

Pinia

↓

Axios

↓

REST API

↓

Flask Backend
```

PyWebView remains the desktop container.

Flask becomes a REST API server only.

---

# Rationale

## Clear Separation of Responsibilities

Frontend responsibilities:

* View rendering
* Navigation
* Client-side state
* User interaction

Backend responsibilities:

* Business rules
* Domain model
* Scheduling
* Persistence

Responsibilities remain independent.

---

## Rich Workspace Experience

The Planning Workspace becomes a true application workspace.

Examples

* Switching tabs without page reload
* Live KPI updates
* Version comparison
* Interactive filtering

The SPA model provides a significantly better user experience.

---

## Better Testability

Frontend can be tested independently.

Backend can be tested independently.

API contracts become explicit.

This aligns with the previously defined OpenAPI Specification.

---

## Future Web Deployment

The backend remains identical whether the application is:

* Desktop (PyWebView)
* Internal Web
* Cloud Deployment

Only the hosting mechanism changes.

---

# Alternatives Considered

## Option A — Flask + Jinja2 Templates

Rejected.

Suitable for administration systems.

Not suitable for an APS workspace with rich client interaction.

---

## Option B — Flask + Vue CDN

Rejected.

Difficult to scale.

Creates mixed frontend technologies.

---

## Option C — Vue 3 + REST API

Accepted.

Provides the clearest separation of concerns.

Supports future evolution without changing business architecture.

---

# Consequences

Positive

* Modern frontend architecture
* Independent frontend development
* Better state management
* Easier future deployment
* Better user experience

Negative

* Frontend build pipeline required
* JavaScript tooling required
* Two development processes (frontend/backend)

These costs are acceptable considering the long-term benefits.

---

# Architectural Impact

The following layers remain unchanged:

* Domain
* Application
* Planning Engine
* Scheduling Engine
* Database
* Solver

Only the Presentation Layer changes.

This demonstrates the effectiveness of the existing layered architecture.

---

# Project Structure Impact

The implementation structure becomes:

```text
src/

    backend/

        api/

        application/

        domain/

        engines/

        solver/

        infrastructure/

    frontend/

        src/

        public/

        package.json

        vite.config.ts
```

Frontend and backend evolve independently.

---

# Related Documents

* Architecture Update 2026-07 — Vue 3 Frontend
* SAD-16 API Architecture
* SAD-19 Project Structure
* UI Information Architecture
* UI Plan Workspace Design

---

# Long-term Vision

The Presentation Layer is now completely replaceable.

Future clients may include:

* Desktop (PyWebView)
* Web Browser
* Tablet
* Mobile Companion App

All clients consume the same REST API and preserve the same Domain Model.

This decision completes the implementation architecture upgrade for Lab APS Version 1.1.
