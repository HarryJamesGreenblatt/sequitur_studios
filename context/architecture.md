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
| Producer | financing, scheduling, logistics | — | project/orchestration | planned |
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
| Sound Mixer · Boom Operator | production sound | *(sound source — to acquire)* | `Shot.audio` (free-text) | partial |
| Script Supervisor · DIT | continuity notes, data, on-set color | Grammar of the Shot (Ch. 5) | feeds the edit layer | planned |

### Post-production — *assemble*  ← **the next architectural layer**

| Department / role | Responsibility | Grounding | Code layer | Status |
|---|---|---|---|---|
| Editor | cut, continuity assembly, pacing, transitions | **Grammar of the Edit** (Ch. 1–8, abridged) + Grammar of the Shot Ch. 5 | **sequence / edit layer** (`movie.py`, planned) | grounded; code planned |
| Colorist / DIT | grade, look | Grammar of the Shot (Ch. 4 color) + *(color source)* | color layer | partial (`ColorTemperature`) |
| Sound editor / mixer | sound design, mix | *(sound source — to acquire)* | sound layer | planned |

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
  can now be built on real grounding. The post-layer code (`movie.py`) is designed
  in [`storyline/0007`](storyline/0007-grounding-the-edit-layer.md) but not yet built.
- **Sound, story, and production design** are named departments with no source yet
  — placeholders in the grounding library, to be imported as the studio grows.

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
  medium-keyed registry is deferred until a *third* backend justifies it.

- **Secrets via Key Vault.** Backend API keys are never stored in plaintext — they
  live in Azure Key Vault (`kv-sequitur484673472841`) and are fetched at runtime via
  `DefaultAzureCredential` (the `az login` identity authorises the vault read). Only
  non-secret pointers (vault name, endpoint, deployment) live in `.env`.
- **MCP** is the eventual **control-plane** connector: sequitur as MCP *client*, the
  production/output stores fronted by MCP *servers* — added once there is more than
  one of anything to route between. It is never the byte path for media.

## Open architectural decisions

- **How far to encode roles in code.** This doc encapsulates roles at the *design*
  level. A future step could make roles first-class (e.g. role-scoped prompt
  personas, or a `department`/`role` module) — worth doing only once a second
  department (editorial) exists to justify the abstraction.
- **Build the post layer (`movie.py`)** — *Grammar of the Edit* is now grounded
  (`0007`); build the cut-decision engine (Ch. 5's six motivators) over a
  shots→scenes→acts model, cuts/fades first (no handles) then handle padding for
  dissolves. Then run the **reconciliation sweep** to align the edit references'
  "Studio application" leads to the real code.
- **Build the provider seams** — `ProductionProvider` + `OutputStore` with
  local-folder implementations first (no platform, no auth), then a Graph-backed
  `OutputStore`. See [`storyline/0005`](storyline/0005-productions-as-instances-and-output-storage.md).
- **Production-store platform** — GitHub Projects v2 vs. ADO for the plan; deferred
  until a first real production exists (the local-folder provider stands in). See
  [`storyline/0005`](storyline/0005-productions-as-instances-and-output-storage.md).
