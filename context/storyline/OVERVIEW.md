# Storyline — Sequitur Studios devlog

This directory is the project's **running history**, written *for the next agent*
(human or AI) picking up the work. Session-scoped memory is lost between
conversations and the original session's notes were never captured, so this
devlog is the durable, in-repo record of *what was done and why*.

## What Sequitur Studios is

A small film studio built on the Gemini **Omni Flash** video model. Its premise:
compose every shot through the **grammar of the shot** (Christopher J. Bowen,
*Grammar of the Shot*, 4th ed.) so the studio speaks proper cinematographic
language to the model instead of vague prompts. The Bowen vocabulary is encoded
as typed enums under `sequitur/crew/` (re-seated from the old `grammar.py`, `0012`);
`sequitur/prompt.py` renders a `Shot`
into a film-literate prompt.

## How to use this devlog

- **Read newest-last.** Entries are numbered `NNNN-slug.md` in chronological order.
- **At the end of a working session, append a new entry.** Copy the shape of the
  most recent one: *Date · Focus · What happened · Decisions · Resulting state ·
  Open threads*.
- **Keep the two live lists below current** (Current state, Open threads) so a new
  agent can orient in ~30 seconds without reading every entry.
- Prefer linking durable artifacts (`sequitur/grammar.py`, the reference chapters)
  over re-explaining them.

## Entries

- [`0000-genesis.md`](0000-genesis.md) — the initial studio scaffold *(reconstructed
  from repo state; original notes were lost)*.
- [`0001-grounding-the-grammar.md`](0001-grounding-the-grammar.md) — migrated the
  source book, abridged it per chapter, and rewrote `grammar.py` to be
  source-derived.
- [`0002-studio-architecture.md`](0002-studio-architecture.md) — mapped the
  Appendix-D roles into a production-studio architecture, formalized the
  multi-source grounding library, and de-conflated the docs (`README`/`INDEX`/
  `OVERVIEW`).
- [`0003-published.md`](0003-published.md) — abridged the verbatim appendices,
  gitignored the raw book text, and published the public repo.
- [`0004-architecture-framing-and-license.md`](0004-architecture-framing-and-license.md)
  — reframed the README/description as a production-studio-in-layers and added the
  MIT license.
- [`0005-productions-as-instances-and-output-storage.md`](0005-productions-as-instances-and-output-storage.md)
  — decided productions are external *content instances* (not repo forks) modeled as
  plans whose buckets = layers, read through `ProductionProvider`/`OutputStore`
  seams; settled **SharePoint via Graph** as the output store. Design only, not yet
  built.
- [`0006-renderer-seam-and-image-backend.md`](0006-renderer-seam-and-image-backend.md)
  — generalized "render video with Gemini" into a **renderer seam** and *built* a
  second, non-Google backend: still images on **Azure Foundry `gpt-image-1`**
  (`ImageStudio`). Moved both API keys into **Azure Key Vault**, fetched at runtime
  via `DefaultAzureCredential`; `.env` now holds only non-secret pointers.
- [`0007-grounding-the-edit-layer.md`](0007-grounding-the-edit-layer.md)
  — imported & abridged Bowen's **Grammar of the Edit** (8 chapters) as the second
  full source, grounding the **post/editorial** layer. Because there's no code to
  retrofit, used the grounding to **design the post architecture**: `movie.py`, the
  shots→scenes→acts hierarchy, the **cut-to-cue** engine, the diegetic/non-diegetic
  **production-dialogue vs post-soundtrack** split, and the **handles** constraint on
  fixed-length shots. Grounding done; post-layer code not yet built.
- [`0008-the-crew-engine.md`](0008-the-crew-engine.md)
  — decided **how the department/role model becomes code**: a **crew engine** —
  roles as classes (`Role` + swappable `Judgment`: heuristic **A** / persona **B** /
  human), three authority tiers (**Producer = HITL**, **Director = agent role**,
  **Crew = components**), and the **`0005` Production (the PM board) as the dumb
  container** (Component/ECS shape: entity = Production data, behavior = engine's
  roles). Retires the `movie.py`→`edit.py` model / `cutter.py` executor naming
  confusion. Design; phase A not yet built.
