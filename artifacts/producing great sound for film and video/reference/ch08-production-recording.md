# Chapter 8 — Production Recording

> Abridged from Jay Rose, *Producing Great Sound for Film and Video* (4th ed.),
> Ch. 8.
> **Scope:** choosing a recorder, getting clean audio into it, setting levels, and
> keeping double-system sound in sync. The capture-and-sync pipeline.

## Core idea

Great pictures ≠ great sound — even high-end cameras skimp on audio. The best
quality and flexibility come from **double-system**: a **separate recorder**,
synced back to picture in post. DSLRs almost always *require* it (treat the camera
track as a low-fi **sync reference** only). **Multitrack recording saves shots** —
isolated mics avoid ADR and preserve editing options.

## Levels (the calibration that matters)

Audio quality is a **noise-vs-distortion** trade, controlled by gain:

- Keep the meter **peaking near the line-up tone**: **−20 dBFS (pro)** /
  **−12 dBFS (prosumer)**.
- Best performance is usually with the **volume control near 50%** — too low adds
  noise, too high distorts.
- **Turn off ALC** (automatic level control — it pumps noise up in pauses) and any
  mic noise-reduction gate.
- Feed a **line-level** signal where possible; put a **mixer/preamp near the mic**
  and run the balanced line to the camera rather than cranking the camera preamp.
- Use **balanced mics + Star-Quad cable + XLR inputs**; keep mic cable ≥2 ft from
  power/video and cross at right angles.

## Sync (double-system)

Two jobs: **start together** and **stay at the same speed**. Modern digital
recorders hold speed like video cameras for ≤~30 min, so non-timecode works for
short takes. Options:

- **Timecode** — the pro solution (SMPTE frame address); worth it for multi-camera.
- **Reference track** — feed the recorder's output to the camera; in the NLE slide
  the good audio until waveforms match and the echo disappears (PluralEyes
  automates this). *Insist the reference be boom-only or scratch* so an editor
  can't accidentally cut the bad camera track.
- **Slate** — the clap is **more accurate than a reference** (no room delay);
  sync to the **last blurred frame** before the sticks meet.

**Log every take** (scene/take, media) — critical for dramatized retakes where the
words repeat.

## Studio application

Provisional leads for the studio's sound layer:

- **Double-system is the studio's decision/execution split, applied to audio.**
  Capture (or generate) audio *independently* of picture, then reconcile — mirrors
  `edit.py` (decision plane) vs. `cutter.py` (execution). Generated dialog and
  the video are separate streams married by sync metadata, not baked together.
- **The level discipline is the `ReRecordingMixer`/ingest contract:** line up to
  **−20 dBFS** (pro) with headroom to peaks, never ALC-pump, never clip (ch. 2).
  These become validate-able invariants for any audio the pipeline emits (ch. 18).
- **Sync-by-reference-waveform is exactly what the `SoundAnalyst` does.** Aligning
  two audio streams by their envelopes is the same MIR operation that feeds the
  Editor's **cut-to-cue**; the "last blurred frame" slate rule is the precision
  version.
- **"Keep isolated tracks to avoid ADR"** reinforces ch. 7: candidate takes stay
  separate until the mixer commits.
