# Chapter 14 — Working with Music

> Abridged from Jay Rose, *Producing Great Sound for Film and Video* (4th ed.),
> Ch. 14.
> **Scope:** sourcing music (original vs. library, licensing traps) and **editing
> music to length on the beat** without knowing music theory. Grounds the
> `Composer` role and the toaster-strudel MCP seam.

## Core idea

You can make music *fit* professionally even if you can't read a note — because
**edits land on the downbeat**. And you must **respect copyright**: music is the
one element where a wrong assumption is a legal liability, not just a bad sound.

## Licensing (the ironclad traps)

- **Any video use needs permission** — YouTube, wedding video, corporate training,
  all of it.
- **Buying a CD ≠ sync rights.** Sync (music-to-picture) is a *separate* right.
- **Two copyrights per song:** the **composition** (notes/lyrics) and the
  **recording** (master) — different owners, both required.
- **Public-domain melody ≠ public-domain recording**; a modern arrangement is a
  new copyright.
- **A broadcaster's annual ASCAP/BMI fee does NOT cover your produced video.**
- **Fair use is near-nonexistent** here; brevity is no defense.
- **Buyout** libraries (pay once, reuse) vs. **needle-drop** (per-use, higher
  quality, deeper catalog; needs a **cue sheet** for broadcast).

## Beat-based editing (the core technique)

Most music is a **4-beat measure**; **beat 1 (the downbeat)** is the strongest
accent. **Every music edit respects a constant measure length (downbeat to
downbeat):**

1. Play, tap the rhythm, **hard-tap only beat 1**; mark each downbeat.
2. **Shorten** by deleting between two downbeat markers; **lengthen** by copying a
   section and pasting at another downbeat.
3. Handle a **melody pickup** (note *before* the downbeat) by rolling the edit back
   to catch the melody start while keeping downbeat spacing.

**Troubleshooting:** a hiccup means a marker landed off-beat; a chord/melody clash
means try an **odd number of measures** earlier/later.

## Tempo and fit

- Speed the whole piece **±3%** before timbre distorts (synths tolerate ~±10%);
  **tempo-without-pitch** stretches up to ~±20%.
- Edit music *to picture* by aligning a **downbeat/climax with a visual hit**.
- **Take-away test:** mute the music — if you don't feel something missing, it
  isn't working.

## Studio application

Provisional leads for the studio's sound layer:

- **This is the `Composer` role's grounding, and it makes the toaster-strudel MCP
  seam pay off.** Beat-based editing *is* an MIR operation — detect the downbeat
  grid, cut/repeat on measures — which is exactly what toaster-strudel's `mir/`
  provides. The studio **drives Strudel through the MIT MCP layer** rather than
  reimplementing music theory; Rose supplies the *editorial* rules
  (downbeat-to-downbeat, odd-measures fix) the MCP client applies.
- **The beat grid + "align a downbeat with a visual hit" is the musical half of
  cut-to-cue.** It composes with ch. 13's *content* cutting: `SoundAnalyst` can
  offer both a **beat grid** (music) and **phoneme/reaction cues** (dialog), and
  the Editor cuts on whichever the scene motivates.
- **Licensing is a first-class constraint, not a footnote.** The `Composer` must
  prefer **generated/owned** score (Strudel) or cleanly-licensed cues, and carry
  rights metadata — a direct parallel to the repo's own **copyright gate** on
  source text.
- **±3% imperceptible tempo tolerance** is an encodable fit heuristic for
  stretching a cue to a scene's length.
