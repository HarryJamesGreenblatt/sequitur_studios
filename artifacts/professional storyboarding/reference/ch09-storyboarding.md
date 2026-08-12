# Chapter 9 — Storyboarding

> Abridged from Sergio Paez & Anson Jew, *Professional Storyboarding: Rules of Thumb* (Focal Press, 2013), Ch. 9.
> **Scope:** the working *process* of turning a script into boards — gather specs, analyse the script, break it into beats, thumbnail, self-edit, then draw finished panels. This is the core workflow chapter.

## Core idea

A storyboard artist is a "mini director": you take ownership of a scene and construct it in the most exciting, most *efficient* visual way possible. But before a single panel is drawn, the work is analytical, not artistic — you read the script until you can recite the who/what/where/when/why *and* how each character feels internally and acts outwardly, you identify the one **story point** the scene exists to deliver, then you plan staging and shot flow in cheap disposable **thumbnails**. Only once the story problems are solved do you commit to finished drawing. Craft serves clarity: every panel is measured against the story point, and anything that distracts from it is cut.

The whole pipeline is front-loaded. On a week-long assignment you might spend three days scratching out thumbnails and organising ideas so that finished boards flow quickly. Skipping that planning means settling for the first idea off the top of your head — occasionally fine, usually shallow.

## Set-up: gather the specs first

Before drawing, collect the technical frame the boards must live inside:
- **Aspect ratio** of the project.
- **Character / background / prop designs** (from the producer; if none exist, research your own reference — never copy).
- **Delivery format** (scanned paper vs digital JPEG).
- **The script or outline** — or, absent one, verbal direction from the director. Take notes; ask every question *before* drawing.

## The process, step by step

**1. Script analysis.** Read the *entire* script, then re-read your section until you no longer need the page. Know the sequence of events, the emotional interior of each character, and how the scene serves the film's themes and the scenes around it.

**2. Break into beats / take inventory / gather reference.** Split the story into beats so you know what to *show* and what to leave out. Scan for every person, place, and prop you must draw and confirm you can draw it (or have reference). Do this before panel one.

**3. Script notes & plan view.** Mark the script with notes and margin thumbnails — deciding *what* to describe and *when*, and which shot serves each moment (close vs wide, high vs low, insert a reaction here, add another establishing shot). Draw an **overhead plan view** (architectural top-down) to plot furniture, entrances/exits, and character positions relative to camera. The plan view doubles as an approval artifact to align the director on your camera choices before you draw.

**4. Interpret the script.** Action cues hide in *both* description and dialogue — read every word. `EXT./INT.` + time of day dictates establishing shots and how you signal time (lit streetlamps, night sky). Named characters ("the General thanks Father Michele and Javier") cue **reaction shots**. Scripts carry no camera or staging detail — that's *your* job to fill. A single sentence ("The Riders come over the hillside as the army battle ensues") can trigger hundreds of panels: *a few words in a script add up to a thousand pictures.*

**5. Fulfil the story point.** Every scene exists for one reason; make it crystal clear. Know it before you draw ("Bob grabs his lunch from the counter") so you choose the most efficient, unique staging and cut everything that doesn't serve it. A clear story point in your head saves rounds of revision.

**6. Read the subtext.** Subtext is the meaning *behind* the lines. The same greeting ("You're all grown up and dashing") is a warm reunion or a grieving widow's pain depending on the story — and the staging changes completely (a hug in the entryway vs a back turned to a photo of the dead husband). Stage to reflect what characters *mean*, not just what they *say*; it adds depth without changing a word.

## Thumbnails

A thumbnail is a fast, tiny (1–2 inch) rough — many to a sheet — testing shot choice and composition *before* detail. Do not polish: fancy drawing hides story flaws, and any good director sees through shading. "Forget about the drawing and start communicating." Thumbnailing is where you discover emotional beats through shots and staging; draw, cross out, redraw, exploring every possibility for the freshest solution. Each takes a minute. What must read even at this size:

- Interesting **composition**
- Unique **camera angles** and shot **variety**
- Interesting **staging**
- Resolved **screen direction**
- A communicated **story point**

**Starting the rough:** if stuck, drop a **vanishing point** (inside or outside the frame) and radiate lines into the image — even bare compositions carry psychology (dynamic, serene, erratic, formal). Roughs should be simple and unlaboured, but *simple ≠ sloppy*: nail the rough and clear, accurate finishes come easily; rush the rough hoping the finish will fix it, and it won't.

