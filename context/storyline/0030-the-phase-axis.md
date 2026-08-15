# 0030 — The Phase Axis (pre/prod/post as named sprints)

> Date: 2026-08-14 · Focus: **board design + infrastructure** — closed the phase axis
> that `0024` deferred ("iteration or a field"). Reframed the Act→Scene→Beat→Shot tree as a
> *multi-department* decomposition rather than a camera-centric one, then gave the three
> **production phases** a real, board-native home: **named, dateless iterations** baked into
> the provisioning template. Only [`scripts/provision_production.py`](../../scripts/provision_production.py)
> changed — no `sequitur/` code.

---

## What happened

- **Named the shallowness.** The concern: the board looked **camera-centric** (only the
  camera's deliverable — the `Shot` — is a work-item type) and had **no home for the
  production phases** pre/prod/post. The worry was that without a phase axis, non-camera
  work would get **conflated between Beat and Shot**.

- **Reframed the tree as multi-department.** The Act→Scene→Beat→Shot spine was *never* a
  camera decomposition — the `0025` team wiring already assigns **Act/Scene→Direction,
  Beat→Editorial, Shot→Camera**. Each narrative level's *granularity* is set by one
  department's atom, but each level is *worked* by several:

  | Level | Sets the granularity | Also worked by |
  |---|---|---|
  | Act | Screenwriter (structure) | score movements |
  | Scene | Production Design (set / concept) | sound ambience · colour scene-balance |
  | **Beat** | **Editor (the cut)** | **Composer (score / rhythm)** |
  | Shot | DP (the take) | upstream reference frame · per-shot grade · per-shot capture |

  This resolves the Beat/Shot worry directly: **a Beat is the editor's unit (the cut); a
  Shot is the DP's unit (the take)** — they *must* stay distinct because they belong to
  different crafts. It also corrects an over-tidy first pass: **sound aligns to Beat**
  (cut-to-cue = the beat grid, Rose Ch. 14), so Beat is the *rhythm* level co-owned by
  Editor + Composer.

- **Gave phase a board-native home — named sprints.** Phase is **orthogonal** to narrative
  (an Act is worked in all three phases), so it must **not** be a work-item parent above Act
  (that would falsely nest narrative under phase). It's the **iteration** axis — and iteration
  is the *only* ADO axis with native cross-team **board** tooling (the Sprints hub); a plain
  field would give only queries. Created three **dateless** iterations — **Pre-Production /
  Production / Post-Production** — and subscribed all eight teams, so every crew gets a
  Pre/Prod/Post switcher over its department bucket.

- **Solved ADO's "current" quirk.** With no dates, ADO marks the **alphabetically-first**
  iteration `current` (verified empirically — creation order *and* dates ruled out). A
  fresh production should open on **Pre-Production**, so the iteration names carry a
  **load-bearing leading digit** (`1/2/3`) — digits sort below letters, pinning `current`
  to Pre even against the stray default `Sprint 1`. An **emoji** follows the digit as pure
  decoration (it sorts *high*, so it can't carry the ordering itself): `1 🎬 Pre-Production`,
  `2 🎥 Production`, `3 ✂️ Post-Production`.

- **Baked it into the template.** All of the above is now in the provisioner
  (`PHASES` + `ensure_iterations()` + `subscribe_teams_to_phases()`), idempotent and
  non-destructive, and **run live** against the production board — so every future
  production inherits the phase axis for free.

## Decisions

1. **The narrative tree is a multi-department decomposition, not camera-centric.** Non-camera
   deliverables map to the *upper levels* (Scene = production design, Beat = editorial + score)
   — they don't get bolted onto the `Shot`. Camera merely owns the finest atom (the leaf).

2. **Phase = the iteration axis, never a work-item parent.** Orthogonality forbids nesting
   narrative under phase; and iteration is the only axis that yields a *board* experience.

3. **Named, dateless sprints with a load-bearing numeric prefix.** ADO's dateless-`current`
   rule is alphabetical, so the digit pins a new production to open on Pre-Production; the
   emoji is decoration. (`:` is an invalid iteration-name char — hence a space/`.`, not `1:`.)

4. **Encapsulate pre/prod/post behind the seam.** Phase stays a closed, typed axis: the code's
   `Phase` enum (`plan`/`shoot`/`assemble`) is the shared pivot the engine already turns on,
   and the board's three iterations sit behind a `ProductionProvider` map — the sprint
   mechanics never leak into callers (the same discipline as the `Renderer` seam).

## Resulting state

- [`scripts/provision_production.py`](../../scripts/provision_production.py) now provisions the
  **three named phase iterations** and subscribes all eight teams; the live board carries them
  with **`1 🎬 Pre-Production` = current** on both the master and department teams. Dry-run is
  idempotent (the emoji nodes read `exists`). The default `Sprint 1/2/3` nodes are left in
  place (non-destructive).
- **No `sequitur/` code changed** — this was board design + template infrastructure.

## Open threads

- **Build the encapsulating provider surface** — a `_PHASE_ITERATION` map (`Phase → iteration`),
  phase-scoped `read_brief(phase, …)`, and an `advance(shot, to=…)` verb for a Shot graduating
  from one phase-sprint to the next. Designed here, not yet built.
- **Deliverables-as-items** — phase-as-iteration gives a work item exactly *one* iteration, which
  suits the **Shot** (it flows pre→prod→post) but means a Scene's pre-prod *design* and post
  *colour-balance* can't both live on the one node. The likely next move is modelling non-camera
  department deliverables — especially the **upstream production-design reference frame** that
  seeds the render — as their own phased work items.
- **Cosmetic** — optionally retire the default `Sprint 1/2/3` nodes (left untouched to keep the
  provisioner non-destructive on existing boards).
