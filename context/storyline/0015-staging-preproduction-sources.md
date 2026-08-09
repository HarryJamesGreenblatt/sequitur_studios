# 0015 — Two pre-production sources staged: Directing + The Screenwriter's Taxonomy

> Date: 2026-08-08 · Focus: **import and stage** two new grounding sources for the
> under-served *plan* phase — Rabiger & Hurbis-Cherrier's *Directing* (6th ed.) and
> Eric R. Williams' *The Screenwriter's Taxonomy* — and **catch the documentation up
> in advance** of the heavy abridgement, which is **deferred to designated sessions**.
> A **grounding/staging** entry: verbatim `source/` + the chapter → role *plan*; no
> `reference/` abridgement and no code.

## What happened

The user curated and supplied both books into their `extraction/` folders; this
session converted, gated, mapped, and documented them.

1. **Converted extraction → verbatim `source/`** with the standard pandoc settings
   (`-t gfm --wrap=none --extract-media`). **Directing:** 28 curated chapters (the
   user's selection — 3–11, 17–20, 23–37). One file (`CH-05`) failed the first pass
   (the recurring misnamed-OLE2/`.doc` issue that also hit Rose's `CH-06` in `0010`);
   the user re-supplied a valid `.docx` and it converted (163 lines). **The
   Screenwriter's Taxonomy:** 8 chapters (1–8), clean.

2. **Copyright gate verified.** The global `.gitignore` globs
   (`artifacts/**/extraction/`, `artifacts/**/source/`) already cover both new
   sources — `git check-ignore` confirmed. Only the transformative `INDEX.md`
   (and eventual `reference/`) ship.

3. **Mapped chapters → roles and wrote both source `INDEX.md` files** — the *plan*
   the deferred abridgement sessions will execute:
   [`directing/INDEX.md`](../../artifacts/directing/INDEX.md),
   [`the screenwriter's taxonomy/INDEX.md`](../../artifacts/the%20screenwriter's%20taxonomy/INDEX.md).

4. **Reconciled the living docs:** catalog rows in
   [`artifacts/INDEX.md`](../../artifacts/INDEX.md) (the *Story/screenwriting* and
   *Production design* "Planned" rows became staged sources; a Directing spine row
   added), and the pre-production table + reading-the-map note in
   [`architecture.md`](../architecture.md).

## Decisions

1. **Stage now, abridge later — in designated sessions.** Two long sources landing
   together would blow a single session's budget and risk losing work mid-abridge
   (the `0009`→`0010` precedent: Rose was staged, then abridged in its own session).
   So this session locks the *plan* (verbatim source + chapter→role map) and defers
   the per-chapter `reference/` transformation. **Abridge per role, on demand** — not
   all 36 chapters up front.

2. **Directing is a spine, not a pre-pro-only source.** Its center of gravity is the
   **Director** — the crew engine's reconciler (`0014`), which today only *borrows*
   Grammar of the Shot Ch. 1 — but its 28 chapters seed **every** phase: dramaturgy
   (3–8), aesthetics/POV/style (9–11, 17), production process (23–30), post (31–36),
   and delivery (37). It is the natural corpus for a Director `PersonaJudgment` (the
   **B** seam).

3. **The Taxonomy is enum-friendly — it's the Screenwriter's *vocabulary*, not a
   prose manual.** Williams' supergenre → macrogenre → microgenre hierarchy plus
   Voice / Pathway / Point-of-View axes map onto **typed enums** a future
   `crew/screenwriting.py` `Screenwriter` role can own — the same pattern that turned
   *Grammar of the Shot* into `crew/camera.py`. This is why it fills the long-open
   *Story/screenwriting* cell so cleanly.

4. **A new dimension surfaced: casting/actors.** Directing Ch. 18–20 (Casting, Acting
   Fundamentals, Directing Actors) grounds a **performance department the architecture
   never modelled**. Recorded as a new pre-production row (unmodeled; future role) so
   it isn't lost.

## Resulting state

- Two sources **imported, gated, and mapped**; both `INDEX.md` files written; the
  catalog and architecture reflect the staging. **No `reference/`, no code.** The
  library now lists **five** sources (three abridged, two staged).
- Overlaps flagged for the abridgement sessions: Point of View (Taxonomy Ch. 7 ↔
  Directing Ch. 9); story craft (Directing 3–8 ↔ Taxonomy); post (Directing 31–36 ↔
  *Grammar of the Edit*); music (Directing 35 ↔ Rose).

## Open threads

- **Abridge Directing — per role, in designated session(s)** — start with the
  **Director** chapters (7–11, 17), since the role exists in code (`0014`).
- **Abridge The Screenwriter's Taxonomy** — then design a `Screenwriter` role +
  typed genre/voice/pathway/POV vocabulary (`crew/screenwriting.py`).
- **Model the casting/actors dimension** — decide whether it becomes a department in
  the crew engine.
- Carried: crew-engine assemble-phase behaviour + Production binding (`0014`); the
  `Renderer` protocol (`0006`); the reconciliation sweeps.
