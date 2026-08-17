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
  rides the existing AIServices account, **no new resource**;
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
  existing AIServices account (**no new resource/deployment**),
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
- [`0024-the-production-board.md`](0024-the-production-board.md)
  — an **infrastructure + design** session (no `sequitur/` code): realized the `0008`
  decision that *the Production **is** the PM board* by choosing **Azure DevOps** as the
  platform (the choice `0005` deferred) and standing up the actual board. Picked ADO over
  **Microsoft Planner** — both auth-proven from the local `az login`, but Planner is
  effectively two levels (plan → bucket → task) while the EDL is **four**
  (Act → Scene → Beat → Shot), which ADO's work-item hierarchy carries natively. Built a
  custom **Basic-derived process** with four domain-named work-item types
  (**Act / Scene / Beat / Shot**) wired to the four backlog levels (a new top portfolio
  for Act; inherited Basic types disabled; states To do / Doing / Done), the seven crew
  **departments as Area Paths** (orthogonal to status — the ADO-native "bucket = layer"),
  and **one project = one Production instance** (`0005`). Driven via the official **Azure
  DevOps MCP** (the toaster-strudel MCP-client pattern); process customization is
  REST + portal (the backlog-level *behaviors* REST surface is too thin, per first-party
  docs). Concrete infra identifiers stay in gitignored local notes.
- [`0025-the-production-provider.md`](0025-the-production-provider.md)
  — **built** the `ProductionProvider` seam — the `0005` → `0008` → `0024` payoff. Finished
  the two board prerequisites (`Mood`/`Look` fields on Shot; a scaffolded
  Act → Scene → Beat → Shot example tree), then wrote
  [`production.py`](../../sequitur/production.py): a `runtime_checkable`
  **`ProductionProvider`** protocol (`read_brief` / `write_sequence`) with two backends —
  **`AzureDevOpsProduction`** (the live board over ADO REST via `DefaultAzureCredential`,
  **no new dependency** — stdlib `urllib`) and **`LocalFolderProduction`** (a JSON test
  double, the `0005` "local folder"). The board's narrative tree now reads into a `Brief`
  the crew `Engine` assembles, and the graded `Sequence` writes back. The mirror of the
  `Renderer` protocol (`0021`) for the *decision* plane — but with **no registry** (the
  caller picks a backend; unlike a role holding a renderer by medium). Guard test
  `tests/test_production.py` (5, an offline round-trip through the real engine); all 31 green.
- [`0026-the-production-template.md`](0026-the-production-template.md)
  — **built** a one-command **board provisioner**
  ([`scripts/provision_production.py`](../../scripts/provision_production.py)) that stands up a
  new production to "where we are now" — the infrastructure sibling of the `ProductionProvider`
  (that seam *reads/writes* an existing board; this *stands one up*). The inherited **process**
  was already the org-level template for the board's *structure* (WITs, fields, the Shot-board
  cascade); this closes the **per-project** gap the `0025` session did by hand — area paths,
  a **team per department**, and each team's iteration + backlog-level visibilities — into one
  **idempotent** script (`DefaultAzureCredential` + stdlib `urllib`, non-secret pointers from
  `.env`). Detect-then-act with a **`--dry-run`** (validated against the live project, no
  changes) and an opt-in **`--with-example`** demo tree; the default is a clean, empty board.
- [`0027-board-to-board.md`](0027-board-to-board.md)
  — **built** the board-to-board binding — closed the top `0025` thread. `Engine` gained
  **`run_production(provider, *, scene=None)`**: read a `Brief` from a
  `ProductionProvider`, let the crew assemble a graded `Sequence`, and write it back — one
  call, board in → board out. The `provider` is reached only through the `runtime_checkable`
  Protocol (a `TYPE_CHECKING`-only import), so the engine stays backend-agnostic (local-folder
  ↔ ADO), the same swappability the `Renderer` seam gives the execution plane. Verified offline
  (guard test, 32 green) and live against the board.
- [`0028-the-production-cli.md`](0028-the-production-cli.md)
  — **built** [`scripts/produce.py`](../../scripts/produce.py), a thin CLI over
  `Engine.run_production`: run a production **board-to-board** from the shell and print the
  assembled timeline. Defaults to the configured ADO board; `--local <path>` runs offline
  against a local-folder production; `--no-write` previews (assemble + print, no write-back).
  Closes the `0027` board-to-board-CLI thread; validated offline and live.
- [`0029-proof-of-output.md`](0029-proof-of-output.md)
  — **verification** (no `sequitur/` code): stopped describing and *produced*. Rendered a real
  **still** (`gpt-image-1`, a 2.0 MB grammar-legible PNG) and — for the **first time ever** — a
  real **video** (**Gemini Omni**, a 2.1 MB `ftyp isom` MP4; the Key-Vault-held Gemini key
  authenticated on its first live call). All four renderers now produce real bytes (still, video,
  voice `0011`, board-to-board assemble `0027`). Repurposed the un-deletable **Test** work-item
  types as the board's **QC / acceptance layer** — a Test Plan "Output Verification" with a passing,
  evidence-backed Test Case per renderer. Verdict: **not spinning yarn**.
