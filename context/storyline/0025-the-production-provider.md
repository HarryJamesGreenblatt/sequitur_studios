# 0025 — The Production Provider (the board becomes a `Brief`)

> Date: 2026-08-13 · Focus: **code** — built the `ProductionProvider` seam the whole
> `0005` → `0008` → `0024` arc was building toward. The Production board (stood up on
> Azure DevOps in `0024`) can now be *read* into a `Brief` the crew engine assembles,
> and the assembled `Sequence` *written* back onto it. The mirror of the `Renderer`
> protocol (`0021`), but for the **decision** plane instead of the execution plane.

---

## What happened

- **Finished the two board prerequisites `0024` left open.** Added the two Shot fields —
  **`Mood`** (text) and **`Look`** (a picklist of the seven `Look` presets, custom values
  allowed) — via the process REST API, and **scaffolded an example
  Act → Scene → Beat → Shot tree** (one Act, one Scene, one Beat, two Shots on the Camera
  area path, each with a mood and a look) as the first read target. Two gotchas worth
  recording: the Fields **Add** endpoint only *attaches* an already-existing org-level
  field, so each field must be **created org-wide first, then attached** to the Shot type;
  and `az boards work-item create` **silently drops a picklist field** at create time (the
  string `Mood` took, the picklist `Look` didn't) — it has to be set with a follow-up
  `update`.

- **Built `sequitur/production.py` — the `ProductionProvider` seam.** A
  `runtime_checkable` **`ProductionProvider`** protocol with two methods —
  `read_brief(*, scene=None) -> Brief` and `write_sequence(sequence) -> None` — and two
  backends behind it:
  - **`AzureDevOpsProduction`** — the live board, over the ADO REST API. It authenticates
    with the same **`DefaultAzureCredential`** identity already used for Key Vault (mint a
    token for the public ADO resource id), so it adds **no new dependency** — just stdlib
    `urllib`. `read_brief` runs a WIQL query for the Shot work items, batch-fetches their
    fields, and builds the `Brief`; `write_sequence` PATCHes each Shot's `Look` with the
    grade the crew applied.
  - **`LocalFolderProduction`** — a JSON-file **test double** that honours the same
    protocol with no network, realizing the "local folder" provider `0005` always
    reserved. It lets the whole round-trip be tested offline through the real engine.

- **Added `config.get_ado_config()`** — an `AzureDevOpsConfig(org_url, project,
  resource_id)`. Everything is non-secret (the board is authorised by the caller's Entra
  identity, so there is *no key*): the org URL and project are tenant-specific
  infrastructure names read only from the gitignored `.env`, while the ADO resource id is
  the **public, first-party constant** (identical for every organisation) and so is a safe
  default in code.

- **Tested and live-verified.** A new `tests/test_production.py` (5 tests) drives the
  `LocalFolderProduction` round-trip **through the real crew `Engine`** — board → `Brief` →
  assembled graded `Sequence` → board — entirely offline; all **31 smoke tests pass**. Then
  verified against the live board both directions: `read_brief` returned the scene label,
  the aggregated look, and the two shots with their moods; a full `write_sequence`
  round-trip PATCHed a Shot's `Look` on the actual board (restored afterward so the example
  tree keeps its distinct per-shot looks as a fixture).

## Decisions

1. **A protocol with two backends, but *no* registry.** The `Renderer` seam (`0021`) has a
   medium-keyed registry because its *holder* — a role — asks for a renderer *by medium*
   and shouldn't know the concrete class. Here the holder (the CLI, or a future engine
   binding) picks a production backend *directly*; a registry would be indirection with no
   caller. Backend-swappability comes from the shared protocol alone (`LocalFolderProduction`
   ↔ `AzureDevOpsProduction`), not a lookup table. (Avoiding the over-engineering the
   `Renderer` pattern might have tempted.)

2. **`urllib` + `DefaultAzureCredential`, not a new SDK.** The board is a REST API and the
   identity is already in the toolbox (Key Vault uses it). A WIQL query + a batch fetch +
   a JSON-patch update is a handful of calls — not worth an `azure-devops` package or a
   `requests` dependency. The credential authorises the board read/write exactly as it
   authorises the vault read.

