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

Today the studio implements **one department in one phase** — the camera
department during production (the DP's grammar of the shot). Everything else is
scaffolded here as the intended architecture, so subsequent work has a frame to
grow into.

This doc maps **two orthogonal dimensions**: the **craft layers** (immediately
below — *what* the studio composes) and the **runtime model** (further down — *how*
a production is represented, driven, and stored, decided in
[`storyline/0005`](storyline/0005-productions-as-instances-and-output-storage.md)).

## The craft layers, by phase

### Pre-production — *plan*

| Department / role (App. D) | Responsibility | Grounding | Code layer | Status |
|---|---|---|---|---|
| Producer | financing, scheduling, logistics | — | **HITL — the human seat** (works the Production/PM board) | decided (`0008`) |
| Screenwriter | script, structure | *(story source — to acquire)* | `Script` / `Scene` model | planned |
| Director | interpret script → shot selection | Grammar of the Shot (Ch. 1) | shot planning | partial (`Shot`) |
| Production Designer | sets, costume, color concepts | *(design/color source)* | art/color layer · `ImageStudio` (gpt-image) | partial (image backend) |
| Assistant Director | schedule, coverage, shot list | Grammar of the Shot (Ch. 1) | shot list / coverage | planned |

### Production — *shoot*  ← **implemented today**

| Department / role | Responsibility | Grounding | Code layer | Status |
|---|---|---|---|---|
| Director · DP · Camera Operator · AC | the shot: framing, composition, angle | Grammar of the Shot (Ch. 1–3) | `ShotSize`, `SubjectView`, `CameraAngle`, `ShootingStyle`, `Composition`, `FocalLength`, `DepthOfField` | **implemented** |
| Gaffer · Electric · Lighting Tech | lighting scheme & quality | Grammar of the Shot (Ch. 4) | `LightQuality`, `LightScheme`, `LightDirection`, `ColorTemperature`, `eye_light` | **implemented** |
| Key Grip · Grip · Dolly Grip | camera support & movement | Grammar of the Shot (Ch. 6) | `CameraMovement`, `MotionSpeed` | **implemented** |
| Sound Mixer · Boom Operator | production sound (diegetic capture) | Grammar of the Edit Ch. 3 + **Rose, *Producing Great Sound*** *(staged)* | `SpeechRenderer` (Azure Speech) + `SoundMixer` role — planned (`0009`) | partial |
| Script Supervisor · DIT | continuity notes, data, on-set color | Grammar of the Shot (Ch. 5) | feeds the edit layer | planned |

### Post-production — *assemble*  ← **the next architectural layer**

| Department / role | Responsibility | Grounding | Code layer | Status |
|---|---|---|---|---|
| Editor | cut, continuity assembly, pacing, transitions | **Grammar of the Edit** (Ch. 1–8, abridged) + Grammar of the Shot Ch. 5 | **sequence / edit layer** (`edit.py` model + `cutter.py` executor) | grounded; code in progress |
| Colorist / DIT | grade, look | Grammar of the Shot (Ch. 4 color) + *(color source)* | color layer | partial (`ColorTemperature`) |
| Sound editor / mixer · Composer | sound design, score, mix | Grammar of the Edit Ch. 3 + **Rose** *(staged)* + **toaster-strudel MCP** (score) | `SpeechRenderer` (VO/ADR) · `Composer`→toaster-strudel · `SoundDesigner`/`ReRecordingMixer` — planned (`0009`) | planned |

### Delivery — *ship*

| Department / role | Responsibility | Grounding | Code layer | Status |
|---|---|---|---|---|
| Producer | marketing, distribution, exhibition | — | out of scope (for now) | — |

## Reading the map

- **Grammar of the Shot already spans the production phase** — camera, grip, and
  electric departments are encoded in `grammar.py`. That is the studio's current
  reach: it can compose a single, fully-grounded **shot**.
- **The next layer is editorial/post — now grounded.** Bowen's companion
  **Grammar of the Edit** has been imported and abridged (8 chapters +
  [INDEX](../artifacts/grammar%20of%20the%20edit/INDEX.md)), so the *sequence* layer
  (which assembles multiple `Shot`s honouring 180°/30°, matching/reverse, eye-line,
  and screen direction; see
  [Ch. 5](../artifacts/grammar%20of%20the%20shot/reference/ch05-shooting-for-editing.md))
  can now be built on real grounding. The post-layer model (`edit.py`) + its MoviePy
  executor (`cutter.py`) are scaffolded; the cut-decision engine is designed in [`storyline/0007`](storyline/0007-grounding-the-edit-layer.md) but not yet built.
- **Sound, story, and production design** are named departments with no dedicated
  source yet — placeholders in the grounding library. **Sound is now designed**
  (`0009`): a multi-phase department grounded by Grammar of the Edit Ch. 3 +
  **Rose, *Producing Great Sound*** *(staged)* + toaster-strudel MCP, with `SpeechRenderer` /
  `Composer` / `SoundAnalyst` capabilities.

## Runtime architecture — engine, instances, and stores

The tables above are the **craft dimension**: the layers of *what* the studio can
compose. Orthogonal to them is the **runtime dimension** — how an actual production
is represented, driven, and stored. Decided in
[`storyline/0005`](storyline/0005-productions-as-instances-and-output-storage.md);
not yet built.

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
  - `ProductionProvider` — `layer(name) → { seeds, guidance_refs, history, output_refs }`.
    First impl: a local folder (folder-per-layer = bucket-per-layer). Later: GitHub
    Projects v2 or ADO, chosen once a real production exists.
  - `OutputStore` — `put(production, layer, artifact) → ref`. Output **bytes** live
    in the **Sequitur Solutions** tenant's **SharePoint, via Microsoft Graph**
    (least-privilege Entra app; Azure Blob deferred). `ref` is a share URL
    registered back into the plan.

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
  departments whose deliverable isn't a model output. A formal `Renderer` protocol +
  medium-keyed registry is deferred until a *third* backend justifies it — the
  **sound layer** (`0009`) is that trigger: `SpeechRenderer` (Azure Speech) and
  `Composer`→Strudel are backends #3–#4, plus a non-generative `SoundAnalyst` (audio
  MIR) sensor.

