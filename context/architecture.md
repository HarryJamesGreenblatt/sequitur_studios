# Sequitur Studios — production workflow architecture

The ultimate vision: not a prompt wrapper, but a **production studio** whose
workflow can fulfill every component requirement of a complete project. We model
that after how a real studio is organized — the crew **roles** of
[Appendix D](../artifacts/grammar%20of%20the%20shot/reference/appendix-d-crew-positions.md)
grouped into **departments**, working across the three **production phases**.

The design principle that ties it together:

> Each department/role owns a responsibility. Every responsibility is served by a
> **grounding source** (in the [grounding library](../artifacts/INDEX.md)) and a
> **code layer** (in `sequitur/`). A user can step into a role and the workflow
> hands them that role's grounded vocabulary and tooling.

Today the studio spans **two phases in code**: the *shoot* crew
(Cinematographer / Gaffer / Key Grip) composes a fully-grounded **shot**, and the
*assemble* crew (Editor + Colorist) reconciles a graded edit **sequence** — both
driven by a real **crew engine** (`Role` + swappable `Judgment`), bound to a live
**Azure DevOps** production board, and rendering **real bytes** across four media
(video, still, voice, film). The remaining seats (the plan-phase Screenwriter /
Storyboard Artist, the sound department) are grounded and scaffolded here.

This doc maps **three dimensions**: the **craft layers** (immediately below — *what*
the studio composes), the **runtime model** (further down — *how* a production is
represented, driven, and stored, decided in
[`storyline/0005`](storyline/0005-productions-as-instances-and-output-storage.md)),
and — the recent **pivot** — the **two Judgment tiers** that decide a layer:
deterministic **code** ([`sequitur/`](../sequitur/), tier A) and persona **agents**
([`.github/agents/`](../.github/agents/), tier B), with the **conversational agent as
the Director** (`0031`).

**The experience is pivoting to the *dailies model* (`0036`).** Rather than one batch
`run_production` pass that commits to the whole film at once, the studio is becoming
**interactive and phase-gated**: each phase emits a **Producer-reviewable deliverable**
(a treatment + poster → storyboard → dailies → cut), and the human **approves or revises
that phase** before spend flows downstream. The data plane this needs is now built — a
durable **`OutputStore`** (`0038`), a render→persist hook (`0039`), and the **deliverable
+ gate** model (`0040`) — so the runtime section below describes a pipeline of gated
deliverables, not a single pass.

## The craft layers, by phase

### Pre-production — *plan*

| Department / role (App. D) | Responsibility | Grounding | Code layer | Status |
|---|---|---|---|---|
| Producer | financing, scheduling, logistics | **Directing** Ch. 25 (line producing) · Ch. 37 (delivery) *(abridged, `0017`)* | **HITL — the human seat** (works the Production/PM board) | decided (`0008`) |
| Screenwriter | script, structure | **The Screenwriter's Taxonomy** (genre/voice/pathway/POV) *([abridged, 8 ch, `0016`](../artifacts/the%20screenwriter's%20taxonomy/INDEX.md))* + **Directing** Ch. 3–8 *(abridged, `0017`)* + **Directing the Story** (Glebas — story spine/structure/heart) *([abridged, 10 ch, `0043`](../artifacts/directing%20the%20story/INDEX.md))* | `Screenwriter` role · typed genre vocabulary (`crew/screenwriting.py`) | **role built — vocab (`0035`)** |
| Director | interpret script → shot selection | **Directing** Ch. 7–11, 17 (aesthetics, POV, style) *(abridged, `0017`)* + **Directing the Story** (Glebas — the story→image bridge, staging the eye) *([abridged, 10 ch, `0043`](../artifacts/directing%20the%20story/INDEX.md))* + Grammar of the Shot Ch. 1 | `Director` role (crew reconciler, `0014`) | partial (`Director`) |
| Casting · Actors | casting, performance | **Directing** Ch. 18–20 *(abridged, `0017`)* — **a new dimension** the architecture did not model | *(unmodeled — future role)* | new (`0015`) |
| Production Designer | sets, costume, color concepts | **Directing** Ch. 23 (visual design) *(abridged, `0017`)* + **The Art Direction Handbook** (Rizzo — art dept. & the design process) *([abridged, 8 ch, `0044`→`0045`](../artifacts/the%20art%20direction%20handbook%20for%20tv%20and%20film/INDEX.md))* | `ProductionDesigner` role · design vocabulary (`crew/production_design.py`) · `ImageStudio` (gpt-image) | **role built — vocab (`0046`)** |
| Storyboard Artist · Previs | previsualize the script → a shot-by-shot visual plan | **Professional Storyboarding** (Paez & Jew) *([abridged, 10 ch, `0018`](../artifacts/professional%20storyboarding/INDEX.md))* + Grammar of the Shot Ch. 1–3 | **reference keyframes** (`ImageStudio`) a video shot conditions on · a future `StoryboardArtist` role | grounded (`0018`); role planned |
| Assistant Director | schedule, coverage, shot list | **Directing** Ch. 24–26 *(abridged, `0017`)* + Grammar of the Shot Ch. 1 | shot list / coverage | planned |

