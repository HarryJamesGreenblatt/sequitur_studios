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
