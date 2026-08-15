# 0042 — Staging *Directing the Story*: the storytelling half landed

> Date: 2026-08-15 · Focus: execute the `0041` staging plan for the first of its two
> sourced books — **Francis Glebas' _Directing the Story_**. The Producer delivered the
> **storytelling half** (chapters 5–13, 15); this session **converted → gated → mapped →
> reconciled** it into a staged `source/` + a chapter→seat `INDEX.md`. A **grounding /
> staging** entry (the `0015` pattern): verbatim `source/` + the chapter→seat map; **no
> `reference/` abridgement, no code.** The per-chapter abridgement is deferred to its own
> designated session.

---

## What happened

The Producer sourced *Directing the Story* — but the delivery arrived in **stages**, with
a few extraction defects to reconcile across the session before the clean set was in hand:

1. **Untangled a mislabeled delivery.** The first drop contained two **duplicate,
   mis-numbered** files: `CH-10.md` was byte-identical to `CH-11.md` (both *Ch. 11,
   Dramatic Irony*), and `CH-13.md` matched `CH-15.md` (both *Ch. 15, Scheherazade*). The
   real Ch. 10 and Ch. 13 were missing. Surfaced this; the Producer confirmed **Ch. 14 is
   intentionally skipped** and re-extracted **10** and **13** as raw `.docx`. Ch. 13
   needed a second re-extraction (the first re-drop was still wrong); the final pass
   verified correct — **Ch. 10 → "How to Convey and Suggest Meaning"**, **Ch. 13 →
   "Aiming for the Heart."**

2. **Converted extraction → verbatim `source/`** with the standard pandoc pass, keeping the
   producer's convention (the `<img>` tags remain; the media bytes are stripped). The two
   corrected chapters overwrote the wrong duplicates; the delivered storytelling half is now
   **10 unique chapters** — **5, 6, 7, 8, 9, 10, 11, 12, 13, 15** (14 omitted).

3. **Copyright gate verified.** The global `.gitignore` globs (`artifacts/**/extraction/`,
   `artifacts/**/source/`) already cover the new folder — `git check-ignore` confirmed both
   `source/*.md` and `extraction/*.docx`. Only the transformative `INDEX.md` (and the eventual
   `reference/`) ship.

4. **Mapped chapters → seats and wrote the source `INDEX.md`** —
   [`directing the story/INDEX.md`](../../artifacts/directing%20the%20story/INDEX.md): all
   delivered chapters ground the **Director** and/or **Screenwriter** (the `0041` decision —
   no new `crew/` module), with the overlaps to reconcile at abridgement logged inline (story
   spine ↔ Taxonomy Ch. 6 / Directing Ch. 5; staging a beat ↔ Directing Ch. 10–11 / Prof.
   Storyboarding Ch. 5–6).

5. **Reconciled the living docs:** the *Directing the Story* row in
   [`artifacts/INDEX.md`](../../artifacts/INDEX.md) moved from **Sourcing (`0041`)** →
   **Imported · staged (`0042`)**, and the **Screenwriter** + **Director** grounding cells in
   [`architecture.md`](../architecture.md) now cite Glebas *(staged, 10 ch, `0042`)* alongside
   Rabiger and Williams.

## Decisions

1. **Stage now, abridge later — hold the `0015` line.** Even though the book is short, the
   per-chapter `reference/` transformation is a **full comprehensive read** (the `0017`/`0018`
   parallel-subagent pattern) and belongs in its own context-heavy session. This session locks
   the *plan* (verbatim source + chapter→seat map) and **defers** the abridgement.

2. **The delivered set is the storytelling half by design.** Chapters 1–4 (intro) and the
   book's whole **storyboarding** half were dropped at source — redundant with *Professional
   Storyboarding* (`0018`) — per the `0041` filtered-extraction decision. **Ch. 14 is an
   intentional omission** (the Producer's call), not a delivery gap. The `INDEX.md` records
   this so a later agent doesn't "repair" a non-problem.

3. **Trust-but-verify every extraction.** The duplicate/mislabel defects (and the recurring
   need to re-extract) confirm the staging discipline: **always diff sizes and read the title
   line** of each converted chapter before writing the `INDEX`. Byte-identical files across two
   chapter numbers is the tell.

4. **Glebas grounds existing seats — the map says so, code doesn't change.** The `INDEX`'s
   chapter→seat column and the architecture edits are **documentation leads**, not new modules.
   The payoff is deferred to the treatment/poster producers the `0036` first slice needs.

## Resulting state

- *Directing the Story* is **imported, gated, and mapped**: 10-chapter verbatim `source/` +
  a staged [`INDEX.md`](../../artifacts/directing%20the%20story/INDEX.md); catalog and
  architecture reconciled. **No `reference/`, no code.** The library now lists **eight** sources
  (seven abridged, one staged).
- The naming guard holds: `directing the story/` (Glebas, visual storytelling) is distinct from
  `directing/` (Rabiger, the Director spine).

## Open threads

- **Abridge *Directing the Story* — its own designated session** (the `0017`/`0018` pattern):
  transform the 10 `source/` chapters into `reference/` + refresh the `INDEX`, staying surgical
  on Glebas' distinctive visual-storytelling material (skip what merely restates Rabiger).
- **Stage the production-design source** (the second `0041` book — Rizzo's *Art Direction
  Handbook*, still raw `.docx` in `extraction/`) in a **dedicated session**: convert → gate →
  map → the Production Designer seat, then abridge.
- Then the **two plan producers** these unblock: the Screenwriter **treatment** output (grounded
  Directing Ch. 3–11 + Glebas) and the **Production Designer** seat + poster — the `0036` first
  slice **plan → {treatment + poster} → gate**.