- [`0009-the-sound-layer.md`](0009-the-sound-layer.md)
  — designed the **sound** layer: a **multi-phase department** (shoot + assemble,
  organized by diegetic/non-diegetic), with a **`SpeechRenderer`** (Azure Speech —
  rides the existing `hjg-m8jtp7uy-eastus2` AIServices account, **no new resource**;
  standard/HD voices are call-and-go, **no deployment**), a **`Composer`** →
  **toaster-strudel (MCP)** score renderer, and a non-generative **`SoundAnalyst`**
  (audio MIR). Grounding is **composite**: Grammar of the Edit Ch. 3 + a craft source
  (Yewdall 4th — since **rejected as too anecdotal**, **Jay Rose** *Producing Great
  Sound* staged instead) + toaster-strudel MCP. First **MCP client** case. `SpeechRenderer`
  builds first; design only so far.
- [`0010-unpacking-the-rose.md`](0010-unpacking-the-rose.md)
  — abridged **Jay Rose, *Producing Great Sound for Film and Video*** (4th ed.) into
  **18 `reference/` chapters + source INDEX** — the **third full grounding source**.
  Mapped each chapter to the sound role it grounds (audio-perspective ↔ shot-size;
  diegetic split as D/M/E stems; cut-to-cue = beat grid × content cues; `SpeechRenderer`
  brief = Ch. 9 dry-render + ADR-match; Ch. 18 = spec for a sound-layer `validate()`).
  Normalized filenames to `chNN-<slug>.md` across all three sources. No code built.
- [`0011-the-voice-layer.md`](0011-the-voice-layer.md)
  — **built** the `SpeechRenderer` (`0009`'s first slice): Azure AI Speech text-to-
  speech, the studio's **third render backend** and first *sound* renderer. Rides the
  existing `hjg-m8jtp7uy-eastus2` AIServices account (**no new resource/deployment**),
  reuses the shared KV key, and emits the Rose Ch. 2/9/12 contract — **dry, 48 kHz /
  16-bit / mono** — validated with a live synth. First code since `0006`.
- [`0012-the-crew-unflattened.md`](0012-the-crew-unflattened.md)
  — **built** the first structural step of the crew engine (`0008`): decomposed the
  source-named, three-departments-in-one `grammar.py` into a **`crew/` package** — a
  thin `Role` base + `Department`/`Phase` axes, and three shoot-phase roles
  (**Cinematographer**/**Gaffer**/**KeyGrip**) each owning its verbatim vocabulary;
  `Shot` moved to `shot.py`. Guarded by a new smoke test and proven **byte-for-byte
  behaviour-neutral**. Vocabulary-only — `Judgment`/`Director` are the next pass.
- [`0013-the-editor-seat.md`](0013-the-editor-seat.md)
  — **built** the second crew pass: re-seated `edit.py`'s vocabulary
  (`Transition`/`EditReason`/`EditCategory`) under a new **`Editor`** role
  (`crew/editorial.py`, assemble phase), leaving the shots→scenes→acts EDL +
  `timeline()`/`validate()` in `edit.py` as the editorial analogue of `shot.py`.
  Added a guard test (`tests/test_edit.py`); public API + `cutter.py` untouched.
- [`0014-the-crew-behaviour.md`](0014-the-crew-behaviour.md)
  — **built** the crew-engine **behaviour** layer: a swappable `Judgment`
  (`HeuristicJudgment` = deterministic **A**), a `Brief`/`Contribution` pair, a
  `Director` reconciler, and a dumb `Engine`. The shoot-phase crew now *chooses* —
  `Engine().run(Phase.SHOOT, Brief(...))` assembles a grammar-complete `Shot` (each
  department fills its owned fields, the Director merges the disjoint slices) that
  renders via `build_prompt`. Guard test `tests/test_engine.py`.
- [`0015-staging-preproduction-sources.md`](0015-staging-preproduction-sources.md)
  — **imported & staged** two *plan*-phase grounding sources: **Directing** (Rabiger &
  Hurbis-Cherrier, 6th ed. — 28 curated ch, a Director-centric spine across every
  phase) and **The Screenwriter's Taxonomy** (Williams — 8 ch, a genre/voice/pathway/
  POV *classification system*, enum-friendly for a future `Screenwriter` role).
  Converted to verbatim `source/` (copyright-gated), mapped chapters→roles in both
  `INDEX.md` files, reconciled the catalog + architecture. **Abridgement deferred to
  designated sessions.** Surfaced a new **casting/actors** dimension (Directing 18–20).
