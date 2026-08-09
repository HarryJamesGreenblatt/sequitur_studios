# Chapter 18 — "Help! It Doesn't Sound Right!"

> Abridged from Jay Rose, *Producing Great Sound for Film and Video* (4th ed.),
> Ch. 18.
> **Scope:** a troubleshooting FAQ across production, post, editing, and mix —
> symptom → cause → fix. Read as the **diagnostic checklist** for a `validate()`
> pass over the sound layer.

## Core idea

Most "it sounds wrong" problems are a **short list of known causes with known
fixes** — and the cheapest fix is almost always *upstream* (on set, not in post).
The value here is a symptom→cause map you can run as checks.

## Production

| Symptom | Cause → Fix |
|---------|-------------|
| Wireless hiss/dropouts | weak batteries; antenna → fresh cells, line-of-sight, orient to transmitter |
| **Hum/buzz** | ground loop / AC pickup → XLR balancing adapter, Star-Quad, cable away from power, isolation transformer or battery |
| Background noise | mic too far → **get closer**; turn off HVAC/fridge/fans |
| **Echoey dialog** | mic too far indoors → treat room **and** get the mic close; boom ~1 ft above, aimed at mouth; never back the mic off to beat ALC |

## Post and editing

| Symptom | Cause → Fix |
|---------|-------------|
| **Constant ~2 frame/min drift** | 30 fps audio vs **29.97 fps NTSC** → fix frame-rate handling (ch. 12) |
| Wild jumps after minutes | dropped frames / hardware → defragment, quit apps |
| Single-system **consistently early** | camera delays video but not its audio → measure slate offset, slide tracks |
| Hum/noise in NLE | re-ingest at **≥16-bit / 48 kHz**; check connections |
| Music edits jumpy | NLE frame-locked (1/30 s is huge for music) → cut in an audio program (ch. 14) |
| Elements vanish in mono/TV | out of phase → check cables; invert one channel |

## Mix and delivery

- **Music too soft/loud, dialog fine** → you mixed on speakers that emphasize
  extremes or in a bad room → **remix on good monitors** (ch. 11).
- **Broadcast loudness rejected** → NLE meters don't qualify → use a **standards
  meter**, hit **−24 LKFS ±2**, peaks ≤ −2 dBFS (ch. 17).
- **Line-up tone must match average program level** — cable/net systems trust the
  tone: **−20 dBFS** (digital) / **−12 dBFS** (miniDV).

## Recurring gotchas

**Reverb = farther, not bigger** (kills intimacy) · there's **no standard "how
loud"** for non-dialog elements — mix by ear against dialog · **temp music must be
replaced** before any public showing · **fair use ≈ none** for licensed music.

## Studio application

Provisional leads for the studio's sound layer:

- **This chapter is the spec for a sound-layer `validate()`** — the analogue of the
  edit layer's `timeline()/validate`. The symptom→cause tables become **automated
  checks** the `SoundAnalyst` runs before delivery: sample rate/bit depth = 48 kHz/
  ≥16-bit, frame-rate/dropframe sanity (no ~2 frame/min drift), phase/mono
  compatibility, **−24 LKFS** loudness, peaks ≤ −2 dBFS, unbroken room-tone bed,
  no clipping.
- **"Cheapest fix is upstream"** is the pipeline's ordering wisdom: validate and
  correct at *capture/ingest* (ch. 8, 12), because post-hoc repair is costlier and
  worse — the software echo of "fix it on set."
- **Phase / mono-compatibility check** is a concrete, encodable rule (an element
  that vanishes in mono is out of phase) the analyst can flag automatically.
- Together with the delivery spec in ch. 17, this closes the loop: the layer
  **knows when a track is done and correct**, not merely rendered.
