# Chapter 8 — Directing the Eyes Deeper in Space and Time

> Abridged from Francis Glebas, *Directing the Story: Professional Storytelling and Storyboarding Techniques for Live Action and Animation* (Routledge/Focal Press), Ch. 8.
> **Scope:** how the camera builds the missing third dimension — perspective and depth cues, the expressive difference between telephoto and wide-angle lenses, framing action one idea at a time, camera mobility, layered/planned staging, and proximity as the dial of audience engagement.

## Core idea

We live in three spatial dimensions; the screen has two. Something has to give — but depth is not *lost*, it is **suggested**, and the viewer supplies it from cues. The Renaissance solved this with **perspective**: an optical system based on a single viewpoint that both rebuilds depth *and* unifies the picture to one vantage, thereby directing the eye. The camera's lens handles perspective automatically, so the director's job is not to know the optics but to command the **effects** — how a given lens, angle, distance, and framing make space *read* and make the audience *feel*. This chapter carries "directing the eyes" from the flat frame into depth and, via proximity and framing, across time.

## Depth cues

Confusion returns whenever depth breaks down (competing viewpoints flatten space, cubist-style, and the eye can't orient). The director keeps space legible by stacking cues the camera captures:

- **Linear perspective** — parallel lines converge to vanishing points on the **horizon**, which always sits at the viewer's **eye level**.
- **Aerial / atmospheric perspective** — the farther an object, the more atmosphere between; distance reads as a **bluish tint, lost contrast, lost detail** (fog and underwater are the extreme).
- **Overlap** — a nearer object obscures those behind it.
- **Size constancy** — assuming like objects are the same size, larger reads as closer; **texture scale** works the same way.
- **Line direction** — diagonals tend to recede into space; horizontals and verticals read as neutral.

**Perspective and viewpoint.** One-point (on axis, subject head-on), two-point (camera to the side, two vanishing points), three-point (a third point high or low — the deepest space, looking up a tall building or down from it). **The spread of the vanishing points sets the lens feel:** points *far apart* read as **telephoto**; points *close together* read as **wide-angle**. Low ("mouse-eye") angles are dynamic — they generate diagonals; high ("bird's-eye") angles show location clearly but feel **emotionally detached** — we are above it all.

## Telephoto vs. wide-angle

The single most expressive lens decision in the chapter:

| | **Telephoto (long)** | **Wide-angle** |
|---|---|---|
| **Distortion** | little | strong at the extreme (fish-eye); unflattering to faces |
| **Space** | **flattens** / compresses | **expands** / pushes space apart |
| **Depth of field** | narrow (isolates the subject) | deep (whole frame sharp) |
| **Verticals / horizontals** | stay neutral | shift into dynamic diagonals |
| **Reach** | brings distant objects near | — |
| **Use for** | **beauty shots**, isolation | **action**, maximum movement through the frame; shoot on axis |
| **On a push-in ("truck in")** | image stays similar, just closer | dramatic change and distortion as space is pushed apart |

*(A "truck in" moves the camera closer; a "zoom in" holds the camera still and narrows the lens on a smaller area — not the same move.)*

## Framing to tell the story — one idea at a time

The frame is a tool for showing **only** what the audience should see. When two things happen at once (the recurring "say one thing at a time" problem), stage them so the frame reveals them in sequence:

- **Entrances and exits catch the eye** — let one subject exit the frame just as another enters, so attention hands off cleanly with only one focus at any instant.
- **Obscure deliberately** — a foreground head or object can hide what the audience mustn't see yet (a near-miss reads as "near," not "far," when both parties stay near the *same screen position* with something blocking their sightline).

## Camera mobility

Computer cameras are no longer bound to the earth — but with freedom comes responsibility. Too much movement **confuses**, and confusion breeds boredom; a 360° spin is not mandatory just because it's possible. Never let camera work break the **threshold of awareness** — unless the movement *is* the point. The camera has **expressive power** in its own right (it can read as ominous or sheepish); a move that tracks a subject through an arc can put the viewer *inside* the action.

## Planning depth: layers, plans, and arrows

- **Layered depth (stage flats).** Separate the scene into a **background, one or more midgrounds, and a foreground** — the logic of Disney's multiplane camera (foreground pans faster than background; one depth zone in focus, the rest blurred). Constrain each layer's **value range** to build atmospheric perspective: foreground carries the greatest contrast (≈95% grey→white), midground a middle band (≈70%→15%), background the narrowest (≈40%→20%). Eastern art has used this for centuries.
- **Plan from a simple top-down map.** Work out figure and prop placement in a schematic plan *first*, then stage for the camera — it's easy to shuffle pieces so nothing important is obscured in depth. The tool scales: block **blocking and camera moves with simple arrows** (like a football play) and you already know the compositions will stage cleanly.

## Proximity — the engagement dial

How close the camera is changes how the audience *feels* about a subject — viewers are keenly sensitive to spatial distance:

- **Wide / silhouetted / backlit** → distancing; we don't engage (good for holding a narrator "outside" the story she tells).
- **Closer** → we feel we are *with a friend*, engaged in the action.
- **Too close** → we feel we are *inside the character's thoughts*.

Proximity governs transitions too: the classic "ride off into the sunset" disengages us as the figures recede until the film can end. Because closeness pulls the audience in, **every shot should be a close-up of what you want to say**.

**POV / subjective camera.** A point-of-view shot reads as a character's view via the **shot-reaction** grammar — a shot of the character looking, then a shot of what they see. Give characters **look room**: breathing space in the direction they face; don't cramp them against the frame edge.

## Depth killers

Watch for these — they destroy the illusion of depth (and so are *useful* by contrast, to flatten a shot deliberately):

- lines run **parallel to the frame** (they flatten space);
- **ignoring size constancy** (wrong relative sizes flatten or turn surreal);
- **all-black shadows** (holes) or **all-white highlights** (pasted-on look);
- objects that don't share the **same horizon** (they feel like they don't belong together).

