# Color Correction Handbook — grounding index

Alexis Van Hurkman, *Color Correction Handbook: Professional Techniques for Video
and Cinema* (Peachpit Press). This is the studio's **color-grading** grounding — the
craft of shaping an image's contrast and color *after* it is shot (or, here,
rendered): primary correction, isolated secondaries, memory-color targets, shot
matching, and broadcast-safe delivery. It sits in the **post / finishing** phase,
after the edit is locked, and grounds a future **Colorist** role plus a
**grade renderer** (a *transform-flavor* backend — LUT/curve over already-rendered
clips, the color counterpart to the `Cutter` execution plane).

> **Abridged (10 ch) — 0020.** The verbatim `source/` (10 chapters, converted to
> Markdown before shipping) has been abridged into 10 session-ready
> [`reference/`](reference/) chapters, each ending in a **Studio application**
> section. The **Colorist** role and the grade renderer do **not** exist in code yet,
> so every mapping below is a **provisional lead** — the color analogue of the shot
> grammar, waiting for the role that will own it.

## Folder layout

- [`source/`](source/) — verbatim Markdown, the **ground truth** (shipped already
  converted; no `.docx` originals). *(gitignored)*
- [`reference/`](reference/) — abridged, session-ready references (10 chapters). *(ships)*

## Chapter → (planned) role map

All chapters ground a future **Colorist** (post / finishing phase). The bold chapters
are the ones that most directly become code — the grade parameter vocabulary, the
secondary-correction masks, the target palette, the shot-match reconcile, and the QC
gate.

| Ch | Reference | Grounds |
|----|-----------|---------|
| 1 | [Color Correction Workflows](reference/ch01-color-correction-workflows.md) | the **grade as the finishing phase** downstream of the locked edit `Sequence` ([`edit.py`](../../sequitur/edit.py)); the NLE↔grade round-trip; a `grade` seat the Colorist works after the `Editor` |
| 2 | [Setting Up a Color Correction Environment](reference/ch02-color-correction-environment.md) | the **scopes** (waveform / vectorscope / histogram / RGB parade) as the objective signal a future **QC / `validate()` analogue** reads — a *sensor/reader*-flavor renderer that measures an image (the color counterpart to `SoundAnalyst` MIR); calibrated display + viewing room |
| 3 | [**Primary Contrast Adjustments**](reference/ch03-primary-contrast-adjustments.md) | **lift / gamma / gain** = the Colorist's **first parameter vocabulary** (a tonal-range enum/struct, the color analogue of the DP's shot enums); the waveform → the legal-signal `validate()` contract; contrast pass **before** color |
| 4 | [**Primary Color Adjustments**](reference/ch04-primary-color-adjustments.md) | color-balance-by-tonal-range + saturation; the **vectorscope** flesh-tone line; ⚠ the **`ColorTemperature` capture-vs-grade overlap** — the `Gaffer` sets white balance in-camera ([`crew/lighting.py`](../../sequitur/crew/lighting.py)), the Colorist re-balances in the grade |
| 5 | [HSL Qualification and Hue Curves](reference/ch05-hsl-qualification-and-hue-curves.md) | the **mask-by-color** secondary — a chroma/luma key → matte limiting a correction to a color range; the grayscale matte already has analogues in `ImageStudio` region conditioning ([`image.py`](../../sequitur/image.py)) |
| 6 | [Shapes](reference/ch06-shapes.md) | the **mask-by-region** secondary — geometric vignettes/windows completing the two-tier grade vocab (primary vs. secondary); **shape tracking** is the animation overlap → reuse the edit-layer timeline ([`edit.py`](../../sequitur/edit.py)) |
| 7 | [Animating Grades](reference/ch07-animating-grades.md) | a **time-varying grade over the edit timeline** — keyframed grade parameters across a `Clip`'s duration; static-vs-dynamic key ≈ the `Editor`'s cut-vs-dissolve `Transition` |
| 8 | [Memory Colors](reference/ch08-memory-colors.md) | the **target palette** — skin / sky / foliage as the reference colors a grade heuristic aims for (the color analogue of the DP's compositional defaults); feeds a Colorist `HeuristicJudgment`; overlaps the open **Production Designer** palette/lookbook seat |
| 9 | [**Shot Matching and Scene Balancing**](reference/ch09-shot-matching-and-scene-balancing.md) | **color continuity across the `Sequence`** — the color analogue of the `Editor`'s "can these shots cut together?"; grade an anchor shot, then a **Colorist/Director reconcile** matches the rest (Omni renders each shot with no shared look) |
| 10 | [**Quality Control and Broadcast Safe**](reference/ch10-quality-control-and-broadcast-safe.md) | the **legal-signal `validate()` delivery gate** — reads scopes, clamps illegal levels; the color counterpart to `Sequence.validate()` and the Rose sound-layer validate(); the legalizer is the **last** transform the grade renderer applies |

## Scope note

This source grounds **grading only** — primary (contrast + color) and secondary
(HSL/shape) correction, hue curves, memory-color targets, shot matching, animated
grades, and broadcast-safe QC. It deliberately does **not** cover **production design**
(set/costume/palette *concepts*), which stays a separate open cell in the architecture
(Directing Ch. 23 is its first lead). It closes the color-grading gap identified in
[`storyline/0019`](../../context/storyline/0019-readiness-renderer-audit-color-gap.md):
before this source, color was only borrowed — the `Gaffer`'s capture-time
`ColorTemperature` (Grammar of the Shot Ch. 4) plus a paragraph of Directing Ch. 36.

**The overlap to reconcile when the Colorist is encoded:** `ColorTemperature` will
live in **two** seats — the **Gaffer** (capture / in-camera white balance) and the
**Colorist** (grade / re-balance), exactly like the POV overlap (Directing Ch. 9 ↔
Taxonomy Ch. 7). Chapter 4 is where the grade seat's claim on it is strongest; give
the Colorist a distinct grade `WhiteBalance`/`Cast` vocabulary (or a deliberately
shared enum) rather than letting the two seats collide silently.

The handbook also anticipates the studio's **renderer flavors** cleanly: the grade
itself is a **transform** renderer (LUT/curve over rendered clips, the `Cutter`
plane under the forthcoming common `Renderer` protocol — [`storyline/0006`](../../context/storyline/0006-renderer-seam-and-image-backend.md)),
while the **scopes** are a **sensor/reader** renderer that measures an image and feeds
the Colorist's judgment and a delivery-time QC gate.