- [`0030-the-phase-axis.md`](0030-the-phase-axis.md)
  — **board design + infrastructure:** closed the phase axis `0024` deferred. Reframed
  Act→Scene→Beat→Shot as a **multi-department** decomposition (each level's granularity =
  one department's atom, but every level is worked by several — Beat is the **rhythm** level
  co-owned by Editor + Composer, so *sound aligns to Beat*), which dissolves the Beat/Shot
  conflation. Gave the three **production phases** a board-native home: **named, dateless
  iterations** (`1 🎬 Pre-Production` / `2 🎥 Production` / `3 ✂️ Post-Production`) with every
  team subscribed, so each crew gets a Pre/Prod/Post switcher. Phase is the **iteration** axis
  (orthogonal — never a work-item parent above Act; iteration is the only axis with a board
  experience). A load-bearing leading **digit** pins ADO's alphabetical dateless-`current` pick
  onto Pre-Production (emoji is decoration). Baked into the provisioner template and run live.
- [`0031-the-director-seat.md`](0031-the-director-seat.md)
  — **agent-customization:** answered *what executes the direction* — the conversational agent
  takes the **Director** seat and the crew become **dispatchable subagents** (`.github/agents/`),
  the **PersonaJudgment (B)** tier beside `sequitur/`'s deterministic **HeuristicJudgment (A)**.
  Built `director.agent.md` (grounded in Directing — interprets the brief, dispatches the crew,
  reconciles their disjoint slices into a `Shot`, reports back for greenlight) + `cinematographer.agent.md`
  (DP — grounded in Grammar of the Shot, returns a typed `Contribution`). **Proved live** (a
  lighthouse brief → a valid, vocabulary-bound camera Contribution → a reconciled `Shot`). Settled
  the grounding style as **persona-bound** (free judgment, output constrained to the code's closed
  enums; subagents not wired into the Python). Every `crew/<role>.py` gets a `<role>.agent.md` twin.
  No `sequitur/` code changed. **Follow-up:** added `gaffer` (electric) + `keygrip` (grip) so the
  Director can dispatch a **full shoot crew** (camera/electric/grip) — all three proven live on a
  shared brief, reconciling into one conflict-free `Shot`.
- [`0032-the-execute-hook.md`](0032-the-execute-hook.md)
  — **built** the `0031` "wire execution" thread: gave the `Director` an **execute-hook** —
  `Director.execute(shot, *, medium=Medium.VIDEO, out_path=None)` resolves the producer for the
  medium from the renderer registry (`0021`) and renders a greenlit `Shot` to **real bytes**
  (video = Gemini Omni, still = `gpt-image`), closing **decision → pixels** in-process. The hook
  lives on the Director (the Engine stays the dumb dispatcher), goes through the `Medium`-keyed
  registry (backend-agnostic, no import cycle), and reuses existing seams — one method, no new
  export, no new dependency. Guard test (`tests/test_engine.py` now 6; suite 33 green) proves the
  greenlit Shot reaches the producer untouched; the Director agent's "don't render" constraint
  became "don't render *before greenlight*" (on greenlight it runs the hook). The B (persona) and
  A (code) tiers now share one decision → pixels path.
- [`0033-architecture-reconciled.md`](0033-architecture-reconciled.md)
  — **docs:** brought [`context/architecture.md`](../architecture.md) up to the pivot. The doc
  still opened with "one department in one phase," framed post as "the next layer," and called
  the runtime model "not yet built." Added a first-class section — **The two Judgment tiers:
  `sequitur/` (A) and `.github/agents/` (B)** — with a diagram, naming the `0031`–`0032` pivot
  (`sequitur/` = A tier + schema + execution + seams; the agents = B tier; the conversational
  agent = the Director; `Director.execute` closes decision → pixels). De-staled the phase-table
  status, the runtime section (`ProductionProvider` + ADO board **built** `0024`–`0028`,
  platform **resolved**), and the open decisions. No `sequitur/` code changed.
