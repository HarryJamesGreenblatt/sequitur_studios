# Chapter 1 — Video Editing: An Introduction to the Process

> Abridged from Christopher J. Bowen, *Grammar of the Edit* (4th ed.), Ch. 1.
> **Scope:** what editing *is*, the factors that shape editorial choices, the
> staged post-production workflow, and the four traditional transitions. This is
> the foundation the studio's planned **post-production layer** (`movie.py`) will
> encode — the companion to *Grammar of the Shot*'s production-phase grammar.

## Core idea

**Editing = assembling clips of picture and sound into a coherent story.** If a
*shot* is a "word" and a *sequence* is a "sentence," editing is the grammar that
orders them. Audiences have *learned to read* this grammar; follow its accepted
rules and the message lands, break them carelessly and it garbles.

- An **edit** (noun) = the **join point** where one shot ends and the next
  begins — a **cut point**. ("Cut" is literal: film was sliced and spliced.)
- The **editor** reviews, refines, modifies, eliminates, and assembles source
  clips into a new form — and, in doing so, *constructs the narrative* and manages
  the audience's experience. Of all the contributors, the editor most directly
  shapes the final felt result.

## Key factors affecting editorial choices

- **Tools** — medium (film / tape / digital) and software impose physical, time,
  and budget limits. Bowen keeps the grammar **tool-agnostic**: no button names,
  because storytelling method matters more than the App. *Good story-showing > latest tech.*
- **Project type & genre** — documentary, narrative short, news package, how-to,
  music video, commercial, wedding, animation. Each carries **duration limits,
  expected styles, and transition conventions** (slow dissolves suit a moody music
  video; a hard news cut does not). Budget/scope/turnaround set the ceiling.
- **Degree of audience manipulation** — the editor guides the viewer like an
  amusement-park ride. **Pacing** and **rhythm** of shots/scenes control mental,
  physical, and emotional response. The *need* and *degree* come from the
  project's **purpose** and **content**.
- **Other factors** — the editor's own creativity, plus the (non-optional) input
  of **director** and **producer**. The editor rarely has total control.

## Stages of the editing process (the post-production workflow)

Post = everything after production wraps. The industry-proven pipeline, in order
— treat **acquisition → picture lock** as the *offline* (structure) phase and
**finishing → delivery** as the *online* (finish) phase:

| Stage | What happens |
|-------|--------------|
| **Acquisition** | Gather/ingest all picture, sound, stills, graphics, music into the edit system; digitize anything not already digital. |
| **Organization** | Label, group, sort into bins/folders (by date, subject, scene). Unglamorous but decisive for a smooth edit. |
| **Review & selection** | Screen everything; **pull the selects** (the good takes), flag/color-code by usability. *Never delete* — the throwaway shot may save the cut. |
| **Assembly** | Lay the major pieces into a logical sequence — the story's longest, roughest skeleton. Follow script/storyboards *or* the narrative the footage reveals. |
| **Rough cut** | Visual fat trimmed; functional but rough — placeholder effects, no final titles, unfinished mix. Pacing readable; scenes may still be restructured. |
| **Fine cut** | Order and timing tuned; pacing fits the story; only minor tweaks remain. "This cut is fine." |
| **Picture lock** | Picture track is **frozen** — no further picture changes. Frees the audio mix (SFX, levels/pan, music) to proceed against a fixed duration. Any later picture-duration change breaks **sync** on every audio track. |
| **Finishing** (online) | Swap proxies for full-res; **color grade** (color timing/correction); best-res titles/graphics/animation; final audio mix placed in sync. |
| **Mastering & delivery** | Render and output to the target (stream file, broadcast master, film cut list, disc). Keep archival copies in multiple locations. |

Not every project touches every stage in a clean sequence, but rushing, skipping,
or reordering too freely compromises the post workflow.

## The four traditional transitions

The edit point itself — expanded in [Ch. 6](ch06-transitions-and-edit-categories.md).
Four ways to move between shots; their meanings are globally understood and have
not changed:

1. **Cut** — instantaneous change: last full frame of A → first full frame of B.
2. **Dissolve** — gradual blend; A fades down as B fades up (momentary
   superimposition). A "dissolves" away while B "resolves" in.
3. **Wipe** — a moving line or shape pushes A off while revealing B behind it.
4. **Fade** — gradual change to/from a solid color (usually black): **fade-in**
   (from black) and **fade-out** (to black).

Each persists because its *purpose* persists: a cut is neutral/continuous, a
dissolve implies passage of time or connection, a fade brackets a beginning/end.

## Durable working principles (from the chapter's PIP)

- **Organization is paramount** — clear drive/folder structure, purposeful naming,
  backed-up source media. The best editors are praised for it.
- **Speed matters** — keyboard shortcuts, consistent timeline track layout
  (same asset types on the same tracks every time) buy efficiency.

## Studio application

The studio has **no `grammar.py` analogue for editing yet** — this chapter grounds
a *new architectural surface* (the post-production layer). It sets the frame for it:

- **The pipeline becomes the agent workflow.** Acquisition → organization →
  review/selection → assembly → rough/fine cut → lock → finish maps onto how a
  future **`movie.py`** would drive post: ingest the production's rendered shots,
  register/organize them (by scene/act), pull selects, assemble a sequence, then
  refine timing. Each stage is a candidate operation on the production plan.
- **Picture lock ⇒ audio sync discipline.** Locking picture before the mix — and
  the rule that *any* picture-duration change re-breaks sync — is the constraint a
  programmatic assembler must respect when stitching shots and their audio.
- **The four transitions are the atomic vocabulary** `movie.py` must emit between
  shots (cut / dissolve / wipe / fade). Chapter 6 will make these first-class; the
  open research problem is an agent **choosing which transition, and where**, from
  the story's cues rather than a fixed rule.
- **Genre sets the pacing contract.** Because "not every project is a music video,"
  the degree of manipulation and cutting rhythm should be a **project-level input**
  to post, not a hardcoded style — so the same assembler serves a narrative short
  and a fast-cut promo.