- [`0016-abridging-the-screenwriters-taxonomy.md`](0016-abridging-the-screenwriters-taxonomy.md)
  — ran the first **designated abridgement session**: transformed **The Screenwriter's
  Taxonomy** (the smaller staged source) into **8 abridged `reference/` chapters** + a
  refreshed INDEX — the library's **fourth abridged source**. Full scan, nothing
  dropped. Converged the Studio applications on one design: the taxonomy as a **layered
  descriptor vector** (`MovieType`/`Supergenre` closed enums · `Macrogenre` large enum ·
  `Microgenre` open tag · `Voice` a struct of axes · `Pathway` closed enum · `POV` three
  small enums) that a future `crew/screenwriting.py` `Screenwriter` owns and that acts
  as the plan-phase control surface (POV→camera, Pathway→edit, Voice→renderers). No code.
- [`0017-abridging-directing.md`](0017-abridging-directing.md)
  — ran the **last designated abridgement session**: transformed **Directing** (Rabiger
  & Hurbis-Cherrier, 6th ed.) into **28 abridged `reference/` chapters** + a refreshed
  INDEX (the **fifth and final staged source**), spanning every phase. Fanned the full
  comprehensive read out to **nine parallel subagents** (3–4 ch each, by arc) to avoid
  semantic-search fidelity loss. Confirmed Directing as a **control spine**: POV as a
  hard coverage constraint, tone/genre as a global style contract, the shooting script
  as the PLAN→SHOOT bridge, Ch. 26 as *meta to the crew engine*, Ch. 30 as the shoot↔edit
  seam, and the natural corpus for a Director `PersonaJudgment`. **All five sources now
  abridged** — the grounding library is complete for the departments modelled today;
  next work is code. No code.
- [`0018-abridging-professional-storyboarding.md`](0018-abridging-professional-storyboarding.md)
  — folded in a **sixth grounding source**: transformed Paez & Jew's *Professional
  Storyboarding: Rules of Thumb* (10 curated ch — career/business ch 11–12 dropped) into
  **10 abridged `reference/` chapters** + a source INDEX, via **four parallel subagents**
  (the `0017` pattern). Grounds a new **Storyboard Artist / previz** seat, and
  crucially gives the deferred **reference-keyframe** flow a grounded home: a storyboard
  panel encodes the DP's grammar, so it *is* a pre-rendered `Shot` and the literal form
  of the keyframe the video studio conditions on (`ImageStudio`). Ch. 8 maps continuity
  board → `Shot` list, animatic → assembled edit, previs → `studio.py` + edit layer. No code.
- [`0019-readiness-renderer-audit-color-gap.md`](0019-readiness-renderer-audit-color-gap.md)
  — a **design/planning** session (no code): assessed deployment readiness (grounding
  spans all four phases, but role code is **one vertical slice** — only the shoot crew
  executes; `Editor` unwired, only `HeuristicJudgment` A, `Production` unbound); named
  the **facilitative-renderer** pattern (decision plane = roles, execution plane =
  renderers) and its principle — *a role warrants its own renderer only when it produces
  or transforms a distinct media artifact*; and decided to **ground color grading**
  (Van Hurkman, *Color Correction Handbook* 2e — **seventh source**, scoped to grading
  only) *before* formalizing the `Renderer` protocol and building the **Colorist + grade
  renderer**. Sequence LOCKED: ground color → protocol → Colorist. Abridgement runs in
  its own fresh session (context-heavy).
- [`0020-grounding-color-the-colorists-handbook.md`](0020-grounding-color-the-colorists-handbook.md)
  — ran the dedicated abridgement session for `0019`'s **step 1**: folded in a **seventh
  grounding source**, **Alexis Van Hurkman's *Color Correction Handbook*** (shipped
  already converted to Markdown), transforming its 10 chapters into **10 abridged
  `reference/` chapters** + a source INDEX via **five parallel subagents**. Grounds a
  future **Colorist** role in the post/finishing phase and its two renderer flavors — a
  *transform* **grade renderer** (LUT/curve over rendered clips, the `Cutter` plane) and
  a *sensor/reader* **scope read** backing a color `validate()`/broadcast-safe gate.
  Lift/gamma/gain = the Colorist's first owned vocabulary; Ch. 9 shot matching = the
  color analogue of the Editor's continuity check across a `Sequence`. Logged the
  **`ColorTemperature` two-seat overlap** (Gaffer capture ↔ Colorist grade). Scoped to
  grading only; production-design concepts stay separate. No code.
