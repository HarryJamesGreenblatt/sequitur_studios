# Chapter 7 — Editing Terms, Topics, and Techniques

> Abridged from Christopher J. Bowen, *Grammar of the Edit* (4th ed.), Ch. 7.
> **Scope:** the working vocabulary beyond transitions — timecode, montage,
> parallel editing, multicam, compositing, **split edits (L/J-cuts)**, color
> grading, and **importing stills**. These are the techniques a future `movie.py`
> would implement; several connect directly to the studio's other layers.

## Timecode & frame rate

- **Timecode (TC)** = `HH:MM:SS:FR` — the clock the edit uses for playback and
  **sync**; picture and its audio share matching TC frame-for-frame.
- **Frame rates:** film 24, NTSC ~30 (29.97), PAL 25; progressive **24p/25p/30p**
  and high-frame-rate **48p/60p** now common. Mixed rates must be conformed.

## Structural techniques

- **Montage** — two senses: the *montage theory* (juxtaposition → new idea = the
  concept edit) and the **montage sequence** (quick music-backed clips condensing
  time — a highlight reel).
- **Parallel editing / cross-cutting** — intercut two plot lines happening
  simultaneously; **shorten the shots progressively** to build suspense toward a
  climax.
- **Multi-camera editing** — several cameras record the same action on one take
  with **shared timecode**, so a cut to any angle lands on a matching sync frame.
  Cut freely between angles like a live TV director.

## Layering techniques

- **Composite editing** — multiple video tracks on screen at once (split-screen,
  **picture-in-picture**, VFX); needs upper-track effects/keys + often a render.
- **Titles & graphics** — text/shapes on upper tracks over video (fill, stroke,
  lower-thirds); transparency via key/alpha.
- **Rendering** — bake complex composites/effects into a new flat media file for
  real-time playback; reverts if the source changes.
- **Green-screen chromakey / luma-key / alpha channel** — key out a color (green/
  blue) or super-black to layer a foreground over a background plate.
- **Video resolution** — pixel grid `W×H` (HD 1920×1080, UHD/4K 3840×2160, 8K);
  more pixels = more detail *and* more processing load.

## Split edits — L-cuts & J-cuts (the audio/picture offset)

Picture and sound are separate streams; offsetting their cut points is a **split
edit** (a.k.a. **lapping**). When both cut together it's a **straight/butt-cut**.

- **J-cut** — **sound leads picture**: you *hear* the new shot's audio before you
  *see* it (the cafeteria voice before you turn to look; the Ch. 5 sound bridge).
  Provides aural motivation to cut.
- **L-cut** — **picture leads sound**: the outgoing audio laps *under* the incoming
  picture (the bowling-yelp continuing over treetops).

Assembly/rough cuts are straight cuts; split edits are a **fine-cut** finesse,
especially for dialogue — they mimic how we hear-then-see in life.

## Sound as storytelling

Audio can reinforce the scene's reality, go **representational** (office noise
drops to internal music as medicine takes effect), or run a **sound metaphor**
against picture (a lion's roar over a "job hunt" in the city jungle). Continuity of
ambience across a cut is expected; breaking it draws negative attention.

## Finishing techniques

- **Color correction / grading** — the finishing pass: **correction** fixes wrong
  exposure/color (neutral grays, right flesh tones); **grading** applies a stylistic
  *look*. Work **luminance** (set-up/gain/gamma) then **chrominance** (hue/
  saturation). **Log/RAW** source holds the most gradeable data; scopes keep the
  signal legal.
- **Importing still images** — a still must be **crop/scaled to the video frame**
  (tiny web images scale badly) and is **replicated to a duration** (≈5s default),
  then trimmed; **alpha channel** (TIFF) preserves cut-out transparency.

## Studio application

Several of these are direct hooks for the future `movie.py` (provisional — no code
yet):

- **L/J-cuts are the audio-picture offset primitive for cut-to-cue.** A J-cut
  encodes "hear the next beat before you see it" — the machine form of the sound
  bridge from [Ch. 5](ch05-when-to-cut.md). An assembler that treats picture-cut and
  audio-cut as **independently offsettable** gets dialogue smoothing and aural
  motivation for free, and it dovetails with the **production-dialogue** thread.
- **Multicam + shared timecode is the model the studio *lacks* and may want.**
  Bowen's free cutting between angles depends on a **common timebase**. Omni
  generates each ~10s shot independently with **no shared clock**, so multicam-style
  cutting requires the studio to *time-align its coverage* (e.g. generate angles of
  the same beat against a shared reference) — a concrete design lead for the
  shots→scenes→acts generator.
- **"Importing stills" wires the `gpt-image` backend into the edit.** A generated
  still becomes a clip (crop-to-frame, hold ~5s, optional scale/reposition = a
  Ken-Burns move) — so the image backend feeds *both* production keyframes **and**
  post inserts/titles/cutaways.
- **Montage & parallel editing are ready-made sequence patterns** `movie.py` can
  offer (condense-time montage; suspense-building cross-cut with progressively
  shorter shots) — structural macros over the cut-decision engine.
- **Color grading is the deferred post pass** for the "fixable exposure/color"
  shots flagged in [Ch. 4](ch04-assessing-footage.md) — a post-layer operation, not
  a re-generation.
