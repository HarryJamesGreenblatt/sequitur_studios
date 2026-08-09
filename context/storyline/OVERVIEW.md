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
as typed enums in `sequitur/grammar.py`; `sequitur/prompt.py` renders a `Shot`
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

## Current state (keep fresh)

- **Code:** `sequitur/` package (`grammar`, `prompt`, `studio`, `image`, `speech`,
  `edit`, `cutter`, `config`) + CLI `scripts/generate.py`. `grammar.py` models Bowen
  as *orthogonal* layers (framing · lens/focus · lighting · motion) — today a *flattened
  crew* to be re-seated under roles (`0008`). **Three render backends over one
  grammar:** [`Studio`](../../sequitur/studio.py) = video (Gemini Omni Flash),
  [`ImageStudio`](../../sequitur/image.py) = still image (Azure Foundry `gpt-image-1`),
  and [`SpeechRenderer`](../../sequitur/speech.py) = voice (Azure AI Speech, built
  `0011`); `--image` on the CLI selects the still path. The
  post layer is [`edit.py`](../../sequitur/edit.py) (EDL/grammar model) +
  [`cutter.py`](../../sequitur/cutter.py) (MoviePy executor) — note `movie.py` was
  renamed to `edit.py` to avoid the `moviepy` collision. `--dry-run` composes prompts
  with no API call. Interpreter is a project `.venv` (Python 3.12). No test suite yet.
- **Grounding library:** `artifacts/` is a *multi-source* library indexed by
  `artifacts/INDEX.md`. **Three full sources** now: *Grammar of the Shot* (production/
  cinematography, encoded in `grammar.py`), *Grammar of the Edit* (post/editorial,
  8 abridged chapters + INDEX, grounding [`edit.py`](../../sequitur/edit.py)), and
  *Producing Great Sound* (Rose — sound, **18 abridged chapters** + INDEX, `0010`). Each source
  holds the raw book (`extraction/` .docx, `source/` .md — gitignored) and the
  abridged, session-ready `reference/` with a per-source `INDEX.md` (chapter → code
  map). Each abridged chapter ends with a "Studio application" section.
- **Architecture:** `context/architecture.md` maps phase → department (Appendix D)
  → grounding source → code layer. Implemented today: camera/grip/electric in the
  production phase, plus the **renderer seam** (video + image backends). **Direction
  (decided `0008`, unbuilt):** a **crew engine** makes roles first-class — `Role` +
  swappable `Judgment` (heuristic A / persona B / human), **Producer = HITL**,
  **Director = agent role**, and the **Production (PM board) as the dumb container**.
  Editorial/post is the next layer to build out.
- **Secrets:** both backend API keys live in **Azure Key Vault**
  (`kv-sequitur484673472841`), fetched at runtime via `DefaultAzureCredential`; `.env`
  holds only non-secret pointers (vault name, endpoint, deployment). Never reintroduce
  plaintext keys.
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
- **Build the crew engine — phase A (`0008`)** — `Role` + `Judgment` +
  `Contribution` and a dumb engine over a **local-folder Production** (`0005`
  provider #1), re-seating `grammar.py`'s enums under
  `Cinematographer`/`Gaffer`/`KeyGrip` and `edit.py`'s under
  `Editor`/`Colorist`/`SoundEditor`, with a `Director` reconciler. Heuristic
  judgment only (no LLM); persona (**B**) and PM-board wiring come later.
- **Build the sound layer (`0009`)** — `SpeechRenderer` **built** (`0011`: Azure
  Speech on the existing `hjg-m8jtp7uy-eastus2` account, no new resource / no
  deployment; dry 48 kHz/16-bit/mono, validated live). Next: formalize the `Renderer`
  protocol (3rd backend now justifies it), ground the sound roles from the **abridged
  Rose** (`0010`) once the crew engine lands, and wire **toaster-strudel** as
  sequitur's first MCP client (`Composer`/`SoundAnalyst`).
- **Reconciliation sweep (standing, `0007`)** — the edit references' "Studio
  application" tie-ins are provisional leads at the not-yet-built post layer; sweep
  all 8 to align them once the roles/`edit.py` code settles.
- **Build the post layer** — the cut-decision engine (Ch. 5 six motivators) over a
  shots→scenes→acts model in [`edit.py`](../../sequitur/edit.py); cuts/fades first (no
  handles), then handle padding for dissolves; time-align coverage for multicam-style
  cutting. Execution via [`cutter.py`](../../sequitur/cutter.py) (MoviePy).
- **Wire the reference-keyframe flow** — pass a `gpt-image-1` still into
  `Studio.render` as a conditioning reference for a shot (the higher-leverage use of
  the image backend); formalize a `Renderer` protocol once a third backend appears
  (`sora` on the same Azure account is a natural next video backend).
- **Sequence layer** — the planned multi-shot planner (180°/30°, matching/reverse,
  eye-line, screen direction). Ch. 5's reference is effectively its spec; build it
  once the editorial grounding lands.
- **Broader discipline library** — sound, story/screenwriting, production design,
  color, producing are named departments in `context/architecture.md`. **Sound is
  now designed** (`0009`) and its source **abridged** (`0010`, Jay Rose *Producing Great
  Sound*, 18 ch); story/design/color still have no source.
- **No test suite yet** — a small `build_prompt` smoke test would guard the grammar.