- [`0021-formalizing-the-renderer-seam.md`](0021-formalizing-the-renderer-seam.md)
  — **built** `0019`'s **step 2**: formalized the renderer seam `0006` deferred. New
  [`render.py`](../../sequitur/render.py) — a `Medium` enum (video/still/voice/film), a
  `RenderResult(raw, ref)` pair, a `runtime_checkable` **`Renderer` protocol**, and a
  lazy **medium-keyed registry** (`renderer_for(medium)`). Retrofitted all four backends
  (`Studio`/`ImageStudio`/`SpeechRenderer`/`Cutter`) onto it — each declares its `medium`
  and returns `RenderResult` — so a role can *hold* a renderer by medium instead of the
  CLI hard-wiring `Studio`. Non-breaking (`RenderResult` is a tuple; legacy unpacking
  survives). Guard test `tests/test_render.py` (6); all 17 smoke tests green. The coming
  Colorist grade renderer plugs a `GRADE` medium into the same registry (`0019` step 3).
- [`0022-the-colorist-and-the-grade-transform.md`](0022-the-colorist-and-the-grade-transform.md)
  — **built** `0019`'s **step 3** (closing the locked sequence): seated the **Colorist**
  role (`crew/colorist.py` — `Look`/`TonalRange`/`Cast`), built the reified **`Grade`**
  decision model ([`grade.py`](../../sequitur/grade.py), a **Command** stack — ordered,
  `validate()`-able, plan-serializable — the color analogue of `edit.py`) and the
  **`Grader`** ffmpeg **transform** ([`grader.py`](../../sequitur/grader.py), the color
  analogue of `cutter.py`). Split the registry into **two planes**: producers keyed by
  `Medium`, and a new **operator** plane (`Transform` / `operator_for`) keyed by an
  `Operation` verb — because a grade is a **medium-preserving Decorator** (Nystrom's
  decorated-service refinement) that can't be keyed by an output artifact kind. `Look`
  is an **open preset library** (no completeness claim) and a **production look registry**
  (`register_look`) lets a production name its own `Grade`. Guard test `tests/test_grade.py`
  (8); all 25 smoke tests green.
- [`0023-the-assemble-phase-and-the-grade.md`](0023-the-assemble-phase-and-the-grade.md)
  — two advances in one: **(1)** made the crew engine **phase-aware** so the
  `Colorist`/`Editor` actually participate — `Brief` gained `shots` (the coverage), the
  `Editor`/`Colorist` gained assemble-phase heuristics (cut structure + base grade), and
  a new **`Director.assemble`** / **`Engine.assemble`** reconcile them into a **graded
  edit `Sequence`** (each `Clip` now carries a `grade`; the default crew is the
  phase-filtered `full_crew`) — advancing the `0014` thread; and **(2)** replaced the
  grade executor's placeholder ffmpeg `eq`/`colorbalance` filters (`0022`) with the
  industry-standard **3D-LUT** path — a new [`lut.py`](../../sequitur/lut.py) bakes the
  grade's primaries (ASC CDL + Rec. 709 saturation) into a spec-correct `.cube` via
  **colour-science**, and the `Grader` applies it with ffmpeg **`lut3d`**. Contained
  executor swap (the `Grade`/registry untouched). Guard tests (`test_engine` 5, a
  LUT-bake test in `test_grade`); all 26 green + verified end-to-end.

## Current state (keep fresh)

