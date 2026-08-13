# 0021 — Formalizing the Renderer Seam

> Date: 2026-08-12 · Focus: **code** — the second step of `0019`'s locked sequence.
> Turned the informal "every backend has a `render()`" convention into an explicit
> **`Renderer` protocol + medium-keyed registry** ([`render.py`](../../sequitur/render.py)),
> and retrofitted the four existing backends onto it. First code since `0014`.

## What happened

`0006` named the renderer seam but deferred a formal contract "until a third backend
justifies it." Four now exist — `Studio` (video), `ImageStudio` (still),
`SpeechRenderer` (voice), and `Cutter` (the edit executor) — and `0019`/`0020` locked
formalizing the protocol as the step **between** grounding color and building the
Colorist, precisely so the coming grade renderer has a seam to plug into rather than a
fifth bespoke class.

New module [`render.py`](../../sequitur/render.py):

- **`Medium`** — an enum keying the registry: `VIDEO` / `STILL` / `VOICE` / `FILM`
  (the assembled edit; a *transform* renderer, distinct from the three generative ones).
- **`RenderResult(raw, ref)`** — a `NamedTuple`. `raw` is the backend's native result
  object; `ref` locates the saved bytes (a local `Path` today, a URL once outputs live
  in a blob/SharePoint store — `0005`). Being a plain 2-tuple, every legacy
  `raw, ref = renderer.render(...)` unpacking keeps working unchanged.
- **`Renderer`** — a `runtime_checkable` `Protocol`: a `medium` attribute + a
  `render(decision, *, out_path=None) -> RenderResult` method. Structural, so a backend
  *satisfies* it without inheriting — no base-class coupling.
- **A lazy, medium-keyed registry** — `register(medium, factory)`,
  `renderer_for(medium) -> Renderer`, `registered_media()`. Factories are zero-arg and
  lazy, so importing the package never constructs an API client or needs credentials;
  the client cost is paid only when a render is actually requested.

## Decisions

1. **Structural protocol, not a base class.** The four backends are curated and already
   share a `render()` shape; a `runtime_checkable` `Protocol` lets them conform by shape
   (each just gains a `medium` class attribute) without an inheritance graph or an import
   cycle. This matches the studio's "closed, curated hierarchy" instinct while keeping
   `render.py` dependency-free.

2. **`RenderResult` is a tuple subclass — a non-breaking formalization.** The three
   generative backends already returned `(raw, path)`; wrapping that in a named 2-tuple
   documents the seam (`.raw` / `.ref`) while leaving every caller — the CLI's
   `_, path = ...render(...)` included — working verbatim. `Studio.edit()` returns the
   same shape.

3. **`Cutter` joins the protocol as the lone transform renderer.** Its `render()` now
   returns `RenderResult(film, path)` (was a bare `Path`) and its `out_path` became
   keyword-only to match the protocol — safe, as it had no callers yet. This makes the
   generative-vs-transform flavor distinction (from the `0019` audit) concrete in code:
   both flavors present one seam.

4. **Lazy factories over eager registration.** The registry maps a medium to a *factory*
   that imports and constructs its backend on demand. `render.py` therefore imports none
   of the backends at module load (no cycle: `studio.py` imports `render.py`, not the
   reverse), and `renderer_for(Medium.VIDEO)` only builds a `genai` client when you truly
   render video.

5. **The `GRADE` medium is intentionally *not* added yet.** The registry gains `GRADE`
   when the Colorist's grade renderer is built (`0019` step 3) — no speculative empty
   slot now.

## Resulting state

- **New:** [`sequitur/render.py`](../../sequitur/render.py) (the seam) and
  [`tests/test_render.py`](../../tests/test_render.py) (6 smoke tests: each backend's
  `medium`, the `RenderResult` pair, full-registry coverage, `renderer_for` builds +
  satisfies the protocol, registry override, and the unknown-medium error).
- **Retrofitted:** `studio.py` / `image.py` / `speech.py` / `cutter.py` each declare a
  `medium` and return `RenderResult`. Public surface (`__init__` `__all__`) adds
  `Renderer` · `Medium` · `RenderResult` · `renderer_for` · `register` ·
  `registered_media`; everything prior unchanged.
- **Green:** all four smoke suites pass (`test_prompt` 3 · `test_edit` 4 · `test_engine`
  4 · `test_render` 6 = 17); the CLI `--dry-run` composes unchanged. The retrofit is
  behaviour-neutral for existing callers.
- Docs reconciled: `architecture.md` (renderer-seam section + open-decisions list now
  say the protocol is built), `README.md` (layout tree + tests line).

## Open threads

- **Build the `Colorist` + grade renderer (`0019` step 3, next)** — a transform renderer
  (LUT/curve over rendered clips on the `Cutter`/ffmpeg plane) registered under a new
  `Medium.GRADE`; the Colorist owns the lift/gamma/gain primary + HSL/shape secondary
  grade vocabulary from the `0020` grounding, and reconciles the `ColorTemperature`
  two-seat overlap with the Gaffer.
- **Register the remaining backends** — `Composer`→toaster-strudel (score) and the
  non-generative `SoundAnalyst` (audio MIR sensor) once the sound roles are built.
- **Let roles *hold* their renderer** — wire `renderer_for(medium)` into the crew engine
  so a role reaches its execution plane through the registry instead of the CLI
  hard-wiring `Studio`; the deferred **non-generative data APIs** (reference/lookbook,
  palette lookup) also register here.
- Carried from `0019`/`0020`: the sound-mix renderer; a dedicated production-design
  source; wiring the assemble phase + seating the plan phase; the `0005` Production
  binding; `PersonaJudgment` (**B**); the reconciliation sweeps.
