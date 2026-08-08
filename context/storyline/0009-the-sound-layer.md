# 0009 — The sound layer: a multi-phase department, Speech/Strudel renderers, and the first MCP client

> Date: 2026-08-08 · Focus: design the **sound** capability layer — the third
> technical layer after shot (prod) and edit (post). Sound is the first department
> that is **multi-phase, multi-backend, includes a non-generative analyzer, and
> wants MCP**, so it exercises (and validates) four generalizations at once. This is
> a **design/decision** entry; only the `SpeechRenderer` slice is slated to build
> first.

## Why sound is the stress-test layer

Grounding *Grammar of the Edit* Ch. 3 already gave us the **diegetic / non-diegetic**
split (production sound = dialogue/ambience; post sound = score/VO/SFX). Building the
sound department forces four things we had only asserted:

1. **A multi-phase department.** Sound has roles in **both** `shoot` (diegetic
   capture) and `assemble` (post) crews — the first department to span phases.
2. **A renderer registry with ≥2 backends** — Azure Speech *and* Strudel — which
   finally justifies formalizing the `Renderer` protocol deferred in `0006`.
3. **A non-generative analyzer / data-API** — audio MIR is a *sensor*, not a
   renderer; it validates the seam's "also admits data APIs" clause.
4. **MCP earning its keep** — `0005` said MCP arrives "once there is ≥2 of anything
   to route between." `toaster-strudel` is already an MCP server; sequitur becomes
   its **first MCP client**.

## Decisions

1. **Organize the sound department by the diegetic/non-diegetic spine.**
   - **shoot · diegetic** → **`SoundMixer` / `Boom`** (dialogue capture). Owns the
     first real branching judgment: *keep Omni's native take, or flag it for ADR.*
   - **assemble · diegetic** → **`SoundDesigner` / `SoundEditor`** (SFX, Foley,
     ambience bed).
   - **assemble · non-diegetic** → **`Composer`** (score/soundtrack) + VO narration.
   - **assemble · technical** → **`ReRecordingMixer`** (final mix, ducking, loudness).
   - **cross-department sensor** → **`SoundAnalyst`** (audio MIR) feeds the
     **`Editor`**'s cut-to-cue (the beat×content composition from edit Ch. 5).

2. **Three capabilities map onto the planes:**
   - **`SpeechRenderer`** (Azure AI Speech) — execution plane, sibling of
     `Studio`/`ImageStudio`/`Cutter`. Two uses (both from the audio brief in `0007`):
     clean **production dialogue**, and **post ADR/overdub** when the Omni take is
     bad (mute-and-dub). *This is the concrete form of "keep diegetic dialogue,
     fall back to TTS."*
   - **`Composer` → `toaster-strudel` (MCP) → strudel.cc** — the score/soundtrack
     renderer.
   - **`SoundAnalyst` → toaster-strudel `mir/` (MCP)** — beat grid / energy / stems;
     a sensor feeding the Editor, **not** a deliverable.

3. **Azure Speech: use the resource we already have — no new deployment.** Both
   Cognitive Services accounts are **`AIServices` (S0)**; **`hjg-m8jtp7uy-eastus2`**
   (eastus2 — the same account hosting `gpt-image-1`/`sora`) **includes Speech**.
   Key correction vs. `gpt-image`: **standard/HD neural TTS voices are built-in and
   call-and-go — there is no "deployment."** A deployment exists only for **Custom
   Neural Voice** (train + deploy, Responsible-AI gated), which is **deferred**.
   `SpeechRenderer` = Speech SDK (`azure-cognitiveservices-speech`), **HD neural
   voices** (fall back to standard if eastus2 lacks HD), **Entra-first** auth
   (`cognitiveservices.azure.com/.default`), reusing the existing KV secret. Realtime
   for lines, batch synthesis for long-form VO.

4. **Don't reimplement — wire toaster-strudel via MCP.** sequitur's `Composer` and
   `SoundAnalyst` call toaster-strudel's MCP tools (`strudel_docs` for grounding,
   `assemble`/`analyze`/`mir` for render/analysis). This matches **both** repos'
   philosophy ("no third-party reimplementation in between") and keeps the
   **AGPL-3.0 Strudel engine at arm's length** — toaster-strudel is MIT and only
   drives strudel.cc, so sequitur-as-MCP-client stays clear of AGPL. **Do not vendor
   the Strudel engine.**

5. **Grounding is partly external — a new pattern.** Unlike shot/edit (one Bowen
   book each), the sound layer's grounding is **composite**:
   - *film-sound taxonomy* → **Grammar of the Edit Ch. 3** (already have it);
   - *score/groove craft* → **toaster-strudel MCP `strudel_docs`** (external, live);
   - *film-sound craft per role* → **David Lewis Yewdall, *Practical Art of Motion
     Picture Sound* (4th ed.)** — chosen over Holman's *Sound for Film and Television*
     (3rd) because Yewdall is **role/process-oriented** (production recording, ADR,
     Foley, editing, the stage) and maps 1:1 onto our crew roles, mirroring how
     Grammar of the Edit grounded the Editor. **Holman is a deferred technical
     companion** for the ReRecordingMixer/loudness/delivery backbone. *(User is
     sourcing Yewdall from O'Reilly; run the standard extraction→reference→INDEX
     pipeline once acquired.)*

## Build order

1. **`SpeechRenderer` slice first** — self-contained, needs **no new resource**:
   add the SDK dep, extend `config.py` (Speech endpoint/region, non-secret), a
   `SpeechRenderer` sibling of `ImageStudio`, and a live synth smoke test. Rides
   Grammar of the Edit Ch. 3 (no Yewdall needed yet).
2. **Formalize the `Renderer` protocol** — now justified by the 3rd backend
   (`0006`'s deferral expires).
3. **Acquire Yewdall → ground the sound roles** (SoundMixer/SoundDesigner).
4. **toaster-strudel over MCP** — the bigger architectural step (sequitur's first MCP
   client); its own future slice, likely its own entry.

## Open threads

- Build the `SpeechRenderer` (defaults: HD neural, Entra-first + KV reuse, realtime
  `render(text, voice) -> .wav` first; batch later).
- Acquire Yewdall 4th ed; extract → reference → INDEX; then the SoundMixer /
  SoundDesigner roles (which need the crew engine, `0008`).
- Wire toaster-strudel as the first MCP client (Composer + SoundAnalyst); confirm
  AGPL arm's-length via the MIT MCP layer.
- Carried: crew engine phase A (`0008`); the edit post layer (`0007`); the
  reconciliation sweep.
