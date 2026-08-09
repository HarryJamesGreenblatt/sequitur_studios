# Chapter 9 — The Voice-Over (and ADR, and Effects)

> Abridged from Jay Rose, *Producing Great Sound for Film and Video* (4th ed.),
> Ch. 9.
> **Scope:** recording voice-over in a controlled space, replacing dialog (ADR),
> and building effects (Foley, ambience, vocal FX). **The single most direct
> grounding for the studio's `SpeechRenderer` and the diegetic-vs-TTS fallback.**

## Core idea

Voice recording is easier than shoot sound because you control the room — and it's
a **performance** job, judged by the **ear, not the eye** (Rose's story: a director
who "heard" the wrong voice because the talent didn't *look* the part). Directing
voice is coaching, not cinematography.

## Engineering a voice recording

- **Room:** kill echo (the "UCK!" bark test); a short same-timbre echo is fine, a
  long hollow one is not. High-pass to tame rumble.
- **Mic:** a **mid/large cardioid** or **short shotgun/hypercardioid ~6–7" off the
  mouth**, condenser over dynamic. Avoid lavs (too omni, pick up echo).
- **Chain stays simple:** no ALC, **no EQ/compression while recording** (those are
  irreversible; decide them in post with full context), no "enhancer" boxes.
- **Script stand + stool + room-temp water** — non-obvious but they shape breath,
  sibilance, and mouth clicks.
- **Record everything, slate every take, don't rehearse the full read** (first
  takes yield usable phrases later).

## ADR (dialog replacement) — the fallback

ADR is **"not automatic and not perfect"** — Hollywood does it constantly and it's
often noticeable. Two engineering goals:

1. **Match the original** mic type, angle, and distance — a close VO mic over
   original wide dialog *won't* match projection or room.
2. **Cue the talent** — *picture-dominant* (streamer, actor watches the mouth) or
   *sound-dominant* (three beeps, then speak in unison with the looped line).

Best practice: record in a **dead room and add digital reverb** matching the
original space. **Don't over-obsess** — if the critical consonants land in sync,
software can nudge word timing and pitch the rest.

## Effects

Record effects **loud**, **mono**, and **dry** (echo rarely fits the target
scene). **Foley** = performing actions to picture in real time; **ambiences** =
≥1 min of continuous background (longer if it has voices, so loops aren't
obvious). **Vocal effects** exploit envelope and pitch — a >octave shift
dehumanizes; envelope tricks turn breath into machines.

## Studio application

Provisional leads for the studio's sound layer:

- **This chapter is the `SpeechRenderer`'s craft brief.** The raw renderer
  (Azure Speech text→wav) needs no grounding; the **quality lift** — SSML prosody,
  "no processing baked in," matching presence/room to the shot, session-style
  direction — attaches to the **`SoundMixer` role** that wields it. Record dry and
  clean; add room/reverb to *match the scene* downstream (ch. 16).
- **ADR-matching is the technical spec for the diegetic-vs-TTS fallback.** When the
  studio substitutes a TTS line for a bad generated take, it must **match the
  original's perspective** (mic distance, room reverb) or the swap will read as
  wrong — the "keep diegetic dialogue, TTS as fallback" decision from `0007` made
  concrete. Dead render + scene-matched reverb is the recipe.
- **"No EQ/compression while recording; decide in post"** is a pipeline rule:
  `SpeechRenderer` emits **clean, unprocessed** audio; processing is a separate,
  reversible stage owned by the `SoundEditor`/`ReRecordingMixer`.
- **Foley/ambience/vocal-FX technique grounds the `SoundDesigner`** (ch. 15
  develops it) — record loud/mono/dry, build ambience beds long enough to avoid
  audible loops.
