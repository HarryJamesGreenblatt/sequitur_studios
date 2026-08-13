# Chapter 5 — HSL Qualification and Hue Curves

> Abridged from Alexis Van Hurkman, *Color Correction Handbook*, Ch. 5.
> **Scope:** the first family of **secondary** (selective) corrections — isolating an object **by colour**. Covers **HSL Qualification** (pulling a chroma/luma key into a matte, refining and softening it, limiting spill) and **hue curves** (hue-vs-hue / hue-vs-sat / hue-vs-luma retargeting). Companion to Ch. 6 (isolation **by region**).

## Primary vs secondary

- A **primary** correction adjusts the **whole image**; a **secondary** correction adjusts **one isolated object or region**, leaving the rest alone. Secondaries are made *after* the primary.
- Don't reach for a secondary for simple problems. First check whether careful **Lift/Gamma/Gain** (primary) does the job — qualifiers waste time on work the tonal controls can do.
- **HSL Qualification = mask-by-colour; Shapes = mask-by-region.** A well-keyed HSL matte follows the subject automatically, so it needs **no tracking or keyframing** — its main advantage over shapes. The two are routinely combined.

## HSL qualification in theory

- You pull a **chroma key** (isolate by a range of colour) or a **luma key** (isolate by a range of lightness). The key produces a **matte** — a grayscale image — that limits *which pixels a correction affects*, not transparency.
- **White = inside** the correction (keyed); **black = outside** (unkeyed). You choose to grade either side.
- Workflow shape: **sample → refine with the H/S/L controls → clean up with blur/edge tools → invert if needed → grade.**

## Viewing the matte while you work

- Judge the key by watching the **matte**, not just the result. Standard views:
  - **High-contrast grayscale matte** — clearest read of white (in) vs black (out) quality; also "solos" the keyed region on the Waveform.
  - **Keyed area in colour over grayscale/flat** — shows *which* details are being included.
  - **False-colour overlay** on the keyed subject over the full-colour image.
  - **Final effect** — the actual correction.
- Always **play the shot** while viewing the matte to catch **buzz/chatter** at edges and in thin areas.

## The individual qualifiers

- **Hue** — a continuous spectrum that wraps seamlessly end-to-end; selects a range of colour.
- **Saturation** — selects a range of colour intensity (0–100%).
- **Luma** — selects a range of lightness (the Y′). A **luma-only key** yields the sharpest edges on compressed media, because luma is always fully sampled while chroma is subsampled.
- Each qualifier can run **alone** (single-component key) or in **combination** for a highly selective key.
- Each has two handle sets:
  - **Range** handles — the hard, white **core** of the key.
  - **Tolerance / softening** handles — a graduated **falloff** around the core. Wider = softer, more inclusive; narrower = harder, more restrictive.
- **Enable/Disable** per qualifier. Control models: **Centered** (3 knobs: move centre, expand range, expand tolerance) vs **Asymmetrical** (4 knobs: low/low-soft, high/high-soft independently).

## Postkey matte utilities

- The matte is just a grayscale image; filter it — but exhaust the qualifiers first, and don't overdo it (aggressive filtering creates worse artefacts than it fixes).
- **Blur / softening / feathering** — smooths edges and kills matte noise; **over-softening spills the correction into a halo**. Some tools blur **inward** ("negative" blur) to feather toward the interior and avoid haloing.
- **Shrink / Erode** — a matte-**choke**: expand to fill small holes, contract to drop spurious pixels. Shrinking alone can blockify edges; follow with a little blur.
- **Matte contrast / curve** — grade the matte itself (Lift/Gamma/Gain or a curve) to **crush fringing** while keeping the strong core. One of the most powerful ways to rescue a marginal key.
- **Limit the key with a shape** — draw a **garbage matte** to exclude unwanted keyed areas elsewhere (wood/sand/skin are the classic collisions). Combining a qualifier **and** a shape preserves only the key **inside** the shape.
- **Invert the key** — swap inside/outside to grade everything *except* the easily-keyed subject (or via an explicit inside/outside setting or an "outside node").

## Optimizing difficult keys

- **Feathering trade-off:** blur softens but overshoots the subject edge (halo risk); widening qualifier **tolerance** hugs the contour better but adds **spill** into the background. Best answer usually **combines a little of each**.
- **Perfect keys are rarely needed** — a subtle grade tolerates a sketchy matte; extreme colour/contrast grades demand a tight, dense one. In all cases, kill buzz/chatter and play it through.
- **Media quality matters most:** 4:4:4 / 4:2:2 key cleanly; 4:1:1 / 4:2:0 give blocky edges (lean on **luma-only keys** and **chroma smoothing** — blurring Cb/Cr — there).
- **Control the pipeline feeding the keyer:** choose to sample the **original** or the **graded** image. Sample the original when the grade is extreme; sample the graded version when the source is flat/low-sat (e.g. raw/RED).
- **Prep the image for keying:** **boost contrast/saturation** before pulling the key to widen the gap between target and background; **pre-blur / noise-reduce** a *keying-only* branch so the final image stays sharp.
- **Secondary before primary:** key on full-detail source *first*, then let a later primary clip/crush — preserves detail you'd otherwise lose.
- **Unusual combos:** **Hue+Sat** for equiluminant shots; **Luma+Sat** to isolate skies from other, less-saturated blues.

