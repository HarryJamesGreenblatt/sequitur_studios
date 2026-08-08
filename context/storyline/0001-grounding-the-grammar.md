# 0001 — Grounding the grammar in the source

> Date: 2026-08-07 · Focus: replace the shallow grammar with one *derived from the
> actual book*, and build a durable, session-ready reference from it.

## Why

Review of the genesis output showed `grammar.py` and `reference.md` were built
from a shallow read of *Grammar of the Shot*. The user has the digital book and
wanted the code informed by the **source**, not by a summary chasing the code.

## What happened (in order)

1. **Migrated the book.** User dropped the chapters/appendices into
   `artifacts/grammar of the shot/extraction/` as `.docx`. Converted them to
   Markdown with **pandoc** (`-t gfm --wrap=none --extract-media`). Confirmed it's
   the **4th edition** (DOI 10.4324/9781003257356).
2. **Organized.** Renamed everything to a `chNN-slug` / `appendix-x-slug`
   convention (kept `.md`/`.docx` pairs aligned). Moved the converted `.md` into
   `source/` (ground truth); `.docx` originals stayed in `extraction/`.
3. **Abridged, per chapter.** Read each chapter in full and wrote a spare,
   session-ready reference into `reference/` — one file per chapter. Format:
   *scope line → core idea → tight thematic sections (tables for dense material) →
   a "Studio application" section tying the chapter to the code.* Dropped pedagogy
   (exercises, reviews, history). The 3 appendices were moved into `reference/`
   **as-is** (short, useful reference material, not worth abridging).
4. **Rewrote `grammar.py` from the source.** The single biggest change. Bowen's
   material is genuinely *orthogonal axes*, so the enums now compose instead of
   forcing one pick:
   - **Framing:** added `ShotSize.VERY_LONG` (VLS); split the horizontal
     `SubjectView` from the vertical `CameraAngle`; added `ShootingStyle`
     (objective/subjective) and `Composition` (centered/thirds).
   - **Lens/focus (Ch. 3):** added `FocalLength` and `DepthOfField`; kept `lens`
     for free-text extras.
   - **Lighting (Ch. 4):** split the old flat `Lighting` enum into `LightQuality`,
     `LightScheme`, `LightDirection`, `ColorTemperature` + an `eye_light` flag.
   - **Motion (Ch. 6):** extended `CameraMovement` (gimbal, drone, whip-pan,
     pan-tilt, dolly-zoom) and added a temporal `MotionSpeed` axis (slow/fast/
     time-lapse), distinct from `timing`.
   - Updated `prompt.py`, `sequitur/__init__.py`, and `scripts/generate.py` to
     match. Verified with `--dry-run`; no errors.
5. **Remediated docs.** `README.md` still advertised the removed `--light` flag,
   the deleted `Lighting` enum, and a non-existent `docs/` path — all fixed to the
   new grammar and the real `artifacts/` tree.
6. **Reconciled the reference to the code.** The abridged chapters' "Studio
   application" sections had flagged the very gaps the rewrite closed (and cited
   the old `Lighting.*` names). Updated ch01–ch06 to describe the grammar
   *as implemented*.

## Key decisions / conventions (durable)

- **Source is ground truth for both code and reference.** If they drift, fix the
  reference to match the source-derived code — never re-shallow the code.
- **Raw source vs. abridged output stay separate** (`source/` vs `reference/`).
- **Grammar is layered/orthogonal**, mirroring the book — layers compose on one
  `Shot`.
- Reference chapters end with a **"Studio application"** section; keep it accurate
  to the code.

## Resulting state

`grammar.py` is now faithfully source-derived; the full `reference/` library
exists and is in sync with the code; README is accurate. `--dry-run` composes
correct prompts across all the new axes (verified with a fisherman example and a
cellist example).

## Open threads

- **Publish as a repo** (next goal). Pre-publish checklist:
  1. **Copyright:** gitignore `artifacts/grammar of the shot/extraction/` and
     `source/` (verbatim book text). Ship only the transformative `reference/`.
     `.gitignore` does **not** exclude them yet.
  2. Confirm no secrets are staged (`.env` is already ignored; `.env.example` is safe).
  3. Consider a `LICENSE`, a short "grounding" note crediting Bowen, and a minimal
     smoke test for `build_prompt`.
- Broader discipline library (editing/sound/directing/…), and the **sequence
  layer** (Ch. 5 is its spec) remain future work.
