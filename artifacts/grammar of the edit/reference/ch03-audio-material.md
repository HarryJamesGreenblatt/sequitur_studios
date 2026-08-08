# Chapter 3 — Understanding the Audio Material

> Abridged from Christopher J. Bowen, *Grammar of the Edit* (4th ed.), Ch. 3.
> **Scope:** the audio an editor works with — what is captured **in production**
> vs. built **in post**, the **diegetic / non-diegetic** split, sync discipline,
> and the dialogue-editing principles that make **sound a cut motivator**. This is
> the source for the studio's open **production-dialogue vs. post-soundtrack**
> question.

## Core idea

Sound moves audiences physiologically and emotionally — "silent" films never
were. Audio is not a garnish: a 15-second web video and a 62-track blockbuster
both live or die on how their tracks are built and mixed. For the studio the key
structural fact is **where each sound comes from**, because that decides which
phase owns it.

## Production audio (captured on the shoot)

| Source | What it is |
|--------|------------|
| **Dialogue** | On-screen talent's intelligible speech (scripted lines, monologue, direct-address host). The primary sync element. |
| **Room tone / NATS / ambience** | The location's constant "soundscape." **Room tone** = ~60s of the space held silent, recorded on set; used later to fill/even out dialogue beds. |
| **Wild sounds** | Non-sync recordings of specific things at the location (a door, a signal, birds) — between ambience and spot SFX. |
| **Source music** | Music actually performed/playing in the scene — **diegetic**, cut straight into the track. |

## Post-production audio (built in the edit)

Narration / **voice-over** (recorded after the rough cut, speaker unseen) ·
**ADR/looping** (re-recorded dialogue hand-synced over bad production audio) ·
**ambience / tonal tracks** (library beds or mood tones) · **SFX / spot effects**
(hand-synced object sounds) · **Foley** (performed footsteps/cloth/props to
picture) · **soundtrack** (licensed songs — *rights warning*) · **stings/stingers**
(short musical stabs marking a beat or a transition) · **score** (original music
composed to the picture).

## Diegetic vs. non-diegetic (the load-bearing distinction)

- **Diegetic** ("actual/literal") — caused by something *in the story world*
  (seen or unseen): dialogue, source music, NATS, Foley. Note: diegetic ≠
  production-recorded — a made-up creature's voice is diegetic yet fabricated; the
  rule is it must carry the *tone, presence, and perspective* of the thing on
  screen.
- **Non-diegetic** ("commentary") — has no source in the story world and no
  character can hear it: **score**, non-source soundtrack, tonal beds, VO
  narration. Purely for audience manipulation.

**Sound design** = the whole layered result. **Sound motifs** = a sting/effect
bound to a character/place, recurring to signal their presence.

## Sync discipline

- **Sync sound** = audio attributable to an on-screen source, kept frame-aligned
  to picture. Dual-system shoots record picture and sound separately and marry
  them via the **slate** clap (or **MOS** = shot with no sync sound).
- Trimming picture without its linked audio **slips sync** by exactly the frames
  added/removed — audiences hate out-of-sync as much as blur. Any duration change
  to picture must be mirrored on audio (ties back to picture-lock in
  [Ch. 1](ch01-the-editing-process.md)).

## Dialogue editing → sound as a cut motivator

The chapter's principles (PIP), which matter most for automated assembly:

- **Cut on vision *and* sound, not just line-ends.** Cutting only when a speaker
  finishes is predictable; a **reaction shot** during listening can carry more
  weight than the words. Dialogue must **not restrict cut-point placement**.
- **Pauses are content.** Don't auto-strip an actor's beats — use a pause as
  *motivation for a cutaway* (reaction/noddy). (Non-fiction may trim "um/ah" and
  mask the jump cut with B-roll.)
- **Clean audio under OTS/off-screen lines.** Lift a clean CU voice track for the
  back-to-camera/off-screen character rather than using the weak boom take.
- **No holes in the audio bed** — keep some clip (even room tone) on every frame;
  dead silence reads as a technical fault unless deliberate.
- **Sound can precede picture** at a program open to prime the imagination.

## Studio application

Directly grounds the studio's audio strategy (provisional — no code yet):

- **Phase ownership follows the diegetic split.** *Production* (Omni, which
  generates synced audio with its video) is the natural home for **diegetic sync
  sound — dialogue and ambience** captured *with* the shot. *Post* (`movie.py` +
  mix) owns **non-diegetic** layers — **score, soundtrack, stings, VO**. This
  resolves the brief's tension: keep well-informed **production dialogue**, treat
  the **soundtrack as a post decision** rather than throwing generated audio away.
- **The dialogue-capture aspiration is legitimate.** Bowen's model expects usable
  on-set dialogue; the studio should aim to *keep* Omni's diegetic dialogue and
  reserve overdub/TTS-style ADR as the *fallback* for a bad take — not the default.
- **"Cut on sound, not just line-ends" is the domain-knowledge alternative to a
  pure beat grid.** The prior music-video workflow drove edits from an audio
  envelope; this chapter gives a *content* motivator — reactions, pauses, motifs —
  so `movie.py` can align cuts to **narrative** cues, not only rhythmic ones (the
  two can compose: beat grid × reaction-availability).
- **Room-tone bed + sync rule are assembler invariants.** An automated stitcher
  must maintain an unbroken audio bed and re-align audio whenever it trims picture
  duration.
