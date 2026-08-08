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

## The layers, by phase

### Pre-production — *plan*

| Department / role (App. D) | Responsibility | Grounding | Code layer | Status |
|---|---|---|---|---|
| Producer | financing, scheduling, logistics | — | project/orchestration | planned |
| Screenwriter | script, structure | *(story source — to acquire)* | `Script` / `Scene` model | planned |
| Director | interpret script → shot selection | Grammar of the Shot (Ch. 1) | shot planning | partial (`Shot`) |
| Production Designer | sets, costume, color concepts | *(design/color source)* | art/color layer | planned |
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
| Editor | cut, continuity assembly, pacing, transitions | **Grammar of the Edit** (to acquire) + Grammar of the Shot Ch. 5 | **sequence / edit layer** | planned |
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
- **The clear next layer is editorial/post.** It needs its own grounding — Bowen's
  companion **Grammar of the Edit** — before the *sequence* layer (which assembles
  multiple `Shot`s honouring 180°/30°, matching/reverse, eye-line, and screen
  direction; see
  [Ch. 5](../artifacts/grammar%20of%20the%20shot/reference/ch05-shooting-for-editing.md))
  can be built well.
- **Sound, story, and production design** are named departments with no source yet
  — placeholders in the grounding library, to be imported as the studio grows.

## Open architectural decisions

- **How far to encode roles in code.** This doc encapsulates roles at the *design*
  level. A future step could make roles first-class (e.g. role-scoped prompt
  personas, or a `department`/`role` module) — worth doing only once a second
  department (editorial) exists to justify the abstraction.
- **Acquire *Grammar of the Edit*** — same pipeline as Grammar of the Shot
  (extraction → source → reference → index). This unlocks the post-production layer.
