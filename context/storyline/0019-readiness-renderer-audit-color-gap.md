# 0019 — Readiness, the Renderer Audit, and the Color-Grading Gap

> Date: 2026-08-12 · Focus: a **design/planning** session after `0018` — no code.
> Assessed deployment readiness, named the **facilitative-renderer** pattern and
> audited which roles warrant one, and decided to **ground color grading** as the next
> source (Van Hurkman) *before* formalizing the `Renderer` protocol and building the
> Colorist. Grounding + code both deferred to fresh sessions (abridgement is
> context-heavy). This entry is the hand-off so the next session executes cleanly.

## What happened

Three linked questions, no code — the outcomes are decisions and a sequence.

1. **Is it deploy-ready?** Honestly assessed: the **grounding library spans all four
   phases (six abridged sources)**, but the **executing role code is one vertical
   slice** — `Engine().run(Phase.SHOOT, Brief)` dispatches only `Cinematographer` /
   `Gaffer` / `KeyGrip` → `Director` → `Shot`. `Editor` owns vocabulary but is **not
   dispatched** (no assemble crew, no `Sequence` reconciliation); only
   `HeuristicJudgment` (**A**) exists; the `Production` container (`0005`) is unwired;
   and `Department` names only 6 seats (no ART/STORY/CASTING/COLOR/PRODUCER). Verdict:
   **ship-able as a grounded proof-of-concept of the crew pattern, not as the "full
   studio that executes the concept."**

2. **The facilitative-renderer pattern.** Named the studio's two planes — a *decision
   plane* (roles choose grammar) and an *execution plane* (**renderers** turn choices
   into a media artifact). Governing principle: **a role warrants its own renderer only
   when it produces or transforms a distinct media artifact no existing renderer already
   makes.** Corollaries: roles that co-author a *shared* artifact ride a shared renderer
   (`Gaffer`/`KeyGrip` → `Studio`; `Storyboard Artist`/`Production Designer` →
   `ImageStudio`); pure-decision roles (`Screenwriter`, `Producer`) render no media.

3. **Where new renderers would pay off.** Audited the seats against that principle (see
   Decisions). The strongest opportunity — a **Colorist grade renderer** — surfaced a
   **grounding gap**: color is only borrowed today, never sourced. That reordered the
   plan: ground color *first*.

## Decisions

1. **Renderer inventory + flavors.** Existing/planned execution-plane renderers fall in
   three flavors:
   - **Generative** (grammar/text → new media): `Studio` (video), `ImageStudio` (still),
     `SpeechRenderer` (voice), `Composer`→toaster-strudel (score, planned).
   - **Transform / assembly** (process existing media per a decision): `Cutter`
     (Editor); *future* Colorist grade + Sound mix.
   - **Sensor / reader** (media → data): `SoundAnalyst` (audio MIR, planned); *future*
     production-design palette/reference lookup.

2. **Top renderer opportunities (ranked).**
   - **Colorist → grade renderer** *(strongest)*: today `ColorTemperature` is a
     `Gaffer` (capture) enum baked into the prompt — there is **no grade step**. A LUT/
     curve transform over rendered clips (ffmpeg/MoviePy or an image model) is a genuine
     transform-flavor renderer.
   - **Re-Recording Mixer / Sound Designer → mix renderer**: `speech.py`'s docstring
     *explicitly* defers presence-match / EQ / reverb / mix to these roles, not the
     dry-by-design `SpeechRenderer`. So a mix renderer over the dry stems is
     architecturally anticipated and currently missing.
   - **Production Designer → reference/lookbook backend** *(different flavor)*: a
     non-generative palette-extraction / reference-search reader (the seam already
     reserves room for "non-generative data APIs"), grounding the lookbook craft.

3. **Color grading is a grounding gap — ground it before the renderer.** Consistent with
   the studio principle (*every responsibility gets a primary source + a code layer*),
   the Colorist must not be the first renderer-bearing role built on borrowed grounding.
   Today color is only: `Gaffer`'s `ColorTemperature` (Grammar of the Shot Ch. 4 —
   *capture*) + Directing Ch. 36 (a director's-eye paragraph). `architecture.md` already
   flags "a dedicated design/color source is still open."

4. **Source + scope.** **Alexis Van Hurkman, *Color Correction Handbook: Professional
   Techniques for Video and Cinema* (2nd ed.)** — a systematic, reference-organized book
   matching the house profile (like Bowen/Rose; the opposite of the rejected Yewdall
   memoir). **Scope = grading only** (primary/secondary correction, lift/gamma/gain,
   hue-vs-sat curves, scopes, shot-matching, LUTs, creative looks). **Production design**
   (sets/costume/palette *concepts*) stays a **separate** open cell (Directing Ch. 23 is
   its first lead). *Color Correction Look Book* is an optional later companion for the
   "looks" vocabulary.

5. **Overlap to log at import.** `ColorTemperature` will live in **two** seats — `Gaffer`
   (capture) and `Colorist` (grade) — like the POV overlap (Directing Ch. 9 ↔ Taxonomy
   Ch. 7). Flag it in the new source's INDEX so capture-temp vs. grade-temp are
   reconciled when the Colorist owns its grade vocabulary.

6. **The sequence (locked).** (1) **Ground color grading** — new
   `artifacts/color grading/` source, abridged per the house pipeline; (2) **formalize
   the `Renderer` protocol** — the `0006` deferral has expired (four backends exist),
   retrofit `Studio`/`ImageStudio`/`SpeechRenderer`/`Cutter` onto a common
   `render(decision) -> (result, ref)` + a medium-keyed registry; (3) **build the
   `Colorist` + grade renderer** onto the protocol, on real grounding.

7. **Process: abridgement runs in its own fresh session.** The `0017`/`0018` pattern
   (full parallel-subagent reads) is **context-window-heavy**; run each abridgement as a
   dedicated session so it doesn't compete with design/code work. The user is returning
   with the Van Hurkman source next.

## Resulting state

- **No code changed.** Decisions logged only. The grounding library is unchanged at six
  abridged sources; **color grading is the seventh source — chosen and scoped, not yet
  imported.**
- The `Renderer` protocol and the `Colorist`/grade renderer are queued **behind** the
  color grounding, per the locked sequence.

## Open threads

- **Ground color grading (next session)** — drop Van Hurkman's chapters into
  `artifacts/color grading/extraction/` (`.docx`), then run convert → abridge → reconcile
  (source INDEX · `artifacts/INDEX.md` row · `architecture.md` Colorist row + reading-the-
  map · README · devlog). Log the capture-vs-grade `ColorTemperature` overlap.
- **Formalize the `Renderer` protocol (`0006`)** — a common `render(decision) ->
  (result, ref)` + medium-keyed registry; retrofit the four existing backends; lets a
  role *hold* its renderer instead of the CLI hard-wiring `Studio`.
- **Build the `Colorist` + grade renderer** — a transform renderer (LUT/curve over
  rendered clips) on the color grounding; `Colorist` owns the grade vocabulary.
- **Role-coverage gaps (from the readiness assessment)** — wire the **assemble** phase
  (`Editor` already owns vocab → `assemble_crew()` + `Director` reconciles a `Sequence`);
  seat the **plan** phase (`Screenwriter` owning the Taxonomy enums, a thin
  `StoryboardArtist` → `ImageStudio`); a **Producer** HITL greenlight/approve hook; then
  `PersonaJudgment` (**B**). Adding these needs new `Department`/`Phase` seats.
- Carried: the sound-mix renderer (Re-Recording Mixer); the production-design reference
  backend + a dedicated production-design source; crew-engine Production binding (`0005`);
  the reconciliation sweeps.
