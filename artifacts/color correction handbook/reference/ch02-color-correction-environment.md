# Chapter 2 — Setting Up a Color Correction Environment

> Abridged from Alexis Van Hurkman, *Color Correction Handbook*, Ch. 2.
> **Scope:** the colorist's measurement apparatus and viewing conditions — display-referred color management, choosing/calibrating a standards-compliant reference display, video scopes as objective instruments, and the controlled room (surround, lighting, placement) that makes visual evaluation trustworthy.

## Core idea

- **"Before you can cook, you need a kitchen."** Grading is only as valid as the display you judge on and the room you judge in. Color correction is **more exacting** about monitoring than editing/compositing are.
- Video color is **display-referred**, not scene-referred: there is no color profile inside the video file — **fidelity is judged by how the image looks on a calibrated display**. What you can't control (consumer TVs, web) makes controlling your **baseline reference** essential.

## Why calibration matters despite uncontrolled viewers

- Consumers watch on wildly varying, uncalibrated TVs with no embedded profile — you'll never control that.
- But a program passes through **multiple facilities/displays** (colorist → finishing → broadcaster QC). If each display isn't calibrated to a **shared standard**, someone "corrects" against a miscalibrated monitor and **erroneously alters** the master. Consistency up to broadcast keeps the audience as the *last* link in the adjustment chain — free to see the true image if they choose.

## Choosing a display

The reference display is the single most important (and often most expensive) tool. Match the technology to the work.

| Tech | Strengths | Watch-outs |
|------|-----------|------------|
| **LCD** | accurate, stable color; wide sizes; 10-bit common; CCFL/white-LED/RGB-LED backlights | black level tech-dependent; backlight sets gamut & warm-up |
| **Plasma** | deep blacks, great contrast, large & affordable | noisy deepest shadows; **ABL** auto-dims bright frames; frequent recal |
| **OLED** | stunning blacks, huge contrast, self-emissive | expensive, small; hard to match in multi-display suites |
| **Projection (DLP/LCoS)** | theatrical scale; DCI P3 for cinema | needs blackout room, space, cost |

- **Metamerism failure**: two displays that *measure* identical (metamers, per CIE 1931) can *look* different side-by-side because their spectral outputs differ — and narrow-band primaries (OLED, laser) make the mismatch **person-dependent**. Lesson: keep **one "hero" display**; the mismatch mostly vanishes when a display is viewed alone.

### What to demand in a display

- **Standards compliance** — the exact **gamut** and **gamma** for your target: **BT.601** (SD), **BT.709** (HD), **DCI P3** (digital cinema); **BT.2020** is future/unreachable today.
- **Bit depth** — 8/10/12-bit; 10-bit isn't required for *color* accuracy but lets you judge **gradient smoothness** (8-bit panels can show false banding, tempting needless corrections).
- **Color temperature** — the "color of white": **D65 (6500K)** for NA/SA/Europe broadcast, **D93 (9300K)** in parts of Asia, **~6300K** DCI reference, **D55/5400K** film. Consumer sets run cooler/bluer (reads as "brighter").
- **Contrast / deep blacks** — judge by **simultaneous (concurrent) contrast** (peak white & min black in one checkerboard). Muddy blacks tempt over-crushing.
- **Gamma (EOTF)** — **2.4** (BT.1886, HD, 1% surround), **2.6** (blackened cinema), **2.35** (dim surround), **2.2 / sRGB 2.2** (consumer/computer). Gamma must be **matched to surround luminance** (Bartleson–Breneman effect: perceived contrast rises with surround brightness).
- **Setup/pedestal** — **all digital signals sit black at 0** (IRE/mV). Use **7.5 IRE only** for analog NTSC Beta SP; everything digital/HD = **0**.
- **Light output** — reference white ≈ **80–120 cd/m² (nits)** in a light-controlled suite (100 common; 120 for brighter client lighting); **48 cd/m²** for a blackened-theater projector. Higher light output raises apparent saturation/contrast (Hunt/Stevens effect) — so it drives grading decisions.
- **Adjustability, resolution, aspect, interlacing** — the display is an **instrument**: under-scan, mono-only, deliberate mis-adjust (bright/chroma/contrast) to spot-check robustness; native resolution for sharpness; correct pillar/letterbox; visible field-order handling (reversed fields = a real QC bug).
- **Interface**: **HD-SDI** for HD; dual-link/3G for 4:4:4; quad-link/6G for 4K; HDMI for home-theater gear; keep the signal chain the weakest-link-free.

## Calibration

- Standards-compliant ≠ accurate from the factory, and displays **drift**. Three strategies: **factory recalibration**, an **on-site specialist**, or **buy a probe + software** yourself.
- **LUT-based calibration** measures ("characterizes") the display with a **probe** (colorimeter — cheap, fast; or spectroradiometer — accurate, pricey) fed by a **pattern generator**, then generates a **3D LUT** that transforms the signal toward an ideal gamut. Loaded into the display, an **outboard LUT box**, or the grading software.
- **Physics limit**: a LUT can shrink a **larger** gamut to a smaller target but can't make a **small-gamut** display show a larger one. *LUT calibration makes good displays accurate; it does not make poor displays good.*
- LUTs also compose: a **calibration LUT** merged with a **film-emulation LUT** lets you grade *in the context of* a print stock, then disable the sim LUT before final render.

