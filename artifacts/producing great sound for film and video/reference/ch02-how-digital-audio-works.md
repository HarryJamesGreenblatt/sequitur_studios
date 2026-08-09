# Chapter 2 — How Digital Audio Works

> Abridged from Jay Rose, *Producing Great Sound for Film and Video* (4th ed.),
> Ch. 2.
> **Scope:** sampling, bit depth, dynamic range, sample rate / Nyquist, dBFS and
> clipping, dither, and data reduction (lossless vs. lossy). The format facts that
> pin down what a renderer must emit and what an asset pipeline must preserve.

## Core idea

Digital isn't magically better than analog — **system design decides quality**.
What digital *does* give you is **perfect copies** (analog accumulates noise every
generation) and **graceful error handling** (small errors reconstructed, large
ones hidden rather than mangled). The engineering is choosing enough resolution
that the format never becomes the weak link.

## Bit depth = dynamic range

Each bit ≈ **+6 dB** of range (loudest to noise floor).

| Depth | Values | Range | Use |
|-------|--------|-------|-----|
| 8-bit | 256 | 48 dB | AM-radio quality |
| 16-bit | 65,536 | 96 dB | **CD / broadcast standard** |
| 24-bit | 16.7 M | 144 dB | professional; margin for mixing math |

**Practice:** record/edit at **24-bit** if storage allows, output **16-bit with
dither**. Gear advertising "24-bit" rarely resolves past ~15–18 bits because the
*analog* front end is the real limit.

- **dBFS** (decibels Full Scale): 0 dBFS = every bit on. You **cannot record past
  0 dBFS** — trying to flat-tops the wave = **clipping** (unfixable distortion).
- **Dither**: a tiny amount of random noise (~⅓ LSB) added *when reducing bit
  depth*, recovering sub-bit detail without raising the noise floor. Only dither
  when down-converting.

## Sample rate = frequency ceiling (Nyquist)

Highest reproducible frequency = **½ the sample rate**; anything above **aliases**
into false tones, so an anti-alias filter must block it.

| Rate | Nyquist | Use |
|------|---------|-----|
| 44.1 kHz | 22 kHz | **CD / internet** |
| 48 kHz | 24 kHz | **professional film / broadcast** |
| 96–192 kHz | 48–96 kHz | pro capture; practical benefit debated |

There's **no "generation loss" in digital** and no gain from up-sampling — a
44.1 vs 48 kHz choice is about matching the delivery target, not quality.

## Data reduction

- **Lossless** (FLAC, ALAC): ~40–60% smaller, bit-perfect on decode.
- **Lossy** (MP3, AAC): perceptual coding exploits **masking** (a loud tone hides
  softer nearby tones). AAC ~30% more efficient than MP3.
- **Never re-encode lossy → lossy** (damage multiplies). Decode → work →
  re-encode once, and **always keep an uncompressed master.**

Loudness metering here too: **K-weighting / LKFS** is the broadcast loudness
measure; **dialnorm** is Dolby's embedded loudness metadata.

## Studio application

Provisional leads for the studio's sound layer:

- **This chapter fixes the `SpeechRenderer` output contract.** Azure Speech →
  emit **48 kHz PCM WAV** (video/broadcast standard) so TTS lines drop straight
  onto the timeline; keep an uncompressed master and reserve MP3/AAC for delivery
  only. 16-bit is sufficient for voice; carry 24-bit only where later mixing math
  benefits.
- **"System design decides quality" is the whole renderer-seam thesis.** The
  grammar/decision plane stays model-agnostic; whether a backend sounds good is a
  property of that backend, not the grammar — exactly the argument that let
  `ImageStudio` be a non-Google renderer.
- **Clipping and the 0 dBFS ceiling are hard invariants for the mix.** The
  `ReRecordingMixer` must guarantee headroom on the summed bus (ch. 17); no amount
  of downstream cleverness recovers a clipped render.
- **Never-re-encode-lossy** is an asset-pipeline rule: intermediate audio artifacts
  in the Production's output store stay uncompressed until final delivery.