### Production — *shoot*  ← **implemented (crew engine, `0012`–`0014`)**

| Department / role | Responsibility | Grounding | Code layer | Status |
|---|---|---|---|---|
| Director · DP · Camera Operator · AC | the shot: framing, composition, angle | Grammar of the Shot (Ch. 1–3) | `ShotSize`, `SubjectView`, `CameraAngle`, `ShootingStyle`, `Composition`, `FocalLength`, `DepthOfField` | **implemented** |
| Gaffer · Electric · Lighting Tech | lighting scheme & quality | Grammar of the Shot (Ch. 4) | `LightQuality`, `LightScheme`, `LightDirection`, `ColorTemperature`, `eye_light` | **implemented** |
| Key Grip · Grip · Dolly Grip | camera support & movement | Grammar of the Shot (Ch. 6) | `CameraMovement`, `MotionSpeed` | **implemented** |
| Sound Mixer · Boom Operator | production sound (diegetic capture) | Grammar of the Edit Ch. 3 + **Rose, *Producing Great Sound*** *([abridged, 18 ch](../artifacts/producing%20great%20sound%20for%20film%20and%20video/INDEX.md))* | `SpeechRenderer` (Azure Speech) + `SoundMixer` role — planned (`0009`) | partial |
| Script Supervisor · DIT | continuity notes, data, on-set color | Grammar of the Shot (Ch. 5) | feeds the edit layer | planned |

### Post-production — *assemble*  ← **now implemented (`0022`–`0023`)**

| Department / role | Responsibility | Grounding | Code layer | Status |
|---|---|---|---|---|
| Editor | cut, continuity assembly, pacing, transitions | **Grammar of the Edit** (Ch. 1–8, abridged) + **Directing** Ch. 30–34 *(abridged, `0017`)* + Grammar of the Shot Ch. 5 | **sequence / edit layer** (`edit.py` model + `cutter.py` executor) | grounded; code in progress |
| Colorist / DIT | grade, look | **Color Correction Handbook** (Van Hurkman) *([abridged, 10 ch, `0020`](../artifacts/color%20correction%20handbook/INDEX.md))* + Grammar of the Shot (Ch. 4 color) + **Directing** Ch. 36 (grade/finishing) *(abridged, `0017`)* | `crew/colorist.py` role + `grade.py` reified model + `lut.py` (ASC CDL → `.cube`) + `grader.py` *transform* (ffmpeg `lut3d`) | **implemented (`0022`–`0023`)** |
| Sound editor / mixer · Composer | sound design, score, mix | Grammar of the Edit Ch. 3 + **Rose** *(abridged)* + **Directing** Ch. 35–36 *(abridged, `0017`)* + **toaster-strudel MCP** (score) | `SpeechRenderer` (VO/ADR) · `Composer`→toaster-strudel · `SoundDesigner`/`ReRecordingMixer` — planned (`0009`) | planned |

### Delivery — *ship*

| Department / role | Responsibility | Grounding | Code layer | Status |
|---|---|---|---|---|
| Producer | marketing, distribution, exhibition | **Directing** Ch. 37 (getting it out there) *(abridged, `0017`)* | out of scope (for now) | grounded |

## Reading the map

- **Grammar of the Shot already spans the production phase** — camera, grip, and
  electric departments are encoded under `crew/` (re-seated from the old `grammar.py`,
  `0012`, as `Cinematographer`/`Gaffer`/`KeyGrip`). That is the studio's current
  reach: it can compose a single, fully-grounded **shot**.
