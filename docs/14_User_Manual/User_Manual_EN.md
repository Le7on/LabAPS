# docs/14_User_Manual/User_Manual_EN.md

# Lab APS — User Manual

**Product:** Laboratory Advanced Planning & Scheduling Platform (Lab APS)

**Version:** 1.0

**Audience:** Laboratory planners, production leads (Production LM) and
administrators.

**Chinese version:** [User_Manual_ZH.md](User_Manual_ZH.md)

---

# 1. What Lab APS Does

Lab APS turns your laboratory's resources and workflows into an optimized
production schedule, then tracks its execution.

You describe:

- **Resources** — equipment (with capabilities) and staff (with skills and
  qualifications), each with availability windows.
- **Workflows** — reusable templates of operations, each with a duration and the
  capability / skill / qualification it needs.
- **Demand** — how much of each project you need, and how urgent it is.

Lab APS then generates a schedule that assigns each operation to a capable
machine and a qualified operator, respects dependencies and availability, and
prioritizes urgent demand. You review it, publish it, and drive execution
(start / complete / fail / cancel) with a full audit trail.

---

# 2. Key Concepts

| Term                | Meaning                                                                                                     |
| ------------------- | ----------------------------------------------------------------------------------------------------------- |
| Equipment           | A machine with a set of capabilities (e.g. "pcr") and optional availability windows.                        |
| Staff               | An operator with skills and qualifications (which can expire) and optional availability.                    |
| Project             | A body of work that demand is raised against.                                                               |
| Workflow Definition | A reusable template: an ordered set of operations with requirements.                                        |
| Operation           | One step: a duration plus what it needs (capability, skill, qualification).                                 |
| Plan                | A production plan for a planning horizon (e.g. a week).                                                     |
| Plan Version        | One attempt at solving a plan; it has a lifecycle (see §7).                                                 |
| Demand              | A requested quantity for a project, with a priority (low / normal / high).                                  |
| Planning Context    | An immutable snapshot of resources taken when a version's work is generated, so a schedule is reproducible. |
| Assignment          | The result: an operation placed in time on an equipment (and staff).                                        |

---

# 3. Getting Started

## 3.1 Running the application

Desktop (recommended for a single user):

```text
cd frontend && npm run build
python desktop.py
```

A window titled "Lab APS" opens. If PyWebView is not installed, open a browser
at `http://127.0.0.1:5000`.

Development (two processes):

```text
python run.py                 # backend API on http://127.0.0.1:5000
cd frontend && npm run dev     # UI on http://127.0.0.1:5173
```

## 3.2 Signing in

If authentication is enabled, the app shows a **Sign in** screen. Paste your API
token and sign in. Your name and role appear at the bottom of the left sidebar;
use **Sign out** to end the session. Ask an administrator to issue you a token if
you do not have one.

---

# 4. The Workspace

The left sidebar navigates the app:

- **Dashboard** — counts across the system at a glance.
- **Plans** — create and list production plans.
- **Scheduling** — the main workspace: build, schedule and execute a plan version.
- **Laboratory**
  - **Projects** — the projects demand is raised against.
  - **Equipment** — machines and their capabilities / availability.
  - **Staff** — operators, skills, qualifications and availability.
  - **Workflows** — reusable operation templates.

---

# 5. Setting Up Laboratory Data

Do this once (and update as things change).

## 5.1 Projects

Projects → enter a **project code** and **name** → **Add project**. Deactivate a
project with the button on its row; deactivated projects are hidden from new
scheduling but past schedules are unchanged.

## 5.2 Equipment

Equipment → fill in:

- **Code** and **Name**.
- **Capabilities** — comma separated, e.g. `pcr, spin`. An operation that
  requires a capability can only run on equipment that has it.