- **Code:** `sequitur/` package (`crew/` · `shot`, `prompt`, `studio`, `image`,
  `speech`, `edit`, `cutter`, `grade`, `grader`, `lut`, `render`, `config`) + CLI
  `scripts/generate.py` + tests
  (`tests/test_prompt.py` · `test_edit.py` · `test_engine.py` · `test_render.py` ·
  `test_grade.py`). The Bowen vocabulary lives under **`crew/`** (`0012`): a  thin `Role` base (`crew/role.py`) with three shoot-phase roles — `Cinematographer`
  (`crew/camera.py`), `Gaffer` (`crew/lighting.py`), `KeyGrip` (`crew/grip.py`) — each
  *owning* its slice of the grammar enums (the old flat `grammar.py`, un-flattened),
  plus the assemble-phase `Editor` (`crew/editorial.py`) and `Colorist`
  (`crew/colorist.py`, `0022`). Roles now have **behaviour**
  (`0014`): a swappable `Judgment` (`HeuristicJudgment` = deterministic A), and
  `Engine().run(Phase.SHOOT, Brief(...))` dispatches the crew — each proposes a
  `Contribution`, the `Director` reconciles them into a complete `Shot`. **Three render
  backends over one grammar:** [`Studio`](../../sequitur/studio.py) = video (Gemini
  Omni Flash), [`ImageStudio`](../../sequitur/image.py) = still image (Azure Foundry
  `gpt-image-1`), and [`SpeechRenderer`](../../sequitur/speech.py) = voice (Azure AI
  Speech, built `0011`) — all four backends (those three + the `Cutter` edit executor)
  now sit behind a formal **`Renderer` protocol + medium-keyed registry**
  ([`render.py`](../../sequitur/render.py), `0021`); a **second registry plane** (`0022`)
  holds **operators** (`Transform`, keyed by `Operation`) — the first being the
  **`Grader`** color grade ([`grader.py`](../../sequitur/grader.py)) driven by the
  Colorist's reified **`Grade`** model ([`grade.py`](../../sequitur/grade.py)); the
  `Grader` bakes the grade's primaries into a `.cube` LUT via colour-science
  ([`lut.py`](../../sequitur/lut.py)) and applies it with ffmpeg `lut3d` (`0023`).
  `--image`
  on the CLI selects the still path. The
  post layer is [`edit.py`](../../sequitur/edit.py) (the editorial EDL model + its
  `timeline()`/`validate()`, the analogue of `shot.py`) with its vocabulary owned by
  the **`Editor`** role (`crew/editorial.py`, `0013`) +
  [`cutter.py`](../../sequitur/cutter.py) (MoviePy executor) — note `movie.py` was
  renamed to `edit.py` to avoid the `moviepy` collision. `--dry-run` composes prompts
  with no API call. Interpreter is a project `.venv` (Python 3.12); tests in `tests/`
  (`test_prompt` · `test_edit` · `test_engine` · `test_render` · `test_grade`).
- **Grounding library:** `artifacts/` is a *multi-source* library indexed by
  `artifacts/INDEX.md`. **Seven abridged sources** now — spanning every department the
  architecture models: *Grammar of the Shot* (production/cinematography,
  encoded under `crew/`), *Grammar of the Edit* (post/editorial, 8 abridged chapters +
  INDEX, grounding [`edit.py`](../../sequitur/edit.py)), *Producing Great Sound* (Rose —
  sound, **18 abridged chapters** + INDEX, `0010`), *The Screenwriter's Taxonomy*
  (Williams — story/development, **8 abridged chapters** + INDEX, `0016`),
  *Directing* (Rabiger & Hurbis-Cherrier — a Director-centric spine across every phase,
  **28 abridged chapters** + INDEX, `0017`), *Professional Storyboarding* (Paez &
  Jew — previsualization / a Storyboard-Artist seat, **10 abridged chapters** + INDEX,
  `0018`; a board panel = a pre-rendered `Shot` = the reference keyframe), and *Color
  Correction Handbook* (Van Hurkman — post/finishing color grading, grounding the
  **Colorist** built `0022`, **10 abridged chapters** + INDEX, `0020`). Each source
  holds the raw book (`extraction/` .docx, `source/` .md — gitignored) and the
  abridged, session-ready `reference/` with a per-source `INDEX.md` (chapter → code
  map). Each abridged chapter ends with a "Studio application" section.
