# Chapter 5 — When to Cut and Why: Factors That Lead to Strong Edits

> Abridged from Christopher J. Bowen, *Grammar of the Edit* (4th ed.), Ch. 5.
> **Scope:** the **decision model** for the cut itself — the six factors that
> motivate *when* and *why* to cut, from new-information and on-screen motivation
> to composition, angle, continuity, and sound. This is the single most important
> source for the studio's **cut-to-cue** problem — how an agent decides where to cut.

## Core idea

Editing isn't stacking shots; it's deciding **why cut here, to this shot, now.**
Every edit should answer two questions at once: *what reason leaves the outgoing
shot?* and *what new value enters the incoming shot?* The six factors below are
the reasons a cut is motivated.

## 1. Information — the incoming reason

Every new shot must deliver **new information** — visual, aural, or **tonal**
(mood/sensory). When a shot has **exhausted its information**, it's time to cut.
The editor's four questions:

- What *would* the audience expect to see next?
- What *should* they see next?
- What *can't* they see next (withhold for suspense)?
- What do *I want* them to see next?

> No matter how beautiful a shot, if it adds no new information (or tonal value),
> it may not belong in the cut.

## 2. Motivation — the outgoing reason

There must be a reason to **leave** the current shot. Three kinds:

- **Picture motivation** — movement/action: a car jump, or a subtle **eye glance
  off-screen** motivating a **reveal** (or a *withheld* reveal for suspense).
- **Sound motivation** —
  - a sound *in* the shot (teakettle whistle) motivates a cut to its source (raise
    its level to match the tighter shot's proximity);
  - a **concept edit** — sound/image as **visual metaphor** (the boiling kettle =
    the farmer's anger);
  - a **sound bridge (J-cut)** — incoming audio starts *under* the outgoing picture
    and leads the viewer into the new shot (kettle whistle morphs into a train
    whistle).
- **Time motivation** — **pace and rhythm**. Shot duration is set by the scene's
  energy: fast/canted cutting for chaos, tango back-and-forth for tension, a long
  static hold for grief. **Film time ≠ real time** — the editor controls it
  (**elliptical** edits jump forward). Pace the whole piece like a roller coaster:
  to go fast you must first go slow.

## 3. Shot composition — eye-line match & eye trace

Alternating characters frame-left / frame-right makes the audience **trace the
eye-line across the cut** (like a tennis ball). Reward the trace: place the
incoming subject where the outgoing subject's gaze pointed. Cutting into/out of
**complex compositions** needs care — give the eye time to find the new
information or the viewer drops out.

## 4. Camera angle — avoid the jump cut

Two shots of the same subject from angles **< 30° apart** (the 30° rule from
[Ch. 4](ch04-assessing-footage.md)) read as a **jump cut**. The editor can't move
the camera but *chooses which angles to juxtapose* — differ by angle **and**
shot size for a clean cut.

## 5. Continuity — "invisible editing"

Continuity (invisible) editing keeps cuts unnoticed. Three forms to preserve, each
fixable by a **cutaway/insert** that buys the audience time to accept a change:

- **Continuity of content** — objects/actions match across coverage (phone stays in
  the same hand; the dog stays at the table). Mask a mismatch with a cutaway.
- **Continuity of movement** — screen direction holds across the cut; to reverse
  direction, insert a **neutral shot** between.
- **Continuity of position** — a subject on frame-right stays frame-right unless
  they move; jumping sides breaks the illusion.

## 6. Sound — continuity & perspective

Diegetic sound carries **across** the cut (the airplane heard in shot A persists,
slightly lower, under shot B). Mix levels by **proximity and narrative
importance**; keep an unbroken **ambience/room-tone bed** (Ch. 3) under everything,
ducked below dialogue.

## Key PIP

- **Cut away once the subject's look *rests* on its object of interest** — the
  solid final gaze + recognition is the strongest cut point (the reveal).
- **Cut to reaction shots *during* a phrase, not at its end** — it's less
  predictable and often carries more weight than the line itself.

## Studio application

The blueprint for a future **`movie.py`** cut-decision engine (provisional — no
code yet):

- **The six factors are the cut-decision ruleset.** "New information or tonal value
  in the next shot" + "a motivation to leave the current one" is the core predicate
  an agent evaluates at every candidate cut point — the concrete shape of the
  brief's **cut-to-cue** problem.
- **Sound motivation unifies the two audio philosophies.** *Time motivation*
  (pace/rhythm) is exactly the prior **beat-grid/energy-contour** workflow;
  *picture/sound motivation* (glance→reveal, teakettle→source, sound bridge) is the
  **content-driven** domain knowledge. They **compose**: an agent can gate a
  beat-aligned cut on whether a *motivated* reveal/reaction is available — rhythm ×
  narrative, not rhythm alone.
- **Eye-line trace + 30° + continuity forms are the "clean cut" constraints** the
  assembler checks when ordering coverage; cutaways/inserts are its **repair
  operations** for masking a discontinuity between two otherwise-wanted clips.
- **Film-time control is the editor's superpower to encode.** Elliptical edits and
  per-scene shot durations mean `movie.py` owns *pacing* as a first-class knob,
  driven by genre/scene energy (echoing [Ch. 1](ch01-the-editing-process.md)'s
  degree-of-manipulation), not fixed clip lengths.
