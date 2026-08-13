# Chapter 10 — Quality Control and Broadcast Safe

> Abridged from Alexis Van Hurkman, *Color Correction Handbook*, Ch. 10.
> **Scope:** Keeping the signal **legal** — luma/chroma/RGB/composite limits, the numeric encoding ranges, what causes illegal levels, and how to legalize gracefully (clippers, secondaries, curves, soft-clip, gamut scopes, legalizing LUTs). The final legality gate before delivery. This grounds a broadcast-safe *validate()* / legalizer at the studio's delivery seam.

## Core idea

A signal is **broadcast safe** when measured **luma and chroma** fall between **reference black** and **reference white**. Cameras, NLEs, and consumer gear will happily record and preserve **super-white** and hyper-saturated color, but broadcasters **clip and reject** them in QC — so legalizing is the mandatory last gate. Even for web/non-broadcast delivery, staying legal guarantees **predictable** appearance across the wildly varied display/menu landscape. Always **get the specific broadcaster's technical requirements first**.

## Numeric encoding (10-bit Y′CbCr the reference)

- **10-bit:** total 0–1023; **luma 64–940**; super-white (headroom) 941–1019; footroom (blacker-than-black) 4–63; **Cb/Cr 64–960**; 0–3 & 1020–1023 reserved for sync.
- **8-bit:** luma 16–235; super-white 236–254; footroom 1–15; Cb/Cr 16–240; 0 & 255 reserved.
- **RGB** has no analog legacy → full range (8-bit 0–255, white = 255,255,255). RGB source rarely super-whites since 255 usually maps to 100%.
- 12-bit data and 32-bit float (0–1, super-white as fractions >1) are for *processing*, not signal analysis. **Film output** (DPX/Cineon): **Dmin 96 / Dmax 685** (10-bit) — 0%→96, 100%→685; confirm with the lab.

## Reference white / black

- **Reference white** = the brightest legal luma: **940** (10-bit) / **100%** / 100 IRE / 700 mV. Measure on a **Waveform set to LOW PASS (LP)** (luma only) or a YRGB parade. Limit every clip's white here — the network clips super-white anyway.
- **Reference white vs diffuse white**: reserve reference white for **speculars, sources, "sparkly" highlights**; **diffuse white** (bounce card / soft cloud, ~10% lower) is ordinary bright. Keeping them distinct preserves highlight contrast.
- **Reference black** = darkest legal: **64** / **0%** / 0 IRE. Footroom/undershoots trigger QC and get clipped. **Setup (7.5 IRE pedestal)** was analog NTSC-only and is **dead in digital** — black sits at 0. But **objectionable black *clipping*** is *also* a QC fail (8-bit compression → **macroblocking** in crushed shadows).
- **Titles**: cap peak luminance lower — many require **≤90 IRE** (RGB 224,224,224) or **≤93%** (235,235,235). High-contrast text edges spike on RGB→Y′CbCr encode even when the fill looks fine.

## Chroma limits

- **Peak chroma** (transient spikes only) **≤110%/IRE** (785 mV); **average chroma ≤100%** (700 mV). Measure on **vectorscope**, **Waveform set to FLAT (FLT)** (chroma composited over luma — thickness = saturation at that tonal height), and **gamut scopes**.
- Illegal chroma comes from: **a hot vectorscope excursion**; **an RGB/parade channel** over 100% or under 0%; or the **composite** (luma+chroma) exceeding limits. Predictable triggers:
  - certain hues — **reds/blues** tend to undershoot (<0), **yellows/deep blues** overshoot (>100);
  - **high luma + high saturation together** (colored bright skies, lighting highlights above ~85–90%);
  - **saturation in near-black regions** (black is *supposed* to be desaturated) — still illegal even though a display would clip it.
- **RGB gamut**: each channel 0–100% is the strict PBS rule; **EBU R103** tolerates −5% to +105% (luma −1% to 103%). Watch the **RGB parade**; hot YRGB on legacy formats causes cross-luminance/audio buzz.

## Six structured steps to legalize

1. **Turn on the clipper / soft-clip** as a safety margin (prefer grading *with* it on to see its effect).
2. **Legalize white per clip** — Gain/Highlights + Lift/Shadows, watching Waveform + Histogram. Luma excursions are the *significant* QC error; use the most conservative standard you'll submit to.
3. **Grade color**, watching the **vectorscope** so saturation stays in bounds — you needn't desaturate everything.
4. **Tame spiking hues** with a **secondary / hue-vs-sat curve** (reds, magentas, blues, yellows offend most).
5. **Waveform FLAT / gamut scope** → **desaturate hot highlights and shadows** without touching legal midtones (Shadows/Highlights sat, HSL luma-key, or Sat-vs-Luma curve).
6. **Final catch** — apply the NLE's broadcast-safe filter or an inline **hardware legalizer** to sweep stray pixels the clipper missed (no clipper is perfect). **The legalizer must be the *last* op in the pipeline.**