- [`0034-the-assemble-crew.md`](0034-the-assemble-crew.md)
  — **agent-customization:** expanded the persona (B) tier from the shoot crew to the
  **assemble crew** — `editor.agent.md` (the cut — grounded in Grammar of the Edit, owns
  `Transition`/`EditReason`/`EditCategory`) and `colorist.agent.md` (the look — grounded in the
  Color Correction Handbook, owns `Look`/`Cast`/`TonalRange`, choosing a `look` the code compiles
  into a `Grade`). **Proved both live** on one assemble brief (a graveside vigil): the Editor
  returned a valid fade-in-then-cuts sequence with named motivators, the Colorist `look: COOL` —
  disjoint fields that reconcile exactly as `Director.assemble` does. Every `crew/<role>.py` with
  enums now has its `<role>.agent.md` twin; the **plan seats wait on their code twin**
  (`crew/screenwriting.py` + a storyboard role aren't built). No `sequitur/` code changed.
- [`0035-the-screenwriter-seat.md`](0035-the-screenwriter-seat.md)
  — **code:** built [`sequitur/crew/screenwriting.py`](../../sequitur/crew/screenwriting.py) —
  the **plan-phase** `Screenwriter` (new `Department.STORY`) over *The Screenwriter's Taxonomy*
  as a **layered descriptor vector**: `MovieType` + closed 11-value `Supergenre` (Ch. 2), a
  curated 50-value `Macrogenre` + open microgenre `str` tag (Ch. 3), a `Voice` **struct** of six
  axes (Ch. 5), the closed 20-value `Pathway` (Ch. 6), and POV as three enums `Scope`×`Focus`×
  `Stance` (Ch. 7). Vocabulary + a neutral-descriptor heuristic — the plan analogue of `0012`'s
  camera re-seating, grounded from the abridged source. Kept **out of `full_crew()`** (a story
  descriptor isn't `Shot`-reconcilable — a plan-phase reconcile is a later pass); added
  `plan_crew()`. Guard test `tests/test_screenwriting.py` (5); suite **38 green**. **Follow-up:**
  added `screenwriter.agent.md` (the persona **B** twin now that the code seat exists) — grounded
  in the Taxonomy, bound to the enums; **proven live** (a neo-noir heist premise → `CRIME` /
  `HEIST_CAPER`+`REVENGE_JUSTICE` / `NOIR` / `LIMITED`·`PRIMARY`·`SUBJECTIVE` / `VOICEOVER`).
- [`0036-the-interactive-production.md`](0036-the-interactive-production.md)
  — **product design / vision** (no code): reframed the studio's *experience* from a batch
  "ramrod" (`run_production`, one pass, dislike → restart) to the **dailies model** — an
  **interactive, phase-gated, iterative** production where each phase emits a **Producer-reviewable
  deliverable** (treatment + **poster** → storyboard/shot list → dailies → rough/final cut) and the
  human **approves or revises that phase** before spend flows on. Reversed the "never emits a
  screenplay" stance: human-readable artifacts are the **cheapest checkpoints**. It's an
  **evolution, not a teardown** — Producer greenlight (`0008`), phase axis (`0030`), board-as-instance,
  and the conversational Director (`0031`) already imply it; `run_production` (`0027`) survives as the
  batch/CI path. New pieces on the critical path: the **`OutputStore`** (`0005`, finally), a
  **deliverable+gate ritual**, a **Screenwriter treatment** (Directing Ch. 3–11), a **Production
  Designer seat + key-art source**. First slice: **plan → {treatment + poster} → gate**.
- [`0037-the-production-parameterized.md`](0037-the-production-parameterized.md)
  — **code:** made the **Production** a first-class parameter (one ADO project = one Production).
  `ADO_PROJECT` was a fixed value; now the project is an **argument** (explicit › `.env` default)
  threaded `config.get_ado_config(project=…)` → `AzureDevOpsProduction(project=…)` →
  `scripts/produce.py --production NAME`, plus `AzureDevOpsProduction.list_productions()` /
  `produce.py --list-productions` to enumerate the org's productions (live-verified). `ADO_ORG_URL`
  and the process template stay studio-wide constants. The prerequisite for the multi-production
  dailies world (`0036`); guard test added, suite **39 green**, single-production default unchanged.
- [`0038-the-output-store.md`](0038-the-output-store.md)
  — **code:** built the long-deferred **`OutputStore`** seam (`0005`) — the studio's **data
  plane**, the sibling of the `Renderer` (execution) and `ProductionProvider` (control) seams.
  A `runtime_checkable` `OutputStore` Protocol (`put(artifact, *, production, layer, name) ->
  Path | str`; `artifact` = raw bytes **or** a rendered path) + one `LocalFolderOutputStore`
  backend that files at `<root>/<production>/<layer>/<name>`. With `OUTPUT_STORE_ROOT` pointed
  at the OneDrive-synced folder, this one disk backend is already the **durability bridge** — no
  API code, no new dependency (just `shutil`/`pathlib`); a `GraphOutputStore` (SharePoint
  share-URL refs) swaps in behind the same protocol later. `config.get_output_store_root()`
  resolver; guard test `tests/test_output.py` (6); **live-verified** through the real OneDrive
  root; suite **45 green**. The `0036` dailies model's data plane now exists — next is the
  deliverable + gate ritual that links a stored `ref` onto the board.
- [`0039-render-then-persist.md`](0039-render-then-persist.md)
  — **code:** wired the execute-hook to the output store, closing **decision → pixels →
  durable**. `Director.execute` gained an optional `store` (+ owning `production`, a `phase`):
  it renders to a scratch path as before, then files that artifact through `OutputStore.put`
  and returns a `RenderResult` whose `ref` is the **durable** location (render-only behaviour
  unchanged when no store is passed; a store without a production raises). The dailies model's
  render→persist step; tests in `tests/test_engine.py` (now 8, offline); suite **47 green**.
  Next: the deliverable + gate ritual that consumes the durable ref.
- [`0040-the-gate.md`](0040-the-gate.md)
  — **code:** built the **deliverable + gate** model, the dailies model's review checkpoint
  (`0036`). `sequitur/gate.py`: an immutable `Deliverable` (production · `Phase` · durable `ref`
  · `GateStatus` pending/approved/revise) with `approve` / `revise` transitions returning new
  versions, and a `Gate` that binds a production to an `OutputStore` and `submit`s an artifact —
  filing it durably under `<production>/<phase>/` and returning a **pending** deliverable ready to
  present. Persists the artifact, not (yet) the verdict — the board State-write is next. One gate
  serves every phase (bytes or a produced path). `tests/test_gate.py` (4, offline); suite **51
  green**. The plan → {treatment + poster} → gate slice is now down to building the two producers.
- [`0041-staging-directing-the-story-and-production-design.md`](0041-staging-directing-the-story-and-production-design.md)
  — **grounding decision / plan** (no code, no `source/` yet): lock the choice to pull in two new
  *plan*-phase sources ahead of delivery — Francis Glebas' **_Directing the Story_** (its
  **storytelling** half only, dropping the storyboarding half as redundant with Paez & Jew) to
  supplement the **Director** and **Screenwriter** (a cross-cutting reference, **no new `crew/`
  module**), and a dedicated **production-design** text (recommended: Rizzo's *Art Direction
  Handbook*) to finally seat the **Production Designer** — the 8th grounding gap `0036` flagged.
  Records the filtering discipline, seat mappings, overlaps, and the "one book per abridgement
  session / copyright gate / extract-on-demand" process; import + mapping happen at staging when the
  Producer's deliverables land. These two unblock the `0036` first slice's two plan producers.
- [`0042-staging-directing-the-story.md`](0042-staging-directing-the-story.md)
  — **grounding / staging** (no code): executed the `0041` plan for the first of its two books.
  The Producer delivered **_Directing the Story_**'s **storytelling half** — **10 chapters**
  (5–13, 15; ch. 14 intentionally omitted, the intro + storyboarding halves dropped at source as
  redundant with Paez & Jew). Untangled a mislabeled first delivery (byte-identical duplicates:
  `CH-10`=Ch. 11, `CH-13`=Ch. 15; the Producer re-extracted the real 10 & 13), **converted →
  gated → mapped**: verbatim `source/` (media-stripped, `<img>` tags kept), `git check-ignore`
  confirmed, and a chapter→seat [`INDEX.md`](../../artifacts/directing%20the%20story/INDEX.md)
  grounding the **Director** + **Screenwriter** (no new `crew/` module). Catalog row → **Imported ·
  staged**; architecture's Screenwriter + Director cells now cite Glebas. **`reference/`
  abridgement deferred** to its own session (the `0015` line held). Library = **8 sources** (7
  abridged, 1 staged); the naming guard (`directing the story/` ≠ `directing/`) holds.
- [`0043-abridging-directing-the-story.md`](0043-abridging-directing-the-story.md)
  — the **dedicated abridgement session** `0042` deferred (no code): transformed *Directing the
  Story*'s **10-chapter storytelling half** from verbatim `source/` into **10 session-ready
  `reference/` chapters** via **three parallel subagents** (the `0017`/`0018` pattern, clustered by
  arc: structure & remit 5/6/12 · directing the eye 7/8/9 · meaning/irony/heart/synthesis
  10/11/13/15). Each ends in a **Studio application** section; all cross-links verified to resolve
  (10/10). Grounds the **Director** + **Screenwriter** — **no new `crew/` module** (all three
  subagents confirmed the `0041` call). Key through-lines: Glebas' story spine / "aim at the heart"
  is the human-readable **treatment** payload the Taxonomy descriptor can't narrate; Ch. 6 & 13 are
  the clearest corpus yet for the Director `PersonaJudgment` (**B** tier); dramatic irony (Ch. 11)
  is the open-information case of POV, timed by the Editor. Catalog + architecture flipped **staged
  → abridged**; the INDEX now links each chapter. Library = **8 sources, all abridged**; the still-
  raw **Art Direction Handbook** (Rizzo) is the last source gap.

- [`0044-staging-the-art-direction-handbook.md`](0044-staging-the-art-direction-handbook.md)
  — **staged** Michael Rizzo's **_The Art Direction Handbook for Film & Television_** (2e), the
  **last outstanding source gap** (no code): converted the Producer's **8 `.docx` chapters** to
  verbatim `source/` (`pandoc -t gfm --wrap=none --extract-media`, `CH-NN.md`), gated (`source/` +
  `extraction/` gitignored), and mapped each chapter to the **Production Designer** seat in a source
  `INDEX.md`. Fought the **misnamed-OLE2 defect** across three re-extractions — a legacy `.doc`
  payload (magic `D0 CF 11 E0`) behind a `.docx` name that pandoc can't read; the bad chapter *moved*
  (CH-04, then CH-03) until a clean re-extract produced eight valid OOXML files. The book is an
  O'Reilly export (bold-linked chapter titles, `<img>` tags kept / media bytes stripped).
- [`0045-abridging-the-art-direction-handbook.md`](0045-abridging-the-art-direction-handbook.md)
  — the **dedicated abridgement session** `0044` deferred (no code): transformed all **8** verbatim
  chapters into **8 session-ready `reference/` chapters** via **three parallel subagents** by arc
  (remit & department 1/2 · design core 3/4/7 · physical/historical/logistics 5/6/8). Each ends in a
  **Studio application** grounding the *planned* **Production Designer** seat over
  [`ImageStudio`](../../sequitur/image.py); all cross-links verified to resolve (8/8). **Closes the
  last source gap — nine sources, all abridged.** Catalog + architecture (Production Designer cell) +
  INDEX flipped **staged → abridged**. A follow-on hygiene pass scrubbed real Azure infra identifiers
  (account name, resource group) from the shipped docs, keeping the KV secret *names* as functional
  `config.py` defaults.
- [`0046-the-production-designer.md`](0046-the-production-designer.md)
  — **built** the **Production Designer** (the last unbuilt crew seat), grounding the just-abridged
  Rizzo into code: a plan-phase, vocabulary-only `ProductionDesigner` role
  ([`crew/production_design.py`](../../sequitur/crew/production_design.py)) in a new
  **`Department.ART`**, owning `ConceptStance`/`MediumLook`/`EraMarker`/`SetKind` + an open
  `visual_concept` (the central metaphor the heuristic leaves blank for the persona) and `motifs`.
  Its `Contribution` is a **design descriptor**, not a `Shot` — added to `plan_crew()` beside the
  Screenwriter, kept out of `full_crew()`; `test_production_design.py` (5), suite 10 modules green.
  A persona twin ([`production_designer.agent.md`](../../.github/agents/production_designer.agent.md))
  + a Director plan-dispatch step make **seven agents** beside the Director. Seams: PD owns the
  *concept*, [`build_prompt`](../../sequitur/prompt.py)/[`ImageStudio`](../../sequitur/image.py) the
  *realisation* (Rizzo Ch. 1); era = design intent, grade = the Colorist (overlap logged); only design
  intent transfers (no build/scout). **Every modeled department now has a code seat + twin.**
- [`0047-the-plan-phase-reconcile.md`](0047-the-plan-phase-reconcile.md)
  — **built the plan-phase reconcile** (the last of three): a new **`Plan`** aggregate
  ([`plan.py`](../../sequitur/plan.py)) — the plan analogue of `shot.py`/`edit.py` — holding the
  reconciled `story` (Screenwriter) + `design` (Production Designer) descriptor halves, plus
  `Director.plan` (groups each seat's disjoint slice, loss-free) and `Engine.plan` (mirrors
  `run`/`assemble`). With every phase now reconcilable, **`full_crew()` spans all three**
  (plan → `Plan`, shoot → `Shot`, assemble → `Sequence`); the `0035`/`0046` "kept out of full_crew"
  caveat is resolved. A `Plan` is *not* renderable — its outputs are the dailies **treatment** (story)
  + **poster** (design). `test_engine.py` 8 → 10; suite 10 modules green. (Sound's `Composer` +
  toaster-strudel MCP deferred until the baseline pipeline is proven.)
- [`0048-the-keyartist-skill.md`](0048-the-keyartist-skill.md)
  — **built the KeyArtist as a Skill, not a Role** — the first **generalist-under-direction** seat.
  A theatrical one-sheet (key art, *with* type) is graphic-design/marketing, not production design, so
  it grounds on **no source** (poster design is general model competence) and lives as
  [`.github/skills/keyartist/`](../../.github/skills/keyartist/) (`SKILL.md` persona + a bundled arm) +
  a deterministic `build_key_art_prompt` composer. Proven live via **invocation pattern (a)**: a
  subagent reads the skill, returns a directive, the tool-holder renders. Empirical: `gpt-image` renders
  **headline** type (title/tagline) legibly, garbles fine print (billing off by default). **Copy
  ownership settled:** title + tagline are the **Screenwriter's** (thematic compression); the KeyArtist
  only *houses* them — its two parents are the PD (look) + Screenwriter (words).
- [`0049-the-assistant-director.md`](0049-the-assistant-director.md)
  — **closed the control-plane gap** (nothing was hitting the board): the `ProductionProvider` gains
  `report`/`fetch_reports` on both backends — a live ADO `Deliverable` work item per deliverable (text →
  Description = the RAG substrate, image → attachment, gate verdict → State). The **AD/PA** is the second
  Skills seat ([`.github/skills/assistant_director/`](../../.github/skills/assistant_director/)) — the
  **Mediator** that owns board I/O so craft seats never touch ADO; two directions (report up / fetch
  down = board-as-memory). Proven live on `TheLaunch` (treatment + one-sheet → board items #13/#14).
  `test_production` 7 → 10; suite green.
- [`0050-board-record-remediation.md`](0050-board-record-remediation.md)
  — **fixed the thin board record** (Producer critique): deliverables landed placeless. `Deliverable`
  gains `author` + `department`; `report()` now sets **AreaPath** (department), **IterationPath** (phase,
  via a `_PHASE_ITERATION` map), an **author tag** (seats aren't ADO identities), and a real **https
  Hyperlink** (a `config.store_url()` path→SharePoint mapper via `OUTPUT_STORE_URL_BASE`) — no more
  filepath strings. Added **Story + Art** departments to the provisioner (the plan seats had no area).
  Reprovisioned `TheLaunch`, re-ran the AD: verified `treatment → Story/Pre-Production/Screenwriter` +
  `key art → Art/Pre-Production/KeyArtist` with attachment + SharePoint link. The record is right; the
  **content coherence** (treatment ↔ key art) is the next pass.
- [`0051-reports-as-events-unfold.md`](0051-reports-as-events-unfold.md)
  — **the coherent re-run, on the record.** Fixed the two `TheLaunch` failures: *separate chambers*
  (key art dropped the protagonist) and *the vacuum* (plan ran in chat, no board trace). Coherence by
  **threading** (not prompting): Screenwriter authors treatment first → Production Designer seeded with
  the *treatment* → KeyArtist seeded with all three → a one-sheet that agrees with the film (Mara the
  subject, her hand to the crayon sun, Sol as glow). And the **AD/PA reports each department as it
  lands** — Story (copy/treatment), Art (concept/directive/key art) → 5 placed/authored/linked board
  items, a live audit trail (answers "how would I know you didn't cook it"). Found the **publish race**:
  the ADO attachment is instant/authoritative, the SharePoint hyperlink eventually-consistent (Tier-0
  sync) → **`GraphOutputStore`** queued as the real fix. Threading is orchestration now; the `Plan`-
  carries-treatment code seam is the future automation step.
- [`0052-the-cut-and-the-marketing-plane.md`](0052-the-cut-and-the-marketing-plane.md)
  — **a schema revision from a board-visibility bug.** `Deliverable` items weren't showing on any board:
  root cause = the WIT was mapped to **no backlog level**. Chasing *why* surfaced two film-craft
  categories the schema had conflated/omitted — **three planes**: *diegetic* (the work), *production
  deliverables* (the film **becoming** — treatment/storyboard/dailies/cut, trace to the tree), and the
  **campaign** (key art / one-sheet — *about* the film, for the market — a different plane, not a missing
  leaf). Built: a new **`Cut`** WIT — the **diegetic crown** (`Cut → Act → Scene → Beat → Shot`),
  editorial's landing node, the board analogue of the code's edit `Sequence` — on a new **Cuts**
  portfolio level; a **`Marketing Asset`** WIT (the campaign plane) under a new **Marketing** area; and
  `Deliverable` + `Marketing Asset` mapped to the **Requirement** level (the visibility fix; boards
  separated by Area Path). The org **process template is now codified** — new
  [`scripts/provision_process.py`](../../scripts/provision_process.py) declares WIT types + icons/colours
  + states + level mappings and applies them idempotently (heals drift), the sibling to
  `provision_production.py`. `production.py`/AD routing file campaign artifacts as `Marketing Asset`.
- [`0053-the-graph-output-store.md`](0053-the-graph-output-store.md)
  — **closed the `0051` publish race.** A second `OutputStore` backend, **`GraphOutputStore`**, uploads a
  produced artifact's bytes to SharePoint/OneDrive **directly over Microsoft Graph** and returns the
  item's **`webUrl`** — authoritative the instant the upload returns (no dependence on the OneDrive sync
  client, unlike Tier-0's eventually-consistent link). Same `OutputStore` protocol (the `Path | str` ref
  `0038` designed in), `DefaultAzureCredential` on the Graph scope + stdlib `urllib` (no new dep), lazy
  `__init__` (offline-safe). Config = non-secret `GRAPH_DRIVE_ID` (+ optional `GRAPH_STORE_ROOT_PATH`).
  `test_output` covers it via a stubbed upload; 11-module suite green.

- **Code:** `sequitur/` package (`crew/` · `shot`, `plan`, `prompt`, `studio`, `image`,
  `speech`, `edit`, `cutter`, `grade`, `grader`, `lut`, `render`, `production`, `output`, `gate`, `config`) + CLIs
  `scripts/generate.py` (render a shot) · `scripts/produce.py` (run a production board-to-board) + tests
  (`tests/test_prompt.py` · `test_edit.py` · `test_engine.py` · `test_render.py` ·
  `test_grade.py` · `test_production.py` · `test_output.py` · `test_gate.py` · `test_screenwriting.py` · `test_production_design.py`). The Bowen vocabulary lives under **`crew/`** (`0012`): a  thin `Role` base (`crew/role.py`) with three shoot-phase roles — `Cinematographer`
  (`crew/camera.py`), `Gaffer` (`crew/lighting.py`), `KeyGrip` (`crew/grip.py`) — each
  *owning* its slice of the grammar enums (the old flat `grammar.py`, un-flattened),
  plus the assemble-phase `Editor` (`crew/editorial.py`) and `Colorist`
  (`crew/colorist.py`, `0022`) and the plan-phase `Screenwriter` (`crew/screenwriting.py`,
  `0035`, vocabulary-only). Roles now have **behaviour**
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
  `artifacts/INDEX.md`. **Nine abridged sources** now — spanning every department the
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
  **Colorist** built `0022`, **10 abridged chapters** + INDEX, `0020`), and *Directing
  the Story* (Glebas — visual storytelling / the story→image bridge, the storytelling
  half, **10 abridged chapters** + INDEX, `0043`; supplements the **Director** +
  **Screenwriter**, no new `crew/` module — `directing the story/` ≠ Rabiger's
  `directing/`), and *The Art Direction Handbook* (Rizzo — production design, grounding the
  planned **Production Designer** seat over [`ImageStudio`](../../sequitur/image.py), **8 abridged
  chapters** + INDEX, `0045`; closed the last source gap). Each source
  holds the raw book (`extraction/` .docx, `source/` .md — gitignored) and the
  abridged, session-ready `reference/` with a per-source `INDEX.md` (chapter → code
  map). Each abridged chapter ends with a "Studio application" section.
- **Architecture:** `context/architecture.md` maps phase → department (Appendix D)
  → grounding source → code layer, plus **the pivot** (`0031`, reconciled into the doc
  `0033`): the crew engine's swappable `Judgment` has **two concrete tiers** —
  deterministic **code** (`sequitur/`, A = schema + execution + seams) and persona
  **agents** (`.github/agents/`, B), with the **conversational agent as the Director**.
  Built today: the **shoot** crew (camera/grip/electric) and the **assemble** crew
  (Editor + `Colorist`, `0022`–`0023`) both decide via the crew engine; the **renderer
  seam** (producers video/image/voice/film + a second **operator** plane whose first
  member is the color **`Grader`**); `Director.execute` closes **decision → pixels**
  (`0032`); and a live **Azure DevOps** production board the engine runs board-to-board.
  Remaining seats: plan-phase (Screenwriter / Storyboard Artist) + the sound department.
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
- **Output verified (`0029`):** all four render backends produce real bytes — still
  (`gpt-image-1` PNG), **video (Gemini Omni MP4 — headline premise, proven on the first live
  call)**, voice (Azure Speech WAV, `0011`), and a board-to-board assembled `Sequence` (`0027`).
  The board's **Test** types are the QC layer (a "Output Verification" Test Plan, one passing case
  per renderer).
