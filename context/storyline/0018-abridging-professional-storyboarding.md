# 0018 — Abridging Professional Storyboarding

> Date: 2026-08-12 · Focus: fold in a **sixth grounding source** — a followup the
> user judged worth the cycles: transform Paez & Jew's *Professional Storyboarding:
> Rules of Thumb* (10 curated chapters) from verbatim `source/` into **10 session-ready
> `reference/` chapters** grounding a **Storyboard Artist / previz** seat. A
> **grounding** entry (transformative references + doc reconciliation); no code.

## What happened

`0017` closed out the last *staged* source and declared the grounding library
"complete for the departments modelled today." This session reopens grounding for one
deliberate addition: **previsualization**, which the architecture had gestured at
(the "reference keyframe" note on the image backend) but never sourced. The book was
already sitting as ten `.docx` files in `artifacts/professional storyborading/` (the
folder name was corrected to `professional storyboarding`).

1. **Set up the house folder layout + converted the source.** Moved the 10 `.docx`
   originals into [`extraction/`](../../artifacts/professional%20storyboarding/extraction/)
   and ran `pandoc -f docx -t gfm --wrap=none --extract-media` into
   [`source/`](../../artifacts/professional%20storyboarding/source/) as `chNN.md`
   (both gitignored). Recovered the book's TOC from the chapters' own nav links to
   confirm titles and that chapters **11–12 (portfolios/unions/business) were dropped**
   at import — the same career/gear-trimming curation used for Directing.

2. **Abridged all 10 chapters via four parallel subagents** (the `0017` pattern —
   full comprehensive reads, not iterative semantic search, writing `reference/`
   directly). Clustered by arc: **foundations & the artist (1–3)** Overview · Visual
   Literacy · Drawing; **film grammar for boards (4–6)** Cinema Language · Story
   Structure · Emotion; **staging & board practice (7–8)** Staging · Storyboard Types;
   **the storyboarding process (9–10)** Storyboarding · Advanced Techniques. Each
   chapter matches the house idiom (title · blockquote scope · core idea · craft
   sections · a closing **"Studio application"** with cross-links).

3. **Reconciled the living docs:** a new source
   [`INDEX.md`](../../artifacts/professional%20storyboarding/INDEX.md) (chapter → code
   map), the catalog row in [`artifacts/INDEX.md`](../../artifacts/INDEX.md), a new
   **Storyboard Artist · Previs** row + a "reading-the-map" note in
   [`architecture.md`](../architecture.md), and the README (intro → six sources,
   pre-production row, Layout, the now-grounded reference-keyframe roadmap item, and the
   License).

## Decisions

1. **Storyboarding earns a seat because Sequitur *is* a generative previs pipeline.**
   The abridgement's through-line: a storyboard **panel** encodes the *same* grammar the
   cinematographer owns (shot size, angle, composition, movement), so a board is a
   **pre-rendered [`Shot`](../../sequitur/shot.py)**, and a board panel is the literal
   form of the **reference keyframe** the video studio conditions a shot on
   ([`ImageStudio`](../../sequitur/image.py)). This gives the long-deferred
   reference-keyframe flow a *grounded* home rather than a bare TODO.

2. **Ch. 8 (Storyboard Types) is the keystone mapping.** A *continuity board* → the
   ordered `Shot` list; an *animatic* → the assembled edit ([`edit.py`](../../sequitur/edit.py)
   + [`cutter.py`](../../sequitur/cutter.py)); *previs* ("rough 3D block-out with
   accurate lenses, cut into an animatic") → functionally what
   [`studio.py`](../../sequitur/studio.py) + the edit layer produce. The
   blueprint-vs-conceptual axis also tells the [`Director`](../../sequitur/crew/director.py)
   reconciler *how binding* a plan-phase `Contribution` should be.

3. **The board is the plan-phase seat that commits the shot grammar FIRST.** Cinema
   Language (Ch. 4) and Staging (Ch. 7) restate *Grammar of the Shot*'s composition and
   coverage grammar as decisions made *before* the shoot; the DP on set (or the render)
   executes what the board decided. Ch. 10 (motion/time in a still — arrows, multi-panel
   moves) is the board analogue of the video-only faces `build_prompt` adds over
   `build_image_prompt`.

## Resulting state

- Professional Storyboarding is the library's **sixth abridged source**.
  `source/`+`extraction/` stay gitignored (the existing `.gitignore` globs already cover
  them); the 10 `reference/` chapters + INDEX ship. **Six sources total, all abridged**
  (Grammar of the Shot, Grammar of the Edit, Rose, Taxonomy, Directing, Storyboarding).
- It grounds a new **Storyboard Artist / previz** role (plan phase) — still **unmodeled
  in code**, framed as a role that emits a per-shot keyframe and feeds it to
  `Studio.render` as a conditioning reference (image-to-video).
- Overlap flags preserved for future encoding: **Cinema Language / Staging** (Ch. 4/7 ↔
  Grammar of the Shot Ch. 1–3/5), **Story Structure** (Ch. 5 ↔ Taxonomy Ch. 6 /
  Directing Ch. 5), **Emotion** (Ch. 6 ↔ Directing Ch. 10–11).

## Open threads

- **Design the `StoryboardArtist` role** — a plan-phase seat (there is no `ART`/previz
  `Department` in [`role.py`](../../sequitur/crew/role.py) yet) that chooses an **output
  fidelity** per shot (thumbnail vs. finished keyframe) and emits an `ImageStudio`
  keyframe; its `Contribution` seeds the `Brief` the `Director` reconciles.
- **Wire the reference-keyframe flow (now grounded)** — pass a `gpt-image-1` still into
  `Studio.render` as a conditioning reference so the shot inherits the board's
  composition (image-to-video). This was a standing open thread; Storyboarding is its
  grounding.
- Carried from `0017`: the `Screenwriter` role (`crew/screenwriting.py`); a Director
  `PersonaJudgment` (**B**); the casting/actors dimension; a dedicated design/color
  source; crew-engine assemble-phase behaviour + Production binding; the reconciliation
  sweeps.