- **Availability** — optional time windows as `start-end` pairs, e.g.
  `0-40, 60-100`. Leave blank for always available. (Times are in the planning
  horizon's units.)

## 5.3 Staff

Staff → fill in:

- **Code** and **Name**.
- **Skills** — comma separated, e.g. `pcr, elisa`.
- **Qualifications** — `name:expiry` pairs, e.g. `gmp:2099-12-31, iso`. A bare
  name (`iso`) never expires. An operation requiring a qualification is only
  assigned to staff whose qualification is still valid.
- **Availability** — like equipment.

## 5.4 Workflows

Workflows → set a **workflow code** and **name**, then add operation rows. For
each operation:

- **Operation type** and **Duration**.
- Optional **Capability** (equipment), **Skill** and **Qualification** (staff).

Use **+ Operation** to add rows and **✕** to remove them, then **Create
workflow**.

---

# 6. Planning & Scheduling

Go to **Scheduling**. The workspace walks you through four steps.

## Step 1 — Plan & workflow

Pick a **Plan** (create one under Plans first) and a **Workflow**, then
**Create version & generate**. This creates a new plan version and generates its
operation instances, capturing an immutable snapshot of the currently active
equipment and staff.

## Step 2 — Demand (optional)

Choose a **Project**, a **Quantity** and a **Priority**, then **Add demand**.
Demand makes the scheduler favor finishing higher-priority work sooner. With no
demand, it simply minimizes the overall finish time (makespan).

## Step 3 — Schedule

Optionally set **Frozen until** (a time before which nothing may start — useful
to lock in near-term work). Click **Run scheduler**. The result shows the
**makespan** and whether the problem was **feasible**.

If it is infeasible, a required capability, skill, qualification or availability
cannot be satisfied by the active resources — adjust resources or the workflow
and re-run.

## Step 4 — Review, publish, execute

- **Review & publish** moves the version through Reviewed to Published and makes
  its assignments executable (Ready).
- The **Timeline** shows assignments as bars grouped by resource.
- In the **Assignments** table, drive execution per row: **Start** → **Complete**
  (or **Fail** / **Cancel**, which ask for a reason).

---

# 7. Plan Version Lifecycle

A version moves in one direction:

```text
Working → Scheduled → Reviewed → Published → Archived
```

- **Working** — just created; no accepted schedule yet.
- **Scheduled** — a feasible schedule was produced.
- **Reviewed** — the planner accepted it.
- **Published** — the official schedule; it is immutable and its assignments
  become executable. Only one published version per plan.
- **Archived** — a historical record.

Trying an invalid step (e.g. publishing before review, or re-scheduling a
published version) is rejected with a clear message.

---

# 8. Executing Assignments

Once a version is published, each assignment starts as **Ready** and moves:

```text
Ready → Running → Completed
             ↘ Failed (reason required)
Ready  ↘ Cancelled (reason required)
```

Every transition is recorded in an audit history you can retrieve per
assignment. Completed / Failed / Cancelled are final.

---

# 9. Reporting

- **Dashboard** — totals for plans, versions, published versions, equipment,
  staff and workflows.
- **KPI** (via the reporting API) — assignment status breakdown and per-equipment
  workload (assignment count and total busy time).

---

# 10. Roles

- **Production LM** — day-to-day planning: plans, versions, scheduling, execution.
- **Administrator** — everything above, plus creating users / issuing tokens.

Access is enforced by the API; if you lack the role for an action you receive a
"forbidden" message.

---

# 11. Troubleshooting

| Symptom                                                       | Likely cause / fix                                                                                                                                            |
| ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Valid authentication token required"                         | Not signed in, or the token expired — sign in again.                                                                                                          |
| Schedule is **infeasible**                                    | No active resource satisfies a required capability / skill / qualification, or availability / frozen window leaves no room. Check resources and the workflow. |
| An operation is unassigned or errors on qualification         | The staff qualification has expired — update its expiry on the Staff page.                                                                                    |
| A deactivated machine/person still appears in an old schedule | Snapshots are immutable by design; deactivation only affects future scheduling.                                                                               |
| Nothing happens on "Run scheduler"                            | Generate instances first (Step 1); you cannot schedule an empty version.                                                                                      |

---

# 12. Notes on Time and Units

This release schedules in abstract integer time units within a planning horizon
(not wall-clock dates). Durations, availability windows and the frozen boundary
all use the same units. Calendar dates and shifts are a planned enhancement.