- **Secrets via Key Vault.** Backend API keys are never stored in plaintext — they
  live in Azure Key Vault (`kv-sequitur484673472841`) and are fetched at runtime via
  `DefaultAzureCredential` (the `az login` identity authorises the vault read). Only
  non-secret pointers (vault name, endpoint, deployment) live in `.env`.
- **MCP** is the eventual **control-plane** connector: sequitur as MCP *client*, the
  production/output stores fronted by MCP *servers* — added once there is more than
  one of anything to route between. It is never the byte path for media. **First
  concrete case (`0009`):** [`toaster-strudel`](https://github.com/HarryJamesGreenblatt/toaster-strudel)
  is already an MCP server (Strudel knowledge + Song-IR assembler + audio MIR);
  sequitur becomes its client for the `Composer`/`SoundAnalyst` roles — keeping the
  AGPL-3.0 Strudel engine at arm's length behind toaster-strudel's MIT MCP layer.

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
- **Judgment is a swappable strategy (the A→B seam).** A role delegates reasoning to
  a **`Judgment`**: `HeuristicJudgment` (**A**, deterministic) · `PersonaJudgment`
  (**B**, an LLM persona over the role's *scoped* grounding) · `HumanJudgment`
  (**HITL**). Same `propose()` signature, so any one role can be upgraded — or hand-
  driven — individually.
- **Three authority tiers.**
  - **Producer = HITL (the user)** — owns *what/whether* (brief, greenlight,
    approval). This is the code analogue the Producer row lacked: **the human seat.**
  - **Director = agent** — owns *how*; a **`Role`** that reconciles the crew (agency
    lives in a component, never the container).
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

## Open architectural decisions

- **How far to encode roles in code — DECIDED (`0008`).** Roles are first-class
  behavior (`Role` + `Judgment`), the **Producer is the HITL seat**, the **Director**
  is the reconciling agent role, and the **Production (PM board)** is the container.
  See the crew-engine section above. Next: build phase A (heuristic roles over a
  local-folder Production), re-seating `grammar.py`/`edit.py` under their roles.
- **Build the post layer (`edit.py`)** — *Grammar of the Edit* is now grounded
  (`0007`); `edit.py` holds the EDL/grammar model and `cutter.py` the MoviePy
  executor. Build out the cut-decision engine (Ch. 5's six motivators) over a
  shots→scenes→acts model, cuts/fades first (no handles) then handle padding for
  dissolves. Then run the **reconciliation sweep** to align the edit references'
  "Studio application" leads to the real code.
- **Build the provider seams** — `ProductionProvider` + `OutputStore` with
  local-folder implementations first (no platform, no auth), then a Graph-backed
  `OutputStore`. See [`storyline/0005`](storyline/0005-productions-as-instances-and-output-storage.md).
- **Production-store platform** — GitHub Projects v2 vs. ADO for the plan; deferred
  until a first real production exists (the local-folder provider stands in). See
  [`storyline/0005`](storyline/0005-productions-as-instances-and-output-storage.md).
- **Build the sound layer (`0009`)** — `SpeechRenderer` first (Azure Speech on the
  existing `hjg-m8jtp7uy-eastus2` AIServices account, no new resource; standard/HD
  neural voices are call-and-go, no deployment; CNV deferred). Then formalize the
  `Renderer` protocol, abridge **Rose** *(staged; its own session)* to ground the sound roles, and wire
  **toaster-strudel** as sequitur's first MCP client (`Composer`/`SoundAnalyst`).