- **The next layer is editorial/post — now grounded.** Bowen's companion
  **Grammar of the Edit** has been imported and abridged (8 chapters +
  [INDEX](../artifacts/grammar%20of%20the%20edit/INDEX.md)), so the *sequence* layer
  (which assembles multiple `Shot`s honouring 180°/30°, matching/reverse, eye-line,
  and screen direction; see
  [Ch. 5](../artifacts/grammar%20of%20the%20shot/reference/ch05-shooting-for-editing.md))
  can now be built on real grounding. The post-layer model (`edit.py`) + its MoviePy
  executor (`cutter.py`) are **built**, and the **assemble crew now runs** (`0023`):
  `Engine.assemble` + `Director.assemble` reconcile the `Editor`'s cut and the
  `Colorist`'s grade into a graded edit `Sequence` (the cut-decision heuristic is still a
  first pass — Ch. 5's six motivators are the next refinement).
- **Sound, story, and the director's craft are now sourced — and the whole grounding
  library is abridged.** **Sound is designed** (`0009`): a multi-phase department
  grounded by Grammar of the Edit Ch. 3 + **Rose, *Producing Great Sound*** *(abridged,
  18 ch — `0010`)* + toaster-strudel MCP, with `SpeechRenderer` / `Composer` /
  `SoundAnalyst` capabilities. **Both plan-phase sources are now abridged** (`0016`–`0017`):
  **The Screenwriter's Taxonomy** (a genre/voice/pathway/POV *classification system* →
  a future typed `Screenwriter` vocabulary) is **abridged** (8 ch, `0016`), and
  **Directing** (Rabiger & Hurbis-Cherrier — a Director-centric *spine* across every
  phase) is now **abridged** (28 ch, `0017` — a full comprehensive scan, nothing
  dropped), touching every seat from Screenwriter to Producer-ship. Directing also
  opens a **casting/actors** dimension the architecture had never modelled (Ch. 18–20,
  still unmodeled in code). Production design gains its first source (Directing Ch. 23),
  and finishing/grade a second (Ch. 36); a **dedicated design/color source is still
  open.** With five sources abridged, the library is **complete for the departments
  modelled today** — the next work is *code*, not grounding.
- **Previsualization is now sourced — a sixth abridged source (`0018`).** **Professional
  Storyboarding** (Paez & Jew — *[abridged, 10 ch](../artifacts/professional%20storyboarding/INDEX.md)*)
  grounds a seat the architecture had gestured at but never modelled: the **Storyboard
  Artist / previz** role. Its payoff is unusually concrete because Sequitur *is* a
  generative previs pipeline — a storyboard panel encodes the same grammar the DP owns
  (shot size, angle, composition, movement), so a board is a *pre-rendered* `Shot`, and
  a board panel is the literal form of the **reference keyframe** the video studio
  conditions a shot on (`ImageStudio`). It gives the long-deferred reference-keyframe
  flow a grounded home, and its Ch. 8 taxonomy maps a *continuity board* → the ordered
  `Shot` list, an *animatic* → the assembled edit, and *previs* → what `studio.py` + the
  edit layer produce. It **overlaps** existing sources from the board artist's upstream
  lens (Cinema Language/Staging ↔ Grammar of the Shot; Story Structure ↔ Taxonomy Ch. 6
  / Directing Ch. 5; Emotion ↔ Directing Ch. 10–11) — the plan-phase seat that *commits
  the shot grammar first*, which the shoot then executes.
- **Color grading is now sourced — a seventh abridged source (`0020`).** The
  **Color Correction Handbook** (Van Hurkman — *[abridged, 10 ch](../artifacts/color%20correction%20handbook/INDEX.md)*)
  closes the color gap flagged in [`storyline/0019`](storyline/0019-readiness-renderer-audit-color-gap.md):
  before it, color was only *borrowed* — the Gaffer's capture-time `ColorTemperature`
  (Grammar of the Shot Ch. 4) plus a paragraph of Directing Ch. 36. It grounds a future
  **Colorist** role in the post/finishing phase and its two renderer flavors: a
  *transform* **grade renderer** (LUT/curve over rendered clips — the `Cutter` plane
  under the coming `Renderer` protocol) and a *sensor/reader* **scope read** (waveform/
  vectorscope/histogram/parade) that backs a color **`validate()`** / broadcast-safe
  gate — the color counterpart of `Sequence.validate()` and the Rose sound-layer
  validate(). Scoped to **grading only**; production-design *concepts* stay a separate
  open cell (Directing Ch. 23). Its **lift/gamma/gain** primary vocabulary is the
  Colorist's first owned enum, and its Ch. 9 **shot matching** is the color analogue of
  the Editor's continuity check across a `Sequence`.
