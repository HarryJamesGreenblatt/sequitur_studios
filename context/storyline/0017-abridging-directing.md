# 0017 — Abridging Directing

> Date: 2026-08-08 · Focus: run the **last of the designated abridgement sessions**
> deferred in `0015` (after `0016` did the Taxonomy) — transform Rabiger &
> Hurbis-Cherrier's *Directing: Film Techniques and Aesthetics* (6th ed.), the larger
> staged plan-phase source, from verbatim `source/` into **28 session-ready
> `reference/` chapters** spanning every production phase. A **grounding** entry
> (transformative references + doc reconciliation); no code.

## What happened

`0015` staged Directing as a **Director-centric spine** — 28 curated chapters (3–11,
17–20, 23–37) touching every phase — with verbatim `source/` and a chapter→role
*plan*, deferring the heavy abridgement because the book is long. `0016` cleared the
smaller staged source (the Taxonomy). This session clears the last one: **Directing**.

1. **Read all 28 chapters in full, in parallel — no further pruning.** Per the user's
   direction the source was scanned **comprehensively, nothing dropped** (the curation
   was already made at staging). To avoid the fidelity loss of iterative semantic
   search over a large corpus, the reading was **fanned out to nine subagents** (3–4
   chapters each, clustered by arc), each doing a full read of its chapters and writing
   the abridged references directly, then reporting a compact digest back.

2. **Wrote 28 abridged [`reference/`](../../artifacts/directing/reference/) chapters**,
   matching the house idiom (title · blockquote scope · core idea · craft sections · a
   closing **"Studio application"** tying each chapter to the code layer it grounds,
   with cross-links). By arc:
   - **Story & dramaturgy (3–8)** — drama primitives, the beat/dramatic-unit machinery,
     plot/time/structure, screenplay form, script judgment, script analysis.
   - **Aesthetics & interpretation (9–11, 17)** — cinematic POV, form & style, tone/
     style/genre, the preproduction interpretation toolkit.
   - **Performance (18–20)** — casting, acting fundamentals, directing actors — the new
     **casting/actors** dimension no other source and no code models.
   - **Production process (23–37)** — visual design, shooting script, line producing,
     crew assembly, production tech, on-set, directing on set, continuity, post
     overview, footage assessment, rough cut, fine cut/picture lock, music, finishing,
     delivery.

3. **Reconciled the living docs:** the directing
   [`INDEX.md`](../../artifacts/directing/INDEX.md) (staged → abridged; per-chapter
   reference links), the catalog row + production-design row in
   [`artifacts/INDEX.md`](../../artifacts/INDEX.md), and the Director/Producer/
   Screenwriter/Casting/Editor/Colorist/Sound/delivery rows + the reading-the-map note
   in [`architecture.md`](../architecture.md).

## Decisions

1. **Parallel subagent fan-out over iterative semantic search.** A 28-chapter corpus
   read one-at-a-time via search would lose signal to context churn. Nine subagents,
   each doing a **full comprehensive read** of a 3–4-chapter cluster and writing its
   references in one pass, preserved fidelity and finished in two waves. Each was given
   the exact house idiom, the copyright rule, the codebase map, and the cross-link
   target lists so the outputs cohere as one connected web.

2. **Abridge the whole source, nothing dropped.** Same rule as `0016`: the selection
   was made at staging, so all 28 chapters were abridged in full — including the
   production-process chapters that overlap other sources (post, sound, music), kept as
   the **director's-eye complement**, not a replacement.

3. **Directing is a *control spine*, not a single-department cell.** The Studio
   applications converge on the same picture the staging note predicted: POV (Ch. 9) is
   a **hard constraint** on camera coverage + the Editor's cross-cutting; the objective/
   subjective axis is a **rendering-fidelity switch**; tone/genre (Ch. 10–11) is a
   **global style contract** biasing crew defaults; the shooting script (Ch. 24) is the
   **PLAN→SHOOT bridge** to the `Shot` list; Ch. 26 (developing a crew) is **meta to the
   crew engine itself** (its department roster ≈ the `Department` enum, its chain of
   command ≈ the Director reconciler); Ch. 30 (continuity) is the **shoot↔edit seam**;
   Ch. 31–34 deepen the existing `Editor`; and Ch. 25/37 ground the **Producer = human**
   ship gate. This source is the natural corpus for a Director `PersonaJudgment` (the
   **B** in the A→B seam).

## Resulting state

- Directing is now the library's **fifth abridged source** — and the last staged one.
  `source/`+`extraction/` stay gitignored; the 28 `reference/` chapters + INDEX ship.
  **Five sources total, all abridged** (Grammar of the Shot, Grammar of the Edit, Rose,
  Taxonomy, Directing) — the grounding library is **complete for the departments
  modelled today**. The next work is *code*, not grounding.
- The **casting/actors** dimension (Ch. 18–20) is grounded but still **unmodeled in
  code** — framed as a future `Casting`/`Actor` role seed wired to the voice layer
  (`0011`) and image keyframes.
- Overlap flags preserved for future encoding: **POV** (Directing Ch. 9 ↔ Taxonomy
  Ch. 7), **structure/pathway** (Directing Ch. 5 ↔ Taxonomy Ch. 6), **post** (Directing
  Ch. 30–34 ↔ Grammar of the Edit), **music** (Directing Ch. 35 ↔ Rose Ch. 14 +
  toaster-strudel).

## Follow-ups (same session, post-abridgement)

- **Scrubbed the Key Vault name from every shipped doc** — removed the hard-coded vault
  name from [`architecture.md`](../architecture.md), [`OVERVIEW.md`](OVERVIEW.md), and the
  [`0006`](0006-renderer-seam-and-image-backend.md) devlog. It's a non-secret pointer,
  but there's no reason to publish infra names; it now lives only in the gitignored
  `.env` (`KEY_VAULT_NAME`) and local memory.
- **Comprehensively revised the [README](../../README.md)** to match current state
  (it predated the crew engine, the speech backend, and the last two groundings):
  reframed the intro around the studio's two halves (a crew that *decides* + a grammar
  that renders through **three** backends), added a crew-engine usage example
  (`Engine().run(Phase.SHOOT, Brief(...))`), updated the architecture table (pre-prod +
  post + delivery now grounded), the Layout (all eight `crew/` modules, `tests/`, the
  two new grounding folders), the Roadmap ("grounding done → code next"; `SpeechRenderer`
  already built), and the License (added Williams + Rabiger & Hurbis-Cherrier). Docs only.

## Open threads

- **Design the `Screenwriter` role** — `crew/screenwriting.py` with the typed
  genre/voice/pathway/POV vocabulary (`0016`); wire its `Contribution` into the plan
  phase of the `Engine` ahead of the shoot crew.
- **Give the `Director` a `PersonaJudgment`** — Directing is now the grounded corpus for
  the **B** side of the A→B seam (`0008`/`0014`); scope the role over Ch. 7–11, 17.
- **Model the casting/actors dimension** (`0015`/`0017`) — a `Casting` role + a playable-
  intent/performance concept, wired to `image.py` keyframes and `speech.py` voices.
- **A dedicated production-design / color source** — Directing Ch. 23/36 give a first
  lead; a systematic design/grade source is still open.
- Carried: crew-engine assemble-phase behaviour + Production binding (`0014`); the
  `Renderer` protocol (`0006`); the reconciliation sweeps (align references' "Studio
  application" leads to real code as the roles land).
