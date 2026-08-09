# Producing Great Sound for Film and Video — grounding index

Jay Rose, *Producing Great Sound for Film and Video* (4th ed.), Focal Press /
Routledge, ISBN `978-0-415-72207-0`. This is the studio's **sound-craft**
grounding — the film-sound department source that sits alongside the taxonomy from
[*Grammar of the Edit* Ch. 3](../grammar%20of%20the%20edit/reference/ch03-audio-material.md)
and the score/MIR capability of the **toaster-strudel** MCP server. Together those
three form the **composite grounding** for the studio's sound layer.

> **No code layer exists yet.** The sound layer is **designed** (devlog
> [`0009-the-sound-layer.md`](../../context/storyline/0009-the-sound-layer.md)) but
> **not built** — `SpeechRenderer` builds first. The "role" column below therefore
> points at the *intended* sound roles (`SoundMixer`/`Boom`, `SoundDesigner`/
> `SoundEditor`, `Composer`, `ReRecordingMixer`, `SoundAnalyst`) and every
> reference's **Studio application** section is a **provisional lead** to be
> reconciled once those analogues are implemented. See
> [`../../context/architecture.md`](../../context/architecture.md) for how the
> department maps to workflow phases.

## Why Rose (and not Yewdall)

Yewdall's *Practical Art of Motion Picture Sound* was evaluated and **rejected** —
too anecdotal (a practitioner memoir, poor signal-to-noise for grounding). Rose is
occasionally anecdotal but is **structured, technical, and phase-organized**, which
suits per-role extraction. Extract chapters **on demand per role**, not all 18 at
once.

## Folder layout

- [`extraction/`](extraction/) — the raw `.docx` originals + `media/` (as imported).
- [`source/`](source/) — pandoc-converted verbatim Markdown, the **ground truth**.
- [`reference/`](reference/) — abridged, session-ready references (what agents load).

> **Naming:** source and reference files use the same descriptive
> `chNN-<slug>.md` scheme as the two Bowen books (normalized from the original bare
> `chNN.md` during this abridgement pass).

## Chapter → (planned) role/concern map

Rose organizes the book in four sections: **Audio Basics** (1–3), **Planning &
Pre-pro** (4–5), **Production Sound** (6–9), and **Postproduction** (10–18).

| Chapter | Covers | Planned sound-layer concern |
|---------|--------|-----------------------------|
| [Ch. 1 — How Sound Works](reference/ch01-how-sound-works.md) | pressure waves, frequency/harmonics, envelope, inverse-square, phase | physics basis of `SoundAnalyst` (MIR) + presence-per-shot-size |
| [Ch. 2 — How Digital Audio Works](reference/ch02-how-digital-audio-works.md) | sampling, bit depth, dBFS/clipping, sample rate, dither, codecs | `SpeechRenderer` output contract (48 kHz / ≥16-bit); asset formats |
| [Ch. 3 — Audio on a Wire](reference/ch03-audio-on-a-wire.md) | analog levels, balanced wiring, digital connectors | boundary of the execution plane (hardware; thin tie) |
| [Ch. 4 — Planning for Sound](reference/ch04-planning-for-sound.md) | elements of a track; assembly order; leave room | the sound dept **data model** + diegetic split (dialog/music/SFX/silence) |
| [Ch. 5 — Budgeting, Scheduling, Pre-production](reference/ch05-budgeting-scheduling-preproduction.md) | costs, time budgets, location scouting, Golden Triangle | **Producer (HITL)** resource decisions; sync-strategy-up-front |
| [Ch. 6 — Microphones and Room Acoustics](reference/ch06-microphones-and-room-acoustics.md) | polar patterns, off-axis coloration, elements, room treatment | `SoundMixer`/`Boom` mic-choice; audio perspective ↔ shot size |
| [Ch. 7 — Production Mic Technique](reference/ch07-production-mic-technique.md) | boom/lav/wireless; **dual-mic, choose in post** | `SoundMixer`/`Boom` capture; the **keep-take-vs-ADR** seam |
| [Ch. 8 — Production Recording](reference/ch08-production-recording.md) | double-system, levels, reference-track & slate sync | capture pipeline; sync = `SoundAnalyst`; level calibration |
| [Ch. 9 — The Voice-Over (+ ADR, Effects)](reference/ch09-the-voice-over.md) | VO recording, ADR matching, Foley/ambience/vocal FX | **`SpeechRenderer` craft brief**; diegetic-vs-TTS fallback |
| [Ch. 10 — Postproduction Workflow](reference/ch10-postproduction-workflow.md) | NLE vs DAW, interchange, handles, priority order | `edit.py`/`cutter.py` audio sequence; stems; handle padding |
| [Ch. 11 — Postproduction Hardware](reference/ch11-postproduction-hardware.md) | monitoring, metering, line-up tone, sync infra | "meter is ground truth" → `SoundAnalyst`; mostly hardware |
| [Ch. 12 — Levels and Digitizing](reference/ch12-levels-and-digitizing.md) | ingest, gain-staging, sample rate, timecode/dropframe | audio asset-ingest contract; timeline coordinate system |
| [Ch. 13 — Editing Voices](reference/ch13-editing-voices.md) | phoneme editing, sync rules, breath/click removal, room tone | `SoundEditor` dialog edit; **cut-to-cue** invariants; room-tone bed |
| [Ch. 14 — Working with Music](reference/ch14-working-with-music.md) | sourcing, licensing traps, beat-based editing | `Composer` + **toaster-strudel MCP** beat grid; rights metadata |
| [Ch. 15 — Sound Effects](reference/ch15-sound-effects.md) | reality vs punctuation, sourcing, sync, layering | `SoundDesigner`; diegetic/non-diegetic in effect form |
| [Ch. 16 — Processing](reference/ch16-processing.md) | EQ, compression, reverb, noise reduction, chain order | processing primitives; **reverb = distance** closes perspective loop |
| [Ch. 17 — The Mix](reference/ch17-the-mix.md) | fader-first mixing, pre-dubs, placement, loudness standards | `ReRecordingMixer` charter; **−24 LKFS** delivery; D/M/E stems |
| [Ch. 18 — "Help! It Doesn't Sound Right!"](reference/ch18-help-it-doesnt-sound-right.md) | production/post/edit/mix troubleshooting FAQ | sound-layer **`validate()`** diagnostic checklist |

## Scope note

Rose grounds the **sound department across two phases** — *production* (capture:
Ch. 6–9) and *post* (assembly & mix: Ch. 10–18) — making it the studio's first
explicitly **multi-phase** grounding source. It is deliberately **composite**:

- **[*Grammar of the Edit* Ch. 3](../grammar%20of%20the%20edit/reference/ch03-audio-material.md)**
  supplies the **taxonomy** (diegetic / non-diegetic, production vs. post) that
  Rose's chapters populate with craft.
- **toaster-strudel** (MCP) supplies the **score renderer + MIR** the `Composer`
  and `SoundAnalyst` drive — Ch. 14's beat-based editing is where that seam pays
  off.
- **Rose** supplies the **capture, editing, processing, and mix craft** the roles
  wield.

The recurring through-line is **audio perspective ↔ shot size**: mic distance and
pattern (Ch. 6), capture technique (Ch. 7), and reverb/EQ/level in the mix
(Ch. 16–17) all set how *close* a sound feels — coupling the sound layer to
[*Grammar of the Shot*](../grammar%20of%20the%20shot/INDEX.md)'s framing, and
feeding the open **cut-to-cue** and **production-dialogue vs. post-soundtrack**
problems recorded in
[`../../context/architecture.md`](../../context/architecture.md).
