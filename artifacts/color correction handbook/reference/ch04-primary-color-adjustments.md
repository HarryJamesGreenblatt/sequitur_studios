# Chapter 4 — Primary Color Adjustments

> Abridged from Alexis Van Hurkman, *Color Correction Handbook*, Ch. 4.
> **Scope:** the *chroma* half of the primary grade — **color temperature** and neutralizing casts; **hue** and **saturation**; additive/**complementary** color and opponent vision; reading color on the **vectorscope**, **RGB parade scope**, and RGB histogram; balancing the three tonal ranges with **color balance controls** (lift/gamma/gain wheels, offset/printer-points, five/nine-way, CDL); **RGB curves**; warm/cool looks and the magenta caution; and **saturation** / "colorfulness."

## Core idea

Color rides the **chroma** component and can be adjusted largely independently of luma. Color speeds object recognition and memory and carries strong emotional signifiers (warm = energy/romance; cool = calm/discomfort). Primary color work doesn't repaint objects — it **shifts the overall color of the light** to set mood, time of day, health of faces, and weather. As with contrast: **fix contrast first, then color** (color-balance zones are luma-defined).

## Color temperature

- Every scene's light has a **color temperature** (Kelvin) set by its **illuminant**. Hotter emitter = **bluer**; cooler = **redder** (black-body model). The 1600K→10000K gradient tracks sunrise→noon sun.
- **D65 (6500K)** = the noon-daylight / broadcast-white / grading-suite-ambient standard (memorize it). D93 (9300K, bluer) is standard in China/Japan/Korea.
- **Spectrally varied sources** break the simple scale: **fluorescent** (green/indigo spikes → green cast), **sodium vapor** (harsh orange, near-monochromatic), **mercury/metal-halide** (off-red / magenta / blue-green). Strong-red sources still let you recover plausible **skin tone** even when other colors can't be saved.
- Correcting or *introducing* a cast = manipulating the light's color temperature. A cast can be a fault (wrong white balance) **or** a deliberate cue (magic hour, candlelight).

## Chroma: hue and saturation

- **Hue** = the wavelength / "which color" — an **angle** around the color wheel.
- **Saturation** = intensity/vividness — **distance from center** (0% = desaturated gray at center, 100% at the rim).
- **Additive RGB:** R+G+B primaries; any two at 100% = a **secondary** (R+G=yellow, G+B=cyan, B+R=magenta); all three equal = **neutral gray/white** at any level. (Film negative is the **subtractive** complement: cyan/magenta/yellow dye layers.)
- **Equal RGB = neutral** is the key diagnostic: on a parade scope, a feature that *should* be gray/white/black but shows **unequal** R/G/B channels has a **cast**.

## Complementary color and opponent vision

- **Complementary colors** sit opposite on the wheel and **cancel to desaturation** when combined; the cancelling effect falls off as hues drift from exactly opposite. This is the engine of every color-balance correction: **push toward the complement of the cast to neutralize it.**
- Vision is **color-opponent** (L/M/S cones compared, not read absolutely): Luma = L+M+S, Red–Green, Yellow–Blue. Byproducts: complementary cancellation, and **simultaneous contrast** (a gray patch takes on the *complement* of its surround). We judge color **relative** to surroundings — which is why an orange stays "orange" under any light.

## Reading color on scopes

- **Vectorscope** — hue = angle, saturation = distance from center. **Off-center graph on a shot that should have neutrals = a cast.** Small graph = low saturation; long arms toward targets = high saturation of those hues; the graticule's R/G/B/Yl/Cy/Mg targets = the color-bar hues.
- **RGB parade scope** — separate R/G/B waveforms, spatially correlated to the frame. **Highlights (top) and shadows (bottom) should nearly align** (neutral extremes); a raised/lowered channel at top/mid/bottom pinpoints *which* channel and *which tonal zone* is at fault. Zoom in to align blacks precisely.
- **RGB overlay** — same data superimposed; where channels align the trace goes **white** (keep scope colors on). **RGB histograms** show per-channel strength per tonal zone but can't localize to a feature.

## Color balance controls

- **Three-way wheels (Lift / Gamma / Gain)** rebalance color per luma zone. Dragging a wheel toward a hue **boosts one channel and lowers the others** (or raises two, lowers one) — you can never raise all three (that's just Offset/brightness). Zones **overlap broadly and smoothly**, so corrections interact — often you make an **opposing move on an adjacent wheel** (e.g. add blue to gain, pull gamma toward yellow) to confine a correction. Overlap width = much of the "feel" difference between apps.
- **Offset / printer points** rebalance the **entire** channel uniformly (a linear add) — fast for a cast running shadows-through-highlights, and often more **natural** than separate zone moves. Printer points echo film color-timing (fractions of an f-stop).
- **Five-way / nine-way** controls subdivide the tonal zones for finer targeting (a control-surface alternative to curves).
- **ASC CDL** standardizes primary grades as **Slope / Offset / Power (SOP)** (+ SAT) for cross-app exchange: `out = (in × Slope + Offset)^Power`. Deliberately limited to primaries — no curves, qualifiers, or secondaries.
- **Automatic balancing** (auto button, or eyedropper on a known white/gray/black) gives a fast neutral starting point, but **manual balancing** is the flexible default — and the eye is the final judge over the numbers. Truly neutral grays are the hardest reference to find (a wrong pick introduces a *new* cast).

## Neutralizing a cast (workflow)

1. **Legalize contrast first** (WFM 0–100%).
2. **Vectorscope** confirms the cast direction (whole graph shoved toward one hue).
3. **Parade scope** locates the tonal zone (top/mid/bottom inequality) and the guilty channel.
4. Pick the matching wheel and push **toward the complement** (e.g. mid-orange cast → gamma toward cyan/blue). Balance the channel bottoms/mids/tops to align.
5. Expect a compensating **opposite move** on an adjacent zone (fixing mids often contaminates shadows).
6. Neutralizing usually **drops saturation** (all channels lowered) — finish with a **saturation boost**. Use the "disable grade" toggle for honest before/after.

## Creative casts, warm/cool, magenta caution

- **Deliberate casts** cue time/place/mood. Golden-hour: push **gain toward orange**, counter **gamma toward cyan/blue** so faces don't over-tan. Cool/clinical: gain toward blue, counter mids toward orange. Fluorescent unease: a little **green** in gain, counter with **magenta** in mids.
- **Avoid magenta** almost always (no natural magenta illuminant; it reads as unpleasant). The trap: over-correcting a green fluorescent cast tips faces into magenta.
- Keep **shadows neutral** even inside a strong cast — neutral shadows preserve contrast against the colored midtones/highlights.

## Log color grading

- Mirrors Ch. 3's log order: **normalize (LUT/curve) as a later op**, and put color moves in the right place. Start log color with a simple **Offset** balance (linear, all-channel — the "color-timer-cinematic" foundation): correct one known feature (skin, sky, foliage) and the rest tends to fall in line.
- When Offset **contaminates** highlights/shadows, use the log **Shadow/Midtone/Highlight** color-balance controls (calibrated to log ranges, movable **pivot/range/band**) for narrow fixes — applied **pre-normalization**. On normalized media these get very narrow → good for **stylized** insertion into a tight tonal band.
- **Color-temperature sliders** (SpeedGrade/RAW) lock hue to the orange↔blue (Temp) and green↔magenta (Magenta) axes — a convenience, nothing you can't do with wheels.

## RGB curves

- Curves adjust **one channel individually** (vs. wheels' simultaneous rebalance) — more specificity, at the cost of sometimes needing two/three curves for what one wheel does. Endpoints are pinned (protect neutral black/white); interior points target tonal zones.
- The **parade scope maps directly to the three curves** — an elevated red waveform → a red-curve point pulled down at that height. Great for large, tonally-specific casts.
- **DaVinci Lum Mix:** YRGB processing raises the other two channels when you lower one (preserving luma); `Lum Mix 0` decouples them.

## Saturation

- Master **saturation** raises/lowers vividness overall. Analyze it with the **WFM set to FLAT (FLT)** (chroma amplitude vs. luma — thickness = saturation, per tonal zone) and the vectorscope (per hue).
- **Targeted saturation** (highlights >~75%, shadows <~25%, with soft falloff; or a **luma-vs-saturation curve**): desaturate shadows for clean deep blacks + apparent contrast, desaturate off-color highlights to white, boost mids without gaudying the whole frame, and **legalize** chroma excursions.
- **Enrich without cheapening:** don't just crank the master — pull down **shadow** saturation while boosting mids. Excess saturation is more successful in **darker** images (lower-brightness colors read richer); over-saturation risks bleed, ringing, and illegality.

## Colorfulness (perception ≠ measured saturation)

- **Colorfulness** (perceived hue strength) diverges from measured saturation. Drivers: **brightness** (**Hunt effect** — brighter = more colorful; higher display peak-white looks more colorful), **contrast** (RGB contrast expansion raises saturation; Y′-only expansion *lowers* perceived colorfulness — why clients conflate "bright" and "saturated"), **size** (bigger feature / bigger display = more colorful for identical saturation), and **color contrast / contrast of hue** (a wider *range* of hues reads as more colorful).

## Studio application

*(Provisional leads — the Colorist role and the grade renderer are not built yet.)*

- **⚠ Capture-vs-grade `ColorTemperature` overlap — the strongest seam to flag.** The **Gaffer already owns a `ColorTemperature` enum** (WARM/NEUTRAL/COOL/MIXED/GOLDEN_HOUR) as a **capture-time, in-camera white-balance** vocabulary ([sequitur/crew/lighting.py](sequitur/crew/lighting.py), Grammar of the Shot Ch. 4). This chapter defines the *other half*: the **Colorist re-balances color temperature in the grade** (post). Both roles speak "warm/cool" but at different pipeline stages — the DP *sets* white balance under the lights; the Colorist *corrects or re-casts* it afterward. When the Colorist lands, decide deliberately: reuse/rename the shared enum, or give the Colorist a distinct **grade** vocabulary (e.g. a `Cast`/`WhiteBalance` value-object) so a Gaffer `GOLDEN_HOUR` capture note and a Colorist "warm the highlights" grade note don't silently collide. This is the clearest place the capture layer and the grade layer touch the same concept.
- **The Colorist's color vocabulary parallels the DP's shot enums.** Color balance (per-zone hue push), saturation, and cast direction can be value-objects with `phrase` + `intent` like [sequitur/crew/lighting.py](sequitur/crew/lighting.py)'s `LightScheme`/`ColorTemperature`, sitting alongside the Ch. 3 lift/gamma/gain contrast vocabulary. Contrast + color together form the full grade decision.
- **Neutralization is complement math the Judgment layer can reason about.** "Cast toward *H* → push toward complement of *H*" is a deterministic rule; a future Colorist heuristic could pick the balance direction from a detected/target cast rather than hard-coding it.
- **Vectorscope + parade scope are the color side of the QC / `validate()` analogue.** "Neutrals centered on the vectorscope, RGB extremes aligned on parade, chroma within gamut" is machine-checkable — the color counterpart to [sequitur/edit.py](sequitur/edit.py)'s `Sequence.validate()`, and a natural QC gate before the grade renderer commits.
- **Grade renderer = transform-flavor over the Cutter plane.** Color balance, RGB curves, and saturation are LUT/curve/matrix transforms over rendered clips — same ffmpeg/MoviePy execution plane as [sequitur/cutter.py](sequitur/cutter.py), held behind the forthcoming `Renderer` protocol (storyline 0006). Order matters: run the **contrast pass before the color pass**, and (if log) corrections **pre- and post-normalization** — so the grade decision is an *ordered stack* of transforms, not a flat blob.
