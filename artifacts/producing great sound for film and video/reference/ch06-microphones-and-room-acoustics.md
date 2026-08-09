# Chapter 6 — Microphones and Room Acoustics

> Abridged from Jay Rose, *Producing Great Sound for Film and Video* (4th ed.),
> Ch. 6.
> **Scope:** how mics actually behave (polar patterns, off-axis coloration,
> element types) and how rooms fight you. The physical basis for choosing a mic
> and getting it close — the core of the `SoundMixer`/`Boom` role's craft.

## Core idea

**What you hear is not what the mic gets.** Two facts drive every choice: a
directional mic **doesn't zoom** — it only makes off-axis sound *softer* and
**changes its timbre** (off-axis coloration); and **there is no telephoto mic** —
every mic is wide-angle, so you must get **close**. "Reach" just means low enough
self-noise to amplify a distant source before hiss becomes annoying.

## Polar patterns

| Pattern | Behavior | Best for |
|---------|----------|----------|
| **Omni** | equal all directions; a lav near the mouth wins via inverse-square | lavs, ambience, wind |
| **Cardioid** | heart-shaped; rear only ~−15 dB and *tubbier* | aim the null at a noise source |
| **Hypercardioid** | more directional, small rear lobe | **best for most interiors** |
| **Shotgun** | interference tube; side slots pick up **echoes** → hollow indoors | exteriors, treated rooms |

The key working rule: **hypercardioid beats shotgun in an untreated interior**,
because a shotgun's side slots collect reflections and sound hollow. Off-axis
rejection is frequency-dependent, so rejected sound is also *colored*, not just
quieter.

## Elements and power

- **Dynamic**: rugged, handles loud SPL, less sensitive; no phantom path.
- **Condenser**: most film mics; needs power (**P48 phantom** over balanced lines);
  **electret** = cheaper permanently-charged variant.
- **Modular** bodies (Sennheiser K6, Schoeps CMC) swap heads like camera lenses.

**Proximity effect:** directional mics boost bass as they get closer (announcers
exploit it; watch popping on plosives at close range).

## Rooms

The brain filters room acoustics after a few minutes; **the mic never does**, so
a home-video track sounds awful on playback. Foam tiles **absorb reflections**,
they don't **soundproof** (mass stops noise; absorption stops echo). Test with the
**foam "ahh" test**; improve by **position** (distance + angle + absorption +
diffusion) before reaching for treatment (blankets, #703 fiberglass, diffusion
from road cases at random angles).

## Studio application

Provisional leads for the studio's sound layer:

- **This is the grounding for `SoundMixer`/`Boom` mic-choice judgment.** "Get
  close, hypercardioid indoors, aim the null at noise" is the heuristic the role
  encodes; the polar-pattern table is its decision vocabulary (a scoped enum the
  role owns, in the crew-engine sense).
- **Off-axis coloration + proximity effect + reverb-with-distance give the studio
  its "presence per shot size" model.** A close-up ⇒ close, dry, bass-forward,
  intimate; a wide shot ⇒ more room and distance. That maps mic behavior onto
  *Grammar of the Shot*'s shot sizes, so audio perspective and framing stay
  coupled — a shot's "sound" is part of its grammar.
- **"A mic doesn't hear like a human" is the caution for generated audio too:**
  whatever the renderer produces must carry the *intended* room, not an incidental
  one — acoustic intent is a parameter, not an accident (ch. 5, 16).
- Mic model names and prices are **reference context** for persona/human judgment,
  not computed values.
