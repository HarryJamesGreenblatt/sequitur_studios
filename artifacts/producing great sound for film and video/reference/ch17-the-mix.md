# Chapter 17 — The Mix

> Abridged from Jay Rose, *Producing Great Sound for Film and Video* (4th ed.),
> Ch. 17.
> **Scope:** mixing strategy — the fader as the primary tool, pre-dubs, spatial
> placement, and loudness/delivery standards. The `ReRecordingMixer` role's
> charter and the layer's final-output contract.

## Core idea

The mix is the one element that **spans the whole movie**, so mix it as a
**continuous whole**, not clip by clip. **A good mix hides imperfect elements; a
bad mix kills great ones.** And the discipline that makes it possible: **once you
set the monitor level, don't touch it** — ears adapt to a reference and judge
dynamics differently at other volumes.

## How to mix

- **The fader is the primary tool** — not rubber-band lines. Automation records and
  replays fader moves so you can concentrate on a few at a time.
- **Pre-dubs (pre-mixing):** with many tracks, blend by category first — a
  **dialog pre-dub** especially, so acoustic changes between shots (even shot on
  different days) can't be heard.
- **Mix "in the box":** the DAW multiplies each track by its fader value and sums.
  Watch the bus — **summed tracks are louder than any one alone**, so lower some as
  you raise others and **meter it** (loud monitoring masks distortion — ch. 2).

## Placing sounds (four levers + time)

| Lever | Effect |
|-------|--------|
| **Volume** | louder = closer |
| **EQ** | 1.2–2.5 kHz peak brings *forward*; HF loss = distance |
| **Reverb** | more = *farther back* (not bigger) |
| **Panning** | keep dialog/important effects **center**; spread music/ambience |

**Phantom center**: mono dialog panned center reads as coming from the screen
regardless of seat (theatrical uses a real center channel). Also mix in the **time
dimension** — don't let a voice's rhythm land exactly on the music's beats; slide
it a couple of frames (a ~60 ms delay ≈ 2 frames).

## Loudness and delivery (the output contract)

- **Broadcast: −24 LKFS ±2 dB** average per segment, momentary peaks ≤ −2 dBFS
  (ITU-R BS.1770 / EBU R128 / ATSC A/85; CALM Act mandates it). Use a **standards
  meter**, measure, and adjust.
- **Theatrical:** dialog ~−20 dBFS = 85 dB SPL on a calibrated stage.
- **Web/DVD:** dialog can run ~10 dB hotter (less headroom for peaks — watch
  distortion).
- Deliver **stems** (dialog / music / effects) and **24-bit / 48 kHz** masters.

## Studio application

Provisional leads for the studio's sound layer:

- **This is the `ReRecordingMixer` role's charter.** Mix as a continuous whole,
  fader-first, pre-dub by category (dialog first), guarantee bus headroom — the
  behavior the role encodes over the Production's stems.
- **The four placement levers + phantom center are the auto-mix's spatial model**,
  and they unify the pipeline's perspective story: **volume/EQ/reverb = distance =
  shot size** (ch. 6, 16), **pan = keep dialog center** (ch. 4). Placing a sound is
  choosing values on these axes to match the framing.
- **−24 LKFS / peaks ≤ −2 dBFS / 48 kHz / 24-bit + stems is the concrete delivery
  spec** the `SoundAnalyst` validates and the mixer targets (ch. 11, 18) — the
  measurable definition of "done."
- **Stems = the diegetic/non-diegetic split, delivered.** Emitting D/M/E keeps
  production dialog separable from post soundtrack — the studio's answer to the
  open **production-dialogue vs. post-soundtrack** question, now a mixer output.
- **Mix automation as recorded control-points-over-time** is the data model that
  makes simultaneous fader moves (ch. 11) tractable for an agent.
