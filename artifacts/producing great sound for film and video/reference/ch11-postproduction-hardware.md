# Chapter 11 — Postproduction Hardware

> Abridged from Jay Rose, *Producing Great Sound for Film and Video* (4th ed.),
> Ch. 11.
> **Scope:** the edit suite — monitoring, D/A conversion, metering, and sync
> infrastructure. Mostly physical, but it establishes one software-relevant
> principle: **your meter/monitor is your ground truth.**

## Core idea

**You can't make a decision you can't hear.** The monitor chain — *room acoustics
first, then speakers* — matters more than any plug-in, and **headphones are too
detailed for mixing** (subtle mixes don't translate). **Detail matters more than
expense.**

## Monitoring

- **Room acoustics dominate.** Reflections cancel/reinforce frequencies
  unpredictably and you can't EQ them away per seat. Treat cheaply with
  Owens-Corning #703 fiberglass panels at side/rear, ear level.
- **Speakers:** avoid "flattering" ones (extra bass, scooped mids). Trust specs
  only if they state **±dB within a range** ("30 Hz–22 kHz" alone is meaningless);
  ±3 dB is reliable. Set tweeters at ear level in an equilateral triangle.
- **Phantom-center stereo is enough** unless you're actually mixing surround;
  don't confuse satellite/sub systems (which split at speech frequencies) with a
  proper 5.1 sub.

## Metering and line-up

- Peak-reading and **loudness meters** (free: Orban Loudness Meter, T-RackS,
  Audacity) are reliable on a digital input; a plain voltmeter-style "VU" can't
  catch digital peaks.
- **Line-up tone:** **−20 dBFS @ 1 kHz** (pro/film), **−12 dBFS** (prosumer/web) —
  the reference every device and delivery is aligned to.
- **Control surfaces** (motorized fader boxes) beat mouse-only "rubber-band"
  automation because film mixes need **simultaneous** fader moves.

## Wiring infrastructure (reference-only)

Balanced wiring for noise rejection; isolation transformers or a single-end shield
for ground loops; **word clock / blackburst** as the master timing reference;
keep **timecode (LTC)** — a ~2.4 kHz chirp — away from audio cabling.

## Studio application

Provisional leads for the studio's sound layer:

- **"The meter/monitor is ground truth" is the `SoundAnalyst`'s reason to exist.**
  An automated pipeline has no ears, so it must *measure* — a calibrated
  **loudness meter** (LKFS, ch. 1/17) is the analyst's instrument, and **−20 dBFS
  line-up** is the reference it validates against. This is the software residue of
  an otherwise hardware chapter.
- **"You can't decide what you can't hear" ⇒ every audio judgment needs a
  measurable signal.** Cut-to-cue, auto-balance, and mix validation all depend on
  the analyst turning sound into numbers the heuristic layer can act on.
- **Simultaneous-fader-moves** motivates keeping mix automation as *data* (control
  points over time), not one-at-a-time edits — the model ch. 17 uses.
- Speaker/room/wiring specifics are **reference context** for human/persona
  judgment, not computed by the code.
