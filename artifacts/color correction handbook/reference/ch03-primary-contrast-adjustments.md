# Chapter 3 — Primary Contrast Adjustments

> Abridged from Alexis Van Hurkman, *Color Correction Handbook*, Ch. 3.
> **Scope:** the *luma* half of the primary grade — reading exposure on the **waveform** and **histogram**, then shaping it with the **lift / gamma / gain** (shadows / midtones / highlights) controls; setting the **black point** and **white point**; expanding vs. compressing tonal range; how contrast drives perceived **saturation** and **sharpness**; log normalization; and rescuing under/over-exposure.

## Core idea

Every digital image splits into **luma** (lightness/darkness) and **chroma** (color). This chapter works *only* on luma. The eye processes luminance in a separate ("where") pathway from color — luma carries **depth, motion, spatial organization, and fine detail** — so contrast decisions have outsized perceptual impact. **Grade contrast first, color second:** the lift/gamma/gain controls act on luma ranges, so any later color balance depends on where the tones already sit.

- **Luminance** = perceived light intensity; **luma (Y′)** = luminance after a nonlinear **gamma** power function (the ′ = gamma-corrected). Broadcast gamma standard is **BT.1886 (γ 2.4)**; encode/display apply matching-but-inverse gamma.
- Luma is weighted from RGB ≈ **21% R, 72% G, 7% B** — the eye is most sensitive to green/yellow. So equal-"brightness" pure R/G/B bars read at very different luma heights.
- **Log-encoded** camera/RAW media is flat and low-contrast to preserve **latitude**; it must be **normalized** ("log-to-lin") — itself a contrast operation — before fine grading.

## What contrast is

- **Contrast (contrast ratio)** = the spread between the darkest and lightest values. Wide spread (0% blacks + 100% whites) = high contrast, vivid; narrow, mid-parked spread = low contrast, muddy/subdued.
- Footage is often shot with **deliberately compressed contrast** (blacks up, whites down) to protect highlight/shadow detail for grading. Expanding it is the everyday "wipe the dust off" win.

## Reading contrast on scopes

Judge on a calibrated display in a controlled room; scopes are the **objective guide**. Learn to spot three things: the **black point** (darkest shadow), the **white point** (brightest highlight), and the **average midtone distribution**.

- **Histogram** — pixel count vs. tonality 0–110%. Width = contrast ratio; leftmost = black point, rightmost = white point, fattest bulge ≈ midtones.
- **Waveform Monitor (WFM, luma)** — height = contrast ratio, and it stays spatially correlated to the frame (left↔right), so you see *which* parts sit high/low.
- **Scales:** software = digital **0–100%**; outboard = **IRE** (1 IRE = 1/140 V = 7.14 mV) or **mV** (0–700 mV). **Super-white** 101–110% exists in many camera signals but is **not broadcast-legal** and gets clamped to 100%.
- **0% is absolute black** for all digital signals (the old 7.5 IRE setup is dead). Cameras often record black slightly elevated (~3%) plus noise — even "black" benefits from deepening.

## The contrast controls

- **Lift** (black point) — raises/lowers the darkest values; pins highlights, compresses midtones between the new floor and the fixed ceiling. *Not* "Shadows." Adjust **blacks first** (lift interacts most with the rest).
- **Gamma** (midtones) — redistributes the mids up/down while (ideally) pinning black and white points; a **nonlinear** curve. Midtones are "the steak" — the main subject and time-of-day/mood live here.
- **Gain** (white point) — raises/lowers the brightest values relative to black. *Not* "Highlights."
- **Master Offset / Exposure** — raises/lowers the **whole signal** uniformly (absolute), unlike Lift (relative to a fixed white). Set **Offset first**; everything else rides on it. Useful for parking the black point.
- **Contrast + Pivot** — one control stretches/compresses both ends at once, scaling everything between; **Pivot** sets the brightness the expansion rotates around (low pivot weights the change toward highlights, high pivot toward shadows). Know whether your app **clips or soft-compresses (S-curve)** past the limits.
- These three always **interact** — a big Lift move drags the mids and even the whites. Expect to make compensating counter-moves.

## Curves