- **Overlaps to reconcile when the axes are encoded:** POV (Directing Ch. 9 ↔ Taxonomy
  Ch. 7 — craft vs. classification), structure/pathway (Directing Ch. 5 ↔ Taxonomy
  Ch. 6), **`ColorTemperature` in two seats** (Gaffer *capture* / in-camera white
  balance ↔ Colorist *grade* / re-balance — Color Correction Handbook Ch. 4), and the
  post chapters (Directing Ch. 30–34 ↔ Grammar of the Edit — the
  director's-eye complement to the editor's working manual). Directing Ch. 35 (music)
  overlaps Rose Ch. 14 + the toaster-strudel score seam.

## Runtime architecture — engine, instances, and stores

The tables above are the **craft dimension**: the layers of *what* the studio can
compose. Orthogonal to them is the **runtime dimension** — how an actual production
is represented, driven, and stored. Decided in
[`storyline/0005`](storyline/0005-productions-as-instances-and-output-storage.md); the
`ProductionProvider` seam and its Azure DevOps board (`0024`–`0028`) **and** the
`OutputStore` data plane (`0038`) are now **built** — a Graph/SharePoint `OutputStore`
backend and the board's **verdict-write** (linking a deliverable's `ref` + moving phase
State) are the remaining pieces.

- **Engine vs. instance.** `sequitur_studios` is a singular, evolving **engine**
  (`sequitur/` + [`artifacts/`](../artifacts/INDEX.md)). A *production* — a specific
  music video, short, or ad — is **not a repo fork**; it is external **content** that
  the engine drives as a **driver client**. One engine every production rides,
  instead of N frozen scaffolds differing only in seeds.
- **A production is a plan; its buckets are these same craft layers.** The two
  dimensions meet here: each department/layer above is a bucket in the production's
  plan, holding that layer's four **faces** —

  | Face | Shape | Home |
  |---|---|---|
  | Seeds | short structured input | in the plan |
  | History | append-only decisions/state | in the plan |
  | Guidance / bible | prose corpus (RAG) | doc store, *by reference* |
  | Output | media | blob store, *by pointer* |

- **Provider seams** keep the platform swappable — the engine reads and writes
  through two interfaces:
  - `ProductionProvider` — **built (`0025`)**: a `runtime_checkable` protocol
    (`read_brief` / `write_sequence`) over the board tree, with a live
    **`AzureDevOpsProduction`** backend (ADO REST via `DefaultAzureCredential`, stdlib
    `urllib`, no new dep) and a **`LocalFolderProduction`** test double. The platform
    question (`0005`) is **resolved — Azure DevOps** (`0024`): a custom Basic-derived
    process, Act→Scene→Beat→Shot hierarchy, departments as Area Paths + Teams, phases as
    named iterations. The engine runs it **board-to-board** (`Engine.run_production`,
    `0027`) with a CLI ([`scripts/produce.py`](../scripts/produce.py), `0028`).
  - `OutputStore` — **built (`0038`)**: a `runtime_checkable` protocol
    (`put(artifact, *, production, layer, name) → ref`; `artifact` = raw bytes or a
    rendered path) with a **`LocalFolderOutputStore`** backend. Its root
    (`OUTPUT_STORE_ROOT`) points at a **OneDrive-synced** folder in the Sequitur
    Solutions tenant, so this one disk backend already buys SharePoint/OneDrive
    durability — no API code, no new dependency. `ref` is a local `Path` today; a
    `GraphOutputStore` (share-URL refs via Microsoft Graph) swaps in behind the same
    protocol later (Azure Blob still deferred). `Director.execute(…, store=…)` files a
    render durably in one call (`0039`), and the **`Gate`** submits any phase's artifact
    to it (see *the dailies model* below).