3. **The v1 read is flat and positional — deliberately matched to the engine.** Every Shot
   in the project becomes one unit of coverage in work-item-id order. That is exactly the
   shape `Director.assemble` consumes (it lays the brief's shots into one ordered scene), so
   the flat read is not a shortcut around the model — it *is* the model the assemble phase
   speaks today. Read and write correlate **positionally** (both walk Shots in id order),
   so no work-item ids need threading through the `Brief`. Scene-scoped reads (a WIQL tree
   query) are a later refinement.

4. **Per-shot look aggregates to a single brief nudge (a named v1 limitation).** The board
   holds a `Look` *per Shot*, but a `Brief` carries *one* look hint and the engine applies
   *one* base grade to the whole sequence. So `read_brief` aggregates to the first shot's
   look, and `write_sequence` records that uniform grade back onto every shot. Honouring
   the distinct per-shot looks is the **shot-matching** work (Color Correction Handbook
   Ch. 9) already queued for the Colorist — this seam surfaces the need rather than hiding
   it.

## Resulting state

- The studio can now **read a production off the board and write the assembled result
  back** — `sequitur/production.py` (`ProductionProvider` + `AzureDevOpsProduction` +
  `LocalFolderProduction`), wired into the public surface and `config.get_ado_config()`.
  The board's two Shot fields (`Mood`, `Look`) exist and an example
  Act → Scene → Beat → Shot tree is scaffolded as a read fixture. `tests/test_production.py`
  (5) covers the offline round-trip through the real engine; **31 smoke tests green**.
- The engine still takes a bare `Brief` in its own API — the provider is the *supplier* of
  that brief, not yet bound *into* `Engine`. Concrete infra identifiers stay in the
  gitignored `.env` / local notes, per the no-infra-names-in-shipped-docs rule.

## Open threads

- **Bind the provider into the engine** — let `Engine` read its `Brief` from a
  `ProductionProvider` (and write its `Sequence` back) instead of the caller passing a bare
  `Brief`, so a production runs board-to-board.
- **Scene-scoped read** — a WIQL *tree* query so `read_brief(scene=…)` returns just that
  scene's coverage, replacing the flat "every Shot in the project" read.
- **Per-shot grade matching (Color Correction Handbook Ch. 9)** — carry each shot's own
  look through the assemble phase so `write_sequence` stops flattening distinct looks to a
  single base grade.
- **Write more than the look** — advance work-item **State** (and other fields) on write, so
  a graded shot visibly progresses on the board; today the write records only the applied
  `Look`.
- **Phase axis** — still deferred (`0024`): represent plan / shoot / assemble as an
  iteration or a Shot field.
- **`OutputStore` (the bytes side of `0005`)** — a Graph-backed store for the rendered
  media, the companion seam to this decision-plane provider; and **app-only auth** for
  unattended/CI use (interactive `az login` covers local today).

---

## Addendum — operationalizing the board (same session)

With the provider code committed, we drove the actual board as a *user* would and hit
three real gaps — none in the code, all in the ADO board's configuration. Fixing them
turned the board from "work items exist" into "each crew has a working Kanban bucket."

### What happened

- **Finished the board prerequisites `0024` deferred.** Added the two Shot fields —
  **`Mood`** (text) and **`Look`** (a picklist of the seven presets, custom allowed) — and
  scaffolded an example **Act → Scene → Beat → Shot** tree as the provider's first read
  target. (Gotcha: the Fields *Add* endpoint only *attaches* an existing org-level field, so
  each must be created org-wide first; and `az boards work-item create` silently drops a
  picklist value at create time — set `Look` with a follow-up `update`.)

- **The board showed nothing.** Root cause: the default team was scoped to the *exact* root
  area with **child areas excluded**, so every work item (all in department sub-areas) was
  filtered out. Set the team's area to include children → the master board now shows the
  whole production.

- **Made "departments as buckets" real — per-department teams.** ADO **cannot pivot a
  board's columns onto Area Path** (columns are workflow *States*, full stop), so the
  Planner "buckets as columns" idea isn't available on one board. The native ADO equivalent
  is **Team + Area Path**: created **seven department teams** (Direction, Camera, Lighting,
  Grip, Editorial, Color, Sound), each scoped to its existing department Area Path, and kept
  the default **`… Team`** as the **all-departments master board** (the Producer's overview).
  Each crew now opens *its own* board and sees *its own* work — the `0008` "crew picks up its
  own bucket" idea as an actual UI surface. It is **buckets-as-boards** (switch teams), not
  buckets-as-columns (side by side) — the one thing ADO's Kanban won't do.

- **Gave the leaf a board — the backlog-level cascade.** The department boards were still
  empty because **Shot sat on the Task backlog tier, which ADO denies a Kanban board**
  (tasks live only on the sprint taskboard / as checklists). Since the crews work *at the
  Shot level*, that tier must be a first-class board. Fixed it structurally by moving the
  whole hierarchy **up one level**: **Shot → Requirement** (now boarded), Beat → Epic,
  Scene → the custom portfolio, Act → a **new top portfolio level**; then renamed the levels
  **Shots / Beats / Scenes / Acts**. Every narrative level now has a Kanban board, and each
  department team shows its shots as draggable cards.

- **Surfaced the right boards on each team.** New teams default the *custom* portfolio levels
  (Acts, Scenes) to **hidden**, so a department initially offered only **Beats / Shots** — and
  perversely, the levels a team actually owned (Direction's Acts/Scenes) were the hidden ones.
  Enabled all four levels (`backlogVisibilities`) on all eight teams, so every board switcher
  now offers Shots / Beats / Scenes / Acts.

- **Clarified why the boards look sparse.** With one small example tree (5 items) and the
  narrative levels owned by *different* departments — Act/Scene in **Direction**, Beat in
  **Editorial**, the two Shots in **Camera** — each team is populated only at the level(s) it
  owns and empty elsewhere. That is inherent, not a bug: the narrative spine (Acts/Scenes/
  Beats) lives with Direction/Editorial, while the **Shots** board is the one that matters for
  the shoot/post crews, and the master team is the only view populated at every level. Fuller
  boards are a matter of more sample data, not more configuration.

1. **Department = Team + Area Path, not board columns.** This is the ADO-native realization
   of the `0024` "department is an axis orthogonal to state" decision. Making department a
   *state* (to fake Planner columns) was rejected — it would destroy the workflow axis, the
   very "Planner smushes two axes" trap `0024` avoided.

2. **Keep the default team as the master board.** It can't be cleanly deleted (it anchors the
   project default dashboard and the project-wide security/notification group), and it earns
   its keep as the all-departments overview. Not a gremlin — the Producer's whole-production
   view above the seven crew buckets.

3. **The working tier deserves a board — move Shot to the Requirement level.** A structural
   fix, not a settings tweak: the tier the crews actually operate in (Shot) should be
   boarded, so the hierarchy shifts up one level rather than leaving the leaf on the boardless
   task tier. (The Basic Task type was already disabled, so the vacated task tier is empty.)

### Resulting state

- **8 teams / 8 boards:** a master **all-departments team** (the project's default team) +
  seven department teams, each scoped to its Area Path. Backlog levels are now
  **Acts → Scenes → Beats → Shots**, all four with working Kanban boards (all four enabled on
  every team); `Shot` lives on the Requirement tier. The example tree's two shots appear on
  the Camera team's **Shots** board; Direction's Act/Scene on its Acts/Scenes boards.
- This was **ADO process/infrastructure surgery — no `sequitur/` code changed** and nothing
  to commit; concrete identifiers stay in the gitignored `.env` / local notes. The provider
  code from the main entry is unaffected (it queries `Shot` work items by type, independent of
  which backlog tier they sit on).

### Board REST gotchas (for the next agent)

- REST **team creation does not spawn a duplicate Area Path** (the portal does); the new
  team's area starts empty and must be pointed at the existing department area.
- REST-created teams start with **no backlog iteration** → the board shows *TF400509
  "Configuration required"* until `backlogIteration` is set to the project root iteration.
- A work-item type can reference **only one backlog behavior** (`VS403194`) → to move a level,
  **remove the old behavior before adding the new**.
- Creating a portfolio level: `POST …/behaviors` with `inherits` as a **string** ref name.
  Renaming a level uses **PUT** (not PATCH). Boards get **no** Kanban view for the **Task**
  tier — the reason the whole cascade was necessary.
- New teams default the **custom** portfolio levels to **hidden** (`backlogVisibilities`) —
  enable them per team (PATCH team settings) or a department only offers the built-in
  Epic/Requirement boards.