## Video scopes — the objective instruments

The eye is fooled by surround and fatigue; **scopes read the actual signal**, independent of the display.

- **Waveform monitor / parade scope / histogram** are the reference graphs — e.g. absolute-black pixels must sit on the **0 line** of the waveform/parade/histogram; scopes make **setup, clipping, and out-of-range excursions** measurable rather than guessed.
- **Outboard vs. built-in scopes**: software scopes read the *internal digital* image state; **outboard scopes** diagnose the signal **after** it leaves your system, often add higher resolution, freeze-frame overlay/compare, and **gamut checking** for composite/RGB excursions. Recommended to have one.
- **QC logging**: many outboard scopes **auto-log QC violations with the offending timecode** as the program plays — an automated, objective conformance check (see forthcoming Ch. 10, broadcast-safe).
- **Video legalizer**: a hardware clamp/compress on out-of-range luma/chroma at output — the *last* wall of defense, **not** a substitute for grading the signal into range by hand.

## The viewing environment

The room affects perception nearly as much as the display.

- **Surround wall** behind the display: **neutral (achromatic) ~18% gray**, *not* faintly blue/red; fill your field of view; gentle top/bottom falloff (a perfectly even field is not optimal) and a coarse texture reduce eye fatigue. A colored or too-bright/too-dark surround skews your color and contrast judgment.
- **Surround lighting**: **match its luminance to your reference luma/gamma** — e.g. surround ≈ **1–10% of a 100-IRE white** for BT.1886/100-nit HD mastering (many suites run ~1%); brighter (~20%) for living-room-style 2.2 grading. Color temperature = **D65** (or D93 in Asia); **CRI ≥ 90**; beware low-CRI LEDs.
- **Workspace**: block *all* outside light; **indirect** lighting only (no source in your field of view, none reflecting off the panel → **veiling reflections** destroy black/shadow/contrast evaluation). Colorist area ~3–4 ft-L just to see controls; client area 2–10 ft-L on their desk, never spilling on the display or facing wall. A **D65 "white spot"** on the wall re-references the fatigued eye.
- **Neutral, non-reflective furniture/decor**; comfortable seating (you'll sit for hundreds of shots).
- **Display placement**: one **hero display** both colorist and client refer to; ideally behind/above the computer displays to avoid glare; seating ≈ **3.3 × picture height**. **Video suite** (LCD/plasma, subdued light, broadcast) vs. **grading theater** (projector, blackout, DCI P3, theatrical).
- **Control surfaces** (three trackballs = lift/gamma/gain, three rings) let you keep eyes on the display, adjust multiple parameters at once, and spare the wrist — the grade's physical instrument.

## Studio application

*Provisional leads — the Colorist role and grade renderer are not built yet; these tie Ch. 2 to Sequitur's existing seams.*

- **Scopes → a color `validate()` / QC analogue (strongest lead).** Scopes are the *objective signal* that a grade is judged against — black on the 0 line, no out-of-range excursions, auto-logged QC violations. That is the color counterpart of [`Sequence.validate()`](../../../sequitur/edit.py) (which returns human-readable `error:`/`warning:` strings against the edit's rules) and of the Rose sound-layer validate (Producing Great Sound, Ch. 18). A future colorist QC step would read an image and return the same shape — a `list[str]` of measurable violations (clipping, illegal levels, black-level drift) with a frame/timecode.
- **A sensor/reader-flavor renderer that *measures* an image.** Reading scopes is the color instance of the **sensor/reader** renderer flavor already named for the SoundAnalyst (MIR) — it consumes media and emits **measurements**, not new media. This pairs with the transform-flavor grade renderer from Ch. 1: **grade → then measure**. Under the forthcoming `Renderer` protocol (`render(decision) -> (result, ref)`), the measure step's `result` is a report/scope-reading rather than a clip.
- **The legalizer ≈ a validate-and-clamp gate.** The hardware legalizer (last-line broadcast-safe clamp) maps onto a `validate()`-then-optionally-clamp step the Colorist would run before delivery — the color analogue of `Cutter.render` refusing to run while `validate()` has blocking errors. Detailed broadcast-safe rules are grounded in the forthcoming Ch. 10.
- **Standards/target as config, not vocabulary.** BT.709 vs. DCI P3, D65 white point, reference gamma/luminance are the **target the grade renders *to*** — a per-production config/enum the grade renderer and the color-QC both consume, distinct from the creative grade decision itself.
- **Capture-vs-grade overlap to flag (again, precisely).** "Color temperature" appears **twice** and must not be conflated: here it is the **display's white point** (D65/D93 — a *measurement/target* the colorist calibrates and grades against), whereas the **Gaffer** owns `ColorTemperature` as the **capture-time color of the light itself** ([`sequitur/crew/lighting.py`](../../../sequitur/crew/lighting.py): WARM/COOL/MIXED/GOLDEN_HOUR). Same words, different seats — the Colorist's color vocabulary must be kept separate from the Gaffer's, even though both name "temperature."
