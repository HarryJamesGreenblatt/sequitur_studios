# Chapter 16 — Processing

> Abridged from Jay Rose, *Producing Great Sound for Film and Video* (4th ed.),
> Ch. 16.
> **Scope:** EQ, compression, reverb, and noise reduction — what each does, how it
> wrecks a track when misused, and the order to chain them. The processing
> primitives the `SoundEditor` / `ReRecordingMixer` own.

## Core idea

**Good processing is invisible** — it improves the message without the viewer
noticing. Two cautions frame everything: you **can't adjust a processor you can't
hear** (monitors, not headphones — ch. 11), and every effect can *wreck* a sound
(watch overload; work at 24-bit and dither down — ch. 2).

## The four tools

**Equalizer** — changes level around a frequency.
- *Peaking* (level/frequency/**Q** bandwidth), *shelving* (broad boost/cut),
  *filters* (high/low-pass, ~6 dB/oct), *parametric* (several bands).
- **Fix by cutting, not boosting:** if a voice is lost under music, **dip the music
  ~1.5–2 kHz** rather than boost the voice.
- Most useful work is **200 Hz–10 kHz**; above ~10 kHz is usually just noise.

**Compressor** — reduces dynamic range above a **threshold** at a **ratio**, with
**attack/release** and **makeup gain**. Gentle on film dialog, heavier for
broadcast/web. **Sidechains** enable a **de-esser** (high-freq-triggered) and
**ducking** (music dips when the narrator talks).

**Reverb** — algorithmic (flexible) or **convolution** (samples a real space).
**Reverb = distance, not size** — more reverb pushes a source *back* and **kills
intimacy**. Prefer **track-based** reverb so the tail decays past the last clip.

**Noise reduction** — gate/expander (below-threshold turndown) or **multiband**
("learn" a clean noise chunk, set per-band thresholds). Limits: if noise is near
dialog level it **can't be removed** cleanly; two gentle passes beat one
aggressive; **always keep the unprocessed version**.

## Chain order (it matters)

**EQ → compression** (EQ changes what's loud, then control it); **gate before
compressor**; **reverb after** to add room, **before** to color the source.
Cookbook recipes: voices = EQ + gentle compression; hard effects = EQ + compress +
gate; music = EQ only (compression kills its rhythm).

## Studio application

Provisional leads for the studio's sound layer:

- **These four tools are the `SoundEditor`/`ReRecordingMixer` primitive set** — a
  scoped vocabulary (like a grammar enum) the post roles wield, with the **chain
  order** as an encodable rule.
- **"Reverb = distance" closes the perspective loop.** ch. 6 set mic distance ↔
  presence at capture; here reverb sets it in *post*. Together they let the studio
  render a dry `SpeechRenderer` line (ch. 9) and **add scene-matched reverb to
  place it at the shot's distance** — audio perspective driven by *Grammar of the
  Shot*'s shot size, applied at both ends of the pipeline.
- **"Fix by cutting, not boosting" + "dip music under dialog" is the auto-balance
  rule** for keeping dialog intelligible — a `ReRecordingMixer` heuristic (the
  sidechain-duck is its automated form).
- **"Always keep the unprocessed version"** is the same non-destructive,
  keep-the-master discipline as ch. 2 and ch. 9 — processing is a reversible stage
  over preserved source audio in the Production's store.