**Double-check.** Read the whole scene back a few times. If you'd never seen the script, would these boards convey the story and the *feel* of the finished film? Fix composition problems, then review with the director before moving to finishes.

## Finished storyboards

The story problems are solved, so this stage is pure execution — but clarity still beats beauty. General finish guidelines:

- Solid poses with a **clear silhouette**.
- 2–3 grey tones is plenty; **limit colour** to where it's necessary.
- **Limit arrows** — add more panels with more poses to carry the action instead.
- Clean, **on-model** drawings for traditional TV boards.
- A **perspective grid** per panel for maximum clarity.

**Digital boards** are now the professional default (Cintiq + Photoshop-style layered software) — vastly faster and higher-volume than paper. Work in **layers** for flexibility: background, perspective grid, character, foreground, and separate tone layers, so revisions and complex camera moves stay editable.

## Self-editing checklist

The key discipline is *self-editing* — seeing whether a shot works and why. Interrogate every panel:

- Does the shot **fulfil the story point**? Is this the *best* angle for it?
- Does it have **depth** — foreground, middle ground, background?
- Is it too **flat** / over-reliant on profile? Good **silhouette**?
- Too many horizontals/verticals — is it **symmetrical**? (avoid)
- Are subjects **coming toward / going away** from camera? (maximise depth)
- Do you **vary angles** across cuts (low ↔ high)? Interesting shapes?
- Are you **reusing a composition**? (avoid — keep the audience engaged)

And per scene / per moment: what changes from the scene's start to its end, and who is affected? Who or what is the focus right now, who's in control, where are we, what's the subtext, what nonverbal cue reveals it — and what do you want the audience to *feel* (speed, calm, chaos)?

## Studio application

- **This workflow *is* the plan-phase pipeline the crew engine models.** Script analysis → break into beats → shot selection → per-panel `Shot` spec → reference keyframe maps directly onto the studio's `Brief` → role `Contribution` → `Director` reconcile → `ImageStudio` keyframe chain ([`../../../sequitur/crew/role.py`](../../../sequitur/crew/role.py), [`../../../sequitur/crew/director.py`](../../../sequitur/crew/director.py), [`../../../sequitur/image.py`](../../../sequitur/image.py); crew-behaviour devlog [`../../../context/storyline/0014-the-crew-behaviour.md`](../../../context/storyline/0014-the-crew-behaviour.md)). A finished board panel is a *pre-rendered `Shot`*: it encodes size/angle/composition and conditions a rendered shot.
- **The "story point" is the invariant every `Shot` and every `Contribution` must serve** — the single reconciliation criterion the `Director` weighs proposals against. Anything a role proposes that doesn't advance the scene's story point is cut, exactly as the artist cuts a distracting panel. It is the plan-phase analogue of the shooting script's intent (Directing [`../../directing/reference/ch24-developing-the-shooting-script.md`](../../directing/reference/ch24-developing-the-shooting-script.md)).
- **The overhead plan view is the staging model that precedes framing.** Positions, entrances/exits, and character-to-camera relationships are decided top-down before any panel encodes a specific `angle` or `size` on the [`../../../sequitur/shot.py`](../../../sequitur/shot.py) — the studio should resolve *staging* (who is where) before *framing* (how the camera sees it), and screen direction resolved here feeds the 180° continuity of Grammar of the Shot [`../../grammar%20of%20the%20shot/reference/ch05-shooting-for-editing.md`](../../grammar%20of%20the%20shot/reference/ch05-shooting-for-editing.md).
- **Thumbnails are cheap exploration before committing to a render.** The plan phase should generate and discard many low-cost `Shot` candidates (fast, unpolished, communicating only shot flow) before spending a real `ImageStudio` keyframe — the studio's own "draw, cross out, redraw." A board panel maps 1:1 onto an `ImageStudio` keyframe, so the still is built from framing/camera/lighting only, matching `build_image_prompt` in [`../../../sequitur/prompt.py`](../../../sequitur/prompt.py).
- **The self-editing checklist is judgment as code.** Depth, silhouette, angle variety, anti-symmetry, and no-reused-compositions are exactly the quality axes a critique/judgment role should score a proposed `Shot` on ([`../../../sequitur/crew/camera.py`](../../../sequitur/crew/camera.py)), and grounds a future **Storyboard Artist** role whose `Contribution` seeds the `Brief` the `Director` reconciles ([`../../../sequitur/studio.py`](../../../sequitur/studio.py)).