- **Luma curve** — x = source tonality, y = adjusted value; the neutral diagonal = no change. Add control points to bend specific tonal zones. Because the endpoints are usually pinned, treat the luma curve as a **very detailed midtones control** (can't push peak white or floor black).
- **S curve** (a point down in the low mids, a point up in the high mids) = localized contrast stretch — denser shadows, glossier highlights, "edgier" look, within a narrow band. A little goes a long way; over-bending "thin" data causes **contouring**.

## Expanding vs. compressing

- **Expand:** lower shadows toward ~0–10%, raise highlights toward ~100%, tune mids to taste. Watch the display — don't crush needed shadow detail (e.g. a dark jacket) or blow real highlight detail. Result = more "punch," definition, apparent sharpness.
- **Gaps in the scopes** after a big stretch are normal — limited data spread over a wider range (worse with 4:2:0/4:1:1 subsampling). The *image* is what matters, not the graph.
- **Compress:** lower gain (mute highlights), gently raise lift (lift blacks off the floor) for dusk/night/low-contrast looks. Perceived brightness is **relative** — keep *some* spread or the image goes flat.
- **Crushing blacks** (piling shadows at 0%) boosts perceived contrast but destroys shadow detail and can cause **macroblocking** under MPEG-2/H.264 delivery. To darken a fill-lit shot, prefer **lowering the mids** over crushing the floor.

## Luma-only vs. RGB processing (contrast ↔ saturation)

- Most primary contrast controls are **RGB (master)** operations: expanding contrast also **raises saturation** (colors intensify) — usually desirable.
- **Y′-only** contrast controls leave measured saturation unchanged (vectorscope flat) but *perceptually* **lower** saturation as you stretch — good for punchier blacks / broadcast fixes without touching color; compensate with a saturation boost if needed.
- Neither is "better"; RGB is the default. Ganged vs. unganged RGB curves behave the same way (ganged = +saturation, unganged/Y′ = starker/desaturated).

## Setting black and white points

- **White level** is a preference/look call. Park **peak highlights** (sun glints, chrome, lamps, sparks — little/no real detail) at/near 100%; keep **average/diffuse highlights** (skin, clouds, cloth) lower, in the mids. High-key → whites near 100; low-key → 60–80 is fine. A conservative **98% self-cap** guards against QC bounces from transient overshoots. **Don't fear clipping detail-free peak highlights.**
- **Legalizing whites:** lowering gain to legalize super-white spikes also darkens mids — compensate by boosting gamma, then re-trim gain/lift. Watch for **luma spikes at high-contrast edges** (white-on-black titles) on an *outboard* WFM.
- **Black level** floor is simply **0%**. Even a few points of Lift-lowering adds "snap." How low depends on the shot — leave lighter shadows for soft/overlit looks.

## Log media and wide latitude

- **Normalize first, fine-tune second.** Normalize log via a **1D LUT** (an inverse of the camera's log encoding — a LUT ≈ a many-point curve) *or* manually with a contrast expansion + S curve, *or* the app's built-in color management/ACES.
- **Order of operations matters:** apply corrections **before** the LUT to reach the raw log data (LUTs clip out-of-bounds data), and **after** the LUT to work on the normalized result.
- **Log Shadow/Midtone/Highlight controls** are calibrated for log's compressed ranges and overlap smoothly **only when applied pre-normalization**; used on normalized media they get too narrow and contour. Their boundaries are movable via **pivot/range/band** params.
- **HDR / wide-latitude RAW** (13–18 stops) can't fully fit a ~5-stop BT.709 display. Three strategies: **compress highlights+shadows** (then curve the mids), **segment with shapes/windows** (grade sky separately from subject), or **soft-clip** unneeded detail. RAW ISO metadata is a non-destructive exposure re-decode.

## Under- and over-exposure

- **Underexposure:** stretching amplifies **noise**, and **chroma subsampling** sets the ceiling — 4:4:4/4:2:2 take aggressive lifts cleanly; 4:1:1/4:2:0 break down fast. Boosting **mids** often beats boosting whites; a low S-curve ("hockey stick") re-densifies shadows and hides noise near black. Data below the camera's noise floor is gone — expect chunky blacks. Denoise (built-in or plug-ins) as needed; the real fix is a **bounce card on set**.
- **Overexposure:** super-white (101–110%) highlight detail is **retrievable** — just lower gain. Fully clipped highlights (all channels maxed) have **no recoverable detail** — lowering gain only greys them. Save detail-bearing highlights (faces, buildings); sacrifice detail-free peaks. Blown windows are an **aesthetic** choice (blow out vs. isolate with a shape/qualifier).

## Contrast and perception

- **Surround effect:** the same gray reads darker against white, lighter against black. You can make shadows *seem* deeper by **raising the highlights** (not lowering blacks) — contrast is entirely relative.
- **Apparent sharpness:** more edge contrast reads as sharper detail (the principle behind sharpen filters) — though you add no real resolution and may cost pixels if you crush.
- **Exhibition:** uncalibrated consumer TVs/projectors and mismatched black setups can wash out or crush your grade — trust your calibrated display but sanity-check on a consumer set.

## Studio application

*(Provisional leads — the Colorist role and the grade renderer are not built yet.)*

- **Lift / gamma / gain is the Colorist's first parameter vocabulary.** It maps cleanly onto the studio's existing pattern: an `Enum`/dataclass of tonal-range adjustments (shadows / midtones / highlights, plus offset, contrast+pivot) is the *color analogue of the DP's shot enums* (cf. the Gaffer's `LightScheme`/`LightQuality` value-objects in [sequitur/crew/lighting.py](sequitur/crew/lighting.py)). Each member can carry a `phrase` + `intent` like the shot vocab, giving the Judgment/heuristic layer something to reason over.
- **The grade renderer is a transform-flavor renderer.** Contrast ops are LUT/curve/level transforms over already-rendered clips — a natural fit for the ffmpeg/MoviePy execution plane in [sequitur/cutter.py](sequitur/cutter.py), and for the forthcoming common `Renderer` protocol (`render(decision) -> (result, ref)`, storyline 0006). The Colorist would hold this renderer and emit a grade *decision* the way the Editor emits a cut.
- **Waveform + histogram are the objective instruments a future QC / `validate()` analogue reads.** "Black point at 0, white point ≤ 100, no super-white spikes" is a machine-checkable legality contract — the color counterpart to [sequitur/edit.py](sequitur/edit.py)'s `Sequence.validate()`. A grade decision could self-report whether it lands legally before render.
- **Normalize-then-grade is an ordered pipeline, not one call.** If the Colorist ever ingests log/RAW, the pre-LUT vs. post-LUT ordering (and shapes/windows for segmentation) implies the grade decision is a *small ordered stack* of transforms, not a single flat parameter set — worth designing the decision object to hold an ordered list.
- **Contrast couples to saturation.** Whatever RGB-space transform the grade renderer applies will move perceived color too; the Colorist's contrast and (Ch. 4) color/saturation vocabularies must be reasoned about **together**, and the contrast pass should run **before** the color pass — mirroring the book's "contrast first" rule.
