# Chapter 1 — The Shots: What, How, and Why?

> Abridged from Christopher J. Bowen, *Grammar of the Shot* (4th ed.), Ch. 1.
> **Scope:** the vocabulary of shot *sizes*, the *frame* itself, and the
> pre-production pipeline that produces shots. This is the foundation the
> studio's `ShotSize` enum encodes.

## Core idea

A **shot** = one subject, one viewpoint, one duration — a discrete unit of
coverage. Shots form a *language*: audiences decode meaning and feeling from a
shot's content, composition, lighting, tonality, and sequence, largely
unconsciously. Compose deliberately, or the message garbles.

**Proximity principle** (the through-line of the whole book): a subject's
*magnitude in frame* reads as its *perceived nearness*, which reads as its
*narrative importance and emotional intimacy*.
- Small / far → insignificant, isolated, vulnerable, observed.
- Big / near → important, intimate, urgent (welcome if we like them,
  threatening if we don't).

## The frame

- **Aspect ratio** = width : height. Studio default **16:9 (1.78:1)**.
  - **9:16 / 4:5** vertical reads mobile/social and often claustrophobic — hard
    to fill the extreme top/bottom; rare in narrative long-form.
  - **1:1** square = social. Widescreen matches the human field of view
    ("we see in widescreen").
- **Resolution** ≠ aspect ratio: HD 1920×1080 and UHD/"4K" 3840×2160 are *both*
  16:9. Resolution is pixel count; aspect ratio is shape.
- The frame is a 2D cut-out of a 3D world; **depth is an illusion** (see Ch. 3).

## The nine shot sizes (the "extended family")

Gauged against a standing human figure, eye-level, subject centered. Three base
families — **LS / MS / CU** — subdivide into nine gradations. Cut points are the
precise, prompt-ready diction:

| Code | Shot | Frame cut | Conveys / use |
|------|------|-----------|---------------|
| ELS / XLS | Extreme long / extreme wide | Subject tiny or absent | Where + when; scale, arrival, epic. Establishing / drone "beauty" shots. |
| VLS | Very long | Full figure small (< ½ frame height), some clothing detail | Where + when + a hint of who. |
| LS / WS | Long / wide / full | Head-to-toe, just inside top & bottom | Where + when + who (gender, dress, gross expression). Establishing in tighter spaces. |
| MLS | Medium long / knee | Cuts just above/below the knee (**above knee = "American" / "cowboy"**) | More who than where. |
| MS | Medium / waist | Cuts at the waist | Who; some where/when. **Dialogue workhorse**; broadcaster stand-up. |
| MCU | Medium close-up / bust | Cuts at chest (~top two buttons); arms cut above the elbow | Face prominent. **Most common shot**; talking-head / interview. |
| CU | Close-up / head | Just below chin to just above hairline | Full face, eyes, subtle emotion. |
| BCU | Big close-up / choker (US) | Forehead & chin cropped; face fills frame | In-your-face emotion; demands stillness. |
| ECU / XCU | Extreme close-up ("Italian shot", per Leone) | A single detail — eyes, mouth, hand, object | Emphasis / symbolism; needs a prior wide for context. |

Supporting notes:
- **Direct address** ("direct-to-lens") — subject looks into the lens, breaking
  the fourth wall. Common in vlogs / non-fiction / UGC.
- Tighter shots benefit from **shallow depth of field** to blur distracting
  backgrounds.
- Small delivery screens (phone, TV) favor **MS–MCU**; big CU / ECU used with
  discretion or they read as visual anomalies.
- Object size on screen ≈ its importance *at that moment* — a lever, not a law.

## Coverage & the master scene technique

Record the whole scene wide (the **master shot / "safety"**), then repeat the
action from tighter and other angles — this is **coverage**. The editor
assembles wide → tight. This guarantees a scene can be cut together and is the
conceptual basis for the studio's planned **sequences** layer.

## Production pipeline (where shots come from)

- **Pre-production** — script + script analysis/breakdown, **shot list**,
  storyboards, **animatics** (animated boards + scratch audio), **overheads /
  floor plans** (bird's-eye blocking of camera/talent/lights), scheduling,
  location scouting.
- **Production** — principal photography. Camera **set-ups** labeled scene +
  letter (`1`, `1A`, `1B`); repeated **takes** (`1-1`, `1-2`).
- **Post-production** — edit, sound, grade, distribute. (Phases overlap.)
- **Shooting ratio** = recorded : used (e.g. `7:1`). Lower = cheaper/faster.

## Studio application

- `ShotSize` in `sequitur/grammar.py` encodes this family — the single richest
  lever for controlling perceived intimacy/importance in a generated shot.
  `build_prompt` already leads with the size, which is correct per this chapter.
- The full nine-shot family is encoded, **including `ShotSize.VERY_LONG` (VLS)** —
  the rung between ELS and LS.
- Prefer **cut-point language** ("frame cuts just above the knee"; "chest, arms
  cut above the elbow") over bare codes when rendering prompts — the model
  responds to the concrete framing description.
- **Aspect ratio** is a real `Shot` field; 9:16 vs 16:9 changes composition
  strategy, not just the crop.
- Master-scene / coverage + shot lists are the vocabulary for the future
  multi-shot **sequence** planner.