## Fixing oversaturation (techniques)

- **Turn overall saturation down** — obvious, fast, sometimes enough.
- **Secondary (HSL) to isolate one offending hue** — keeps the rest of the image's color intact; far more image detail than a blanket auto-clipper (which flattens weave/texture).
- **Key all bright + saturated values** — turn the **Hue qualifier off**, isolate via **Saturation + Luma** only (police strobes, neon, concert lights).
- **Hue-vs-Sat curve** — fast, soft; but its gentle falloff can drain neighbors (desaturating red also hits skin) — use HSL when a hard boundary is needed.

## Highlight / shadow oversaturation

- **Waveform FLAT (FLT) reveals what the vectorscope hides** — hot skin highlights ("golden glow") can read legal on the vectorscope yet spike above 100% in FLAT.
- **Lower the highlights to preserve saturation** — trading a few % of lightness keeps (even gains) highlight color that a legalizer would clip.
- **Highlights/Shadows saturation controls** or an **HSL luma-key** to desaturate a tonal band; **be gentle in shadows** (don't drain richness or skin). A **Sat-vs-Luma curve** fixes both ends in one move.

## RGB legality (parade)

- Watch R/G/B waveforms crossing 0% or 100%. Fixes: **channel curve control points** rolled off at the top (**knee / soft clip**); **neutralize casts** in the highlights (pure white) and shadows (pure black); **lower highlights**; **desaturate** the extremes.
- **Soft clip** (e.g. Resolve Low/High Soft) compresses the top/bottom of a hard grade to **retrieve detail** and give a **halated glow** instead of an aliased clip — not a full legalizer (does nothing for gamut).
- **Scope signal filtering** — Y′CbCr→RGB math throws tiny out-of-bounds transients that trip **false-alarm** scope warnings; EBU R103 / Tektronix specify low-pass measurement filters (IEEE-205).

## Gamut scopes & QC ownership

- Specialized displays: **Tektronix Diamond** (RGB gamut; black = center, casts veer L/R), **Arrowhead** (composite luma×chroma — height = tonality, right edge = chroma limit), **Spearhead** (LSV); **Harris Gamut Iris** (hue by angle, legal band between inner/outer rings).
- **QC violations the colorist owns**: white/video level, black level, chroma level, excessive shadow/highlight clipping, image clarity. Format-borne (dropouts, compression artifacts, aliasing, bad edits) and shoot-borne (focus, white balance, moiré) are separate.
- Facilities run **incoming + outgoing QC**; modern scopes do an **automatic QC pass**, logging every violation with **timecode**. You then walk the list and fix.
- Apply broadcast-safe scene-wide via **track grade / adjustment layer / stretched strip**, or **legalizing LUTs** (Full→Legal / Clip / Soft-Clip). Choose title/graphic colors carefully up front — muted primaries; use image-editor "video safe" filters.
- **HDR future**: OLED/laser + HDR question the wisdom of clipping; full-range 4–1019 would give highlight headroom and shadow footroom — but *today* the legal-world guidelines stand.

## Studio application

Provisional leads — the **Colorist** role and the **grade renderer** are not built yet.

- **Ch. 10 is the studio's legal-signal `validate()` delivery gate.** It's the delivery-time check that **reads scopes and clamps illegal levels** — the direct color analogue of the edit-layer `Sequence.validate()` ([sequitur/edit.py](../../../sequitur/edit.py)) and the Rose sound-layer `validate()` (Producing Great Sound Ch. 18): a **QC step before ship**, not a creative pass.
- **Strongest lead — a broadcast-safe `validate()`/legalizer is the last transform the grade renderer applies.** Model it as a delivery gate on the `Cutter` execution plane ([sequitur/cutter.py](../../../sequitur/cutter.py)): after all per-clip grades, run one legalizing pass (ffmpeg limiter / a legal-range LUT) — honoring the rule that **the legalizer is the *last* op in the pipeline**.
- **Backed by a sensor/reader-flavor scope read.** A scope reader measures the concrete constants (**luma 64–940**, **chroma ≤110% peak / ≤100% avg**, RGB 0–100%) and returns a **violations list with timecodes** — exactly the automatic-QC-log shape a `HeuristicJudgment` can consume. The **six-step legalize** is the ordered checklist that pass runs; measure → clamp.
- **Two-tier like the edit gate:** a fast deterministic legalizer catches stray pixels (the clipper safety net), while the grade renderer's manual/heuristic pass preserves detail (lower highlights to keep saturation, desaturate only hot extremes) rather than blanket-clipping — the "manual beats auto-clipper" lesson.
- **Downstream of both color seats.** QC sits *after* Gaffer capture-time `ColorTemperature` and the future Colorist's grade-time match (Ch. 9) — the delivery gate that guarantees whatever those two decided still ships **legal**.
