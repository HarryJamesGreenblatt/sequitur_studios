# 0010 — Unpacking the Rose: the sound craft source, abridged

> Date: 2026-08-08 · Focus: execute the deferred abridgement of **Jay Rose,
> *Producing Great Sound for Film and Video* (4th ed.)** — the craft source staged
> in `0009` — into 18 session-ready `reference/` chapters + a source `INDEX.md`.
> This is a **grounding** entry (transformative text only); no sound code was
> built. It completes the third full source in the library.

## What happened

`0009` designed the sound layer and *staged* Rose (extraction present) but left the
18-chapter abridgement to "its own session." This is that session.

1. **Recovered `CH-06`.** One extraction file (`CH-06.docx`) failed to convert: it
   was a **misnamed OLE2 `.doc`** (Word 97–2003 binary, `D0 CF 11 E0` signature),
   not a real `.docx` zip — pandoc can't read it. The user re-supplied a valid
   `.docx` (now `PK` zip signature); converted with the same
   `pandoc --wrap=none --extract-media` settings as the other 17, so the `source/`
   ground truth is complete (18/18).

2. **Fixed the naming disparity (user directive).** Rose's `source/` files were
   bare `chNN.md`, while both Bowen books use descriptive `chNN-<slug>.md`.
   Normalized **both** `source/` and `reference/` to the slug scheme (titles
   pulled from the chapter heads), so all three sources now mirror each other and
   read consistently in the catalog.

3. **Abridged all 18 chapters** into
   [`reference/`](../../artifacts/producing%20great%20sound%20for%20film%20and%20video/),
   in the house style (scope blockquote → Core idea → structured sections → a
   **Studio application** section tying each chapter to the *intended* sound
   roles). Reading was parallelized across six read-only explore passes over the
   verbatim `source/`; the abridgements + role tie-ins were written against the
   `0009` design and the crew-engine model (`0008`).

4. **Wrote the source
   [`INDEX.md`](../../artifacts/producing%20great%20sound%20for%20film%20and%20video/INDEX.md)**
   (chapter → planned-role map, four-section structure, composite-grounding scope
   note) mirroring the *Grammar of the Edit* INDEX, and updated the library catalog
   [`artifacts/INDEX.md`](../../artifacts/INDEX.md) row from *"Designed · staged ·
   abridgement pending"* to *"Imported · abridged (18 ch)."*

5. **Reconciled the living docs.** Flipped the four Rose references in
   [`architecture.md`](../architecture.md) (both Sound rows, the reading-the-map
   bullet, the open-decision) from *staged* → *abridged (18 ch)* with INDEX links,
   and **refreshed the [`README.md`](../../README.md)**, which had gone stale around
   `0006`: it still called *Grammar of the Edit* "to acquire" and omitted the edit
   (`edit.py`/`cutter.py`) and sound layers. The README now reflects both companion
   sources as grounded, lists all three library sources + the post-layer code, and
   broadens the license note to all three works.

## Decisions

1. **Map each chapter to the sound role it grounds**, not to a generic "post
   concern." The through-lines that emerged and are now recorded in the references:
   - **Audio perspective ↔ shot size** is the spine coupling sound to *Grammar of
     the Shot*: mic distance/pattern (Ch. 6), capture technique (Ch. 7), and
     reverb/EQ/level at the mix (Ch. 16–17) all set how *close* a sound feels.
     "Reverb = distance, not size" (Ch. 16) closes the loop at the post end.
   - **Diegetic / non-diegetic** (from edit Ch. 3) gets two concrete homes: the
     track-element taxonomy (Ch. 4) and reality-vs-punctuation effects (Ch. 15);
     **stems (D/M/E)** at the mix (Ch. 10, 17) are that split *rendered* — the
     studio's answer to the open production-dialogue vs post-soundtrack question.
   - **Cut-to-cue** gets both halves: the **beat grid** (Ch. 14, via toaster-
     strudel MIR) and **content cues** — phoneme/hard-attack edit points and the
     one-sided *"sound early is disturbing"* invariant (Ch. 13).
   - **`SpeechRenderer`**'s craft brief is Ch. 9 (VO/ADR): render **dry and clean**,
     add scene-matched reverb downstream; ADR-matching (mic distance/room) is the
     technical spec for the keep-diegetic-vs-TTS fallback.
   - **`SoundAnalyst`** = "the meter is ground truth" (Ch. 11) because an automated
     pipeline has no ears; **Ch. 18** reads as the spec for a sound-layer
     **`validate()`** (the analogue of `edit.py`'s `timeline()/validate`): sample
     rate/bit depth, dropframe/sync drift, phase/mono, **−24 LKFS**, peaks ≤ −2
     dBFS, unbroken room-tone bed, no clipping.

2. **Keep the hardware chapters honestly thin.** Ch. 3 (wiring) and much of
   Ch. 11 ground *physical* signal chains the code never touches; their Studio
   application sections say so and point at the format-interchange rules (Ch. 2,
   12) that *do* survive into software, rather than inventing a code tie.

3. **Extract on demand, per role.** The catalog and INDEX both reiterate `0009`'s
   guidance: pull Rose chapters for the role being built, not all 18 at once.

## Resulting state

- Third full grounding source complete: **18 `reference/` chapters + source
  `INDEX.md`**, catalog row updated, naming normalized across all three sources.
- Copyright gate verified: `source/` + `extraction/` stay gitignored; only the
  transformative `reference/` + `INDEX.md` (and the catalog edit) are staged to
  ship.
- **No code change.** The sound layer remains designed (`0009`) and unbuilt;
  `SpeechRenderer` is still first to build.

## Open threads

- **Build `SpeechRenderer`** (`0009`) — now with Ch. 9 as its craft brief and
  Ch. 2/12 as its output/format contract (48 kHz, ≥16-bit, dry, unprocessed).
- **Sound reconciliation sweep** — the 18 references' "Studio application" tie-ins
  are provisional leads at the not-yet-built layer; sweep them once the roles /
  `SpeechRenderer` / a sound-layer `validate()` settle (same standing task as the
  edit sweep from `0007`).
- **Wire toaster-strudel (MCP)** — Ch. 14's beat-based editing is where the
  `Composer`/`SoundAnalyst` MCP-client seam earns its keep.