- **Architecture:** `context/architecture.md` maps phase → department (Appendix D)
  → grounding source → code layer. Implemented today: camera/grip/electric in the
  production phase, the assemble-phase **`Colorist`** (`0022`), plus the **renderer seam**
  — producers (video + image + voice + film) and a second **operator** plane whose first
  member is the color **`Grader`**. **Direction
  (decided `0008`, unbuilt):** a **crew engine** makes roles first-class — `Role` +
  swappable `Judgment` (heuristic A / persona B / human), **Producer = HITL**,
  **Director = agent role**, and the **Production (PM board) as the dumb container**.
  Editorial/post is the next layer to build out.
- **Secrets:** both backend API keys live in **Azure Key Vault**, fetched at runtime
  via `DefaultAzureCredential`; `.env` holds only non-secret pointers (vault name,
  endpoint, deployment). Never reintroduce plaintext keys.
- **Published:** public repo at
  <https://github.com/HarryJamesGreenblatt/sequitur_studios> (`main`). Verbatim
  book text (`extraction/`, `source/`) and secrets (`.env`) are gitignored; only
  code, docs, and the transformative `reference/` ship. Licensed **MIT**
  ([`LICENSE`](../../LICENSE)).
- **Doc naming convention:** `README.md` (repo root only) · `INDEX.md` (catalogs)
  · `OVERVIEW.md` (guides, like this file).
- **Production model (decided `0005`, not yet built):** the engine is singular and
  evolves here; a *production* is external **content** (not a repo fork), modeled as
  a plan whose buckets = layers, each holding seeds/history *in* the plan and
  guidance/output *by reference*. The engine is a **driver client** reading through
  a `ProductionProvider` seam and writing via an `OutputStore` seam. Output bytes
  live in the **Sequitur Solutions** tenant's **SharePoint via Microsoft Graph**
  (Azure Blob deferred); MCP is the eventual control-plane connector.

## Open threads (keep fresh)

- **Build the provider seams (`0005`)** — `ProductionProvider` +
  `OutputStore` interfaces with **local-folder** implementations first (no platform,
  no auth) to prove the driver-client loop against `output/`; then a Graph-backed
  `OutputStore` (Entra app, least-privilege, scoped to one SharePoint library).
  Production-store platform (GitHub Projects v2 vs. ADO) is deferred until a first
  real production exists.
- **Acquire *Grammar of the Edit*** — **DONE** (`0007`): 8 chapters abridged into
  `artifacts/grammar of the edit/reference/`. Next is building the post layer it
  grounds.