- **Renderer seam** — the *backend* dimension, decided and first-built in
  [`storyline/0006`](storyline/0006-renderer-seam-and-image-backend.md). The
  **grammar is model-agnostic**; a **renderer** is the swappable thing that turns a
  `Shot` (seeds + guidance) into output, and the right backend follows the
  *deliverable's medium*, not the studio:
  - [`Studio`](../sequitur/studio.py) → **video** (Gemini Omni Flash).
  - [`ImageStudio`](../sequitur/image.py) → **still image** (Azure Foundry
    `gpt-image-1`) — the first non-Google backend; a Production-Designer deliverable
    and, more usefully, a **reference keyframe** a shot can be conditioned on.
  Both share one `Shot` and a `render() → (result, path)` contract;
  [`build_image_prompt`](../sequitur/prompt.py) is [`build_prompt`](../sequitur/prompt.py)
  minus the video-only faces (motion, speed, `single_scene`, audio). The seam should
  also admit **non-generative data APIs** (licensing, colour/reference lookups) for
  departments whose deliverable isn't a model output. The formal **`Renderer` protocol
  + medium-keyed registry** is now **built** ([`render.py`](../sequitur/render.py),
  `0021`): a `Medium` enum (video/still/voice/film), a `RenderResult(raw, ref)` pair,
  a `runtime_checkable` `Renderer` protocol, and a lazy `renderer_for(medium)` registry.
  The four producers were retrofitted onto it — `Studio` (video), `ImageStudio` (still),
  `SpeechRenderer` (voice), and `Cutter` (film, a *reducer*: n clips → one film) — so a
  role can now *hold* a renderer by medium instead of the CLI hard-wiring `Studio`. A
  **second plane** (`0022`) holds **operators** (`Transform`) — medium-preserving
  decorators over a producer's output (1 media in → 1 out), keyed by an `Operation` verb
  rather than an output `Medium`, because a colour grade *preserves* its input's medium
  and so can't be keyed by artifact kind. Its first member is the **`Grader`**
  (`Operation.GRADE`), built with the Colorist (`0022`) and made true-to-form in `0023`:
  it bakes the grade's primaries into a spec-correct `.cube` LUT via colour-science
  (`lut.py`, ASC CDL + Rec. 709 saturation) and applies it with ffmpeg `lut3d` (replacing
  the `0022` `eq`/`colorbalance` placeholder). `Composer`→Strudel and a
  non-generative `SoundAnalyst` (audio MIR) are the next backends to register.

- **Secrets via Key Vault.** Backend API keys are never stored in plaintext — they
  live in Azure Key Vault and are fetched at runtime via
  `DefaultAzureCredential` (the `az login` identity authorises the vault read). Only
  non-secret pointers (vault name, endpoint, deployment) live in `.env`.