## Uses of HSL qualification

- **Isolate & adjust one element** — most commonly to tame an over-saturated distraction, or (via **contrast of extension**) to boost *one* subject's saturation for colour contrast rather than the whole frame.
- **Two exclusive corrections** — key an easy subject, then grade **inside** and **outside** separately (protect a costume colour while restyling the environment).
- **Grade light & dark regions separately** — a **luma-only key** balances a backlit window against an underlit interior; watch matte overlap to avoid haloing.
- **Control shadow contrast** — luma-key the midtone shadows to lift them (change apparent time of day); don't overdo it or the image **solarizes**.
- **Isolate a subject with desaturation** (*Pleasantville*) — key the subject, invert, desaturate the rest.
- **Combine mattes** — a **Key Mixer** merges several optimized keys into one. Compositing **blend modes** apply: **lighten** = union of two mattes; **darken** = intersection (this is exactly how a shape limits a key); an **inverted** matte under darken **carves** a hole.
- **Saturation within a tonal range** — a luma qualifier alone selects a lightness band to raise/lower saturation.
- **Desaturate then selectively re-saturate** — desaturate the image, key off the **original source** colours, paint colour back in (fixes chroma noise; stylized looks).

## Hue curves

- **Hue curves** plot a colour **component against a range of hue** (unlike RGB curves, which plot a channel against **tonality**). Adjustments are smooth with **none of the edge artefacts** of a pulled key.
- Three core curves:
  - **Hue vs Hue** — retarget a hue range to another hue (localized "rainbow shift"); good for subtle skin/foliage/sky nudges and **mixed-lighting fixes** (swing a fluorescent spill toward the scene's daylight).
  - **Hue vs Saturation** — raise/lower saturation of a hue range (the most-used curve); stylize, tame QC-illegal reds, enhance colour contrast.
  - **Hue vs Luma** — lighten/darken a hue range; **tricky** — it drives the data-rich luma against data-poor chroma, so it artefacts on 4:2:0/4:2:2 and only truly behaves on 4:4:4.
- Optional extras: **Sat vs Luma** and **Sat vs Sat** (a **Vibrance**-style lift of the least-saturated areas).
- **Lock off** hues you don't want to move by planting neutral control points at the borders of the target range.
- Selective saturation ≠ a colour cast: emphasizing a hue's saturation leaves neutrals untouched (film-stock-like looks).

## Related tools

- **Vectors / Kilovector** — six customizable hue "pots" (Centre + Width) shifting hue/sat/lightness of a wedge; ancestor of the hue curve. Variants: Six Vector, Revolver, **Hue Shift** sliders.
- **Advanced keyers** — RGB keyers; **3D-cube keyers** (Baselight **Dkey** samples colour *volumes*; Autodesk **Diamond**/Master keyer) for isolations HSL can't reach.

## Studio application

Provisional leads for a future **Colorist** role and **grade renderer** (neither built yet):

- **Two-tier grade vocabulary.** Ch. 3–4 give the **primary** (whole-image) grade; Ch. 5–6 give the **secondary** (masked) grade. Model the Colorist's output as exactly this split: a primary correction plus zero-or-more secondaries. **HSL Qualification is the mask-by-colour flavour**; Ch. 6 Shapes is the **mask-by-region** flavour. Both are *the same secondary tier with different matte sources* — a clean provisional class shape (`Correction` with a `matte: Qualifier | Shape | None`).
- **The matte is a first-class intermediate.** A key/qualifier produces a **grayscale matte** that limits an op. That grayscale-mask-limits-a-transform pattern already exists in the studio: the **Editor / edit layer** compositing masks and **`ImageStudio` region conditioning** ([sequitur/image.py](../../../sequitur/image.py)). A Colorist `Matte` type could be produced grade-side and consumed the same way — worth unifying rather than inventing a parallel mask concept.
- **A grade is an ordered graph, not one op.** "Secondary before primary," "boost-then-key," "combine mattes with blend modes," inside/outside splits — these make the grade an **ordered list of corrections** (echoing how an edit `Sequence` is an ordered list of clips, [sequitur/edit.py](../../../sequitur/edit.py)). Provisional lead: the Colorist owns a small correction stack the **grade renderer** executes as a transform chain.
- **Grade renderer = transform-flavor over rendered clips.** LUT/curve/matte passes belong on the existing execution plane — the **`Cutter`** (MoviePy, [sequitur/cutter.py](../../../sequitur/cutter.py)) — applied over already-rendered footage via ffmpeg/MoviePy, not at image-generation time.
- **Capture vs grade split.** The **Gaffer** owns capture-time **`ColorTemperature`** ([sequitur/crew/lighting.py](../../../sequitur/crew/lighting.py)); hue-curve mixed-lighting fixes are the **grade-time** answer to the same problem. Keep the vocab on opposite sides of the seam: Gaffer sets the light, Colorist corrects it after the fact.
- **Tracking is out of scope here.** HSL mattes deliberately need no tracking/keyframing — they follow the subject by colour. That property is why the color layer's *animation* concern (Ch. 7) and shape **tracking** (Ch. 6) can be deferred: the mask-by-colour path is the simplest first target for a Colorist prototype.
