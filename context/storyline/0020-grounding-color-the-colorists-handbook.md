# 0020 — Grounding Color: the Colorist's Handbook

> Date: 2026-08-12 · Focus: the **first locked step of `0019`'s sequence** — ground
> color grading. Ran the dedicated abridgement session for **Alexis Van Hurkman,
> *Color Correction Handbook*** (the seventh grounding source), transforming its 10
> chapters into session-ready `reference/` files and reconciling the library. No code.

## What happened

`0019` locked a three-step sequence — **ground color → formalize the `Renderer`
protocol → build the Colorist + grade renderer** — and flagged that abridgement is
context-heavy, so it must run in its own fresh session. This is that session for step 1.

The user sourced the handbook and shipped it **already converted to Markdown** (10
chapters in `source/`, no `.docx` originals — the convert step was done upstream), so
the job was the abridge → reconcile half of the house pipeline.

Following the `0017`/`0018` pattern, the full read was fanned out to **five parallel
subagents** (two chapters each, full reads — not semantic search — writing `reference/`
directly and reporting digests). The 10 chapters:

1. Color Correction Workflows · 2. Setting Up a Color Correction Environment ·
3. Primary Contrast Adjustments · 4. Primary Color Adjustments · 5. HSL Qualification
and Hue Curves · 6. Shapes · 7. Animating Grades · 8. Memory Colors · 9. Shot Matching
and Scene Balancing · 10. Quality Control and Broadcast Safe.

Each abridged chapter ends with a **Studio application** section of *provisional leads*
(the Colorist role and the grade renderer are not built yet).

## Decisions

1. **Folder = `artifacts/color correction handbook/`** (named for the book, matching the
   house convention), not the working title "color grading" from `0019`. Copyright is
   already covered — the `.gitignore` `artifacts/**/source/` glob catches the new
   `source/`; only `reference/` + `INDEX.md` ship.

2. **Scope = grading only** (as `0019` decided): primary (contrast + color), secondary
   (HSL/hue-curve, shapes), memory-color targets, animated grades, shot matching, and
   broadcast-safe QC. **Production-design *concepts*** (sets/costume/palette) stay a
   **separate** open cell (Directing Ch. 23 is its lead) — the catalog's old
   "Production design / color" row was split so color now stands as its own source.

3. **The grade maps onto the studio in two renderer flavors** (the `0019` audit):
   - a **transform** *grade renderer* — LUT/curve over already-rendered clips, a natural
     fit for the `Cutter` execution plane under the forthcoming common `Renderer`
     protocol (`0006`); the Colorist emits a grade *decision* the way the Editor emits a
     cut;
   - a **sensor/reader** *scope read* — waveform/vectorscope/histogram/parade — that
     backs a color **`validate()`** / broadcast-safe gate (Ch. 2 + Ch. 10), the color
     counterpart of `Sequence.validate()` and the Rose sound-layer validate().

4. **The Colorist's first owned vocabulary is lift / gamma / gain** (Ch. 3) — a
   tonal-range enum/struct, the color analogue of the DP's shot enums (each member
   carrying `phrase` + `intent` like the shot grammar). Ch. 5–6 add the **secondary**
   tier (mask-by-color qualifier + mask-by-region shape → a `Correction.matte` seam),
   Ch. 7 makes a grade **time-varying** over the edit timeline, and Ch. 8 supplies the
   **target palette** (skin/sky/foliage) a Colorist `HeuristicJudgment` aims for.

5. **Logged the `ColorTemperature` two-seat overlap.** It now lives in **both** the
   **Gaffer** (capture / in-camera white balance, `crew/lighting.py`) and the **Colorist**
   (grade / re-balance) — like the POV overlap (Directing Ch. 9 ↔ Taxonomy Ch. 7). Ch. 4
   is where the grade seat's claim is strongest; the reconcile note (give the Colorist a
   distinct grade `WhiteBalance`/`Cast` vocab, or a deliberately shared enum) is recorded
   in the source INDEX and `architecture.md`'s overlap list.

6. **Ch. 9 shot matching is the color analogue of the Editor's continuity check.** Since
   Omni renders each ~10 s shot independently with no shared look, shot-to-shot color
   drift is expected; scene balancing (grade an anchor shot, then a **Colorist/Director
   reconcile** matches the rest across a `Sequence`) is exactly the Colorist's job — the
   grade counterpart of `Sequence.validate()`/continuity.

## Resulting state

- **Seventh grounding source, abridged.** `artifacts/color correction handbook/` now has
  `source/` (verbatim, gitignored) + **10 abridged `reference/` chapters** + a source
  `INDEX.md` (chapter → Colorist code map, provisional leads, overlap flagged).
- **Reconciled** the library docs: `artifacts/INDEX.md` catalog (new row + split the
  design/color cell), `context/architecture.md` (Colorist row cites Van Hurkman + a
  reading-the-map bullet + the `ColorTemperature` overlap in the reconcile list),
  `README.md` (six→seven sources, post-production row, layout tree, license credit).
- **No code changed.** The grounding library is now **complete for the departments
  modelled today plus the Colorist** — the next work is `0019`'s step 2.

## Open threads

- **Formalize the `Renderer` protocol (`0006`, next in the locked sequence)** — a common
  `render(decision) -> (result, ref)` + medium-keyed registry; retrofit
  `Studio`/`ImageStudio`/`SpeechRenderer`/`Cutter` so a role can *hold* its renderer.
- **Build the `Colorist` + grade renderer** onto the protocol, on this grounding — a
  transform renderer (LUT/curve over rendered clips); the Colorist owns the lift/gamma/
  gain primary + HSL/shape secondary grade vocabulary, and reconciles the
  `ColorTemperature` two-seat overlap with the Gaffer.
- **A color `validate()` / broadcast-safe gate** — the scope-read sensor + legalizer as
  a delivery gate (Ch. 2 + Ch. 10), the color sibling of the edit/sound validates.
- Carried from `0019`: the sound-mix renderer (Re-Recording Mixer); a dedicated
  **production-design** source + reference/lookbook backend; wiring the **assemble** phase
  (`Editor` → `Sequence`) and seating the **plan** phase; the crew-engine Production
  binding (`0005`); `PersonaJudgment` (**B**); the reconciliation sweeps.