- **MCP** is the eventual **control-plane** connector: sequitur as MCP *client*, the
  production/output stores fronted by MCP *servers* — added once there is more than
  one of anything to route between. It is never the byte path for media. **First
  concrete case (`0009`):** [`toaster-strudel`](https://github.com/HarryJamesGreenblatt/toaster-strudel)
  is already an MCP server (Strudel knowledge + Song-IR assembler + audio MIR);
  sequitur becomes its client for the `Composer`/`SoundAnalyst` roles — keeping the
  AGPL-3.0 Strudel engine at arm's length behind toaster-strudel's MIT MCP layer.

### The dailies model — phase-gated deliverables (`0036`–`0040`)

The runtime experience is evolving from a single batch `run_production` pass into an
**interactive, phase-gated pipeline** (`0036`): each phase emits a **deliverable** the
Producer reviews at a **gate**, and *revise re-runs that phase only*, not the film. The
pieces are built bottom-up:

- **Data plane — `OutputStore` (`0038`).** Produced bytes → a durable `ref`, filed under
  `production / phase / name`; the OneDrive-synced root makes the local backend durable
  today (see the seam above).
- **Render → persist (`0039`).** `Director.execute(shot, …, store=…, production=…)`
  renders to a scratch path, then files it via the store and returns a `RenderResult`
  whose `ref` is the durable location — the shoot phase's dailies, addressable and
  comparable across revisions.
- **The gate (`0040`) — [`sequitur/gate.py`](../sequitur/gate.py).** A `Gate` binds a
  production to an `OutputStore` and `submit`s any artifact (a shot render, a poster, an
  encoded treatment), returning an immutable **`Deliverable`** (`production` · `Phase` ·
  durable `ref` · `GateStatus` = pending / approved / revise). `approve()` /
  `revise(notes)` are version-producing transitions — a deliverable's life is a chain, so
  "revise → re-run → new version" is native. The gate persists the *artifact*; the
  *verdict* becoming a board State-write is the next step.

The **Producer's authority evolves** from a single greenlight into a **per-phase gate**
(still the human/HITL seat); the **phase axis** (named ADO iterations, `0030`) becomes the
pipeline's stages; and the **conversational Director** presents each deliverable and
captures the verdict in chat. The first slice is **plan → {treatment + poster} → gate**,
now down to building the two plan producers (a Screenwriter *treatment* output and a
Production Designer seat).

## The crew engine — roles as behavior, the Production as container

Decided in [`storyline/0008`](storyline/0008-the-crew-engine.md); makes the
department/role model *executable* rather than merely documentary. The table at the
top of this doc stops being a description and becomes objects.

- **Roles are classes; grammar stays enums.** Enums are the closed *vocabulary*
  (`ShotSize`, `LightScheme`, `Transition`). A **`Role`** (abstract base + concrete
  subclasses — `Cinematographer`, `Gaffer`, `KeyGrip`, `Editor`, …) is the *chooser*
  that **owns and wields a slice** of that vocabulary. `grammar.py`/`edit.py` enums
  get re-seated under the role that owns them — `grammar.py` today is a *flattened
  crew* (camera + electric + grip fused into flat enums); this un-flattens it.
- **Judgment is a swappable strategy (the A→B seam) — now with concrete homes.** A role
  delegates reasoning to a **`Judgment`**: `HeuristicJudgment` (**A**, deterministic, in
  [`sequitur/crew/`](../sequitur/crew/)) · `PersonaJudgment` (**B**, an LLM persona over
  the role's *scoped* grounding — realized as a **VS Code custom agent** in
  [`.github/agents/`](../.github/agents/), `0031`) · `HumanJudgment` (**HITL**). Same
  `propose()` signature, so any one role can be upgraded — or hand-driven — individually.
  See *The two Judgment tiers* below.
- **Three authority tiers.**
  - **Producer = HITL (the user)** — owns *what/whether* (brief, greenlight,
    approval), now as a **per-phase gate** (`0036`): approve or revise each phase's
    deliverable before spend flows on. This is the code analogue the Producer row
    lacked: **the human seat.**
  - **Director = agent** — owns *how*; reconciles the crew. Two faces (`0031`): the
    **conversational agent** *is* the acting Director (it dispatches the crew subagents
    and reconciles their disjoint slices), while the code `Director`
    ([`crew/director.py`](../sequitur/crew/director.py)) is the A-tier reconciler plus the
    **execute-hook** (`0032`). Agency lives in a component, never the container.
  - **Crew = role-components** — each decides its own concern in isolation.
- **The container is the Production, not a new `Unit`.** The dumb container is the
  `0005` **Production** (a plan whose buckets = department layers). It *encapsulates
  the crew*. This is Nystrom's Component Pattern in its data-oriented (ECS) form:
  **Entity = Production** (dumb per-instance data = the buckets), **behavior = the
  engine's Roles** (singular), **dumb dispatch = the engine** (driver-client). No
  film logic in the container or the dispatcher.
- **Behavior vs. state** (maps onto `0005`'s engine-vs-instance): role *behavior*
  lives in the singular **engine**; role *state* lives in the per-instance
  **Production** bucket, bound at runtime via the `ProductionProvider` seam.
- **The Production is the PM board — the keystone.** Its buckets are the
  `ProductionProvider`'s per-department items, so the Production *is* the
  Planner/ADO/GH-Projects board. The **Producer (human) works the board**; the
  **agent crew executes against its buckets**. Project state lives in the PM tool,
  as intended.
- **Phase = which crew is on call**, not a container. A Production moves through
  **plan → shoot → assemble** (the phase verbs above); one engine, one Production,
  phase-activated crews.
- **The renderer plane is unchanged.** `Studio`/`ImageStudio`/`Cutter` remain the
  *execution* plane; roles are the *decision* plane.

### The shape, in diagrams

**Structure — entity vs. behavior (Component / ECS).** The Production holds dumb
per-department data; the engine binds role *behavior*; the Director is itself a role;
the Judgment is a swappable strategy (heuristic → persona → human).

```mermaid
classDiagram
    class Production {
        «entity · PM board · dumb data»
        +buckets: Department to Bucket
    }
    class Bucket {
        +seeds
        +history
        +guidance_refs
        +output_refs
    }
    class Engine {
        «driver-client · dumb dispatch»
        +mount(production)
        +run(phase, context) Decision
    }
    class Role {
        «behavior · in engine»
        +concern
        +grounding
        +judgment
        +propose(context, bucket) Contribution
    }
    class Director {
        +reconcile(contributions) Decision
    }
    class Judgment {
        «strategy»
        +decide(role, context) Contribution
    }
    class HeuristicJudgment
    class PersonaJudgment
    class HumanJudgment
    Production o-- Bucket
    Engine --> Production : mounts
    Engine o-- Role : binds crew
    Role <|-- Director
    Role o-- Judgment
    Judgment <|-- HeuristicJudgment
    Judgment <|-- PersonaJudgment
    Judgment <|-- HumanJudgment
    Role ..> Bucket : reads seeds/guidance · writes history/output
```

**Authority & data flow — the Producer works the PM board; the crew executes
against its buckets; the Director reconciles.**

```mermaid
flowchart TB
    PROD["Producer — HITL"]
    subgraph BOARD["Production = PM board (Planner / ADO / GH Projects)"]
        BC["Camera bucket"]
        BE["Electric bucket"]
        BG["Grip bucket"]
        BED["Editorial bucket"]
    end
    subgraph ENG["Engine (singular driver-client) — dumb dispatch"]
        DP["Cinematographer"] --> DIR["Director (reconciler)"]
        GAF["Gaffer"] --> DIR
        GRP["Key Grip"] --> DIR
    end
    PROD -->|"brief · greenlight · approve"| BOARD
    ENG -->|"read seeds/guidance"| BOARD
    DIR -->|"write decision → history/output"| BOARD
```

### The two Judgment tiers — `sequitur/` (A) and `.github/agents/` (B)

The **pivot** of [`storyline/0031`](storyline/0031-the-director-seat.md): the crew
engine's swappable `Judgment` gets two concrete runtime homes, and the three authority
tiers get concrete seats. `sequitur/` stops being "the studio" — it is the **A tier +
schema + execution + seams**; the agents are the **B tier**; the conversational agent is
the **orchestrator**.

- **Tier A — `sequitur/` (code).** `HeuristicJudgment` — deterministic, offline,
  no-persona. Owns the **enum schema** (the closed answer space every seat chooses from),
  the **execution** plane (`build_prompt` → renderers; the `Grader` transform), and the
  **seams** (`Renderer`, `ProductionProvider`). The always-available fallback for
  tests / CI / no-network.
- **Tier B — `.github/agents/` (personas).** `PersonaJudgment` — every `crew/<role>.py`
  gets a `<role>.agent.md` twin (a VS Code custom agent). A subagent reasons **freely**
  from its `reference/` grounding but its output is **bound to the code's closed enums**
  (single source of truth = `crew/`). The two are the *same seat's* two strategies —
  nothing is duplicated: the code twin owns *vocabulary + heuristic default*, the agent
  twin owns *grounded judgment*. Built + proven live: the **shoot** crew
  (`cinematographer` · `gaffer` · `keygrip`), the **assemble** crew (`editor` ·
  `colorist`), and the **plan** seat (`screenwriter`) — every seat that has a code twin
  (`0034`–`0035`).
- **The Director is the conversational agent, not a subagent.** Producer = the human
  (HITL); Director = the orchestrating conversational agent (interprets the brief,
  dispatches the crew subagents, reconciles their disjoint field slices into a `Shot`,
  reports back for greenlight, and — on greenlight — runs the execute-hook); Crew =
  dispatchable department subagents. The Director suffers session amnesia, so the
  **devlog is its continuity** — the through-line of directorial intent.
- **Decision → pixels is closed (`0032`).** `Director.execute(shot, medium=…)` resolves
  the producer for the medium from the renderer registry and renders a greenlit `Shot`
  to real bytes — so both tiers share one path from a reconciled decision to output.
- **Split cleanly: judgment / schema / execution.** Decision-time needs only the
  *vocabulary*, so the agents are **not** wired into the Python heuristics. Open risk:
  the agents list enums by hand (vocab-drift) — a generated per-role *vocabulary card*
  from the enums would keep the code authoritative.

```mermaid
flowchart TB
    PROD["Producer — human (HITL)"]
    DIR["Director — conversational agent (orchestrator)"]
    subgraph B["Tier B · .github/agents/ · PersonaJudgment"]
        SCR["screenwriter.agent.md"]
        PDS["production_designer.agent.md"]
        CIN["cinematographer.agent.md"]
        GAF["gaffer.agent.md"]
        GRP["keygrip.agent.md"]
        EDT["editor.agent.md"]
        COL["colorist.agent.md"]
    end
    subgraph A["Tier A · sequitur/ · HeuristicJudgment + schema + execution"]
        ENUMS["crew/ enums — closed answer space"]
        HOOK["Director.execute → renderer_for(medium)"]
    end
    PROD -->|"brief · greenlight"| DIR
    DIR -->|"dispatch"| SCR & PDS & CIN & GAF & GRP & EDT & COL
    SCR & PDS & CIN & GAF & GRP & EDT & COL -->|"Contribution (enum-bound)"| DIR
    B -.->|"output bound to"| ENUMS
    DIR -->|"reconciled Shot"| HOOK
    HOOK -->|"real bytes"| OUT["video / still"]
```

## Open architectural decisions

- **How far to encode roles in code — DECIDED (`0008`); phase A STARTED (`0012`).**
  Roles are first-class behavior (`Role` + `Judgment`), the **Producer is the HITL
  seat**, the **Director** is the reconciling agent role, and the **Production (PM
  board)** is the container. See the crew-engine section above. **In progress:**
  `grammar.py` un-flattened into a `crew/` package (`0012`), `edit.py`'s vocabulary
  re-seated under an `Editor` role (`0013`), and the **behaviour** layer built
  (`0014`) — a swappable `Judgment` (`HeuristicJudgment` = deterministic A), a
  `Brief`/`Contribution` pair, a `Director` reconciler, and a dumb `Engine` that
  assembles a shoot-phase `Shot`. **Assemble-phase behaviour built (`0023`):**
  `Engine.assemble` + a phase-aware `Director.assemble` reconcile the `Editor` (cut) and
  `Colorist` (base grade) into a graded edit `Sequence`. **Persona tier realized
  (`0031`):** the crew's `PersonaJudgment` (B) is a set of VS Code custom agents in
  [`.github/agents/`](../.github/agents/) and the Director is the conversational agent;
  **decision→pixels closed (`0032`):** `Director.execute` renders a greenlit `Shot`
  through the renderer registry. **Plan + assemble agent seats now exist:** Screenwriter
  (`0035`), Production Designer (`0046`), Editor + Colorist (`0034`) — seven agents beside the
  Director. Next: a `StoryboardArtist` seat, a generated vocabulary card (drift), binding a
  local-folder Production in place of the bare `Brief`, a real cut-decision heuristic, and
  per-shot grade matching.
- **Build the provider seams — `ProductionProvider` DONE (`0025`).** A
  `runtime_checkable` protocol (`read_brief` / `write_sequence`) with live
  `AzureDevOpsProduction` + `LocalFolderProduction` backends, run board-to-board by
  `Engine.run_production` (`0027`) + [`scripts/produce.py`](../scripts/produce.py)
  (`0028`). The **`OutputStore`** is now **built** (`0038`, `LocalFolderOutputStore` over
  a OneDrive-synced root), wired to the render→persist hook (`0039`) and the **gate**
  (`0040`); remaining: a Graph-backed `OutputStore` backend, the board **verdict/State
  write** (link a deliverable `ref` + advance phase), scene-scoped reads, and per-shot
  grade matching. See
  [`storyline/0005`](storyline/0005-productions-as-instances-and-output-storage.md).
- **Production-store platform — RESOLVED: Azure DevOps (`0024`).** GitHub Projects v2
  vs. ADO settled on **ADO** for its native 4-level hierarchy (Act→Scene→Beat→Shot);
  the board is provisioned by a one-command template
  ([`scripts/provision_production.py`](../scripts/provision_production.py), `0026`) with
  departments as Team + Area-Path buckets and phases as named iterations (`0030`).
- **Build the sound layer (`0009`)** — `SpeechRenderer` first (Azure Speech on the
  existing AIServices account, no new resource; standard/HD
  neural voices are call-and-go, no deployment; CNV deferred). The
  `Renderer` protocol is now **formalized** (`0021`); still to do: ground the sound
  roles from the **abridged Rose** (`0010`), and wire **toaster-strudel** as sequitur's
  first MCP client (`Composer`/`SoundAnalyst`).
