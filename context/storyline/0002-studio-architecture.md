# 0002 — Studio architecture + grounding-library formalization

> Date: 2026-08-07 · Focus: grow the vision from "grammar-of-the-shot encoder"
> toward a **production studio** with department roles and a multi-source
> grounding library — and clean up the docs so they don't conflate purpose at
> publish time.

## Why

`grammar.py` now grounds one department (camera) in one phase (production). A real
studio needs every department across all phases (Appendix D lists the roles). To
grow well, the repo needs (a) an explicit workflow architecture mapping roles →
grounding → code, and (b) a grounding library that can host *more than one* source
(e.g. *Grammar of the Edit* for post-production).

## What happened

1. **Formalized the grounding library.** The deprecated top-level one-pager
   (`grammar of the shot/reference.md`) was superseded by a per-source **grounding
   index** (`grammar of the shot/INDEX.md`) — a chapter → code map + folder-layout
   guide. Added a top-level `artifacts/INDEX.md` cataloging *all* sources by
   production phase/department, with an "anatomy of a source folder" convention
   and an "adding a new source" recipe. Deleted the deprecated `reference.md`.
2. **Encapsulated the Appendix-D roles into the workflow.** New
   [`context/architecture.md`](../architecture.md) maps **phase → department/role →
   grounding source → code layer → status**. It makes explicit that the studio
   today implements the camera/grip/electric departments in the production phase,
   and scaffolds pre-pro, post, and delivery as the intended shape. Design
   principle recorded: *every responsibility is served by a grounding source + a
   code layer; a user steps into a role and gets that role's grounded vocabulary.*
3. **Named *Grammar of the Edit* as the next source to acquire** — it grounds the
   post-production/editorial layer, which unlocks the **sequence** layer (Ch. 5 of
   Grammar of the Shot is that layer's spec).
4. **Doc-naming cleanup (anti-conflation for publish).** Too many `README.md`
   files. Convention adopted:
   - `README.md` — **repo root only** (canonical landing page).
   - `INDEX.md` — navigational catalogs of contents (`artifacts/INDEX.md`,
     `artifacts/grammar of the shot/INDEX.md`).
   - `OVERVIEW.md` — orienting narrative guides (`context/storyline/OVERVIEW.md`,
     formerly the devlog's `README.md`).
   Repointed all cross-links; verified no broken links.

## Key decisions / conventions (durable)

- **Doc naming:** `README.md` (root) · `INDEX.md` (catalogs) · `OVERVIEW.md`
  (guides). Don't add second-level `README.md`s.
- **Architecture is role-first:** phase → department (Appendix D) → grounding
  source → code layer. `context/architecture.md` is the map; keep it current as
  layers land.
- **The grounding library is multi-source.** Every source follows the same
  `extraction/ · source/ · reference/ · INDEX.md` shape; register it in
  `artifacts/INDEX.md` and map it in `context/architecture.md`.
- **Roles stay design-level for now** — only make `role`/`department` first-class
  in code once a *second* department (editorial) exists to justify it.

## Resulting state

Docs are publish-clean (no `README` conflation). The grounding library is
formalized and ready to host additional sources. The full production-studio
architecture is captured in `context/architecture.md`, with the camera/production
layer marked implemented and the editorial/post layer marked as the clear next
step (pending *Grammar of the Edit*).

## Open threads

- **Acquire *Grammar of the Edit*** → run the standard pipeline (extraction →
  source → reference → INDEX), then build the **sequence/edit** layer.
- **Publish** — still blocked on copyright hygiene: gitignore
  `artifacts/**/extraction/` and `artifacts/**/source/` (verbatim book text)
  before any public push; ship only `reference/`.
- **Make roles first-class in code** — deferred until editorial exists.
