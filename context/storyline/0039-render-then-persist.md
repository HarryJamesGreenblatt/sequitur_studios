# 0039 — Render, Then Persist

> Date: 2026-08-15 · Focus: **code** — wired the execute-hook to the output store, closing
> **decision → pixels → durable** in one call. `Director.execute` now takes an optional
> `store` (+ owning `production`, and a `phase`): it renders to a scratch path as before,
> then files that artifact through `OutputStore.put` and returns a `RenderResult` whose
> `ref` is the **durable** location. The dailies model's render→persist step. 47 tests green.

---

## What happened

`0038` built the `OutputStore` seam (bytes → a durable ref); `0032` built `Director.execute`
(a greenlit `Shot` → rendered bytes at a scratch path). This session joined them: a render is
only a *daily* once it survives past the workstation, so the execute-hook now optionally
persists.

- **`Director.execute(shot, *, medium=…, out_path=…, store=None, production=None, phase="shoot",
  name=None)`.** With no `store` it behaves exactly as before (render → scratch `RenderResult`).
  With a `store`, it files the rendered artifact under `production / phase / name` and returns a
  `RenderResult` whose `ref` is the durable store path — the same tuple type, just a better `ref`.
  This is precisely what `render.py`'s docstring anticipated: *"a local Path today, a URL once
  outputs live in a store."*

- **Guard: a store requires a production.** You cannot key an artifact without the production
  that owns it, so `store` without `production` raises `ValueError` — fail loud at the boundary.

- **Tests** (`tests/test_engine.py`, now 8): a fake renderer writes real bytes to the scratch
  path, then `execute(store=…, production=…, name=…)` files them — asserting the returned `ref`
  is the store location `…/HeistNoir/shoot/shot_001.png` and the bytes made it there; plus the
  store-without-production error. All offline (no credentials, no network). Suite **47 green**.

## Decisions

1. **Persistence is opt-in and non-breaking.** The store is an optional parameter, not a new
   method — the existing render-only contract (and its test) is untouched. The batch path,
   the CLI, and the coming gate ritual all call the same hook, passing a store when they want
   durability.

2. **The store *upgrades* the ref, it does not wrap it.** `execute` keeps returning a
   `RenderResult`; only its `ref` changes from scratch to durable. No new return type, no new
   concept — the seam already models "ref = a Path now, something else later" (`Path | str`).

3. **`phase` is the store's `layer`, defaulting to `"shoot"`.** The execute-hook renders a
   `Shot`, which is shoot-phase work, so `"shoot"` is the natural default; a caller in another
   phase overrides it. This keeps the store key (`production / layer / name`) meaningful without
   the hook needing to know about the whole phase model.

4. **The hook stays backend-agnostic on both sides.** It resolves the renderer from the registry
   *by medium* and takes the store *by protocol* — never a concrete class of either. The Director
   orchestrates render + persist without binding to a video backend or a storage backend.

## Resulting state

`Director.execute` now closes render → durable end-to-end: a greenlit `Shot` becomes bytes in the
tenant's OneDrive-backed store, addressed by `production / phase / name`, returned as a durable
`RenderResult`. Both judgment tiers (code + the Director agent) reach it through the one hook. No
new dependency, no new public symbol; 47 tests green; render-only behaviour unchanged.

## Open threads

- **The gate ritual (next).** A small `Deliverable` record (production · phase · ref · status) +
  a per-phase review point: present the durable ref to the Producer (chat + board), approve →
  advance State/phase, revise → re-open and re-run *that* phase. This is what consumes the durable
  ref this hook now produces.
- **Non-shot deliverables.** The plan phase's treatment (text) and poster (image) file through the
  same `OutputStore.put` — they don't go through `execute` (which renders a `Shot`), so the gate
  ritual should persist an arbitrary artifact directly, not only via the shot hook.
- Unchanged from `0036`: the **Screenwriter treatment** (Directing Ch. 3–11), the **Production
  Designer seat + key-art source**, then the first slice — **plan → {treatment + poster} → gate**.