- **Production model (decided `0005`; board built `0024`, provider bound `0027`):** the
  engine is singular and evolves here; a *production* is external **content** (not a repo
  fork), modeled as a plan whose buckets = layers, each holding seeds/history *in* the
  plan and guidance/output *by reference*. The engine is a **driver client** reading
  through a `ProductionProvider` seam and writing via an `OutputStore` seam. The
  **production board is now backed by Azure DevOps** (`0024`: a custom Basic-derived
  process, Act→Scene→Beat→Shot hierarchy, departments as Area Paths, driven via the ADO
  MCP); the `ProductionProvider` *code* seam over it is **now built** (`0025`:
  [`production.py`](../../sequitur/production.py) — `read_brief` / `write_sequence`, a live
  `AzureDevOpsProduction` backend + a `LocalFolderProduction` test double). The board is also
  **operationalized** (`0025` addendum): the narrative levels are **Cuts → Acts → Scenes → Beats →
  Shots** (`0052` added the **`Cut`** crown — the complete assembled work, editorial's landing node;
  Shot sits on the Requirement tier so the crew's working leaf has a Kanban board), and
  each department is a **Team + Area Path** with its own board (the bucket), under
  a master all-departments team. The board also carries **three planes** (`0052`): the *diegetic*
  narrative tree, *production* **`Deliverable`** items, and *campaign* **`Marketing Asset`** items
  (key art) under a **Marketing** area — the review WITs share the Requirement level, separated by
  board via Area Path. A new production stands up to this state with one command
  (`0026`: [`scripts/provision_production.py`](../../scripts/provision_production.py) —
  idempotent, `--dry-run`/`--with-example`); the **org process template itself** is now codified too
  (`0052`: [`scripts/provision_process.py`](../../scripts/provision_process.py) — WIT types, icons,
  colours, states, backlog-level mappings, applied idempotently / drift-healing). The **phase axis** is
  on the board too (`0030`): three **named,
  dateless iterations** (Pre/Prod/Post) that every team subscribes to — a per-crew Pre/Prod/Post
  switcher — provisioned as part of the baseline template. Output bytes live
  in the **Sequitur Solutions** tenant's **SharePoint via Microsoft Graph** — both an
  eventually-consistent Tier-0 (`LocalFolderOutputStore` over a synced folder) and, since `0053`, an
  authoritative-URL **`GraphOutputStore`** (direct Graph upload).

## Open threads (keep fresh)

- **★ NORTH STAR — the interactive production / dailies model (`0036`, design).** Reframe the
  experience from a batch `run_production` ramrod to a **phase-gated, iterative** production: each
  phase emits a **Producer-reviewable deliverable** (plan → **treatment + poster** → previz board →
  shoot **dailies** → **rough/final cut**); the Producer **approves or revises that phase** before
  spend flows on, and the board persists each approved phase so *revise re-runs one phase, not the
  whole film*. An **evolution not a teardown** (Producer greenlight `0008`, phase axis `0030`,
  board-as-instance, conversational Director `0031` already imply it; batch `run_production` `0027`
  becomes the CI path). Critical-path pieces: **`OutputStore`** (`0005`, finally), a **deliverable+
  gate ritual**, a **Screenwriter treatment** (grounded Directing Ch. 3–11), a **Production Designer
  seat + key-art source**. **First slice: plan → {treatment + poster} → gate** (builds the
  `OutputStore` + gate ritual once, reusable everywhere).
- **Build the provider seams (`0005`)** — `ProductionProvider` **built** (`0025`):
  [`production.py`](../../sequitur/production.py) — a `runtime_checkable` protocol with
  `read_brief()` (board tree → `Brief`) / `write_sequence()` (graded `Sequence` → work
  items), a live **`AzureDevOpsProduction`** backend (ADO REST via `DefaultAzureCredential`,
  stdlib `urllib`, no new dep) and a **`LocalFolderProduction`** test double. The board's
  `Mood`/`Look` Shot fields and an example Act→Scene→Beat→Shot tree are in place, and the
  board is **operationalized** (`0025` addendum: per-department **Team + Area Path** boards
  under a master team; the narrative levels cascaded to **Acts→Scenes→Beats→Shots** so the
  Shot leaf has a Kanban board), and a new production stands up to this state with one command
  (`0026`). The engine is now **bound to the board** (`0027`): `Engine.run_production(provider)`
  runs a production board-to-board (read a `Brief` → assemble → write the `Sequence` back). Still
  to do: a **scene-scoped** WIQL tree read (the v1 read is flat/positional), **per-shot
  grade matching** so the write stops flattening distinct looks, writing work-item **State**
  (not just `Look`), and the **provider-side phase seam** (`0030` put the phase axis on the board
  as named Pre/Prod/Post iterations; still to build the `Phase → iteration` map, phase-scoped
  reads, and an `advance(shot, to=…)` verb, plus modelling non-camera deliverables — e.g. the
  upstream production-design reference frame — as their own phased items). The Graph-backed
  **`OutputStore`** is **built** (`0053`: `GraphOutputStore` — direct Graph upload, authoritative
  `webUrl`, closing the `0051` publish race); still to wire a live `GRAPH_DRIVE_ID` into a real run.
- **Acquire *Grammar of the Edit*** — **DONE** (`0007`): 8 chapters abridged into
  `artifacts/grammar of the edit/reference/`. Next is building the post layer it
  grounds.
- **Build the crew engine — phase A (`0008`)** — **in progress:** vocabulary re-seated
  under `crew/` — `Cinematographer`/`Gaffer`/`KeyGrip` (`0012`) and `Editor` (`0013`);
  **behaviour** added (`0014`) — `Judgment`/`HeuristicJudgment`, `Brief`/`Contribution`,
  `Director`, and a dumb `Engine` that assembles a shoot-phase `Shot`. **Assemble-phase
  behaviour built (`0023`):** `Engine.assemble` + a phase-aware `Director.assemble`
  reconcile the `Editor` (cut) and `Colorist` (base grade) into a graded edit `Sequence`.
  **Execution wired (`0032`):** `Director.execute` renders a greenlit `Shot` through the
  renderer registry to real bytes — decision → pixels closed in-process. Next: bind a
  **local-folder Production** (`0005` provider #1) in place of the bare
  `Brief`, a real cut-decision heuristic (Ch. 5 motivators) + per-shot grade matching
  (Ch. 9), then `PersonaJudgment` (**B**) and PM-board wiring.
- **Build the sound layer (`0009`)** — `SpeechRenderer` **built** (`0011`: Azure
  Speech on the existing account, no new resource / no
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