- **Build the crew engine — phase A (`0008`)** — **in progress:** vocabulary re-seated
  under `crew/` — `Cinematographer`/`Gaffer`/`KeyGrip` (`0012`) and `Editor` (`0013`);
  **behaviour** added (`0014`) — `Judgment`/`HeuristicJudgment`, `Brief`/`Contribution`,
  `Director`, and a dumb `Engine` that assembles a shoot-phase `Shot`. **Assemble-phase
  behaviour built (`0023`):** `Engine.assemble` + a phase-aware `Director.assemble`
  reconcile the `Editor` (cut) and `Colorist` (base grade) into a graded edit `Sequence`.
  Next: bind a **local-folder Production** (`0005` provider #1) in place of the bare
  `Brief`, a real cut-decision heuristic (Ch. 5 motivators) + per-shot grade matching
  (Ch. 9), then `PersonaJudgment` (**B**) and PM-board wiring.
- **Build the sound layer (`0009`)** — `SpeechRenderer` **built** (`0011`: Azure
  Speech on the existing `hjg-m8jtp7uy-eastus2` account, no new resource / no
  deployment; dry 48 kHz/16-bit/mono, validated live). The `Renderer` protocol is now
  **formalized** (`0021`) with an operator plane (`0022`); still to do: ground the sound
  roles from the **abridged
  Rose** (`0010`) once the crew engine lands, and wire **toaster-strudel** as
  sequitur's first MCP client (`Composer`/`SoundAnalyst`).
- **Reconciliation sweep (standing, `0007`)** — the edit references' "Studio
  application" tie-ins are provisional leads at the not-yet-built post layer; sweep
  all 8 to align them once the roles/`edit.py` code settles.
- **Build the post layer** — the cut-decision engine (Ch. 5 six motivators) over a
  shots→scenes→acts model in [`edit.py`](../../sequitur/edit.py); cuts/fades first (no
  handles), then handle padding for dissolves; time-align coverage for multicam-style
  cutting. Execution via [`cutter.py`](../../sequitur/cutter.py) (MoviePy).
- **Wire the reference-keyframe flow** — **now grounded** (`0018`, *Professional
  Storyboarding*: a board panel *is* a reference keyframe). Pass a `gpt-image-1` still
  into `Studio.render` as a conditioning reference for a shot (the higher-leverage use
  of the image backend); a future `StoryboardArtist` role emits that per-shot keyframe.
  Formalize a `Renderer` protocol once a third backend appears (`sora` on the same Azure
  account is a natural next video backend).
- **Ground color grading (next session, `0019`)** — **decided:** **Van Hurkman,
  *Color Correction Handbook* (2e)** as the **seventh source**, scoped to *grading only*
  (primary/secondary, lift/gamma/gain, hue-vs-sat curves, scopes, shot-matching, LUTs,
  looks); production design stays a separate open cell. Drop chapters into
  `artifacts/color grading/extraction/` (`.docx`) → convert → abridge → reconcile; log
  the capture-vs-grade `ColorTemperature` overlap (`Gaffer` ↔ `Colorist`). **Abridgement
  runs as its own fresh session** (context-heavy, per `0017`/`0018`).
- **Formalize the `Renderer` protocol (`0006`)** — **DONE** (`0021`): a `Medium` enum,
  `RenderResult(raw, ref)`, a `runtime_checkable` `Renderer` protocol, and a lazy
  `renderer_for(medium)` registry; the four backends retrofitted. Extended (`0022`) with
  a second **operator** plane (`Transform` / `operator_for`, keyed by `Operation`) for
  medium-preserving transforms. Still to do: let a **role hold its renderer** through the
  registry instead of the CLI hard-wiring `Studio`.
- **Build the `Colorist` + grade renderer (`0019`)** — **DONE** (`0022`–`0023`): the `Colorist`
  role owns the grade vocabulary (`Look`/`TonalRange`/`Cast`), the reified `Grade` model
  ([`grade.py`](../../sequitur/grade.py)) is a plan-serializable Command stack, and the
  `Grader` ([`grader.py`](../../sequitur/grader.py)) is the medium-preserving transform —
  now the **true-to-form 3D-LUT path** (`0023`): grade primaries baked to a spec-correct
  `.cube` via colour-science ([`lut.py`](../../sequitur/lut.py)), applied with ffmpeg
  `lut3d` (replacing the `0022` `eq`/`colorbalance` placeholder). Next: **HSL/shape
  secondaries** (Ch. 5–6, as *masked passes* around the primary LUT), a **scope-reader
  `validate()`**/broadcast-safe gate (Ch. 2/10, a *reader*-flavor transform), and Ch. 9
  **shot matching** across a `Sequence`. The renderer audit also queued a **sound-mix
  renderer** (Re-Recording Mixer, anticipated in `speech.py`) and a non-generative
  **production-design reference/lookbook** reader.
- **Sequence layer** — the planned multi-shot planner (180°/30°, matching/reverse,
  eye-line, screen direction). Ch. 5's reference is effectively its spec; build it
  once the editorial grounding lands.
- **Broader discipline library** — sound, story/screenwriting, production design,
  color, producing are named departments in `context/architecture.md`. **Sound**
  designed (`0009`) + **abridged** (`0010`, Jay Rose, 18 ch). **Story abridged**
  (`0016`): **The Screenwriter's Taxonomy** (8 ch) transformed into `reference/` — the
  basis for a typed `Screenwriter` vocabulary. **The rest of the plan phase staged**
  (`0015`): **Directing** (28 ch) imported & mapped, **abridgement deferred to the
  remaining designated session(s)** — start with the Director chapters (7–11, 17). A
  dedicated **color** source is now **decided** (`0019`: Van Hurkman, *Color Correction
  Handbook* 2e — awaiting import); **production design** remains a separate open cell; a
  **casting/actors** department is surfaced but unmodelled.
- **No test suite yet** — **done (`0012`–`0014`):** `tests/` holds `test_prompt.py`,
  `test_edit.py`, `test_engine.py` (assert the public surface). Add coverage as new
  layers land.