## Studio application

- **This chapter is the *why* behind the lens and depth enums the DP already owns.** Telephoto-flattens / wide-expands, narrow-vs-deep depth of field, and "bring the distant near" map directly onto [`FocalLength`](../../../sequitur/crew/camera.py) (`WIDE`/`NORMAL`/`LONG`/`FISHEYE`) and [`DepthOfField`](../../../sequitur/crew/camera.py) (`SHALLOW`/`DEEP`) on the [`Shot`](../../../sequitur/shot.py); the low/high-angle "dynamic vs detached" note is the intent behind [`CameraAngle`](../../../sequitur/crew/camera.py). These are **plan-phase** choices the DP sets and [`prompt.py`](../../../sequitur/prompt.py) renders as "shot on a long telephoto lens, background thrown soft."
- **Proximity as the engagement dial is the emotional reading of [`ShotSize`](../../../sequitur/crew/camera.py).** "Wide = disengaged, closer = with a friend, too close = inside their thoughts" gives each `ShotSize` rung a *feeling*, and "every shot is a close-up of what you want to say" is the studio's justification for choosing size by story point rather than by convention — a judgement the [`Director`](../../../sequitur/crew/director.py) makes when it reconciles the crew's fields.
- **Layered depth + value-range-per-layer is a shared spec between framing, the render, and the grade.** The background/midground/foreground plan with constrained value bands is exactly the atmospheric-perspective legibility that [`image.py`](../../../sequitur/image.py) must produce and the colour layer must preserve — a cross-department check that "the depth reads," not a per-shot tuning knob.
- **"Say one thing at a time" via framing is the plan-side complement of the cut.** Handing focus off with entrances/exits inside a single frame is the *in-shot* version of the same one-idea-at-a-time discipline the edit enforces across shots — keep it aligned with the [Director](../../../sequitur/crew/director.py) reconciler's single-decision model ([storyline 0014](../../../context/storyline/0014-the-crew-behaviour.md)) and the [architecture](../../../context/architecture.md)'s PLAN→SHOOT seam.

> **Overlap flag:** perspective, lenses, and depth of field here reconcile with **[Grammar of the Shot Ch. 3 — Depth, Perspective, Focus](../../grammar%20of%20the%20shot/reference/ch03-depth-perspective-focus.md)**; the "plan from a simple map / block with arrows" staging reconciles with **[Professional Storyboarding Ch. 7 — Staging](../../professional%20storyboarding/reference/ch07-staging.md)** and the shot-for-editing coverage in **[Grammar of the Shot Ch. 5](../../grammar%20of%20the%20shot/reference/ch05-shooting-for-editing.md)**. Glebas supplies the *feeling* of each lens and distance; the Grammar-of-the-Shot chapters supply the *grammar* that becomes `FocalLength`/`DepthOfField`; the board pre-visualises the depth staging.

Depth makes an image *locatable*; the next chapter asks the harder question — how a legible image is made to *mean* ([Ch. 9 — How to Make Images Speak](ch09-how-to-make-images-speak.md)).
