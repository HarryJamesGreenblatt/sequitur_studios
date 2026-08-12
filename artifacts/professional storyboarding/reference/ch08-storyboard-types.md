# Chapter 8 — Storyboard Types

> Abridged from Sergio Paez & Anson Jew, *Professional Storyboarding: Rules of Thumb* (Focal Press, 2013), Ch. 8.
> **Scope:** the distinct *kinds* of boards and when each is used — beat, continuity/shooting, live-action, feature-animation, advertising/pitch, TV-animation, video-game — plus **previs**, and the level of finish each purpose demands.

## Core idea

The fundamentals of visual storytelling are constant; what changes across board types are the **technical requirements** and the **level of finish** dictated by the deliverable's purpose. One axis governs the whole taxonomy: is the board a **blueprint** (a faithful record of every shot, to be executed) or a **conceptual sell / early sketch** (an idea to be imagined or pitched, expecting revision downstream)? Blueprints trade rendering for accuracy and use **more poses, fewer arrows** so hook-ups read cleanly; conceptual and pitch boards trade accuracy for polish and lean on **arrows** to imply motion in a single rendered frame.

## The board taxonomy

| Type | Purpose | Finish | Motion shown by | Notes |
|---|---|---|---|---|
| **Beat boards** | Convey major story points early; agency/commercial work | Higher (more time per image) | Single climactic image | *Not* how it's shot — one-image storytelling à la Rockwell/Cornwell; others flesh out the gaps later |
| **Continuity / shooting boards** | Describe **every shot and beat**; hand-off to the cinematographer | Functional | **More poses, fewer arrows** | The blueprint; source material for an **animatic** |
| **Live-action boards** | Plan compositions, schedule set pieces & gear | Conceptual, often rendered | **Arrows** for camera/stage direction | Usually *inspiration only* — director/DP finalize angles on set; execution-only work, freelance/union |
| **Feature-animation boards** | **Design and mold the story itself** | Varies wildly (even thumbnails ship) | **Multiple poses**, rarely arrows | Story dept is central; artist may alter dialogue; **not** "on model"; value = the story point, not the render |
| **Advertising / pitch boards** | Sell the idea to a client | Highest — finished illustrations, full color | Arrows | Presentation over story design |
| **TV-animation boards** | Tight production blueprint | Continuity-level, **on model** | Poses + indicated camera/layout | Drawn for overseas animation to key off directly; tight deadlines |
| **Video-game boards** | In-game action **and** cinematic cut-scenes | Cross of continuity + TV-animation | Mixed | Cut-scenes are mini-movies needing feature-level care; rarely a dedicated staff role |

## What separates the types

- **Fidelity is set by purpose, not pride.** A last-minute thumbnail that communicates the beat can out-value a beautiful drawing that doesn't — most explicit in feature animation, where "the true value is the communication of the story point."
- **Arrows vs. poses is a hook-up decision.** Boards meant to be *executed as animation* (continuity, feature, TV) add poses and drop arrows so each beat is legible; boards meant as *reference or pitch* (live-action, advertising) use arrows to compress motion into one rendered frame.
- **"On model" only where it's the blueprint.** TV animation must be on model (overseas teams key straight off it); feature animation deliberately need not be (animators define the final look).
- **Authorship varies.** Live-action and advertising are largely execution against a locked script/director's notes; feature animation grants real story authorship.

## Previs — the 3D cousin

**Previs** (previsualization) blocks a script's shots as **rough 3D animation** — from simple cameras flying a digital set to lit, effects-laden sequences — cut together into an **animatic** like final footage. Its advantage over drawings is exact **timing, scale, and true camera lenses**; its cost is that every element must be modeled, rigged, and animated, so it's usually reserved for the most complex action. It doesn't replace story sense: no amount of 3D rescues a poorly conceived scene, and the mandate is unchanged — **tell the best story possible.** Previs teams often board on paper first before committing to expensive assets.

## Studio application

- **This is the taxonomy of the studio's deliverable.** It defines what a (future) **Storyboard Artist** role would emit and at what **fidelity** — the axis that maps directly onto [ImageStudio](../../../sequitur/image.py): a **rough thumbnail** (cheap, for blocking) vs. a **finished reference keyframe** that conditions a video shot. A board is a pre-rendered [Shot](../../../sequitur/shot.py); the *type* chooses how much of that shot's grammar the keyframe must nail down.
- **Continuity board → the ordered `Shot` list; animatic → the assembled edit.** A shooting board's "every shot and every beat" is the studio's shot sequence; the **animatic** cut from it is the province of [edit.py](../../../sequitur/edit.py) and [cutter.py](../../../sequitur/cutter.py). The blueprint-vs-conceptual split tells the [Director](../../../sequitur/crew/director.py) reconciler how binding a plan-phase `Contribution` should be.
- **Previs is the closest analogue to Sequitur's own pipeline.** "Rough 3D block-out with accurate lenses, cut into an animatic" is functionally what [studio.py](../../../sequitur/studio.py) + the edit layer produce — Sequitur is a *generative previs/production* pipeline. The lens/timing precision previs adds over drawings mirrors why a rendered keyframe conditions the video model better than a text prompt alone (`build_image_prompt` in [prompt.py](../../../sequitur/prompt.py)).
- **A Storyboard Artist seat, when added.** Such a role would live beside the plan-phase crew (there is no `ART`/previz department in [role.py](../../../sequitur/crew/role.py) yet) and choose an **output fidelity** per shot — thumbnail for internal blocking, finished keyframe for the shots the video studio actually conditions on. See the crew-behaviour pattern in [0014](../../../context/storyline/0014-the-crew-behaviour.md) and the preproduction framing in Directing [ch23-planning-the-visual-design](../../directing/reference/ch23-planning-the-visual-design.md).
