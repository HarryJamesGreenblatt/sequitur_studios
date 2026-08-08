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
| **Grammar of the Shot** — Bowen, 4th ed. | Production — cinematography: framing, composition, lens, lighting, shooting-for-the-edit | Imported · abridged · **encoded** in `sequitur/grammar.py` | [`grammar of the shot/`](grammar%20of%20the%20shot/INDEX.md) |
| **Grammar of the Edit** — Bowen, 4th ed. | Post-production — editing, continuity assembly, pacing, transitions | Imported · **abridged** (8 ch); post layer `movie.py` planned | [`grammar of the edit/`](grammar%20of%20the%20edit/INDEX.md) |
| Story / screenwriting | Development — script, structure | Planned | — |
| **Sound** — Yewdall, *Practical Art of Motion Picture Sound* (4th) | Production & post — sound department (multi-phase) | **Designed** (`0009`); Yewdall **to acquire**. Composite grounding: Grammar of the Edit Ch. 3 + toaster-strudel MCP (score) | — |
| Production design / color | Art department — sets, costume, grade | Planned | — |

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
