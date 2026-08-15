# 0037 — The Production, Parameterized

> Date: 2026-08-15 · Focus: **code** — made the **Production** a first-class parameter. One
> ADO project = one Production instance (`0024`), but `ADO_PROJECT` was read as a fixed value,
> so the studio could only ever address *one* production. Now the project is an **argument**
> (explicit › `.env` default), threaded config → provider → CLI, with a `list_productions()`
> enumerator — the prerequisite for the multi-production dailies world (`0036`). 39 tests green.

---

## What happened

- **Split the ADO pointers by what actually scales.** `ADO_ORG_URL` (the studio org) and the
  process template are **studio-wide constants**; `ADO_PROJECT` (the Production) is
  **per-production**. So `ADO_PROJECT` in `.env` is reframed as the *default active production*,
  not the only value.

- **Threaded `project` as a parameter** (explicit › env default):
  - `config.get_ado_config(project=None)` — resolves `project or os.environ["ADO_PROJECT"]`;
  - `AzureDevOpsProduction(*, project=None)` — builds its config with that selection (still no
    network at construction — the token stays lazy);
  - `scripts/produce.py --production NAME` — the CLI selector, defaulting to the `.env` value.

- **Added the enumerator.** `AzureDevOpsProduction.list_productions()` — a classmethod that needs
  **no** project selected (it's what you call *before* picking one): reads `ADO_ORG_URL`,
  authenticates with the caller's Entra identity, and returns the org's project names sorted.
  Exposed as `produce.py --list-productions`. **Live-verified** (returns `ASequiturProduction`).

- **Guard test** (`tests/test_production.py`, now 7): the project defaults to the env pointer and
  an explicit argument overrides it, on both `get_ado_config` and `AzureDevOpsProduction`, while
  `org_url` stays constant — all offline (construction hits no network). Suite **39 green**.

## Decisions

1. **`.env` value = default, selection = parameter.** The single-production case stays
   zero-friction (the default just works); multi-production is `--production <name>` or a
   `project=` argument — no `.env` juggling. Mirrors how `read_brief(*, scene=…)` already
   overrides a default.

2. **`ADO_PROCESS_NAME` stays a constant.** It's the org-level *template* every production is
   created on (the thing that makes them structurally identical). It only becomes per-production
   if the studio ever wants *different* templates — YAGNI today.

3. **`list_productions()` needs no project by design.** Enumeration must precede selection, so it
   takes `org_url` (+ the public ADO app constant) and no project — you can't require the thing
   you're trying to choose.

## Resulting state

- The Production is now a parameter everywhere it's addressed: `get_ado_config(project=…)` →
  `AzureDevOpsProduction(project=…)` → `produce.py --production`, with `--list-productions` to
  enumerate. `provision_production.py` already *creates* new projects and the OutputStore keys are
  already per-production, so the studio now scales across productions with only the selector made
  dynamic. No behaviour changed for the single-production default; 39 tests green.

## Open threads

- **Bind the selector into the Director / dailies loop** — "which production?" as a plan-phase
  choice (enumerate → pick → work), the natural companion to the `0036` gate ritual.
- Unchanged from `0036`: build the **`OutputStore`** (Tier-0 OneDrive junction is in place), the
  **deliverable + gate ritual**, the **Screenwriter treatment**, and the **Production Designer
  seat + key-art source**.
