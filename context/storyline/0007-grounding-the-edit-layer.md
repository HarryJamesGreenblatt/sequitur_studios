# 0007 — Grounding the edit layer; the post-production architecture takes shape

> Date: 2026-08-08 · Focus: acquire and abridge Bowen's **Grammar of the Edit**
> (the long-standing "next source"), and — because the editorial capabilities have
> **no pre-existing code to retrofit** — use that grounding to sketch the
> **post-production architecture** (`movie.py`, the shots→scenes→acts hierarchy,
> the cut-to-cue and production-dialogue problems). Grounding is **done**; the
> post-layer code is **designed, not built**.

## What happened

1. **Imported & converted.** Eight chapters of *Grammar of the Edit* (4th ed., DOI
   `10.4324/9781003257349`) arrived as `.docx` in
   [`extraction/`](../../artifacts/grammar%20of%20the%20edit/extraction/). (First
   pass failed — the files were label-encrypted, not valid ZIP/docx containers;
   re-extraction produced valid `PK`-signature files.) Converted to verbatim
   Markdown in [`source/`](../../artifacts/grammar%20of%20the%20edit/source/) via
   **pandoc** (`-t markdown --wrap=none --extract-media`), then renamed to semantic
   slugs (`ch01-the-editing-process` … `ch08-editors-mindset`).

2. **Abridged, serially.** Each chapter was read in full and abridged into
   [`reference/`](../../artifacts/grammar%20of%20the%20edit/reference/) following the
   Grammar of the Shot idiom (`# Chapter N — Title` + Scope blockquote + condensed
   sections + a **Studio application** tie-in). Wrote the source
   [`INDEX.md`](../../artifacts/grammar%20of%20the%20edit/INDEX.md) and flipped the
   [library catalog](../../artifacts/INDEX.md) row to imported/abridged.

3. **Copyright gate verified.** `git add --dry-run` confirmed only the 8
   `reference/*.md` + `INDEX.md` ship; `source/` and `extraction/` (verbatim text +
   media) stay local via the existing `artifacts/**/{source,extraction}/` ignores.

## The key departure from the shot layer

The shot layer *retrofitted* an existing POC `grammar.py`. **The edit layer has no
such code** — editing is the **post phase**, a genuinely new architectural surface.
So the references' **Studio application** sections are **provisional leads** aimed at
a *future* `movie.py`, not present code. This is deliberate: ground first, design
from the grounding, build later.

## The post-production architecture (designed from the grounding)

The intended shape, per the user's brief and what the eight chapters surfaced:

- **Production emits coverage; post assembles it.** Omni (with pre-production +
  image inputs, in a session-hosted orchestration) generates **coverage** — ~10s
  shots — organized by the native **shots → scenes → acts** hierarchy, then handed
  to a post layer.
- **`movie.py` is the post-layer stitcher**, the editorial counterpart to
  `studio.py`/`image.py`. Its hard problem is **cut-to-cue**: an agent deciding
  *where/why/how* to cut. Ch. 5's **six motivators** (information, motivation,
  composition, angle, continuity, sound) are its decision ruleset; Ch. 4's checklist
  + continuity rules are its **shot-selection** and "can-these-cut-together?"
  predicate; Ch. 4's outside-in order is a ready **assembly template**.
- **Audio: the diegetic split resolves the throw-away-sound tension.** Ch. 3
  separates **diegetic** sound (dialogue, ambience — caused by the story world) from
  **non-diegetic** (score, soundtrack, VO). Decision: **keep Omni's diegetic
  production dialogue**; treat the **soundtrack as a post (non-diegetic) decision** —
  so generated audio isn't discarded by default, and ADR/TTS overdub is the
  *fallback* for a bad take, not the norm.
- **The two audio philosophies compose.** The prior music-video workflow drove edits
  from a **beat grid/energy contour** (= Ch. 5 *time motivation*); Bowen adds
  **content motivation** (reveals, reactions, sound bridges). `movie.py` can gate a
  beat-aligned cut on whether a *motivated* reveal/reaction exists — **rhythm ×
  narrative**, generalizing beyond music videos.
- **Handles are a real constraint on fixed-length shots.** Ch. 6: dissolves/wipes
  need frames **beyond** the visible clip. So fixed-~10s Omni coverage must either
  **generate handle padding** or restrict transitions to **cuts/fades** (which need
  none) — a concrete instruction back to the coverage generator.
- **Multicam needs a shared timebase the studio lacks.** Ch. 7's free angle-cutting
  assumes common **timecode**; independently generated Omni shots have **no shared
  clock**, so multicam-style coverage must be **time-aligned** by design.
- **The image backend feeds post too.** Ch. 7's "importing stills" makes a
  `gpt-image` still a clip (crop-to-frame, hold ~5s, Ken-Burns move) — so the image
  renderer serves **both** production keyframes and post inserts/titles/cutaways.
- **Pre-production authors the deliberate edits.** Form/concept edits (Ch. 6) are
  "preconceived," so the pre-production layer should be able to **mark intended
  match/concept edits** for production to shoot and post to execute — a clean
  phase seam.

## Resulting state

- **Grammar of the Edit is grounded** — 8 abridged chapters + INDEX, the second
  full source in the library. The **editorial/post** row of
  [`architecture.md`](../architecture.md) now has a real grounding source.
- **The post architecture is specified but unbuilt** — `movie.py`, the
  shots→scenes→acts model, and the cut-to-cue engine are designed above, awaiting
  implementation.

## Open threads

- **Reconciliation sweep (standing):** the references' **Studio application** leads
  point at a not-yet-built `movie.py`. Once that analogue is designed, sweep all 8
  references to align the tie-ins to the real code (the discipline the shot layer got
  from `grammar.py`).
- **Build `movie.py`** — start with the cut-decision engine (Ch. 5 six motivators)
  over a simple shots→scenes→acts model; cuts/fades first (no handles), then handle
  padding for dissolves.
- **Time-align coverage** so multicam-style cutting and beat×content composition are
  possible.
- Carried: the `0005` provider seams; first-class roles-in-code; a `build_prompt`
  smoke test; broader discipline sources (story, production design/color).
