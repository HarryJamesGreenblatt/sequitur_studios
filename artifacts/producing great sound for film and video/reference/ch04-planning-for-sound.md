# Chapter 4 — Planning for Sound

> Abridged from Jay Rose, *Producing Great Sound for Film and Video* (4th ed.),
> Ch. 4.
> **Scope:** sound design begins in the *script*, not in post. The elements of a
> soundtrack, how they earn their place, and the order they're assembled in. This
> is the sound department's **plan** — the taxonomy the whole layer organizes
> around.

## Core idea

Sound is roughly **half the film** but usually gets a tenth of the attention, and
**a microphone does not hear like a human** — it captures every reflection and
noise the brain would filter out. So a good track is *designed early*: you hear
the dialog, effects, and music in your head while writing, mark the script for
cues, and leave frequency and time **room** for each element. Planning is nearly
free; not planning is expensive.

## The four elements of a track

| Element | Role |
|---------|------|
| **Dialog** | top of the pyramid; most important; must sound natural for the character |
| **Music** | the emotional bed — **source** (diegetic, in the scene) or **scoring** (underscore) |
| **Sound effects** | realism + storytelling |
| **Silence** | strategic absence; a deliberate hole is powerful |

Sound effects split three ways: **hard effects** (sync to on-screen action —
crash, gunshot), **natural sounds** (footsteps, rustles — texture), and
**backgrounds / ambiences** (smooth edits, establish the world).

## Design principles

- **Leave room.** Don't stack dialog under hard effects in the same frequency band
  (a metallic crunch fights a male shout). Composers layer *high* strings under
  action to leave the low-mids for effects and voice.
- **Sounds need a reference.** An off-screen sound must be established by a shot or
  a line before it can carry meaning alone.
- **Protect the center.** Dialog is almost always **mono, center channel**, even in
  surround; move a solo instrument in the vocal range off to one side if it
  coincides with a line.
- **Match perspective.** A boomed line (more room) and a close lav (intimate, dry)
  shouldn't cut together without matching; VO narration lives in "limbo" (no room
  ambience).
- **Remember the medium** — theatrical surround → broadcast → web/small speakers
  each shrink the usable dynamic range.

## The assembly order (layers of the track)

1. **Dialog** (foreground; edited first and most)
2. **Hard effects** (plot-critical)
3. **Music** (third for low-budget; *last* for theatrical)
4. **Backgrounds** (before natural sounds; smooth the edits)
5. **Natural sounds** (last; fill gaps)

**ADR is a last resort** ("that's replacing it, not fixing it") and **noise
reduction is not magic** — clean location sound always wins.

## Studio application

Provisional leads for the studio's sound layer:

- **This taxonomy *is* the sound department's data model.** The four elements and
  the three effect classes are the buckets the roles own: `SoundMixer`/`Boom`
  (dialog), `Composer` (music), `SoundDesigner` (effects), with **silence** as a
  first-class, deliberate choice. It refines the diegetic/non-diegetic split
  inherited from *Grammar of the Edit* Ch. 3.
- **The assembly order is the sound layer's pipeline sequence.** Dialog → hard FX →
  music → backgrounds → natural sounds is the order `edit.py`/`cutter.py` should
  build and the `ReRecordingMixer` should pre-dub in (ch. 10, 17).
- **"A mic doesn't hear like a human" reframes the Omni-audio question.** Because
  captured/generated audio carries everything, the studio *designs* the track in
  layers rather than trusting a single generated bed — keep well-informed
  diegetic dialog, build the rest deliberately.
- **"Leave room" + "protect the center" are mix invariants** the automated mixer
  must honor: don't collide elements in the same band or pan dialog off-center.
