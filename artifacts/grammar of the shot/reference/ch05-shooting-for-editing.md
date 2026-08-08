# Chapter 5 — Will It Cut? Shooting for Editing

> Abridged from Christopher J. Bowen, *Grammar of the Shot* (4th ed.), Ch. 5.
> **Scope:** the continuity grammar that makes separately-shot coverage cut
> together — screen direction, the 180° and 30° rules, matching/reciprocal
> shots, and eye-line match. This is the backbone of the planned **sequence**
> layer; today's single `Shot` only touches it via `single_scene`.

## Core idea

Shots are recorded out of order and must edit into a seamless whole:
**shot → scene → act → film.** "Shooting for editing" = anticipating what the
editor and audience will need next, and keeping every coverage angle consistent
so the cuts read as one continuous reality.

## Continuity types

- **Continuity of performance** — actors repeat action/dialogue identically across
  every camera set-up. A dialogue scene may need 8 set-ups × N takes. Alternatives:
  **multi-camera** (always a matching cut) or the **long take** (one master, no
  coverage, nothing to cut to).
- **Continuity of screen direction** — the frame edges (frame-left/right/top/bottom)
  are the audience's compass. A subject exiting **frame left** must enter the next
  shot from **frame right** to preserve direction across the cut.

## The Line — the 180° rule

- Every scene has an **axis of action** (a.k.a. the line / imaginary line / action
  line / 180° line): an imaginary line through the subjects, traced along their
  **sight line** / line of attention.
- Once established, **keep the camera on one side** — within the 180° arc. This
  keeps left = left and right = right across all coverage. In an A↔B dialogue:
  A stays frame-left looking right, B stays frame-right looking left, even in their
  clean singles.
- **Jumping / crossing the line** — shooting from the wrong side flips screen
  direction; both characters suddenly look the same way and the cut makes no sense.
  Legit *only* as a conscious choice (or via moving talent/camera, Ch. 6) — never
  by accident.

## The 30° rule

- Between two shots of the same subject, move the camera **≥ 30° around the arc**
  (and ideally change focal length / shot size). Less than that and the two frames
  are too similar → a **jump cut** (a visible jump in space/time).
- Jump cuts are a valid *style* (French New Wave; modern vlog speech-tightening) —
  but that's an editorial choice, not the coverage default.

## Reciprocating imagery (matching / answering shots)

Whatever you shoot on Character A, shoot the **mirror** on B: match **shot size,
subject placement, camera height, angle, focal length, and lighting**. Editors
build scenes **outside-in** (wide → tight), so give equal, matching coverage of
each character. Same rule for **OTS reverses** — mismatched size/height/angle
between an OTS and its reverse reads as wrong.

## Eye-line match

A **set-up-and-pay-off**: shot 1 shows a subject looking off-frame; shot 2 reveals
what they see, framed from a **corresponding vantage** (angle/height/direction) —
a near-POV. **Withholding** the pay-off shot is a cheap, effective suspense tool.

## Consistency the editor also compares

Match **format / resolution / frame rate** (4K60 ≠ 1080p24), **exposure & color
balance**, and **camera support** (don't intercut tripod with handheld) across
coverage — especially when a scene is shot across multiple days.

## Studio application

- This chapter is the **spec for the future `sequence` planner** — the rules that
  turn a list of `Shot`s into a coherent scene:
  - Track an **axis of action** per scene; keep generated angles on one side (180°).
  - Enforce **≥30° + size change** between successive shots of a subject.
  - Generate **reciprocal/answering** shots as matched pairs (size, height, angle,
    light) for A↔B dialogue and OTS reverses.
  - Model **screen direction** (exit-left → enter-right) and **eye-line match**
    (look-off → matched reveal, with optional withhold).
- `Shot.single_scene` today enforces "no cuts *within* one clip" — the inverse
  concern. The sequence layer is where continuity *between* clips lives.
- For a generative model, continuity becomes **prompt constraints carried across
  shots**: consistent screen direction, subject side, eye-line, lighting, and
  format — the state the planner must thread from shot to shot.
