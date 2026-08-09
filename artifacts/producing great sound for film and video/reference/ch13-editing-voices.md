# Chapter 13 — Editing Voices

> Abridged from Jay Rose, *Producing Great Sound for Film and Video* (4th ed.),
> Ch. 13.
> **Scope:** the phonetics of cutting dialog invisibly — where edit points hide,
> the sync rules, breath/noise removal, and the room-tone bed. The `SoundEditor`'s
> core craft, and the chapter that most directly grounds **cut-to-cue**.

## Core idea

Good dialog editing is **transparent**: you change the performance or the length
without it sounding "edited." That requires knowing **phonetics** — how the mouth
forms individual sounds — because you cut *between phonemes by ear*, not between
words by eye (waveform blobs lie).

## The sync invariant

**Sound early is disturbing; sound late is tolerated.** Light is effectively
instant and sound takes time, so viewers accept audio a touch late but reject it
**even one frame early**. (Sync a slate to the **last blurred frame** before the
sticks meet.)

## Phoneme-based editing

| Family | Behavior | Edit value |
|--------|----------|-----------|
| **Fricatives** (/s/ /f/ /sh/) | air-friction hiss | easy to *spot* while scrubbing |
| **Plosives** (/b/ /p/ /t/ /k/) | tiny silence + burst | the burst **masks** an edit |
| **Voiced vs. unvoiced** | vocal-cord buzz vs. pure air | **unvoiced consonants swap across actors; voiced can't** |

Three rules: **(1)** never cut *into* a continuous sound (vowel, sustained
fricative, breath); **(2)** you *can* cut from a soft continuous sound into a
**hard attack** (the burst hides the join); **(3)** you can almost always cut from
the **start of a sound to the start of the same sound** in another word.

## Breaths, clicks, room tone

- **Breaths:** replace with **two-thirds of their original length** (an empirically
  verified ratio) to keep natural pacing; on-camera, duck ~6 dB rather than delete
  (a full hole shows a moving mouth with no sound).
- **Clicks/glottal shocks:** never erase (destroys rhythm) — copy an adjacent vowel
  and **replace** over the click.
- **Room tone:** the unbroken bed. Record 30 s on set; harvest from pauses; or
  *manufacture* it (convolution reverb seeded with location tone → infinite
  non-repeating background). **No frame should be dead silent** unless deliberate.
- **Track-splitting:** separate characters/mics onto their own tracks, hide timbre
  shifts with overlaps and short crossfades, preset EQ/level per track.

## Studio application

Provisional leads for the studio's sound layer:

- **"Sound early is disturbing" is a hard cut-to-cue invariant.** The Editor's
  audio-driven cut engine may place a cut *late* relative to a sound cue but must
  **never** place picture/sound early — a one-sided tolerance the `SoundAnalyst`→
  Editor path must enforce.
- **Phoneme families are the alphabet of an audio-aware cut engine.** "Cut on a
  hard attack (plosive burst masks the join)" and "match phoneme starts" are
  concrete, detectable rules the `SoundAnalyst` can surface so the Editor cuts on
  *content*, not just a beat grid — the domain alternative to a pure envelope
  edit, echoing *Grammar of the Edit* Ch. 5's cut motivators.
- **The room-tone bed is an assembler invariant** (as in *Grammar of the Edit*
  Ch. 3): the mixer keeps some signal — even manufactured tone — under every
  frame; dead silence reads as a fault.
- **Two-thirds breath replacement + "replace, don't cut"** are the kind of exact,
  encodable heuristics `HeuristicJudgment` can carry for the `SoundEditor` role
  before any LLM persona.
