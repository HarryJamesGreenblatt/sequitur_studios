# Chapter 12 — Levels and Digitizing

> Abridged from Jay Rose, *Producing Great Sound for Film and Video* (4th ed.),
> Ch. 12.
> **Scope:** getting audio *into* the project cleanly — ingest vs. capture,
> gain-staging, sample rate and sync, metering standards, and timecode (including
> the NTSC dropframe trap). The asset-ingest contract.

## Core idea

**Clean ingest is the foundation** — check and fix damage *before* editing. Modern
files are **ingested** (high-speed copy, no quality loss), not **captured** in
real time. Stay **all-digital end-to-end**; every analog re-digitize adds noise and
distortion.

## Sample rate, bit depth, sync

| Target | Rate |
|--------|------|
| CD / internet | 44.1 kHz |
| **video / broadcast / film** | **48 kHz** (US film ±0.1%) |

- **No "generation loss" in digital** and **no benefit to up-sampling** past the
  original — pick the rate to match the delivery target.
- **16-bit minimum**; carry 24-bit only where a DAW's mixing math benefits.
- **Common clock** (word clock / video sync) prevents clicks; a **pitch shift on
  transfer = a sample-rate mismatch**, not a reason to fall back to analog.

## Gain-staging (the calibration ritual)

Each device has finite dynamic range — set levels so the signal sits in the sweet
spot. Raise input until the overload light flickers only on peaks; keep controls
**near midpoint** (a control far off midpoint signals a level-standard mismatch —
use an attenuator/buffer, don't just twist the knob). Diagnose noise by recording
**silence from the source**: noise there = the source; noise only in the file =
your digitizing/ground path (hum = ground loop, hiss = gain-staging).

**Don't normalize per-clip** — it shifts background levels clip-to-clip and ruins
a smooth mix.

## Metering and line-up tone

- **−20 dBFS @ 1 kHz** (broadcast/film; peaks ≤ −10 broadcast, ≤ −2 film) or
  **−12 dBFS** (prosumer/web).
- Analog **0 VU ≠ digital 0 dBFS** — digital has *no* headroom above 0; the
  standard maps digital −20 dBFS ↔ analog 0 VU.

## Timecode and the dropframe trap

- **Timecode (HH:MM:SS:FF)** is a frame *address* — it does **not** guarantee
  long-term sync; a **speed reference** (blackburst/word clock) does.
- **NTSC runs at 29.97 fps**, so **dropframe** timecode skips *numbers* (not
  frames) to stay wall-clock accurate — used for broadcast masters.
  **Non-dropframe** is fine for commercials/web. A **constant ~2 frames/min drift =
  30 fps audio against 29.97 fps NTSC.**
- **PAL = 25 fps, never dropframe.** Film = 24 (or 23.976) fps.

## Studio application

Provisional leads for the studio's sound layer:

- **This is the audio asset-ingest contract for the Production's output store.**
  Generated audio lands as **48 kHz, ≥16-bit** files (ch. 2), all-digital,
  line-up-aware — the conventions `cutter.py` reads and the pipeline validates
  (ch. 18).
- **Timecode-≠-sync + dropframe math is the timeline's coordinate system.** When
  `cutter.py` places audio against video it must respect the frame rate and the
  29.97/dropframe reality, or accrue exactly the ~2 frame/min drift Rose warns of.
- **Gain-staging + "no per-clip normalize"** become mixer invariants: set levels
  once against the −20 dBFS reference, preserve relative background levels across
  clips so the bed stays smooth (ch. 13, 17).
- **"Diagnose digital, don't fall back to analog"** is the debugging posture for
  the `SoundAnalyst`: a pitch/click artifact is a *rate/clock* bug to fix, not
  noise to mask.
