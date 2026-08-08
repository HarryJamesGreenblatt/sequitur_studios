# Chapter 4 — Assessing Footage: Selecting Shots for the Edit

> Abridged from Christopher J. Bowen, *Grammar of the Edit* (4th ed.), Ch. 4.
> **Scope:** the criteria for judging coverage and choosing which shots to cut
> together — the technical/aesthetic **quality checklist**, the continuity rules
> (screen direction, 180°/30°, matching angles/eye-line/action), and the
> **outside-in master-scene assembly order**. This is the richest source for the
> future assembler's **shot-selection logic**. Overlaps
> [*Grammar of the Shot* Ch. 5](../../grammar%20of%20the%20shot/reference/ch05-shooting-for-editing.md).

## Core idea

Once footage is organized, the editor **assesses each shot** for technical and
aesthetic quality, then selects — not always the *best* shot, but the *most
appropriate* one for the story and genre. Some flaws are fixable in post; one is
not.

## The assessment checklist

| Criterion | What to judge | Fixable in post? |
|-----------|---------------|------------------|
| **Focus** | Soft/blurry image | **No — the one unfixable flaw.** Audiences won't tolerate blur; salvage only the in-focus regions. |
| **Framing & composition** | Headroom, look/nose room, horizon level, aspect reformatting (pan-and-scan, pillar-box) | Partially (reframe/scale); composition mostly not. |
| **Exposure & color balance** | Too bright/dark, color-temp shifts, mismatched brightness within a scene | **Yes** — grade/correct (luminance, chrominance). |
| **Performance** | Acting/direction quality | No — but a strong performance *masks* minor continuity glitches. |
| **Audio quality** | Levels, presence (matches shot size?), hiss, overlap, ambience pollution, room tone present?, audio exists?, rights | Mostly yes (gain/EQ/ADR); overlap & missing audio are hard. |

## The continuity rules (which shots may cut together)

- **Screen direction** — frame left = screen left. Exit frame-left in A ⇒ enter
  frame-right in B. Break it and the subject seems to reverse (reads as a jump cut).
- **180° rule / axis of action / the line** — the first (wide) set-up draws an
  *imaginary line* along the subjects' sight lines; all coverage stays on one side
  or spatial relationships flip. **Crossing the line** ⇒ characters look the same
  way instead of at each other.
- **30° rule** — successive angles on the same subject must differ by ≥30° (and
  ideally shot size too), or the cut "jumps." The editor can't move the camera but
  *chooses which two angles to juxtapose*.
- **Matching angles** — dialogue coverage is shot so each character's CU/OTS
  mirrors the other's (same size, height, lighting, focus, opposite side). They
  "answer" one another.
- **Matching eye-line** — the line from a subject's eyes to their off-screen object
  of interest must trace *across the cut* into the next shot.
- **Continuity of action** — the same action must match across framings (the
  water-bottle mustn't jump hands). Trimming a frame or two off the tail/head
  smooths minor mismatches; major ones need a cutaway.
- **Continuity of dialogue** — words/timbre/pace may vary take to take; a stronger
  performance often beats strict continuity.

## The outside-in master-scene assembly order

The tried-and-true template for cutting a dialogue scene:

1. **Establishing shot** (very wide — where/when)
2. **Wide shot** (characters placed in the space)
3. **Closer two-shot** (bring them together)
4. **OTS on character A**
5. **Answering OTS on character B**
6. **MCU of character A**
7. **Answering MCU of character B**

Cutting between *matching* coverage (OTS↔OTS, MCU↔MCU) reads as balanced and
belonging together.

## Best vs. most appropriate

The technically perfect take isn't always the right one. Genre sets the tolerance
(a vlog forgives auto-focus hunting; a drama does not), and a compelling
performance with a minor glitch usually beats a clean but flat take.

## Studio application

The single most directly encodable chapter for a future **`movie.py`**
(provisional — no code yet):

- **The checklist is the assembler's shot-selection scoring function.** Each
  criterion becomes a feature to rank Omni-generated coverage on; the
  **fixable/unfixable split is decisive** — *focus/framing* problems mean
  **re-generate the shot** (Omni/`gpt-image`), while *exposure/color* problems mean
  **defer to a post color pass**, not a re-shoot.
- **The continuity rules are the "can these two clips cut together?" predicate.**
  Screen direction, 180°/30°, matching angle/eye-line/action are exactly the
  constraints an agent must check when ordering coverage — the concrete form of the
  brief's **cut-to-cue** problem. (These are the same rules the shot layer's planned
  *sequence* layer references; the edit layer is their post-side consumer.)
- **The outside-in order is a ready-made assembly template.** A scene-level
  assembler can default to establishing→wide→2S→OTS/OTS→MCU/MCU, requesting exactly
  that coverage from production — which tells the **shots→scenes→acts** generator
  what to shoot.
- **"Most appropriate > best" argues for genre as a first-class input**, echoing
  [Ch. 1](ch01-the-editing-process.md): the selection weights should shift by
  project type, not be hardcoded.
