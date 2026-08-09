# Chapter 10 — Postproduction Workflow

> Abridged from Jay Rose, *Producing Great Sound for Film and Video* (4th ed.),
> Ch. 10.
> **Scope:** the order of operations from picture lock to final mix, the NLE-vs-DAW
> division of labor, and NLE↔DAW interchange. The sound layer's pipeline spine.

## Core idea

Getting the **sequence right saves money and improves the track.** A dedicated
audio program (**DAW**) beats an NLE's audio tools substantially — better faders,
better rooms, cleaner path — but the discipline that matters most is *ordering the
work* so you never redo it.

## The workflow

1. **Lock picture first** — any change to picture *timing* means rebuilding audio.
2. Have the **non-sync drivers** (montage music, VO) ready up front.
3. Edit picture + **sync dialog/VO** together (use **handles** — a few extra
   seconds on each clip — for room tone and soft transitions).
4. Drop **placeholder effects** (plot-critical only).
5. **Approve picture**; warn stakeholders that later picture changes cost audio.
6. Fine-tune audio in **priority order** (below).
7. **Pre-mix** if complex (dialog → effects → music).
8. **Full playback review** without stopping; note fixes.
9. Render final + **stems** (dialog / effects / music separately).

## Audio priority order

**Dialog → narration/VO → plot-critical SFX → (music, for small projects) →
backgrounds → smaller sync effects → (music last, for theatrical).** Dialog is
edited first and most; cutaways smooth or substitute problem lines.

## Interchange (keeping sync across tools)

- **Sync-beep method** (most robust): export mixed tracks with a beep on the head;
  re-import and realign to the beep — survives off-speed playback.
- **OMF/AAF**: industry standards but with proprietary quirks — test before a big
  job (AATranslator bridges formats).
- **EDL**: human-readable clip/timecode list — good for debugging.
- **Handles**: always carry a few seconds beyond each in/out for room tone and
  transitions.

**Hollywood dialog editing** splits one NLE track into **many tracks by
character/setup** (different room tones and voices treated separately), extended
with matching room tone for smooth overlaps.

## Studio application

Provisional leads for the studio's sound layer:

- **This is the ordering contract for `edit.py` / `cutter.py` on the audio side.**
  The nine-step workflow and the dialog→FX→music priority define the sequence the
  post crew (`SoundEditor` → `ReRecordingMixer`) executes; "lock picture first"
  means the **cut is committed before the mix is built**.
- **Handles map directly onto the edit layer's handle-padding.** *Grammar of the
  Edit* Ch. 6 already gave the studio handle padding on generated shots; this
  chapter shows the *audio* reason — room-tone overlap and soft transitions — so
  the two handle concepts unify.
- **Stems = the diegetic/non-diegetic split, rendered.** Emitting D/M/E stems is
  how the studio keeps production dialog separable from post soundtrack (the
  open question from the brief), and it's a concrete `ReRecordingMixer` output
  (ch. 17).
- **Track-splitting by character/setup** is the data shape for candidate dialog:
  per-source tracks with their own room tone and treatment, chosen and blended at
  mix — reinforcing ch. 7–8's "keep separate until commit."
