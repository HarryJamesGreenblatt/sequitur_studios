# 0026 — The Production Template (a one-command board provisioner)

> Date: 2026-08-13 · Focus: **code** — turned the ad-hoc, throwaway board setup from
> the `0025` session into a single **idempotent provisioner** so a new production can be
> stood up to "where we are now" with one command. The infrastructure sibling of the
> `ProductionProvider` seam: that reads/writes an *existing* board; this **stands one up**.

---

## What happened

- **Named the two tiers of the "template".** Standing up a production has an org-level tier
  and a per-project tier, and only the first was already reusable:
  - **Org-level (already a template):** the inherited **process** *is* the reusable template
    for the board's *structure* — the Act/Scene/Beat/Shot work-item types, the `Mood`/`Look`
    fields, and the backlog-level cascade that puts `Shot` on the Requirement tier. Every
    project created on the process inherits all of it for free.
  - **Per-project (was ad-hoc):** the Area Paths, department Teams, and team settings
    (iteration + backlog-level visibilities + the default team's include-children) were done
    by hand via throwaway probe scripts in the `0025` session — tribal knowledge, not a
    template.

- **Consolidated the per-project tier into one script.** New
  [`scripts/provision_production.py`](../../scripts/provision_production.py) takes a project
  name and idempotently stands up: the project on the process → the seven department **Area
  Paths** → the default team's *include-children* → a **team per department** (each scoped to
  its area) → each team's **backlog iteration + level visibilities**. It reuses the studio's
  own stack — `DefaultAzureCredential` for auth and stdlib `urllib` for REST (the same
  no-new-dependency approach as [`production.py`](../../sequitur/production.py)) — and reads
  only non-secret pointers from `.env` (`ADO_ORG_URL`, `ADO_PROCESS_NAME`).

- **Made it safe to run and to re-run.** Every step is **detect-then-act** (skip what exists),
  so re-running is a no-op, and a **`--dry-run`** reports intended actions without touching
  anything. Validated dry-run against the existing project: it correctly saw the project, all
  seven areas, and all seven teams as already present, and made no changes. Sample items are
  **opt-in** via `--with-example` (the demo Act → Scene → Beat → Shot tree); the default is a
  clean, empty board.

## Decisions

1. **The provisioner is infrastructure, the provider is runtime — keep them siblings, not
   merged.** `provision_production.py` *creates* a production's board; `AzureDevOpsProduction`
   *reads/writes* an existing one. Different lifecycles, different call sites; a shared REST
   idiom (urllib + `DefaultAzureCredential`) but no forced coupling.

2. **A script, not a process/project export.** ADO has no first-class "clone a project with its
   teams, areas, and settings" feature, so a version-controlled, idempotent script is the
   pragmatic, reviewable template — and it doubles as executable documentation of the whole
   per-project setup (including every gotcha the `0025` addendum recorded).

3. **Reproduce, don't hard-code.** The provisioner **resolves the process by name** and
   **discovers the custom portfolio levels** from the process behaviors (rather than baking in
   GUIDs), so it self-adjusts to the process as it stands and reproduces the real structure.

## Resulting state

- `python scripts/provision_production.py "My New Film"` stands up a fresh production board
  identical to the current one, minus samples; `--with-example` seeds the demo tree; `--dry-run`
  previews. The org-level process remains the structural template it always was; this closes the
  per-project gap. Added one non-secret pointer (`ADO_PROCESS_NAME`) to the gitignored `.env`.
- Validated via `--dry-run` against the live project (all detection correct, no mutation). The
  per-project write calls (areas / teams / settings) are the same ones exercised live in the
  `0025` session; the project-create-and-poll path runs on the first real provision.

## Open threads

- **First real run** — provision an actual second production when a name is chosen, exercising
  the project-create-and-poll path end-to-end (dry-run covers everything else).
- **Optional process bootstrap** — a companion that (re)creates the *org-level* process itself
  (work-item types, fields, the backlog cascade) for full from-scratch disaster recovery; today
  the process is assumed to already exist.
- Back to code: **bind the `ProductionProvider` into `Engine`** so a provisioned production runs
  board-to-board (the standing `0025` thread).
