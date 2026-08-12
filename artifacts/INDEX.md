# Grounding Library

Sequitur Studios grounds its generative workflow in real film-craft domain
knowledge rather than vague prompts. This directory **hosts the source
materials** ("grounding contexts") — one folder per work — that the studio's
code and reasoning are derived from.

Sources are organized by the **production phase / department** they serve (see
[`../context/architecture.md`](../context/architecture.md) for how each maps to a
workflow layer and the crew roles it supports).

## Catalog

| Source | Department / phase | Status | Folder |
|--------|--------------------|--------|--------|
| **Grammar of the Shot** — Bowen, 4th ed. | Production — cinematography: framing, composition, lens, lighting, shooting-for-the-edit | Imported · abridged · **encoded** under `sequitur/crew/` | [`grammar of the shot/`](grammar%20of%20the%20shot/INDEX.md) |
| **Grammar of the Edit** — Bowen, 4th ed. | Post-production — editing, continuity assembly, pacing, transitions | Imported · **abridged** (8 ch); grounds `edit.py` + the `Editor` role | [`grammar of the edit/`](grammar%20of%20the%20edit/INDEX.md) |
| **The Screenwriter's Taxonomy** — Eric R. Williams | Development — story: a genre/voice/pathway/POV *classification system* | **Imported · abridged** (8 ch, `0016`) into `reference/` + source INDEX. Enum-friendly → a future `Screenwriter` role vocabulary | [`the screenwriter's taxonomy/`](the%20screenwriter's%20taxonomy/INDEX.md) |
| **Directing: Film Techniques and Aesthetics** — Rabiger & Hurbis-Cherrier, 6th ed. | Director-centric **spine** across plan→shoot→assemble→ship (dramaturgy, aesthetics, casting/actors, production process, post, delivery) | **Imported · abridged** (28 ch, `0017`) into `reference/` + source INDEX. Grounds the **Director** role; secondary for many depts | [`directing/`](directing/INDEX.md) |
| **Professional Storyboarding: Rules of Thumb** — Paez & Jew | Pre-production — **previsualization**: turning a script into a shot-by-shot visual plan (staging, board types, the storyboarding workflow) | **Imported · abridged** (10 ch, `0018`) into `reference/` + source INDEX. Grounds a **Storyboard Artist** seat + the **reference-keyframe** pipeline (a board panel = an `ImageStudio` keyframe) | [`professional storyboarding/`](professional%20storyboarding/INDEX.md) |
| **Sound** — Jay Rose, *Producing Great Sound for Film and Video* | Production & post — sound department (multi-phase) | **Imported** (`0009`/`0010`); **abridged (18 ch)** into `reference/` + source INDEX. Composite grounding: Grammar of the Edit Ch. 3 + toaster-strudel MCP (score). *(Yewdall 4th evaluated & rejected — too anecdotal.)* | [`producing great sound for film and video/`](producing%20great%20sound%20for%20film%20and%20video/INDEX.md) |
| Production design / color | Art department — sets, costume, grade | **Partly grounded:** Directing Ch. 23 (visual design) + Ch. 36 (grade/finishing) *(abridged, `0017`)*; dedicated design/color source still planned | *(see [`directing/`](directing/INDEX.md))* |

## Anatomy of a source folder (the convention)

Each imported work follows the same shape, so a new agent (or a new source) knows
exactly where things live:

```
<source name>/
  extraction/   raw imported originals (.docx, etc.) + media/   ← copyright-sensitive
  source/       converted verbatim text — ground truth (.md)     ← copyright-sensitive
  reference/    abridged, session-ready references (.md)         ← transformative, safe to ship
  INDEX.md      this source's grounding index (chapter → code map)
```

## Adding a new source

1. Create the `<source name>/` folder and drop originals into `extraction/`.
2. Convert to Markdown into `source/` (pandoc: `-t gfm --wrap=none --extract-media`).
3. Abridge each chapter into `reference/` (spare, session-ready; end each with a
   "Studio application" section tying it to the code).
4. Write the source's `INDEX.md` grounding index (copy the shape of Grammar of
   the Shot's).
5. Add a row to the catalog above, and map it into
   [`../context/architecture.md`](../context/architecture.md).
6. **Copyright:** if `extraction/` and `source/` are verbatim copyrighted text,
   add them to `.gitignore` before any public push. Only `reference/` ships.
