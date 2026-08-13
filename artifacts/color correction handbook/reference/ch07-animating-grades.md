# Chapter 7 — Animating Grades

> Abridged from Alexis Van Hurkman, *Color Correction Handbook*, Ch. 7.
> **Scope:** Making a grade change *over time* with keyframes (dynamics) — repairing exposure/hue drift inside a take, wiping a correction on with a tracked shape, animating lighting or a creative saturation bloom, and dissolving between two different grades. A grade that varies across a clip's duration.

## The keyframing model

- **Keyframes (a.k.a. dynamics)** let a correction vary across the length of a clip — the same idea as compositing/NLE animation, but grading UIs are built for **speed over features** (few controls, control-surface-friendly).
- **Two keyframe types.** *Static / hold* keyframes make an **abrupt one-frame change** (used to re-grade sub-shots of a "baked master" where there's no real cut). *Dynamic / dissolve* keyframes make a **gradual interpolated transition** from one keyed state to the next.
- **Interpolation** of a dynamic transition can be **constant**, **linear**, **eased / S-curve**, or **smooth** (with over/undershoot). The **distance between two keyframes sets the duration** of the animated change.
- **Scope** runs from **correction-wide** (one keyframe track animates every parameter of a node at once — fast, coarse) to **parameter-level** (a separate track per parameter — precise, slower). Animating a **shape independently of the colour** is the important special case (see wipes).
- Entry modes across apps: **place-and-adjust**; **After-Effects-style** (arm a parameter, then every change adds a key); **fully-auto** (every change spawns keys — remember to disable it). **Some parameters can't be keyframed** (often curves, sometimes HSL qualifiers) — a real limit; check the docs.
- **Golden rule:** build the animated fix on a **separate correction / node / layer** from the base grade, so you can reset it without disturbing the underlying look — and re-grade the base later without rippling every keyframe.

## Correcting exposure drift

- The most common animated fix: an **auto-exposure / auto-knee / iris / cloud-over-sun** brightness shift *in the middle of a take* — often the best-performed take has the worst exposure change.
- **Method:** play through to find the shift's **start and end frames**. Set an **unaltered keyframe** at the frame where the shot is "normal", grab that frame as a **still**, then keyframe the frame of **maximum deviation** and correct exposure (and saturation, if contrast moved it) to **match the still** via split-screen.
- Judge timing on the **Waveform Monitor** — its top contour tracks luma changes too subtle to see by eye. You rarely fix it *perfectly*; the goal is to make the shift **unnoticeable on a casual viewing**.

## Correcting hue / colour-temperature shifts

- Cause: **auto-white-balance** re-triggering mid-shot, or a manual-WB camera **panning between two illuminants** (exterior→interior) — a neutral→orange (tungsten) or neutral→blue (daylight) swing right in the middle of a shot.
- **Keyframe the grade** (easiest): on a second correction, keyframe a colour-balance move across the shift's frame range to compensate. The most seamless transition isn't always the same length as the shift — sneak it **slower** in darkness, **faster** under a whip-pan; only playback tells you which reads best.
- **Mixed-light residue:** compensating for the interior can turn a window's exterior light vivid blue — isolate that pool with a **well-softened HSL Qualifier** and rebalance it (isolating a differently-lit window pool is a reusable move).
- **Wipe the correction with a tracked shape** when a *hard moving border* can't be dissolved seamlessly: grade the match, then animate a **shape / Power Window** whose edge rides the moving border (car-window frame, wall corner), keeping the leading edge **hidden in shadow** and feathered. Keyframe the **shape independently of the colour** so later colour tweaks don't force re-animating the wipe.

## Animating lighting & creative looks

- **Practical light on/off:** a flicked switch reads weakly on screen. Lock an unaltered keyframe at the last "normal" frame, then a second keyframe ~2–3 frames later where you compress/lower contrast and swing highlights from tungsten-orange toward cool moonlight — tight spacing = near-instant change.
- **Fake time-of-day (sunset) shift:** keyframe highlights (via HSL) from neutral toward golden/orange, and *separately* lower master gamma over the same span; optionally cool the shadows inversely as the highlights warm for a richer light/shadow interplay.
- **Creative saturation bloom** (e.g. *A Single Man*): open a shot muted and cool, then over two slow blooms keyframe an overall saturation + warmth boost and a second HSL-isolated "rosy" boost of the face/lips. Tie it to a narrative/emotional beat and keep the animation gentle so it seeps in subliminally.

## Grade-to-grade transitions (through edits, dissolves, baked masters)

- To dissolve between two **completely different grades**, deliberately cut a **through edit** and add a **dissolve transition**, then grade the outgoing / incoming clips separately — smoother than hand-keyframing between very different looks.
- **Baked-master ("tape-to-tape") workflow:** the program is flattened to one self-contained file. Far better to also receive an **EDL / AAF / XML** so the app can **notch / preconform** the file back into individual clips — then real edit dissolves become grade-handle dissolves and no keyframing is needed.
- **Caveat:** on a notched baked master, **HSL-qualified keys shift at every baked-in dissolve/fade** (the underlying levels change, so the key drifts, sometimes vanishing). Keyframe the qualifier through the transition to hold the key if it's a problem.

## When to animate vs cut

- **Animate** to *repair within a continuous take* (exposure / hue / lighting drift) or to *grow a look over time* for a narrative beat. Prefer a **cut + dissolve** (through edit) when the two states are genuinely *different grades*. Two keyframes suffice for most drift; add a third only if the change is non-linear.

## Studio application

- This chapter is the **time axis of the grade** — it maps onto the studio's edit model. A keyframed grade is a grade whose parameters **vary across a `Clip`'s duration** on the timeline in [edit.py](../../../sequitur/edit.py) (`Clip`/`Beat`/`Scene`/`Sequence`, `timeline()`). A provisional lead: the future **Colorist** emits a *time-varying grade* decision — a `Contribution` carrying start/end keyframe states + an interpolation mode over a `Clip` (or over a `Sequence` span), the colour analogue of what the crew already produce as a static `Shot`.
- The **static-vs-dynamic keyframe** distinction is the grade echo of the Editor's own cut-vs-dissolve vocabulary (`Transition`/`EditReason` in [editorial.py](../../../sequitur/crew/editorial.py), re-exported by [edit.py](../../../sequitur/edit.py)): a static key ≈ a hard cut between sub-grades; a dynamic key ≈ a dissolve. A grade-to-grade **through edit** is literally an editorial decision that then splits into two graded clips — so this seam is shared between the Editor and the Colorist.
- **Execution is transform-flavor:** a keyframed grade is applied by a **grade renderer** — a LUT/curve interpolated over already-rendered frames via ffmpeg/MoviePy, i.e. the `Cutter` execution plane ([cutter.py](../../../sequitur/cutter.py)), not a generative backend. This is the strongest new-renderer opportunity named in the readiness audit ([0019](../../../context/storyline/0019-readiness-renderer-audit-color-gap.md)); it should slot into the `Renderer` protocol being formalized ([0006](../../../context/storyline/0006-renderer-seam-and-image-backend.md)). Keeping the grade a **separate layer over the assembled clip** (never baked in) mirrors the studio's decision-plane / execution-plane split.
- **Overlap to flag — shape animation (Ch. 6):** the "wipe a correction on with a tracked shape" technique reuses the *animate-a-shape-over-time* primitive from [Ch. 6 — Shapes](ch06-shapes.md); a tracked/keyframed vignette that follows a moving subject is one capability shared by grade wipes, mixed-light isolation, and the Colorist's targeted (secondary) corrections.
- **Overlap to flag — the `ColorTemperature` seam:** the hue-shift fix is a *grade-time* correction of the scene illuminant, which the **Gaffer** owns at **capture** (`ColorTemperature`, `eye_light` in [lighting.py](../../../sequitur/crew/lighting.py)). Colour temperature therefore sits in two seats — Gaffer (capture) vs. Colorist (grade) — the overlap logged for this source, analogous to POV living in both the Director and Screenwriter seats.
