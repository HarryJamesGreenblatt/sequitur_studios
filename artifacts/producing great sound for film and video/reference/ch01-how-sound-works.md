# Chapter 1 — How Sound Works

> Abridged from Jay Rose, *Producing Great Sound for Film and Video* (4th ed.),
> Ch. 1.
> **Scope:** the physics an audio decision rests on — pressure waves, frequency
> and harmonics, the envelope, loudness-vs-level, the speed of sound, phase, and
> directionality. This is the layer of hard facts every later chapter (and every
> studio sound role) reasons over.

## Core idea

Sound is **changes in air pressure** propagating as a wave — compressions and
rarefactions spreading spherically. You can't aim it like light. Two consequences
dominate the craft: sound **bounces** (reflections degrade a track) and sound
**spreads** (it gets predictably quieter with distance). Everything else is
detail on top of those two facts.

## The inverse-square law (the load-bearing rule)

Intensity drops **6 dB every time the distance doubles** (~9.5 dB when it
triples). This is the single most useful lever in production sound: to beat noise,
get the mic **much closer to the wanted source than to the noise** — a mic 1 ft
from a mouth and 8 ft from an air conditioner hears the voice ~18 dB hotter than
the noise, for free.

## Frequency, harmonics, envelope

| Concept | Fact |
|---------|------|
| Hearing range | ~20 Hz–20 kHz; the *useful* speech band is ~350 Hz–3.5 kHz |
| Pure tone | a single-frequency **sine wave** |
| **Harmonics** (overtones) | integer multiples of the fundamental — they define *timbre* (why an oboe ≠ a violin at the same pitch) |
| Intelligibility floors | telephone survives on a 3.5 kHz cutoff; dialog is identifiable by ~7.5 kHz |
| **Envelope** | the loudness *shape* over time (attack→decay). A trumpet's attack is ~0.03 s ≈ one video frame; a clarinet's is slow |

**Edit envelopes, not words.** Speech elides — words blur into each other, so you
can't mark cut points by looking at a waveform. You find edit points *by ear*
(ch. 13 builds the whole discipline on this).

## Loudness ≠ level

The **decibel** is a logarithmic *ratio*, not an absolute. Ears judge ratios and
constantly recalibrate to context, so **a meter cannot measure perceived
loudness** — that needs loudness-weighted metering (LKFS / EBU R128; the CALM Act
mandates it for broadcast, ch. 17). Doubling voltage/pressure = **+6 dB**.
Perceived loudness depends on frequency (ears are most sensitive ~2–4 kHz),
duration/density, and surrounding context.

## Speed, delay, phase

- Sound travels ~1,087 ft/s → roughly **1 ms per foot**. A source 10 yards off
  arrives ~1 frame late; sync that's 3 frames late reads as wrong.
- **Echo** = a single reflection ≥0.1 s later; **reverberation** = dense random
  bounces. Reflections arriving out of phase with the direct sound **cancel**
  frequencies (comb filtering) — position-dependent, with no universal fix.

## Directionality

- **High frequencies are directional** (short wavelengths); **lows are nearly
  omnidirectional** (a subwoofer's placement barely matters).
- Mono routed to two channels is **not** stereo. Theatrical mixes anchor dialog to
  a **center channel** so voices come from the screen regardless of seat (ch. 17).

## Studio application

Provisional leads for the studio's sound layer (designed, not yet built):

- **The inverse-square law is the physical basis of `SoundMixer` presence
  judgment.** "Presence per shot size" — a close-up wanting intimate, dry, hot
  dialog vs. a wide shot wanting more room — is just the mic-distance ↔ level/
  reverb trade-off, and it composes directly with *Grammar of the Shot*'s shot
  sizes.
- **Loudness ≠ level ⇒ the `SoundAnalyst` (MIR sensor) must measure perceived
  loudness, not peaks.** A peak meter is the wrong instrument for cut-to-cue or
  auto-balance decisions; the analyst needs LKFS-style weighting (ch. 11, 17).
- **Timbre = harmonics ⇒ audio is a first-class signal for the cut engine.**
  Frequency/envelope content is what makes "cut on a hard attack" (ch. 13) and
  beat detection (ch. 14) possible — the `SoundAnalyst` feeds these to the
  Editor's cut-to-cue.
- **"Edit by ear, waveforms lie"** is a caution for any automated assembler: the
  envelope, not the visual blob, marks the real edit point.
