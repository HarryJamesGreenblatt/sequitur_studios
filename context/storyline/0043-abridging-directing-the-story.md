# 0043 — Abridging *Directing the Story*: the storytelling half, session-ready

> Date: 2026-08-15 · Focus: the **dedicated abridgement session** `0042` deferred —
> transform Francis Glebas' *Directing the Story* (the 10-chapter storytelling half,
> `source/`) into **10 session-ready `reference/` chapters** grounding the **Director**
> and **Screenwriter** seats. A **grounding** entry (transformative references + doc
> reconciliation); **no code.**

---

## What happened

`0042` staged the source (verbatim `source/` + a chapter→seat `INDEX.md`) and deferred
the per-chapter transformation. This session ran it — the `0017`/`0018` pattern: **full
comprehensive reads fanned out to parallel subagents**, each writing `reference/`
directly, clustered by arc.

1. **Three parallel subagents, clustered by arc:**
   - **Structure & the director's remit (Ch. 5, 6, 12)** — Structural Approach (the
     two-plane model: events above the *threshold of awareness*, structure below;
     narrative-question → delay → answer) · What Do Directors Direct? (capture and
     *protect* the audience's attention — contrast/motion/pointing, misdirection,
     suggestion/gestalt closure) · The BIG Picture (macro/mid/micro structure — Propp,
     Aristotle, Hero's Journey reconciled against *narration* as the real motor).
   - **Directing the eye — staging attention (Ch. 7, 8, 9)** — How to Direct the Eyes
     (the design equation Elements + Principles = Effects; "composition is subtext") ·
     Deeper in Space and Time (perspective/depth cues, telephoto-vs-wide-angle,
     layered staging, proximity as the engagement dial) · How to Make Images Speak
     (semiotics — denotation/connotation, icon/index/symbol, the four master tropes,
     genre codes).
   - **Meaning, irony, heart & synthesis (Ch. 10, 11, 13, 15)** — Convey and Suggest
     Meaning (juxtaposition, the five causalities, screen geography, the Kuleshov
     effect, the motivated cut) · Dramatic Irony (narration as control of information;
     suspense vs. surprise; the pendulum of hope and fear) · Aiming for the Heart
     (emotional targeting, the four emotion-genres, emotional truth over logic, theme
     as compass) · the Scheherazade Project (a worked end-to-end case study — the
     synthesis chapter, closing the storytelling half).

2. **Every chapter matches the house idiom** (title · citation+scope blockquote · Core
   idea · craft sections with tables · a closing **Studio application** with code +
   sibling cross-links · overlap flags · a linked transition). **Link integrity
   verified**: all relative cross-links across the 10 files resolve on disk (10/10),
   with `%20`/`%27` encoding for spaced sibling paths (the house exemplar's convention).

3. **Reconciled the living docs:** the source
   [`INDEX.md`](../../artifacts/directing%20the%20story/INDEX.md) flipped **staged →
   abridged** (each chapter row now links its reference; `reference/` now *ships*); the
   catalog row in [`artifacts/INDEX.md`](../../artifacts/INDEX.md) → **Imported ·
   abridged (10 ch, `0043`)**; and the **Screenwriter** + **Director** grounding cells
   in [`architecture.md`](../architecture.md) now cite Glebas as *abridged*.

## Decisions

1. **No new `crew/` module — confirmed by all three subagents.** Every chapter grounds
   the **existing** Director and Screenwriter seats, exactly the `0041` staging call.
   Glebas is a cross-cutting reference, not a department.

2. **Glebas resolves the "Taxonomy only classifies" gap for the treatment.** Ch. 5's
   story spine / character objectives / "aim at the heart" is the **human-readable
   telling** the plan-phase *treatment* needs — the payload the machine-readable
   Taxonomy descriptor (Supergenre/Voice/Pathway/POV) abbreviates but can't narrate.
   This is the strongest through-line the session surfaced: Glebas grounds the
   Screenwriter **treatment** output on the `0036` critical path.

3. **The Director `PersonaJudgment` (the "B" tier) gained its clearest corpus.** Ch. 6
   ("capture attention, then protect it") and Ch. 13 ("aiming for the heart") read
   directly as the Director persona's charter — the *voice* a `HeuristicJudgment`
   cannot supply. The [`judgment.py`](../../sequitur/crew/judgment.py) A→B swap is the
   Observer→Storyteller step (alongside Rabiger Ch. 9); these chapters are its grounding.

## Overlaps logged (for the encoder)

- **Story spine / structure (Ch. 5, 12)** ↔ **Taxonomy Ch. 6 (`Pathway` enum)** ↔
  **Directing (Rabiger) Ch. 5** ↔ **Prof. Storyboarding Ch. 5**. The four-way
  reconciliation for the future `Screenwriter` structural axis: the descriptor
  *classifies* (Pathway), the treatment *tells the spine* (Glebas), Rabiger gives the
  dramaturgy, the board restates it visually.
- **Dramatic irony (Ch. 11)** ↔ **POV** (Rabiger Ch. 9 limited/open-info axis · Taxonomy
  Ch. 7 Scope×Focus×Stance). Dramatic irony **is** the open-information case. One control
  surface: the Taxonomy *names* the POV → Rabiger sets the *limited/open schedule* →
  Glebas supplies the *timing craft* → the **Editor** executes the reveal
  (`EditReason`/`EditCategory` over a `Sequence`).
- **Staging / directing the eye (Ch. 7–8)** ↔ **Grammar of the Shot Ch. 2–3** (the
  `Composition`/`FocalLength`/`DepthOfField` grammar) ↔ **Prof. Storyboarding Ch. 7**.
  Glebas gives the *why* (lead the eye to the story point); the grammar gives the enums;
  the board gives the pre-visualization. A shot that reads as confusing is a
  prompt/legibility failure, not a tuning problem.
- **Emotion (Ch. 13)** ↔ **Prof. Storyboarding Ch. 6** ↔ **Directing (Rabiger) Ch. 3**;
  **conveying meaning (Ch. 10)** ↔ **Rabiger Ch. 10 (Form and Style)**.

## Resulting state

- *Directing the Story* is the library's **eighth abridged source** (10 `reference/`
  chapters + INDEX ship; `source/` + `extraction/` stay copyright-gated — the existing
  `.gitignore` globs cover them). **No code.** The grounding library is again complete
  for the departments modelled today — the outstanding source gap is the still-raw
  **Art Direction Handbook** (Rizzo, `0041`'s second book).
- The naming guard holds: `directing the story/` (Glebas) ≠ `directing/` (Rabiger).

## Open threads

- **Stage + abridge the production-design source** (Rizzo's *Art Direction Handbook*,
  raw `.docx` in `extraction/`) in its own dedicated session — the last grounding gap
  before the **Production Designer** seat.
- **Build the two plan producers** these unblock — the `0036` first slice
  **plan → {treatment + poster} → gate**: the Screenwriter **treatment** output
  (grounded Directing Ch. 3–11 + Glebas' story spine / heart) and the **Production
  Designer** seat + poster.
- **Encode the reconciliations above** when the `Screenwriter` structural/POV vocabulary
  and the Director `PersonaJudgment` are built (Glebas Ch. 5/11/13 are the corpus).
- Carried: crew-engine per-shot grade matching + real cut-decision heuristic; the
  provider-side phase seam; the Graph-backed `OutputStore` hardening.
