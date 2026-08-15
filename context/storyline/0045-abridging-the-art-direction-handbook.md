# 0045 — Abridging *The Art Direction Handbook*: the Production Designer, grounded

> Date: 2026-08-15 · Focus: the **abridgement session** `0044` deferred — transform
> Michael Rizzo's *The Art Direction Handbook* (8-chapter `source/`) into **8
> session-ready `reference/` chapters** grounding the planned **Production Designer**
> seat over `ImageStudio`. A **grounding** entry (transformative references + doc
> reconciliation); **no code.** Closes the last source gap.

---

## What happened

`0044` staged the source (verbatim `source/` + a chapter → seat `INDEX.md`) and deferred
the transformation. This session ran it — the `0017`/`0043` pattern: **full comprehensive
reads fanned out to parallel subagents**, each writing `reference/` directly, clustered
by arc.

1. **Three parallel subagents, clustered by arc:**
   - **Remit & department (Ch. 1, 2)** — Introduction (the Art Director as **design
     manager**; the Production Designer vs. Art Director split — PD owns the *concept*,
     AD owns the *realisation*) · Responsibilities, Relationships & Setup (the hierarchy
     of loyalties, the interdepartmental interfaces, the art-department roster).
   - **Design core (Ch. 3, 4, 7)** — the high-value arc, the payload for the generative
     backend: Visual History · The Design Process (script → **visual concept** → research
     → thumbnails → concept art → models → drafting — the spine of the seat) · CGI and
     Digital Filmmaking (matte painting → digital set extension → fully synthetic scene —
     the bridge to prompting a model).
   - **Physical, historical & logistics (Ch. 5, 6, 8)** — surgical abridgement: The
     Physical Design (location-vs-build, the set list, spatial design) · A Legacy of
     Historical Techniques (a lexicon of in-camera techniques a generative model
     collapses) · Paperwork & Daily Shooting Tasks (art-department logistics).

2. **Every chapter matches the house idiom** (title · citation+scope blockquote · craft
   sections with tables · a closing **Studio application** grounding the *planned*
   Production Designer seat over `ImageStudio`, with code + sibling cross-links · overlap
   flags · a linked transition; Ch. 8 closes the set). **Link integrity verified**: all
   relative cross-links across the eight files resolve on disk, with `%20`/`%27` encoding
   for spaced sibling paths.

3. **Reconciled the living docs:** the source
   [`INDEX.md`](../../artifacts/the%20art%20direction%20handbook%20for%20tv%20and%20film/INDEX.md)
   flipped **staged → abridged** (each chapter row now links its reference); the catalog
   row in [`artifacts/INDEX.md`](../../artifacts/INDEX.md) → **Imported · abridged (8 ch,
   `0044`→`0045`)**; and the Production Designer grounding cell in
   [`architecture.md`](../architecture.md) now cites Rizzo as *abridged*.

## Decisions

1. **No new `crew/` module.** Every chapter grounds the **planned** Production Designer
   seat — a *peer* `Role` to the Director in the plan phase, owning the frame's look
   while the Director owns the shot's intent. The seat is not yet in code; the references
   are its charter, cross-linked to the modules that exist today
   ([`image.py`](../../sequitur/image.py), [`prompt.py`](../../sequitur/prompt.py),
   [`director.py`](../../sequitur/crew/director.py)).

2. **The visual concept is the strongest through-line.** Rizzo's Ch. 4 "visual concept"
   — one central metaphor that "optically binds" a film — is the plan-phase intent the
   whole image backend serves: the art-department *overlay* the machine-readable
   `Screenwriter` descriptor classifies but cannot *narrate*, and the concept a future
   Production Designer seat must hold coherent across every `build_prompt` call.

3. **Honesty about weak transfer, recorded in the references themselves.** Ch. 6 gives a
   *lexicon* but zero process; Ch. 8 is human production management with no analogue and
   maps to a future AD/logistics concern; Ch. 5's location-vs-build economy has no
   analogue — only design intent survives. Ch. 7's digital-art-direction lineage, by
   contrast, *is* what `ImageStudio` does — one `build_prompt` call is a concept
   illustration.

## Correction logged

- **Rizzo Ch. 3 is not a period-palette chapter.** The `0044` staging map assumed
  "Visual History" supplied era/style palette vocabulary; the full read showed it is a
  **media-technology** history (persistence-of-vision, telecine, film-vs-video look) plus
  a **genre taxonomy**. The reference reflects what is actually there and points the
  palette-concept grounding to the **Colorist** (`Look`/`Cast`/`TonalRange`) and the
  Color Correction Handbook instead. The INDEX scope note records the correction.

## State

- **The source library is complete** — all nine full sources now `source/` + `reference/`
  + `INDEX.md`, every plan/shoot/post/art department grounded. No source gap remains.
- **`Brief` link precision:** one chapter (Ch. 4) initially bundled `Brief` under the
  `director.py` link; fixed to point at its real home,
  [`role.py`](../../sequitur/crew/role.py), consistent with Ch. 1–2.
